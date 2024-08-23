# CodeCraft: Personalized Coding Challenge Platform

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google_Gemini-AI-4285F4?style=for-the-badge&logo=google&logoColor=white)

## Overview

CodeCraft is a simple web application that generates personalized coding challenges for users based on their skill level, preferred programming languages, and topics of interest. It leverages Google's Gemini AI to create unique challenges and evaluate user solutions.

## Demo

A demonstration video of CodeCraft in action is available in the `demo` folder of this repository. 


## Features

- User registration and authentication
- Personalized user profiles
- AI-generated coding challenges
- Automated solution evaluation
- Progress tracking and leaderboard
- Hint system for challenging problems

## Technology Stack

- **Backend**: Python, Flask
- **Database**: SQLAlchemy ORM
- **AI Integration**: Google Generative AI (Gemini)

## Key Components

### Models (`models.py`)

- `UserProfile`: Stores user information, including completed challenges
- `CodingChallenge`: Represents individual coding challenges

### Forms (`forms.py`)

- `RegistrationForm`: User registration
- `LoginForm`: User login
- `ProfileForm`: User profile updates

### Routes (`routes.py`)

- User authentication (register, login, logout)
- Dashboard and profile management
- Challenge recommendation and completion
- Leaderboard
- Hint generation

### Recommender (`recommender.py`)

- `generate_coding_challenge()`: Creates personalized challenges using Gemini AI
- `evaluate_solution()`: Assesses user solutions with AI

## Setup and Installation

(Include steps for setting up the project, such as:)

1. Clone the repository
2. Install dependencies
3. Set up environment variables (including GEMINI_API_KEY)
4. Initialize the database
5. Run the Flask application

## Usage

1. Register for an account
2. Update your profile with skill level and preferences
3. Navigate to the dashboard to receive personalized coding challenges
4. Solve challenges and submit solutions for AI evaluation
5. Track your progress and compare with others on the leaderboard


## Contributing

Contributions are welcome! If you have a feature request or bug report, please open an issue on GitHub. If you wish to contribute code, please fork the repository, make your changes, and submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.