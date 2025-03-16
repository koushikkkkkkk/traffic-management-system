import tkinter as tk
from tkinter import filedialog, messagebox
import torch
import cv2
from PIL import Image, ImageTk
import numpy as np

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', source='github')

def detect_vehicles(image):
    results = model(image)
    detected_objects = results.pred[0]
    labels = detected_objects[:, -1].cpu().numpy()
    
    # Dictionary to keep count of each type of vehicle
    vehicle_counts = {"car": 0, "motorbike": 0, "ambulance": 0}
    
    for label in labels:
        if int(label) == 2:  # Car
            vehicle_counts["car"] += 1
        elif int(label) == 3:  # Motorcycle
            vehicle_counts["motorbike"] += 1
        elif int(label) == 7:  # Truck
            vehicle_counts["ambulance"] += 1

    return vehicle_counts

def process_image(image_file):
    image = cv2.imread(image_file)
    if image is None:
        print(f"Error loading image {image_file}")
        return {}
    
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    vehicle_counts = detect_vehicles(image_rgb)
    return vehicle_counts

# GUI Application
class VehicleDetectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Vehicle Detector")
        self.root.geometry("600x400")
        
        # Initialize image panel
        self.panel = None
        self.image_file = None
        
        # Add Buttons
        btn_upload = tk.Button(self.root, text="Upload Image", command=self.upload_image)
        btn_upload.pack(side="top", pady=10)
        
        btn_process = tk.Button(self.root, text="Process Image", command=self.process_image)
        btn_process.pack(side="top", pady=10)
        
        # Add a label for green light
        self.light_label = tk.Label(self.root, text="Ambulance Light", bg="gray", width=20, height=2)
        self.light_label.pack(side="bottom", pady=20)

    def upload_image(self):
        file_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=[("Image Files", "*.jpg *.jpeg *.png")]
        )
        if file_path:
            self.image_file = file_path
            messagebox.showinfo("Info", "Image selected.")

    def process_image(self):
        if not self.image_file:
            messagebox.showerror("Error", "No image to process.")
            return

        vehicle_counts = process_image(self.image_file)

        # Output vehicle counts in terminal
        vehicle_array = []
        for vehicle_type, count in vehicle_counts.items():
            vehicle_array.extend([vehicle_type, count])

        print(f"Vehicle count array: {vehicle_array}")

        # Update the light label color based on ambulance count
        if vehicle_counts.get("ambulance", 0) >= 1:
            self.light_label.config(bg="green")
        else:
            self.light_label.config(bg="gray")

        messagebox.showinfo("Info", "Processing complete. Check terminal for results.")

# Main function
if __name__ == "__main__":
    # Initialize Tkinter window
    root = tk.Tk()
    app = VehicleDetectorApp(root)
    root.mainloop()
