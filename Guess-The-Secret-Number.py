#guessNumber 
#code by @mnk17arts

import random
randomNumber =random.randint(1,100)
#print(randomNumber)
guesses=0
yourGuess=None
if __name__ =='__main__':
 while yourGuess != randomNumber:
   yourGuess =(input("Enter your guess : "))
   guesses+=1
   try :
     yourGuess =int(yourGuess)
     if yourGuess == randomNumber:
       print("\n Congo🎉🎊!! you guessed right :)\n")
     else:
       if yourGuess < randomNumber:
        print("\n you guessed wrong😐! guess some larger number!\n")
       else: print("\n you guessed wrong😐! guess some smaller number\n")
   except Exception as e:
     print(f'\n the input was an error :\n{e}')
      
 print(f"\n you guessed the number in {guesses} guesses\n ")  

 with open ('topScores.txt','r') as f:
   score =f.read()

 if guesses <int(score):
   print("\n 🎊congrats🎊! you made a new high score🏆!\n")
   with open('topScores.txt','w') as f:
     f.write(str(guesses))
