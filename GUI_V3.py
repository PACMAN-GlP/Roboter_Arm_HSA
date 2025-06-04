import paramiko
import time

# SSH-Zugangsdaten
PI_HOST = "10.42.0.204"
PI_USER = "pi"
PI_PASSWORD = "pi"
PI_COMMAND = "/home/pi/Test1.py"

# Winkel, die gesendet werden sollen (Liste von Listen)
angles = [0, 180, 90, 0, 0]

# SSH-Verbindung aufbauen
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(PI_HOST, username=PI_USER, password=PI_PASSWORD)

print("SSH-Verbindung aufgebaut")

try:

    command = f"python3 {PI_COMMAND} " + " ".join(map(str, angles))
    stdin, stdout, stderr = ssh.exec_command(command)

    output = stdout.read().decode().strip() #OUTPUT vom pi
    error = stderr.read().decode().strip() #ERROR vom pi

    if error:
        print(f"Fehler:\n{error}")
    else:
        print(f"Gesendet: {angles}")
        print(f"Antwort: {output}")

    time.sleep(1)

finally:
    ssh.close()
    print("SSH-Verbindung geschlossen")