import tkinter as tk
import tkinter.font as font
from PIL import Image, ImageTk
from motion_detection import start_motion_detection
from object_detection import start_object_detection
from facial_recognition import start_facial_recognition
from traffic_rules_monitoring import TrafficRulesApp  # Import the class

def start_traffic_monitoring_window():
    # Create a new window for Traffic Rules Monitoring
    traffic_window = tk.Toplevel()
    app = TrafficRulesApp(traffic_window)  # Initialize the TrafficRulesApp with the new window

def setup_main_window():
    window = tk.Tk()
    window.title("Smart CCTV for Traffic Signals")
    window.geometry('1080x760')
    
    # Load the background image
    background_image = Image.open('assets/images/background.jpg')
    background_photo = ImageTk.PhotoImage(background_image)
    
    # Create a Canvas and set the background image
    canvas = tk.Canvas(window, width=1080, height=760)
    canvas.pack(fill='both', expand=True)
    canvas.create_image(0, 0, image=background_photo, anchor='nw')
    
    frame1 = tk.Frame(canvas)
    frame1.place(relx=0.5, rely=0.5, anchor='center')
    
    label_title = tk.Label(frame1, text="Smart CCTV for Traffic Signals", bg='white', fg='black')
    label_font = font.Font(size=35, weight='bold', family='Helvetica')
    label_title['font'] = label_font
    label_title.grid(pady=(10, 10), column=1, row=0)
    
    # Load icons
    icon = Image.open('assets/icons/trafficlight2.jpg').resize((150, 150), Image.LANCZOS)
    icon = ImageTk.PhotoImage(icon)
    label_icon = tk.Label(frame1, image=icon, bg='white')
    label_icon.grid(row=1, pady=(7, 10), column=1)
    
    # Add buttons
    btn_font = font.Font(size=25)
    
    btn_motion = tk.Button(frame1, text='Motion Detection', height=2, width=20, fg='white', bg='#4d0000', command=start_motion_detection)
    btn_motion['font'] = btn_font
    btn_motion.grid(row=2, pady=(20, 10), column=0)
    
    btn_object = tk.Button(frame1, text='Object Detection', height=2, width=20, fg='white', bg='#80ff00', command=start_object_detection)
    btn_object['font'] = btn_font
    btn_object.grid(row=2, pady=(20, 10), column=2, padx=(20, 5))
    
    btn_facial = tk.Button(frame1, text='Facial Recognition', height=2, width=20, fg='white', bg='#33ff57', command=start_facial_recognition)
    btn_facial['font'] = btn_font
    btn_facial.grid(row=3, pady=(20, 10), column=0)
    
    btn_traffic = tk.Button(frame1, text='Traffic Rules Monitoring', height=2, width=20, fg='white', bg='#ff33bb', command=start_traffic_monitoring_window)
    btn_traffic['font'] = btn_font
    btn_traffic.grid(row=3, pady=(20, 10), column=2)
    
    # Keep a reference to the background image to prevent garbage collection
    canvas.background = background_photo
    
    window.mainloop()

if __name__ == "__main__":
    setup_main_window()
