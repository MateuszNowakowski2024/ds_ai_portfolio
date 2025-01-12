---
comments: true
---

# How to Securely Retrieve Environment Variables from AWS Systems Manager Parameter Store

Below is a step-by-step guide on how to securely retrieve environment variables from AWS Systems Manager Parameter Store and use them in a Python (Streamlit) application. This includes:

- Storing parameters in Parameter Store
- Assigning an IAM role with correct policies
- Creating a Python script (`fetch_secrets.py`) to retrieve secrets
- Integrating secrets into your main application so it can read environment variables

## 1. Store Your Secrets in AWS Parameter Store

1. Log in to your AWS Console and open Systems Manager.
2. In the left menu, under Application Management, select **Parameter Store**.
3. Click **Create parameter**.
4. Enter the **Name** (e.g., `/myapp/OPENAI_API_KEY`) and choose **Type = SecureString** if it’s a sensitive secret.
5. Provide your **Value** (e.g., the actual OpenAI API key).
6. Click **Create parameter**.
7. Repeat these steps for each secret you need (e.g., `LANGFUSE_SECRET_KEY`, `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_HOST`, etc.):

```

    /myapp/LANGFUSE_SECRET_KEY
    /myapp/LANGFUSE_PUBLIC_KEY
    /myapp/LANGFUSE_HOST
    /myapp/OPENAI_API_KEY

```

**Note:** The prefix `/myapp/` is arbitrary; you can use `/example/` or any naming convention you prefer. It’s just a way to group your parameters. You can gruop them by application, environment, or any other logical grouping.

## 2. Set Up IAM Role with SSM Read Permissions

If you’re running on EC2 or ECS, you should attach an IAM role that allows reading from SSM Parameter Store. Here’s how:

1. Go to the IAM console and create or select a role assigned to your EC2/ECS.
2. Attach an inline policy or a separate policy JSON that includes something like this:

```json

    {
        "Version": "2012-10-17",
        "Statement": [
        {
            "Effect": "Allow",
            "Action": "ssm:GetParameter",
            "Resource": [
            "arn:aws:ssm:REGION:ACCOUNT_ID:parameter/myapp/*"
            ]
        }
        ]
    }

```

Replace `REGION` and `ACCOUNT_ID` with your actual AWS region (e.g., `eu-central-1`) and AWS account ID (e.g., `123456789012`).
Adjust the parameter resource to match your naming (`myapp`).

3. Save the policy and ensure the role is attached to the instance or service that will run your application.

If you need help with IAM roles, refer to the AWS documentation on [IAM roles](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html).

## 3. Create a Script to Fetch Secrets and Set Environment Variables

In your project folder, make a file called `fetch_secrets.py`. This Python script will:

- Retrieve each parameter from AWS SSM.
- Set them as environment variables (in memory).
- Then run your Streamlit (or other) application as a subprocess so that these environment variables carry over.

```python
import boto3
import os
import subprocess

def fetch_secrets_to_env(parameter_mapping, region="eu-central-1"):
    """
    Fetches parameters from AWS Parameter Store (SSM) and sets them as environment variables.
    :param parameter_mapping: A dict mapping from 'parameter_name_in_ssm' -> 'ENV_VARIABLE_NAME'
    :param region: AWS region where SSM parameters are stored
    """
    ssm = boto3.client("ssm", region_name=region)

    for param_name, env_var in parameter_mapping.items():
        try:
            response = ssm.get_parameter(Name=param_name, WithDecryption=True)
            value = response["Parameter"]["Value"]
            os.environ[env_var] = value
            print(f"Loaded secret for {env_var}.")
        except Exception as e:
            print(f"Failed to fetch [{param_name}] for env var [{env_var}]: {str(e)}")

if __name__ == "__main__":
    # Define the mapping from SSM parameter names to environment variable names
    parameter_mapping = {
        "/myapp/LANGFUSE_SECRET_KEY": "LANGFUSE_SECRET_KEY",
        "/myapp/LANGFUSE_PUBLIC_KEY": "LANGFUSE_PUBLIC_KEY",
        "/myapp/LANGFUSE_HOST":       "LANGFUSE_HOST",
        "/myapp/OPENAI_API_KEY":      "OPENAI_API_KEY"
    }

    # 1. Fetch secrets and set them as environment variables
    fetch_secrets_to_env(parameter_mapping, region="eu-central-1")

    # 2. Now run your main Python application (Streamlit) as a subprocess
    #    Inherits environment variables
    subprocess.run([
        "streamlit",
        "run",
        "app.py",
        "--server.port", "8501"
    ])
```

- Replace the `parameter_mapping` dictionary with your actual parameter names and the environment variable names you want to use in your application.
- Replace `region="eu-central-1"` with your actual AWS region.

**Important Details:**

- `WithDecryption=True` ensures if the parameter is stored as a `SecureString`, it returns the decrypted value.
- By calling `subprocess.run([...])` after setting `os.environ[...]`, the child process (Streamlit) inherits those environment variables. This ensures your secrets are available in `app.py`.

## 4. Update Your Main Application to Use Environment Variables

In your `app.py` (the Streamlit or Python application), retrieve the environment variables:

```python
import os
import streamlit as st

# Example usage:
openai_api_key = os.getenv("OPENAI_API_KEY")
langfuse_secret = os.getenv("LANGFUSE_SECRET_KEY")
langfuse_public = os.getenv("LANGFUSE_PUBLIC_KEY")
langfuse_host   = os.getenv("LANGFUSE_HOST")

# Then pass these variables to your code that needs them.
if not openai_api_key:
    st.error("No OpenAI API key found! Ensure fetch_secrets.py set it in the environment.")

# Rest of your app...
st.write("If you see no error, environment variables are loaded!")
```

You do not need to handle the environment variables in a separate shell script or `.env` file because `fetch_secrets.py` does that for you in memory.

## 5. Run the Entire Flow

1. SSH into your instance (or ensure you have your container set up).
2. Make sure you have the correct IAM role attached (Section 2).
3. Install dependencies for your Python environment, including `boto3`, `streamlit`, etc.:

```bash
    pip install boto3 streamlit
```

4. Run your `fetch_secrets.py`:

```bash
    python3 fetch_secrets.py
```

This script will:
- Connect to SSM and fetch secrets, printing “Loaded secret for ...” if successful.
- Launch `streamlit run app.py --server.port 8501`.

5. Check your console output. If everything is correct, you’ll see logs indicating secrets were loaded, then Streamlit logs.

## 6. Optional: Create a `startup.sh` (Alternative Approach)

If you want a shell script for convenience, you can create a simple `startup.sh` like this:

```bash
#!/bin/bash
cd "$(dirname "$0")"

# Just run the Python script (it handles secrets and launching the app)
python3 fetch_secrets.py
```

Make it executable:

```bash
chmod +x startup.sh
```

Then run:

```bash
./startup.sh
```

But note that all the real logic is in `fetch_secrets.py`—the shell script is just a helper.

## 7. Summary

- Store secrets in Parameter Store (SSM).
- Attach an IAM role with `ssm:GetParameter` permission to your instance (EC2/ECS).
- Write a `fetch_secrets.py` script that:
  - Uses `boto3` to fetch secrets.
  - Sets environment variables using `os.environ`.
  - Spawns Streamlit (or your Python app) with `subprocess.run([...])`.
- In your main `app.py`, call `os.getenv(...)` to access secrets.

This ensures your secrets remain securely in Parameter Store and never saved in plaintext on disk or in `.env` or `secrets.toml`. Your app dynamically loads them at runtime, in memory, using the correct IAM permissions.