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


