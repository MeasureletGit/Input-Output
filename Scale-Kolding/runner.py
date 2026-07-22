import os
import subprocess as sp
import tkinter as tk
import threading as thr
import time
import datetime
import platform
from tkinter import messagebox
import socket
import psutil
from tkinter.messagebox import showerror
import http.client
from urllib.parse import urlparse

import customtkinter as ctk
# import zxing

import aws_uploader as au
import Kern


test = 24
LEDs = 17
if platform.platform()[0:7] != 'Windows':
    import RPi.GPIO as GPIO
    sp.Popen(['xrandr', '-o', 'inverted'])
    sp.Popen(["xinput", "set-prop", "10-0038generic ft5x06 (00)", "Coordinate Transformation Matrix", "-1", "0", "1", "0", "-1", "1", "0", "0", "1"])
    sp.Popen(["xinput", "set-prop", "generic ft5x06 (79)", "Coordinate Transformation Matrix", "-1", "0", "1", "0", "-1", "1", "0", "0", "1"])
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(LEDs, GPIO.OUT)
    GPIO.setup(test, GPIO.OUT)

sp.Popen(["python", "inputreader.py"])

def makeupper1(*args):
    global input1
    if len(input1.get()) == 1:
        input1.set(input1.get().upper())

def makeupper2(*args):
    global input2
    if len(input2.get()) == 1:
        input2.set(input2.get().upper())

def readmass():
    global massv
    massv.set( str(int(Kern.getMass()))+" g")
    win.after(1000, readmass)


def zeroscale():
    zero = Kern.zero()
    #print("zero bliver kaldt") test for at se om den blev kaldt

def gpiocommand(on,myport):
    try:
        if on:
            # print('')
            # if platform.platform()[0:7] != 'Windows':
            mycmd = GPIO.HIGH
        elif not on: # off
            # print('')
            # if platform.platform()[0:7] != 'Windows':
            mycmd = GPIO.LOW

        # command
        # if platform.platform()[0:7] != 'Windows':
        GPIO.output(myport,mycmd)

        # print('switched : ' + str(myport) + ' to ' + str(on))
        scs = True
    except:
        scs = False


    return scs

def leds_on():
    gpiocommand(True,LEDs)

def leds_off():
    gpiocommand(False,LEDs)

def test_on():
    gpiocommand(True, test)

def test_off():
    gpiocommand(False, test)

test_off()

def onscreenkeyboard(test):
    if platform.platform()[0:7] != 'Windows':
        #sp.Popen(['setxkbmap', 'dk'])
        sp.Popen(['onboard'])

def inputname(name):
    backstaff.destroy()
    print(name)

# reader = zxing.BarCodeReader()
win = tk.Tk()
win.config(bg='white')
win.title('Measurelet Input')
win.geometry('800x480')
if platform.platform()[0:7] != 'Windows':
    win.wm_attributes('-fullscreen', 'True')
    win.config(cursor="none")
win.resizable(0,0)
win.event_generate('<Motion>', warp=True, x=0, y=480)

software_version = '1.0.1a' #Bruger vi ikke da vi ikke har et versions system endnu

my_id = ''
mode = ''
cprn = ''
back = ''
name = ''
backstaff = ''
backstaffpicker = ''
backswitch = ''
massv = tk.StringVar()
input1 = tk.StringVar()
input2 = tk.StringVar()

# massv.set('0 g')

scale_type = 'input'

with open('setup.txt', 'r') as stp:
    scale_type = stp.readline().strip()
    if scale_type not in ('input', 'output'):
        scale_type = 'input'

def open_keyboard():
    if platform.platform()[0:7] != 'Windows':
        sp.Popen(['onboard', "--layout", "Phone", "--theme", "HighContrast"])

def close_keyboard():
    if platform.platform()[0:7] != 'Windows':
        sp.Popen(['sudo', 'pkill', '-9', 'onboard'])

def standby(back_frame):
    back_frame.destroy()
    black_button = tk.Button(master=win, command=lambda: close_black_button(black_button), fg='black', bg='black')
    black_button.pack(expand=True,fill='both')
    black_button.focus_set()

def close_black_button(black_button):
    black_button.destroy()
    welcome()

'''def input_choice(type, weight, comment, container_type=None):
    global backstaffpicker, massv
    print('her')

    input1.set('')

    backstaffpicker.destroy()

    comment = comment.replace(';', '')

    backstaffpicker = tk.Frame(master=win, bg='#fafafa')
    backstaffpicker.pack(fill=tk.BOTH, expand=1)

    leftframe = tk.Frame(master=backstaffpicker, bg='#fafafa', height=1)
    leftframe.pack(fill=tk.BOTH, expand=1)

    rightframe = tk.Frame(master=backstaffpicker, bg='#fafafa', height=10)
    rightframe.pack(fill=tk.BOTH, expand=1)

    backstaffpicker.rowconfigure(0, weight=1)
    backstaffpicker.rowconfigure(1, weight=2)
    backstaffpicker.grid_columnconfigure(0, weight=1)

    input_label = tk.Label(master=leftframe, text=str(massv.get()), bg='#fafafa', height=1, width=1)
    input_label.place(x=335, y=20, height=60, width=125)
    input_label.config(font=('Helvetica', 25))

    drink_label = tk.Label(master=backstaffpicker, text='Vælg hvad du har drukket', bg='#fafafa')
    drink_label.place(x=150, y=115, height=30, width=500)
    drink_label.config(font=("Helvetica", 20))

    # Sæt ens kolonne-bredder
    leftframe.grid_columnconfigure(0, weight=1, minsize=200)
    leftframe.grid_columnconfigure(1, weight=1, minsize=200)

    # Sæt 2 ekstra tomme rækker øverst + 3 rækker med knapper
    for i in range(5):
        leftframe.grid_rowconfigure(i, weight=1, minsize=80)

    # Fælles stil og størrelse for knapper
    common_width = 20
    common_font = ('Helvetica', 25)
    common_style = {
        "master": leftframe,
        "bg": '#007f93',
        "fg": 'white',
        "height": 2,
        "width": common_width,
        "font": common_font
    }

    # Ryk alle knapper ned med 2 rækker (starter fra row=2 nu)

    # Øverste række
    tk.Button(**common_style, text='Vand', command=lambda: verify(type, weight, "Vand", container_type)).grid(row=2, column=0, padx=5, pady=5, sticky='NSEW')
    tk.Button(**common_style, text='Mælk', command=lambda: verify(type, weight, "Mælk", container_type)).grid(row=2, column=1, padx=5, pady=5, sticky='NSEW')

    # Midterste række
    tk.Button(**common_style, text='Kaffe', command=lambda: verify(type, weight, "Kaffe", container_type)).grid(row=3, column=0, padx=5, pady=5, sticky='NSEW')
    tk.Button(**common_style, text='Sodavand', command=lambda: verify(type, weight, "Sodavand", container_type)).grid(row=3, column=1, padx=5, pady=5, sticky='NSEW')

    # Nederste række
    tk.Button(**common_style, text='The', command=lambda: verify(type, weight, "The", container_type)).grid(row=4, column=0, padx=5, pady=5, sticky='NSEW')


    tk.Button(**common_style, text='Andet', command = lambda: approve(type, weight, comment)).grid(row=4, column=1, padx=5, pady=5, sticky='NSEW')

        
    backstafftest = tk.Button(master=backstaffpicker, text='Tilbage', bg='#525252', command=lambda: cancel(),
    fg='white', width=100, height=50)
    backstafftest.place(x=650, y=20, height=60, width=125)
    backstafftest.config(font=('Helvetica', 15))

    leftframe.rowconfigure(0, weight=1)
    leftframe.rowconfigure(1, weight=1)
    leftframe.grid_columnconfigure(0, weight=2)
    leftframe.grid_columnconfigure(1, weight=1)

    input1.trace('w', makeupper1)

    #vand_button.update()
    #maelk_button.update()
    #kaffe_button.update()
    #sodavand_button.update()
    #the_button.update()
    #andet_button.update()

    backstaffpicker.update()
'''
def approve(type, weight, comment='', container_type=None):
    global backstaffpicker, massv, input1
    print('her')

    input1.set('')

    backstaffpicker.destroy()

    comment = comment.replace(';', '')

    backstaffpicker = tk.Frame(master=win, bg='#fafafa')
    backstaffpicker.pack(fill=tk.BOTH, expand=1)

    leftframe = tk.Frame(master=backstaffpicker, bg='#fafafa', height=1)
    leftframe.pack(fill=tk.BOTH, expand=1)

    rightframe = tk.Frame(master=backstaffpicker, bg='#fafafa', height=10)
    rightframe.pack(fill=tk.BOTH, expand=1)

    backstaffpicker.rowconfigure(0, weight=1)
    backstaffpicker.rowconfigure(1, weight=2)
    backstaffpicker.grid_columnconfigure(0, weight=1)

    input_label = tk.Label(master=leftframe, text=str(massv.get()), bg='#fafafa', height=1, width=1)
    input_label.grid(row=0, column=0, padx=5, pady=5, sticky='NSEW')
    input_label.config(font=('Helvetica', 25))

    #Her er keyboarded til at skrive hvilken type væske de har indtaget
    input = tk.Entry(master=leftframe, textvariable=input1, bg='white', width=1)
    input.grid(row=1, column=0, padx=5, pady=5, sticky='EW')
    input.config(font=('Helvetica', 25))

    # Bind directly to enforce character limit
    input.bind("<KeyPress>", lambda event: "break" if len(input.get()) >= 10 and event.keysym not in ("BackSpace", "Delete", "Left", "Right") else None)

    # Optional: Bind focus event for the keyboard
    input.bind("<FocusIn>", lambda event: open_keyboard())

    accept_button = tk.Button(master=leftframe, text='Godkend', command=lambda: verify(type, weight, input.get(), container_type), bg='#007f93', fg='white', height=1, width=1)
    accept_button.grid(row=0, column=1, padx=5, pady=5, sticky='NSEW')
    accept_button.config(font=('Helvetica', 25))
    # accept_button.pack()

    cancel_button = tk.Button(master=leftframe, text='Annuller', command=lambda: cancel(), bg='#525252', fg='white', height=1, width=1)
    cancel_button.grid(row=1, column=1, padx=5, pady=5, sticky='NSEW')
    cancel_button.config(font=('Helvetica', 25))
    # cancel_button.pack()

    with open('setup.txt', 'r') as stp:
        scale_type = stp.readline().strip()
    if scale_type not in ('output'):
        drink_label = tk.Label(master=backstaffpicker, text='Indtast drikkevare', bg='#fafafa')
        drink_label.place(x=118, y=160, height=28, width=300)
        drink_label.config(font=("Helvetica", 20))

    with open('setup.txt', 'r') as stp:
        scale_type = stp.readline().strip()
    if scale_type not in ('input'):
        drink_label = tk.Label(master=backstaffpicker, text='Kommentar', bg='#fafafa')
        drink_label.place(x=105, y=160, height=22, width=300)
        drink_label.config(font=("Helvetica", 20))
    

    leftframe.rowconfigure(0, weight=1)
    leftframe.rowconfigure(1, weight=1)
    leftframe.grid_columnconfigure(0, weight=2)
    leftframe.grid_columnconfigure(1, weight=1)

    input1.trace('w', makeupper1)

    input.focus_set()

    accept_button.update()
    cancel_button.update()

    backstaffpicker.update()


def set_container(type, weight, comment=''):
    global backstaffpicker, massv, input1
    comment = comment.replace(';', '')

    glass_weight = 155
    cup_weight = 230
    plasticGlass_weight = 50

    input1.set('')

    backstaffpicker.destroy()

    backstaffpicker = tk.Frame(master=win, bg='#fafafa')
    backstaffpicker.pack(fill=tk.BOTH, expand=1)

    backstafftest = tk.Button(master=backstaffpicker, text='Tilbage', bg='#525252', command=lambda: cancel(),
        fg='white', width=100, height=50)
    backstafftest.place(x=650, y=40, height=60, width=125)
    backstafftest.config(font=('Helvetica', 15))

    button1 = tk.Button(master=backstaffpicker, text='Glas', command = lambda: approve(type, str(int(weight) - glass_weight), comment, "Hvid plastikkop"), bg = '#007f93', fg = 'white', height = 1, width = 1)
    button1.grid(row=0, column=0, padx=25, pady=125, sticky='NSEW')
    button1.config(font=('Helvetica', 25))
    # button1.pack()

    button2 = tk.Button(master=backstaffpicker, text='Kop', command = lambda: approve(type, str(int(weight) - cup_weight), comment, "Papkop"), bg = '#007f93', fg = 'white', height = 1, width = 1)
    button2.grid(row=0, column=1, padx=25, pady=125, sticky='NSEW')
    button2.config(font=('Helvetica', 25))
    # button2.pack()

    button3 = tk.Button(master=backstaffpicker, text='Plastikglas', command = lambda: approve(type, str(int(weight) - plasticGlass_weight), comment, "Tudekop"), bg = '#007f93', fg = 'white', height = 1, width = 1)
    button3.grid(row=0, column=2, padx=25, pady=125, sticky='NSEW')
    button3.config(font=('Helvetica', 25))
    # button3.pack()

    backstaffpicker.rowconfigure(0, weight=1)
    backstaffpicker.grid_columnconfigure(0, weight=1)
    backstaffpicker.grid_columnconfigure(1, weight=1)
    backstaffpicker.grid_columnconfigure(2, weight=1)

    backstaffpicker.update()

    button1.update()
    button2.update()
    button3.update()

def set_container_output(type, weight, comment=''):
    global backstaffpicker, massv, input1
    comment = comment.replace(';', '')

    diaper_weight = 100
    bedpan_weight = 345
    flask_weight = 110  

    input1.set('')

    backstaffpicker.destroy()

    backstaffpicker = tk.Frame(master=win, bg='#fafafa')
    backstaffpicker.pack(fill=tk.BOTH, expand=1)

    backstafftest = tk.Button(master=backstaffpicker, text='Tilbage', bg='#525252', command=lambda: cancel(),
        fg='white', width=100, height=50)
    backstafftest.place(x=650, y=40, height=60, width=125)
    backstafftest.config(font=('Helvetica', 15))

    button1 = tk.Button(master=backstaffpicker, text='Ble',
        command=lambda: approve(type, str(int(weight) - diaper_weight), comment, "Ble"),
        bg='#007f93', fg='white', height=1, width=1)
    button1.grid(row=0, column=0, padx=25, pady=125, sticky='NSEW')
    button1.config(font=('Helvetica', 25))

    button2 = tk.Button(master=backstaffpicker, text='Grøn bækken \n uden låg',
        command=lambda: approve(type, str(int(weight) - bedpan_weight), comment, "Bækken"),
        bg='#007f93', fg='white', height=1, width=1)
    button2.grid(row=0, column=1, padx=25, pady=125, sticky='NSEW')
    button2.config(font=('Helvetica', 25))

    button3 = tk.Button(master=backstaffpicker, text='Kolbe',
        command=lambda: approve(type, str(int(weight) - flask_weight), comment, "Kolbe"),
        bg='#007f93', fg='white', height=1, width=1)
    button3.grid(row=0, column=2, padx=25, pady=125, sticky='NSEW')
    button3.config(font=('Helvetica', 25))

    backstaffpicker.rowconfigure(0, weight=1)
    backstaffpicker.grid_columnconfigure(0, weight=1)
    backstaffpicker.grid_columnconfigure(1, weight=1)
    backstaffpicker.grid_columnconfigure(2, weight=1)

    backstaffpicker.update()

    button1.update()
    button2.update()
    button3.update()


