from flask import Flask, render_template, Response, request, jsonify
import base64
import cv2
import numpy as np
import color_tracking as ct
import controller as mc
import os

app = Flask(__name__)

wCam, hCam = 640, 480
frameR = 100

tracker = ct.ColorTracker()
screen_w, screen_h = 800, 600
try:
    if os.environ.get('DISPLAY'):
        import pyautogui
        screen_w, screen_h = pyautogui.size()[0], pyautogui.size()[1]
except Exception:
    pass

mouse = mc.MouseController(screen_w, screen_h, frameR)

VIDEO_SOURCE = os.environ.get('VIDEO_SOURCE', 'server')
cap = None
if VIDEO_SOURCE == 'server':
    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)

perform_mouse = os.environ.get('PERFORM_MOUSE', 'false').lower() in ('1', 'true', 'yes')


def generate_frames():
    while True:
        if cap is None:
            img = np.zeros((hCam, wCam, 3), dtype=np.uint8)
        else:
            success, img = cap.read()
            if not success:
                break
            img = cv2.flip(img, 1)

        info = tracker.findColor(img)
        if len(info) != 0:
            cx, cy, area = info
            cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)
            mouse.move_mouse(cx, cy, wCam, hCam)
            if area > 2000:
                cv2.putText(img, "Clicking", (cx, cy - 20), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
                mouse.click()

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


@app.route('/frame', methods=['POST'])
def frame():
    try:
        data = request.get_data()
        nparr = np.frombuffer(data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None:
            return jsonify({'error': 'could not decode image'}), 400

        img = cv2.flip(img, 1)
        info = tracker.findColor(img)
        if len(info) == 0:
            return jsonify({'found': False})
        cx, cy, area = info

        try:
            ih, iw = img.shape[:2]
            if perform_mouse:
                mouse.move_mouse(cx, cy, iw, ih)
                if area > 2000:
                    mouse.click()
        except Exception:
            pass

        mask = tracker.get_mask() if hasattr(tracker, 'get_mask') else None
        mask_b64 = None
        try:
            if mask is not None:
                m_bgr = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
                _, mbuf = cv2.imencode('.jpg', m_bgr)
                mask_b64 = base64.b64encode(mbuf.tobytes()).decode('ascii')
        except Exception:
            mask_b64 = None

        return jsonify({'found': True, 'cx': int(cx), 'cy': int(cy), 'area': int(area), 'mask': mask_b64})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/set_mouse', methods=['POST'])
def set_mouse():
    global perform_mouse
    try:
        js = request.get_json(force=True)
        perform_mouse = bool(js.get('perform', False))
        return jsonify({'ok': True, 'perform': perform_mouse})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 400


@app.route('/set_hsv', methods=['POST'])
def set_hsv():
    try:
        js = request.get_json(force=True)
        hmin = int(js.get('hmin', 100))
        hmax = int(js.get('hmax', 130))
        smin = int(js.get('smin', 50))
        smax = int(js.get('smax', 255))
        vmin = int(js.get('vmin', 50))
        vmax = int(js.get('vmax', 255))
        tracker.set_hsv(hmin, hmax, smin, smax, vmin, vmax)
        return jsonify({'ok': True})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 400


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=5000)
