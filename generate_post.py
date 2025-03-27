import openai
import os
import yaml
from datetime import datetime
import re
import glob
from llm import tutorial_post

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_recent_posts_titles(directory="docs/blog/posts", limit=25):
    """
    Retrieve titles of recent posts by reading from existing markdown files.
    Assumes that the title is in the YAML front matter or the first heading (# Title).
    """
    posts = sorted(glob.glob(os.path.join(directory, "*.md")), key=os.path.getmtime, reverse=True)
    recent_titles = []
    for post in posts[:limit]:
        with open(post, "r", encoding="utf-8") as f:
            content = f.read()
            # Try to extract title from front matter or first heading
            front_matter_match = re.search(r"(?m)^title:\s*(.*)", content)
            if front_matter_match:
                title = front_matter_match.group(1).strip('"\' ')
            else:
                heading_match = re.search(r"(?m)^#\s+(.*)", content)
                title = heading_match.group(1).strip() if heading_match else os.path.basename(post)
            recent_titles.append(title)
    return recent_titles



def extract_title_and_insert_excerpt(content):
    """
    Extracts the title from the content and inserts an excerpt marker (`<!-- more -->`).
    """
    lines = content.split("\n")
    title_line = next((l for l in lines if l.startswith("# ")), "# Recent AI Advancements")
    title = title_line.replace("# ", "").strip()
    
    if "<!-- more -->" in content:
        return title, content
    
    try:
        title_index = lines.index(title_line)
        paragraph_lines = 0
        first_paragraph_end = title_index + 1
        
        for i in range(title_index + 1, len(lines)):
            line = lines[i].strip()
            if line == "":
                first_paragraph_end = i
                break
            paragraph_lines += 1
            first_paragraph_end = i + 1

        if paragraph_lines >= 5:
            insert_position = first_paragraph_end
        else:
            insert_position = title_index + 1 + 5
            insert_position = min(insert_position, len(lines))
        
        lines.insert(insert_position, "<!-- more -->")
        
    except Exception as e:
        print(f"Error inserting excerpt: {e}")
        insert_position = title_index + 1
        lines.insert(insert_position, "<!-- more -->")
    
    modified_content = "\n".join(lines)
    return title, modified_content

def save_post(content, title):
    # Create a slug from the title
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    
    metadata = {
        'title': title,
        'date': datetime.now().date()
    }

    md = f"---\n{yaml.dump(metadata)}---\n\n{content}"
    file_path = f"docs/blog/posts/{slug}.md"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(md)

    print(f"Generated blog post: {file_path}")

if __name__ == "__main__":
    recent_titles = get_recent_posts_titles()
    post = tutorial_post(recent_titles)
    title, final_content = extract_title_and_insert_excerpt(post)
    save_post(final_content, title)