last_measurement = None
def verify(type, mass, comment='', container_type=None):
    global backstaffpicker
    global last_measurement  

    comment = comment.replace(';', '')

    close_keyboard()

    if mass == '--':
        mass = '0'

    current_measurement = (type, mass, comment, container_type)

    if last_measurement is not None:
        try:
            if abs(int(mass) - int(last_measurement)) <= 1:
                # Vis popup med mulighed for at annullere
                proceed = messagebox.askyesno(
                    "Advarsel",
                    "Denne måling er ens med den seneste måling. Vil du fortsætte?"
                )
                if not proceed:
                    # Brugeren annullerede målingen
                    rungui_s()
                    return
        except:
            pass


    # Forhindr 0 gram målinger
    try:
        if int(mass) <= 0 and "kropsvægt" not in comment.lower():
            showerror("Fejl", "Måling der vejer mindre end beholder er ikke tilladt.")
            rungui_s()
            return
    except ValueError:
        showerror("Fejl", "Ugyldig måling.")
        rungui_s()
        return
    
    with open('configuration.txt', 'r') as t:
        try:
            au.uploadmeasurement(mass, type, comment)
        except:
            print('could not upload measurement')

    backstaffpicker.destroy()

    backstaffpicker = tk.Frame(master=win, bg='#fafafa')
    backstaffpicker.pack(fill=tk.BOTH, expand=1)

    weight_label = tk.Label(master=backstaffpicker, text='Måling registreret!', bg='#fafafa', fg='#575756')
    weight_label.grid(row=0, column=1, sticky='NSEW', padx=10, pady=10)
    weight_label.config(font=('Helvetica', 35))

    backstaffpicker.grid_columnconfigure(0, weight=1)
    backstaffpicker.grid_columnconfigure(1, weight=1)
    backstaffpicker.grid_columnconfigure(2, weight=1)
    backstaffpicker.rowconfigure(0, weight=1)
    backstaffpicker.rowconfigure(1, weight=1)


    if container_type == 'Hvid plastikkop' and type =='K':
        typs = 'Hvid plastikkop '
    elif container_type == 'Hvid plastikkop' and type =='I':
        typs = 'Hvid plastikkop'
    elif container_type == 'Papkop' and type == 'K':
        typs = 'Papkop '
    elif container_type == 'Papkop' and type == 'I':
        typs = 'Papkop'
    elif container_type == 'Tudekop' and type == 'K':
        typs = 'Tudekop '
    elif container_type == 'Tudekop' and type == 'I':
        typs = 'Tudekop'
    elif container_type == 'IV' and type =='V':
        typs = 'IV'
    elif container_type == 'IV' and type == 'K': 
        typs = 'IV '
    elif type == 'U':
        typs = 'urin'
    elif type == 'A':
        typs = 'afføring'
    elif type == 'B':
        typs = 'andet'
    else:
        typs = 'andet'

    minus = ''
    if type == 'K':
        minus = '-'


    if container_type in ('Hvid plastikkop', 'Papkop', 'Tudekop', 'IV'):
        with open('measurements.txt', 'a') as gf:
            timenow = datetime.datetime.now()
            gf.write(timenow.strftime("%d-%m-%Y, %H:%M:%S") + f';{typs};{comment};{minus}{mass} g\n')
    elif type in ('U', 'A', 'B') and "kropsvægt" not in comment.lower():
        with open('measurements.txt', 'a') as gf:
            timenow = datetime.datetime.now()
            gf.write(timenow.strftime("%d-%m-%Y, %H:%M:%S") + f';{typs};{comment};{minus}{int(mass)} g\n')
    else:
        with open('measurements.txt', 'a') as gf:
            timenow = datetime.datetime.now()
            gf.write(timenow.strftime("%d-%m-%Y, %H:%M:%S") + f';{typs};{comment};{minus}{int(mass)} g\n')

 
    last_measurement = int(mass)
  

    backstaffpicker.update()
    win.after(3000, rungui_s)



def cancel():
    global backstaffpicker, mode

    close_keyboard()

    if mode == 'multiuse':
        test_on()

    rungui()

#Det her bruges til at sørge for at kun rigtige danske cpr-numre blvier scannet, men det laver problemer med udlandske folk der gerne må have bogstaver i de sidste 4 cifre
def is_valid_cpr(cpr):
    if len(cpr) != 10:
        return False
    if not cpr[:6].isdigit():
        return False
    day = int(cpr[:2])
    month = int(cpr[2:4])
    year = int(cpr[4:6])
    return 1 <= day <= 31 and 1 <= month <= 12

def extract_cpr_from_scanned(text):
    if not text:
        return None

    text = text.strip()

    # Fjern 'AC' eller 'A' i starten
    if len(text) >= 2 and text[1].lower() == 'c':
        text = text[2:]
    elif text[0].lower() == 'a':
        text = text[1:]

    # Tag de første 10 cifre (ignorer bogstaver)
    candidate = ''.join([c for c in text if c.isdigit()][:10])

    # Tjek om vi faktisk fik 10 cifre
    if len(candidate) != 10:
        return None

    # Valider CPR
    if is_valid_cpr(candidate):
        return candidate
    else:
        return None

def check_input(e):
    global my_id, cprn, mode

    print(e.char, flush=True)

    if e.char == '\r' or e.char == '\n':
        cprn = ''
        time.sleep(.1)

        # Læs rå linje fra fil
        with open('measurelet.ID', 'r') as g:
            scanned = g.readline().strip()
            print('raw scanned:', scanned, flush=True)

            # Ekstraher CPR (funktionen gør validering)
            cprn = extract_cpr_from_scanned(scanned)
            if not cprn:
                messagebox.showerror("CPR-fejl", "Ugyldigt CPR-nummer")
                return

        # Sørg for at cprn kun indeholder cifre (sikkerhed)
        cprn = ''.join([c for c in cprn if c.isdigit()])[:10]
        if len(cprn) != 10:
            messagebox.showerror("CPR-fejl", "Ugyldigt CPR-nummer")
            return

        # Ryd alt tastet input så tidligere navne/kommentarer ikke kan blive gemt
        my_id = ''

        # (Valgfrit men nyttigt) Overskriv measurelet.ID med kun CPR, så filen er "ren"
        # Hvis du ikke vil overskrive scanner-filen, kan du fjerne denne blok.
        try:
            with open('measurelet.ID', 'w') as g:
                g.write(cprn + '\n')
        except Exception as ex:
            print("Kunne ikke overskrive measurelet.ID:", ex, flush=True)

        # Specialkommando
        if cprn == '2468135790':
            with open('setup.txt', 'r') as ses:
                put = ses.readline().strip()
            put = 'output' if put == 'input' else 'input'
            with open('setup.txt', 'w') as sew:
                sew.write(put + '\n')

        print('CPR gemt:', cprn, flush=True)

        if mode == 'singleuse':
            test_on()
            checkinput()
        elif mode == 'multiuse':
            # Her skriver vi kun CPR: ingen andre variable kan komme med
            with open('configuration.txt', 'w') as c:
                c.write('multiuse;' + str(cprn) + ';\n')
                mode = 'multiuse'
            multi_scan()

    elif e.char.isalnum() or e.char == ',':
        my_id += e.char


''' Gammel version af check input hvor der var fejl med at cpr numre kunne blive scannet forkert
def check_input(e):
    global my_id, cprn, mode
    # print(e, flush=True)

    print(e.char, flush=True)

    if e.char == '\r' or e.char == '\n':
        # print('id is : ', my_id, flush=True)
        # cprn = my_id
        cprn = ''
        time.sleep(.1)
        with open('measurelet.ID', 'r') as g:
            rl = g.readline().strip()
            print(rl, flush=True)
            cprn = rl
            g.close()
        if cprn == '2468135790':
            put = ''
            with open('setup.txt', 'r') as ses:
                put = ses.readline().strip()
            if put == 'input':
                put = 'output'
            else:
                put = 'input'
            with open('setup.txt', 'w') as sew:
                sew.write(put + '\n')
        print('enter', flush=True)
        if mode == 'singleuse':
            test_on()
            print('check input', flush=True)
            checkinput()
        elif mode == 'multiuse':
            with open('configuration.txt', 'w') as c:
                c.write('multiuse;' + str(cprn) + '; \n')
                mode = 'multiuse'
            multi_scan()
    elif e.char.isalnum() or e.char == ',':
        my_id += e.char'''


'''
    found = True
    while found:
        with open('measurelet.ID', 'r') as g:
            rl = g.readline().strip()
            print(rl, flush=True)
            cprn = rl
            found = False
        time.sleep(.5)
    '''

def check_service_code(e):
    global scale_type

    if e.char == '\r' or e.char == '\n':
        time.sleep(.1)
        with open('measurelet.ID', 'r') as g:
            rl = g.readline().strip()
            g.close()
            if rl == '6969696969':
                if scale_type == 'output':
                    scale_type = 'input'
                else:
                    scale_type = 'output'


def multi_scan():
    global cprn, backstaffpicker

    if scale_type == 'input':
        still_looking = True

        # test_on()

        time.sleep(.2)
        if platform.platform()[0:7] != 'Windows':
            while still_looking:
                time.sleep(.2)
                print('still looking', flush=True)
                with open('measurelet.ID', 'r') as f:
                    try:
                        cpr_s = f.readline().strip()
                        if len(cpr_s) > 0:
                            cprn = cpr_s
                            still_looking = False
                    except:
                        pass

        test_off()

        with open('measurelet.ID', 'w') as d:
            d.write(' \n')

        if len(cprn) > 10:
            cprn = cprn[2:12]

        # au.uploadmeasurement(Kern.getMass(), 'I', cprn)

        backstaffpicker.destroy()

        backstaffpicker = tk.Frame(master=win, bg='#fafafa')
        backstaffpicker.pack(fill=tk.BOTH, expand=1)

        backstafftop = tk.Frame(master=backstaffpicker, bg='#fafafa')
        backstafftop.pack(fill=tk.BOTH, expand=1)

        backstaffbottom = tk.Frame(master=backstaffpicker, bg='#fafafa')
        backstaffbottom.pack(fill=tk.BOTH, expand=1)

        backstaffpicker.rowconfigure(0, weight=1)
        backstaffpicker.rowconfigure(1, weight=1)
        backstaffpicker.grid_columnconfigure(0, weight=1)

        weight_label = tk.Label(master=backstafftop, textvariable=massv, bg='#fafafa', fg='#575756')
        weight_label.grid(row=1, column=0, sticky='NSEW', padx=10, pady=10)
        weight_label.config(font=('Helvetica', 45))

        weight_name_label = tk.Label(master=backstafftop, text=str(cprn)[0:6] + '-xxxx', bg='#fafafa', fg='#575756')
        weight_name_label.grid(row=2, column=0, sticky='NSEW', padx=10, pady=10)
        weight_name_label.config(font=('Helvetica', 25))

        backstafftop.rowconfigure(0, weight=1)
        backstafftop.rowconfigure(1, weight=1)
        backstafftop.rowconfigure(2, weight=1)
        backstafftop.grid_columnconfigure(0, weight=1)

        text_label = tk.Label(master=backstaffpicker, text='Sæt først koppen på vægten', bg='#fafafa')
        text_label.place(x=205, y=185, height=33, width=400)
        text_label.config(font=("Helvetica", 20))


        weight_button1 = tk.Button(master=backstaffpicker, text='Tilføj', command=lambda: set_container('I', massv.get()[:-2]),
                                   bg='#007f93',
                                   fg='white', height=1, width=1)
        # weight_button1.grid(row=0, column=0, sticky='NSEW', padx=10, pady=10)
        weight_button1.place(x=20, y=300, height=150, width=350)
        weight_button1.config(font=('Helvetica', 25))
        # weight_button1.pack()

        weight_button2 = tk.Button(master=backstaffpicker, text='Kassér', command=lambda: set_container('K', massv.get()[:-2]),
                                   bg='#b64909', fg='white', height=1, width=1)
        # weight_button2.grid(row=0, column=1, sticky='NSEW', padx=10, pady=10)
        weight_button2.place(x=420, y=300, height=150, width=350)
        weight_button2.config(font=('Helvetica', 25))
        # weight_button2.pack()

        iv = tk.Button(master=backstaffpicker, text='IV', bg='#525252', command=lambda: iv_measurement(),
                                        fg='white', width=100, height=50)
        iv.place(x=40, y=40, height=60, width=125)
        iv.config(font=('Helvetica', 15))

        ''' Ikke noget vi bruger endnu
        b_weight = tk.Button(master=backstaffpicker, text='Kropsvægt', bg='#525252', command=lambda: body_weight(),
                                            fg='white', width=100, height=50)
        b_weight.place(x=40, y=100, height=60, width=125)
        b_weight.config(font=('Helvetica', 15))
        '''

        # weight_button2.grid(row=3, column=1, sticky='NSEW', padx=10, pady=10)
        # weight_button2.config(font=('Helvetica', 25))

        # backstafftest = tk.Button(master=backstaffpicker, text='Tilbage', bg='#525252', command=lambda: lukvindue(),
                                  # fg='white', width=100, height=50)
        # backstafftest.place(x=650, y=40, height=60, width=125)

        # weight_button3 = tk.Button(master=backstaffbottom, text='Andet', command=lambda: approve('B', massv.get()[:-2]),
                                   # bg='#936c00', fg='white', height=1, width=1)
        # weight_button3.grid(row=0, column=2, sticky='NSEW', padx=10, pady=10)
        # weight_button3.config(font=('Helvetica', 25))

        '''
        weight_button1 = tk.Button(master=backstaffpicker, text='Tilføj', command=lambda: add_measurement('t'), bg='#007f93',
                                   fg='white', height=1, width=1)
        weight_button1.grid(row=1, column=0, sticky='NSEW', padx=10, pady=10)
        weight_button1.config(font=('Helvetica', 25))
    
        weight_button2 = tk.Button(master=backstaffpicker, text='Kassér', command=lambda: add_measurement('k'),
                                   bg='#b64909', fg='white', height=1, width=1)
        weight_button2.grid(row=1, column=1, sticky='NSEW', padx=10, pady=10)
        weight_button2.config(font=('Helvetica', 25))
        '''

        backstafftest = tk.Button(master=backstaffpicker, text='Tilbage', bg='#525252', command=lambda: lukvindue(),
                                  fg='white', width=100, height=50)
        backstafftest.place(x=650, y=40, height=60, width=125)
        backstafftest.config(font=('Helvetica', 15))
        # backstafftest.pack()

        reset = tk.Button(master=backstaffpicker, text='Nulstil', bg='#525252', command=lambda: zeroscale(),
                                        fg='white', width=100, height=50)
        reset.place(x=650, y=100, height=60, width=125)
        reset.config(font=('Helvetica', 15))

        # weight_button3 = tk.Button(master=backstaffbottom, text='Tilbage', bg='#525252', command=lambda: lukvindue(),
                                   # fg='white', height=1, width=1)
        # weight_button3.grid(row=0, column=2, sticky='NSEW', padx=10, pady=10)
        # weight_button3.config(font=('Helvetica', 25))

        backstaffbottom.rowconfigure(0, weight=1)
        backstaffbottom.grid_columnconfigure(0, weight=1)
        backstaffbottom.grid_columnconfigure(1, weight=1)
        backstaffbottom.grid_columnconfigure(2, weight=1)

        # test_on()

        time.sleep(.2)

        backstaffpicker.bind("<KeyRelease>", check_input)


        massv.set('-- g')

        backstaffpicker.focus_set()

        weight_button1.update()
        weight_button2.update()
        reset.update()
        iv.update()
        backstafftest.update()
        #b_weight.update()

        # win.after(100, zeroscale)

        # thread1 = thr.Thread(target=readmass)
        # thread1.start()

        # backstaffpicker = tk.Frame(master=win, bg='white')
        # backstaffpicker.pack(fill=tk.BOTH, expand=1)
    else:
        still_looking = True

        time.sleep(.2)
        if platform.platform()[0:7] != 'Windows':
            while still_looking:
                time.sleep(.2)
                print('still looking', flush=True)
                with open('measurelet.ID', 'r') as f:
                    try:
                        cpr_s = f.readline().strip()
                        if len(cpr_s) > 0:
                            cprn = cpr_s
                            still_looking = False
                    except:
                        pass

        test_off()

        with open('measurelet.ID', 'w') as d:
            d.write(' \n')

        if len(cprn) > 10:
            cprn = cprn[2:12]

        backstaffpicker.destroy()

        backstaffpicker = tk.Frame(master=win, bg='#fafafa')
        backstaffpicker.pack(fill=tk.BOTH, expand=1)

        backstafftop = tk.Frame(master=backstaffpicker, bg='#fafafa')
        backstafftop.pack(fill=tk.BOTH, expand=1)

        backstaffbottom = tk.Frame(master=backstaffpicker, bg='#fafafa')
        backstaffbottom.pack(fill=tk.BOTH, expand=1)

        backstaffpicker.rowconfigure(0, weight=1)
        backstaffpicker.rowconfigure(1, weight=1)
        backstaffpicker.grid_columnconfigure(0, weight=1)

        weight_label = tk.Label(master=backstafftop, textvariable=massv, bg='#fafafa', fg='#575756')
        weight_label.grid(row=1, column=0, sticky='NSEW', padx=10, pady=10)
        weight_label.config(font=('Helvetica', 45))

        weight_name_label = tk.Label(master=backstafftop, text=str(cprn)[0:6] + '-xxxx', bg='#fafafa', fg='#575756')
        weight_name_label.grid(row=2, column=0, sticky='NSEW', padx=10, pady=10)
        weight_name_label.config(font=('Helvetica', 25))

        backstafftop.rowconfigure(0, weight=1)
        backstafftop.rowconfigure(1, weight=1)
        backstafftop.rowconfigure(2, weight=1)
        backstafftop.grid_columnconfigure(0, weight=1)

        text_label = tk.Label(master=backstaffpicker, text='Sæt først beholder/ble på vægten', bg='#fafafa')
        text_label.place(x=150, y=185, height=33, width=500)
        text_label.config(font=("Helvetica", 20))

        weight_button1 = tk.Button(master=backstaffpicker, text='Urin',
                                   command=lambda: set_container_output('U', massv.get()[:-2]), bg='#007f93', fg='white',
                                   height=1, width=1)
        weight_button1.place(x=20, y=300, height=150, width=240)
        weight_button1.config(font=('Helvetica', 25))
        # weight_button1.pack()

        weight_button2 = tk.Button(master=backstaffpicker, text='Afføring',
                                   command=lambda: set_container_output('A', massv.get()[:-2]), bg='#b64909', fg='white',
                                   height=1, width=1)
        weight_button2.place(x=280, y=300, height=150, width=240)
        weight_button2.config(font=('Helvetica', 25))
        # weight_button2.pack()

        weight_button3 = tk.Button(master=backstaffpicker, text='Andet',
                                   command=lambda: set_container_output('B', massv.get()[:-2]), bg='#00935e', fg='white',
                                   height=1, width=1)
        weight_button3.place(x=540, y=300, height=150, width=240)
        weight_button3.config(font=('Helvetica', 25))
        # weight_button3.pack()

        backstafftest = tk.Button(master=backstaffpicker, text='Tilbage', bg='#525252', command=lambda: lukvindue(),
                                  fg='white', width=100, height=50)
        backstafftest.place(x=650, y=40, height=60, width=125)
        backstafftest.config(font=('Helvetica', 15))
        # backstafftest.pack()

        reset = tk.Button(master=backstaffpicker, text='Nulstil', bg='#525252', command=lambda: zeroscale(),
                                        fg='white', width=100, height=50)
        reset.place(x=650, y=100, height=60, width=125)
        reset.config(font=('Helvetica', 15))

        ''' ikke i brug endnu
        b_weight = tk.Button(master=backstaffpicker, text='Kropsvægt', bg='#525252', command=lambda: body_weight(),
                                            fg='white', width=100, height=50)
        b_weight.place(x=40, y=40, height=60, width=125)
        b_weight.config(font=('Helvetica', 15))
        '''

        backstaffbottom.rowconfigure(0, weight=1)
        backstaffbottom.grid_columnconfigure(0, weight=1)
        backstaffbottom.grid_columnconfigure(1, weight=1)
        backstaffbottom.grid_columnconfigure(2, weight=1)

        time.sleep(.2)

        backstaffpicker.bind("<KeyRelease>", check_input)

        massv.set('-- g')

        weight_button1.update()
        weight_button2.update()
        weight_button3.update()
        reset.update()
        backstafftest.update()
        #b_weight.update()

        backstaffpicker.focus_set()

    backstaffpicker.update()

