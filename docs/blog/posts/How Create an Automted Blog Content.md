---
date:
  created: 2024-12-12
tags: [Manual, Guide]
---

# How to Create an AI-powered Automated Blog

Ok. So this is where the fun part begins. I am going to show you how to create an automated blog content pipeline using AI tools and services. This pipeline will generate blog posts, format them, and publish them on your website without any manual intervention. It utilizes GPT-4o-mini, Python, and GitHub Actions to create an end-to-end automated blog content pipeline.
<!-- more -->

## Stuff you need to know before we start

Before we start I recommend you read the previous blog post on [how to add a blog section](https://mateusznowakowski2024.github.io/ds_ai_portfolio/blog/2024/12/12/how-to-add-a-blog-section-to-mkdocs-portfolio/). This guide assumes you have some basic knowledge of Python, Git, and GitHub Actions. For those who are new to this, here is a short explanation of terms used in this guide:

### GitHub Actions

GitHub Actions is a tool provided by GitHub for automating tasks such as CI/CD pipelines. It allows you to create, manage, and execute workflows directly in your GitHub repository.

### CI/CD Pipeline 

CI/CD stands for Continuous Integration/Continuous Deployment. It is an automated process that:

- **CI (Continuous Integration)**: Automatically builds, tests, and integrates code changes.
- **CD (Continuous Deployment/Delivery)**: Automatically deploys code to production or staging environments.

### GitHub Workflow

A GitHub Workflow is a YAML file that defines a series of automated steps (jobs). Workflows are triggered by events such as code pushes, pull requests, or scheduled times. These files are stored in the `.github/workflows/` directory.

### GitHub Runner

A GitHub Runner is a server or environment that executes the tasks in a GitHub workflow. There are two types of runners:
- **GitHub-hosted runners**: Provided by GitHub (e.g., Ubuntu, Windows, macOS machines).
- **Self-hosted runners**: You can set up your own servers to run workflows.

### YAML File

A YAML file is a configuration file format used to define workflows in GitHub Actions. The syntax is clean and structured, using key-value pairs and lists.

#### Example

```yaml
name: CI Workflow
on: [push]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: npm test
```
### Personal Access Token (PAT)

A GitHub Personal Access Token (PAT) is a secure way to authenticate and access GitHub resources without using your password. It's commonly used for automation, scripts, and tools requiring GitHub access.

#### How to Create a PAT

1. **Log in to GitHub**
  - Go to [GitHub](https://github.com)

2. **Access Settings**
  - Click your profile picture (top-right)
  - Select "Settings"

3. **Developer Settings**
  - Scroll down to "Developer settings" in left sidebar

4. **Generate Token**
  - Select "Personal access tokens" → "Tokens (classic)"
  - Click "Generate new token"
  - Set expiration date (recommended)

5. **Configure Scopes**
  Select required permissions:
  - `repo`: Repository access
  - `workflow`: GitHub Actions access
  - `write:packages`: Packages access
  - Other scopes as needed

6. **Create and Save**
  - Click "Generate token"
  - Copy token immediately (it won't be shown again)

### Summary
- **Ci/CD Pipeline**: The automated process of building, testing, and deploying code.
- **GitHub Actions**: The tool for automation.
- **GitHub Workflow**: The automation steps defined in a YAML file.
- **GitHub Runner**: The environment where workflows run.
- **YAML File**: The format used to define workflows.
- **Personal Access Token (PAT)**: A secure way to access GitHub resources.

The guide is in the form of a conversation with GPT Model-o1, where I ask questions and the model provides responses. The model's responses are generated based on my input.

## Prompt #1

**Persona**: You are an experienced website designer and AI specialist.

**Problem**: I want to automate the process of creating blog content for your website.

**Objectives**:

- Automated Content Generation: Generate high-quality blog posts on Data Science and AI topics without manual intervention.
- Scheduling: Ensure posts are created and published once a week.
- Integration with MkDocs: Automatically add generated posts to your MkDocs blog.
- Deployment: Build and deploy the updated site automatically.
- Monitoring & Maintenance: Implement logging and alerting for failures.

**Key Components**:

- Content Generation Module: Uses AI (e.g., OpenAI's GPT) to create blog posts.
- File Management Module: Creates Markdown (.md) files with proper metadata.
- Scheduling System: Triggers the content generation and deployment process weekly.
- Deployment Pipeline: Builds the MkDocs site and deploys it to a hosting platform.
- Hosting Service: Hosts your MkDocs site (e.g., GitHub Pages, Netlify).
- Version Control: Manages your blog's source code and content (e.g., GitHub).
- Environment & Security: Handles API keys and sensitive information securely.



## Response #1

## Overview

The idea is to have a pipeline that, on a weekly schedule, will:

- Generate a blog post via an AI model like OpenAI’s GPT.
- Convert the generated text into a properly formatted Markdown file.
- Add metadata and structure the file for MkDocs’ blog plugin.
- Commit and push the changes to a remote Git repository.
- Build and deploy the MkDocs site to a hosting platform (e.g., GitHub Pages).
- Provide monitoring/logging to ensure the process runs smoothly and errors are notified.

## Step-by-Step Implementation Plan

### Step 1: Set Up Your Basic Environment

**Actions:**

1. **Install Python:**
  Make sure you have Python 3.8+ installed.

  ```bash
  python --version
  ```

2. **Install MkDocs and Material Theme:**

  ```bash
  pip install mkdocs mkdocs-material
  ```

3. **Initialize MkDocs Project:**

  ```bash
  mkdocs new my-automated-blog
  cd my-automated-blog
  ```

4. **Set Up Blog Plugin:**
  In your `mkdocs.yml`, add the blog plugin configuration:

  ```yaml
  site_name: My Automated AI Blog
  theme:
    name: material

  plugins:
    - search
    - blog
  ```

  After a first run (`mkdocs serve`), the plugin creates a `docs/blog/posts` directory.

5. **Version Control:**
  Initialize a Git repository and push to GitHub (or GitLab, etc.):

```bash
  git init
  git add .
  git commit -m "Initial commit"
  git remote add origin https://github.com/yourusername/my-automated-blog.git
  git push -u origin main
```
  **Result:**
  You have a basic MkDocs site with a blog plugin ready and a Git repository to track changes.

  ### Step 2: Integrate AI Content Generation

  **Objective:** Use an AI model like OpenAI’s GPT to create a blog post about Data Science and AI once a week.

  **Actions:**

  1. **Obtain API Access:**
    Sign up at OpenAI and get an API key.

  2. **Install OpenAI Python SDK:**

    ```bash
    pip install openai PyYAML
    ```

  3. **Create a Content Generation Script:**

    Create `generate_post.py` in your project root:

  ```python

    import openai
    import os
    import yaml
    from datetime import datetime
    import re
    # Set your OpenAI API key from environment variable
    openai.api_key = os.getenv("OPENAI_API_KEY")

    def generate_blog_post():
        prompt = (
            "Write a detailed blog post about a recent advancement in Data Science or AI. "
            "The post should be informative, technical yet understandable, with headings, an introduction, and a conclusion. "
            "Aim for roughly 300 words. Include references to known techniques or research. Avoid repetition."
            "Make the post more casual and less academic language"
          )

          response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
              {"role": "system", "content": "You are an talented aspiring data scientist and AI enthusist."},
              {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.7,
          )

          return response.choices[0].message.content.strip()

        def extract_title_and_insert_excerpt(content):
          """
          Extracts the title from the content and inserts an excerpt marker (`<!-- more -->`)
          after the first paragraph block or after ensuring at least 8 lines of text are visible.

          Parameters:
            content (str): The blog post content in markdown format.

          Returns:
            tuple: A tuple containing the extracted title and the modified content.
          """
          # Split the content into lines for easier manipulation
          lines = content.split("\n")
          
          # Extract the first heading as the title
          title_line = next((l for l in lines if l.startswith("# ")), "# Recent AI Advancements")
          title = title_line.replace("# ", "").strip()
          
          # If the excerpt marker already exists, return the title and original content
          if "<!-- more -->" in content:
            return title, content
          
          try:
            # Find the index of the title line
            title_index = lines.index(title_line)
            
            # Initialize variables to track the end of the first paragraph
            first_paragraph_end = title_index + 1
            paragraph_lines = 0
            
            # Iterate through the lines starting after the title to find the first paragraph
            for i in range(title_index + 1, len(lines)):
              line = lines[i].strip()
              if line == "":
                # Blank line signifies the end of the first paragraph
                first_paragraph_end = i
                break
              paragraph_lines += 1
              first_paragraph_end = i + 1  # Update to the line after the current

            # Determine if the first paragraph has at least 8 lines
            if paragraph_lines >= 5:
              insert_position = first_paragraph_end
            else:
              # If not, ensure at least 8 lines are visible after the title
              insert_position = title_index + 1 + 5
              # Adjust if the content has fewer than 8 lines after the title
              insert_position = min(insert_position, len(lines))
            
            # Insert the excerpt marker at the determined position
            lines.insert(insert_position, "<!-- more -->")
            
          except Exception as e:
            # In case of any unexpected error, append the excerpt after the title
            print(f"Error inserting excerpt: {e}")
            insert_position = title_index + 1
            lines.insert(insert_position, "<!-- more -->")
          
          # Reconstruct the content from the modified lines
          modified_content = "\n".join(lines)
          
          return title, modified_content

        def save_post(content, title):
          # Create a slug from the title
          slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")

          # Metadata
          metadata = {
            'date': datetime.now().date()  # Provide a datetime object directly
          }

          # Construct final markdown
          md = f"---\n{yaml.dump(metadata)}---\n\n{content}"
          file_path = f"docs/blog/posts/{slug}.md"
          with open(file_path, "w", encoding="utf-8") as f:
            f.write(md)

          print(f"Generated blog post: {file_path}")

        if __name__ == "__main__":
          post = generate_blog_post()
          title, final_content = extract_title_and_insert_excerpt(post)
          save_post(final_content, title)
        ```

  4. **Test Locally:**

  ```bash

    export OPENAI_API_KEY=your_secret_key
    python generate_post.py
  ```

  Check `docs/blog/posts/` for the newly created `.md` file.
  Run `mkdocs serve` and open `http://localhost:8000/blog` to view the new post.

  **Result:**
  You now have a script that, when executed, produces a new AI-generated blog post.

  ### Step 3: Automate Scheduling

  **Objective:** Run the `generate_post.py` script once a week, automatically.

  **Option:** GitHub Actions (recommended for a GitHub-based project)

  **Actions:**

  1. **Set Up GitHub Action Workflow:**
    Inside your repo, create `.github/workflows/weekly-blog.yml`:

  ```yaml

    name: Weekly Automated Blog Post

    on:
      schedule:
       - cron: '30 20 * * TUE' # Every Tuesday at 8:30 PM UTC you can change the time and day
      workflow_dispatch:

    permissions:
      contents: write

    jobs:
      generate_and_deploy:
       runs-on: ubuntu-latest

       steps:
        - name: Check out Repo
          uses: actions/checkout@v3
          with:
           fetch-depth: 0  # Ensure full history is fetched
           ref: main

        - name: Set up Python
          uses: actions/setup-python@v4
          with:
           python-version: '3.11'

        - name: Install Dependencies
          run: |
           pip install mkdocs mkdocs-material openai PyYAML

        - name: Set Remote with PAT
          env:
           PERSONAL_TOKEN: ${{ secrets.PERSONAL_TOKEN }} 
          run: |
          git remote set-url origin https://x-access-token:${{ secrets.PERSONAL_TOKEN }}@github.com/yourusername/your-repo.git     git fetch origin main
           git checkout -B main origin/main

        - name: Generate and Commit Changes
          env:
           OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }} 
          run: |
           # Generate blog post
           python generate_post.py
           
           # Configure git user
           git config user.name "GitHub Actions"
           git config user.email "actions@github.com"
           
           # Commit changes
           git add .
           git commit -m "Automated blog post - $(date +'%Y-%m-%d')"

        - name: Ensure Up-to-Date Branch
          run: |
           # Pull changes from remote to ensure no conflicts before pushing
           git pull --rebase origin main

        - name: Push changes to main
          env:
           PERSONAL_TOKEN: ${{ secrets.PERSONAL_TOKEN }} 
          run: |
           git push origin main

        - name: Build MkDocs
          run: mkdocs build

        - name: Deploy to GitHub Pages
          uses: peaceiris/actions-gh-pages@v3
          with:
           personal_token: ${{ secrets.PERSONAL_TOKEN }} 
           publish_dir: ./site
    ```

  2. **Add OpenAI Key to GitHub Secrets:**

  Go to your repository’s Settings > Secrets and variables > Actions.
  Add a secret named `OPENAI_API_KEY` with your OpenAI key.

3. **Enable GitHub Pages Hosting:**

  In Settings > Pages, select the `gh-pages` branch and root as the source (the action creates `gh-pages` for you).

**Result:**
Your GitHub Actions workflow will now run every Monday at 8:00 UTC, generate a new post, commit it, and deploy your site automatically.

### Step 4: Deployment and Hosting

**Objective:** After each generation, the site should update online without intervention.

**GitHub Pages Setup:**
Once the workflow runs successfully, your site will be available at `https://yourusername.github.io/my-automated-blog/`.

**Custom Domain (Optional):**
If you have a custom domain, configure it in GitHub Pages settings and update DNS accordingly.

**Result:**
Visitors can see the new post live every week after the automated workflow completes.

### Step 5: Monitoring & Maintenance

**Objective:** Ensure reliability, monitor for errors, and get alerts if something breaks.

**Actions:**

1. **GitHub Actions Logs:**
  Each run logs output. Check the Actions tab for any failures.

2. **Alerting (Optional):**
  Configure email notifications in GitHub Actions settings or integrate with Slack/Microsoft Teams using webhooks or additional Actions steps.

3. **Failure Handling in Script:**
  Enhance `generate_post.py` to handle exceptions (e.g., if the API fails or returns an error).
  Add retry logic if OpenAI returns rate-limit errors.

4. **Cost Monitoring (OpenAI):**
  Regularly check OpenAI usage to avoid unexpected charges.

5. **Backup and Logging:**
  All posts are versioned in Git. You can also periodically store backups of the `docs/blog/posts` folder.

**Result:**
You stay informed about the system’s health, can troubleshoot quickly, and ensure smooth, long-term operation.

### Step 6: Security & Best Practices

**Actions:**

1. **Store Secrets Securely:**
  Never hardcode the OpenAI API key in code. Only use GitHub Secrets.

2. **Branch Protection Rules:**
  Enable branch protection on `main` or `gh-pages` to prevent accidental direct pushes.

3. **Regular Updates:**
  Update dependencies periodically (`mkdocs`, `mkdocs-material`, `openai` library) to ensure compatibility and security patches.

**Result:**
Your environment and data remain secure, and you run with best practices in place.

### Step 7: Enhancement Opportunities

**Future Improvements:**

1. **Topic Diversity:**
  Update the prompt to generate different themes each week. For instance, feed it a list of topics and pick one randomly.

2. **Quality Control:**
  Implement a lightweight sanity check on the generated content before posting (e.g., check if the response contains a title).

3. **Tagging and Categories:**
  Automatically pick tags based on the content’s keywords or add categories for better organization.

4. **Analytics:**
  Integrate Google Analytics or Plausible Analytics to track reader engagement.

5. **Social Media Integration:**
  Add steps in the workflow to tweet or post on LinkedIn after a new post is published (using additional APIs or GitHub Actions marketplace tools).

### Step 8: Documentation & Portfolio Integration

**Actions:**

1. **Write a README or a dedicated page in your MkDocs site explaining the automation process, tools used, and a small diagram of the workflow.**

2. **Showcase in Portfolio:**
  Highlight this project in your portfolio as an example of combining web design, DevOps, AI content generation, and automation skills.

3. **Screenshots & Diagrams:**
  Include screenshots of the GitHub Action runs, the final published blog, and a flow diagram showing the entire pipeline.

**Result:**
Your portfolio now features a fully automated, AI-generated blog, showcasing your abilities in a clean, documented manner.

## Summary

You have:

- A MkDocs-powered blog hosted on GitHub Pages.
- An AI-driven content generation script run via GitHub Actions on a weekly schedule.
- Automatic commit and deployment pipeline, no manual intervention needed.
- Logging and monitoring through GitHub Actions and optional alerting integrations.

By following this detailed, step-by-step guide, you will establish a sustainable, automated content creation and deployment system. This project demonstrates not only technical implementation skills but also the ability to integrate multiple services, maintain security best practices, and enhance over time.

