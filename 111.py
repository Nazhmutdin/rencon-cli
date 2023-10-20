import time
from random import randint

from rich.progress import Progress

progress = Progress()

progress.start()

array = [1, 2, 5, 6, 8, 9, 7, 9]

task3 = progress.add_task("[red]Processing...", total=len(array))

while True:
    try:
        array.pop(0)
    except:
        break
    progress.update(task3, advance=1)
    time.sleep(randint(1, 3))

progress.stop()
