
# The Candy Monster program

from msilib.schema import TextStyle
from tkinter import *
import random

# create window
window = Tk()
window.title('The Candy Monster Game')

# create a canvas to put objects on the screen
canvas = Canvas(window, width=500, height=400, bg = 'black')
canvas.pack()

# set up welcome screen with title and directions

title = canvas.create_text(250, 200, text = 'The Candy Monster game', fill = 'white', font = ('Helvetica', 30))
directions = canvas.create_text(250, 300, text="Collect Candy but avoid the red ones", fill = "white", font = ('Helvetica', 20))

# set up score diplay using label widget
score = 0 
score_display = Label(window, text = "Score :" + str(score))
score_display.pack()

# setup level display using label widget
level = 1
level_display = Label(window, text = "Level :" + str(level))
level_display.pack()

# create an image object using a gif file
player_image = PhotoImage(file='greenChar.gif')

# use image object to createa character at position 200, 360
mychar = canvas.create_image(250, 360, image = player_image)




#variables and lists needed for managing candies

candy_list = [] # list containing the candy
bad_candy_list = [] # list that holds bad candy
candy_speed = 2 #initial speed of falling candy
candy_color_list = ['red', 'yellow', 'blue', 'green', 'purple', 'pink', 'white']

#function that places candy at random places
def make_candy():
    #random x position
    xposition = random.randint(1, 400)
    #get ranodm color
    candy_color = random.choice(candy_color_list)
    #create candy of size 30 at random x position
    candy = canvas.create_oval(xposition, 0, xposition+30, 30, fill = candy_color)
    #add candy to candy_list
    candy_list.append(candy)
    #if color of candy is red - add it to bad_candy_list
    if candy_color == 'red':
        bad_candy_list.append(candy)
    #schedule another candy
    window.after(1000, make_candy)


#function that moves candy downwards, and schedule call to move_candy
def move_candy():
    #loops through liost of candy and change y position
    for candy in candy_list:
        canvas.move(candy, 0 , candy_speed)
        #check if candy is at end of screen - restart at random position
        if canvas.coords(candy)[1] > 400:
            xposition = random.randint(1, 400)
            canvas.coords(candy, xposition, 0, xposition + 30, 30)
    #schedule this function to move candy again
    window.after(50, move_candy)



#function updates score, level end candy_speed
def update_score_level():
    #use global since variables are changed
    global score, level, candy_speed
    score = score + 1
    score_display.config(text="Score :" + str(score))
    if score > 5  and score <= 10:
        candy_speed += 2
        level = 3
        level_display.config(text = "Level : " + str(level))
    if score > 10 and score <= 15:
        candy_speed += 1
        level = 4
        level_display.config(text = "Level : " + str(level))
    if score > 15 and score <= 20:
        candy_speed += 1
        level = 5
        level_display.config(text = "Level : " + str(level))
    if score > 20 and score <= 25:
        candy_speed += 1
        level = 6
        level_display.config(text = "Level : " + str(level))
    if score > 30 and score <= 35:
        candy_speed += 1
        level = 7
        level_display.config(text = "Level : " + str(level))
    if score > 35 and score <= 40:
        candy_speed += 1
        level = 8
        level_display.config(text = "Level : " + str(level))
    if score > 40 and score <= 45:
        candy_speed += 1
        level = 9
        level_display.config(text = "Level : " + str(level))
    
# function called to the end game - destroys window
def end_game_over():
    window.destroy()

# this destroys the instructions on the screen
def end_title():
    canvas.delete(title) # remove title
    canvas.delete(directions) # remove directions




# COLLISION MODULE

# check distance between 2 objects - return true if they "touch"
def collision(item1, item2, distance):
    xdistance = abs(canvas.coords(item1)[0] - abs(canvas.coords(item2)[0]))
    ydistance = abs(canvas.coords(item1)[1] - abs(canvas.coords(item2)[1]))
    overlap = xdistance < distance and ydistance < distance
    return overlap

# checks if char hits bad candy, schedule game over
# if char hits good candy, remove from screen, list, update score
def check_hits(): #check if hit bad candy
    for candy in bad_candy_list:
        if collision(mychar, candy, 35):
            game_over = canvas.create_text(200,200, text= 'GAME OVER', fill = 'red', font = ('Helvetica', 30))
            # end game but after user can see score
            window.after(2000, end_game_over)
            # do not check any other candy, window to be destroyed
            return
    #check if hit good candy
    for candy in candy_list:
        if collision(mychar, candy, 35):
            canvas.delete(candy) # removes candy from board
            #delete candy from list
            candy_list.remove(candy)
            update_score_level()
    #check hits again
    window.after(100, check_hits)



move_direction = 0 #track  which direction player is moving
#Function handles when user first presses arrow keys
def check_input(event):
    global move_direction
    key = event.keysym
    if key == "Right":
        move_direction = "Right"
    elif key == "Left":
        move_direction = "Left"

#Function handles when use stops pressing arrow keys
def end_input(event):
    global move_direction
    move_direction = "None"

#Function checks if not onedge and updates x coordinates based on right/left
def move_character():
    if move_direction == "Right" and canvas.coords(mychar)[0] < 500:
        canvas.move(mychar, 10, 0)
    if move_direction == "Left" and canvas.coords(mychar)[0] > 0:
        canvas.move(mychar, -10, 0)
    window.after(16, move_character)


# binds the keys to the character
canvas.bind_all('<KeyPress>', check_input) # bind key press
canvas.bind_all('<KeyRelease>', end_input) # bind all keys to circle


#Start game / Loop schedule all funcitons

window.after(1000, end_title) #destroy title and instruction
window.after(1000, make_candy) #start making candy 
window.after(1000, move_candy) #start moving candy
window.after(1000, check_hits) #check if character hit a candy
window.after(1000, move_character) # handle keyboard controls

window.mainloop() # last line is the GUI main event

