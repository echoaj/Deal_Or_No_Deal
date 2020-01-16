# Authors: Alexander Joslin, Noah Simon
# Description: GUI version of Deal or No Deal
# Date: Jan 16th 2020

from Noah import dodlib
from tkinter import*
from functools import partial       # allows you to send parameters to a function
from pygame import*

DEAL = False
CASES_LEFT = [18,13,9,6,4,2,1,0]
cases = 24
dod = dodlib.DealNoDeal()


######################################## GUI FUNCTIONS ########################################


def switch_yes():
    player_case_before_switch = dod.switch_case()
    player_case_after_switch = dod.playersCase
    directions.config(text="CONGRADULATIONS!!!!!\nYOU WIN $%d\n Your Case Was\nWorth $%d" % (player_case_after_switch, player_case_before_switch), font=("arial", 62, "bold"))
    deal_button.destroy()
    no_deal_button.destroy()
    right_frame.destroy()
    left_frame.destroy()


def deal(offer):
    directions.config(text="CONGRADULATIONS!!!!!\nYOU WIN %s\n Your Case Was\nWorth $%s" %(offer, str(dod.playersCase)),font=("arial", 62, "bold"))
    deal_button.destroy()
    no_deal_button.destroy()
    right_frame.destroy()
    left_frame.destroy()


def no_deal():
    # Directions
    if cases == 18:
        directions.config(text="SELECT 5 CASES")
    elif cases == 13:
        directions.config(text="SELECT 4 CASES")
    elif cases == 9:
        directions.config(text="SELECT 3 CASES")
    elif cases == 6:
        directions.config(text="SELECT 2 CASES")
    elif cases == 4:
        directions.config(text="SELECT 2 CASES")
    elif cases == 2:
        directions.config(text="SELECT 1 CASES")
    elif cases == 1:
        directions.config(text="SELECT 1 CASES")


    deal_button.config(state=DISABLED)
    no_deal_button.config(state=DISABLED)

    activate_cases(True)

    if cases == 0:
        last_case = list(dod.cases.keys())[0]
        directions.config(text="SWITCH WITH \n%s?"%(last_case.capitalize()))
        deal_button.config(text="NO", image="", state=ACTIVE)
        no_deal_button.config(text="YES", image="", state=ACTIVE, command=switch_yes)
        for button in list_buttons:                                                 #Added this to fix index out of range error
            if button.cget("text") == last_case:
                button.config(highlightbackground="black", state=DISABLED)


def activate_cases(state):
    button_grey_out = list(dod.cases)
    for case in button_grey_out:
        for button in list_buttons:
            if button.cget("text") == case:
                if state == True:
                    button.config(state=ACTIVE)
                elif state == False:
                    button.config(state=DISABLED)


def removing_cases(pos):
    global cases

    cases -= 1
    if cases in CASES_LEFT:
        # Bank's Offer
        offer = dod.bankOffer()                             #returns integer
        offer = "${:,d}".format(offer)                      # BANK OFFER as a string with commas
        directions.config(text="BANKER'S OFFER\n"+offer)

        # Deal or no deal
        # dod.deal_or_no_deal()                               # DEAL OR NO DEAL
        deal_button.config(state=ACTIVE, command=partial(deal, offer))
        no_deal_button.config(state=ACTIVE, command=no_deal)

        #GREY OUT BUTTONS
        activate_cases(False)


    case_remove = list_buttons[pos].cget('text')            # ANOTHER WAY TO DO IT: list_buttons[0]['text']
    value = "$" + str(dod.cases[case_remove])               # Get value of the case we remove
    list_buttons[pos].config(text=value, state=DISABLED)    # Grey out cases


    for c,lbl in enumerate(list_labels):                    # Loop through the lables to delete
        if lbl.cget("text") == value:                       # the values we got
            lbl.config(text='')                                   # delete value from the board
            del list_labels[c]                              # remove label from the list

    dod.remove_cases(case_remove)                           # REMOVE CASES



