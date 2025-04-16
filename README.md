# Person Check App

The Person Check App is a Python-based application designed to detect people in a camera frame and automatically save snapshots. It uses FastAPI for the backend, OpenCV for image processing, and MediaPipe for person detection.

## Features

**Camera Control**: Start and stop the camera through a user-friendly web interface.
**Person Detection**: Automatically captures photos when a person is detected in the frame for a specified duration.
**Photo Management**: View and filter saved photos by date through the web interface.
**Data Storage**: Stores captured photos and metadata in an SQLite database for easy access and management.

## Installation

1. Ensure Python 3.9 or higher is installed on your system.
2. Clone the repository and navigate to the project directory.
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## How to Start the App

To start the Person Check App, follow these steps:

1. **Run the Application**  
   Start the FastAPI server by executing the following command in the terminal:
   ```bash
   python app.py
   ```

2. **Access the Web Interface**  
   Open your browser and navigate to [http://127.0.0.1:8000](http://127.0.0.1:8000).  
   From here, you can:
   - Start or stop the camera.
   - View and manage captured photos.
   - Configure detection settings if needed.

3. **Stop the Application**  
   To stop the app, press `Ctrl+C` in the terminal where the server is running.

By following these steps, you can easily start and use the Person Check App.
