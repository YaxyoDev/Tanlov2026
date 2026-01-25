import os
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeDefault
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv



load_dotenv()


bot_token = os.getenv("API_TOKEN")
bot = Bot(bot_token, default=DefaultBotProperties(parse_mode="HTML"))

dp = Dispatcher()


"""Menu command"""

async def menu_commands():
    command = [
        BotCommand(command="start", description="Botni ishga tushirish uchun")
    ]
    await bot.set_my_commands(command, scope=BotCommandScopeDefault())

"""Middle Ware"""

import time
from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Dict, Any

class ThrottleMiddleware(BaseMiddleware):
    def __init__(self, rate_limit: float = 1.0):
        self.rate_limit = rate_limit
        self.last_time = {}

    async def __call__(
        self,
        handler,
        event: Message,
        data: Dict[str, Any]
    ):
        user_id = event.from_user.id
        current_time = time.time()

        last = self.last_time.get(user_id)

        if last and (current_time - last) < self.rate_limit:
            # juda tez yozsa
            await event.answer("⏳ Iltimos, sekinroq yozing")
            return

        self.last_time[user_id] = current_time
        return await handler(event, data)
