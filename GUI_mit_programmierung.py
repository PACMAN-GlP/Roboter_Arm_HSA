import paramiko
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
import tkinter as tk

# SSH-Zugangsdaten
PI_HOST = "raspberrypi.local"
PI_USER = "nils"
PI_PASSWORD = "1234"
PI_COMMAND = "/home/nils/Test1.py"

# Initiale Winkel und Werte
angles = [90, 0, 180, 90, 0]
MAX_VALUES = [180, 180, 180, 180, 180]
HOMING = [90, 0, 180, 90, 0]
xyz_values = [0.0, 0.0, 0.0]
rotation1 = 90

# Positionen speichern
saved_positions = []
playback_running = False
playback_index = 0

# SSH verbinden
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(PI_HOST, username=PI_USER, password=PI_PASSWORD)
print("SSH-Verbindung aufgebaut")

def send_angles():
    command = f"python3 {PI_COMMAND} " + " ".join(map(str, angles))
    try:
        stdin, stdout, stderr = ssh.exec_command(command)
        output = stdout.read().decode().strip()
        error = stderr.read().decode().strip()
        print(f"→→ PI: {output}")
        if error:
            status_label.config(text=f"Fehler: {error}", foreground="red")
        else:
            status_label.config(text=f"Gesendet: {angles}", foreground="green")
    except Exception as e:
        status_label.config(text=f"SSH-Fehler: {e}", foreground="red")

def update_angle(index, val):
    angle = int(float(val))
    angles[index] = angle
    angle_labels[index].config(text=f"{angle}°")

def update_xyz(index, val):
    xyz_values[index] = round(float(val), 2)
    xyz_labels[index].config(text=f"{xyz_values[index]:.2f}")

def update_rotation1(val):
    global rotation1
    rotation1 = int(float(val))
    rotation1_label.config(text=f"{rotation1}°")

def send_xyz():
    # Beispiel-Kommando für XYZ + Rotation
    command = f"python3 {PI_COMMAND} XYZ {xyz_values[0]} {xyz_values[1]} {xyz_values[2]} {rotation1}"
    try:
        stdin, stdout, stderr = ssh.exec_command(command)
        output = stdout.read().decode().strip()
        error = stderr.read().decode().strip()
        print(f"→→ PI: {output}")
        if error:
            status_label.config(text=f"Fehler: {error}", foreground="red")
        else:
            status_label.config(text=f"Gesendet: {xyz_values}, Rotation1: {rotation1}", foreground="green")
    except Exception as e:
        status_label.config(text=f"SSH-Fehler: {e}", foreground="red")

def loop_send():
    if notebook.index(notebook.select()) == 0:
        send_angles()
    else:
        send_xyz()
    root.after(100, loop_send)

def set_homing():
    for i, val in enumerate(HOMING):
        sliders[i].set(val)
    for i, val in enumerate([0.0, 0.0, 0.0]):
        xyz_sliders[i].set(val)
    rotation1_slider.set(90)

def save_position():
    if notebook.index(notebook.select()) == 0:
        pos = list(angles)
    else:
        pos = list(xyz_values) + [rotation1]
    saved_positions.append(pos)
    listbox.insert(tk.END, str(pos))

def start_playback():
    global playback_running, playback_index
    if not saved_positions:
        status_label.config(text="Keine Positionen gespeichert!", foreground="red")
        return
    playback_running = True
    playback_index = 0
    run_playback()

def run_playback():
    global playback_index
    if not playback_running:
        return
    pos = saved_positions[playback_index]
    if notebook.index(notebook.select()) == 0:
        for i in range(5):
            sliders[i].set(pos[i])
    else:
        for i in range(3):
            xyz_sliders[i].set(pos[i])
        rotation1_slider.set(pos[3])
    playback_index = (playback_index + 1) % len(saved_positions)
    root.after(1000, run_playback)

def stop_playback():
    global playback_running
    playback_running = False

def on_close():
    print("Verbindung wird beendet...")
    try:
        ssh.close()
    except:
        pass
    root.destroy()

