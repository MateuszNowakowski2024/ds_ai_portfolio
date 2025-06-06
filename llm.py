import openai
import random

def generate_intro_thu(title, summary_text, blog_url):
    """
    Uses the LLM to create a short, appealing LinkedIn introduction for the blog post.
    The intro should:
    - Reference the blog's title.
    - Highlight some details from the summary.
    - Include emojis and an enthusiastic tone.
    - Provide a call-to-action to read the full post.
    - Vary content to avoid repetition over time.
    """
    
    prompt = (
        "You are a marketing copywriter creating a LinkedIn introduction for a new blog post. "
        "Start from the words 'Welcome to Python Thursday!'"
        "Write a short (50-100 words) LinkedIn post introduction that:\n"
        "- References the blog title provided.\n"
        "- Summarizes or teases some key insights from the summary text.\n"
        "- Uses emojis to convey enthusiasm.\n"
        "- Encourages the reader to click through to read the full post.\n"
        "- Is casual, engaging, and varied each time it's generated.\n\n"
        f"Blog Title: {title}\n"
        f"Post Summary:\n{summary_text}\n\n"
        f"Blog URL: {blog_url}\n\n"
        "Draft the introduction now."
    )
    
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a professional content creator with a flair for catchy, engaging marketing copy."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500,
        temperature=0.8,
    )

    return response.choices[0].message.content.strip()


def generate_intro_mon(title, summary_text, blog_url):
    """
    Uses the LLM to create a short, appealing LinkedIn introduction for the blog post.
    The intro should:
    - Reference the blog's title.
    - Highlight some details from the summary.
    - Include emojis and an enthusiastic tone.
    - Provide a call-to-action to read the full post.
    - Vary content to avoid repetition over time.
    """
    
    prompt = (
        "You are a marketing copywriter creating a LinkedIn introduction for a new blog post. "
        "Write a short (100-150 words) LinkedIn post introduction that:\n"
        "Start from the words 'Happy Monday Everyone!'" 
        "- References the blog title provided.\n"
        "- Summarizes or teases some key insights from the summary text.\n"
        "- Uses emojis to convey enthusiasm.\n"
        "- Encourages the reader to click through to read the full post.\n"
        "- Is casual, engaging, and varied each time it's generated.\n\n"
        f"Blog Title: {title}\n"
        f"Post Summary:\n{summary_text}\n\n"
        f"Blog URL: {blog_url}\n\n"
        "Draft the introduction now."
    )
    
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a professional content creator with a flair for catchy, engaging marketing copy."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500,
        temperature=0.8,
    )

    return response.choices[0].message.content.strip()


def blog_post(recent_titles, scraped_context):
    recent_posts_str = "\n".join([f"- {t}" for t in recent_titles]) if recent_titles else "No recent posts found."

    # Instead of relying on a hardcoded topic, we instruct the model to choose a topic 
    # based on the scraped news context.
    prompt = (
        "Write a detailed blog post (around 500 words) that focuses on a timely and relevant "
        "topic derived from the recent data science and AI news and updates provided below. "
        "Your post should identify a key theme from these updates and center the discussion around it. "
        "The writing style should be casual, yet informative and technical. "
        "Include headings, an introduction, and a conclusion. "
        f"Avoid repeating content and topics covered in recent posts:\n{recent_posts_str}\n\n"
        f"Below are the recent data science and AI news and updates:\n\n"
        f"{scraped_context}\n\n"
        "Integrate these insights to make the post feel current and relevant. "
        "Also include references to known techniques or research related to the chosen topic. "
        "Ensure to provide unique insights and avoid repetition of previously discussed material."
    )

    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a talented aspiring data scientist and AI enthusiast."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=2000,
        temperature=0.7,
    )

    return response.choices[0].message.content.strip()

