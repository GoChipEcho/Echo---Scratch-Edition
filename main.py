import os
import openai
import scratchattach as scratch3
from keep_alive import keep_alive
from datetime import datetime

session = scratch3.Session(SESSION, username=“PlanetCatYT”)
conn = session.connect_cloud(project_id=“940994317”)
keep_alive()
KEY = os.environ
openai.api_key = KEY
client = scratch3.CloudRequests(conn)

user_histories = {}

user_daily_limits = {}

daily_limit = 10 

@client.request
def test():
    print(“Hello!”)
    return “Hello!”
@client.event
def on_ready():
    print(“Request handler is running”)

def is_next_day(username):
    if username in user_daily_limits:
        last_reset_time = user_daily_limits.get(“last_reset”, datetime.min)
        return datetime.now().date() > last_reset_time.date()
    return False
@client.request
def cat(message, username):
    global user_histories, user_daily_limits

    if is_next_day(username):
        user_daily_limits = {“count”: 0, “last_reset”: datetime.now()}

    user_history = user_histories.setdefault(username, )


    system_message = {“role”: “system”, “content”: “You are a bot on a Scratch project made to help people create projects on Scratch. You were created by a Scratch user named PlanetCatYT. Your name is CatGPT. You can remember previous messages.”}
    if not any(entry == “system” for entry in user_history):
        user_history.insert(0, system_message)

    if user_daily_limits.get(username, {}).get(“count”, 0) >= daily_limit:
        print(username + “ reached the daily limit.”)
        return “Sorry, you've reached the daily limit. Come back tomorrow! If you would like more messages, get CatGPT+ (Check the settings)”

    user_message = {“role”: “user”, “content”: f“{username}: {message}”}
    user_history.append(user_message)

    max_history_length = 10
    if len(user_history) > max_history_length:
        user_history.pop(0)

    response = openai.ChatCompletion.create(
        model=“gpt-3.5-turbo”,
        messages=user_history,
        max_tokens=200,
        temperature=0.5,
    )

    bot_response = response

    bot_message = {“role”: “assistant”, “content”: bot_response}
    user_history.append(bot_message)

    user_daily_limits.setdefault(username, {}).setdefault(“count”, 0)
    user_daily_limits += 1

    user_histories = user_history
    print(user_daily_limits.get(username, {}).get(“count”, 0))
    print(username + “: ” + message)
    print(“Bot: ” + bot_response)

    return str(bot_response) + “ (Message ” + str(user_daily_limits.get(username, {}).get(“count”, 0)) + “/” + str(daily_limit) + “)”

@client.request
def reset(username):
    global user_histories, user_daily_limits
    if username in user_histories:
        user_histories = 
        user_daily_limits.pop(username, None)
        print(f“Reset successful for {username}'s conversation history and daily limit!”)
    else:
        print(f“No conversation history found for the username: {username}”)

client.run()
