from motion import motionMain
#main interface to star up the program

print("-Press O to start up the program-")
print("-Press X to terminate and exit the program")
print("-Press Z to exit the program")

while True:
    inp = input("-: ")
    if inp == 'O' or inp == 'o':
        motionMain()
        break
    elif inp =='z' or inp =='Z':
        print("Goodbye!")
        break
    else:
        print("incorrect input")
    
