#rock-paper-scissor.m
#code by @mnk17arts

import random
import time
from random import randrange

def rockPaperScissor(system,you):
  if system == you:
    return 
  elif system == 1 and you == 2: return True
  elif system == 1 and you == 3: return False
  elif system == 2 and you == 1: return False
  elif system == 2 and you == 3: return True
  elif system == 3 and you == 1: return True 
  elif system == 3 and you == 2: return False
  else : return 4
    
def comp ():
    global end
    while end != 0:
      system= randrange(1,3)
      you=int(input('''********************************************************\n
      choose(enter) 
      Rock ✊   (1) 
      Paper ✋  (2) 
      Scissor ✂ (3)
      
*******************************************************"\n '''))
      if system==1:
          p1="ROCK ✊"
      elif system==2:
          p1="PAPER ✋"
      else :
          p1="SCISSOR ✂"
      if you==1:
          p2="ROCK ✊"
      elif you==2:
          p2="PAPER ✋"
      elif you==3:
          p2="SCISSOR ✂"
      else :
          p2='invalid choice😐'
      time.sleep(0.5)
      print("*"*50+"\n")
      time.sleep(0.2)
      print(f"system chosen {p1}")
      time.sleep(0.1)
      print(f"you chosen {p2}")
      time.sleep(0.2)
      print("\n"+"*"*50+"\n")
      result=rockPaperScissor(system,you)
      time.sleep(0.5)
      if result == None :
       print("it's a tie! let's try again!\n")
       comp()
       break
      elif result == True :
       print(f"{p2} dominates {p1} !\n Congo! you won 🎉🎊\n")
      elif result == False : 
       print (f"{p1} dominates {p2} !\n system won! better luck next time😐\n")
      else :
          print("oops! you have entered invalid choice.\n let's try again \n")
          comp()
          break
      print("*"*50+"\n")
      time.sleep(0.5)
      end =(int(input("if you don't want to play again, enter 0 ")))

def twoPlayers ():
   global end
   while end !=0:
      plr1=int(input('''
************************************************
              PLAYER 1
      choose(enter) 
      Rock ✊   (1) 
      Paper ✋ (2) 
      Scissor ✂ (3)\n '''))
      plr2=int(input('''
************************************************
              PLAYER 2
      choose(enter) 
      Rock ✊    (1) 
      Paper ✋  (2) 
      Scissor ✂ (3)\n '''))
      if plr1==1:
          p1="ROCK ✊"
      elif plr1==2:
          p1="PAPER ✋"
      elif plr1==3:
          p1="SCISSOR ✂"
      else :
          p1='invalid choice😐'
      if plr2==1:
          p2="ROCK ✊"
      elif plr2==2:
          p2="PAPER ✋"
      elif plr2==3:
          p2="SCISSOR ✂"
      else :
          p2='invalid choice😐'
      time.sleep(0.5)
      print("*"*50+"\n")
      time.sleep(0.2)
      print(f"player1 chosen {p1}")
      time.sleep(0.1)
      print(f"player2 chosen {p2}\n")
      time.sleep(0.2)
      print("*"*50+"\n")
      result=rockPaperScissor(plr1,plr2)
      time.sleep(0.5)
      if result == None :
       print("it's a tie!\n choose once again!!\n")
       twoPlayers()
       break
      elif result == True :
       print(f"{p2} dominates {p1} ! \nCongo PLAYER 2 !🎊🎊 \n you won :)\n")
      elif result == False : 
       print (f" {p1} dominates {p2} ! \nCongo PLAYER 1 ! 🎊🎊\n you won :)\n")
      else :
          print("oops! an invalid choice was entered!\n let's try again\n")
          twoPlayers()
          break
      
      print("-"*50+"\n")
      time.sleep(0.5)
      end =(int(input("if you don't want to play again, enter 0 ")))
 
end= 1 
while 1:
    mode=int(input('''
******************* ROCK-PAPER-SCISSOR *****************
        Enter  1 for playing with computer!💻🤖
               2 for two players 🤼🏻
                        
********************************************************
''')) 
    if mode==1:
        comp()
        break
    elif mode ==2:
        twoPlayers ()
        break
    else :
        print("invalid choice! ")
        time.sleep (0.5)
        print(" re-enter the mode!")
        time.sleep (1)
        continue

print ("\n"+"*"*50)
time.sleep(1)
print ("----       THANKS FOR PLAYING           ----")
