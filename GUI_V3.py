import paramiko
import time
import os
import threading
import tkinter as tk
from tkinter import ttk

# SSH-Zugangsdaten
PI_HOST = "10.42.0.204"
PI_USER = "pi"
PI_PASSWORD = "pi"
PI_COMMAND = "/home/pi/Test1.py"

# Initiale Winkelwerte
angles = [0, 90, 90, 0, 0]

# SSH-Verbindung aufbauen
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(PI_HOST, username=PI_USER, password=PI_PASSWORD)
print("SSH-Verbindung aufgebaut")

# Sendet aktuelle Winkelwerte per SSH
def send_angles():
    command = f"python3 {PI_COMMAND} " + " ".join(map(str, angles))
    try:
        stdin, stdout, stderr = ssh.exec_command(command) #Führt Test1.py aus und übergibt die Werte
        output = stdout.read().decode().strip()
        error = stderr.read().decode().strip()

        print(f"→→ PI: {output}")

        if error:
            status_label.config(text=f"Fehler: {error}", foreground="red")
            print(f"ERROR: {error}")
        else:
            status_label.config(text=f"Gesendet: {angles}", foreground="green")
    except Exception as e:
        status_label.config(text=f"SSH-Fehler: {e}", foreground="red")

# Wird bei Änderung eines Sliders aufgerufen
def update_angle(index, val):
    angles[index] = int(float(val))

# Wiederholt das Senden alle 100ms
def loop_send():
    send_angles()
    root.after(100, loop_send)

# GUI erstellen
root = tk.Tk()
root.title("Live Steuerung")
root.geometry("400x400")

sliders = []
for i in range(5):
    tk.Label(root, text=f"Achse {i + 1}").pack()
    max_val = 180
    slider = ttk.Scale(root, from_=0, to=max_val, orient="horizontal",
                       command=lambda val, idx=i: update_angle(idx, val))
    slider.set(angles[i])
    slider.pack(fill="x", padx=20, pady=5)
    sliders.append(slider)

status_label = tk.Label(root, text="Bereit", foreground="gray")
status_label.pack(pady=20)

# Starte Loop
root.after(100, loop_send)

# SSH beim Schließen beenden
def on_close():
    print("Verbindung wird beendet...")
    ssh.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()
