# AI Virtual Mouse (Web App)

A **Web Application** that allows you to control your mouse cursor using a **colored object** (like a blue pen or bottle cap) captured by your webcam.

## Features
- **Web Interface**: View the camera feed in your browser.
- **Move Cursor**: Hold a **BLUE** object to the camera. The cursor follows it.
- **Click**: Move the object **closer** to the camera (make it appear larger) to click.

## Prerequisites
- Python 3.x installed.
- A webcam.
- A **Blue** object.

## Installation
1. Open the project folder.
2. Run the following command to install dependencies:
   ```bash
   pip install flask opencv-python pyautogui numpy
   ```

## How to Run
1. Run the `app.py` script:
   ```bash
   python app.py
   ```
2. Open your web browser and go to:
   `http://127.0.0.1:5000`
3. Show a **BLUE** object to the camera.
   - **Move**: Move the object around.
   - **Click**: Move the object closer to the camera.
4. Press `Ctrl+C` in the terminal to stop.

## Files
- `app.py`: The Flask server and main logic.
- `templates/index.html`: The web page.
- `color_tracking.py`: Module for detecting the colored object.
- `controller.py`: Module for controlling the mouse.
