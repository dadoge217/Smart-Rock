#include <Arduino.h>

class ConnectedDevice{
public:
    void connectDevice(String info);
    void runDevice();
private:
    String ip;
    int pin;
    String state;
    String type;
};

void ConnectedDevice::connectDevice(String info){ //Format: ConnectionType.ip/pin.state
    for(int i = 0; i < info.length(); i++){
        String tempNum; //For storing pinNumber
        char value = info.charAt(i); //Get current char
        char charPreviousCommand;
        if(value >= 'A' && value <= 'Z'){
            switch(value){
                case 'M': //Motor (manually plugged in)
                charPreviousCommand = 'M';
                type = value;
                break;
                case 'W': //WiFi (connected via ip)
                charPreviousCommand = 'W';
                type = value;
                break;
            }
        }
        else{
            switch(charPreviousCommand){
                tempNum += value;
                case 'M':
                if(info.charAt(i+1) >= 'A' && info.charAt(i+1) <= 'Z'){
                    pin = tempNum.toInt();
                    pinMode(pin, OUTPUT);
                }
                break;
                case 'Z':
                if(info.charAt(i+1) >= 'A' && info.charAt(i+1) <= 'Z'){
                    ip = tempNum;
                }
            }
        }
    }
    state = "OFF";
}