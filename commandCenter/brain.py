from RealtimeSTT import AudioToTextRecorder
from time import sleep
from smartplug import SmartPlug
from playsound3 import playsound
import random

wake_word = "smart rock"

flag_words = ["on ", "off ", "play ", "stop ", "make ", "tell ", "cup "]

topic_words = [
    "light",
    "coffee",
    "timer",
    "weather",
    "joke",
    "joe",
    "evanescence",
    "radiohead",
    "my chemical romance",
    "cranberries"
]


def execute_command(action, topic, brain):
    match action:
        case "on ":
            if topic == "light":
                print("Turning light ON")
                brain.light_plug.turn_on()
            elif topic == "coffee":
                print("Turning coffee ON")
                brain.coffee_plug.turn_on()

        case "off ":
            if topic == "light":
                print("Turning light OFF")
                brain.light_plug.turn_off()
            elif topic == "coffee":
                print("Turning coffee OFF")
                brain.coffee_plug.turn_off()
        
        case "cup ":
            if topic == "joe":
                print("Starting coffee pot")
                brain.coffee_plug.toggle()

        case "toggle ":
            if topic == "light":
                print("Toggling light")
                brain.light_plug.toggle()

        case "play ":
            if topic == "evanescence":
                playsound(r"assets/songs/Wake_Grug_Up_In_Cave.wav")
            elif topic == "radiohead":
                playsound(r"assets/songs/Grug.wav")
            elif topic == "my chemical romance":
                playsound(r"assets/songs/Cavechildren.wav")
            elif topic == "cranberries":
                playsound(r"assets/songs/Mammoth.wav")

        case "off ":
            if topic == "song":
                print("Stopping music")

        case "make ":
            if topic == "coffee":
                print("Starting coffee pot")
                brain.coffee_plug.toggle()

        case "tell ":
            if topic == "joke":
                print("Telling joke")

        case _:
            print("No action found")


def be_angry():
    print("BEING ANGRY")


def parse_command(command, brain):
    for flag in flag_words:
        if flag in command:
            flag = flag
            for topic in topic_words:
                if topic in command:
                    execute_command(flag, topic, brain)


class SmartRockBrain:
    def __init__(self, recorder, smart_plug1, smart_plug2):
        self.recorder = recorder
        self.light_plug = smart_plug1
        self.coffee_plug = smart_plug2

        self.state = "IDLE"
        self.counter = 0
        self.limit = 0

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
                xlimit = self.limit
            self.counter = 0
        check = random.randint(1, 40)
        print("check:")
        print(check)
        if check < self.limit:
            be_angry()
            self.counter = 0
            self.limit = 0
            xlimit = self.limit


        if wake_word in text:
            print("Wake word detected!")
            self.counter = 0
            self.limit = 0
            xlimit = self.limit

            # 'command' is the command after hearing "smart rock"
            parts = text.split(wake_word, 1)
            command = parts[1].strip() if len(parts) > 1 else ""

            if command:
                print("Command:", command)
                parse_command(command, self)
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
        parse_command(final_text, self)
        self.state = "IDLE"

    def run(self):
        if self.state == "IDLE":
            self.idle_mode()
        else:
            self.active_mode()


if __name__ == "__main__":
    recorder = AudioToTextRecorder()

    # 🔌 Smart plug connection
    light_plug = SmartPlug("192.168.137.92")
    coffee_plug = SmartPlug("192.168.137.186")

    brain = SmartRockBrain(recorder, light_plug, coffee_plug)

    while True:
        brain.run()
        sleep(0.1)