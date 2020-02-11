import sched,time,sys,datetime
from multiprocessing import Process, Queue, Manager, Value
import pygame
pygame.mixer.init()

shellPrefix = '[PiAlarm Shell] '
timeFormat = '%I:%M%p'
manager = Manager()
alarms = manager.list()
alarmObjects = []
scheduler = sched.scheduler(time.time, time.sleep)

class Alarm:
    currentID = 0
    def __init__(self, name, time, sound):
        self.goal = datetime.datetime.strptime(time, timeFormat) #test code
        Alarm.currentID += 1
        self.ID = Alarm.currentID
        self.sound = sound
        self.time = time
        self.name = name
        self.process = Process(target=self.runTimer)
        self.process.start()
        
    def runTimer(self):
        while self.ID in alarms:
            #get delta time
            now = datetime.datetime.now()
            seconds = (datetime.timedelta(hours=24) - (now - self.goal)).total_seconds() % (24 * 3600)
            scheduler.enter(seconds, 1, self.alarm)
            scheduler.run()
    
    def alarm(self):
        if self.ID in alarms:
            pygame.mixer.music.load('Sounds/'+self.sound)
            pygame.mixer.music.play()
            print('alarm!')
        else:
            p('Alarm no longer exists!')


def p(text):
    print('PiAlarm: '+text)
def i(text):
    return input(text+' > ')

while True:
    cmd = input(shellPrefix)
    if cmd == 'stop' or cmd == 'exit':
        p('Stopping..')
        exit()
    elif cmd == 'new':
        time = i('Time of alarm (format: '+timeFormat+'?')
        name = i('Name of alarm?')
        sound = i('Sound of alarm?')
        try:
            alarm = Alarm(name,time,sound)
            alarms.append(Alarm.currentID)
            alarmObjects.append(alarm)
            p('Added '+alarm.name+' to queue with ID: '+str(alarm.ID) + '!')
        except:
            p('Invalid alarm!')
    elif cmd == 'delete':
        name = i('Name of alarm to delete?')
        removed = False
        for alarm in alarmObjects:
            if alarm.ID in alarms:
                alarms.remove(alarm.ID)
                alarmObjects.remove(alarm)
                removed = True
        if removed:
            p('Removed alarm')
        else:
            p("Couldn't find alarm!")
    elif cmd == 'list':
        p('Listing '+str(len(alarmObjects))+' alarms:')
        for alarm in alarmObjects:
            print('Name: ' + alarm.name + '\tTime: '+alarm.time+'\tID:'+str(alarm.ID))
    else:
        p('Invalid command')
