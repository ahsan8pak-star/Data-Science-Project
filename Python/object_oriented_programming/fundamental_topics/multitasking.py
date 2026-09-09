# multithreading = Used to perform multiple tasks concurrently (multitasking)
# Good for I/O bound tasks like reading files or fetching data from APIs

# Use chores as an example of multitasking

import threading
import time

def clean_bedroom(first_name, last_name):
   time.sleep(15)
   print(f"You finish cleaning {first_name} {last_name}'s bedroom.")

def take_out_trash():
   time.sleep(10)
   print("You took out the trash.")

def get_mail():
   time.sleep(5)
   print("You got mail!")

chore1 = threading.Thread(target=clean_bedroom, args=("Scooby", "Doo"))
chore1.start()

chore2 = threading.Thread(target=take_out_trash)
chore2.start()

chore3 = threading.Thread(target=get_mail)
chore3.start()

# .join() ensures that all tasks are completed before proceeding
chore1.join()
chore2.join()
chore3.join()

print("All chores are complete!")

