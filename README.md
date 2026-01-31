# Night-Time CCTV Human Detection System

A lightweight, automated system to detect humans in your CCTV feed during the night and send image alerts to Telegram.

## Features
- **Real-time Human Detection**: Uses YOLOv8 (Nano) for fast and accurate detection.
- **Night Vision Enhancement**: Applies CLAHE (Contrast Limited Adaptive Histogram Equalization) to improve detection in dark/IR footage.
- **Instant Alerts**: Sends a photo to your Telegram immediately upon detection.
- **Smart Cooldown**: Prevents spamming by waiting 30 seconds between alerts.
- **Serverless Friendly**: Can run on Google Colab, a free VPS, or any local PC.

## Prerequisites
1.  **Python 3.8+**
2.  **RTSP Stream Access**:
    *   If running **locally** (same network as camera): Use the local IP (e.g., `192.168.18.88`).
    *   If running **cloud/remote** (Colab, VPS): You MUST enable **Port Forwarding** on your router for port 554 (RTSP) to your camera's IP. Your URL will look like `rtsp://user:pass@YOUR_PUBLIC_IP:554/...`.

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure the System
Open `config.py` and update the following:

-   **RTSP_URL**: Your camera's stream URL.
    -   Hikvision Default: `rtsp://admin:password@IP:554/ISAPI/Streaming/Channels/101`
-   **TELEGRAM_BOT_TOKEN**:
    1.  Open Telegram and search for **@BotFather**.
    2.  Send `/newbot` and follow instructions to get a Token.
    3.  Paste the token in `config.py`.
-   **TELEGRAM_CHAT_ID**:
    1.  Search for **@userinfobot** in Telegram.
    2.  Click Start to get your numeric ID (e.g., 123456789).
    3.  Paste it in `config.py`.

### 3. Run the System
```bash
python main.py
```

## Running on Google Colab (Free Cloud)
1.  Upload all files (`main.py`, `detection.py`, `notifier.py`, `config.py`, `requirements.txt`) to your Google Drive.
2.  Open a new Colab Notebook.
3.  Mount Drive:
    ```python
    from google.colab import drive
    drive.mount('/content/drive')
    %cd /content/drive/MyDrive/path_to_your_folder
    ```
4.  Install & Run:
    ```python
    !pip install -r requirements.txt
    !python main.py
    ```
    *Note: Colab sessions time out. For 24/7, use a Cheap VPS (e.g., Oracle Cloud Free Tier).*

## Troubleshooting
-   **"Failed to open stream"**:
    -   Check if the IP is correct.
    -   If remote, check if Port Forwarding is active (test with VLC Media Player on your phone using 4G).
-   **"Error loading model"**:
    -   Ensure you have internet connection for the first run to download `yolov8n.pt`.