def tutorial_post(recent_titles):
    # Define an extensive variety of topics to choose from
    topics = [
        # Original Python coding tutorials
        "Python coding tutorial: conditional statements",
        "Python coding tutorial: data structures",
        "Python coding tutorial: file handling",
        "One-line data modeling techniques in Python",
        "Python coding tutorial: virtual environments and dependency management",
        "Python coding tutorial: writing and running tests",
        "Python coding tutorial: error handling and exceptions",
        "Terminal tutorial: navigating the filesystem using `cd`, `ls`, and `pwd`",
        "Terminal tutorial: using `grep` and `find` for searching files",
        "Terminal tutorial: using `curl` and `wget` for data retrieval",
        "Terminal tutorial: automating tasks with `cron` jobs",
        "Python coding tutorial: comprehensions (list, dictionary, and set)",
        "Python coding tutorial: working with APIs and HTTP requests",
        "Python coding tutorial: regular expressions for text processing",
        "Python coding tutorial: multithreading and multiprocessing",
        "Python coding tutorial: working with dates and times",
        "Python coding tutorial: decorators and advanced function usage",
        "Python coding tutorial: context managers and the with statement",
        "Python coding tutorial: creating and using Python packages",
        "Python coding tutorial: exploring Python's collections module",
        "Python coding tutorial: introduction to asynchronous programming",

        # Additional Python libraries and frameworks
        "Data Analysis with Pandas: Harnessing DataFrames",
        "Visualizing Data Beautifully with Matplotlib",
        "Interactive Data Visualization with Plotly",
        "Machine Learning Simplified with Scikit-Learn",
        "Building Deep Learning Models with TensorFlow",
        "Natural Language Processing with NLTK",
        "Web Development Made Easy with Flask",
        "Web Apps at Scale with Django",
        "Automation Tasks Simplified with PyAutoGUI",
        "Creating Modern GUIs with Tkinter",
        "Efficient Array Computing with NumPy",
        "Working with APIs Made Simple: Requests Library",
        "Advanced Web Scraping Techniques with Beautiful Soup",
        "Seamless Task Scheduling with APScheduler",
        "Automate Excel Tasks with OpenPyXL",
        "Image Processing Basics with Pillow",
        "Real-Time Data Streaming with Kafka-Python",
        "Build Command-Line Interfaces Effortlessly with Click",
        "Automated Testing Made Easy with Pytest",
        "Time Series Analysis with Prophet",

        # Advanced Libraries
        "Symbolic Mathematics with SymPy",
        "Interactive Data Science with JupyterLab",
        "Managing ML Lifecycles with MLflow",
        "Deep Learning Flexibility with PyTorch",
        "Rapid Deep Learning Prototyping with FastAI",
        "Gradient Boosting with XGBoost",
        "Advanced Gradient Boosting with LightGBM",
        "Scalable Gradient Boosting with CatBoost",
        "Explainable Machine Learning with SHAP",
        "Efficient Hyperparameter Tuning with Optuna",
        "AutoML Made Simple with PyCaret",
        "Distributed Data Processing with Dask",
        "Accelerated Machine Learning with RAPIDS",
        "Time-Series Forecasting with sktime",
        "State-of-the-Art NLP with SpaCy",
        "Efficient Reinforcement Learning with Stable-Baselines3",
        "Deep Reinforcement Learning with RLlib",
        "Bayesian Modeling with PyMC",
        "Deploying Machine Learning Models with Streamlit",
        "Production-Ready AI Pipelines with Kubeflow"
    ]

    chosen_topic = random.choice(topics)

    # Create a prompt that references recent posts to avoid repetition
    recent_posts_str = "\n".join([f"- {t}" for t in recent_titles]) if recent_titles else "No recent posts found."
    prompt = (
        f"Write a detailed blog post (around 800 words) on {chosen_topic}. "
        f"The writing style should be casual, yet informative and technical. "
        f"Include headings, an introduction, and a conclusion. "
        f"Avoid repeating content and topics covered in recent posts:\n{recent_posts_str}\n\n"
        "Also include references to known techniques or research related to the chosen topic. "
        "Make sure to provide unique insights and not repeat previously discussed material."
    )

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an experienced Python tutor and blog author."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=2000,
        temperature=0.7,
    )

    return response.choices[0].message.content.strip()
