import logging
import os
import openai
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.environ["TG_API_KEY"])
dp = Dispatcher(bot)


def text_complition(prompt: str) -> dict:
    try:
        openai.api_key = os.environ["API_KEY"]
        openai.Model.list()
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"Human: {prompt}\nAI: ",
            temperature=0.9,
            max_tokens=1024,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
            stop=["Human:", "AI:"],
        )
        return {"status": 1, "response": response["choices"][0]["text"]}
    except:
        return {"status": 0, "response": ""}


@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi! I am chatGPT bot :)")


@dp.message_handler()
async def say(message: types.Message):
    my_text = text_complition(message)
    // print(my_text["response"])
    await message.reply(my_text["response"])


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
