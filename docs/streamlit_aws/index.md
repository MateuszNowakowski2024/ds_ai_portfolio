---
comments: true
---

# Setting Up Multiple Streamlit Apps on a Single EC2 Instance Free for 12 mths


This guide will walk you through setting up an AWS EC2 Linux instance to host multiple Streamlit applications. We'll cover necessary tools, their purposes, and how to install and configure software to run multiple apps concurrently using Nginx, Tmux, Vim, Certbot, and Git. Additionally, you'll learn how to clone your application repositories from GitHub using a personal access token.

## Introduction to Tools and Concepts

### $0 Cost for 12 Months Challenge Limitations

The idea of this guide is to set up multiple apps and/or static websites on a single EC2 instance while staying within the AWS free tier, thereby incurring $0 for the first year. As of February 2024, AWS charges $0.005 per hour for every public IP assigned to a resource. We only get one public IP within the free tier. If we start another AWS resource that faces the internet (e.g., a second EC2 instance, database, or load balancer), we will be charged $0.005 per hour for each one.

To fit within the $0 rule, we can't use Route 53 to host our domain. Route 53 also costs $0.50 per month. There are also charges per every 1 million packets transferred. We can't use AWS Certificate Manager even though it's free, as it requires an AWS load balancer. According to their policy, the load balancer must have at least two availability zones assigned, which means it will have two public IP addresses assigned and will incur charges.

We will have to use a domain registrar that provides free DNS services. Additionally, we will use a free SSL certificate provider like Let's Encrypt.


### Amazon EC2 Instance

**What is an EC2 Instance?**

Amazon Elastic Compute Cloud (EC2) is a web service that provides resizable compute capacity in the cloud. An EC2 instance is a virtual server that runs applications and services.
I choose Amazon Linux 2023 as the operating system for this guide. It's a free, stable, and optimized Linux distribution provided by AWS. A lot of the commands in this guide are specific to Amazon Linux 2023. If you are using a different distribution, you may need to adjust the commands accordingly.

**Why are we using it?**

It provides a flexible, scalable, and cost-effective way to host web applications, like multiple Streamlit apps, without needing to manage physical hardware.

### Nginx

**What is Nginx?**

Nginx (pronounced "Engine-X") is a high-performance web server and reverse proxy server.

**Why are we using it?**

- **Reverse Proxy:** Nginx forwards incoming web requests from your domain to the correct Streamlit app running on a specific port.
- **Load Balancing & Security:** It handles traffic efficiently, provides load balancing, and can enforce HTTPS for secure communication.

### Tmux

**What is Tmux?**

Tmux is a terminal multiplexer that allows you to manage multiple terminal sessions in one window.

**Why do we need it?**

- **Manage Multiple Apps:** Run each Streamlit app in its own Tmux session so they operate independently.
- **Persistence:** Sessions can continue running in the background even after disconnecting, allowing apps to keep running without an active SSH connection.

### Vim

**What is Vim?**

Vim is a powerful text editor used within the terminal.

**What are we using it for?**

Editing Configuration Files: We use Vim to edit configuration files (e.g., Nginx settings, startup scripts) directly on the server.

### Certbot

**What is Certbot?**

Certbot is an automated tool for obtaining and installing SSL/TLS certificates from Let's Encrypt.

**Why are we using it?**

- **HTTPS Setup:** Certbot simplifies the process of configuring HTTPS for your domains, ensuring secure communication between users and your server.
- **Automation:** It automatically handles certificate renewal, reducing manual maintenance.

### Git

**What is Git?**

Git is a distributed version control system that helps track changes in source code during software development.

**Why are we using it?**

- **Cloning Repositories:** We'll use Git to clone our Streamlit application code from GitHub to the EC2 instance.
- **Personal Access Token:** Since GitHub no longer supports password authentication, a personal access token is required for accessing private repositories.


## 1. Launching and Connecting to an EC2 Instance

### Step 1.1: Launch an EC2 Instance

This is only a short overview. There is virtually a ton of content on how to launch an ec2 on YouTube and Medium etc. Start here [AWS documentation](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EC2_GetStarted.html).

- **Log in to AWS Console:** Go to the EC2 Dashboard and click "Launch Instance".
- **Configure the Instance:**
    - **AMI:** Select Amazon Linux 2023.
    - **Instance Type:** Choose t2.micro (free tier-eligible) or another type based on your needs.
    - **Key Pair:** Select an existing key pair or create a new one. This *.pem file is needed for SSH access.
    - **Security Group:** Ensure the following ports are open:
        - 22 (SSH)
        - 80 (HTTP)
        - 443 (HTTPS)
- **Launch Instance:** Confirm the settings and launch the instance.

