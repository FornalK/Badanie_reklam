import time
import random
import os
import cv2
from scenariusze import get_scenario_params
from tkinter import *
from PIL import ImageTk, Image

ad_playing = False
paused_time = 0
round_number = 1

### Variables for eye coordinates read from the eye tracker
global_leX = 0.0
global_leY = 0.0
global_reX = 0.0
global_reY = 0.0

dots = 0  # Number of dots placed by the user
condition = 1  # Important variable to move between game stages
czas_gry = 0
kropki = []  # List of dots placed by the user on game images

clicked_areas = set()

# Variables to keep track of scheduled ads
ad_scheduled = False
ad_scheduled_event_id = None

def play_video(video_path, time_reset=True, width=400, height=300, x=100, y=100, scenario="Unknown Scenario", prior_notice=False, countdown_before_ad=0, skip_after=None):
    global ad_playing

    ad_playing = True  # Pause the game timer

    # Declare variables in the enclosing scope
    cap = None
    video_label = None
    skip_button = None
    start_pause_time = None
    ad_start_time = None

    def start_ad():
        nonlocal cap, video_label, skip_button, start_pause_time, ad_start_time

        cap = cv2.VideoCapture(video_path)
        video_label = Label(root)
        video_label.pack()
        video_label.place(x=x, y=y)

        with open('czasy.txt', 'a') as log_file:
            log_file.write(f"Reklama Start: {int(time.time())}, Nazwa Reklamy: {video_path}, Scenariusz: {scenario}\n")

        if time_reset:
            global paused_time
            start_pause_time = time.time()  # Start measuring pause time

        ad_start_time = time.time()

        if skip_after is not None:
            # Create skip button but disable it initially
            skip_button = Button(root, text="Pomiń reklamę", command=skip_ad,
                                 font=("Arial", 16, "bold"), width=15, height=2,
                                 bg="green", fg="white")
            skip_button.place(x=x + width - 300, y=y + height - 100)
            skip_button['state'] = 'disabled'
        else:
            skip_button = None

        update_frame()

    def update_frame():
        nonlocal ad_start_time, cap, video_label, skip_button
        ret, frame = cap.read()
        if ret:
            frame = cv2.resize(frame, (width, height))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            img_tk = ImageTk.PhotoImage(img)
            video_label.img_tk = img_tk
            video_label.configure(image=img_tk)

            # Enable skip button after skip_after seconds
            if skip_after is not None:
                elapsed_ad_time = time.time() - ad_start_time
                if elapsed_ad_time >= skip_after:
                    skip_button['state'] = 'normal'

            video_label.after(30, update_frame)
        else:
            end_ad()

    def skip_ad():
        nonlocal cap
        with open('czasy.txt', 'a') as log_file:
            log_file.write(
                f"Reklama Pominięta: {int(time.time())}, Nazwa Reklamy: {video_path}, Scenariusz: {scenario}\n")
        cap.release()
        end_ad()

    def end_ad():
        nonlocal cap, video_label, skip_button, start_pause_time
        global paused_time, ad_playing, STIME
        with open('czasy.txt', 'a') as log_file:
            log_file.write(
                f"Reklama Zakończona: {int(time.time())}, Nazwa Reklamy: {video_path}, Scenariusz: {scenario}\n")
        cap.release()
        cap.release()
        video_label.pack_forget()  # Remove the label after the ad
        video_label.img_tk = None
        video_label.destroy()
        if skip_button:
            skip_button.destroy()
        if time_reset:
            end_pause_time = time.time()  # End of pause
            paused_duration = end_pause_time - start_pause_time
            paused_time += paused_duration
            STIME += paused_duration  # Adjust STIME to compensate for pause time
        ad_playing = False  # Resume the game timer

    # If prior notice or countdown_before_ad, display a label before starting the ad
    def show_ad():
        if prior_notice or countdown_before_ad > 0:
            notice_label = Label(root, text="", font=("Arial", 20))
            notice_label.pack()
            notice_label.place(x=1400, y=400)

            def update_notice(count):
                if count > 0:
                    notice_label.config(text=f"Reklama pojawi się za {count} sekund")
                    root.after(1000, update_notice, count - 1)
                else:
                    notice_label.destroy()
                    start_ad()

            if countdown_before_ad > 0:
                update_notice(countdown_before_ad)
            else:
                notice_label.config(text="Za chwilę pojawi się reklama")
                root.after(5000, lambda: [notice_label.destroy(), start_ad()])
        else:
            start_ad()

    show_ad()

