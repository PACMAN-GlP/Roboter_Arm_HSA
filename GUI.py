import paramiko
from Pose import Pose
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
import tkinter as tk
from CircularLinkedList import CircularLinkedList #Zirkuläre verkettete Liste zur Speicherung von Positionen und widergabe in Schleife

# SSH-Zugangsdaten
PI_HOST = "pi.local"
PI_USER = "pi"
PI_PASSWORD = "pi"
PI_COMMAND = "/home/pi/Main.py"
PI_COMMAND_XYZ = "/home/pi/MainXYZ.py"

# Initiale Winkel und Werte
angles = [90, 0, 180, 90, 0]
MAX_VALUES = [180, 180, 180, 180, 180]
HOMING = [90, 0, 180, 90, 0]
xyz_values = [0.0, 0.0, 0.0]
rotation1 = 90

# Positionen speichern
saved_positions = CircularLinkedList()

playback_running = False


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
        print(f"→→ axis-PI: {output}")
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

def adjust_angle(index, delta):
    new_val = angles[index] + delta
    new_val = max(0, min(MAX_VALUES[index], new_val))
    sliders[index].set(new_val)


def update_xyz(index, val):
    xyz_values[index] = round(float(val), 2)
    xyz_labels[index].config(text=f"{xyz_values[index]:.2f}")

def update_rotation1(val):
    global rotation1
    rotation1 = int(float(val))
    rotation1_label.config(text=f"{rotation1}°")

def send_xyz():
    # Beispiel-Kommando für XYZ + Rotation
    command = f"python3 {PI_COMMAND_XYZ} {xyz_values[0]} {xyz_values[1]} {xyz_values[2]} {rotation1}"
    try:
        stdin, stdout, stderr = ssh.exec_command(command)
        output = stdout.read().decode().strip()
        error = stderr.read().decode().strip()
        print(f"→→ xyz-PI: {output}")
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
    global playback_running
    if saved_positions.is_empty():
        status_label.config(text="Keine Positionen gespeichert!", foreground="red")
        return
    playback_running = True
    saved_positions.reset()
    run_playback()


def run_playback():
    if not playback_running:
        return
    pos = saved_positions.next()
    if notebook.index(notebook.select()) == 0:
        for i in range(5):
            if i < 4:
                sliders[i].set(pos[i])
            else:
                set_angle_5(pos[i])
    else:
        for i in range(3):
            xyz_sliders[i].set(pos[i])
        rotation1_slider.set(pos[3])
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

def clear_positions():
    saved_positions.clear()
    listbox.delete(0, END)
    status_label.config(text="Alle Positionen gelöscht", foreground="orange")


def set_angle_5(value):
    angles[4] = value
    send_angles()



# GUI
root = tb.Window(themename="flatly")
root.title("Robotersteuerung")
root.geometry("600x600")

# Scrollbares Canvas
outer_frame = tb.Frame(root)
outer_frame.pack(fill=BOTH, expand=True)

canvas = tk.Canvas(outer_frame, borderwidth=0)
canvas.pack(side=LEFT, fill=BOTH, expand=True)

scrollbar = tb.Scrollbar(outer_frame, orient=VERTICAL, command=canvas.yview)
scrollbar.pack(side=RIGHT, fill=Y)

canvas.configure(yscrollcommand=scrollbar.set)
canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(-1 * int(event.delta / 120), "units"))


# Inneres Frame in Canvas
frame = tb.Frame(canvas)
frame_id = canvas.create_window((0, 0), window=frame, anchor="nw")

# Scrollregion automatisch anpassen
def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

frame.bind("<Configure>", on_frame_configure)

# Breite des Frames immer anpassen
def on_canvas_configure(event):
    canvas.itemconfig(frame_id, width=event.width)

canvas.bind("<Configure>", on_canvas_configure)



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

    if i < 4:
        # Achsen 1-4: Slider + Buttons + Label
        slider = tb.Scale(row, from_=0, to=MAX_VALUES[i], orient=HORIZONTAL,
                          command=lambda val, idx=i: update_angle(idx, val),
                          bootstyle="info", length=200)
        slider.set(angles[i])
        slider.pack(side=LEFT, padx=5, fill=X, expand=True)

        label = tb.Label(row, text=f"{angles[i]}°", width=6)
        label.pack(side=LEFT, padx=5)

        btn_frame = tb.Frame(row)
        btn_frame.pack(side=LEFT, padx=5)

        tb.Button(btn_frame, text="-1", width=3, bootstyle="secondary",
                  command=lambda idx=i: adjust_angle(idx, -1)).pack(side=TOP, pady=2)
        tb.Button(btn_frame, text="+1", width=3, bootstyle="secondary",
                  command=lambda idx=i: adjust_angle(idx, 1)).pack(side=TOP, pady=2)

        sliders.append(slider)
        angle_labels.append(label)
    else:
        # Achse 5: nur Auf/Zu Buttons
        btn_frame_5 = tb.Frame(row)
        btn_frame_5.pack(side=LEFT, padx=5)

        tb.Button(btn_frame_5, text="Auf", width=5, bootstyle="success",
                  command=lambda: set_angle_5(180)).pack(side=TOP, pady=2)
        tb.Button(btn_frame_5, text="Zu", width=5, bootstyle="danger",
                  command=lambda: set_angle_5(0)).pack(side=TOP, pady=2)


        
# XYZ-Tab
tab_xyz = tb.Frame(notebook)
notebook.add(tab_xyz, text="XYZ + Rotation1")

xyz_sliders = []
xyz_labels = []

for i, axis in enumerate(["X", "Y", "Z"]):
    row = tb.Frame(tab_xyz)
    row.pack(fill=X, pady=8)

    tb.Label(row, text=axis, width=10).pack(side=LEFT)
    slider = tb.Scale(row, from_=-(Pose.S1+Pose.S2), to=Pose.S1+Pose.S2, orient=HORIZONTAL,
                      command=lambda val, idx=i: update_xyz(idx, val),
                      bootstyle="warning", length=350)
    slider.set(xyz_values[i])
    slider.pack(side=LEFT, padx=10, fill=X, expand=True)

    label = tb.Label(row, text=f"{xyz_values[i]:.2f}", width=6)
    label.pack(side=LEFT)

    xyz_sliders.append(slider)
    xyz_labels.append(label)

# Achse 5: nur Auf/Zu Buttons
btn_frame_5 = tb.Frame(tab_xyz)
btn_frame_5.pack(pady=10)

tb.Label(btn_frame_5, text="Greifer").pack()

tb.Button(btn_frame_5, text="Auf", width=10, bootstyle="success",
          command=lambda: set_angle_5(180)).pack(side=LEFT, padx=10)
tb.Button(btn_frame_5, text="Zu", width=10, bootstyle="danger",
          command=lambda: set_angle_5(0)).pack(side=LEFT, padx=10)


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
tb.Button(frame, text="Alle Positionen löschen", bootstyle="danger", command=lambda: clear_positions()).pack(pady=5)



listbox = tk.Listbox(frame, height=8)
listbox.pack(fill=X, padx=20, pady=10)

status_label = tb.Label(frame, text="Bereit", font=("Segoe UI", 10), foreground="gray")
status_label.pack(pady=10)

root.protocol("WM_DELETE_WINDOW", on_close)
root.after(100, loop_send)
root.mainloop()
