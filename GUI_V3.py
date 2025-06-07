import paramiko
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from PIL import Image, ImageTk


# SSH-Zugangsdaten
PI_HOST = "f"
PI_USER = "nils"
PI_PASSWORD = "1234"
PI_COMMAND = "/home/nils/Main.py"

# Initiale Winkel
angles = [90, 0, 180, 90, 0]
MAX_VALUES = [180, 180, 180, 180, 180]
HOMING = [90, 0, 180, 90, 0]

# SSH-Verbindung aufbauen
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(PI_HOST, username=PI_USER, password=PI_PASSWORD)
print("SSH-Verbindung aufgebaut")


# Sendet aktuelle Winkelwerte per SSH
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


# Winkel aktualisieren
def update_angle(index, val):
    angle = int(float(val))
    angles[index] = angle
    angle_labels[index].config(text=f"{angle}°")


# Sende-Befehl alle 100ms
def loop_send():
    send_angles()
    root.after(100, loop_send)


# Homing-Position
def set_homing():
    for i, val in enumerate(HOMING):
        sliders[i].set(val)


# GUI mit ttkbootstrap
root = tb.Window(themename="flatly")
root.title("Live Robotersteuerung")
root.geometry("500x550")
root.resizable(False, False)

frame = tb.Frame(root, padding=20)

# Logo einfügen
logo_path = "robo_bild.png"  # Datei im gleichen Verzeichnis
try:
    img = Image.open(logo_path)
    img = img.resize((120, 120))
    logo = ImageTk.PhotoImage(img)

    logo_label = tb.Label(frame, image=logo)
    logo_label.image = logo  # Referenz halten!
    logo_label.pack(pady=10)
except Exception as e:
    print(f"Logo konnte nicht geladen werden: {e}")

frame.pack(fill=BOTH, expand=True)

sliders = []
angle_labels = []

for i in range(5):
    row = tb.Frame(frame)
    row.pack(fill=X, pady=10)

    tb.Label(row, text=f"Achse {i + 1}", width=10).pack(side=LEFT)
    slider = tb.Scale(row, from_=0, to=MAX_VALUES[i], orient=HORIZONTAL,
                      command=lambda val, idx=i: update_angle(idx, val),
                      bootstyle="info")
    slider.set(angles[i])
    slider.pack(side=LEFT, fill=X, expand=True, padx=10)

    angle_lbl = tb.Label(row, text=f"{angles[i]}°", width=5)
    angle_lbl.pack(side=LEFT)

    sliders.append(slider)
    angle_labels.append(angle_lbl)

# Homing Button
tb.Button(frame, text="Homing Position", command=set_homing, bootstyle="primary").pack(pady=15)

# Statusanzeige
status_label = tb.Label(frame, text="Bereit", font=("Segoe UI", 10), foreground="gray")
status_label.pack(pady=10)


# Fenster schließen = SSH beenden
def on_close():
    print("Verbindung wird beendet...")
    try:
        ssh.close()
    except:
        pass
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_close)
root.after(100, loop_send)
root.mainloop()
