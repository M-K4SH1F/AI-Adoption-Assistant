import os
import anthropic

# grab the API key from environment variables
# you need to set ANTHROPIC_API_KEY in your .env file
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# this is the system prompt for the AI literacy chatbot
# it keeps the bot focused on AI-related questions
CHAT_SYSTEM_PROMPT = """You are an internal AI literacy assistant for a software company.
Your job is to help employees understand artificial intelligence concepts in plain, 
simple English — no jargon. You answer questions about:
- What AI is and how it works at a high level
- Common AI tools (ChatGPT, Claude, Copilot, etc.)
- How AI is being used in enterprise software
- Best practices for using AI responsibly at work
- General questions about machine learning, LLMs, and automation

Keep your answers concise (2-4 paragraphs max), friendly, and easy to understand 
for someone with no technical background. If you don't know something, say so honestly.
Do not answer questions unrelated to AI or technology."""


def get_chat_response(user_message: str) -> str:
    """
    Send a message to Claude and get back a plain-english AI literacy response.
    Returns the response text, or an error message if something goes wrong.
    """
    try:
        response = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=512,
            system=CHAT_SYSTEM_PROMPT,
            messages=[
                {"role": "user", "content": user_message}
            ]
        )
        # the response is in a list of content blocks, we just want the text
        return response.content[0].text

    except anthropic.AuthenticationError:
        return "Error: Invalid API key. Please check your ANTHROPIC_API_KEY in the .env file."
    except anthropic.RateLimitError:
        return "Error: Rate limit hit. Please wait a moment and try again."
    except Exception as e:
        return f"Something went wrong: {str(e)}"


def generate_newsletter(projects: list[dict]) -> str:
    """
    Takes a list of project dicts and asks Claude to write an internal AI newsletter.
    Returns the newsletter as a formatted string.
    """
    # build a readable summary of the projects to pass to the AI
    project_lines = []
    for i, p in enumerate(projects, start=1):
        line = f"{i}. {p['name']} (Owner: {p['owner'] or 'TBD'}, Status: {p['status']})"
        if p.get("description"):
            line += f"\n   Description: {p['description']}"
        if p.get("milestone"):
            line += f"\n   Latest Milestone: {p['milestone']}"
        project_lines.append(line)

    projects_text = "\n\n".join(project_lines)

    prompt = f"""You are an internal communications writer for a tech company.
Write a friendly, professional internal newsletter update about the company's AI initiatives.
Use the project data below to write the newsletter. Keep it under 400 words.

Format it with:
- A catchy subject line
- A short intro paragraph
- A section for each project (brief, 2-3 sentences each)
- A short motivational closing paragraph

Here is the current AI project data:

{projects_text}

Write the newsletter now:"""

    try:
        response = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.content[0].text

    except anthropic.AuthenticationError:
        return "Error: Invalid API key. Please check your ANTHROPIC_API_KEY in the .env file."
    except anthropic.RateLimitError:
        return "Error: Rate limit hit. Please wait a moment and try again."
    except Exception as e:
        return f"Something went wrong generating the newsletter: {str(e)}"
