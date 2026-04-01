from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from database import init_db, get_db
from ai_agent import get_chat_response, generate_newsletter
from dotenv import load_dotenv
import os

# load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-prod")

# initialize the database when app starts
with app.app_context():
    init_db()


# ── Dashboard ──────────────────────────────────────────────────────────────────

@app.route("/")
def dashboard():
    db = get_db()
    projects = db.execute("SELECT * FROM projects ORDER BY created_at DESC").fetchall()
    db.close()

    # count projects by status for the summary cards
    status_counts = {"Planning": 0, "In Progress": 0, "Completed": 0, "On Hold": 0}
    for p in projects:
        status = p["status"]
        if status in status_counts:
            status_counts[status] += 1

    return render_template("dashboard.html", projects=projects, status_counts=status_counts)


# ── Projects (CRUD) ────────────────────────────────────────────────────────────

@app.route("/projects/add", methods=["GET", "POST"])
def add_project():
    if request.method == "POST":
        name        = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()
        owner       = request.form.get("owner", "").strip()
        status      = request.form.get("status", "Planning")
        milestone   = request.form.get("milestone", "").strip()

        if not name:
            flash("Project name is required.", "error")
            return redirect(url_for("add_project"))

        db = get_db()
        db.execute(
            "INSERT INTO projects (name, description, owner, status, milestone) VALUES (?, ?, ?, ?, ?)",
            (name, description, owner, status, milestone)
        )
        db.commit()
        db.close()

        flash(f'Project "{name}" added successfully!', "success")
        return redirect(url_for("dashboard"))

    return render_template("add_project.html")


@app.route("/projects/edit/<int:project_id>", methods=["GET", "POST"])
def edit_project(project_id):
    db = get_db()
    project = db.execute("SELECT * FROM projects WHERE id = ?", (project_id,)).fetchone()

    if project is None:
        flash("Project not found.", "error")
        db.close()
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        name        = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()
        owner       = request.form.get("owner", "").strip()
        status      = request.form.get("status")
        milestone   = request.form.get("milestone", "").strip()

        db.execute(
            "UPDATE projects SET name=?, description=?, owner=?, status=?, milestone=? WHERE id=?",
            (name, description, owner, status, milestone, project_id)
        )
        db.commit()
        db.close()

        flash(f'Project "{name}" updated.', "success")
        return redirect(url_for("dashboard"))

    db.close()
    return render_template("edit_project.html", project=project)


@app.route("/projects/delete/<int:project_id>", methods=["POST"])
def delete_project(project_id):
    db = get_db()
    project = db.execute("SELECT name FROM projects WHERE id = ?", (project_id,)).fetchone()

    if project:
        db.execute("DELETE FROM projects WHERE id = ?", (project_id,))
        db.commit()
        flash(f'Project "{project["name"]}" deleted.', "success")

    db.close()
    return redirect(url_for("dashboard"))


# ── Newsletter Generator ───────────────────────────────────────────────────────

@app.route("/newsletter")
def newsletter_page():
    db = get_db()
    projects = db.execute("SELECT * FROM projects ORDER BY created_at DESC").fetchall()
    db.close()
    return render_template("newsletter.html", projects=projects, newsletter=None)


@app.route("/newsletter/generate", methods=["POST"])
def generate_newsletter_route():
    db = get_db()
    projects = db.execute("SELECT * FROM projects ORDER BY created_at DESC").fetchall()
    db.close()

    if not projects:
        flash("No projects found. Add some projects first before generating a newsletter.", "error")
        return redirect(url_for("newsletter_page"))

    # build a plain text summary of projects for the AI
    project_data = []
    for p in projects:
        project_data.append({
            "name": p["name"],
            "description": p["description"],
            "owner": p["owner"],
            "status": p["status"],
            "milestone": p["milestone"]
        })

    newsletter_text = generate_newsletter(project_data)
    return render_template("newsletter.html", projects=projects, newsletter=newsletter_text)


# ── AI Chat (Literacy Bot) ─────────────────────────────────────────────────────

@app.route("/chat")
def chat_page():
    return render_template("chat.html")


@app.route("/chat/send", methods=["POST"])
def chat_send():
    data = request.get_json()
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    response = get_chat_response(user_message)
    return jsonify({"response": response})


# ── Run ────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app.run(debug=True)
