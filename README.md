# AI Virtual Mouse

Control your computer mouse cursor using a **blue object** and your webcam! Point a blue pen, marker, or bottle cap at your camera, and watch the cursor follow it in real-time.

## 🎯 Features

- 🎥 **Live Webcam Feed** – See what the app sees in your browser
- 🖱️ **Move Cursor** – Move a blue object to control the mouse
- 🖱️‍➡️ **Click** – Move the object closer to click
- 🎨 **HSV Tuning** – Adjust color detection in real-time with sliders
- 📺 **Mask Preview** – See exactly what the app detects
- 🖥️ **Web-Based** – Works in any modern browser

---

## 📋 Prerequisites

Before you start, make sure you have:

- **Python 3.7 or later** ([download here](https://www.python.org/downloads/))
- A **webcam** (built-in or USB)
- A **blue object** (blue pen, bottle cap, sticky note, etc.)
- **Internet browser** (Chrome, Firefox, Safari, Edge, etc.)

---

## 🚀 Quick Start (5 minutes)

### Step 1: Download the Project

```bash
git clone https://github.com/ranahafsrajput862-design/ai-mouse.git
cd ai-mouse
```

Or download as ZIP and extract it.

### Step 2: Create a Virtual Environment (Recommended)

This isolates the project and prevents conflicts with other Python projects.

**On Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

After running this, you should see `(.venv)` at the start of your terminal line.

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs all required libraries (Flask, OpenCV, PyAutoGUI, NumPy, etc.).

### Step 4: Run the Server

```bash
python app.py
```

You should see output like:
```
 * Running on http://127.0.0.1:5000
```

### Step 5: Open in Browser

Open your web browser and go to:

```
http://127.0.0.1:5000
```

You should see the AI Virtual Mouse interface with a video feed.

---

## 📖 How to Use

### 1. **Allow Camera Access**
   - Your browser will ask for permission to access your webcam
   - Click **"Allow"** to proceed

### 2. **Show a Blue Object**
   - Hold a **blue object** (pen, marker, bottle cap) in front of your camera
   - The app will detect it and show a green circle around it

### 3. **Move the Cursor**
   - Move your blue object around – the mouse cursor follows it
   - The cursor position is shown on the overlay

### 4. **Click**
   - Move the object **closer** to the camera (make it bigger)
   - When the area is large enough, you'll see "CLICK" text
   - The cursor will click automatically

### 5. **Adjust Color Detection** (if detection isn't working)
   - Use the **HSV sliders** on the right side
   - Adjust them until the **mask preview** shows your object in white
   - Click **"Apply HSV"** to save changes

### 6. **Enable Mouse Control** (Optional)
   - Check the **"Enable Mouse"** checkbox to actually control your computer's mouse
   - Leave unchecked to just test detection

---

## 🛠️ Troubleshooting

### Camera Not Showing
- Make sure you allowed browser camera access
- Check if another app is using your webcam
- Try refreshing the browser (`Ctrl+R` or `Cmd+R`)

### Blue Object Not Detected
- Make sure your object is **bright blue** (not dark or purple)
- Adjust the **HSV sliders** to match your object's color
- The **mask preview** should show your object in white

### Mouse Not Moving
- Check the **"Enable Mouse"** checkbox
- Make sure you're in a supported operating system (Windows, macOS, Linux)
- Try running the app in a different browser

### "Camera access denied" Error
- Your browser blocked camera access
- Go to browser settings → Privacy → Camera → Allow this site

---

## 📁 Project Structure

```
ai-mouse/
├── app.py                 # Main Flask server
├── color_tracking.py      # Blue object detection logic
├── controller.py          # Mouse movement/click control
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── templates/
    └── index.html        # Web interface (HTML/CSS/JavaScript)
```

---

## 💻 System Requirements

| Requirement | Minimum | Recommended |
|---|---|---|
| Python | 3.7 | 3.9+ |
| RAM | 512 MB | 2 GB |
| CPU | Dual Core | Quad Core |
| Webcam | 720p | 1080p |
| Internet | None | Broadband |

---

## 🎓 How It Works (Technical)

1. **Browser captures webcam video** using HTML5 `getUserMedia`
2. **Sends frames to server** via `/frame` endpoint
3. **Server detects blue objects** using HSV color space and OpenCV
4. **Calculates cursor position** based on object location
5. **Moves mouse** using PyAutoGUI library
6. **Returns detection data** (with mask preview) back to browser

---

## ⌨️ Keyboard Shortcuts

- `Ctrl+C` – Stop the server (in terminal)
- `F5` – Reload browser
- `F12` – Open developer console (for debugging)

---

## 🐛 Common Issues & Fixes

| Issue | Solution |
|---|---|
| `ModuleNotFoundError: No module named 'flask'` | Run `pip install -r requirements.txt` |
| `Port 5000 already in use` | Close other apps using port 5000, or change port in `app.py` |
| `Permission denied` (macOS/Linux) | Run `chmod +x app.py` before running |
| Slow detection | Reduce webcam resolution in browser settings |

---

## 📝 Configuration

Edit **environment variables** before running:

```bash
# Use browser camera (default)
set VIDEO_SOURCE=browser

# Enable mouse control (default: disabled for safety)
set PERFORM_MOUSE=false
```

Or in `app.py`, change these lines at the top:
```python
VIDEO_SOURCE = os.environ.get('VIDEO_SOURCE', 'browser')
perform_mouse = os.environ.get('PERFORM_MOUSE', 'false')
```

---

## 📞 Support

If you encounter issues:
1. Check the **browser console** (`F12` → Console tab)
2. Check the **terminal output** for error messages
3. Open an issue on GitHub with error details

---

## 📜 License

This project is open-source and available for personal and educational use.

---

**Enjoy controlling your mouse with AI! 🎉**
