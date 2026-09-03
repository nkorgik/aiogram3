# Lesson 2 – Routers and Modular Structure

[Watch the tutorial on YouTube](https://www.youtube.com/@python-javascript/videos)

In this lesson, we refactor the bot from Lesson 1 to use **Routers**. This allows us to split our code into multiple files, making it easier to maintain as the bot grows.

## New Structure

- `main.py`: Entry point. Initializes the bot and dispatcher, and includes routers.
- `handlers.py`: Contains the command handlers, registered via a `Router`.

## 1. Install dependencies

```bash
# If you haven't created a venv yet:
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
python -m pip install -r ../lesson_1/requirements.txt
```

## 2. Configure the bot token

1. Copy your `.env` file from `lesson_1` or create a new one.
2. Ensure `BOT_TOKEN` is set.

## 3. Run the bot

```bash
python main.py
```

The bot behaves exactly the same as in Lesson 1, but the code is now modular!