def input_name():
    global backstaffpicker

    backstaff_entry_ok = tk.Button(master=backstaffpicker, text='Godkend', bg='white', fg='#575756')
    backstaff_entry_ok.grid(row=2, column=2, sticky='NSEW', padx=10, pady=10)
    backstaff_entry_ok.config(font=("Helvetica", 25))
    # backstaff_entry_ok.pack()

    backstaff_entry_ok.update()

    backstaffpicker.update()

def checkinput():
    global cprn, backstaffpicker, mode, input2

    input2.set('')

    still_looking = True

    test_on()

    time.sleep(.2)
    print('looking', flush=True)
    if platform.platform()[0:7] != 'Windows':
        while still_looking:
            time.sleep(.2)
            with open('measurelet.ID', 'r') as f:
                try:
                    cpr_s = f.readline().strip()
                    if len(cpr_s) > 0:
                        cprn = cpr_s
                        still_looking = False
                except:
                    pass
    print('not looking', flush=True)

    test_off()

    with open('measurelet.ID', 'w') as d:
        d.write(' \n')

    if len(cprn) > 10:
        if cprn[1].lower() == 'c':
            cprn = cprn[2:12]
        elif cprn[0].lower() == 'a':
            cprn = cprn[1:]

    with open('configuration.txt', 'w') as c:
        c.write('singleuse;' + str(cprn) + '; \n')
        mode = 'singleuse'

    backstaffpicker.destroy()

    backstaffpicker = tk.Frame(master=win, bg='#fafafa')
    backstaffpicker.pack(fill=tk.BOTH, expand=1)


    leftframe = tk.Frame(master=backstaffpicker, bg='#fafafa', height=1)
    leftframe.pack(fill=tk.BOTH, expand=1)

    rightframe = tk.Frame(master=backstaffpicker, bg='#fafafa', height=10)
    rightframe.pack(fill=tk.BOTH, expand=1)

    backstaffpicker.rowconfigure(0, weight=1)
    backstaffpicker.rowconfigure(1, weight=2)
    backstaffpicker.grid_columnconfigure(0, weight=1)

    input_label = tk.Label(master=leftframe, text='CPR:', bg='#fafafa', height=1, width=1)
    input_label.grid(row=0, column=0, padx=5, pady=5, sticky='NSEW')
    input_label.config(font=('Helvetica', 25))

    input_label2 = tk.Label(master=leftframe, text=cprn, bg='#fafafa', height=1, width=1)
    input_label2.grid(row=0, column=1, padx=5, pady=5, sticky='NSEW')
    input_label2.config(font=('Helvetica', 25))

    input_label3 = tk.Label(master=leftframe, text='Navn:', bg='#fafafa', height=1, width=1)
    input_label3.grid(row=1, column=0, padx=5, pady=5, sticky='NSEW')
    input_label3.config(font=('Helvetica', 25))

    vcmd = win.register(lambda P: P.replace(" ", "").replace("-", "").isalpha() or P == "")

    input = tk.Entry(
        master=leftframe,
        textvariable=input2,
        bg='white',
        width=1,
        validate="key",
        validatecommand=(vcmd, '%P')
    )
    input.grid(row=1, column=1, padx=5, pady=5, sticky='EW')
    input.config(font=('Helvetica', 25))
    input.bind("<FocusIn>", open_keyboard())

    input_button = tk.Button(master=leftframe, text='Godkend', command=lambda: new_single_user(input.get()), bg='#007f93', fg='white')
    input_button.grid(row=1, column=2, padx=5, pady=5, sticky='EW')
    input_button.config(font=('Helvetica', 25))
    # input_button.pack()

    leftframe.rowconfigure(0, weight=1)
    leftframe.rowconfigure(1, weight=1)
    leftframe.grid_columnconfigure(0, weight=1)
    leftframe.grid_columnconfigure(1, weight=1)
    leftframe.grid_columnconfigure(2, weight=1)

    input2.trace('w', makeupper2)

    input.focus_set()

    input_button.update()

    backstaffpicker.update()


def new_single_user(navn):
    global cprn, backstaffpicker, mode, name

    name = navn

    close_keyboard()

    with open('configuration.txt', 'w') as c:
        c.write('singleuse;' + str(cprn) + ';' + name + '\n')
        mode = 'singleuse'

    backstaffpicker.destroy()

    backstaffpicker = tk.Frame(master=win, bg='#fafafa')
    backstaffpicker.pack(fill=tk.BOTH, expand=1)


    backstaffpicker_label1 = tk.Label(master=backstaffpicker, text='Single-use tilstand', bg='#fafafa', fg='#575756')
    backstaffpicker_label1.grid(row=1, column=0, sticky='NSEW', padx=10, pady=10)
    backstaffpicker_label1.config(font=("Helvetica", 25))

    backstaffpicker_label2 = tk.Label(master=backstaffpicker, text='Navn : ' + name, bg='#fafafa', fg='#575756')
    backstaffpicker_label2.grid(row=2, column=0, sticky='NSEW', padx=10, pady=10)
    backstaffpicker_label2.config(font=("Helvetica", 25))

    backstaffpicker_label3 = tk.Label(master=backstaffpicker, text='CPR: ' + cprn[0:6] + '-xxxx', bg='#fafafa',
                                      fg='#575756')
    backstaffpicker_label3.grid(row=3, column=0, sticky='NSEW', padx=10, pady=10)
    backstaffpicker_label3.config(font=("Helvetica", 25))

    backstaffbottom = tk.Frame(master=backstaffpicker, bg='#fafafa')
    backstaffbottom.grid(row=4, column=0, sticky='NSEW', padx=10, pady=10)

    backstaffpicker_button1 = tk.Button(master=backstaffbottom, text='Ny bruger', command=lambda: switchtosingle(),
                                        bg='#007f93', fg='white', width=25)
    backstaffpicker_button1.grid(row=0, column=0, sticky='NSEW', padx=10, pady=10)
    backstaffpicker_button1.config(font=("Helvetica", 25))
    # backstaffpicker_button1.pack()

    backstaffpicker_button2 = tk.Button(master=backstaffbottom, text='Skift til multi-use',
                                        command=lambda: switchtomulti(), bg='#007f93', fg='white', width=25)
    backstaffpicker_button2.grid(row=0, column=1, sticky='NSEW', padx=10, pady=10)
    backstaffpicker_button2.config(font=("Helvetica", 25))
    # backstaffpicker_button2.pack()

    # backstaffpicker_button3 = tk.Button(master=backstaffpicker, text='Tilbage', command=lambda: lukvindue(),
    #                                     bg='#525252', fg='white')
    # backstaffpicker_button3.grid(row=4, column=2, sticky='NSEW', padx=10, pady=10)
    # backstaffpicker_button3.config(font=("Helvetica", 25))

    backstafftest = tk.Button(master=backstaffpicker, text='Tilbage', bg='#525252', command=lambda: lukvindue(),
                              fg='white', width=100, height=50)
    backstafftest.place(x=650, y=40, height=60, width=125)
    backstafftest.config(font=('Helvetica', 15))
    # backstafftest.pack()

    backstafftest = tk.Button(master=backstaffpicker, text='Support', bg='#525252', command=lambda: support(), fg='white', width=100, height=50)
    backstafftest.place(x=650, y=100, height=60, width=125)
    backstafftest.config(font=('Helvetica', 15))


    backstaffpicker.grid_columnconfigure(0, weight=1)
    backstaffpicker.rowconfigure(0, weight=1)
    backstaffpicker.rowconfigure(1, weight=1)
    backstaffpicker.rowconfigure(2, weight=1)
    backstaffpicker.rowconfigure(3, weight=1)
    backstaffpicker.rowconfigure(4, weight=1)

    backstaffbottom.grid_columnconfigure(0, weight=1)
    backstaffbottom.grid_columnconfigure(1, weight=1)
    backstaffbottom.rowconfigure(0, weight=1)

    backstaffpicker_label0 = tk.Label(master=backstaffpicker, text='Enhed: ', bg='#fafafa', fg='#575756', height=1,
                                      anchor='w')
    backstaffpicker_label0.place(x=20, y=40, height=20, width=125, anchor='w')
    # backstaffpicker_label0.grid(row=0, column=0, sticky='W', padx=0, pady=0)
    backstaffpicker_label0.config(font=("Helvetica", 14), anchor='w')

    backstaffpicker_label1 = tk.Label(master=backstaffpicker, text='M-06-1A00133', bg='#fafafa', fg='#575756', height=1,
                                      anchor='w')
    backstaffpicker_label1.place(x=90, y=40, height=20, width=450, anchor='w')
    # backstaffpicker_label1.grid(row=0, column=1, sticky='W', padx=0, pady=0)
    backstaffpicker_label1.config(font=("Helvetica", 14, 'bold'), anchor='w')
    '''
    backstaffpicker_label1 = tk.Label(master=backstaffpicker, text='Single-use tilstand', bg='#fafafa',
                                      fg='#575756')
    backstaffpicker_label1.grid(row=1, column=1, sticky='NSEW', padx=10, pady=10)
    backstaffpicker_label1.config(font=("Helvetica", 25))

    backstaff_entry = tk.Label(master=backstaffpicker, text='Navn: ' + name, bg='#fafafa', fg='#575756')
    backstaff_entry.grid(row=2, column=1, sticky='EW', padx=10, pady=10)
    backstaff_entry.config(font=("Helvetica", 25))

    backstaffpicker_label3 = tk.Label(master=backstaffpicker, text='CPR: ' + cprn, bg='#fafafa',
                                      fg='#575756')
    backstaffpicker_label3.grid(row=3, column=1, sticky='NSEW', padx=10, pady=10)
    backstaffpicker_label3.config(font=("Helvetica", 25))

    backstaffpicker_button1 = tk.Button(master=backstaffpicker, text='Ny bruger',
                                        command=lambda: switchtosingle(),
                                        bg='#007f93', fg='white')
    backstaffpicker_button1.grid(row=4, column=0, sticky='NSEW', padx=10, pady=10)
    backstaffpicker_button1.config(font=("Helvetica", 25))

    backstaffpicker_button2 = tk.Button(master=backstaffpicker, text='Skift til multi-use',
                                        command=lambda: switchtomulti(), bg='#007f93', fg='white')
    backstaffpicker_button2.grid(row=4, column=1, sticky='NSEW', padx=10, pady=10)
    backstaffpicker_button2.config(font=("Helvetica", 25))

    backstafftest = tk.Button(master=backstaffpicker, text='Tilbage', bg='#525252', command=lambda: lukvindue(),
                              fg='white', width=100, height=50)
    backstafftest.place(x=650, y=40, height=60, width=125)
    backstafftest.config(font=('Helvetica', 15))

    # backstaffpicker_button3 = tk.Button(master=backstaffpicker, text='Tilbage',
                                        # command=lambda: lukvindue(),
                                        # bg='#525252', fg='white')
    # backstaffpicker_button3.grid(row=4, column=2, sticky='NSEW', padx=10, pady=10)
    # backstaffpicker_button3.config(font=("Helvetica", 25))

    backstaffpicker.grid_columnconfigure(0, weight=1)
    backstaffpicker.grid_columnconfigure(1, weight=1)
    backstaffpicker.grid_columnconfigure(2, weight=1)
    backstaffpicker.rowconfigure(0, weight=1)
    backstaffpicker.rowconfigure(1, weight=1)
    backstaffpicker.rowconfigure(2, weight=1)
    backstaffpicker.rowconfigure(3, weight=1)
    backstaffpicker.rowconfigure(4, weight=1)
    '''
    backstaffpicker.focus_set()

    backstaffpicker_button1.update()
    backstaffpicker_button2.update()
    backstafftest.update()

    backstaffpicker.update()

def waiter():
    global backswitch
    backswitch.destroy()

    welcome()


def closedesktop():
    if platform.platform()[0:7] != 'Windows':
        sp.Popen(['sudo', 'shutdown', '-h', 'now'])

        #sp.Popen(['sudo', 'systemctl', '--force', 'poweroff'])
    else:
        exit()


def welcome():
    global back, mode, cprn

    with open('configuration.txt', 'r') as t:
        cn = t.readline().strip()
        mode = cn.split(';')[0]
        cprn = cn.split(';')[1]

    back = tk.Frame(master=win, bg='#fafafa')
    back.pack(fill=tk.BOTH, expand=1)
  
    with open('setup.txt', 'r') as stp:
            scale_type = stp.readline().strip()
            if scale_type not in ('output'):
                gui = tk.Button(master=back, text='LAV MÅLING', bg='#007f93', fg='white', command=lambda: rungui_s(), height=4,
                                width=25)
                gui.grid(row=1, column=1, sticky='NSEW', padx=10, pady=10)
                gui.configure(font=('Helvetica', '22'))
                # gui.pack()
            else:
                gui = tk.Button(master=back, text='LAV MÅLING', bg='#007f93', fg='white', command=lambda: rungui_s(), height=4,
                                width=25)
                gui.grid(row=1, column=1, sticky='NSEW', padx=10, pady=10)
                gui.configure(font=('Helvetica', '22'))
                # gui.pack()

    staff = tk.Button(master=back, text='PERSONALE', bg='#007f93', fg='white', command=lambda: runstaff(), height=4,
                      width=25)
    staff.grid(row=1, column=3, sticky='NSEW', padx=10, pady=10)
    staff.configure(font=('Helvetica', '22'))
    # staff.pack()


    showdata = tk.Button(master=back, text='VIS DATA', bg='#007f93', fg='white', command=lambda: runshowdata(0),
                         height=4,
                         width=25)
    showdata.grid(row=1, column=5, sticky='NSEW', padx=10, pady=10)
    showdata.configure(font=('Helvetica', '22'))
    # showdata.pack()

    close = tk.Button(master=back, text='SLUK', bg='#525252', fg='white', command=lambda: closedesktop(), height=1,
                         width=25)
    close.grid(row=2, column=5, sticky='NSEW', padx=10, pady=10)
    close.configure(font=('Helvetica', '22'))
    # close.pack()

    
    back.grid_columnconfigure(0, weight=1)
    back.grid_columnconfigure(1, weight=1)
    back.grid_columnconfigure(2, weight=1)
    back.grid_columnconfigure(3, weight=1)
    back.grid_columnconfigure(4, weight=1)
    back.grid_columnconfigure(5, weight=1)
    back.grid_columnconfigure(6, weight=1)
    back.grid_rowconfigure(0, weight=1)
    back.grid_rowconfigure(1, weight=1)
    back.grid_rowconfigure(2, weight=1)

    back.focus_set()


    gui.update()
    showdata.update()
    staff.update()
    close.update()

    time.sleep(0.01)
    back.update()

    # win.after(60000, standby, back)

    # zeroscale()

