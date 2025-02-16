How to Run the Model

 Run the License Plate Recognition

Run the Main.ipynb notebook and modify the image_path variable:

image_path = 'IMG_9518.jpeg' #change the path to test the model

Then, execute the cells to process the image.

Expected Output Example:

License Plate: LUD 1229 0.999042088857666

Process a single image:

python src/main.py --image data/IMG_9518.jpeg


 View Results

Detected license plate data is saved in:

results/output.csv


Project Structure

YOLO_License_Plate_Recognition/
│── models/          # Pre-trained YOLO models
│── data/            # Input images/videos
│── notebooks/       # Jupyter Notebooks for testing
│   ├── main.ipynb   # Main script
│   ├── util.py      # Helper functions
│   ├── sort.py      # Online and real-time tracking for 2D multiple object tracking in videos
│   ├── add_missing_data.py # Data processing
│   ├── visualize.py # Visualization utilities
│── results/         # CSV logs and detection outputs
│── requirements.txt # Dependencies libraries that need to be installed
│── README.md        # This guide
YOLO_License_Plate_Recognition/
│── models/          # Pre-trained YOLO models
│── data/            # Input images/videos
│── notebooks/       # Jupyter Notebooks for testing
│── src/             # Source code scripts
│── results/         # CSV logs and detection outputs
│── requirements.txt # Python dependencies
│── README.md        # This guide

