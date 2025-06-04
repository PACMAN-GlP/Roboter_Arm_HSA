import ttkbootstrap as tb
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
import paramiko
import time
import os

# SSH-Konfiguration
PI_HOST = "raspberrypi.local"  # IP oder Hostname deines Pi
PI_USER = "nils"
PI_PASSWORD = "1234"
PI_COMMAND = "/home/pi/roboterarm.py"

HOMING_ANGLES = [90, 0, 180, 90, 0]

# Global für Debounce
last_sent = 0

def send_angles(angles):
    global ssh
    try:
        command = f"python3 {PI_COMMAND} " + " ".join(map(str, angles))
        ssh.exec_command(command)
        output_label.config(text=f"Winkel gesendet: {angles}", foreground="green")
    except Exception as e:
        output_label.config(text=f"Fehler: {e}", foreground="red")

def on_scale_change(val):
    global last_sent
    now = time.time()
    if now - last_sent > 0.1:  # Mind. 100ms Pause
        last_sent = now
        angles = [int(scale.get()) for scale in scales]
        update_angle_labels()
        send_angles(angles)

def update_angle_labels():
    for i, scale in enumerate(scales):
        angle_labels[i].config(text=f"{int(scale.get())}°")

def move_to_homing():
    for i, angle in enumerate(HOMING_ANGLES):
        scales[i].set(angle)
    update_angle_labels()
    send_angles(HOMING_ANGLES)

# --- SSH-Verbindung aufbauen ---
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    ssh.connect(PI_HOST, username=PI_USER, password=PI_PASSWORD)
except Exception as e:
    print(f"SSH-Verbindung fehlgeschlagen: {e}")

# --- GUI Setup ---
root = tb.Window(themename="flatly")
root.title("Roboterarm Steuerung")
root.geometry("520x620")

# Logo laden
script_dir = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(script_dir, "robo_bild.png")
try:
    logo_img = Image.open(logo_path)
    # Pillow >10: Resampling verwenden
    try:
        resample_mode = Image.Resampling.LANCZOS
    except AttributeError:
        resample_mode = Image.ANTIALIAS
    logo_img = logo_img.resize((140, 140), resample_mode)
    logo_photo = ImageTk.PhotoImage(logo_img)
    logo_label = tb.Label(root, image=logo_photo)
    logo_label.image = logo_photo  # Referenz sichern
    logo_label.pack(pady=10)
except Exception as e:
    tb.Label(root, text="Logo konnte nicht geladen werden.").pack(pady=10)

# Steuerungsframe
main_frame = tb.Frame(root, padding=20)
main_frame.pack(fill=BOTH, expand=True)

scales = []
angle_labels = []

for i in range(5):
    tb.Label(main_frame, text=f"Achse {i+1}", font=("Segoe UI", 11)).grid(row=i, column=0, sticky=W, pady=10)

    min_angle = 0
    max_angle = 45 if i == 4 else 180

    scale = tb.Scale(main_frame, from_=min_angle, to=max_angle, orient=HORIZONTAL,
                     length=300, command=on_scale_change)
    scale.set(min_angle)
    scale.grid(row=i, column=1)
    scales.append(scale)

    angle_label = tb.Label(main_frame, text=f"{min_angle}°", width=6)
    angle_label.grid(row=i, column=2, padx=12)
    angle_labels.append(angle_label)

# Buttons
tb.Button(main_frame, text="Homing Position anfahren", bootstyle="info", command=move_to_homing)\
    .grid(row=6, column=0, columnspan=3, pady=(15, 6), sticky=EW)

output_label = tb.Label(main_frame, text="", font=("Segoe UI", 10), foreground="gray")
output_label.grid(row=7, column=0, columnspan=3, pady=12)

root.mainloop()

# SSH Verbindung sauber schließen
ssh.close()