def switchtomulti():
    global backstaffpicker, backswitch, mode

    with open('configuration.txt', 'w') as cnf:
        cnf.write('multiuse;\n')
        mode = 'multiuse'

    with open('measurements.txt', 'w') as msn:
        msn.write('')

    backstaffpicker.destroy()

    backswitch = tk.Frame(master=win, bg='#fafafa')
    backswitch.pack(fill=tk.BOTH, expand=1)

    backswitch_label1 = tk.Label(master=backswitch, text='Skiftet til multi-use!', bg='#fafafa')
    backswitch_label1.grid(row=1, column=1, sticky='NSEW', padx=10, pady=10)
    backswitch_label1.config(font=("Helvetica", 45))

    backswitch.grid_columnconfigure(0, weight=1)
    backswitch.grid_columnconfigure(1, weight=1)
    backswitch.grid_columnconfigure(2, weight=1)
    backswitch.rowconfigure(0, weight=1)
    backswitch.rowconfigure(1, weight=1)
    backswitch.rowconfigure(2, weight=1)

    time.sleep(0.01)

    backswitch.update()

    win.after(2000, waiter)

    backswitch.update()


''''def choose(): # DETTE ER SIDEN HVOR MAN SKULLE VÆLGE MELLEM IV ELLER DRIKKEVARE EFTER MAN HAR TRYKKET LAV MÅLING (droppet)
    global back, backstaff, backstaffpicker

    if isinstance(back, tk.Frame):
        back.destroy()

    backstaffpicker = tk.Frame(master=win, bg='#fafafa')
    backstaffpicker.pack(fill=tk.BOTH, expand=1)

    backstaffpicker.grid_rowconfigure(0, weight=1)
    backstaffpicker.grid_rowconfigure(2, weight=1)  # Tom række under knapperne

    # Knapperne placeres i midten
    drink = tk.Button(master=backstaffpicker, text='Drikkevare', bg='#007f93', command=lambda: rungui_s(),
                      fg='white', width=15, height=5, font=('Helvetica', 25))
    drink.grid(row=1, column=0, sticky='NSEW', padx=10, pady=10)

    iv = tk.Button(master=backstaffpicker, text='IV', bg='#007f93', command=lambda: iv_measure(),
                   fg='white', width=15, height=5, font=("Helvetica", 25))
    iv.grid(row=1, column=1, sticky='NSEW', padx=10, pady=10)

    backstafftest = tk.Button(master=backstaffpicker, text='Tilbage', bg='#525252', command=lambda: lukvindue(),
                              fg='white', width=100, height=50)
    backstafftest.place(x=650, y=40, height=60, width=125)
    backstafftest.config(font=('Helvetica', 15))

    backstaffpicker.grid_columnconfigure(0, weight=1)
    backstaffpicker.grid_columnconfigure(1, weight=1)
    backstaffpicker.focus_set()

    time.sleep(0.01)
    backstaffpicker.update()'''


def iv_measurement(comment=''):
    global backstaffpicker, input1, name, cpr, mode
    back.destroy()
    print('der')
    try:
        backstaffpicker.destroy()
    except:
        print('failed')

    cpr = ''
    name = ''
    with open('configuration.txt', 'r') as cnf:
        conf = cnf.readline().strip()
        if mode == 'singleuse':
            cpr = conf.split(';')[1]
            name = conf.split(';')[2]
    
    #if scale_type == 'input':
     #   if mode == 'singleuse':
    input1.set('')
    #backstaffpicker.destroy()

    comment = comment.replace(';', '')
    
    #name = ''
    #with open('configuration.txt', 'r') as cnf:
     #   conf = cnf.readline().strip()
      #  if mode == 'singleuse':
       #     cpr = conf.split(';')[1]
        #    name = conf.split(';')[2]


    
    backstaffpicker = tk.Frame(master=win, bg='#fafafa')
    backstaffpicker.pack(fill=tk.BOTH, expand=1)

    
    backstaffpicker.grid_rowconfigure(0, weight=1) 
    backstaffpicker.grid_rowconfigure(1, weight=3)  
    backstaffpicker.grid_rowconfigure(2, weight=1) 

    backstaffpicker.grid_columnconfigure(0, weight=2)  
    backstaffpicker.grid_columnconfigure(1, weight=1)  

    # Navn og CPR labels
    backstaffpicker_label2 = tk.Label(master=backstaffpicker, text='Navn: ', bg='#fafafa', fg='#575756', font=("Helvetica", 14), anchor='w')
    backstaffpicker_label2.place(x=20, y=50, height=20, width=125, anchor='w')
    
    backstaffpicker_label4 = tk.Label(master=backstaffpicker, text=name, bg='#fafafa', fg='#575756', font=("Helvetica", 14, 'bold'), anchor='w')
    backstaffpicker_label4.place(x=120, y=50, height=20, width=450, anchor='w')

    backstaffpicker_label5 = tk.Label(master=backstaffpicker, text='CPR-nr.: ', bg='#fafafa', fg='#575756', font=("Helvetica", 14), anchor='w')
    backstaffpicker_label5.place(x=20, y=90, height=20, width=125, anchor='w')

    backstaffpicker_label6 = tk.Label(master=backstaffpicker, text=cprn[0:6] + '-xxxx', bg='#fafafa', fg='#575756', font=("Helvetica", 14, 'bold'), anchor='w')
    backstaffpicker_label6.place(x=120, y=90, height=20, width=450, anchor='w')

    # Input felt sektion 
    input_frame = tk.Frame(master=backstaffpicker, bg='#fafafa')
    input_frame.grid(row=1, column=0, pady=100, padx=20, sticky='NSEW') 

    input_label = tk.Label(master=input_frame, text="Indtast vægt på intravenøs væske i gram", bg='#fafafa', font=('Helvetica', 22))
    input_label.pack()

    input_entry = tk.Entry(master=input_frame, textvariable=input1, bg='white', font=('Helvetica', 22), width=30, justify="center")
    input_entry.pack(pady=15, ipadx=15, ipady=10)

    # Begræns indtastning til 4 tegn
    input_entry.bind("<KeyPress>", lambda event: "break" 
                 if (len(input1.get()) >= 4 and event.keysym not in ("BackSpace", "Delete", "Left", "Right")) 
                 or (not event.char.isdigit() and event.keysym not in ("BackSpace", "Delete", "Left", "Right")) 
                 else None)

    # Åbn keyboard ved fokus
    input_entry.bind("<FocusIn>", lambda event: open_keyboard())

    # Knapper i højre side
    button_frame = tk.Frame(master=backstaffpicker, bg='#fafafa')
    button_frame.grid(row=1, column=1, padx=10, pady=30, sticky='N')

    # **Brug `pack()` for at sikre, at knapperne er direkte under hinanden**
    add = tk.Button(master=button_frame, text='Tilføj', bg='#007f93', fg='white', font=('Helvetica', 22),
                    height=2, width=10, command=lambda: verify(type = "V", mass=input1.get() if input1.get() else "0", container_type = "IV"))
    add.pack(pady=5, fill="x")

    bin = tk.Button(master=button_frame, text='Kasser', bg='#b64909', fg='white', font=('Helvetica', 22),
                    height=2, width=10, command=lambda: verify(type = "K", mass=input1.get() if input1.get() else "0", container_type = "IV"))
    bin.pack(pady=5, fill="x")

    # Tilbage-knap i øverste højre hjørne
    backstafftest = tk.Button(master=backstaffpicker, text='Tilbage', bg='#525252', command=lambda: cancel(), 
                            fg='white', font=('Helvetica', 14))
    backstafftest.place(x=662, y=10, height=50, width=120)

    input1.trace('w', makeupper1)

    input_entry.focus_set()

    bin.update()
    add.update()

    backstaffpicker.update()


def body_weight(comment=''):
    global backstaffpicker, input1, name, cpr, mode
    back.destroy()
    print('der')
    try:
        backstaffpicker.destroy()
    except:
        print('failed')

    cpr = ''
    name = ''
    with open('configuration.txt', 'r') as cnf:
        conf = cnf.readline().strip()
        if mode == 'singleuse':
            cpr = conf.split(';')[1]
            name = conf.split(';')[2]
    
    #if scale_type == 'input':
     #   if mode == 'singleuse':
    input1.set('')
    #backstaffpicker.destroy()

    comment = comment.replace(';', '')
    
    #name = ''
    #with open('configuration.txt', 'r') as cnf:
     #   conf = cnf.readline().strip()
      #  if mode == 'singleuse':
       #     cpr = conf.split(';')[1]
        #    name = conf.split(';')[2]


    
    backstaffpicker = tk.Frame(master=win, bg='#fafafa')
    backstaffpicker.pack(fill=tk.BOTH, expand=1)

    
    backstaffpicker.grid_rowconfigure(0, weight=1) 
    backstaffpicker.grid_rowconfigure(1, weight=3)  
    backstaffpicker.grid_rowconfigure(2, weight=1) 

    backstaffpicker.grid_columnconfigure(0, weight=2)  
    backstaffpicker.grid_columnconfigure(1, weight=1)  

    # Navn og CPR labels
    backstaffpicker_label2 = tk.Label(master=backstaffpicker, text='Navn: ', bg='#fafafa', fg='#575756', font=("Helvetica", 14), anchor='w')
    backstaffpicker_label2.place(x=20, y=50, height=20, width=125, anchor='w')
    
    backstaffpicker_label4 = tk.Label(master=backstaffpicker, text=name, bg='#fafafa', fg='#575756', font=("Helvetica", 14, 'bold'), anchor='w')
    backstaffpicker_label4.place(x=120, y=50, height=20, width=450, anchor='w')

    backstaffpicker_label5 = tk.Label(master=backstaffpicker, text='CPR-nr.: ', bg='#fafafa', fg='#575756', font=("Helvetica", 14), anchor='w')
    backstaffpicker_label5.place(x=20, y=90, height=20, width=125, anchor='w')

    backstaffpicker_label6 = tk.Label(master=backstaffpicker, text=cprn[0:6] + '-xxxx', bg='#fafafa', fg='#575756', font=("Helvetica", 14, 'bold'), anchor='w')
    backstaffpicker_label6.place(x=120, y=90, height=20, width=450, anchor='w')

    # Input felt sektion 
    input_frame = tk.Frame(master=backstaffpicker, bg='#fafafa')
    input_frame.grid(row=1, column=0, pady=100, padx=20, sticky='NSEW') 

    input_label = tk.Label(master=input_frame, text="Indtast din kropsvægt i kg", bg='#fafafa', font=('Helvetica', 22))
    input_label.pack()

    input_entry = tk.Entry(master=input_frame, textvariable=input1, bg='white', font=('Helvetica', 22), width=30, justify="center")
    input_entry.pack(pady=15, ipadx=15, ipady=10)

    # Begræns indtastning til 4 tegn
    input_entry.bind("<KeyPress>", lambda event: "break" 
    if (len(input1.get()) >= 5 and event.keysym not in ("BackSpace", "Delete", "Left", "Right"))
    or (not (event.char.isdigit() or event.char in ",.") and event.keysym not in ("BackSpace", "Delete", "Left", "Right"))
    else None)

    # Åbn keyboard ved fokus
    input_entry.bind("<FocusIn>", lambda event: open_keyboard())


    # Knapper i højre side
    button_frame = tk.Frame(master=backstaffpicker, bg='#fafafa')
    button_frame.grid(row=1, column=1, padx=10, pady=30, sticky='N')

    # **Brug `pack()` for at sikre, at knapperne er direkte under hinanden**
    add = tk.Button(master=button_frame, text='Tilføj', bg='#007f93', fg='white', font=('Helvetica', 22),
                    height=2, width=10, command=lambda: verify(type = "B", comment="Kropsvægt = "+input1.get()+" kg" if input1.get() else "0", mass="0", container_type = "B_weight"))
    add.pack(pady=5, fill="x")

    # Tilbage-knap i øverste højre hjørne
    backstafftest = tk.Button(master=backstaffpicker, text='Tilbage', bg='#525252', command=lambda: cancel(), 
                            fg='white', font=('Helvetica', 14))
    backstafftest.place(x=662, y=10, height=50, width=120)

    input1.trace('w', makeupper1)

    input_entry.focus_set()

    add.update()

    backstaffpicker.update()

def support():
    global backstaffpicker  
    back.destroy()
    print('der')
    try:
        backstaffpicker.destroy()
    except:
        print('failed')

    backstaffpicker = tk.Frame(master=win, bg='#fafafa')
    backstaffpicker.pack(fill=tk.BOTH, expand=1)

    
    backstaffpicker.grid_rowconfigure(0, weight=1) 
    backstaffpicker.grid_rowconfigure(1, weight=3)  
    backstaffpicker.grid_rowconfigure(2, weight=1) 

    backstaffpicker.grid_columnconfigure(0, weight=2)  
    backstaffpicker.grid_columnconfigure(1, weight=1)  

    support_label = tk.Label(master=backstaffpicker, text='Support', bg='#fafafa')
    support_label.place(x=90, y=30, height=50, width=600)
    support_label.config(font=("Helvetica", 30, 'bold'))

    phoneNumber_label = tk.Label(master=backstaffpicker, text='Telefon: +45 29921111', bg='#fafafa')
    phoneNumber_label.place(x=90, y=120, height=35, width=600)
    phoneNumber_label.config(font=("Helvetica", 20))

    
    mail_label = tk.Label(master=backstaffpicker, text='Mail: support@measurelet.com', bg='#fafafa')
    mail_label.place(x=90, y=180, height=35, width=600)
    mail_label.config(font=("Helvetica", 20))

    info_label = tk.Label(master=backstaffpicker, text='Telefon åben Mandag til fredag kl. 7-17 \nEllers er du er altid velkommen til at sende en mail', bg='#fafafa')
    info_label.place(x=65, y=240, height=60, width=700)
    info_label.config(font=("Helvetica", 20))

    # Tilbage-knap i øverste højre hjørne
    backstafftest = tk.Button(master=backstaffpicker, text='Tilbage', bg='#525252', command=lambda: lukvindue(), 
                            fg='white', font=('Helvetica', 14))
    backstafftest.place(x=662, y=10, height=50, width=120)


    backstaffpicker.update()


def switchtosingle():
    global backstaffpicker, backswitch, cprn, mode

    au.sync_measurements()

    test_on()

    file_name = os.path.join("temp", "pending_measurements.json")
    if os.path.exists(file_name):
        os.remove(file_name)
        print(f"{file_name} slettet.")
    else:
        print(f"{file_name} findes ikke.")

    mode = 'singleuse'

    backstaffpicker.destroy()

    with open('measurements.txt', 'w') as msn:
        msn.write('')

    backstaffpicker = tk.Frame(master=win, bg='#fafafa')
    backstaffpicker.pack(fill=tk.BOTH, expand=1)

    backswitch_label1 = tk.Label(master=backstaffpicker, text='Single-use tilstand', bg='#fafafa')
    backswitch_label1.grid(row=0, column=1, sticky='NSEW', padx=10, pady=10)
    backswitch_label1.config(font=("Helvetica", 25))

    backswitch_label2 = tk.Label(master=backstaffpicker, text='Skan armbånd', bg='#fafafa')
    backswitch_label2.grid(row=1, column=1, sticky='NSEW', padx=10, pady=10)
    backswitch_label2.config(font=("Helvetica", 25))

    backswitch_label3 = tk.Label(master=backstaffpicker, text='←', bg='#fafafa')
    backswitch_label3.grid(row=1, column=0, sticky='W', padx=10, pady=0)
    backswitch_label3.config(font=("Helvetica", 45))

    luk_vindue_button = tk.Button(master=backstaffpicker, bg='#525252', fg='white', text='Luk vindue',
                            command=lambda: lukvindue_light(), height=1, width=1)
    luk_vindue_button.grid(row=2, column=2, sticky='NSEW', padx=10, pady=10)
    luk_vindue_button.config(font=("Helvetica", 25))
    # luk_vindue_button.pack()

    backstaffpicker.grid_columnconfigure(0, weight=1)
    backstaffpicker.grid_columnconfigure(1, weight=1)
    backstaffpicker.grid_columnconfigure(2, weight=1)
    backstaffpicker.rowconfigure(0, weight=1)
    backstaffpicker.rowconfigure(1, weight=1)
    backstaffpicker.rowconfigure(2, weight=1)

    backstaffpicker.bind("<KeyPress>", check_input)

    backstaffpicker.focus_set()

    time.sleep(0.01)

    luk_vindue_button.update()

    backstaffpicker.update()

    # win.after(100, checkinput)




