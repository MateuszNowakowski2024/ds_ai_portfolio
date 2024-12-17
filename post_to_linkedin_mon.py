import os
from linkedin import LinkedIn
from dotenv import load_dotenv  # Only if using a .env file
import glob
import re
import openai
from llm import generate_intro_mon

# Load variables from .env file if present
load_dotenv()

# Retrieve LinkedIn cookies from environment variables
cookies = {
    "JSESSIONID": os.getenv("LINKEDIN_JSESSIONID"),
    "li_at": os.getenv("LINKEDIN_LI_AT"),
    # Add any other required cookies if needed
}

# OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# The URL to your blog (GitHub Pages URL or custom domain)
BLOG_URL = "https://mateusznowakowski2024.github.io/ds_ai_portfolio/blog/"

files = glob.glob("docs/blog/posts/*.md")
if files:
    # Sort by modification time, get the newest file
    latest_file = max(files, key=os.path.getmtime)
    with open(latest_file, "r", encoding="utf-8") as f:
        content = f.read()
        
        # Attempt to extract title from the markdown
        title_match = re.search(r'^# (.+)', content, re.MULTILINE)
        if title_match:
            latest_post = title_match.group(1)
        else:
            latest_post = "New Post"
        
        # Extract the content after the title
        lines = content.split("\n")
        
        # Find the line index of the title
        title_index = None
        for i, line in enumerate(lines):
            if line.strip().startswith("# "):
                title_index = i
                break
        
        # Extract lines after the title
        post_body_lines = lines[title_index+1:] if title_index is not None else lines
        
        # Clean empty lines
        post_body_lines = [l.strip() for l in post_body_lines if l.strip()]
        
        # Create paragraphs by splitting on blank lines again if needed
        content_blocks = []
        current_block = []
        
        for line in post_body_lines:
            if line == "":
                if current_block:
                    content_blocks.append(" ".join(current_block))
                    current_block = []
            else:
                current_block.append(line)
        
        if current_block:
            content_blocks.append(" ".join(current_block))
        
        # Take the first two blocks for summary
        summary_blocks = content_blocks[:2]
        summary_text = "\n\n".join(summary_blocks).strip()
        
        # Generate a dynamic introduction using the LLM
        message = generate_intro_mon(latest_post, summary_text, BLOG_URL)
        
    # Initialize LinkedIn client and post
    linkedin = LinkedIn(cookies=cookies)
    linkedin.post(message)
    print("Posted to LinkedIn successfully!")
else:
    print("No blog posts found. Nothing to share on LinkedIn.")
