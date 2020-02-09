import schedule,time
from multiprocessing import Process, Queue
import pygame
pygame.mixer.init()


def job():
    print("I'm working...")


class Alarm:
    def __init__(self, name, time, sound):
        # MOVE THIS TO self.setup - self.job = schedule.every().day.at(time).do(self.alarm)
	#SETUP WILL BE CALLED FROM THE OTHER THREAD
        pygame.mixer.music.load('Sounds/' + sound)
        self.sound = sound
        self.time = time
        self.name = name
    def alarm(self):
        pygame.mixer.music.load('Sounds/'+self.sound)
        pygame.mixer.music.play()
        print('alarm!')

alarms = []
q = Queue()

def p(text):
    print('PiAlarm: '+text)
def i(text):
    return input(text+' > ')

def clockLoop():
    while True:
        schedule.run_pending()
        time.sleep(1)
        print(repr(schedule.default_scheduler.jobs))

clockProcess = Process(target=clockLoop)
clockProcess.start()

while True:
    cmd = input('[PiAlarm Shell] ')
    if cmd == 'stop':
        p('Stopping..')
        exit()
    elif cmd == 'new':
        t = i('Time of alarm?')
        n = i('Name of alarm?')
        s = i('Sound of alarm?')
        try:
            alarm = Alarm(n,t,s)
            alarms.append(alarm)
        except:
            p('Invalid alarm!')
    elif cmd == 'run all':
        schedule.default_scheduler.run_all()
    else:
        p('Invalid command')