def new_user():

    backstaff = tk.Frame(master=win, bg='#fafafa')
    backstaff.pack(fill=tk.BOTH, expand=1)

    name_label = tk.Label(master=backstaff, text='Indtast navn:', bg='#fafafa', fg='#575756')
    name_label.grid(row=1, column=0, sticky='NSEW', padx=10, pady=10)
    name_label.config(font=("Helvetica", 25))

    name_field = tk.Entry(master=backstaff, bg='#fafafa', fg='#575756')
    name_field.bind("<FocusIn>", open_keyboard())
    name_field.grid(row=1, column=1, sticky='NSEW', padx=10, pady=10)
    name_field.config(font=("Helvetica", 25))

    name_button = tk.Button(master=backstaff, bg='#007f93', fg='white', text='OK',
                            command=lambda: inputname(name_field.get()), height=1, width=2)
    name_button.grid(row=1, column=2, sticky='NSEW', padx=10, pady=10)
    name_button.config(font=("Helvetica", 25))
    # name_button.pack()

    backstaff.grid_columnconfigure(0, weight=1)
    backstaff.grid_columnconfigure(1, weight=1)
    backstaff.grid_columnconfigure(2, weight=1)
    backstaff.rowconfigure(0, weight=1)
    backstaff.rowconfigure(1, weight=1)
    backstaff.rowconfigure(2, weight=1)
    backstaff.rowconfigure(3, weight=1)
    backstaff.rowconfigure(4, weight=1)
    backstaff.rowconfigure(5, weight=1)
    backstaff.rowconfigure(6, weight=1)
    backstaff.rowconfigure(7, weight=1)

    if platform.platform()[0:7] != 'Windows':
        sp.Popen(['onboard'])

    time.sleep(0.01)

    name_button.update()

    backstaffpicker.update()

def lukvindue():
    test_off()
    backstaffpicker.destroy()
    welcome()

def lukvindue_light():
    test_off()
    lukvindue()

def new_gui():
    global backstaffpicker
    backstaffpicker.destroy()

    backstaffpicker = tk.Frame(master=win, bg='#fafafa')
    backstaffpicker.pack(fill=tk.BOTH, expand=1)

    weight_label = tk.Label(master=backstaffpicker, textvariable=massv, bg='#fafafa', fg='#575756')
    weight_label.grid(row=0, column=1, sticky='NSEW', padx=10, pady=10)
    weight_label.config(font=('Helvetica', 25))

    weight_button1 = tk.Button(master=backstaffpicker, text='Tilføj', command=lambda: add_measurement('t'), bg='#007f93',
                               fg='white', height=1, width=1)
    weight_button1.grid(row=1, column=0, sticky='NSEW', padx=10, pady=10)
    weight_button1.config(font=('Helvetica', 25))
    # weight_button1.pack()

    weight_button2 = tk.Button(master=backstaffpicker, text='Kassér', command=lambda: add_measurement('k'),
                               bg='#b64909', fg='white', height=1, width=1)
    weight_button2.grid(row=1, column=1, sticky='NSEW', padx=10, pady=10)
    weight_button2.config(font=('Helvetica', 25))
    # weight_button2.pack()

    backstafftest = tk.Button(master=backstaffpicker, text='Tilbage', bg='#525252', command=lambda: lukvindue(),
                              fg='white', width=100, height=50)
    backstafftest.place(x=650, y=40, height=60, width=125)
    backstafftest.config(font=('Helvetica', 15))
    # backstafftest.pack()

    reset = tk.Button(master=backstaffpicker, text='Nulstil', bg='#525252', command=lambda: zeroscale(),
                            fg='white', width=100, height=50)
    reset.place(x=650, y=100, height=60, width=125)
    reset.config(font=('Helvetica', 15))


    # weight_button3 = tk.Button(master=backstaffpicker, text='Tilbage', bg='#525252', command=lambda: lukvindue(),
                               # fg='white', height=1, width=1)
    # weight_button3.grid(row=1, column=2, sticky='NSEW', padx=10, pady=10)
    # weight_button3.config(font=('Helvetica', 25))

    backstaffpicker.grid_columnconfigure(0, weight=1)
    backstaffpicker.grid_columnconfigure(1, weight=1)
    backstaffpicker.grid_columnconfigure(2, weight=1)
    backstaffpicker.rowconfigure(0, weight=1)
    backstaffpicker.rowconfigure(1, weight=1)

    backstaffpicker.focus_set()

    time.sleep(0.01)

    weight_button1.update()
    weight_button2.update()
    reset.update()
    backstafftest.update()

    backstaffpicker.update()

def add_measurement(type):
    global backstaffpicker

    with open('configuration.txt', 'r') as t:
        con = t.readline().strip()
        cpr = con.split(';')[1]
        try:
            au.uploadmeasurement(Kern.getMass(), type)
        except:
            print('could not upload measurement')

    backstaffpicker.destroy()

    backstaffpicker = tk.Frame(master=win, bg='#fafafa')
    backstaffpicker.pack(fill=tk.BOTH, expand=1)

    weight_label = tk.Label(master=backstaffpicker, text='Måling registreret!', bg='#fafafa', fg='#575756')
    weight_label.grid(row=0, column=1, sticky='NSEW', padx=10, pady=10)
    weight_label.config(font=('Helvetica', 25))

    backstaffpicker.grid_columnconfigure(0, weight=1)
    backstaffpicker.grid_columnconfigure(1, weight=1)
    backstaffpicker.grid_columnconfigure(2, weight=1)
    backstaffpicker.rowconfigure(0, weight=1)
    backstaffpicker.rowconfigure(1, weight=1)

    time.sleep(0.01)

    backstaffpicker.update()

    win.after(5000, new_gui)


def add_cancel():
    with open('configuration.txt', 'r') as t:
        con = t.readline().strip()
        cpr = con.split(';')[1]
        try:
            au.uploadmeasurement(Kern.getMass(), 'K')
        except:
            print('could not upload measurement')


def add_multi_measurement(type):
    global backstaffpicker

    with open('configuration.txt', 'r') as t:
        con = t.readline().strip()
        cpr = con.split(';')[1]
        try:
            au.uploadmeasurement(Kern.getMass(), type)
        except:
            print('could not upload measurement')


    backstaffpicker.destroy()

    backstaffpicker = tk.Frame(master=win, bg='#fafafa')
    backstaffpicker.pack(fill=tk.BOTH, expand=1)

    weight_label = tk.Label(master=backstaffpicker, text='Måling registreret!', bg='#fafafa', fg='#575756')
    weight_label.grid(row=0, column=1, sticky='NSEW', padx=10, pady=10)
    weight_label.config(font=('Helvetica', 25))

    backstaffpicker.grid_columnconfigure(0, weight=1)
    backstaffpicker.grid_columnconfigure(1, weight=1)
    backstaffpicker.grid_columnconfigure(2, weight=1)
    backstaffpicker.rowconfigure(0, weight=1)
    backstaffpicker.rowconfigure(1, weight=1)

    time.sleep(0.01)

    backstaffpicker.update()

    win.after(5000, new_gui)


def rungui_s():
    global mode, cprn
    # zeroscale()
    if mode == 'multiuse':
        with open('configuration.txt', 'w') as c:
            c.write('multiuse;' + str(cprn) + '; \n')
        test_on()
    au.sync_measurements()
    rungui()

def iv_measure(): #Jeg prøvede bare at efterligne rungui_s for at få multiuse til at fungere (måske overflødigt)
    global mode
    # zeroscale()
    if mode == 'multiuse':
        test_on()
    iv_measurement()

