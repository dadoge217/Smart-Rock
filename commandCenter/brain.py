from RealtimeSTT import AudioToTextRecorder
from time import sleep
from playsound3 import playsound
import random

wake_word = "smart rock"
#moods
#0 - happy
#5 - irritated
#10 - angry
#15 - superAngry

# flag words
# play, turn on/off, make, tell
flag_words = [
    "on",
    "off",
    "play",
    "stop",
    "make",
    "tell"
]

# topic words
# jokes, lights, coffee, timer, weather, fun fact
topic_words = [
    "light",
    "coffee",
    "timer",
    "weather",
    "joke",
    "evanescence",
    "radiohead",
    "my chemical romance",
    "cranberries"
]

def execute_command(action, topic):
    match action:
        case "on ":
            if topic == "light":
                # execute light_on
                print("light on")
            else:
                print(action, "no corresponding topic:", topic)

        case "off ":
            if topic == "light":
                print("light off")
            elif topic == "coffee":   
                print("turning off coffee")
            elif topic == "song":  
                print("stopping music")
            else:
                print(action, "no corresponding topic:", topic)

        case "play ":
            if topic == "evanescence":
                sound = playsound(r"C:\Users\ninea\OneDrive\Documents\GitHub\Smart-Rock\sounds\songs\Wake_Grug_Up_In_Cave.wav")
            elif topic == "radiohead":
                sound = playsound(r"C:\Users\ninea\OneDrive\Documents\GitHub\Smart-Rock\sounds\songs\Grug.wav")
            elif topic == "my chemical romance":
                sound = playsound(r"C:\Users\ninea\OneDrive\Documents\GitHub\Smart-Rock\sounds\songs\Cavechildren.wav")
            elif topic == "cranberries":
                sound = playsound(r"C:\Users\ninea\OneDrive\Documents\GitHub\Smart-Rock\sounds\songs\Mammoth.wav")
            else:
                print(action, "no corresponding topic:", topic)

        case "stop ":
            if topic == "coffee":
                print("stopping coffee pot")
            elif topic == "song":
                sound.stop()
            elif topic == "timer":
                print("stopping timer")
            else:
                print(action, "no corresponding topic:", topic)

        case "make ":
            if topic == "coffee":
                print("starting coffee pot")
            elif topic == "timer":
                print("starting timer")
            elif topic == "joke":
                print("telling joke")
            else:
                print(action, "no corresponding topic:", topic)

        case "tell ":
            if topic == "joke":
                print("telling joke")
            elif topic == "weather":
                print("telling weather")
            else:
                print(action, "no corresponding topic:", topic)
            
        case _:
            print("No action")

def be_angry():
    print("BEING ANGRY")

def parse_command(command):
    split_char = " "
    tokens = command.split(split_char)

    for flag in flag_words:
        if flag in command:
            flag = flag+" "
            for topic in topic_words:
                if topic in command:
                    execute_command(flag, topic)

class SmartRockBrain:
    def __init__(self, recorder, port=None):
        self.port = port
        self.state = "IDLE"
        self.counter = 0 #counter to increase limit
        self.limit = 0 #likelihood of angry event
        self.recorder = recorder

    def idle_mode(self):
        text = self.recorder.text().lower()
        print("idle")
        self.counter += 1
        print("counter:")
        print(self.counter)
        print("limit:")
        print(self.limit)
        if self.counter == 5:
            if self.limit != 15:
                self.limit += 5
            self.counter = 0
        check = random.randint(1, 40)
        print("check:")
        print(check)
        if check < self.limit:
            be_angry()
            self.counter = 0
            self.limit = 0


        if wake_word in text:
            print("Wake word detected!")
            self.counter = 0
            self.limit = 0

            # 'command' is the command after hearing "smart rock"
            parts = text.split(wake_word, 1)
            command = parts[1].strip() if len(parts) > 1 else ""

            if command:
                print("Command:", command)
                parse_command(command)
            else:
                self.state = "ACTIVE"

    def active_mode(self):
        print("Listening for command...")
        final_text = ""

        for _ in range(30):
            text = self.recorder.text().lower()
            if text:
                final_text = text
            sleep(0.1)

        print("Command:", final_text.strip())
        self.state = "IDLE"

    def run(self):
        if self.state == "IDLE":
            self.idle_mode()
        else:
            self.active_mode()


if __name__ == '__main__':
    recorder = AudioToTextRecorder()
    smartRock = SmartRockBrain(recorder)

    while True:
        smartRock.run()
        sleep(0.1)