### Step 1.2: Connect to Your Instance

- Find your instance's Public IPv4 address in the AWS Console.
- Open your terminal and connect via SSH:

```bash
ssh -i /path/to/your_key.pem ec2-user@your_instance_ip
```

Replace `/path/to/your_key.pem` with your key's path. Replace `your_instance_ip` with the instance’s public IP.

## 2. System Update and Software Installation

### Step 2.1: Update Your System

Run the following command to update package lists and software:

```bash
sudo dnf update -y
```

### Step 2.2: Install Python 3.11 and pip

- **Install Python 3.11:**

```bash
sudo dnf install -y python3.11 python3.11-devel
```

- **Install or upgrade pip:**

```bash
python3.11 -m ensurepip --upgrade
```

- **Verify installation:**

```bash
python3.11 --version
pip3.11 --version
```

### Step 2.3: Install Git and Tmux

- **Install Git:**

```bash
sudo dnf install -y git
```

- **Install Tmux:**

```bash
sudo dnf install -y tmux
```

### Step 2.4: Install and Start Nginx

- **Enable Nginx repository:**

```bash
sudo amazon-linux-extras enable nginx1
```
- If this command fails that means you can skip this step and go to the next one.

- **Install Nginx:**

```bash
sudo dnf install -y nginx
```

- **Start and enable Nginx:**

```bash
sudo systemctl start nginx
sudo systemctl enable nginx
```

## 3. Nginx Setup for Multiple Domains

### Step 3.1: Update DNS Settings

For each domain (e.g., example.com, example2.com):

- Log in to your domain registrar.
- Create an A record pointing your domain to the EC2 instance’s public IP.

- Refer to your registrar's documentation for specific instructions on updating DNS settings.

### Step 3.2: (Optional) Set Up HTTPS with Certbot

- Do you need SSL? If you want to use your app "internally," you can skip this step. However, without a certificate, you won't be able to add features like login with Google or payment gateways.
- You are not required to use Certbot; you can obtain a certificate from any other provider. Refer to their documentation on how to install it on your server. However, Certbot is free and automates the process of obtaining and installing SSL certificates from Let's Encrypt.

- **Install Certbot:**

```bash
sudo dnf install -y certbot python3-certbot-nginx
```

- **Obtain and install SSL certificates for each domain:**

```bash
sudo certbot --nginx -d example.com -d www.example.com
sudo certbot --nginx -d example2.com -d www.example2.com
```

    Follow prompts to configure and automate certificate renewal.

### Step 3.3: Configure Nginx as a Reverse Proxy

- Open a new Nginx configuration file:

```bash
sudo vim /etc/nginx/conf.d/streamlit.conf
```
We create a separate configuration file to keep the main Nginx configuration clean. You can name it anything you like. I chose `streamlit.conf`.
Use vim to edit the file. If you are not familiar with vim you can use nano or any other text editor. i to insert text, esc to exit insert mode, :wq to save and exit.

- Add configuration blocks for each domain:

```nginx
# Domain 1: example.com
server {
        listen 80;
        server_name example.com www.example.com;
        return 301 https://$host$request_uri;
}

server {
        listen 443 ssl;
        server_name example.com www.example.com;

        ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

        location / {
                proxy_pass http://127.0.0.1:8501;
                proxy_http_version 1.1;
                proxy_set_header Upgrade $http_upgrade;
                proxy_set_header Connection "upgrade";
                proxy_set_header Host $host;
                proxy_cache_bypass $http_upgrade;
        }
}

# Domain 2: example2.com
server {
        listen 80;
        server_name example2.com www.example2.com;
        return 301 https://$host$request_uri;
}

server {
        listen 443 ssl;
        server_name example2.com www.example2.com;

        ssl_certificate /etc/letsencrypt/live/example2.com/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/example2.com/privkey.pem;

        location / {
                proxy_pass http://127.0.0.1:8502;
                proxy_http_version 1.1;
                proxy_set_header Upgrade $http_upgrade;
                proxy_set_header Connection "upgrade";
                proxy_set_header Host $host;
                proxy_cache_bypass $http_upgrade;
        }
}
```

Replace `example.com` and `example2.com` with your actual domain names. Configure paths for SSL certificates when Certbot generates them.

- Save and exit Vim: Press `Esc`, type `:wq`, and press `Enter`.

- If you used certbot then most of the script should be generated for you. You can check the configuration file at `/etc/nginx/conf.d/your_domain.conf` and make sure that the configuration is correct.

- Test and reload Nginx configuration:

```bash
sudo nginx -t
sudo systemctl reload nginx
```


## 4. Running Multiple Streamlit Apps with Tmux