use = 0
def rungui():
    global back, weight_label, massv, backstaffpicker, mode, name, cprn, my_id, use
    back.destroy()
    print('der')
    try:
        backstaffpicker.destroy()
    except:
        print('failed') 

    if use == 0:
        zeroscale()
        use = 1

    cpr = ''
    name = ''
    with open('configuration.txt', 'r') as cnf:
        conf = cnf.readline().strip()
        if mode == 'singleuse':
            cpr = conf.split(';')[1]
            name = conf.split(';')[2]
    
    if scale_type == 'input':
        if mode == 'singleuse':
            backstaffpicker = tk.Frame(master=win, bg='#fafafa')
            backstaffpicker.pack(fill=tk.BOTH, expand=1)

            weight_label = tk.Label(master=backstaffpicker, textvariable=massv, bg='#fafafa', fg='#575756')
            weight_label.grid(row=0, column=1, sticky='NSEW', padx=10, pady=10)
            weight_label.config(font=('Helvetica', 45))

            name_label = tk.Label(master=backstaffpicker, text=name, bg='#fafafa', fg='#575756')
            name_label.grid(row=1, column=1, sticky='EW', padx=2, pady=2)
            name_label.config(font=('Helvetica', 20))

            name_label2 = tk.Label(master=backstaffpicker, text=cprn[0:6] + '-xxxx', bg='#fafafa', fg='#575756')
            name_label2.grid(row=2, column=1, sticky='EW', padx=2, pady=2)
            name_label2.config(font=('Helvetica', 20))

            text_label = tk.Label(master=backstaffpicker, text='Sæt først koppen på vægten', bg='#fafafa')
            text_label.place(x=205, y=110, height=30, width=400)
            text_label.config(font=("Helvetica", 20))

            weight_button1 = tk.Button(master=backstaffpicker, text='Tilføj', command=lambda: set_container('I',
                                                    massv.get()[:-2]), bg='#007f93', fg='white', height=1, width=1)
            weight_button1.place(x=20, y=300, height=150, width=350)
            # weight_button1.grid(row=3, column=0, sticky='NSEW', padx=10, pady=10)
            weight_button1.config(font=('Helvetica', 25))
            # weight_button1.pack()

            weight_button2 = tk.Button(master=backstaffpicker, text='Kassér', command=lambda: set_container('K',
                                                    massv.get()[:-2]), bg='#b64909', fg='white', height=1, width=1)
            weight_button2.place(x=420, y=300, height=150, width=350)
            # weight_button2.grid(row=3, column=1, sticky='NSEW', padx=10, pady=10)
            weight_button2.config(font=('Helvetica', 25))
            # weight_button2.pack()

            backstafftest = tk.Button(master=backstaffpicker, text='Tilbage', bg='#525252', command=lambda: lukvindue(),
                                      fg='white', width=100, height=50)
            backstafftest.place(x=650, y=40, height=60, width=125)
            backstafftest.config(font=('Helvetica', 15))

            reset = tk.Button(master=backstaffpicker, text='Nulstil', bg='#525252', command=lambda: zeroscale(),
                                            fg='white', width=100, height=50)
            reset.place(x=650, y=100, height=60, width=125)
            reset.config(font=('Helvetica', 15))


            iv = tk.Button(master=backstaffpicker, text='IV', bg='#525252', command=lambda: iv_measurement(),
                                            fg='white', width=100, height=50)
            iv.place(x=40, y=40, height=60, width=125)
            iv.config(font=('Helvetica', 15))

            ''' ikke i brug endnu
            b_weight = tk.Button(master=backstaffpicker, text='Kropsvægt', bg='#525252', command=lambda: body_weight(),
                                            fg='white', width=100, height=50)
            b_weight.place(x=40, y=100, height=60, width=125)
            b_weight.config(font=('Helvetica', 15))
            '''
            # backstafftest.pack()

            # weight_button3 = tk.Button(master=backstaffpicker, text='Tilbage', bg='#525252',
            #                            command=lambda: lukvindue(), fg='white', height=1, width=1)
            # weight_button3.grid(row=3, column=2, sticky='NSEW', padx=10, pady=10)
            # weight_button3.config(font=('Helvetica', 25))

            backstaffpicker.grid_columnconfigure(0, weight=1)
            backstaffpicker.grid_columnconfigure(1, weight=1)
            backstaffpicker.grid_columnconfigure(2, weight=1)
            backstaffpicker.rowconfigure(0, weight=1)
            backstaffpicker.rowconfigure(1, weight=1)
            backstaffpicker.rowconfigure(2, weight=1)
            backstaffpicker.rowconfigure(3, weight=5)

            massv.set('-- g')

            time.sleep(0.01)

            weight_button1.update()
            weight_button2.update()
            reset.update()
            iv.update()
            backstafftest.update()
            #b_weight.update()
            

            backstaffpicker.update()

            # win.after(100, zeroscale)

            # thread1 = thr.Thread(target=readmass)
            # thread1.start()

        elif mode == 'multiuse':
            my_id = ''
            backstaffpicker = tk.Frame(master=win, bg='#fafafa')
            backstaffpicker.pack(fill=tk.BOTH, expand=1)

            backswitch_label1 = tk.Label(master=backstaffpicker, text='Lav måling', bg='#fafafa')
            backswitch_label1.grid(row=0, column=1, sticky='NSEW', padx=10, pady=10)
            backswitch_label1.config(font=("Helvetica", 25))

            backswitch_label2 = tk.Label(master=backstaffpicker, text='Skan patientarmbånd', bg='#fafafa')
            backswitch_label2.grid(row=1, column=1, sticky='NSEW', padx=10, pady=10)
            backswitch_label2.config(font=("Helvetica", 40))

            disclaimer_label = tk.Label(master=backstaffpicker, text='OBS: Vægten står i Multi-use tilstand \n\n Hvis vægten kun skal bruges af én patient, skift til Single-use i personalemodulet', bg='#fafafa')
            disclaimer_label.place(x=0, y=350, height=60, width=820)
            disclaimer_label.config(font=("Helvetica", 12))            

            backswitch_label3 = tk.Label(master=backstaffpicker, text='←', bg='#fafafa')
            backswitch_label3.grid(row=1, column=0, sticky='W', padx=10, pady=0)
            backswitch_label3.config(font=("Helvetica", 45))

            backswitch_label4 = tk.Label(master=backstaffpicker, text='', bg='#fafafa')
            backswitch_label4.grid(row=2, column=2, sticky='NSEW', padx=10, pady=0)
            backswitch_label4.config(font=("Helvetica", 25))

            # luk_vindue_button = tk.Button(master=backstaffpicker, bg='#525252', fg='white', text='Luk vindue',
                                          # command=lambda: lukvindue(), height=1, width=1)
            # luk_vindue_button.grid(row=2, column=2, sticky='NSEW', padx=10, pady=10)
            # luk_vindue_button.config(font=("Helvetica", 25))

            backstafftest = tk.Button(master=backstaffpicker, text='Tilbage', bg='#525252', command=lambda: lukvindue_light(),
                                      fg='white', width=100, height=50)
            backstafftest.place(x=650, y=40, height=60, width=125)
            backstafftest.config(font=('Helvetica', 15))
            # backstafftest.pack()

            backstaffpicker.grid_columnconfigure(0, weight=1)
            backstaffpicker.grid_columnconfigure(1, weight=1)
            backstaffpicker.grid_columnconfigure(2, weight=1)
            backstaffpicker.rowconfigure(0, weight=1)
            backstaffpicker.rowconfigure(1, weight=1)
            backstaffpicker.rowconfigure(2, weight=1)

            backstaffpicker.bind("<KeyPress>", check_input)

            backstaffpicker.focus_set()

            time.sleep(0.01)

            backstafftest.update()

            backstaffpicker.update()

            '''
            backstaffleft = tk.Frame(master=backstaffpicker, bg='orange', width=200, height=480)
            backstaffleft.grid(row=0, column=0)
            backstaffleft.grid_propagate(False)
    
            backstaffmid = tk.Frame(master=backstaffpicker, bg='blue', width=400, height=480)
            backstaffmid.grid(row=0, column=1)
            backstaffmid.grid_propagate(False)
    
            backstaffright = tk.Frame(master=backstaffpicker, bg='green', width=200, height=480)
            backstaffright.grid(row=0, column=2)
            backstaffright.grid_propagate(False)
    
            backstaffpicker.grid_columnconfigure(0)
            backstaffpicker.grid_columnconfigure(1)
            backstaffpicker.grid_columnconfigure(2)
            backstaffpicker.rowconfigure(0, weight=1)
    
            weight_label = tk.Label(master=backstaffmid, text='Skan armbånd', bg='#fafafa', fg='#575756')
            weight_label.grid(row=0, column=1, sticky='NSEW', padx=10, pady=10)
            weight_label.config(font=('Helvetica', 25))
    
            weight_button3 = tk.Button(master=backstaffright, text='Tilbage', bg='#525252', command=lambda: lukvindue(), fg='white', height=2, width=2)
            weight_button3.grid(row=0, column=2, sticky='NE', padx=10, pady=10)
            weight_button3.config(font=('Helvetica', 25))
    
            backstaffmid.grid_columnconfigure(0, weight=1)
            backstaffmid.rowconfigure(0, weight=1)
    
            weight_label1 = tk.Label(master=backstaffleft, text='←', bg='#fafafa', fg='#575756')
            weight_label1.grid(row=0, column=0, sticky='NW', padx=10, pady=0)
            weight_label1.config(font=('Helvetica', 25))
    
            # weight_button3 = tk.Button(master=backstaffbottom, text='Tilbage', bg='#525252', command=lambda: lukvindue(), fg='white', height=1, width=1)
            # weight_button3.grid(row=1, column=2, sticky='NSEW', padx=10, pady=10)
            # weight_button3.config(font=('Helvetica', 25))
    
            backstaffleft.grid_columnconfigure(0, weight=1)
            backstaffleft.rowconfigure(0, weight=1)
            backstaffleft.rowconfigure(1, weight=1)
            backstaffleft.rowconfigure(2, weight=1)
    
            backstafftest = tk.Button(master=backstaffpicker, text='Tilbage', bg='red', fg='white', width=100, height=50)
            backstafftest.place(x=650, y=240, height=50, width=100)
            backstafftest.config(font=('Helvetica', 15))
    
    
            backstaffpicker.bind("<KeyPress>", check_input)
    
            backstaffpicker.focus_set()
            '''

            # win.after(100, multi_scan)
    else:
        if mode == 'singleuse':
            backstaffpicker = tk.Frame(master=win, bg='#fafafa')
            backstaffpicker.pack(fill=tk.BOTH, expand=1)

            weight_label = tk.Label(master=backstaffpicker, textvariable=massv, bg='#fafafa', fg='#575756')
            weight_label.grid(row=0, column=1, sticky='NSEW', padx=10, pady=10)
            weight_label.config(font=('Helvetica', 45))

            name_label = tk.Label(master=backstaffpicker, text=name, bg='#fafafa', fg='#575756')
            name_label.grid(row=1, column=1, sticky='EW', padx=2, pady=2)
            name_label.config(font=('Helvetica', 20))

            name_label2 = tk.Label(master=backstaffpicker, text=cprn[0:6] + '-xxxx', bg='#fafafa', fg='#575756')
            name_label2.grid(row=2, column=1, sticky='EW', padx=2, pady=2)
            name_label2.config(font=('Helvetica', 20))

            text_label = tk.Label(master=backstaffpicker, text='Sæt først beholder/ble på vægten', bg='#fafafa')
            text_label.place(x=150, y=110, height=33, width=500)
            text_label.config(font=("Helvetica", 20))


            weight_button1 = tk.Button(master=backstaffpicker, text='Urin',
                                       command=lambda: set_container_output('U', massv.get()[:-2]), bg='#007f93', fg='white',
                                       height=1, width=1)
            weight_button1.place(x=20, y=300, height=150, width=240)
            # weight_button1.grid(row=3, column=0, sticky='NSEW', padx=10, pady=10)
            weight_button1.config(font=('Helvetica', 25))
            # weight_button1.pack()

            weight_button2 = tk.Button(master=backstaffpicker, text='Afføring',
                                       command=lambda: set_container_output('A', massv.get()[:-2]), bg='#b64909', fg='white',
                                       height=1, width=1)
            weight_button2.place(x=280, y=300, height=150, width=240)
            # weight_button2.grid(row=3, column=1, sticky='NSEW', padx=10, pady=10)
            weight_button2.config(font=('Helvetica', 25))
            # weight_button2.pack()

            weight_button3 = tk.Button(master=backstaffpicker, text='Andet',
                                       command=lambda: set_container_output('B', massv.get()[:-2]), bg='#00935e', fg='white',
                                       height=1, width=1)
            weight_button3.place(x=540, y=300, height=150, width=240)
            # weight_button3.grid(row=3, column=1, sticky='NSEW', padx=10, pady=10)
            weight_button3.config(font=('Helvetica', 25))
            # weight_button3.pack()

            backstafftest = tk.Button(master=backstaffpicker, text='Tilbage', bg='#525252', command=lambda: lukvindue(),
                                      fg='white', width=100, height=50)
            backstafftest.place(x=650, y=40, height=60, width=125)
            backstafftest.config(font=('Helvetica', 15))
            # backstafftest.pack()

            reset = tk.Button(master=backstaffpicker, text='Nulstil', bg='#525252', command=lambda: zeroscale(),
                                            fg='white', width=100, height=50)
            reset.place(x=650, y=100, height=60, width=125)
            reset.config(font=('Helvetica', 15))

            ''' ikke i brug endnu
            b_weight = tk.Button(master=backstaffpicker, text='Kropsvægt', bg='#525252', command=lambda: body_weight(),
                                            fg='white', width=100, height=50)
            b_weight.place(x=40, y=40, height=60, width=125)
            b_weight.config(font=('Helvetica', 15))
            '''

            # weight_button3 = tk.Button(master=backstaffpicker, text='Tilbage', bg='#525252', command=lambda: lukvindue(), fg='white', height=1, width=1)
            # weight_button3.grid(row=3, column=2, sticky='NSEW', padx=10, pady=10)
            # weight_button3.config(font=('Helvetica', 25))

            backstaffpicker.grid_columnconfigure(0, weight=1)
            backstaffpicker.grid_columnconfigure(1, weight=1)
            backstaffpicker.grid_columnconfigure(2, weight=1)
            backstaffpicker.rowconfigure(0, weight=1)
            backstaffpicker.rowconfigure(1, weight=1)
            backstaffpicker.rowconfigure(2, weight=1)
            backstaffpicker.rowconfigure(3, weight=5)

            time.sleep(0.01)

            weight_button1.update()
            weight_button2.update()
            weight_button3.update()
            reset.update()
            backstafftest.update()
            #b_weight.update()

            backstaffpicker.update()

            massv.set('-- g')

            # win.after(100, zeroscale)

            # thread1 = thr.Thread(target=readmass)
            # thread1.start()

        elif mode == 'multiuse':
            my_id = ''
            backstaffpicker = tk.Frame(master=win, bg='#fafafa')
            backstaffpicker.pack(fill=tk.BOTH, expand=1)
            backstaffpicker.pack(fill=tk.BOTH, expand=1)

            backswitch_label1 = tk.Label(master=backstaffpicker, text='Lav måling', bg='#fafafa')
            backswitch_label1.grid(row=0, column=1, sticky='NSEW', padx=10, pady=10)
            backswitch_label1.config(font=("Helvetica", 25))

            backswitch_label2 = tk.Label(master=backstaffpicker, text='Skan patientarmbånd', bg='#fafafa')
            backswitch_label2.grid(row=1, column=1, sticky='NSEW', padx=10, pady=10)
            backswitch_label2.config(font=("Helvetica", 40))

            disclaimer_label = tk.Label(master=backstaffpicker, text='OBS: Vægten står i Multi-use tilstand \n\n Hvis vægten kun skal bruges af én patient, skift til Single-use i personalemodulet', bg='#fafafa')
            disclaimer_label.place(x=0, y=350, height=60, width=820)
            disclaimer_label.config(font=("Helvetica", 12))    
            
            backswitch_label3 = tk.Label(master=backstaffpicker, text='←', bg='#fafafa')
            backswitch_label3.grid(row=1, column=0, sticky='W', padx=10, pady=0)
            backswitch_label3.config(font=("Helvetica", 45))

            backswitch_label4 = tk.Label(master=backstaffpicker, text='', bg='#fafafa')
            backswitch_label4.grid(row=2, column=2, sticky='NSEW', padx=10, pady=0)
            backswitch_label4.config(font=("Helvetica", 25))

            # luk_vindue_button = tk.Button(master=backstaffpicker, bg='#525252', fg='white', text='Luk vindue',
            # command=lambda: lukvindue(), height=1, width=1)
            # luk_vindue_button.grid(row=2, column=2, sticky='NSEW', padx=10, pady=10)
            # luk_vindue_button.config(font=("Helvetica", 25))

            backstafftest = tk.Button(master=backstaffpicker, text='Tilbage', bg='#525252', command=lambda: lukvindue_light(),
                                      fg='white', width=100, height=50)
            backstafftest.place(x=650, y=40, height=60, width=125)
            backstafftest.config(font=('Helvetica', 15))
            # backstafftest.pack()

            backstaffpicker.grid_columnconfigure(0, weight=1)
            backstaffpicker.grid_columnconfigure(1, weight=1)
            backstaffpicker.grid_columnconfigure(2, weight=1)
            backstaffpicker.rowconfigure(0, weight=1)
            backstaffpicker.rowconfigure(1, weight=1)
            backstaffpicker.rowconfigure(2, weight=1)

            backstaffpicker.bind("<KeyPress>", check_input)

            backstaffpicker.focus_set()

            time.sleep(0.01)

            backstafftest.update()

            backstaffpicker.update()

            '''
            backstaffleft = tk.Frame(master=backstaffpicker, bg='orange', width=200, height=480)
            backstaffleft.grid(row=0, column=0)
            backstaffleft.grid_propagate(False)

            backstaffmid = tk.Frame(master=backstaffpicker, bg='blue', width=400, height=480)
            backstaffmid.grid(row=0, column=1)
            backstaffmid.grid_propagate(False)

            backstaffright = tk.Frame(master=backstaffpicker, bg='green', width=200, height=480)
            backstaffright.grid(row=0, column=2)
            backstaffright.grid_propagate(False)

            backstaffpicker.grid_columnconfigure(0)
            backstaffpicker.grid_columnconfigure(1)
            backstaffpicker.grid_columnconfigure(2)
            backstaffpicker.rowconfigure(0, weight=1)

            weight_label = tk.Label(master=backstaffmid, text='Skan armbånd', bg='#fafafa', fg='#575756')
            weight_label.grid(row=0, column=1, sticky='NSEW', padx=10, pady=10)
            weight_label.config(font=('Helvetica', 25))

            weight_button3 = tk.Button(master=backstaffright, text='Tilbage', bg='#525252', command=lambda: lukvindue(), fg='white', height=2, width=2)
            weight_button3.grid(row=0, column=2, sticky='NE', padx=10, pady=10)
            weight_button3.config(font=('Helvetica', 25))

            backstaffmid.grid_columnconfigure(0, weight=1)
            backstaffmid.rowconfigure(0, weight=1)

            weight_label1 = tk.Label(master=backstaffleft, text='←', bg='#fafafa', fg='#575756')
            weight_label1.grid(row=0, column=0, sticky='NW', padx=10, pady=0)
            weight_label1.config(font=('Helvetica', 25))

            # weight_button3 = tk.Button(master=backstaffbottom, text='Tilbage', bg='#525252', command=lambda: lukvindue(), fg='white', height=1, width=1)
            # weight_button3.grid(row=1, column=2, sticky='NSEW', padx=10, pady=10)
            # weight_button3.config(font=('Helvetica', 25))

            backstaffleft.grid_columnconfigure(0, weight=1)
            backstaffleft.rowconfigure(0, weight=1)
            backstaffleft.rowconfigure(1, weight=1)
            backstaffleft.rowconfigure(2, weight=1)

            backstafftest = tk.Button(master=backstaffpicker, text='Tilbage', bg='red', fg='white', width=100, height=50)
            backstafftest.place(x=650, y=240, height=50, width=100)
            backstafftest.config(font=('Helvetica', 15))


            backstaffpicker.bind("<KeyPress>", check_input)

            backstaffpicker.focus_set()
            '''

            # win.after(100, multi_scan)

    backstaffpicker.focus_set()


def runstaff():
    global back, backstaff, backstaffpicker, massv, mode
    back.destroy()
    cpr = ''
    name = ''
    with open('configuration.txt', 'r') as cnf:
        conf = cnf.readline().strip()
        if mode == 'singleuse':
            cpr = conf.split(';')[1]
            name = conf.split(';')[2]
    if mode == 'singleuse':

        backstaffpicker = tk.Frame(master=win, bg='#fafafa')
        backstaffpicker.pack(fill=tk.BOTH, expand=1)


        backstaffpicker_label1 = tk.Label(master=backstaffpicker, text='Single-use tilstand', bg='#fafafa', fg='#575756')
        backstaffpicker_label1.grid(row=1, column=0, sticky='NSEW', padx=10, pady=10)
        backstaffpicker_label1.config(font=("Helvetica", 25))

        backstaffpicker_label2 = tk.Label(master=backstaffpicker, text='Navn : ' + name, bg='#fafafa', fg='#575756')
        backstaffpicker_label2.grid(row=2, column=0, sticky='NSEW', padx=10, pady=10)
        backstaffpicker_label2.config(font=("Helvetica", 25))

        backstaffpicker_label3 = tk.Label(master=backstaffpicker, text='CPR: ' + cpr[0:6] + '-xxxx', bg='#fafafa', fg='#575756')
        backstaffpicker_label3.grid(row=3, column=0, sticky='NSEW', padx=10, pady=10)
        backstaffpicker_label3.config(font=("Helvetica", 25))

        backstaffbottom = tk.Frame(master=backstaffpicker, bg='#fafafa')
        backstaffbottom.grid(row=4, column=0, sticky='NSEW', padx=10, pady=10)

        backstaffpicker_button1 = tk.Button(master=backstaffbottom, text='Ny bruger', command=lambda: switchtosingle(), bg='#007f93', fg='white', width=25)
        backstaffpicker_button1.grid(row=0, column=0, sticky='NSEW', padx=10, pady=10)
        backstaffpicker_button1.config(font=("Helvetica", 25))
        # backstaffpicker_button1.pack()

        backstaffpicker_button2 = tk.Button(master=backstaffbottom, text='Skift til multi-use', command=lambda: switchtomulti(), bg='#007f93', fg='white', width=25)
        backstaffpicker_button2.grid(row=0, column=1, sticky='NSEW', padx=10, pady=10)
        backstaffpicker_button2.config(font=("Helvetica", 25))
        # backstaffpicker_button2.pack()

        # backstaffpicker_button3 = tk.Button(master=backstaffpicker, text='Tilbage', command=lambda: lukvindue(), bg='#525252', fg='white')
        # backstaffpicker_button3.grid(row=4, column=2, sticky='NSEW', padx=10, pady=10)
        # backstaffpicker_button3.config(font=("Helvetica", 25))

        backstafftest = tk.Button(master=backstaffpicker, text='Tilbage', bg='#525252', command=lambda: lukvindue(), fg='white', width=100, height=50)
        backstafftest.place(x=650, y=40, height=60, width=125)
        backstafftest.config(font=('Helvetica', 15))
        # backstafftest.pack()

        backstaffpicker.grid_columnconfigure(0,weight=1)
        backstaffpicker.rowconfigure(0,weight=1)
        backstaffpicker.rowconfigure(1,weight=1)
        backstaffpicker.rowconfigure(2,weight=1)
        backstaffpicker.rowconfigure(3,weight=1)
        backstaffpicker.rowconfigure(4,weight=1)

        backstaffbottom.grid_columnconfigure(0, weight=1)
        backstaffbottom.grid_columnconfigure(1, weight=1)
        backstaffbottom.rowconfigure(0, weight=1)

        backstaffpicker_label0 = tk.Label(master=backstaffpicker, text='Enhed: ', bg='#fafafa', fg='#575756', height=1, anchor='w')
        backstaffpicker_label0.place(x=20, y=40, height=20, width=125, anchor='w')
        # backstaffpicker_label0.grid(row=0, column=0, sticky='W', padx=0, pady=0)
        backstaffpicker_label0.config(font=("Helvetica", 14), anchor='w')

        backstaffpicker_label1 = tk.Label(master=backstaffpicker, text='M-06-1A00133', bg='#fafafa', fg='#575756', height=1, anchor='w')
        backstaffpicker_label1.place(x=90, y=40, height=20, width=450, anchor='w')
        # backstaffpicker_label1.grid(row=0, column=1, sticky='W', padx=0, pady=0)
        backstaffpicker_label1.config(font=("Helvetica", 14, 'bold'), anchor='w')
        
        backstafftest = tk.Button(master=backstaffpicker, text='Sync', bg='#525252', command=lambda: au.sync_measurements(), fg='white', width=100, height=50)
        backstafftest.place(x=650, y=100, height=60, width=125)
        backstafftest.config(font=('Helvetica', 15))
        
        backstafftest = tk.Button(master=backstaffpicker, text='Support', bg='#525252', command=lambda: support(), fg='white', width=100, height=50)
        backstafftest.place(x=650, y=160, height=60, width=125)
        backstafftest.config(font=('Helvetica', 15))


        time.sleep(0.01)

        backstaffpicker_button1.update()
        backstaffpicker_button2.update()
        backstafftest.update()

    elif mode == 'multiuse':

        backstaffpicker = tk.Frame(master=win, bg='#fafafa')
        backstaffpicker.pack(fill=tk.BOTH, expand=1)

        upperpicker = tk.Frame(master=backstaffpicker, bg='#fafafa')

        backstaffpicker_label1 = tk.Label(master=backstaffpicker, text='Multi-use tilstand', bg='#fafafa', fg='#575756')
        backstaffpicker_label1.grid(row=1, column=1, sticky='NSEW', padx=10, pady=10)
        backstaffpicker_label1.config(font=("Helvetica", 25))

        backstaffpicker_button1 = tk.Button(master=backstaffpicker, text='Skift til single-use', command=lambda: switchtosingle(), bg='#007f93', fg='white')
        backstaffpicker_button1.grid(row=4, column=1, sticky='NSEW', padx=10, pady=10)
        backstaffpicker_button1.config(font=("Helvetica", 25))
        # backstaffpicker_button1.pack()

        # backstaffpicker_button2 = tk.Button(master=backstaffpicker, text='Tilbage', command=lambda: lukvindue(), bg='#525252', fg='white')
        # backstaffpicker_button2.grid(row=4, column=2, sticky='NSEW', padx=10, pady=10)
        # backstaffpicker_button2.config(font=("Helvetica", 25))

        backstafftest = tk.Button(master=backstaffpicker, text='Tilbage', bg='#525252', command=lambda: lukvindue(), fg='white', width=100, height=50)
        backstafftest.place(x=650, y=40, height=60, width=125)
        backstafftest.config(font=('Helvetica', 19))
        # backstafftest.pack()

        backstaffpicker.grid_columnconfigure(0,weight=1)
        backstaffpicker.grid_columnconfigure(1,weight=2)
        backstaffpicker.grid_columnconfigure(2,weight=1)
        backstaffpicker.rowconfigure(0,weight=1)
        backstaffpicker.rowconfigure(1,weight=1)
        backstaffpicker.rowconfigure(2,weight=1)
        backstaffpicker.rowconfigure(3,weight=1)
        backstaffpicker.rowconfigure(4,weight=1)

        backstaffpicker_label0 = tk.Label(master=backstaffpicker, text='Enhed: ', bg='#fafafa', fg='#575756', height=1, anchor='w')
        backstaffpicker_label0.place(x=20, y=40, height=20, width=125, anchor='w')
        # backstaffpicker_label0.grid(row=0, column=0, sticky='W', padx=0, pady=0)
        backstaffpicker_label0.config(font=("Helvetica", 14), anchor='w')

        backstaffpicker_label1 = tk.Label(master=backstaffpicker, text='M-06-1A00133', bg='#fafafa', fg='#575756', height=1, anchor='w')
        backstaffpicker_label1.place(x=90, y=40, height=20, width=450, anchor='w')
        # backstaffpicker_label1.grid(row=0, column=1, sticky='W', padx=0, pady=0)
        backstaffpicker_label1.config(font=("Helvetica", 14, 'bold'), anchor='w')

        backstafftest = tk.Button(master=backstaffpicker, text='Support', bg='#525252', command=lambda: support(), fg='white', width=100, height=50)
        backstafftest.place(x=650, y=100, height=60, width=125)
        backstafftest.config(font=('Helvetica', 15))

        time.sleep(0.01)

        backstafftest.update()

    backstaffpicker.bind("<KeyPress>", check_service_code)

    backstaffpicker.focus_set()

    time.sleep(0.01)

    backstaffpicker.update()

