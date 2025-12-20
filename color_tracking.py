import cv2
import numpy as np

class ColorTracker:
    def __init__(self):
        # Default Color: Blue (HSV)
        # H: 100-130, S: 50-255, V: 50-255
        self.lower_color = np.array([100, 50, 50])
        self.upper_color = np.array([130, 255, 255])
        self.kernel = np.ones((5, 5), np.uint8)

    def findColor(self, img, draw=True):
        imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(imgHSV, self.lower_color, self.upper_color)
        
        # Morphological operations to remove noise
        mask = cv2.erode(mask, self.kernel, iterations=1)
        mask = cv2.dilate(mask, self.kernel, iterations=2)
        
        self.mask = mask # Store for display if needed
        
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        x, y, w, h = 0, 0, 0, 0
        area = 0
        
        # Find biggest contour
        maxArea = 0
        bestCnt = None
        
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 500: # Minimum area to detect
                if area > maxArea:
                    maxArea = area
                    bestCnt = cnt
                    
        if bestCnt is not None:
            x, y, w, h = cv2.boundingRect(bestCnt)
            cx, cy = x + w // 2, y + h // 2
            if draw:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)
            return [cx, cy, maxArea]
            
        return []

    def get_mask(self):
        return self.mask