### Step 4.1: Virtual Environment

**Do you need a virtual environment?**

Setting up a virtual environment on your EC2 instance introduces minimal overhead and is highly recommended for managing Python dependencies effectively, especially in multi-version scenarios. Here's a detailed comparison of the two approaches to help you decide:

**Option 1: Use Virtual Environments**

**Pros:**
- **Dependency Isolation:** Virtual environments isolate dependencies for your Streamlit app, preventing conflicts with system-level packages or other projects.
- **Clean Environment:** You can install libraries and tools specific to your app without cluttering the global Python environment.
- **Portability:** If you need to replicate your environment on another instance, you can use the `requirements.txt` file to easily reinstall dependencies.
- **Best Practice:** Using virtual environments is considered a best practice in Python development.

**Cons:**
- **Minimal Overhead:** While virtual environments consume some disk space (mainly for copied binaries and installed packages), this is generally negligible on modern EC2 instances.
- **Setup Steps:** You need to create and activate the virtual environment before running your app, which adds a step to your workflow.

**Option 2: Use Global Python Installation**

**Pros:**
- **Simplicity:** You directly use `python3.11` without additional setup for virtual environments.
- **Less Disk Usage:** No duplicate copies of the Python binary or libraries are created.

**Cons:**
- **Risk of Conflicts:** Installing dependencies globally may cause conflicts with system Python packages or dependencies for other projects.
- **System Stability:** There is a small risk of inadvertently installing or upgrading packages that affect system scripts or tools.
- **Difficulty in Maintenance:** Managing dependencies globally can lead to a cluttered environment and challenges during upgrades or migrations.

**Recommendation**

For most Streamlit app setups, using a virtual environment is the better choice, even on a lightweight EC2 instance. Here's why:
- The overhead of a virtual environment is negligible compared to the benefits of dependency isolation.
- It prevents issues that may arise from global installations, such as version conflicts or unintended system changes.
- It aligns with Python best practices, making your app more robust and easier to manage.

If simplicity is your priority and you are confident the global installation won't cause conflicts (e.g., it's a dedicated EC2 instance for a single project), you can skip the virtual environment. However, this approach is less flexible and more error-prone in the long run.

If you choose to use a virtual environment, follow the steps below to set it up for your Streamlit apps.

**Recommended Folder Structure**

```bash
/main_project_folder
├── venv/                 # Shared virtual environment
├── app1/                 # Subfolder for App 1
│   ├── app1_code/        # Cloned Git repo for App 1
│   │   ├── app.py
│   │   ├── requirements.txt
│   ├── static/           # Optional: App-specific static files
├── app2/                 # Subfolder for App 2
│   ├── app2_code/        # Cloned Git repo for App 2
│   │   ├── app.py
│   │   ├── requirements.txt
│   ├── data/             # Optional: App-specific data
```

### Step 4.2: Step-by-Step Setup

1. **Create the Main Folder**

    Create a folder to hold everything:

```bash
mkdir ~/main_project_folder
cd ~/main_project_folder
```

2. **Set Up the Shared Virtual Environment**

    Create a single virtual environment in the main folder:

```bash
python3.11 -m venv venv
```

    Activate the virtual environment:

```bash
source venv/bin/activate
```

### Step 4.3: Prepare Your Streamlit Apps

Before starting your apps, you'll need to have the source code on the EC2 instance. If your code is hosted on GitHub, you can clone your repositories directly onto the server.

#### Cloning Repositories from GitHub

- **Create a Personal Access Token on GitHub:**
    - Log into GitHub.
    - Go to Settings > Developer settings > Personal access tokens.
    - Generate a new token with appropriate scopes (e.g., repo for private repositories).
    - Save this token securely; you'll need it for cloning.

- **Clone Your Repositories:**

For a public repository, you can simply run:

```bash
git clone https://github.com/your_username/your_repo.git ~/app1
```

For a private repository or if prompted for authentication, use your personal access token as the password:

```bash
git clone https://github.com/your_username/your_private_repo.git ~/app1
```

When asked for a password, paste your personal access token instead of your GitHub password.

- **Repeat for Additional Apps:**

```bash
git clone https://github.com/your_username/another_repo.git ~/app2
```

Use the token for authentication if required.

Now you should have your application code in directories like `~/main_project_folder/app1` and `~/main_project_folder/app2`.

3. **Install Dependencies**

While the virtual environment is active, navigate to each app's folder and install its dependencies:

For App 1:

```bash
cd ~/main_project_folder/app1/app1_code
pip install -r requirements.txt
```

For App 2:

```bash
cd ~/main_project_folder/app2/app2_code
pip install -r requirements.txt
```

