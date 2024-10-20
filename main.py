#import tobii_research as tr # biblioteka do integracji z eyetrackerem
import time
from datetime import datetime
from tkinter import *
from PIL import ImageTk, Image

### zmienne do ktorych sa przypisywane wspolrzedne x y oczu odczytane z eyetrackera
global_leX = 0.0
global_leY = 0.0
global_reX = 0.0
global_reY = 0.0

dots = 0 # liczba postawionych przez użytkownika kropek
condition = 1 # bardzo ważna zmienna, w pętli pozwala się przemieszczać między kolejnymi etapami gry
czas_gry = 0
kropki = [] # lista na kropki które stawia użytkownik na obrazkach z gry

### wykrycie podłączonego eyetrackera
#TobiiEyeTracker = tr.find_all_eyetrackers()
#EyeTracker = TobiiEyeTracker[0]

"""
def gaze_data_callback(gaze_data):  # funkcja ktora odczytuje wspolrzedne spojrzenia na ekran i przypisuje je do zmiennych globalnych
        global global_leX
        global global_leY
        global global_reX
        global global_reY
        print("Left eye: ({global_gaze_left_eye}) \t Right eye: ({global_gaze_right_eye})".format(
            global_gaze_left_eye=gaze_data['left_gaze_point_on_display_area'],
            global_gaze_right_eye=gaze_data['right_gaze_point_on_display_area']))
        gaze_left_eye = gaze_data['left_gaze_point_on_display_area']
        gaze_right_eye = gaze_data['right_gaze_point_on_display_area']
        global_leX, global_leY = gaze_left_eye
        global_reX, global_reY = gaze_right_eye
"""

# metoda, którą podepnę pod zdarzenie klikniecia LPM nad kontrolką obrazek
# rysuje kropkę nad obrazkiem w miejscu kliknięcia
def draw_dot(event):
    #"#93F600"
    color = "black"
    global dots
    dots += 1

    # rysowanie kropki na obrazku
    x1, y1 = (event.x - 10), (event.y - 10)
    x2, y2 = (event.x + 10), (event.y + 10)
    id = obrazek.create_oval(x1, y1, x2, y2, fill=color, outline=color, width=14)
    kropki.append(id)
    x = x1+x2/2
    y = y1+y2/2
    # zapis informacji gdzie uzytkownik stawial kropki (nie pamietam po co mi to bylo xd)
    f = open('dots_xy.txt', 'a')
    f.write(str(dots) + ":\t x: " + str(x) + " y: " + str(y) + "\n")
    f.close()

# metoda, którą podepnę pod zdarzenie klikniecia PPM nad kontrolką obrazek
# usuwa ostatnio narysowaną kropkę
def delete_dot(event): # metoda, która podpinam pod zdarzenie klikniecia myszki nad kontrolką obrazek
    obrazek.delete(kropki[-1])
    del kropki[-1]

# Funkcja wywolywana po nacisnieciu przycisku START na ekranie startowym
def zacznij():
    global condition
    # kolejny etap gry
    condition = 2
    # Usuwanie elementow z ekranu startowego
    startup_text.destroy()
    startup_button.destroy()
    # zapis z timestempem z rozpoczecia gry
    f = open('czasy.txt', 'a')
    f.write("CZAS STARTU: " + str(datetime.now()) + "\n")
    f.close()
    global czas_gry
    czas_gry = time.time()

# zmienne dla obrazków: nr_image => ktory obrazek sie wyswietla;   img_names => sciezki do obrazkow
nr_image = 0
img_names = ["O/testowy_9_1.jpg", "O/testowy_6_1.jpg", "O/testowy_2_1.jpg", "O/testowy_8_1.jpg", "O/testowy_3_1.jpg", "O/testowy_7_1.jpg", "O/testowy_1_1.jpg", "O/testowy_5_1.jpg"]
czas_obrazka = 10 # co ile ma zmieniac sie obrazek w grze

# Stworzenie głownego okna aplikacji
root = Tk()
root.title("Find_the_difference_game")
root.geometry("1920x1080")
root.attributes('-fullscreen', True)

# Zmienna na info startowe z instrukcja dla uzytkownika
info = "Po kliknięciu przycisku \"START\" po kolei zostanie Ci wyświetlonych 8 obrazków.\n" \
       "Twoim zadaniem jest znalezienie na każdym z nich jak największej liczby określonych elementów.\n" \
       "Informacje o tym czego masz szukać będą znajdować się bezpośrednio pod każdym obrazkiem.\n" \
       "Na każdy z obrazków masz 75 sekund. Kiedy znajdziesz szukany element postaw na nim kropkę\n" \
       "lewym przyciskiem myszy (LPM). Aby usunąć postawioną kropkę użyj prawego przycisku myszy (PPM).\n\n " \
       "Naciśnij przycisk \"START\" aby rozpocząć" \

# Elementy ekranu startowego
startup_text = Label(root, text=info, font=("Arial", 20), anchor = CENTER)
startup_text.place(x=336, y=230) # metoda place we wszystkich kontrolkach sluzy do oznaczenia w jakiej pozycji
# (w pikselach) ma pojawic sie stworzona kontrolka w elemencie nadrzędnym (tutaj root, czyli okno głowne)
startup_button = Button(root, text="START", font=("Arial", 50), command = zacznij, anchor = CENTER) # command = zacznij
# oznacza ze po kliknieciu przycisku wywolywana jest funckja zacznij()
startup_button.place(x=820, y=500)

# Wczytanie pierwszego obrazka do zmiennej
img1 = Image.open(img_names[nr_image])
img_1 = ImageTk.PhotoImage(img1)

