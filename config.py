import os
from dotenv import load_dotenv

load_dotenv()

# --- Camera Settings ---
# RTSP URL format: rtsp://username:password@ip_address:port/Streaming/Channels/101
# Default is set to the one found in your existing cctv.py, but using env vars is safer.
RTSP_URL = os.getenv("RTSP_URL", "rtsp://admin:admin123@192.168.18.88/ISAPI/Streaming/Channels/101?transportmode=unicast")

# --- Detection Settings ---
MODEL_PATH = "yolov8n.pt"  # Will be downloaded automatically by ultralytics
CONFIDENCE_THRESHOLD = 0.5 # Confidence score to trigger detection (0.0 - 1.0)
NIGHT_MODE_ENHANCEMENT = True # Apply CLAHE contrast enhancement

# --- Notification Settings ---
# Telegram Bot Token (Get from @BotFather)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
# Telegram Chat ID (Get from @userinfobot or similar)
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "YOUR_CHAT_ID_HERE")

# --- System Settings ---
COOLDOWN_SECONDS = 30 # Time to wait between alerts to prevent spam
SNAPSHOT_DIR = "snapshots" # Directory to save detected images