Since you're using a shared virtual environment, the dependencies of both apps will be installed together.

4. **Add .gitignore**

To keep the repositories clean, exclude the `venv/` folder from being tracked by Git. Add the following line to the `.gitignore` file of each repository:

```bash
../venv/
```

### Step 4.4: Environment Variables

You have three options to set the environment variables. You can simply upload a `.env` file (or `secrets.toml`) to the server - not recommended but it's easy. You can store your variables in AWS Parameter Store - a free option although not as secure. Finally, if you would like to be 100% professional, you can store your variables in AWS Secrets Manager, which is fully secure but will cost you a few cents a month depending on the number of variables you store and how often you access them.
I put detailed instructions on how to save variables in AWS Parameter Store and how to dynamically pass them to the app in my other article [here](../par_store/index.md).

### Step 4.5: Start a Tmux Session for Each App

#### For the First App:

1. **Create and attach to a Tmux session:**

```bash
tmux new -s streamlit-app1
```

2. **Navigate to the app directory:**

```bash
cd ~/main_project_folder/app1/app1_code
```

3. **(Optional) Activate a virtual environment if needed:**

```bash
source venv/bin/activate
```

4. **Run the Streamlit app on port 8501:**

```bash
streamlit run app.py --server.port 8501
```

5. **Detach from Tmux session:**

    Press `Ctrl+B`, release, then press `D`.

#### For the Second App:

1. **Create another Tmux session:**

```bash
tmux new -s streamlit-app2
```

2. **Navigate to the second app's directory:**

```bash
cd ~/main_project_folder/app2/app2_code
```

3. **(Optional) Activate its virtual environment if applicable:**

```bash
source venv/bin/activate
```

4. **Run the second Streamlit app on port 8502:**

```bash
streamlit run app.py --server.port 8502
```

5. **Detach from this Tmux session:**

    Press `Ctrl+B`, release, then press `D`.

Note: For additional Streamlit apps, repeat the Tmux session setup on different ports.

## 5. Adding database

If you require a database to store login data for your app, I've made a separate article on how to set up a free database on AWS. You can find it [here](../database_aws/index.md).

## 6. Automating Startup on Reboot (Optional)

To ensure your apps start automatically after a reboot:

### Step 6.1: Create a Startup Script

- **Create a script file:**

```bash
vim ~/start_streamlit_apps.sh
```

- **Add the following content:**

```bash
#!/bin/bash

# Start first app
tmux new -d -s streamlit-app1 "cd ~/app1 && streamlit run app.py --server.port 8501"

# Start second app
tmux new -d -s streamlit-app2 "cd ~/app2 && streamlit run app.py --server.port 8502"
```

Adjust paths and ports according to your setup.

- **Save and exit:**

    Press `Esc`, type `:wq`, then press `Enter`.

- **Make the script executable:**

```bash
chmod +x ~/start_streamlit_apps.sh
```

### Step 6.2: Configure Crontab to Run Script at Boot

- **Edit crontab:**

```bash
crontab -e
```

- **Add this line at the end to run the script on reboot:**

```bash
@reboot /home/ec2-user/start_streamlit_apps.sh
```

Save and exit the editor.

Now, when your server reboots, the script will automatically start your Streamlit apps in separate Tmux sessions.

## 7. Summary of Commands

### System Update:

```bash
sudo dnf update -y
```

### Install Dependencies:

```bash
sudo dnf install -y python3.11 python3.11-devel git tmux nginx
```

### Manage Tmux Sessions:

- **Start new session:**

```bash
tmux new -s session_name
```

- **Detach session:** Press `Ctrl+B`, then `D`

- **List sessions:**

```bash
tmux ls
```

### Run a Streamlit App in Tmux:

```bash
tmux new -d -s session_name "cd /path/to/app && streamlit run app.py --server.port PORT_NUMBER"
```

### Nginx Check and Reload:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

### Certbot for SSL:

```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

### Clone a Repository Using a Personal Access Token:

```bash
git clone https://github.com/your_username/your_repo.git ~/app_directory
```

    When prompted for a password, use your GitHub personal access token.

### Automate Startup:

Create `~/start_streamlit_apps.sh`, set up crontab with:

```bash
@reboot /home/ec2-user/start_streamlit_apps.sh
```

## 8: Conclusion

To access your app, simply type your domain name into your browser. If you encounter any issues, you can check the logs located at `/var/log/nginx/error.log` or `/var/log/nginx/access.log`. Your app should now be up and running. Ensure that when you type `http`, you are redirected to `https`. Similarly, typing `www.yourdomain.com` should redirect you to your app. If you have any questions or need further assistance, feel free to ask in the comments below.
