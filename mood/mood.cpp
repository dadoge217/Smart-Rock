#include <iostream>
#include <cstdlib>
#include <ctime>

//abstract state
class abstractMood{
public:
    void throwCommand();
private:
    //number based on anger for how likely the command will happen
    int limit;
};

void abstractMood::throwCommand(){
    //this is literally FNAF AI logic
    std::srand(static_cast<unsigned int>(std::time(nullptr)));

    // Generate a random number between 0 and the max number
    int check = (std::rand() % 20) + 1;
    if(check <= limit){
        //do something
    }
}

//concrete states
class happy : public abstractMood{
public:
    happy(): limit(1) {}
private:
    int limit;
};

class irritated : public abstractMood{
public:
    irritated(): limit(5) {}
private:
    int limit;
};

class angry : public abstractMood{
public:
    angry(): limit(10) {}
private:
    int limit;
};

class superAngry : public abstractMood{
public:
    superAngry(): limit(15) {}
private:
    int limit;
};