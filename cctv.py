import cv2

def display_cctv_feed():
    ip = "192.168.18.88"
    username = "admin"
    password = "admin123"
    
    # RTSP URL with transport protocol specified
    rtsp_url = f"rtsp://{username}:{password}@{ip}/ISAPI/Streaming/Channels/101?transportmode=unicast"
    
    # Set OpenCV to use FFMPEG with buffer options
    cap = cv2.VideoCapture(rtsp_url, cv2.CAP_FFMPEG)
    
    # Additional buffer configuration
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 3)
    cap.set(cv2.CAP_PROP_FPS, 20)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'H264'))
    
    if not cap.isOpened():
        print("Error: Could not open video stream")
        return
    
    print("Connected - Press 'q' to quit")
    
    while True:
        try:
            ret, frame = cap.read()
            if not ret:
                print("Frame read error - reconnecting...")
                cap.release()
                cap = cv2.VideoCapture(rtsp_url, cv2.CAP_FFMPEG)
                continue
                
            cv2.imshow('CCTV Feed', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
        except KeyboardInterrupt:
            break
    
    cap.release()
    cv2.destroyAllWindows()

display_cctv_feed()