def runshowdata(picker):
    global backstaffpicker, back, mode

    with open('configuration.txt', 'r') as cnf:
        conf = cnf.readline().strip()
        if mode == 'singleuse':
            cpr = conf.split(';')[1]
            name = conf.split(';')[2]
    if mode == 'singleuse':
        test_dict = {

        }
        # test_dict = {
            # '13/3 - 2024': []
        # }
        with open('measurements.txt') as gf:
            gf_list = gf.readlines()
            gf_list.reverse()
            # print(gf_list, flush=True)
            for li in gf_list:
                li = li.strip()
                if li.split(';')[0].split(',')[0] in test_dict:
                    test_dict[li.split(';')[0].split(',')[0]].append(li.split(';'))
                else:
                    test_dict[li.split(';')[0].split(',')[0]] = [li.split(';')]

        # test_lines = [[256, 'I', '2024-02-12 05:00:00'], [128, 'F', '2024-02-12 06:00:00']]

        back.destroy()

        try:
            backstaffpicker.destroy()
        except:
            print('f')

        backstaffpicker = tk.Frame(master=win, bg='#fafafa')
        backstaffpicker.pack(fill=tk.BOTH, expand=1)
        # backstaffpicker.pack_propagate(False)

        backstaffmenu = tk.Frame(master=backstaffpicker, bg='#fafafa' ,height=1, pady=15, padx=5)
        backstaffmenu.pack(fill=tk.BOTH, expand=1)

        bottompicker = tk.Frame(master=backstaffpicker, bg='#fafafa' ,height=10, pady=15, padx=5)
        bottompicker.pack(fill=tk.BOTH, expand=1)

        backstaffpicker.grid_columnconfigure(0, weight=1)
        backstaffpicker.rowconfigure(0, weight=1)
        backstaffpicker.rowconfigure(1, weight=6)

        # backstaffpicker_y = tk.Frame(master=backstaffpicker, bg='#e4e4e4', height=40, width=500)
        # backstaffpicker_y.place(x=20, y=150, height=40, width=500)

        backstaffpicker_x = tk.Frame(master=backstaffpicker, bg='#fafafa' , height=500, width=500)
        backstaffpicker_x.place(x=0, y=190, height=500, width=500)
        # backstaffpicker_x.grid(row=0, column=0, sticky='NSEW', padx=0, pady=0)

        backstafftest = tk.Button(master=backstaffpicker, text='Tilbage', bg='#525252', command=lambda: lukvindue(), fg='white', width=100, height=50)
        backstafftest.place(x=650, y=40, height=60, width=125)
        backstafftest.config(font=('Helvetica', 15))
        # backstafftest.pack()


        bottompicker.grid_columnconfigure(0, weight=3)
        bottompicker.grid_columnconfigure(1, weight=1)
        bottompicker.rowconfigure(0, weight=1)

        device_frame = tk.Frame(master=backstaffmenu, bg='#fafafa')
        device_frame.grid(row=1, column=0, sticky='NSEW', padx=0, pady=0)

        device_frame.grid_columnconfigure(0, weight=1)
        device_frame.grid_columnconfigure(1, weight=1)
        device_frame.grid_columnconfigure(2, weight=1)
        device_frame.grid_columnconfigure(3, weight=1)
        device_frame.grid_columnconfigure(4, weight=1)
        device_frame.grid_columnconfigure(5, weight=1)
        device_frame.grid_columnconfigure(6, weight=1)
        device_frame.rowconfigure(0, weight=1)

        name_frame = tk.Frame(master=backstaffmenu, bg='#fafafa')
        name_frame.grid(row=2, column=0, sticky='NSEW', padx=0, pady=0)

        backstaffpicker_label2 = tk.Label(master=backstaffpicker, text='Navn: ', bg='#fafafa', fg='#575756', height=1, anchor='w')
        backstaffpicker_label2.place(x=20, y=50, height=20, width=125, anchor='w')
        # backstaffpicker_label2.grid(row=0, column=0, sticky='W', padx=0, pady=0)
        backstaffpicker_label2.config(font=("Helvetica", 14), anchor='w')

        backstaffpicker_label4 = tk.Label(master=backstaffpicker, text=name, bg='#fafafa', fg='#575756', height=1, anchor='w')
        backstaffpicker_label4.place(x=120, y=50, height=20, width=450, anchor='w')
        # backstaffpicker_label4.grid(row=0, column=1, sticky='W', padx=0, pady=0)
        backstaffpicker_label4.config(font=("Helvetica", 14, 'bold'), anchor='w')

        name_frame.grid_columnconfigure(0, weight=1)
        name_frame.grid_columnconfigure(1, weight=1)
        name_frame.grid_columnconfigure(2, weight=1)
        name_frame.grid_columnconfigure(3, weight=1)
        name_frame.grid_columnconfigure(4, weight=1)
        name_frame.grid_columnconfigure(5, weight=1)
        name_frame.grid_columnconfigure(6, weight=1)
        name_frame.rowconfigure(0, weight=1)

        cpr_frame = tk.Frame(master=backstaffmenu, bg='#fafafa')
        cpr_frame.grid(row=3, column=0, sticky='NSEW', padx=0, pady=0)

        backstaffpicker_label5 = tk.Label(master=backstaffpicker, text='CPR-nr.: ', bg='#fafafa', fg='#575756', height=1, anchor='w')
        backstaffpicker_label5.place(x=20, y=90, height=20, width=125, anchor='w')
        # backstaffpicker_label5.grid(row=0, column=0, sticky='W', padx=0, pady=0)
        backstaffpicker_label5.config(font=("Helvetica", 14), anchor='w')

        backstaffpicker_label6 = tk.Label(master=backstaffpicker, text=cprn[0:6] + '-xxxx', bg='#fafafa', fg='#575756', height=1, anchor='w')
        backstaffpicker_label6.place(x=120, y=90, height=20, width=450, anchor='w')
        # backstaffpicker_label6.grid(row=0, column=1, sticky='W', padx=0, pady=0)
        backstaffpicker_label6.config(font=("Helvetica", 14, 'bold'), anchor='w')


        counter = 0

        key_list = []

        label_list = []

        page_list = []

        total_dict = {}
        # print(test_dict)
        #Vigtigt at Glas, kop og kande alle har et mellemrum før ', ellers kan den ikke finde ud af det.
        for key, value in test_dict.items():
            for vals in value:
                if key in total_dict:
                    if vals[1] in ['Hvid plastikkop ', 'Papkop ', 'Tudekop ', 'IV ']:
                        total_dict[key]['kasseret'] = str(int(total_dict[key]['kasseret']) + int(vals[3][1:-2]))
                        total_dict[key]['total'] = str(int(total_dict[key]['total']) - int(vals[3][1:-2]))
                    else:
                        total_dict[key]['input'] = str(int(total_dict[key]['input']) + int(vals[3][:-2]))
                        total_dict[key]['total'] = str(int(total_dict[key]['total']) + int(vals[3][:-2]))
                else:
                    if vals[1] in ['Hvid plastikkop ', 'Papkop ', 'Tudekop ', 'IV ']:
                        total_dict[key] = {
                            'input': '0',
                            'kasseret': str(int(vals[3][1:-2])),
                            'total': str(-int(vals[3][1:-2]))
                        }
                    else:
                        total_dict[key] = {
                            'input': str(int(vals[3][:-2])),
                            'kasseret': '0',
                            'total': str(int(vals[3][:-2]))
                        }


        # print('total_dict', flush=True)
        # print(total_dict, flush=True)

        for key, value in test_dict.items():
            # print(key, flush=True)

            # print(value, flush=True)

            max_len = (len(value) % 5) + 1

            cn = 1

            while len(value) > 5:
                page_list.append({'key': key, 'value': value[0:5], 'max_len': max_len, 'cn': cn})
                value = value[5:]
                cn += 1
            page_list.append({'key': key, 'value': value, 'max_len': max_len, 'cn': cn})
            # for l in page_list:
                # print(l, flush=True)
                # print(' ', flush=True)

        print(page_list)


        # for ky, vl in page_list[picker].items():


        for val in page_list[picker]['value']:
            label_list.append(str(val[0]))
            label_list.append(str(val[1]))
            label_list.append(str(val[2]))
            label_list.append(str(val[3]))
            label_list[counter] = tk.Label(master=backstaffpicker_x, text='                 ' + str(val[0].split(',')[1]), bg='#fafafa', fg='#575756', height=2, anchor='sw')
            label_list[counter].grid(row=counter, column=0, sticky='SW', pady=5)
            label_list[counter].config(font=("Helvetica", 12), anchor='sw')
            label_list[counter+1] = tk.Label(master=backstaffpicker_x, text=str(val[1]), bg='#fafafa', fg='#575756', height=2, anchor='sw')
            label_list[counter+1].grid(row=counter, column=1, sticky='SW', pady=5)
            label_list[counter+1].config(font=("Helvetica", 12), anchor='sw')
            label_list[counter+1] = tk.Label(master=backstaffpicker_x, text=str(val[2]), bg='#fafafa', fg='#575756', height=2, anchor='sw')
            label_list[counter+1].grid(row=counter, column=2, sticky='SW', pady=5)
            label_list[counter+1].config(font=("Helvetica", 12), anchor='sw')
            label_list[counter+2] = tk.Label(master=backstaffpicker_x, text=str(val[3]), bg='#fafafa', fg='#575756', height=2, anchor='se')
            label_list[counter+2].grid(row=counter, column=3, sticky='SE', pady=5)
            label_list[counter+2].config(font=("Helvetica", 12), anchor='se')
            backstaffmenu.grid_rowconfigure(counter, weight=1)
            counter += 4
            
        '''
        for ky, vl in page_list[picker].items():
            # label_list.append(str(ky))
            # label_list[counter] = tk.Label(master=backstaffpicker_x, text=str(ky), bg='#fafafa', fg='#575756', height=1)
            # label_list[counter].grid(row=counter, column=0, sticky='W', padx=24, pady=2)
            # label_list[counter].config(font=("Helvetica", 15))
            date_label = tk.Label(master=backstaffpicker_y, text=str(ky), bg='#fafafa', fg='#575756', height=40)
            date_label.grid(row=0, column=0, sticky='W', padx=24, pady=2)
            date_label.config(font=("Helvetica", 15))
            in_label = tk.Label(master=backstaffpicker, text='Tilføjet i dag' , bg='#fafafa', fg='#575756', height=20)
            in_label.place(x=170, y=151, height=20, width=120)
            in_label.config(font=("Helvetica", 12, 'bold'))
            out_label = tk.Label(master=backstaffpicker, text='Kasseret i dag' , bg='#fafafa', fg='#575756', height=20)
            out_label.place(x=300, y=151, height=20, width=120)
            out_label.config(font=("Helvetica", 12, 'bold'))
            total_label = tk.Label(master=backstaffpicker, text='Total i dag' , bg='#fafafa', fg='#575756', height=20)
            total_label.place(x=430, y=151, height=20, width=120)
            total_label.config(font=("Helvetica", 12, 'bold'))
            in_text = tk.Label(master=backstaffpicker, text=total_dict[ky]['input'] + ' g', bg='#fafafa', fg='#575756', height=20)
            in_text.place(x=170, y=172, height=20, width=120)
            in_text.config(font=("Helvetica", 12))
            out_text = tk.Label(master=backstaffpicker, text=total_dict[ky]['kasseret'] + ' g', bg='#fafafa', fg='#575756', height=20)
            out_text.place(x=300, y=172, height=20, width=120)
            out_text.config(font=("Helvetica", 12))
            total_text = tk.Label(master=backstaffpicker, text=total_dict[ky]['total'] + ' g', bg='#fafafa', fg='#575756', height=20)
            total_text.place(x=430, y=172, height=20, width=120)
            total_text.config(font=("Helvetica", 12))
            # backstaffmenu.grid_rowconfigure(counter, weight=1)
            # counter += 1

            for val in vl:
                label_list.append(str(val[0]))
                label_list.append(str(val[1]))
                label_list.append(str(val[2]))
                label_list.append(str(val[3]))
                label_list[counter] = tk.Label(master=backstaffpicker_x, text='                 ' + str(val[0].split(',')[1]), bg='#fafafa', fg='#575756', height=2, anchor='sw')
                label_list[counter].grid(row=counter, column=0, sticky='SW', pady=5)
                label_list[counter].config(font=("Helvetica", 12), anchor='sw')
                label_list[counter+1] = tk.Label(master=backstaffpicker_x, text=str(val[1]), bg='#fafafa', fg='#575756', height=2, anchor='sw')
                label_list[counter+1].grid(row=counter, column=1, sticky='SW', pady=5)
                label_list[counter+1].config(font=("Helvetica", 12), anchor='sw')
                label_list[counter+1] = tk.Label(master=backstaffpicker_x, text=str(val[2]), bg='#fafafa', fg='#575756', height=2, anchor='sw')
                label_list[counter+1].grid(row=counter, column=2, sticky='SW', pady=5)
                label_list[counter+1].config(font=("Helvetica", 12), anchor='sw')
                label_list[counter+2] = tk.Label(master=backstaffpicker_x, text=str(val[3]), bg='#fafafa', fg='#575756', height=2, anchor='se')
                label_list[counter+2].grid(row=counter, column=3, sticky='SE', pady=5)
                label_list[counter+2].config(font=("Helvetica", 12), anchor='se')
                backstaffmenu.grid_rowconfigure(counter, weight=1)
                counter += 4
        '''
        backframe = tk.Frame(master=backstaffpicker, bg='#ececec')
        backframe.place(x=45, y=110, height=65, width=480)

        with open('setup.txt', 'r') as stp:
            scale_type = stp.readline().strip()
            if scale_type not in ('output'):
                date_label = tk.Label(master=backstaffpicker, text=str(page_list[picker]['key']), bg='#ececec', fg='#575756', height=40)
                date_label.place(x=50, y=120, height=40, width=120)
                date_label.config(font=("Helvetica", 15, 'bold'))
                in_label = tk.Label(master=backstaffpicker, text='Tilføjet' , bg='#ececec', fg='#575756', height=20)
                in_label.place(x=175, y=120, height=22, width=120)
                in_label.config(font=("Helvetica", 12, 'bold'))
                out_label = tk.Label(master=backstaffpicker, text='Kasseret' , bg='#ececec', fg='#575756', height=20)
                out_label.place(x=290, y=120, height=22, width=120)
                out_label.config(font=("Helvetica", 12, 'bold'))
                total_label = tk.Label(master=backstaffpicker, text='Total' , bg='#ececec', fg='#575756', height=20)
                total_label.place(x=425, y=120, height=22, width=80)
                total_label.config(font=("Helvetica", 14, 'bold'))
                in_text = tk.Label(master=backstaffpicker, text=total_dict[page_list[picker]['key']]['input'] + ' g', bg='#ececec', fg='#575756', height=20)
                in_text.place(x=175, y=141, height=22, width=120)
                in_text.config(font=("Helvetica", 12))
                out_text = tk.Label(master=backstaffpicker, text=total_dict[page_list[picker]['key']]['kasseret'] + ' g', bg='#ececec', fg='#575756', height=20)
                out_text.place(x=290, y=141, height=22, width=120)
                out_text.config(font=("Helvetica", 12))
                total_text = tk.Label(master=backstaffpicker, text=total_dict[page_list[picker]['key']]['total'] + ' g', bg='#ececec', fg='#575756', height=20)
                total_text.place(x=425, y=141, height=22, width=80)
                total_text.config(font=("Helvetica", 14, 'bold'))
            # backstaffmenu.grid_rowconfigure(counter, weight=1)
            # counter += 1

        with open('setup.txt', 'r') as stp:
            scale_type = stp.readline().strip()
            if scale_type not in ('input'):
                date_label = tk.Label(master=backstaffpicker, text=str(page_list[picker]['key']), bg='#ececec', fg='#575756', height=40)
                date_label.place(x=50, y=120, height=40, width=120)
                date_label.config(font=("Helvetica", 15, 'bold'))
                total_label = tk.Label(master=backstaffpicker, text='Total' , bg='#ececec', fg='#575756', height=20)
                total_label.place(x=425, y=120, height=22, width=80)
                total_label.config(font=("Helvetica", 14, 'bold'))
                total_text = tk.Label(master=backstaffpicker, text=total_dict[page_list[picker]['key']]['total'] + ' g', bg='#ececec', fg='#575756', height=20)
                total_text.place(x=425, y=141, height=22, width=80)
                total_text.config(font=("Helvetica", 14, 'bold'))

        backframe = tk.Frame(master=backstaffpicker, bg='#ececec')
        backframe.place(x=45, y=175, height=30, width=480)

        description_label = tk.Label(master=backstaffpicker, text='Tid' , bg='#ececec', fg='#575756', height=20)
        description_label.place(x=53, y=175, height=22, width=100)
        description_label.config(font=("Helvetica", 12, 'bold'))
        
        with open('setup.txt', 'r') as stp:
            scale_type = stp.readline().strip()
            if scale_type not in ('output'):
                description_label = tk.Label(master=backstaffpicker, text='Beholder' , bg='#ececec', fg='#575756', height=20)
                description_label.place(x=164, y=175, height=22, width=120)
                description_label.config(font=("Helvetica", 12, 'bold'))
            else:
                description_label = tk.Label(master=backstaffpicker, text='Type' , bg='#ececec', fg='#575756', height=20)
                description_label.place(x=164, y=175, height=22, width=120)
                description_label.config(font=("Helvetica", 12, 'bold'))

        ''' Ikke i brug endnu
        with open('setup.txt', 'r') as stp:
            scale_type = stp.readline().strip()
            if scale_type not in ('output'):
                description_label = tk.Label(master=backstaffpicker, text='Drikkevare/ \nKropsvægt' , bg='#ececec', fg='#575756', height=20)
                description_label.place(x=285, y=168, height=37, width=120)
                description_label.config(font=("Helvetica", 12, 'bold'))
            else:
                description_label = tk.Label(master=backstaffpicker, text='Kommentar/ \nKropsvægt' , bg='#ececec', fg='#575756', height=20)
                description_label.place(x=285, y=168, height=37, width=120)
                description_label.config(font=("Helvetica", 12, 'bold'))
        '''
        with open('setup.txt', 'r') as stp:
            scale_type = stp.readline().strip()
            if scale_type not in ('output'):
                #description_label = tk.Label(master=backstaffpicker, text='Drikkevare/ \nKropsvægt' , bg='#ececec', fg='#575756', height=20)
                description_label = tk.Label(master=backstaffpicker, text='Drikkevare' , bg='#ececec', fg='#575756', height=20)
                description_label.place(x=302, y=170, height=37, width=120)
                description_label.config(font=("Helvetica", 12, 'bold'))
            else:
                #description_label = tk.Label(master=backstaffpicker, text='Kommentar/ \nKropsvægt' , bg='#ececec', fg='#575756', height=20)
                description_label = tk.Label(master=backstaffpicker, text='Kommentar' , bg='#ececec', fg='#575756', height=20)
                description_label.place(x=302, y=170, height=37, width=120)
                description_label.config(font=("Helvetica", 12, 'bold'))


        description_label = tk.Label(master=backstaffpicker, text='Måling' , bg='#ececec', fg='#575756', height=20)
        description_label.place(x=425, y=175, height=22, width=100)
        description_label.config(font=("Helvetica", 12, 'bold'))

        #Vandrette linjer
        canvas = tk.Canvas(master=backstaffpicker, bg='#fafafa')
        canvas.place(x=45, y=163, height=5, width=480)
        canvas.create_line(2, 2, 485, 2, fill='black', width=3)

        canvas = tk.Canvas(master=backstaffpicker)
        canvas.place(x=45, y=205, height=5, width=480)
        canvas.create_line(2, 2, 485, 2, fill='black', width=3)

        #Lodrette linjer
        canvas = tk.Canvas(master=backstaffpicker, bg='#fafafa')
        canvas.place(x=45, y=163, height=480, width=5)
        canvas.create_line(2, 2, 485, 2, fill='black', width=1000)
    
        canvas = tk.Canvas(master=backstaffpicker, bg='#fafafa')
        canvas.place(x=153, y=163, height=480, width=5)
        canvas.create_line(2, 2, 485, 2, fill='black', width=1000)

        canvas = tk.Canvas(master=backstaffpicker, bg='#fafafa')
        canvas.place(x=290, y=163, height=480, width=5)
        canvas.create_line(2, 2, 485, 2, fill='black', width=1000)

        canvas = tk.Canvas(master=backstaffpicker, bg='#fafafa')
        canvas.place(x=425, y=163, height=480, width=5)
        canvas.create_line(2, 2, 485, 2, fill='black', width=1000)

        canvas = tk.Canvas(master=backstaffpicker, bg='#fafafa')
        canvas.place(x=520, y=163, height=480, width=5)
        canvas.create_line(2, 2, 485, 2, fill='black', width=1000)


        if picker != 0:
            backstaff_button_up = tk.Button(master=backstaffpicker, height=150, width=150, text='↑', command=lambda: runshowdata(picker-1), bg='#007f93', fg='white')
            backstaff_button_up.place(x=620, y=150, height=120, width=150)
            # backstaff_button_up.grid(row=0, column=1, sticky='NW', padx=5, pady=5)
            backstaff_button_up.config(font=("Helvetica", 25))
            # backstaff_button_up.pack()
            backstaff_button_up.update()

        if picker != len(page_list) - 1:
            backstaff_button = tk.Button(master=backstaffpicker, height=150, width=150, text='↓', command=lambda: runshowdata(picker+1), bg='#007f93', fg='white')
            backstaff_button.place(x=620, y=290, height=120, width=150)
            backstaff_button.config(font=("Helvetica", 25))
            # backstaff_button.pack()
            backstaff_button.update()

        # if page_list[picker - 1]['key'] == page_list[picker]['key']:
        backstaff_lb = tk.Label(master=backstaffpicker, height=30, width=150, text=str(picker + 1) + '/' + str(len(page_list)), bg='#fafafa', fg='black')
        backstaff_lb.place(x=620, y=430, height=30, width=150)
        backstaff_lb.config(font=("Helvetica", 15))
        '''else:
            backstaff_lb = tk.Label(master=backstaffpicker, height=30, width=150, text=page_list[picker + 1]['key'] + ' ↓', bg='#fafafa', fg='black')
            backstaff_lb.place(x=620, y=430, height=30, width=150)
            backstaff_lb.config(font=("Helvetica", 15))
        '''
        #if picker != 0:
         #   if page_list[picker - 1]['key'] != page_list[picker]['key']:
          #      canvas = tk.Canvas(master=backstaffpicker, bg='#fafafa')
           #     canvas.place(x=40, y=130, height=5, width=485)
            #    canvas.create_line(2, 2, 485, 2, fill='black', width=3)
        #else:
         #   canvas = tk.Canvas(master=backstaffpicker, bg='#fafafa')
          #  canvas.place(x=40, y=130, height=5, width=485)
           # canvas.create_line(2, 2, 485, 2, fill='black', width=3)
        #Det over er udkommenteret for at fjerne den sorte linje (jeg har lavet en ny sort linje)

        cpr_frame.grid_columnconfigure(0, weight=1)
        cpr_frame.grid_columnconfigure(1, weight=1)
        cpr_frame.grid_columnconfigure(2, weight=1)
        cpr_frame.grid_columnconfigure(3, weight=1)
        cpr_frame.grid_columnconfigure(4, weight=1)
        cpr_frame.grid_columnconfigure(5, weight=1)
        cpr_frame.grid_columnconfigure(6, weight=1)
        cpr_frame.rowconfigure(0, weight=1)

        backstaffmenu.grid_columnconfigure(0, weight=1)
        backstaffmenu.grid_columnconfigure(1, weight=1)
        backstaffmenu.grid_columnconfigure(2, weight=1)
        backstaffmenu.grid_columnconfigure(3, weight=1)
        backstaffmenu.rowconfigure(0, weight=1)
        backstaffmenu.rowconfigure(1, weight=1)
        backstaffmenu.rowconfigure(2, weight=1)
        backstaffmenu.rowconfigure(3, weight=1)

        backstaffpicker_x.grid_columnconfigure(0, weight=1)
        backstaffpicker_x.grid_columnconfigure(1, weight=2)
        backstaffpicker_x.grid_columnconfigure(2, weight=1)
        backstaffpicker_x.grid_columnconfigure(3, weight=1)

        # backstaffpicker_y.grid_columnconfigure(0, weight=1)
        # backstaffpicker_y.grid_columnconfigure(1, weight=1)
        # backstaffpicker_y.grid_columnconfigure(2, weight=1)
        # backstaffpicker_y.grid_columnconfigure(3, weight=1)
        # backstaffpicker_y.rowconfigure(0, weight=1)

        time.sleep(0.01)

        backstafftest.update()

    else:
        back.destroy()

        try:
            backstaffpicker.destroy()
        except:
            print('f')

        backstaffpicker = tk.Frame(master=win, bg='#fafafa', height=100, pady=15, padx=5)
        backstaffpicker.pack(fill=tk.BOTH, expand=1)

        backstafflabel1 = tk.Label(master=backstaffpicker, text='Skift til single-use tilstand for at se data', bg='#fafafa')
        backstafflabel1.grid(row=1, column=0, sticky='NSEW', padx=10, pady=10)
        backstafflabel1.config(font=("Helvetica", 25))

        backstaffpicker2 = tk.Frame(master=backstaffpicker, bg='#fafafa', height=100, pady=15, padx=15)
        backstaffpicker2.grid(row=2, column=0, sticky='NSEW', padx=10, pady=10)

        backstafftest = tk.Button(master=backstaffpicker, text='Tilbage', bg='#525252', command=lambda: lukvindue(), fg='white', width=100, height=50)
        backstafftest.place(x=650, y=40, height=60, width=125)
        backstafftest.config(font=('Helvetica', 15))
        # backstafftest.pack()

        # backstaffpicker_button1 = tk.Button(master=backstaffpicker2, text='Tilbage', command=lambda: lukvindue(), bg='#525252', fg='white')
        # backstaffpicker_button1.grid(row=0, column=4, sticky='NSEW', padx=5, pady=5)
        # backstaffpicker_button1.config(font=("Helvetica", 25))

        backstaffpicker.grid_columnconfigure(0, weight=1)
        backstaffpicker.rowconfigure(0, weight=1)
        backstaffpicker.rowconfigure(1, weight=1)
        backstaffpicker.rowconfigure(2, weight=1)
        backstaffpicker.rowconfigure(3, weight=1)

        backstaffpicker2.grid_columnconfigure(0, weight=1)
        backstaffpicker2.grid_columnconfigure(1, weight=1)
        backstaffpicker2.grid_columnconfigure(2, weight=1)
        backstaffpicker2.grid_columnconfigure(3, weight=1)
        backstaffpicker2.grid_columnconfigure(4, weight=1)
        backstaffpicker2.rowconfigure(0, weight=1)

    backstaffpicker.focus_set()

    time.sleep(0.01)

    backstafftest.update()

    backstaffpicker.update()

    # sp.Popen(['python', 'show_data.py'])

