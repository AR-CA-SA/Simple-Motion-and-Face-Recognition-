from motion import motionMain


print("-Press O to start up the program-")
print("-Press X to kill the program-")

inp = input("-: ")
togg = True



while(togg == True):
    if inp == 'O' or inp == 'o':
        motionMain()
    else:
        print("incorrect input")
        inp = input('-:')
print("Goodbye!")