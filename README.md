# Hand Tracking Without Pretrained Pose Models  
Real-Time Safety Interaction Prototype — Classical Computer Vision

This project tracks a user’s hand in real time using classical computer vision techniques (no MediaPipe, no OpenPose, no cloud APIs). It detects when the hand approaches a virtual danger boundary and visualizes interaction states:

SAFE → WARNING → DANGER

---

## Objective
Goals:
• Real-time CPU-only hand tracking
• Virtual boundary interaction
• Three safety states with visual feedback
• ≥ 8 FPS performance

---

## How It Works

Pipeline:
1. Webcam frame capture (OpenCV)
2. Skin detection:
   - HSV + YCrCb color segmentation
   - Morphological noise cleaning
3. Face region suppression using Haar cascade
4. Contour extraction + largest contour = hand
5. Centroid tracking through time smoothing
6. Distance to rectangle boundary
7. State transitions:
   - SAFE: far from boundary
   - WARNING: approaching
   - DANGER: touching or inside

---

## Directory Structure

HandTracking/
│
├── camera.py
├── segment.py
├── tracker.py
├── logic.py
├── haarcascade_frontalface_default.xml
├── requirements.txt
└── README.md

---

## Installation

pip install -r requirements.txt

Run:
python camera.py

---

## Demo Video

Demo Video (MP4):
https://github.com/roystond12/Hand-Tracking-without-Using-Pretrained-Model/blob/main/HandTracking_Demo.mp4


---


## Author

Royston Dsouza  
Computer Engineering  
GitHub Repo: https://github.com/roystond12/Hand-Tracking-without-Using-Pretrained-Model

---

## Status

Prototype complete
