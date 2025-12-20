from flask import Flask, render_template, Response
import cv2
import time
import numpy as np
import color_tracking as ct
import controller as mc
import pyautogui

app = Flask(__name__)

##########################
wCam, hCam = 640, 480
frameR = 100 # Frame Reduction
smoothening = 7
##########################

# Initialize Tracker and Mouse
# Note: PyAutoGUI might have issues running in a background thread or server context 
# depending on the OS, but for a local Flask app it usually works if the user is logged in.
tracker = ct.ColorTracker()
mouse = mc.MouseController(pyautogui.size()[0], pyautogui.size()[1], frameR)

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

def generate_frames():
    last_click_time = 0
    
    while True:
        success, img = cap.read()
        if not success:
            break
            
        # Flip image for mirror view
        img = cv2.flip(img, 1)
            
        # Find Color Object
        info = tracker.findColor(img)
        
        if len(info) != 0:
            cx, cy, area = info
            
            # Draw Boundary Box for Mouse Movement
            cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),
                          (255, 0, 255), 2)
            
            # Move Mouse
            mouse.move_mouse(cx, cy, wCam, hCam)
            
            # Click Logic
            if area > 2000: 
                cv2.putText(img, "Clicking", (cx, cy - 20), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
                if time.time() - last_click_time > 0.5:
                    mouse.click()
                    last_click_time = time.time()

        # Encode frame
        ret, buffer = cv2.imencode('.jpg', img)
        frame = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
