# Lesson 4 – FSM & Comprehensive Example

[Watch the tutorial on YouTube](https://www.youtube.com/@python-javascript/videos)

In this lesson, we build a **Developer Survey Bot** to demonstrate the power of **FSM (Finite State Machine)**, **Reply Keyboards**, and **Inline Keyboards**.

## Features

1.  **FSM (Finite State Machine)**: Tracks the user's progress through the survey (Name -> Language -> Experience).
2.  **Reply Keyboard**: Used for selecting the programming language.
3.  **Inline Keyboard**: Used for selecting experience level and confirming the submission.
4.  **HTML Formatting**: Used for styling the summary message.

## New Files

-   `states.py`: Defines the states (`Survey.name`, `Survey.language`, etc.).
-   `keyboards.py`: Contains the keyboard builders.
-   `handlers.py`: Contains the logic for handling each step of the survey.

## 1. Install dependencies

```bash
# If you haven't created a venv yet:
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
python -m pip install -r ../lesson_1/requirements.txt
```

## 2. Configure the bot token

1.  Copy `.env.example` to `.env`.
2.  Set your `BOT_TOKEN`.

## 3. Run the bot

```bash
python main.py
```