#zeroscale()

'''def check_wifi():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        return True
    except OSError:
        return False


def show_wifi_warning():
    messagebox.showwarning(
        "WiFi-fejl",
        "Mistet forbindelse til wifi!\n\n"
        "OBS: Husk at brug sync knappen på personalesiden når vægten har wifi igen"
    )


def monitor_wifi():
    while True:
        is_connected = check_wifi()
        print("wifi:", is_connected)

        if not is_connected:
            print("viser popup")
            win.after(0, show_wifi_warning)

        time.sleep(300)   # 5 minutter
# Initial opsætning
root = tk.Tk()
root.withdraw()  # Skjul hovedvinduet'''

'''def check_https_access(url="https://rsd.fluidbalancemonitor.com/api/public/device/events", timeout=5):
    """
    Returns True if the HTTPS endpoint is reachable, False if not.
    Uses only Python's standard library (no curl, no requests).
    """
    try:
        parsed = urlparse(url)
        conn = http.client.HTTPSConnection(parsed.hostname, parsed.port or 443, timeout=timeout)
        path = parsed.path or "/"
        if parsed.query:
            path += "?" + parsed.query
        conn.request("HEAD", path)
        response = conn.getresponse()
        conn.close()
        return 100 <= response.status < 600
    except Exception:
        return False

# Tkinter setup
root = tk.Tk()
root.withdraw()  # Skjul hovedvinduet

if check_https_access():
    messagebox.showinfo("Connection Test", "✅ Connection OK")
else:
    messagebox.showerror("Connection Test", "❌ Connection failed or blocked")'''

''' VIRKER PÅ PC MEN IKKE TIL DET BATTERI DER ER I VÆGTEN
def check_battery():
    battery = psutil.sensors_battery()
    if battery is None:
        return None  # Ingen batteri fundet (for stationære systemer)
    
    percent = battery.percent
    plugged = battery.power_plugged
    
    return percent, plugged


def monitor_battery():
    percent, plugged = check_battery()
    
    if percent is not None:
        if percent < 5 and not plugged:
            messagebox.showwarning("Batteri advarsel", "Batteriet er meget lavt! Tilslut oplader!")
        elif percent < 20 and not plugged:
            messagebox.showwarning("Batteri advarsel", "Batteriet er lavt! Tilslut oplader.")
    
    root.after(60000, monitor_battery)  # Tjek hver minut

# Initial opsætning
root = tk.Tk()
root.withdraw()  # Skjul hovedvinduet

monitor_battery()  # Start overvågning
'''

thread1 = thr.Thread(target=readmass)
thread1.start()
welcome()
#thread_wifi = thr.Thread(target=monitor_wifi, daemon=True)
#thread_wifi.start()

#check_https_access()
win.mainloop()
