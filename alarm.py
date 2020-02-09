from datetime import datetime
from threading import Timer
import pygame
pygame.mixer.init()
pygame.mixer.music.load("Sounds/Wishes.mp3")
pygame.mixer.music.play()


timeTemplate = datetime.today()
alarms = []

def p(text):
    print('PiAlarm: '+text)

x=datetime.today()
delta_t=y-x

secs=delta_t.seconds+1

def alarm():
    print('hello, world!')

t = Timer(secs, hello_world)
t.start()

while True:
    cmd = input('[PiAlarm Shell] ')
    if cmd == 'stop':
        p('Stopping..')
        t.cancel()
        exit()
    else:
        p('Invalid command')
