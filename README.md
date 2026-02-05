# Flood Extent Delineation & Post-Disaster Damage Assessment

This project is a MERN + Machine Learning based system for analyzing satellite imagery after floods or disasters. It performs flood extent delineation, flood severity prediction using CNN regression, and building-level damage visualization using xBD annotations.

## Features

- Pre/Post disaster image upload
- Pixel-wise flood mask generation
- Flood overlay visualization
- CNN-based flood severity prediction (%)
- Building damage distribution (xBD dataset)
- React dashboard for visualization
- Flask ML backend + Node API gateway

## Tech Stack

Frontend:
- React
- Chart.js

Backend:
- Node.js
- Express
- Multer
- Axios

ML Service:
- Python
- Flask
- PyTorch
- OpenCV

Dataset:
- xBD Disaster Dataset

## System Architecture

React UI  
→ Node Backend  
→ Flask ML Server  
→ CNN Flood Regression + Flood Mask  
→ Results returned to Dashboard

## How to Run

### ML Server

```bash
cd ml
python server.py
Node Backend
cd backend
node index.js
Frontend
cd frontend
npm start
Open browser at:

http://localhost:3000

Output
Actual Flood Percentage (from mask)

Predicted Flood Percentage (CNN)

Flood Mask Image

Flood Overlay Image

Building Damage Distribution Pie Chart

Building severity is available only for xBD dataset images.

Future Work
Building-level damage prediction using instance segmentation

SAR imagery support

Real-time deployment

Author
Final Year Project


Save.

Commit:

```bash