def draw_dot(event):
    image_name = img_names[nr_image-1 % len(img_names)].split('/')[-1].split('_')[1]
    areas_filename = f'areas/areas_{image_name}.txt'
    print(areas_filename)
    with open(areas_filename, 'r') as f:
        areas = [tuple(map(int, line.strip().split(','))) for line in f.readlines()]
    flag = False  # Flag to record if click is correct
    for (x1, y1, x2, y2) in areas:
        if (x1, y1, x2, y2) not in clicked_areas:
            if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                global points
                flag = True
                points += 1
                points_var.set(f"Punkty: {points}")
                clicked_areas.add((x1, y1, x2, y2))  # Mark this area as clicked
                break

    color = "black"
    global dots
    dots += 1

    # Drawing a dot on the image
    x1, y1 = (event.x - 10), (event.y - 10)
    x2, y2 = (event.x + 10), (event.y + 10)
    id = obrazek.create_oval(x1, y1, x2, y2, fill=color, outline=color, width=14)
    kropki.append(id)
    x = x1 + x2 / 2
    y = y1 + y2 / 2

    # Saving information where the user placed dots
    c = open('czasy.txt', 'a')
    if not flag:
        c.write("KLIKNIECIE: " + str(int(time.time())) + ", 0" + "\n")
    else:
        c.write("KLIKNIECIE: " + str(int(time.time())) + ", 1" + "\n")
    c.close()

    with open('dots_xy.txt', 'a') as f:
        f.write(str(dots) + ":\t x: " + str(x) + " y: " + str(y) + "\n")

# Removes the last drawn dot
def delete_dot(event):
    if kropki:
        obrazek.delete(kropki[-1])
        del kropki[-1]

# Function called after pressing the START button on the start screen
def zacznij():
    global condition
    condition = 2
    startup_text.destroy()
    startup_button.destroy()
    f = open('czasy.txt', 'a')
    f.write("CZAS STARTU: " + str(int(time.time())) + "\n")
    f.close()
    global czas_gry
    czas_gry = time.time()

nr_image = 0
img_names = ["images/testowy_9_1.jpg", "images/testowy_6_1.jpg", "images/testowy_2_1.jpg", "images/testowy_8_1.jpg",
             "images/testowy_3_1.jpg", "images/testowy_7_1.jpg", "images/testowy_1_1.jpg", "images/testowy_5_1.jpg"] * 3
czas_obrazka = 90  # Time for each image

# Create the main application window
root = Tk()
root.title("Find_the_difference_game")
root.geometry("1920x1080")

points = 0
points_var = StringVar()
points_var.set(f"Punkty: {points}")
points_label = Label(root, textvariable=points_var, font=("Arial", 20))
points_label.place(x=1500, y=50)

# Info text for the user
info = "Po kliknięciu przycisku \"START\" po kolei zostanie Ci wyświetlonych 8 obrazków.\n" \
       "Twoim zadaniem jest znalezienie na każdym z nich jak największej liczby określonych elementów.\n" \
       "Informacje o tym czego masz szukać będą znajdować się bezpośrednio pod każdym obrazkiem.\n" \
       "Na każdy z obrazków masz 75 sekund. Kiedy znajdziesz szukany element postaw na nim kropkę\n" \
       "lewym przyciskiem myszy (LPM). Aby usunąć postawioną kropkę użyj prawego przycisku myszy (PPM).\n\n " \
       "Naciśnij przycisk \"START\" aby rozpocząć"

# Start screen elements
startup_text = Label(root, text=info, font=("Arial", 20), anchor=CENTER)
startup_text.place(x=336, y=230)
startup_button = Button(root, text="START", font=("Arial", 50), command=zacznij, anchor=CENTER)
startup_button.place(x=820, y=500)

# Load the first image
img1 = Image.open(img_names[nr_image % len(img_names)])
img_1 = ImageTk.PhotoImage(img1)

# Variables for time tracking
STIME = time.time()
STIME2 = time.time()

# Variable for displaying remaining time
remaining_time_var = StringVar()
remaining_time_var.set("Pozostały czas: 0 s")
remaining_time_label = None

def get_random_video():
    video_files = [f for f in os.listdir("videos") if f.endswith(".mp4")]
    return os.path.join("videos", random.choice(video_files)) if video_files else None

