import time

now = time.time()

while True:
    if time.time() - now > 2:
        print("Hello Nils!")
        now = time.time()
