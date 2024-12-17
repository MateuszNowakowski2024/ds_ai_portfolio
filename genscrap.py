import os
import re
import glob
import openai
import yaml
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import feedparser
from feedparser import FeedParserDict
from llm import blog_post


openai.api_key = os.getenv("OPENAI_API_KEY")


class Scraper:
    def __init__(self, url, character_limit=2000):
        self.url: str = url
        self.character_limit = character_limit

    def fetch_content(self):
        try:
            if self.url.endswith('rss') or self.url.endswith('xml') or 'feed' in self.url:
                return self.rss_parse(self.url)
            response = requests.get(self.url)
            response.raise_for_status()
            return self.parse(response.text)
        except Exception as e:
            print(f"Error fetching content from {self.url}: {e}")
            return None

    def parse(self, content):
        soup = BeautifulSoup(content, 'html.parser')

        # Removing undesired elements
        for element in soup.find_all(["nav", "header"]):
            element.decompose()

        # Removing script and style elements
        for script in soup(["script", "style"]):
            script.extract()

        # Extract text using the get_text() method
        all_text = soup.get_text()

        # Clean up the text
        lines = (line.strip() for line in all_text.splitlines())
        all_text_clean = re.sub(r'\s+', ' ', (' '.join(line for line in lines if line)))

        return all_text_clean[0:self.character_limit]

    def rss_parse(self, url):
        feed: FeedParserDict = feedparser.parse(url)
        if not feed.entries:
            return None
        # Instead of random entry, we might gather a few entries
        entries_summaries = []
        for entry in feed.entries[:3]:  # take top 3 entries
            summary = getattr(entry, 'summary', '') or getattr(entry, 'description', '')
            title = getattr(entry, 'title', '')
            link = getattr(entry, 'link', '')
            # Combine title and summary for context
            combined = f"Title: {title}\nSummary: {summary}\nLink: {link}\n"
            entries_summaries.append(combined)
        return "\n".join(entries_summaries)


def get_recent_posts_titles(directory="docs/blog/posts", limit=3):
    """
    Retrieve titles of recent posts by reading from existing markdown files.
    """
    posts = sorted(glob.glob(os.path.join(directory, "*.md")), key=os.path.getmtime, reverse=True)
    recent_titles = []
    for post in posts[:limit]:
        with open(post, "r", encoding="utf-8") as f:
            content = f.read()
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
    # Example feeds or websites:
    urls = [
        "https://www.kdnuggets.com/feed",    
        "https://dataconomy.com/",  
        "https://aibusiness.com/rss.xml"   
    ]

    # Scrape from multiple sources and combine
    scraped_contents = []
    for u in urls:
        scraper = Scraper(u)
        content = scraper.fetch_content()
        if content:
            scraped_contents.append(content)

    combined_scraped_context = "\n\n".join(scraped_contents)

    recent_titles = get_recent_posts_titles()
    post = blog_post(recent_titles, combined_scraped_context)
    title, final_content = extract_title_and_insert_excerpt(post)
    save_post(final_content, title)
