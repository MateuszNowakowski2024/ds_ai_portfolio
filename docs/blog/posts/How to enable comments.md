---
date:
  created: 2024-12-11
tags: [Manual, Guide]
---

# How to Enable Comments in MkDocs Portfolio

This guide explains how to enable comments in your MkDocs site. I created it by analyzing the MkDocs documentation and using AI assistance to create clear, step-by-step instructions.

<!-- more -->


## Prompt GPT-o1 

**Context**: MkDocs documentation

**Problem**: Adding comments functionality to MkDocs portfolio

**Objective**: Create a step-by-step guide to enable comments in a MkDocs website using Giscus

Below is a detailed walkthrough that will help you integrate Giscus comments into your MkDocs site using the Material for MkDocs theme. Follow these instructions carefully to enable interactive comments on your documentation pages.

## Repsonse:

### Prerequisites

- You already have a MkDocs project set up with the Material for MkDocs theme.
- You have a GitHub account and a repository where you’d like to host the discussions for your comments.

### Steps

1. **Install Material for MkDocs (if not already)**
    
    - If you haven’t installed Material for MkDocs yet, do so by running:
        
        `pip install mkdocs-material`
        
        
    - Ensure it’s activated in your `mkdocs.yml` config:
        
        `theme:`   
    
	    `name: material`
        
        
1. **Set up a GitHub repository for discussions**
    
    - Decide which GitHub repository will host the discussions for your comments. This can be the same repo that holds your documentation source, or a completely separate repo.
    - Enable [GitHub Discussions](https://docs.github.com/en/discussions) on that repository if you haven’t already. Go to the repo’s "Settings" → "General" tab, scroll down to "Features," and enable Discussions.
3. **Install the Giscus GitHub App**
    
    - Go to [https://giscus.app/](https://giscus.app/) and follow the instructions to install the Giscus GitHub App.
    - Grant the app permission to the repository you’ve chosen for discussions.
    - This app will handle the backend for your comments.
4. **Generate your Giscus snippet**
    
    - While still on [https://giscus.app/](https://giscus.app/), follow their configuration tool:
        - Choose the repository and discussion category you want to use.
        - Set the "Discussion Mapping" to something appropriate, for example `pathname`.
        - Select your preferred theme (you can leave it as `light` for now; Material for MkDocs will handle theme switching).
    - The tool will generate a `<script>` snippet. Copy this entire snippet.
5. **Create the `comments.html` partial override**
    
    - In your MkDocs project, create a folder named `overrides` (if it does not already exist):
        
        `mkdir overrides`
        
    - Inside `overrides`, create a folder structure matching the theme’s partial structure:
    
        `mkdir -p overrides/partials`
        
    - Create (or edit) `comments.html` inside `overrides/partials/`:
        
        
        
```htm
`<!-- overrides/partials/comments.html -->`
`{% if page.meta.comments %}`
  `<h2 id="__comments">{{ lang.t("meta.comments") }}</h2>`
  
  `<!-- Paste your Giscus snippet directly below this line -->`
  
  `<!-- Synchronize Giscus theme with palette -->`
  `<script>`
    `var giscus = document.querySelector("script[src*=giscus]")`

    `// Set palette on initial load`
    `var palette = __md_get("__palette")`
    `if (palette && typeof palette.color === "object") {`
      `var theme = palette.color.scheme === "slate"`
        `? "transparent_dark"`
        `: "light"`
      `giscus.setAttribute("data-theme", theme)` 
    `}`

    `// Register event handlers after document loaded`
    `document.addEventListener("DOMContentLoaded", function() {`
      `var ref = document.querySelector("[data-md-component=palette]")`
      `ref.addEventListener("change", function() {`
        `var palette = __md_get("__palette")`
        `if (palette && typeof palette.color === "object") {`
          `var theme = palette.color.scheme === "slate"`
            `? "transparent_dark"`
            `: "light"`
          `var frame = document.querySelector(".giscus-frame")`
          `frame.contentWindow.postMessage(`
            `{ giscus: { setConfig: { theme } } },`
            `"https://giscus.app"`
          `)`
        `}`
      `})`
    `})`
  `</script>`
`{% endif %}`
`
```
        
- **Important:** Replace the `<!-- Paste your Giscus snippet here -->` comment with the actual `<script>` code you copied from Giscus.
    

Your final `comments.html` might look like this (simplified example):
    
```htm
    ``{% if page.meta.comments %}`
  `<h2 id="__comments">{{ lang.t("meta.comments") }}</h2>`
  `<script`
    `src="https://giscus.app/client.js"`
    `data-repo="username/repo"`
    `data-repo-id="..."`
    `data-category="..."`
    `data-category-id="..."`
    `data-mapping="pathname"`
    `data-reactions-enabled="1"`
    `data-emit-metadata="1"`
    `data-theme="light"`
    `data-lang="en"`
    `crossorigin="anonymous"`
    `async>`
  `</script>`

  `<script>`
    `// Theme synchronization code (from the docs)`
    `var giscus = document.querySelector("script[src*=giscus]")`
    `var palette = __md_get("__palette")`
    `if (palette && typeof palette.color === "object") {`
      `var theme = palette.color.scheme === "slate"`
        `? "transparent_dark"`
        `: "light"`
      `giscus.setAttribute("data-theme", theme)` 
    `}`
    `document.addEventListener("DOMContentLoaded", function() {`
      `var ref = document.querySelector("[data-md-component=palette]")`
      `ref.addEventListener("change", function() {`
        `var palette = __md_get("__palette")`
        `if (palette && typeof palette.color === "object") {`
          `var theme = palette.color.scheme === "slate"`
            `? "transparent_dark"`
            `: "light"`
          `var frame = document.querySelector(".giscus-frame")`
          `frame.contentWindow.postMessage(`
            `{ giscus: { setConfig: { theme } } },`
            `"https://giscus.app"`
          `)`
        `}`
      `})`
    `})`
  `</script>`
`{% endif %}`
`
```
6. **Point MkDocs to the overrides directory**
    
    - In your `mkdocs.yml`, add or confirm the following:
        
        `theme:`   
	     `name: material`   
	     `custom_dir: overrides`
        
    - This tells MkDocs to use the `overrides` directory to replace default theme partials.
7. **Enable comments on a page**
    
    - Open a Markdown page file where you want comments enabled, e.g. `docs/index.md`.
    - At the top of the page, add:
        
        `---` 
        `comments: true` 
        `---`
        
    - This front matter signals to the theme that it should display the comment section on this page.
8. **Build and serve your site**
    
    - Run `mkdocs serve` to start the development server:
        
        `mkdocs serve`
        
    - Open http://127.0.0.1:8000 in your browser.
    - Navigate to the page where you enabled comments. You should see the Giscus comment widget.
9. **Test, commit, and deploy**
    
    - Once you verify that comments are working locally, commit your changes.
    - Deploy your MkDocs site the way you usually do (e.g., GitHub Pages, Netlify, etc.).
    - After deployment, visitors to those pages will be able to view and add comments.

### That’s it!

By following these simple steps, you’ve integrated Giscus comments into your MkDocs Material site. Now you have an interactive comment system that uses GitHub Discussions as a backend—completely free and open source.