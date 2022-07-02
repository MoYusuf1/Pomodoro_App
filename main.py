from tkinter import *
import math

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
sesh = 1
timer = NONE
checkmark = NONE
# ---------------------------- TIMER RESET ------------------------------- #

# ---------------------------- TIMER MECHANISM ------------------------------- #

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #

# ---------------------------- UI SETUP ------------------------------- #

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20


# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    global sesh
    global reps
    global checkmark
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text=f"00:00")
    sesh = 1
    reps = 0
    checks.config(text="")
    title_label.config(text="Pomodoro!", fg=GREEN)


# ---------------------------- TIMER MECHANISM ------------------------------- #
# triggered by the start button. It starts the countdown
def start_timer():
    # amount of breaks and sessions combined
    global reps
    # amount of sessions
    global sesh

    # converts minutes into seconds for each respective time interval
    work_secs = WORK_MIN * 60
    short_break_secs = SHORT_BREAK_MIN * 60
    long_break_secs = LONG_BREAK_MIN * 60

    # adds onto the reps accumulator so the program can keep track of the pomodoro pattern
    reps += 1

    # I put the label hear in order for it to update the session number accordingly
    Label(text=f"Session {sesh}", font=(FONT_NAME, 15, "bold"), highlightthickness=0, bg=YELLOW,
          foreground=GREEN).grid(row=4, column=2)

    # if the amount of reps are divisible by 2 but not equal to 0 then the clock will cycle back and forth between
    # study session and short break time
    if reps % 2 == 0 and reps != 0:
        # this edits the header to signal to the user that it's break time
        title_label.config(text="Short Break", fg=RED)
        count_down(short_break_secs)
        # adds one to the session accumulator. I put it here so the order makes sense. I also put it on the one below
        sesh += 1
    # same deal here but after the eighth rep it will turn into a long break instead of a short one
    elif reps % 8 == 0:
        title_label.config(text="Long Break", fg=PINK)
        count_down(long_break_secs)
        sesh += 1
    # here is where the study session lies. It's defaults to it if the conditions above are not met according the the
    # rep number.
    else:
        title_label.config(text="Study Time", fg=GREEN)
        count_down(work_secs)
        print(sesh)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
# this function subtracts the number written in the canvas after 1000 milliseconds (1 second) with a given input
# if the number digresses past 0 the counting mechanism ends
def count_down(count):
    global timer
    # displays the amount of minutes left by dividing the amount of seconds by 60
    count_min = math.floor(count / 60)
    # displays the amount of seconds by 60 just like a digital clock would
    count_sec = count % 60
    # there was a bug that messed with the format. It erased the 0 when the seconds were in the single digits.
    # this fixes that
    if count_sec == 0 or count_sec <= 9:
        count_sec = f"0{count_sec}"

    if count_min < 10:
        count_min = f"0{count_min}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")

    if count > 0:
        timer = window.after(1000, count_down, count - 1)
    else:
        global checkmark
        checkmark_list = []
        for rep in range(1, sesh):
            checkmark_list.append("✓")
        checkmark = "".join(checkmark_list)
        print(checkmark)
        start_timer()
        checks.config(text=checkmark)


def timer_restart():
    window.after_cancel()
    global reps
    reps = 0
    canvas.itemconfig(timer_text, text="00:00")


# ---------------------------- UI SETUP ------------------------------- #

# initializes the window
window = Tk()

# names the window "Pomodoro"
window.title("Pomodoro App")

# configures the edges of the window by extending it an x amount
# changes the window into the stores hex color code
window.config(padx=100, pady=50, bg=YELLOW)

# initializes a canvas to play around with, makes it the hex color yellow and deletes the highlighted border around it
canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)

# stores a photo of a tomato inside a variable
tomato = PhotoImage(file="tomato.png")

# creates an image with that variable and sets the coordinates to the middle of the window
tomato_img = canvas.create_image(100, 112, image=tomato)

# creates and writes text in a digital clock format
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))

# puts the tomato in the center of the grid layout I made
canvas.grid(column=2, row=2)

# This is what the function start_timer() above edits. It shows the user if it's studying time
title_label = Label(text="Pomodoro!", font=(FONT_NAME, 50, "bold"), highlightthickness=0, bg=YELLOW, foreground=GREEN)
title_label.grid(row=1, column=2)

# This button says start, and it triggers the start_timer() function if clicked
Button(text="Start", command=start_timer, bg=YELLOW, highlightthickness=0).grid(row=3, column=1)

# This button says restart, and it triggers the timer_restart() function if clicked
Button(text="Restart", command=reset_timer, bg=YELLOW, highlightthickness=0).grid(row=3, column=3)

Label(text="Pomodoro!", font=(FONT_NAME, 50, "bold"), highlightthickness=0, bg=YELLOW, foreground=GREEN)
title_label.grid(row=1, column=2)

checks = Label(text="", font=(FONT_NAME, 20, "bold"), highlightthickness=0, bg=YELLOW, foreground=RED)
checks.grid(row=5, column=2)
# keeps the window open which replaces out earlier method of making a program in a while loop
window.mainloop()