### Tutaj checkbox na ekranie glownym. Jesli uzytkownik go zaznaczy to po uruchomieniu gry, w prawym gornym rogu
### beda wyswietlane odczyty z eye-trackera w aplikacji
var2 = IntVar()
wyswietl_xy= Checkbutton(root, text="Wyswietlaj informacje o spojrzeniu", variable=var2, onvalue=1, offvalue=0)
wyswietl_xy.pack()
wyswietl_xy.place(x=1690, y=10)

# zmienne wykorzystywane do liczenia uplywu czasu badz mowiace aplikacji o tym z ktorym
# obrazkiem mamy obecnie doczynienia
STIME = time.time()
STIME2 = time.time()

# zmienne zwiazane z checkboxem
var = StringVar()
var.set("---")
flaga = 0

temp_leX = 0
temp_leY = 0
eyes_movement = "------"

#Ponizsza linia rozpoczyna zbieranie danych z eyetrackera
#EyeTracker.subscribe_to(tr.EYETRACKER_GAZE_DATA, gaze_data_callback, as_dictionary=True)

while(True):
    ### Badanie uplywu czasu
    ETIME = time.time()
    ETIME2 = time.time()
    seconds = ETIME - STIME # czas od wyswietlenia obrazka
    seconds2 = ETIME2 - STIME2 # czas aktualizacji odczytow z eytrackera

    ### Ponizej wyswietlanie danych z eye-trackera w aplikacji, raczej nie bedzie nam przydatne
    ### na razie zostawie

    if(global_leX == None) or (global_leY == None) or (temp_leX == None) or (temp_leY == None):
        eyes_movement = "------"
    elif((abs(global_leX - temp_leX) > 0.005) or (abs(global_leY - temp_leY) > 0.005)):
        eyes_movement = "SAKADA"
    else:
        eyes_movement = "FIKSACJA"

    temp_leX = global_leX
    temp_leY = global_leY
    if (condition == 2) and (var2.get() == 1):
        gaze_data = Label(root, background="grey", textvariable=var, width=38, height=3)
        gaze_data.place(x=1650, y=0)

    if(seconds2 > 0.2) and (var2.get() == 1):
        lx = round(global_leX, 4)
        ly = round(global_leY, 4)
        rx = round(global_reX, 4)
        ry = round(global_reY, 4)
        var.set("L_eye X:" + str(lx) + "   L_eye Y:" + str(ly) + "\nR_eye X:" + str(rx) + "   R_eye Y:" + str(ry) + "\n" + eyes_movement)
        STIME2 = time.time()

    ### Do tego ifa wpadamy po klkinieciu przycisku START na ekranie startowym
    if (condition == 2):
        # stworzenie kontrolki z obrazkiem
        # kontrolka Canvas pozwala na rysowanie na niej elementów. Uzytkownik do zaznaczania znalezionych elementow
        # uzywal LPM do narysowania kropki na znalezionym elemencie
        obrazek = Canvas(root, width = 1137, height = 1000)
        obrazek.place(x=100, y=20)
        obrazek.create_image((570, 500), image = img_1)
        # Podpiecie pod LMP rysoawania kropek, i pod PPM usuwania ostatnio narysowanej
        obrazek.bind("<ButtonPress-1>", draw_dot)
        obrazek.bind("<ButtonPress-3>", delete_dot)

        nr_image += 1
        condition += 1
        STIME = time.time()
        STIME2 = time.time()
        seconds = 0
        seconds2 = 0
        wyswietl_xy.destroy()  # usuwanie checkboxa

    # kiedy upłynął jakiś tam czas na obrazek
    if (seconds > czas_obrazka) and (condition == 3):
        if (nr_image > 7):
            condition = -1
            obrazek.destroy()
            continue
        obrazek.destroy()  # Ponizej zastapienie starego obrazka nowym
        img1 = Image.open(img_names[nr_image]) # Otworzenie obrazka po ścieżce
        img = ImageTk.PhotoImage(img1)
        # To samo co wczesniej, opis gdzieś wyżej
        obrazek = Canvas(root, width=1137, height=1000)
        obrazek.place(x=100, y=20)
        obrazek.create_image((570, 500), image=img)
        obrazek.bind("<ButtonPress-1>", draw_dot)
        obrazek.bind("<ButtonPress-3>", delete_dot)

        nr_image += 1

        STIME = time.time()                    #od nowa mierzymy czas do wyswietlenia nastepnego obrazka

    ### Tutaj aplikacja tkwi 5 sekund przed wylaczeniem się
    if(condition == -2):
        time.sleep(5) # zatrzymujemy na 5 sekund aby podziękowanie bylo przez tyle widoczne dla badanego
        koniec.destroy()
        temp = time.time()
        KONIEC = temp - czas_gry # obliczenie czasu zakonczenia badania

        # zapis danych o czasie do pliku
        f = open('czasy.txt', 'a')
        f.write("CZAS ZAKONCZENIA: " + str(datetime.now()) + "\n" + "CAŁKOWITY CZAS EKSERYMENTU: " + str(KONIEC) + "\n\n==========================================================\n\n")
        f.close()

        #EyeTracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA, gaze_data_callback) #zakonczenie pracy eyetrackera
        break

    ### Tutaj wpadamy kiedy wszystkie obrazki zostana wyswietlone
    if(condition == -1):
        koniec = Label(root, text="KONIEC\nDzięki za udział! :)", font=("Arial", 80), anchor=CENTER)
        koniec.place(x=570, y=350)
        condition = -2

    root.update()
