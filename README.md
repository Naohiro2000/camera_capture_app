# Camera Capture App

A fun gesture-recognition app using OpenCV and MediaPipe that displays meme images based on your hand gestures and facial expressions!

## Features

- 👆 **Index Finger**: Shows a meme when you point with your index finger
- 🖕 **Middle Finger**: Displays a meme when you raise your middle finger
- 👍 **Thumbs Up**: Shows a meme when you give a thumbs up
- 👅 **Tongue Out**: Displays a meme when you stick your tongue out

## Requirements

- Python 3.8+
- Webcam

## Installation

1. **Clone or download this repository**

2. **Create a virtual environment**
   ```bash
   python3 -m venv .venv
   ```

3. **Activate the virtual environment**
   ```bash
   source .venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## File Structure

```
camera_capture_app/
├── main.py                  # Main application
├── main_im.py              # Alternative implementation
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── .gitignore             # Git ignore rules
├── .venv/                 # Virtual environment (created during setup)
└── imgs/                  # Image assets
    └──  meme/              # Meme version images
        ├── index_finger.jpg
        ├── middle_finger.jpg
        ├── thumb_up.jpeg
        └── tongue_out.png

```

## Usage

1. **Make sure your virtual environment is activated**
   ```bash
   source .venv/bin/activate
   ```

2. **Run the application**
   ```bash
   python main.py
   ```

3. **Perform gestures in front of your webcam:**
   - Point with your **index finger only**
   - Raise your **middle finger only**
   - Give a **thumbs up**
   - **Stick out your tongue**

4. **Press 'q' to quit**

## How It Works

- Uses **MediaPipe Hands** for hand landmark detection
- Uses **MediaPipe Face Mesh** for facial landmark detection
- Detects specific finger positions to trigger different meme images
- Real-time processing with your webcam feed

## Notes

- Ensure good lighting for better gesture recognition
- Keep your hand clearly visible to the camera
- Only one hand is tracked at a time
- Face detection works best when facing the camera directly

## License

MIT