# RETRIEVE CASE NUMBER CHOSEN
def show_player_case(my_case, pos):
    global case_choosen_label


    # show player's case in the middle of frame
    #case_choosen_label.config(text=my_case, font=("arial", 16), fg="black", bg="gold", relief="solid")
    case_choosen_label.destroy()
    case_choosen_label = Button(left_frame, image=images[my_case], highlightbackground='#DAA520', state=DISABLED, padx=5, pady=5)
    case_choosen_label.grid(row=8, column=2, padx=10, pady=0)
    # disable button clicked
    list_buttons[pos-1].config(state=DISABLED)
    # change original button's functions
    for b in range(26):
        list_buttons[b].config(command=partial(removing_cases, b))
    # call function to store my case
    dod.players_choosen_case(my_case)                       # PLAYER SELECTS PERSONAL CASE!
    directions.config(text="SELECT 6 CASES")

######################################## END GUI FUNCTIONS ########################################




# create gui
window = Tk()
window.geometry("800x580+235+85")
window.title("deal or no deal")


######################################## LEFT FRAME (CASES) ########################################
# frame for showing cases left
left_frame = LabelFrame(window, pady=10, bg="#4FA7E2", relief=SUNKEN)
left_frame.grid(row=1, column=0, padx=10, pady=10)

# list to keep track of buttons made for the cases numbers
list_buttons = []

images = {} #dictionary that will contain the case images
row = 0
col = 0

# create cases on the left-hand side of frame
for i in range(1, 27):
    case_image = PhotoImage(file="Case_Images/case_"+str(i)+".png").subsample(5,5)
    case_number = "case %d" % i
    images.update({case_number: case_image})

    b = Button(left_frame, text=case_number, image=case_image, command=partial(show_player_case, case_number, i), state=ACTIVE, padx=5, pady=5)
    b.grid(row=row, column=col, padx=10, pady=3)
    list_buttons.append(b)
    col += 1
    if col % 3 == 0:
        row += 1
        col = 0


# label for where your case will go
case_choosen_label = Label(left_frame, text="YOUR\nCASE", font=("arial", 18, "normal"), fg="gold", bg="black")
case_choosen_label.grid(row=8, column=2, padx=10, pady=0)


######################################## END LEFT FRAME (CASES) ########################################




######################################## MIDDLE FRAME #################################################

middle_frame = LabelFrame(window, pady=10, relief=SUNKEN)
middle_frame.grid(row=1, column=1, padx=10, pady=0)

# user selects first case
directions = Label(middle_frame, text="SELECT YOUR CASE", font=("arial", 20, "bold"), fg="#1f1200", bg="#ffd700", borderwidth=1, relief="solid", padx=5)
directions.grid(row=1, column=1, padx=20, pady=10)

deal_image = PhotoImage(file="Button&Label_Images/deal.png").subsample(4,4)
deal_button = Button(middle_frame, text="DEAL", image=deal_image, padx=10, pady=10, highlightbackground="green", state=DISABLED)
deal_button.grid(row=2, column=1, padx=10, pady=10)

no_deal_image = PhotoImage(file="Button&Label_Images/no_deal.png").subsample(4,4)
no_deal_button = Button(middle_frame, text="NO DEAL", image=no_deal_image, padx=10, pady=10, highlightbackground="red", state=DISABLED)
no_deal_button.grid(row=3, column=1, padx=10, pady=10)


######################################## END MIDDLE FRAME ############################################




######################################## RIGHT FRAME (VALUES) ########################################
list_labels = []

right_frame = LabelFrame(window, pady=10, relief=SUNKEN)
right_frame.grid(row=1, column=3, padx=10, pady=0)

for i in range(0,13):
    lable_val = Label(right_frame, text='$' +str(dod.values2[i]), font=("arial", 16, "normal"))
    lable_val.grid(row=i, column=0,padx=25,pady=1)
    list_labels.append(lable_val)

for r,i in enumerate(range(13,26)):
    lable_val = Label(right_frame, text='$' +str(dod.values2[i]), font=("arial", 16, "normal"))
    lable_val.grid(row=r, column=1,padx=20,pady=1)
    list_labels.append(lable_val)

######################################## END RIGHT FRAME (VALUES) ########################################


######################################## START BACKGROUND MUSIC ########################################
mixer.init()
mixer.music.load("Sound/Deal cue.mp3")
mixer.music.set_volume(0.5)
mixer.music.play()
######################################## END BACKGROUND MUSIC ########################################


window.mainloop()