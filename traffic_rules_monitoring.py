import cv2
import numpy as np
from PIL import Image, ImageTk
import tkinter as tk
import time
from collections import defaultdict

class TrafficRulesApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Traffic Rules Monitoring")
        self.master.geometry("800x600")

        self.cap = None  # Initialize capture object

        self.label = tk.Label(self.master)
        self.label.pack(fill="both", expand=True)

        self.stop_line_position = 400  # Example position for the stop line
        self.counting_line_position = 350  # Horizontal line for counting vehicles
        self.line1_position = 200  # Line for speed measurement start
        self.line2_position = 300  # Line for speed measurement end
        self.speed_limit = 60  # Speed limit in km/h
        self.vehicle_count = 0

        self.tracked_objects = defaultdict(dict)
        self.next_object_id = 0
        self.object_speeds = {}  # Store object speeds

        self.info_label = tk.Label(self.master, text="", font=("Helvetica", 14), bg="white")
        self.info_label.pack(fill="x")

        self.bg_subtractor = cv2.createBackgroundSubtractorMOG2()  # Background subtractor

        self.start_traffic_rules_monitoring()

    def start_traffic_rules_monitoring(self):
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Use webcam
        if not self.cap.isOpened():
            print("Error: Could not open webcam.")
            return
        self.update_frame()

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            print("Failed to grab frame.")
            return

        fg_mask = self.bg_subtractor.apply(frame)  # Apply background subtraction
        _, thresh = cv2.threshold(fg_mask, 200, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            if cv2.contourArea(contour) > 500:
                x, y, w, h = cv2.boundingRect(contour)
                object_center = (x + w // 2, y + h // 2)

                # Update or assign unique IDs to objects
                matched = False
                for object_id, obj_data in self.tracked_objects.items():
                    if abs(obj_data.get('center', (0, 0))[0] - object_center[0]) < 50:
                        self.tracked_objects[object_id]['center'] = object_center
                        self.tracked_objects[object_id]['y_position'] = y + h
                        matched = True
                        break

                if not matched:
                    self.tracked_objects[self.next_object_id] = {
                        'center': object_center,
                        'y_position': y + h,
                        'start_time': None
                    }
                    self.next_object_id += 1

                # Speed measurement
                obj_data = self.tracked_objects[self.next_object_id - 1]
                if obj_data['y_position'] > self.line1_position and obj_data['start_time'] is None:
                    self.tracked_objects[self.next_object_id - 1]['start_time'] = time.time()

                if obj_data['y_position'] > self.line2_position and obj_data['start_time'] is not None:
                    elapsed_time = time.time() - obj_data['start_time']
                    if elapsed_time > 0:  # Prevent division by zero
                        speed = (10 / elapsed_time) * 3.6  # Assume 10 meters between lines
                        self.object_speeds[self.next_object_id - 1] = speed

                        if speed > self.speed_limit:
                            cv2.putText(frame, f"SPEEDING: {speed:.2f} km/h", (x, y - 10),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

                # Count vehicles crossing the counting line
                if obj_data['y_position'] > self.counting_line_position:
                    if not obj_data.get('counted', False):
                        self.vehicle_count += 1
                        self.tracked_objects[self.next_object_id - 1]['counted'] = True

                # Check stop line violation
                if y + h > self.stop_line_position:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    cv2.putText(frame, "VIOLATION", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        # Draw lines
        cv2.line(frame, (0, self.counting_line_position), (frame.shape[1], self.counting_line_position), (0, 255, 0), 2)
        cv2.line(frame, (0, self.line1_position), (frame.shape[1], self.line1_position), (255, 255, 0), 2)
        cv2.line(frame, (0, self.line2_position), (frame.shape[1], self.line2_position), (255, 255, 0), 2)

        # Update information label
        self.info_label.configure(
            text=f"Vehicle Count: {self.vehicle_count} | Speed Limit: {self.speed_limit} km/h")

        # Convert frame for Tkinter
        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        img_tk = ImageTk.PhotoImage(image=img)
        self.label.img_tk = img_tk
        self.label.configure(image=img_tk)

        self.master.after(10, self.update_frame)  # Schedule the next frame

    def __del__(self):
        if self.cap and self.cap.isOpened():
            self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    root = tk.Tk()
    app = TrafficRulesApp(root)
    root.mainloop()
