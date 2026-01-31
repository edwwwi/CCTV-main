import cv2
import time
import os
import datetime
import config
from detection import HumanDetector
from notifier import send_telegram_alert

def ensure_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def main():
    print("=== Night-Time CCTV Human Detection System ===")
    
    ensure_directory(config.SNAPSHOT_DIR)
    
    # Initialize component
    try:
        detector = HumanDetector()
    except Exception as e:
        print(f"CRITICAL: Failed to initialize detector: {e}")
        return

    # Connection Loop
    while True:
        try:
            print(f"[*] Connecting to RTSP stream: {config.RTSP_URL}")
            # Use FFMPEG for better compatibility
            cap = cv2.VideoCapture(config.RTSP_URL, cv2.CAP_FFMPEG)
            
            # Reduce buffer size to minimize latency
            cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            
            if not cap.isOpened():
                print("[-] Failed to open stream. Retrying in 5 seconds...")
                time.sleep(5)
                continue
                
            print("[+] Stream connected successfully.")
            
            last_alert_time = 0
            frame_count = 0
            process_every_n_frames = 5 # Process every 5th frame to save CPU
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("[-] Frame read failed. Stream might have dropped.")
                    break
                
                frame_count += 1
                if frame_count % process_every_n_frames != 0:
                    continue
                
                try:
                    # Run Detection
                    is_human, result = detector.detect(frame)
                    
                    if is_human:
                        current_time = time.time()
                        if current_time - last_alert_time > config.COOLDOWN_SECONDS:
                            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                            print(f"[!] Human Detected at {timestamp}!")
                            
                            # Draw boxes on the frame for the alert
                            annotated_frame = result[0].plot() # plot() returns BGR numpy array
                            
                            # Update last alert time immediately to prevent double sends
                            last_alert_time = current_time
                            
                            # Save Image
                            filename = f"alert_{timestamp}.jpg"
                            filepath = os.path.join(config.SNAPSHOT_DIR, filename)
                            cv2.imwrite(filepath, annotated_frame)
                            print(f"    Saved snapshot: {filepath}")
                            
                            # Send Notification
                            print("    Sending notification...")
                            if send_telegram_alert(filepath, caption=f"Human Detected at {datetime.datetime.now().strftime('%H:%M:%S')}!"):
                                print("    Notification sent.")
                            else:
                                print("    Notification failed.")
                                
                    # Optional: Display feed locally if running on a machine with a screen
                    # cv2.imshow("CCTV Monitor", frame)
                    # if cv2.waitKey(1) & 0xFF == ord('q'):
                    #    cap.release()
                    #    return

                except Exception as e:
                    print(f"[-] Error during processing loop: {e}")
                    # Don't break the loop, just skip this frame
                    continue
                    
        except KeyboardInterrupt:
            print("\n[!] Stopping system...")
            break
        except Exception as e:
            print(f"[-] unexpected error: {e}")
            time.sleep(5)
            
    if 'cap' in locals():
        cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
