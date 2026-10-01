import os
import json
import uuid
from functools import wraps
from flask import (
    Flask, render_template, request, redirect, url_for, session, flash
)
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "super-secret-key-change-this-in-production")

# Credentials for Admin
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "your_secure_password"

DATA_FILE = "profile.json"
UPLOAD_FOLDER = os.path.join("static", "uploads", "videos")
ALLOWED_EXTENSIONS = {"mp4", "webm", "ogg", "mov"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
# Set max file size limit to 50MB
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def load_profile():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_profile(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

@app.context_processor
def inject_profile():
    return dict(profile=load_profile())

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("is_admin"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

# ==================== PUBLIC ROUTES ====================

@app.route("/")
@app.route("/index.html")
def home():
    return render_template("index.html")

@app.route("/projects")
@app.route("/projects.html")
def projects():
    return render_template("projects.html")

@app.route("/skills")
@app.route("/skills.html")
def skills():
    return render_template("skills.html")

@app.route("/experience")
@app.route("/experience.html")
def experience():
    return render_template("experience.html")

@app.route("/education")
@app.route("/education.html")
def education():
    return render_template("education.html")

@app.route("/contact")
@app.route("/contact.html")
def contact():
    return render_template("contact.html")

# ==================== AUTHENTICATION & ADMIN ====================

@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("is_admin"):
        return redirect(url_for("admin"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["is_admin"] = True
            flash("Logged in successfully!", "success")
            return redirect(url_for("admin"))
        else:
            flash("Invalid username or password.", "error")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("is_admin", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))

@app.route("/admin", methods=["GET", "POST"])
@login_required
def admin():
    profile = load_profile()

    if request.method == "POST":
        # 1. Basic Profile
        profile["name"] = request.form.get("name", "").strip()
        profile["title"] = request.form.get("title", "").strip()
        profile["bio"] = request.form.get("bio", "").strip()

        # 2. Contact Details
        profile["contact"]["email"] = request.form.get("email", "").strip()
        profile["contact"]["phone"] = request.form.get("phone", "").strip()
        profile["contact"]["location"] = request.form.get("location", "").strip()
        profile["contact"]["github"] = request.form.get("github", "").strip()
        profile["contact"]["linkedin"] = request.form.get("linkedin", "").strip()

        # 3. Technical Skills
        skill_categories = request.form.getlist("skill_category[]")
        skill_items_list = request.form.getlist("skill_items[]")
        updated_skills = {}
        for cat, items_str in zip(skill_categories, skill_items_list):
            cat_clean = cat.strip()
            if cat_clean:
                updated_skills[cat_clean] = [s.strip() for s in items_str.split(",") if s.strip()]
        profile["skills"] = updated_skills

        # 4. Featured Projects with Video Uploads
        p_titles = request.form.getlist("p_title[]")
        p_categories = request.form.getlist("p_category[]")
        p_descs = request.form.getlist("p_description[]")
        p_techs = request.form.getlist("p_tech_stack[]")
        p_githubs = request.form.getlist("p_github[]")
        p_demos = request.form.getlist("p_live_demo[]")
        p_video_urls = request.form.getlist("p_video_url[]")
        existing_video_files = request.form.getlist("p_existing_video[]")
        uploaded_files = request.files.getlist("p_video_file[]")

        updated_projects = []
        for i in range(len(p_titles)):
            title = p_titles[i].strip()
            if not title:
                continue

            # Determine existing or new video upload
            saved_filename = existing_video_files[i] if i < len(existing_video_files) else ""
            if i < len(uploaded_files):
                file = uploaded_files[i]
                if file and file.filename != "" and allowed_file(file.filename):
                    ext = file.filename.rsplit(".", 1)[1].lower()
                    unique_name = f"{uuid.uuid4().hex[:12]}_{secure_filename(file.filename)}"
                    file.save(os.path.join(app.config["UPLOAD_FOLDER"], unique_name))
                    saved_filename = unique_name

            updated_projects.append({
                "title": title,
                "category": p_categories[i].strip(),
                "description": p_descs[i].strip(),
                "tech_stack": [t.strip() for t in p_techs[i].split(",") if t.strip()],
                "github": p_githubs[i].strip(),
                "live_demo": p_demos[i].strip() if i < len(p_demos) else "",
                "video_file": saved_filename,
                "video_url": p_video_urls[i].strip() if i < len(p_video_urls) else ""
            })
        profile["projects"] = updated_projects

        # 5. Academic Details
        profile["education"]["degree"] = request.form.get("degree", "").strip()
        profile["education"]["institution"] = request.form.get("institution", "").strip()
        profile["education"]["period"] = request.form.get("education_period", "").strip()
        profile["education"]["coursework"] = request.form.get("coursework", "").strip()

        # 6. Project Domains
        domains_raw = request.form.get("project_domains", "")
        profile["project_domains"] = [d.strip() for d in domains_raw.split(",") if d.strip()]

        save_profile(profile)
        flash("All portfolio details & video uploads updated successfully!", "success")
        return redirect(url_for("admin"))

    domains_str = ", ".join(profile.get("project_domains", []))
    return render_template("admin.html", profile=profile, domains_str=domains_str)

@app.errorhandler(404)
def page_not_found(e):
    return render_template("index.html"), 404

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)