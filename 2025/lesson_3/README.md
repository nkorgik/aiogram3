# Lesson 3 – Keyboards

[Watch the tutorial on YouTube](https://www.youtube.com/@python-javascript/videos)

In this lesson, we learn how to use **Reply Keyboards** and **Inline Keyboards**.

## Features

1.  **Reply Keyboard**: A menu with buttons that appears instead of the user's keyboard.
    -   Shown automatically on `/start`.
    -   Buttons: "👋 Hello", "ℹ️ Help".
2.  **Inline Keyboard**: Buttons that appear under a message.
    -   Triggered by `/counter`.
    -   Interactive counter with `+` and `-` buttons.

## New Files

-   `keyboards.py`: Contains the keyboard builders.
-   `handlers.py`: Handles button clicks and callbacks.

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
