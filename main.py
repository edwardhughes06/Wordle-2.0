from string import ascii_letters
import random as r
import time as t
from colorama import Fore,  Style
from pick import pick
streak = 0
from datetime import datetime
from replit import db
username = ""
password = ""
db["pass"] = "Matt"
signin = False
title = 'Welcome to Word Game \n Select an option'
options = ["Play Game","Sign in"]


option, index = pick(options, title, indicator='=>', default_index=0)

if option == "Sign in":
  signin = True
  username = str(input("Enter Username: "))
  password = str(input("Enter Password: "))

  if db[password] == username:
    print("Success")
  
  keys = db.keys()
  print(keys)


play_again = True
while play_again == True:
  
  perfectletter = []
  somewhereinword = []
  notinword = []
  letter_status = {}
  
  randomise = r.randint(0,5757)

  with open('sgb-words.txt',"r") as w:
    word = w.readlines(randomise-5)

  new_word = [y.replace("\n", "") for y in word[-1]]
  new_word.pop(5)
  #word =''.join(new_word)
  word = "irate"

  #print(word)

  def clearscreen():
    print("\033[H\033[J")

  guessessofar = []

  letterposition=[]
  clearscreen()

  def guessesprint(grid, position):
    
    for i in range(0, len(grid)): 
      print("Guess", str(i+1)+": ", end="")
      

      for x in range(0, 5):
    
        if position[x+(i*5)] == "perfect":
          print(Fore.GREEN + grid[i][x], Style.RESET_ALL, end="")
          perfectletter.append(grid[i][x])
          
        
        if position[x+(i*5)] == "somewhere":     
          print(Fore.YELLOW + grid[i][x], Style.RESET_ALL, end="")
          somewhereinword.append(grid[i][x])
        
        if position[x+(i*5)] == "nowhere":     
          print(Fore.RED + grid[i][x], Style.RESET_ALL, end="")
          notinword.append(grid[i][x])
      # print("\nGuess", str(i+2)+": ", end="")
      
      print("\n")
  
  def keyboard_selection():
    keyboard_order = "qwertyuiopasdfghjklzxcvbnm"
    
    global perfectletter, somewhereinword, notinword
    for i in range(0,len(keyboard_order)):
      if keyboard_order[i] in "az":
        print("\n")
      
      if keyboard_order[i] in perfectletter:
        print(Fore.GREEN + keyboard_order[i] , Style.RESET_ALL, end="")

      elif keyboard_order[i] in somewhereinword:
        print(Fore.YELLOW + keyboard_order[i] , Style.RESET_ALL, end="")

      elif keyboard_order[i] in notinword:
        print(Fore.RED + keyboard_order[i] , Style.RESET_ALL, end="")
      
      else:
        print(Fore.WHITE + keyboard_order[i] , Style.RESET_ALL, end="")
    
    print("\n")

  win = False
  loop = True
  tries=0


  def toolbar():
    print(Fore.GREEN + "Word Game by Matt Gillett and Ed Hughes", end=" ~ ")
    if signin == True:
      print("Username: ",db[username])
    
    print("Streak:",streak ,end=" ~ ")
    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    print("Time:", current_time,"\n",Style.RESET_ALL)
    
  icode =0
  debug = []
  while loop == True:
    
    tries+=1
    
    if tries <=6:

      Style.RESET_ALL
      user_input = ""
      i = 0

      valid = False
      
      while valid == False:
        numbers = False
        clearscreen()

        if signin == True:
          toolbar()

        keyboard_selection()
        guessesprint(guessessofar, letterposition)
        
        
        print(word)
        
        nth = ["nth","first","second","third","fourth","fifth","last"]
        user_input = str(input("\nEnter your "+ nth[tries] + " guess:  ")).lower()
        if len(user_input) < 1:
          valid = False
        
        wordfound = False

        
        file = open("sgb-words.txt")
        for line in file:
          if user_input in line:
            valid = True
            wordfound = True      
        if wordfound == False:
          valid = False
  

        if len(user_input) == 5:
          valid = True
        
        for i in range(0,len(user_input)):
          if user_input[i] not in ascii_letters:
            numbers = True

        if numbers == True:  
          print("Only letters are allowed!")
        if wordfound == False:
          valid = False
        
        if valid == False:
          print("You did not enter a valid option. [Wait 2 seconds]")
          t.sleep(2)
          clearscreen()
        if len(user_input) < 1:
          valid = False
        
      guessessofar.append(user_input)

      
      if user_input == word:
        print("You win.")

        loop = False
        win = True
        check = True
      else:
        check = True
        for i in range(0,5):
          while check == True:
            if user_input[i] == word[i]:
              
              letterposition.append("perfect")
              perfectletter.append(user_input[i])
              break
              
            if user_input[i] in word and user_input[i] != word[i]: 
              
              letterposition.append("somewhere")
              somewhereinword.append(user_input[i])
              break
              
            if user_input[i] not in word:
                
              letterposition.append("nowhere")
              notinword.append(user_input[i])
              break
              

      clearscreen()

    else:

      loop = False
   
  if win == False: 
    streak = 0
    print("You Lose! The word was: ", word)
    t.sleep(1)
  if win == True:
    streak +=1
    print("Success, it took you", tries, "tries!")
    t.sleep(1)
    
  title = 'Would you like to play another game? '
  options = ["Yes","No"]

  option, index = pick(options, (title), indicator='=>', default_index=1)

  if option == "Yes":
    loop = True
    clearscreen()
  elif option == "No":
    loop = False
    play_again = False
    