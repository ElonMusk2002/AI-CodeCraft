# recommender.py

import google.generativeai as genai
from app.models import CodingChallenge
from flask import current_app


def generate_coding_challenge(user):
    genai.configure(api_key=current_app.config["GEMINI_API_KEY"])
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = (
        f"Generate a coding challenge for a user with skill level {user.skill_level} "
        f"who is interested in {user.preferred_languages} and {user.preferred_topics}."
    )

    try:
        response = model.generate_content(prompt, stream=True)

        challenge_data = ""
        for chunk in response:
            if hasattr(chunk, "text"):
                challenge_data += chunk.text
            else:
                print(f"Received non-text chunk: {chunk}")

        if not challenge_data.strip():
            raise ValueError("Received empty or invalid content from the model.")

        challenge_lines = challenge_data.split("\n")
        if len(challenge_lines) < 2:
            raise ValueError("Challenge data format is incorrect.")

        title = challenge_lines[0].strip()
        description = "\n".join(challenge_lines[1:]).strip()
        difficulty = user.skill_level
        programming_language = user.preferred_languages
        topic = user.preferred_topics

        challenge = CodingChallenge(
            title=title,
            description=description,
            difficulty=difficulty,
            programming_language=programming_language,
            topic=topic,
        )

        return challenge

    except Exception as e:
        print(f"An error occurred while generating the coding challenge: {e}")
        raise


def evaluate_solution(user_solution, challenge):
    genai.configure(api_key=current_app.config["GEMINI_API_KEY"])
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = f"Evaluate the user's solution for the coding challenge '{challenge.title}' on a scale of 1 to 10. User's solution: {user_solution}"

    try:
        response = model.generate_content(prompt, stream=True)

        evaluation_data = ""
        for chunk in response:
            if hasattr(chunk, "text"):
                evaluation_data += chunk.text
            else:
                print(f"Received non-text chunk: {chunk}")

        if not evaluation_data.strip():
            raise ValueError("Received empty response from the model.")

        if evaluation_data.strip().isdigit():
            score = int(evaluation_data.strip())
        else:
            raise ValueError("The response did not contain a valid numeric score.")

        return score

    except Exception as e:
        print(f"An error occurred while evaluating the solution: {e}")
        raise
