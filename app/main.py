# import threading
# import uvicorn
# from .api import app
# from .bot import run_bot
# from .settings import settings
#
# if __name__ == "__main__":
#     threading.Thread(target=run_bot, daemon=True).start()
#
#     uvicorn.run(
#         app,
#         host=settings.HOST,
#         port=settings.PORT,
#     )