from RealtimeSTT import AudioToTextRecorder

wake_word="Smart Rock"

class SmartRockBrain:
    def __init__(self, port = None):
        self.port = port
        self.state = "IDLE"
    def idle_mode(self):
        #idle
    def active_mode(self):
        #stuff
    def run(self):
        if(self.state == "IDLE"):
            self.idle_mode()
        elif(self.state == "ACTIVE"):
            self.active_mode()


if __name__ == '__main__':
    smartRock = SmartRockBrain()
    recorder = AudioToTextRecorder()
    while True:
        smartRock.run()