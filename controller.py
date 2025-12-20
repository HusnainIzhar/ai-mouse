import pyautogui
import numpy as np
import time

class MouseController:
    def __init__(self, screen_w, screen_h, frame_r=100):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.frame_r = frame_r # Frame Reduction
        self.plocX, self.plocY = 0, 0 # Previous locations
        self.clocX, self.clocY = 0, 0 # Current locations
        self.smoothening = 7 # Smoothening factor

    def move_mouse(self, x1, y1, w, h):
        # Convert coordinates
        x3 = np.interp(x1, (self.frame_r, w - self.frame_r), (0, self.screen_w))
        y3 = np.interp(y1, (self.frame_r, h - self.frame_r), (0, self.screen_h))

        # Smoothen values
        self.clocX = self.plocX + (x3 - self.plocX) / self.smoothening
        self.clocY = self.plocY + (y3 - self.plocY) / self.smoothening

        # Move Mouse
        try:
            pyautogui.moveTo(self.screen_w - self.clocX, self.clocY) # Flip X for mirror effect
        except pyautogui.FailSafeException:
            pass # Ignore failsafe for now
        
        self.plocX, self.plocY = self.clocX, self.clocY

    def click(self):
        pyautogui.click()
        
    def scroll(self, direction):
        # direction: 1 for up, -1 for down
        pyautogui.scroll(direction * 100)