def schedule_ad():
    global ad_scheduled_event_id, ad_scheduled, round_number
    if not ad_scheduled:
        # Pobierz parametry scenariusza dla obu reklam
        scenario_params1 = get_scenario_params(round_number * 2 - 1)
        scenario_params2 = get_scenario_params(round_number * 2)
        if scenario_params1 and scenario_params2:
            video_path1 = get_random_video()
            video_path2 = get_random_video()
            ad_duration = 15  # Maksymalny czas trwania reklamy w sekundach

            # Oblicz czasy wyświetlenia reklam
            delay1 = random.randint(5, (czas_obrazka // 2 - ad_duration)) * 1000
            delay2 = random.randint((czas_obrazka // 2 + 5), (czas_obrazka - ad_duration)) * 1000

            # Zaplanuj obie reklamy
            ad_scheduled_event_id = [
                root.after(delay1, lambda: play_video(video_path1, **scenario_params1)),
                root.after(delay2, lambda: play_video(video_path2, **scenario_params2))
            ]
            ad_scheduled = True


while True:
    ETIME = time.time()
    ETIME2 = time.time()
    seconds = ETIME - STIME  # Time since image was displayed
    seconds2 = ETIME2 - STIME2  # Time since last eye tracker update

    # Update remaining time
    remaining_time = max(0, int(czas_obrazka - seconds))
    if condition > 2:
        remaining_time_var.set(f"Pozostały czas: {remaining_time} s")

    # After clicking START on the start screen
    if condition == 2:
        # Create widget for displaying remaining time
        remaining_time_label = Label(root, textvariable=remaining_time_var, font=("Arial", 20))
        remaining_time_label.place(x=1500, y=100)
        # Create widget for displaying the image
        obrazek = Canvas(root, width=1137, height=1000)
        obrazek.place(x=100, y=20)
        obrazek.create_image((570, 500), image=img_1)
        # Bind LMB and RMB for drawing and deleting dots
        obrazek.bind("<ButtonPress-1>", draw_dot)
        obrazek.bind("<ButtonPress-3>", delete_dot)
        condition += 1
        nr_image += 1
        STIME = time.time()
        STIME2 = time.time()
        seconds = 0
        seconds2 = 0
        # Schedule the ad for this round
        schedule_ad()

    # Update game timer only if ad is not playing
    if not ad_playing:
        ETIME = time.time()
        seconds = ETIME - STIME
        remaining_time = max(0, int(czas_obrazka - seconds))
        if condition > 2:
            remaining_time_var.set(f"Pozostały czas: {remaining_time} s")

    # When time is up for an image
    if (seconds > czas_obrazka) and (condition == 3):
        # Cancel any scheduled ads
        if ad_scheduled_event_id is not None:
            root.after_cancel(ad_scheduled_event_id)
            ad_scheduled_event_id = None
            ad_scheduled = False

        if round_number >= 18:
            condition = -1
            obrazek.destroy()
            continue

        with open('czasy.txt', 'a') as log_file:
            log_file.write(f"KONIEC RUNDY: {int(time.time())}\n")

        obrazek.destroy()
        img1 = Image.open(img_names[nr_image % len(img_names)])
        img = ImageTk.PhotoImage(img1)
        obrazek = Canvas(root, width=1137, height=1000)
        obrazek.place(x=100, y=20)
        obrazek.create_image((570, 500), image=img)
        obrazek.bind("<ButtonPress-1>", draw_dot)
        obrazek.bind("<ButtonPress-3>", delete_dot)
        nr_image += 1
        # Update timers and round number
        STIME = time.time()
        paused_time = 0
        round_number += 1
        condition = 3  # Ensure condition remains 3 to continue the game
        # Reset ad scheduling variables
        ad_scheduled = False
        ad_scheduled_event_id = None
        # Schedule the ad for this round
        schedule_ad()

    if condition == -2:
        time.sleep(5)
        koniec.destroy()
        temp = time.time()
        KONIEC = temp - czas_gry

        # Save time data to file
        f = open('czasy.txt', 'a')
        f.write("CZAS ZAKONCZENIA: " + str(int(time.time())) + "\n" + "CALKOWITY CZAS EKSERYMENTU: " + str(
            KONIEC) + "\n\n==========================================================\n\n")
        f.close()
        break

    # When all images have been displayed
    if condition == -1:
        koniec = Label(root, text="KONIEC\nDzięki za udział! :)", font=("Arial", 80), anchor=CENTER)
        koniec.place(x=570, y=350)
        condition = -2

    root.update()
