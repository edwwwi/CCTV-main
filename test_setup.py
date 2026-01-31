import config
import os
import sys

def test_setup():
    print("=== System Verification ===")
    
    # 1. Check Config
    print(f"[*] Checking configuration...")
    if "YOUR_" in config.TELEGRAM_BOT_TOKEN:
        print("[-] WARNING: Telegram Token not set in config.py")
    else:
        print("[+] Telegram Token set.")
        
    print(f"[*] RTSP URL: {config.RTSP_URL}")
    
    # 2. Check Dependencies & Model
    print(f"[*] Loading Detection Module (this will download the model if missing)...")
    try:
        from detection import HumanDetector
        detector = HumanDetector()
        print("[+] Model loaded successfully.")
    except Exception as e:
        print(f"[-] CRITICAL: Model load failed: {e}")
        return

    # 3. Check Directory Write Access
    try:
        if not os.path.exists(config.SNAPSHOT_DIR):
            os.makedirs(config.SNAPSHOT_DIR)
        test_file = os.path.join(config.SNAPSHOT_DIR, "test_write.txt")
        with open(test_file, "w") as f:
            f.write("test")
        os.remove(test_file)
        print("[+] Snapshot directory is writable.")
    except Exception as e:
        print(f"[-] Error checking directory: {e}")

    print("\n=== Verification Complete ===")
    print("If all checks passed, you can run 'python main.py'")

if __name__ == "__main__":
    test_setup()