# GUI
root = tb.Window(themename="flatly")
root.title("Robotersteuerung")
root.geometry("600x600")
root.resizable(False, False)

frame = tb.Frame(root, padding=20)
frame.pack(fill=BOTH, expand=True)

try:
    img = Image.open("robo_bild.png")
    img = img.resize((120, 120))
    logo = ImageTk.PhotoImage(img)
    logo_label = tb.Label(frame, image=logo)
    logo_label.image = logo
    logo_label.pack(pady=10)
except Exception as e:
    print(f"Logo konnte nicht geladen werden: {e}")

notebook = tb.Notebook(frame)
notebook.pack(fill=BOTH, expand=True)

# Achsen-Tab
tab_angles = tb.Frame(notebook)
notebook.add(tab_angles, text="Achsensteuerung")

sliders = []
angle_labels = []

for i in range(5):
    row = tb.Frame(tab_angles)
    row.pack(fill=X, pady=8)

    tb.Label(row, text=f"Achse {i+1}", width=10).pack(side=LEFT)
    slider = tb.Scale(row, from_=0, to=MAX_VALUES[i], orient=HORIZONTAL,
                      command=lambda val, idx=i: update_angle(idx, val),
                      bootstyle="info", length=350)
    slider.set(angles[i])
    slider.pack(side=LEFT, padx=10, fill=X, expand=True)

    label = tb.Label(row, text=f"{angles[i]}°", width=6)
    label.pack(side=LEFT)

    sliders.append(slider)
    angle_labels.append(label)

# XYZ-Tab
tab_xyz = tb.Frame(notebook)
notebook.add(tab_xyz, text="XYZ + Rotation1")

xyz_sliders = []
xyz_labels = []

for i, axis in enumerate(["X", "Y", "Z"]):
    row = tb.Frame(tab_xyz)
    row.pack(fill=X, pady=8)

    tb.Label(row, text=axis, width=10).pack(side=LEFT)
    slider = tb.Scale(row, from_=-1, to=1, orient=HORIZONTAL,
                      command=lambda val, idx=i: update_xyz(idx, val),
                      bootstyle="warning", length=350)
    slider.set(xyz_values[i])
    slider.pack(side=LEFT, padx=10, fill=X, expand=True)

    label = tb.Label(row, text=f"{xyz_values[i]:.2f}", width=6)
    label.pack(side=LEFT)

    xyz_sliders.append(slider)
    xyz_labels.append(label)

row_rot = tb.Frame(tab_xyz)
row_rot.pack(fill=X, pady=8)

tb.Label(row_rot, text="Rotation1", width=10).pack(side=LEFT)
rotation1_slider = tb.Scale(row_rot, from_=0, to=180, orient=HORIZONTAL,
                           command=update_rotation1,
                           bootstyle="success", length=350)
rotation1_slider.set(rotation1)
rotation1_slider.pack(side=LEFT, padx=10, fill=X, expand=True)

rotation1_label = tb.Label(row_rot, text=f"{rotation1}°", width=6)
rotation1_label.pack(side=LEFT)

# Steuerungs-Buttons
btn_frame = tb.Frame(frame)
btn_frame.pack(pady=10)

tb.Button(btn_frame, text="Homing Position", command=set_homing, bootstyle="primary").pack(side=LEFT, padx=5)
tb.Button(btn_frame, text="Speichern", command=save_position, bootstyle="success").pack(side=LEFT, padx=5)
tb.Button(btn_frame, text="Start", command=start_playback, bootstyle="success").pack(side=LEFT, padx=5)
tb.Button(btn_frame, text="Stop", command=stop_playback, bootstyle="danger").pack(side=LEFT, padx=5)

listbox = tk.Listbox(frame, height=8)
listbox.pack(fill=X, padx=20, pady=10)

status_label = tb.Label(frame, text="Bereit", font=("Segoe UI", 10), foreground="gray")
status_label.pack(pady=10)

root.protocol("WM_DELETE_WINDOW", on_close)
root.after(100, loop_send)
root.mainloop()
