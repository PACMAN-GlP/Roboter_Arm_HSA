import tkinter as tk


root = tk.Tk()
root.title("Roboterarm Steuerung")
root.geometry("400x500")

# Funktion zur Steuerung der Achsen
def update_axis(axis, value):
    print(f"Achse {axis}: {value}")

# Funktion zur Homing-Position
def homing_position():
      
    print("Roboterarm fährt in die Homing-Position")


control_frame = tk.Frame(root)
tk.Label(control_frame, text="Steuerung der Achsen in °").pack(pady=10)



sliders = []
for i in range(4):
    tk.Label(control_frame, text=f"Achse {i+1}").pack()
    slider = tk.Scale(control_frame, from_=0, to=180, orient="horizontal", command=lambda value, axis=i+1: update_axis(axis, value))
    slider.pack()
    sliders.append(slider)
    
tk.Label(control_frame, text=f"Achse 5").pack()
slider = tk.Scale(control_frame, from_=0, to=45, orient="horizontal", command=lambda value, axis=i+1: update_axis(axis, value))
slider.pack()
sliders.append(slider)


# Button für Homing-Position
tk.Button(control_frame, text="Homing anfahren", command=homing_position).pack(pady=10)

# Steuerungsansicht direkt aktivieren
control_frame.pack(fill="both", expand=True)

# Hauptloop starten
root.mainloop()




 



