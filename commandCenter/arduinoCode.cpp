#include <Arduino.h>
#include <vector>

class ConnectedDevice;


class ConnectedDevice{
public:
    ConnectedDevice(){}
    void connectDevice(String info);
    int getPin(){return pin;}
    String getIP(){return ip;}
    String getState(){return state;}
    void setState(String newState){state = newState;}
private:
    String ip = "";
    int pin = 0;
    String state = "";
    String type = "";
};

std::vector<ConnectedDevice> connectedDevices;

void ConnectedDevice::connectDevice(String info){ //Format: ConnectionType.ip/pin.state
    char charPreviousCommand = '\0';
    String tempNum; //For storing pinNumber
    for(int i = 0; i < info.length(); i++){
        char value = info.charAt(i); //Get current char
        if(value >= 'A' && value <= 'Z'){
            switch(value){
                case 'M': //Motor (manually plugged in)
                charPreviousCommand = 'M';
                type = String(value);
                break;

                case 'W': //WiFi (connected via ip)
                charPreviousCommand = 'W';
                type = String(value);
                break;
            }
        }
        else{ //If not uppercase (for ip/pin or misc)
          tempNum += value; //Add current char
            switch(charPreviousCommand){
                case 'M': //If device type is motor
                if (i + 1 >= info.length() || isUpperCase(info.charAt(i+1))) {
                  int tempPin = tempNum.toInt();
                  bool exists = false;
                  for(ConnectedDevice& connectedDevice : connectedDevices){
                    if((connectedDevice.getPin() == tempPin)){
                      exists = true;
                      break;
                    }
                  }
                  if(!exists){
                    pin = tempNum.toInt(); //Get and prep pin
                    pinMode(pin, OUTPUT);
                  }
                }
                break;
                case 'W': //If wifi connected
                if (i + 1 >= info.length() || isUpperCase(info.charAt(i+1))) {
                  String tempIP = tempNum; //Get wifi
                  bool exists = false;
                  for(ConnectedDevice& connectedDevice : connectedDevices){
                    if((connectedDevice.getIP() == tempIP)){
                      exists = true;
                      break;
                    }
                  }
                  if(!exists){
                    ip = tempIP; //Get and prep ip
                  }
                  tempNum="";
                }
            }
        }
    }
    state = "OFF"; //Don't run yet
}

void runDevice(String info){
  char charPreviousCommand = '\0';
  char commandState = '\0';
  String tempNum; //For storing pinNumber
  for(int i = 0; i < info.length(); i++){
      char value = info.charAt(i); //Get current char
      if(value >= 'A' && value <= 'Z'){
        switch(value){
          case 'M': //Motor (manually plugged in)
          charPreviousCommand = 'M';
          break;
          
          case 'W': //WiFi (connected via ip)
          charPreviousCommand = 'W';
          break;

          case 'O': //turn device on
          //i want these NOT added to tempNum
          break;

          case 'F': //turn device off
          break;
        }
      }
      else{
        tempNum += value;
        commandState = value; //this should end up with either 'O' or 'F'
      }
    }
    switch(charPreviousCommand){
      case 'M':
        for(ConnectedDevice& connectedDevice : connectedDevices){
          int num = tempNum.toInt();
          if(connectedDevice.getPin() == num){
            String tempState = connectedDevice.getState();
            if(connectedDevice.getState() == "OFF" && commandState == 'O'){
              connectedDevice.setState("ON");
              digitalWrite(connectedDevice.getPin(), HIGH);
            }
            else if(connectedDevice.getState() == "ON" && commandState == 'F'){
              connectedDevice.setState("OFF");
              digitalWrite(connectedDevice.getPin(), LOW);
            }
          }
        }
      break;
      case 'W':
        for(ConnectedDevice& connectedDevice : connectedDevices){
          if(connectedDevice.getIP() == tempNum){
            //Run whatever you want
          }
        }
      }
  tempNum = "";
}

void interpretCommand(String info){
  char value = info.charAt(0);
  if (value == 'P'){
    ConnectedDevice newDevice;
    newDevice.connectDevice(info);
    connectedDevices.push_back(newDevice);
  }
  else if (value == 'R'){
    runDevice(info);
  }
}

void setup(){
  Serial.begin(115200);
  interpretCommand("PW123.234.10.5");
  interpretCommand("PW123.234.10.5");
  interpretCommand("PW123.234.10.6");
  interpretCommand("PM25");
  for(ConnectedDevice& connectedDevice : connectedDevices){
    Serial.println("Connected Device IPs:");
    Serial.println(connectedDevice.getIP());
    Serial.println(connectedDevice.getPin());
  }
}
void loop(){
  interpretCommand("RM25O");
  delay(2000);
  interpretCommand("RM25O");
  delay(2000);
  interpretCommand("RM25F");
  delay(2000);
  interpretCommand("RM25F");
  delay(2000);
}