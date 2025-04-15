# Person Check App

The Person Check App is a Python-based application designed to detect people in a camera frame and save snapshots automatically. It uses FastAPI for the backend, OpenCV for image processing, and MediaPipe for person detection.

## Features

- **Camera Control**: Start and stop the camera through a user-friendly web interface.
- **Person Detection**: Automatically captures photos when a person is detected in the frame for a specified duration.
- **Photo Management**: View and filter saved photos by date through the web interface.
- **Data Storage**: Stores captured photos and metadata in an SQLite database for easy access and management.

## Project Structure

- `app.py`: The main application file containing the FastAPI server and camera logic.
- `templates/`: Contains HTML templates for the web interface.
  - `photos_page.html`: Displays saved photos with filtering options.
  - `root_page.html`: Shows recent photos and application status.
  - `start_page.html` and `stop_page.html`: Pages for starting and stopping the camera.
- `static/photos/`: Directory where captured photos are stored.
- `db/photos.db`: SQLite database file for storing photo metadata.
- `settings.json`: Configuration file for defining the frame area for person detection.

## Installation

1. Ensure Python 3.9 or higher is installed on your system.
2. Clone the repository and navigate to the project directory.
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt