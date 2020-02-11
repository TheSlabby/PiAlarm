import sched,time,sys,datetime,json,os.path
from os import path
from multiprocessing import Process, Queue, Manager, Value
import pygame

shellPrefix = '[PiAlarm Shell] '
timeFormat = '%I:%M%p'
manager = Manager()
alarms = manager.list()
alarmObjects = []
scheduler = sched.scheduler(time.time, time.sleep)
alarmsFile = 'alarms.json'

class Alarm:
    currentID = 0
    def __init__(self, name, time, sound,ID=None):
        self.goal = datetime.datetime.strptime(time, timeFormat) #test code
        if not path.exists('Sounds/'+sound):
            raise
        Alarm.currentID += 1
        self.ID = Alarm.currentID
        if ID: #code mostly unneccesary
            self.ID = ID
            if ID > currentID:
                currentID = ID
        self.sound = sound
        self.time = time
        self.name = name
        self.process = Process(target=self.runTimer)
        self.process.start()
        
        #add to lists if successful
        alarms.append(Alarm.currentID)
        alarmObjects.append(self)
        
        
    def decode(self):
        struct = {}
        struct['time'] = self.time
        struct['name'] = self.name
        struct['ID'] = self.ID
        struct['sound'] = self.sound
        return struct
        
    def runTimer(self):
        while self.ID in alarms:
            #get delta time
            now = datetime.datetime.now()
            seconds = (datetime.timedelta(hours=24) - (now - self.goal)).total_seconds() % (24 * 3600)
            scheduler.enter(seconds, 1, self.alarm)
            scheduler.run()
    
    def alarm(self):
        if self.ID in alarms:
            pygame.mixer.init()
            pygame.mixer.music.load('Sounds/'+self.sound)
            pygame.mixer.music.play()
        else:
            p('Alarm no longer exists!')


def p(text):
    print('PiAlarm: '+text)
def i(text):
    return input(text+' > ')

def tryCreateAlarm(name,time,sound,ID=None):
    try:
        alarm = Alarm(name,time,sound,ID)
        p('Added '+alarm.name+' to queue with ID: '+str(alarm.ID) + '!')
    except:
        p('Invalid alarm!')


def clearAlarms():
    p('Clearing alarms...')
    alarms[:] = []
    alarmObjects.clear()

def save():
    f = open(alarmsFile, 'w')
    arr = []
    for a in alarmObjects:
        struct = a.decode()
        arr.append(struct)
    data = json.dumps(arr)
    p('Saving data to file: '+data)
    f.write(data)

def load():
    clearAlarms()
    f = open(alarmsFile, 'r')
    data = json.loads(f.read())
    for alarm in data:
        tryCreateAlarm(alarm['name'],alarm['time'],alarm['sound'])
    p('Finished loading!')

while True:
    cmd = input(shellPrefix)
    if cmd == 'stop' or cmd == 'exit':
        if i('Save?') == 'y':
            save()
        p('Stopping..')
        sys.exit()
    elif cmd == 'new':
        time = i('Time of alarm (format: '+timeFormat+'?')
        while True:
            name = i('Name of alarm?')
            duplicate = False
            for alarm in alarmObjects:
                if name == alarm.name: duplicate = True
            if not duplicate: break
            p('Name already taken!')
        sound = i('Sound of alarm?')
        tryCreateAlarm(name,time,sound)
    elif cmd == 'delete' or cmd == 'remove':
        name = i('Name of alarm to delete?')
        removed = False
        for alarm in alarmObjects:
            if alarm.name == name:
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
    elif cmd == 'save':
        save()
    elif cmd == 'load':
        load()
    elif cmd == 'clear':
        clearAlarms()
    else:
        p('Invalid command')
