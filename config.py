import os

BOT_TOKEN = os.getenv("BOT_TOKEN", "8435705646:AAEJULzHr7N2Z-lleYsoQKf36yVnHxd0iXU")
ADMIN_ID = int(os.getenv("ADMIN_ID", 7617397626))

MANDATORY_CHANNELS = [
    "@your_channel_1",
    "@your_channel_2"
]

DOWNLOAD_PATH = "downloads"

MAX_FILE_SIZE_MB = 100
