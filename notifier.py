import requests
import config
import os

def send_telegram_alert(image_path, caption="Human Detected!"):
    """
    Sends an image with a caption to the configured Telegram chat.
    """
    token = config.TELEGRAM_BOT_TOKEN
    chat_id = config.TELEGRAM_CHAT_ID
    
    if "YOUR_BOT_TOKEN" in token or "YOUR_CHAT_ID" in chat_id:
        print("[!] Telegram credentials not set. Skipping notification.")
        return False

    url = f"https://api.telegram.org/bot{token}/sendPhoto"
    
    try:
        with open(image_path, "rb") as image_file:
            payload = {
                "chat_id": chat_id,
                "caption": caption
            }
            files = {
                "photo": image_file
            }
            response = requests.post(url, data=payload, files=files, timeout=10)
            
            if response.status_code == 200:
                print(f"[+] Alert sent successfully to Telegram.")
                return True
            else:
                print(f"[-] Failed to send Telegram alert. Status: {response.status_code}, Response: {response.text}")
                return False
    except Exception as e:
        print(f"[-] Error sending Telegram alert: {e}")
        return False
