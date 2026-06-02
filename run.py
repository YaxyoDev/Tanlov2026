import asyncio, logging 

from loader import dp, bot, ThrottleMiddleware, menu_commands
from handlers.start import start_router
from handlers.accept_files import accept_router
from handlers.admin import admin_router
from handlers.error import error_router



dp.message.middleware(ThrottleMiddleware(1.0))

dp.include_router(start_router)
dp.include_router(admin_router)
dp.include_router(accept_router)

dp.include_router(error_router)

async def main():
    await menu_commands()
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())