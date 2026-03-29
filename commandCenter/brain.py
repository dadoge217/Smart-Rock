from RealtimeSTT import AudioToTextRecorder
from time import sleep

wake_word = "smart rock"

class SmartRockBrain:
    def __init__(self, recorder, port=None):
        self.port = port
        self.state = "IDLE"
        self.recorder = recorder

    def idle_mode(self):
        text = self.recorder.text().lower()
        print("idle")

        if wake_word in text:
            print("Wake word detected!")

            parts = text.split(wake_word, 1)
            command = parts[1].strip() if len(parts) > 1 else ""

            if command:
                print("Command:", command)
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