# routes.py

from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request,
    jsonify,
    current_app,
)
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import RegistrationForm, LoginForm, ProfileForm
from app.models import UserProfile, CodingChallenge
from app import db
from app.recommender import generate_coding_challenge
import google.generativeai as genai
import re

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bp = Blueprint("routes", __name__)


@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = UserProfile(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you are now a registered user!", "success")
        return redirect(url_for("routes.login"))
    return render_template("register.html", form=form)


@bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = UserProfile.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash("You have been logged in.", "success")
            return redirect(url_for("routes.dashboard"))
        else:
            flash("Invalid email or password.", "danger")
    return render_template("login.html", form=form)


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("routes.index"))


@bp.route("/dashboard")
@login_required
def dashboard():
    user = current_user
    challenges = user.completed_challenges
    num_challenges = len(challenges)
    return render_template(
        "dashboard.html", challenges=challenges, num_challenges=num_challenges
    )


@bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        current_user.skill_level = form.skill_level.data
        current_user.preferred_languages = form.preferred_languages.data
        current_user.preferred_topics = form.preferred_topics.data
        db.session.commit()
        flash("Your profile has been updated.", "success")
        return redirect(url_for("routes.profile"))
    form.skill_level.data = current_user.skill_level
    form.preferred_languages.data = current_user.preferred_languages
    form.preferred_topics.data = current_user.preferred_topics
    return render_template("profile.html", form=form)


@bp.route("/recommend")
@login_required
def recommend():
    challenge = generate_coding_challenge(current_user)
    db.session.add(challenge)
    db.session.commit()

    return jsonify(
        id=challenge.id,
        title=challenge.title,
        description=challenge.description,
        difficulty=challenge.difficulty,
        programming_language=challenge.programming_language,
        topic=challenge.topic,
    )


@bp.route("/leaderboard")
def leaderboard():
    users = UserProfile.query.order_by(UserProfile.skill_level.desc()).all()
    num_users = len(users)
    return render_template("leaderboard.html", users=users, num_users=num_users)


def parse_ai_response(response_text):
    lines = response_text.split("\n")
    score = None
    feedback = []

    for line in lines:
        if score is None and ("score" in line.lower() or "/10" in line):
            score_match = re.search(r"(\d+)/10", line)
            if score_match:
                score = int(score_match.group(1))
            continue
        feedback.append(line)

    return score, "\n".join(feedback).strip()


@bp.route("/complete/<int:challenge_id>", methods=["POST"])
@login_required
def complete_challenge(challenge_id):
    challenge = CodingChallenge.query.get(challenge_id)

    if challenge and challenge not in current_user.completed_challenges:
        genai.configure(api_key=current_app.config["GEMINI_API_KEY"])
        model = genai.GenerativeModel("gemini-1.5-flash")

        user_solution = request.form.get("solution", "").strip()

        if user_solution.lower() == "i don't know" or user_solution == "":
            flash(
                "It looks like you're having trouble with this challenge. Don't worry, that's normal! Would you like some hints or resources to help you?",
                "info",
            )
            return redirect(url_for("routes.dashboard"))

        prompt = f"Evaluate the user's solution for the coding challenge '{challenge.title}' on a scale of 1 to 10. Provide a brief explanation of the score. User's solution: {user_solution}"

        try:
            response = model.generate_content(prompt, stream=True)
            evaluation_text = ""

            for chunk in response:
                if hasattr(chunk, "text"):
                    evaluation_text += chunk.text

            score = None
            feedback = ""
            score, feedback = parse_ai_response(evaluation_text)
            lines = evaluation_text.split("\n")
            for line in lines:
                if "score" in line.lower() or "/10" in line:
                    score_match = re.search(r"(\d+)/10", line)
                    if score_match:
                        score = int(score_match.group(1))
                    break

            feedback = "\n".join(lines[1:])

            if score is None:
                logger.warning(
                    f"Could not extract numeric score from AI response: {evaluation_text}"
                )
                flash(
                    "We couldn't determine a precise score for your solution, but here's some feedback: "
                    + feedback,
                    "info",
                )
            elif score >= 5:
                current_user.completed_challenges.append(challenge)
                db.session.commit()
                flash(
                    f"Congratulations! You have completed the coding challenge with a score of {score}/10! "
                    + feedback,
                    "success",
                )
            else:
                flash(
                    f"Your solution scored {score}/10. Here's some feedback to help you improve: "
                    + feedback,
                    "info",
                )
        except Exception as e:
            logger.error(f"An error occurred while evaluating the solution: {str(e)}")
            flash(
                "An error occurred while evaluating your solution. Please try again later.",
                "danger",
            )

    else:
        flash(
            "You are not authorized to complete this challenge or it has already been completed.",
            "danger",
        )

    return redirect(url_for("routes.dashboard"))


@bp.route("/hint/<int:challenge_id>")
@login_required
def get_hint(challenge_id):
    challenge = CodingChallenge.query.get(challenge_id)
    if not challenge:
        flash("Challenge not found.", "danger")
        return redirect(url_for("routes.dashboard"))

    genai.configure(api_key=current_app.config["GEMINI_API_KEY"])
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = f"Provide a hint for the coding challenge: '{challenge.title}'. The hint should guide the user without giving away the full solution."

    try:
        response = model.generate_content(prompt)
        hint = response.text
        return render_template("hint.html", challenge=challenge, hint=hint)
    except Exception as e:
        logger.error(f"An error occurred while generating a hint: {str(e)}")
        flash(
            "An error occurred while generating a hint. Please try again later.",
            "danger",
        )
        return redirect(url_for("routes.dashboard"))


@bp.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors."""
    return render_template("404.html"), 404

@bp.errorhandler(500)
def internal_server_error(e):
    """Handle 500 errors."""
    return render_template("500.html"), 500