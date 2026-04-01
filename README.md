# 🤖 AI Adoption Assistant

A Flask web application that helps organizations track AI initiatives, auto-generate internal AI newsletters, and promote AI literacy through a conversational chatbot — powered by the Anthropic Claude API.

Built as a portfolio project targeting enterprise AI communication and adoption workflows.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Environment Variables](#environment-variables)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Future Improvements](#future-improvements)

---

## Overview

Many organizations struggle with tracking AI initiatives and communicating their progress internally. The AI Adoption Assistant solves three specific problems:

1. **Traceability** — A centralized dashboard to track AI projects, their status, owners, and milestones
2. **Communication** — An AI-powered newsletter generator that turns project data into polished internal updates in seconds
3. **Literacy** — A chatbot that answers employee questions about AI in plain, jargon-free English

This project was built to demonstrate practical AI tool integration in an enterprise context, with a focus on communication, documentation, and adoption — not just the technical side of AI.

---

## Features

- 📊 **Project Tracker Dashboard** — Add, edit, and delete AI initiatives with status labels (Planning, In Progress, Completed, On Hold)
- 📰 **AI Newsletter Generator** — Pulls current project data and generates a formatted internal newsletter using Claude
- 💬 **AI Literacy Chatbot** — Conversational bot that answers questions about AI concepts in plain English
- ✅ **Status Summary Cards** — At-a-glance counts of projects by status
- 📋 **One-click Copy** — Copy generated newsletters to clipboard instantly
- 💡 **Suggested Questions** — Pre-built prompts to help users get started with the chatbot

---

## Tech Stack

| Layer       | Technology                        |
|-------------|-----------------------------------|
| Backend     | Python, Flask                     |
| AI / LLM    | Anthropic Claude API (`anthropic` SDK) |
| Database    | SQLite (via Python `sqlite3`)     |
| Frontend    | Jinja2 templates, vanilla CSS/JS  |
| Config      | `python-dotenv`                   |

---

## Project Structure

```
ai-adoption-assistant/
│
├── app.py              # Flask routes and app setup
├── database.py         # SQLite connection and schema init
├── ai_agent.py         # Claude API calls (chat + newsletter)
├── requirements.txt
├── .env.example        # Template for environment variables
├── .gitignore
│
├── templates/
│   ├── base.html       # Shared layout (navbar, flash messages)
│   ├── dashboard.html  # Project tracker
│   ├── add_project.html
│   ├── edit_project.html
│   ├── newsletter.html # Newsletter generator
│   └── chat.html       # AI literacy chatbot
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js     # Chat logic and clipboard copy
│
└── instance/
    └── projects.db     # Auto-created on first run (gitignored)
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- An [Anthropic API key](https://console.anthropic.com/)

### Installation

**1. Clone the repository**

```bash
git clone https://github.com/YOUR_USERNAME/ai-adoption-assistant.git
cd ai-adoption-assistant
```

**2. Create and activate a virtual environment**

```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate
```

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Set up environment variables**

```bash
cp .env.example .env
```

Then open `.env` and add your Anthropic API key (see [Environment Variables](#environment-variables)).

**5. Run the app**

```bash
python app.py
```

Open [http://localhost:5000](http://localhost:5000) in your browser.

---

## Environment Variables

Create a `.env` file in the root directory based on `.env.example`:

```env
ANTHROPIC_API_KEY=your_anthropic_api_key_here
SECRET_KEY=pick-a-random-secret-string-here
```

> ⚠️ Never commit your `.env` file. It's included in `.gitignore`.

You can get an Anthropic API key at [console.anthropic.com](https://console.anthropic.com/).

---

## Usage

### Adding a Project
1. Go to the **Dashboard**
2. Click **+ Add Project**
3. Fill in the project name, description, owner, status, and latest milestone
4. The project appears in the tracker dashboard immediately

### Generating a Newsletter
1. Add at least one project to the tracker
2. Navigate to **Newsletter**
3. Click **✨ Generate Newsletter**
4. Claude reads your project data and writes a formatted internal update
5. Click **📋 Copy Text** to copy it to your clipboard

### Using the AI Chat
1. Navigate to **AI Chat**
2. Click a suggested question or type your own
3. Ask anything about AI — Claude will respond in plain English

---

## Future Improvements

- [ ] User authentication (login/logout per team member)
- [ ] Export newsletter as `.txt` or `.pdf`
- [ ] Filter and search projects by status or owner
- [ ] Chat history persistence across sessions
- [ ] Email integration to send newsletters directly
- [ ] File upload support for importing project data from CSV

---

## Author

**Mohammed Alhajri**  
Software Engineering Student @ University of New Brunswick  
[GitHub](https://github.com/YOUR_USERNAME) · [LinkedIn](https://linkedin.com/in/YOUR_LINKEDIN)
