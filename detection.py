from ultralytics import YOLO
import cv2
import config

class HumanDetector:
    def __init__(self):
        print(f"[*] Loading YOLO model: {config.MODEL_PATH}...")
        try:
            self.model = YOLO(config.MODEL_PATH)
        except Exception as e:
            print(f"[-] Error loading model: {e}")
            raise e
        self.clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))

    def preprocess(self, frame):
        """
        Applies Contrast Limited Adaptive Histogram Equalization (CLAHE)
        to improve visibility in night vision/IR footage.
        """
        if not config.NIGHT_MODE_ENHANCEMENT:
            return frame
            
        # Convert to LAB color space
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        # Apply CLAHE to L-channel
        cl = self.clahe.apply(l)
        
        # Merge and convert back to BGR
        limg = cv2.merge((cl, a, b))
        enhanced_frame = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
        return enhanced_frame

    def detect(self, frame):
        """
        Detects humans in the frame.
        Returns: (bool values_detected, list detections)
        """
        # Preprocess for night vision
        processed_frame = self.preprocess(frame)
        
        # Run inference
        # class=0 is 'person' in COCO dataset
        results = self.model(processed_frame, classes=[0], conf=config.CONFIDENCE_THRESHOLD, verbose=False)
        
        detections = []
        human_detected = False
        
        for result in results:
            if len(result.boxes) > 0:
                human_detected = True
                # Draw bounding boxes on the ORIGINAL frame for the alert image
                # (You might want to draw on the processed frame, but usually original is better for recognizing context)
                # But since we want to SEE what the AI saw in the dark, maybe processed is better?
                # Let's stick to returning detection status, the visualizer can draw on whichever frame.
                
                # We can return the plotted image directly from ultralytics for convenience
                # but let's just return true for now and let main handle saving.
                return True, result
        
        return False, None
