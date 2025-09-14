# face-attendance-system
Face Recognition Attendance System with Python, OpenCV, Excel, and TTS

Face Attendance System

This project is a Face Recognition Based Attendance System built with Python and OpenCV.
It detects faces using the webcam and automatically marks attendance by saving data into an Excel/CSV file.

Features

Real-time face detection with webcam

Face recognition using face_recognition library

Attendance logging (Name, Date, Time) into Excel/CSV

Prevents duplicate entries in one session

Project Structure
face-attendance-system/
│-- images/            # Folder for training face images
│-- attendance.csv     # Attendance log
│-- main.py            # Main program
│-- README.md          # Project description

How to Run

Clone the repository

git clone https://github.com/qayzaalx/face-attendance-system.git
cd face-attendance-system


Install dependencies

pip install -r requirements.txt


Run the program

python main.py

Requirements

Python 3.8+

OpenCV

face_recognition

numpy

pandas

Future Improvements

Add GUI for easier use

Store attendance in database (MySQL/SQLite)

Export attendance as PDF

Author

Created by Qayza Al Gifari

https://youtu.be/hlx9Fsq3PmA?si=X7-LuPYvc-0YdLxv
