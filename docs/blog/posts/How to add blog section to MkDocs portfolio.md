---
date:
  created: 2024-12-12
tags: [Manual, Guide]
---

# How to add a blog section to MkDocs portfolio
Here you have a complete step-by-step guide that walks you through the process of adding a blog section to your MkDocs portfolio. It's in the form of a conversation between myself and a OpenAi o1 model.
<!-- more -->
## Prompt #1

**Persona Adoption**: You are an experienced website designer

reference content: [MkDocs Blog Plugin Documentation](https://squidfunk.github.io/mkdocs-material/tutorials/blogs/basic/)

**Context**: Documentation above describes how to set up a blog section

**Problem**: I don't have time to fetch the information from the documentation and learn how to do it. I need a simple step-by-step guide.

**Objective**: Create a step-by-step instruction on how to set up a blog section in my MkDocs portfolio. Keep it simple. Baby steps.

ChatGPT model 01

## Response

Below is a very simple, step-by-step guide based on the documentation above. Think of it like a checklist you can follow, even if you’re new to this.

### Step-by-Step Instructions

1. **Create a basic MkDocs project**
        
        - If you don’t already have one, open a terminal and run:
                
                ```bash
                mkdocs new my-blog
                ```
                
                This creates a folder called `my-blog` with some starter files.
2. **Move into your project folder**
        
        ```bash
        cd my-blog
        ```
        
3. **Open your configuration file**
        
        - Find the `mkdocs.yml` file inside `my-blog`.
        - Open it with a text editor (e.g., Visual Studio Code, Notepad++, or any text editor).
4. **Add the blog plugin**
        
        - Inside `mkdocs.yml`, look for the `plugins:` section. If you don’t see one, add it:

                ```yaml
                site_name: My Blog
                site_description: Just a simple blog
                site_url: http://www.example.com
                theme:
                    name: material
                plugins:
                    - search
                    - blog
                ```
                
        - Save the file.
5. **Start the development server**
        
        - Back in your terminal:
        
                ```bash
                mkdocs serve
                ```
                
        - This starts a local server. Open your web browser and go to `http://localhost:8000`.
        - After the first run, the blog plugin will create a `docs/blog/posts` folder structure for you.
6. **Create your first blog post**
        
        - Look inside `docs/blog/posts`. You should see it’s empty (or just a placeholder).
        - Create a file named something like `my-first-post.md` inside `docs/blog/posts`.
        - Paste in this simple content:
                
                ```markdown
                ---
                date:
                    created: 2023-12-31
                ---
                # My First Blog Post

                This is my first post! Welcome to my blog.

                <!-- more -->

                Here’s some more details that only show up on the full post page.
                ```
                
        - Save the file.
7. **Check your blog**
        
        - With the dev server running (`mkdocs serve`), refresh `http://localhost:8000/blog`.
        - You should see your first post listed. Click “Continue reading” to view the full post.
8. **Adjust and experiment**
        
        - Try changing the title (the line starting with `#`) in your post file to see how the URL changes.
        - If you add more posts (just copy the same structure, change the title and date), you’ll see them appear in the blog list.
9. **Using drafts (optional)**
        
        - If you add `draft: true` under `date:` in a post’s header, that post will show up when using `mkdocs serve` but will not appear when you do `mkdocs build`.  
                Example:

                ```markdown
                ---
                date:
                    created: 2024-01-01
                draft: true
                ---
                # Coming Soon Post

                This post is a draft and not ready to be published!
                ```
                
        - Good for preparing future posts without publishing them yet.
10. **Build your final blog**
        
        - When you’re ready to make your blog live, just run:
                
                ```bash
                mkdocs build
                ```
                
        - This creates a `site` folder with all the final, ready-to-upload website files. Any draft posts won’t be there.

---

That’s it! You now have a simple blog section in your MkDocs portfolio site. Just keep creating new `.md` files in `docs/blog/posts`, each with a date and a heading, and your blog will grow.

## Prompt #2

**Context**: Conversation above

**Problem**: This instruction creates a new website rather than a blog section in my existing portfolio website

**Objective**: Modify this instruction so it creates a blog section within my portfolio MkDocs website

## Response:

Understood! To integrate a blog section into your existing MkDocs portfolio website instead of creating a new website, you'll need to modify your current setup. Below is a detailed, step-by-step guide to help you seamlessly add a blog to your existing MkDocs portfolio.

### Step-by-Step Instructions to Add a Blog Section to Your Existing MkDocs Portfolio

1. **Ensure Prerequisites Are Met**

        Before proceeding, make sure you have:

        - MkDocs Installed: Verify that MkDocs is installed on your system.
        
                ```bash
                mkdocs --version
                ```
        
        - Existing MkDocs Project: You should have an existing MkDocs project set up for your portfolio.
        - Text Editor: A text editor like Visual Studio Code, Sublime Text, or Notepad++.

2. **Install Necessary Plugins**

        To add blogging capabilities, you'll need the Blog Plugin and possibly other extensions depending on your requirements.

        - Activate a Virtual Environment (Optional but Recommended):

                ```bash
                python -m venv venv
                # Activate the virtual environment:
                # On Windows:
                venv\Scripts\activate
                # On macOS/Linux:
                source venv/bin/activate
                ```

        - Install MkDocs Material and Blog Plugin:

                If you haven't installed MkDocs Material theme yet, do so along with the Blog Plugin.

                ```bash
                pip install mkdocs-material mkdocs-blog-plugin
                ```

                Note: The exact name of the blog plugin may vary. Ensure you're installing the correct plugin compatible with your MkDocs version. If you're using a specific blog plugin like Material for MkDocs Blog, follow its installation instructions.

3. **Modify Your mkdocs.yml Configuration**

        Update your existing `mkdocs.yml` to include the blog plugin and configure necessary settings.

        - Open `mkdocs.yml`:

                Navigate to your project's root directory and open the `mkdocs.yml` file in your text editor.

        - Add/Update Configuration:

                Here's how to modify your `mkdocs.yml` to integrate the blog:

                ```yaml
                site_name: My Portfolio
                site_description: A portfolio showcasing my projects and insights on Data Science and AI.
                site_url: https://yourusername.github.io/my-portfolio/  # Replace with your actual site URL

                theme:
                    name: material

                plugins:
                    - search
                    - blog:
                            # Optional Blog Plugin Configurations
                            # You can customize the blog settings as needed
                            blog_dir: blog/posts  # Directory for blog posts
                            feed_url: rss.xml      # RSS feed URL
                            # Add other configurations if required

                nav:
                    - Home: index.md
                    - About: about.md
                    - Blog:
                            - Home: blog/index.md
                    - Contact: contact.md

                # Optional: Add other configurations like markdown_extensions, extra_css, etc.
                ```

                Explanation of Changes:

                - **Plugins Section**: Added the blog plugin alongside the existing search plugin. You can customize the blog plugin settings as needed.
                - **Navigation (nav)**: Added a Blog section to the navigation menu, linking to `blog/index.md`. This ensures your blog appears as a section within your portfolio.

                Tip: Ensure that indentation and YAML syntax are correct to prevent configuration errors.

        - Save the `mkdocs.yml` File.

4. **Create the Blog Directory Structure**

        Set up the necessary folders for your blog posts.

        - Navigate to the `docs` Directory:

                ```bash
                cd my-portfolio/docs
                ```

        - Create Blog Folders:

                Create the `blog` and `posts` directories.

                ```bash
                mkdir -p blog/posts
                ```

        - Create the Blog Index Page:

                Inside the `blog` folder, create an `index.md` file which will serve as the main blog page.

                ```bash
                touch blog/index.md
                ```

        - Edit `blog/index.md`:

                Open `blog/index.md` in your text editor and add the following content:

                ```markdown
                ---
                title: Blog
                ---

                # Blog

                Welcome to my blog! Here you'll find articles on Data Science, AI, and more.

                <!-- blog_post_list -->
                ```

                Note: The `<!-- blog_post_list -->` placeholder is used by the blog plugin to inject the list of blog posts dynamically.

5. **Create Your First Blog Post**

        Add your initial blog post to kickstart the blog section.

        - Navigate to the `posts` Directory:

                ```bash
                cd blog/posts
                ```

        - Create a Markdown File for Your Post:

                Name the file using a consistent naming convention, such as `my-first-post.md`.

                ```bash
                touch my-first-post.md
                ```

        - Edit `my-first-post.md`:

                Open `my-first-post.md` in your text editor and add the following content:

                ```markdown
                ---
                date:
                    created: 2024-04-27
                tags: [Introduction, Welcome]
                ---

                # My First Blog Post

                Welcome to my blog! This is the first post where I'll be sharing insights on Data Science and AI.

                <!-- more -->

                In this post, I'll introduce the topics I plan to cover and what you can expect from my future articles.
                ```

                Explanation of Content:

                - **YAML Front Matter (---)**: Contains metadata such as the creation date and tags.
                - **Title (# My First Blog Post)**: The main heading of the post, which will be used to generate the slug and URL.
                - **Excerpt (`<!-- more -->`)**: Defines where the excerpt ends on the blog index page.

        - Save the File.

6. **Update Navigation to Include Blog**

        Ensure that your blog appears correctly in the site's navigation.

        - Open `mkdocs.yml`:

                Ensure that the `nav` section includes the Blog link as shown earlier.

        - Verify Navigation Structure:

                ```yaml
                nav:
                    - Home: index.md
                    - About: about.md
                    - Blog:
                            - Home: blog/index.md
                    - Contact: contact.md
                ```

                Note: Adjust the navigation as per your existing portfolio structure to integrate the blog seamlessly.

        - Save the `mkdocs.yml` File.

7. **Start the Development Server and Test**

        Run MkDocs locally to verify that the blog section is integrated correctly.

        - Navigate to Project Root (if not already there):

                ```bash
                cd ../../
                ```

        - Start the MkDocs Development Server:

                ```bash
                mkdocs serve
                ```

        - Access Your Site Locally:

                Open your web browser and go to `http://localhost:8000/`.

        - Navigate to the Blog Section:

                Click on the Blog link in the navigation menu.

                You should see your first blog post listed.

                Click on "Continue reading" (or the equivalent link) to view the full post.

                Tip: If you don't see the blog post, ensure that the blog plugin is correctly installed and configured, and that the `blog/index.md` and post files are properly formatted.

8. **Create Additional Blog Posts**

        Continue adding more content to your blog by creating new Markdown files.

        - Navigate to `docs/blog/posts`:

                ```bash
                cd docs/blog/posts
                ```

        - Create a New Post:

                For example, create `data-science-trends-2024.md`.

                ```bash
                touch data-science-trends-2024.md
                ```

        - Edit `data-science-trends-2024.md`:

                ```markdown
                ---
                date:
                    created: 2024-05-04
                tags: [Data Science, Trends]
                ---

                # Data Science Trends in 2024

                <!-- more -->

                In this post, we'll explore the emerging trends in Data Science that are shaping the industry in 2024.
                ```

        - Save the File.

        - Refresh the Blog Page:

                With the development server running, refresh `http://localhost:8000/blog` to see the new post listed.

9. **Optional: Using Drafts**

        Manage posts that are not ready to be published by marking them as drafts.

        - Create a Draft Post:

                ```bash
                touch upcoming-features.md
                ```

        - Edit `upcoming-features.md`:

                ```markdown
                ---
                date:
                    created: 2024-05-10
                draft: true
                tags: [Upcoming, Features]
                ---

                # Upcoming Features

                This post is a draft and not ready to be published!
                ```

        - Save the File.

        - Behavior:

                - During Development (`mkdocs serve`): The draft post will appear on the blog index with a label indicating it's a draft.
                - When Building for Production (`mkdocs build`): Draft posts marked with `draft: true` will not be included in the final build.

                Tip: Remember to remove the `draft: true` line when you're ready to publish the post.

10. **Build and Deploy Your Portfolio with the Integrated Blog**

        Once you're satisfied with the blog integration, build your MkDocs site for deployment.

        - Stop the Development Server:

                Press `Ctrl + C` in your terminal where `mkdocs serve` is running.

        - Build the Site:

                ```bash
                mkdocs build
                ```

                This command generates a `site` directory containing all the static files ready for deployment.

        - Deploy the Site:

                Deploy the `site` folder to your hosting platform. Common hosting options include:

                - **GitHub Pages**:
                        - Push your `site` directory to the `gh-pages` branch.
                        - Alternatively, use MkDocs Material's deployment commands for seamless deployment.
                - **Netlify, Vercel, or Other Static Hosts**:
                        - Follow their specific deployment instructions, pointing to the `site` directory.

                Tip: Consider automating deployments using Continuous Integration/Continuous Deployment (CI/CD) tools like GitHub Actions for seamless updates.

11. **Final Verification**

        After deployment, ensure that:

        - **Blog Section is Accessible**:

                Visit your portfolio website's blog section (e.g., `https://yourusername.github.io/my-portfolio/blog`) to verify that posts appear correctly.

        - **Navigation Works**:

                Ensure that the navigation menu links to the blog and other sections properly.

        - **Responsive Design**:

                Check that the blog section is responsive and displays well on different devices (desktop, tablet, mobile).

12. **Maintain and Update Your Blog**

        Regularly add new posts and manage existing content to keep your blog active and engaging.

        - **Adding New Posts**:

                Create new `.md` files in `docs/blog/posts` following the established structure.
                Ensure each post has the necessary YAML front matter (date, tags, etc.).

        - **Managing Existing Posts**:

                Update posts as needed.
                Use drafts for posts that are still in progress.

        - **Enhancing Blog Features**:

                - **Categories and Tags**:
                        Organize posts using categories and tags for better navigation and SEO.
                - **Search Functionality**:
                        The search plugin allows visitors to search through your blog content.
                - **RSS Feeds**:
                        Enable RSS feeds for your blog to allow users to subscribe.
                - **Comments Section**:
                        Integrate a comments system like Disqus or Staticman if you wish to enable user interactions.

13. **Troubleshooting Tips**

        If you encounter issues during integration, consider the following:

        - **Check YAML Syntax**:
                Ensure that your `mkdocs.yml` and blog post `.md` files have correct YAML front matter and proper indentation.
        - **Plugin Compatibility**:
                Verify that the blog plugin version is compatible with your MkDocs and Material theme versions.
        - **Build Errors**:
                Run `mkdocs serve` locally to identify and fix any errors before deploying.
        - **Plugin Documentation**:
                Refer to the [Blog Plugin Documentation](https://squidfunk.github.io/mkdocs-material/plugins/blog/) for advanced configurations and troubleshooting.

### Summary

By following these steps, you've successfully integrated a blog section into your existing MkDocs portfolio website. This setup allows you to:

- **Create and Manage Blog Posts**: Easily add new content by creating Markdown files within the `docs/blog/posts` directory.
- **Organize Content**: Utilize tags and categories to structure your blog for better navigation and SEO.
- **Seamless Navigation**: The blog appears as a distinct section within your portfolio, accessible via the navigation menu.
- **Flexible Deployment**: Build and deploy your updated site with integrated blog posts to your chosen hosting platform.

### Additional Resources

- [MkDocs Official Documentation](https://www.mkdocs.org/)
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
- [Blog Plugin for MkDocs Material](https://squidfunk.github.io/mkdocs-material/plugins/blog/)
- [Deploying MkDocs Sites](https://www.mkdocs.org/user-guide/deploying-your-docs-site/)

Feel free to reach out if you need further assistance or have specific questions about your setup!