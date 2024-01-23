import tkinter as tk
import tkinter.messagebox
from pathlib import Path

root = tk.Tk()
root.geometry("800x500")
root.resizable(False, False)
root.title("Dots and Boxes")

file_name = Path("./background.ppm")
backimg = tk.PhotoImage(file=file_name)
backframe = tk.Label(root, image=backimg)
backframe.place(relwidth=1, relheight=1)
frame = tk.Frame(root, highlightthickness=1, highlightbackground="black")
frame.place(relwidth=0.32, relx=0.34, rely=0.1)

player_flag = True
nxtturn = True
p1_score = 0
p2_score = 0
last_move = ""


class HoverButton(tk.Button):
    def __init__(self, master, **kw):
        tk.Button.__init__(self, master=master, **kw)
        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        global player_flag
        if self['state'] == 'normal' or self['state'] == 'active':
            if player_flag:
                self['background'] = '#268bff'
            else:
                self['background'] = '#ff542e'
        else:
            pass

    def on_leave(self, e):
        if self['state'] == 'normal' or self['state'] == 'active':
            self['background'] = "white"
        elif self['state'] == 'disabled':
            self['background'] = "black"


def check_boxes():
    global player_flag, p1_score, p2_score, nxtturn
    count = 0
    n = 0
    while n < 31:
        if count == 4:
            count = 0
            n += 5
        if edge[n]["bg"] == "black" and edge[n + 4]["bg"] == "black" and edge[n + 5]["bg"] == "black" and edge[n + 9][
            "bg"] == "black":
            if player_flag and box[str(n)]['bg'] != '#ff542e' and box[str(n)]['bg'] != '#268bff':
                box[str(n)]["bg"] = "#268bff"
                p1_score += 1
                nxtturn = False

            elif box[str(n)]['bg'] != '#ff542e' and box[str(n)]['bg'] != '#268bff' and not player_flag:
                box[str(n)]["bg"] = "#ff542e"
                p2_score += 1
                nxtturn = False
        n += 1
        count += 1


def check_win():
    global p1_score, p2_score
    if p1_score + p2_score == 16:
        f = f"  Blue:   {p1_score}\n  Red:   {p2_score}\n\n"
        lastmove["state"] = "disabled"
        if p1_score > p2_score:
            tkinter.messagebox.showinfo("Dots and Boxes", f + "  Blue wins!")
        elif p2_score > p1_score:
            tkinter.messagebox.showinfo("Dots and Boxes", f + "  Red wins!")
        elif p1_score == p2_score:
            tkinter.messagebox.showinfo("Dots and Boxes", f + "  Match tied!")


def btnClick(index):
    global player_flag, nxtturn, last_move, p1_score, p2_score
    if edge[index]["state"] == "normal":
        edge[index]["state"] = "disabled"
        edge[index]["background"] = "black"
        check_boxes()
        last_move = index
        if player_flag and nxtturn:
            player_flag = False
        elif not player_flag and nxtturn:
            player_flag = True
        nxtturn = True
        blue_sc['text'] = str(p1_score)
        red_sc['text'] = str(p2_score)
        check_win()
    else:
        pass


def reset():
    global player_flag, p1_score, p2_score, nxtturn, last_move
    player_flag = True
    nxtturn = True
    last_move = ""
    p1_score = 0
    p2_score = 0
    m = 0
    l = 0
    count = 0
    lastmove["state"] = "normal"
    blue_sc['text'] = str(p1_score)
    red_sc['text'] = str(p2_score)
    while m < 40:
        edge[m]["background"] = "white"
        edge[m]["state"] = "normal"
        m += 1
    while l < 31:
        if count == 4:
            count = 0
            l += 5
        box[str(l)]['background'] = "SystemButtonFace"
        l += 1
        count += 1
    tkinter.messagebox.showwarning("Dots and Boxes", "Game Reset!")


def lastmove():
    global last_move
    if last_move == "":
        tkinter.messagebox.showerror("Dots and Boxes", "No moves registered yet!")
    else:
        def blink():
            edge[last_move]["background"] = "black"

        edge[last_move]["background"] = "#b300ff"
        edge[last_move].after(250, blink)


for r in range(5):
    for c in range(5):
        temp_C = tk.Canvas(frame, width="7", height="7", bg="black")
        temp_C.grid(row=r, column=c, padx="20", pady="20")

introhead = tk.Label(root, font="Broadway 20", text="Dots and Boxes", relief="ridge")
introhead.place(relx=0.01, rely=0.08, relwidth=0.32)

intro = tk.Label(root, font="Arial 11", relief="ridge",
                 text="Rules: Players take turns joining two\nhorizontally or vertically adjacent\n dots by a line. A "
                      "player that\n completes the fourth side of\n a square (a box) colors that box\n and must play "
                      "again. When all boxes\n have been colored, the game ends\n and the player who has "
                      "colored\nmore boxes wins.",
                 anchor="w")
intro.place(relx=0.01, rely=0.18, relwidth=0.32, relheight=0.4)

reset = tk.Button(root, text="Reset", command=reset, height=2, width=20)
reset.place(relx=0.25, rely=0.7)

lastmove = tk.Button(root, text="Last Move", command=lastmove, height=2, width=20)
lastmove.place(relx=0.75, rely=0.7, anchor="ne")

scoreboard = tk.Frame(root, background="SystemButtonFace", highlightthickness=2, highlightbackground="black")
scoreboard.place(relx=1, rely=0.35, anchor="e", relwidth=0.2, relheight=0.4)

blue_label = tk.Label(scoreboard, text="Blue: ", font="Forte 20")
blue_label.place(relx=0.2, rely=0.2)
blue_sc = tk.Label(scoreboard, text=str(p1_score), font="Forte 20", fg="blue")
blue_sc.place(relx=0.7, rely=0.2)

red_label = tk.Label(scoreboard, text="Red: ", font="Forte 20")
red_label.place(relx=0.2, rely=0.6)
red_sc = tk.Label(scoreboard, text=str(p2_score), font="Forte 20", fg="red")
red_sc.place(relx=0.6, rely=0.6)

footer = tk.Label(root, text="Made by: Pranay Sinha     Version 0.2      ", font="Times 7", anchor="e", relief="ridge")
footer.place(relx=0, rely=0.97, relwidth=1, relheight=0.03)

edge = [HoverButton(frame, text="", activebackground="black", background="white", relief="ridge",
                      command=lambda i=i: btnClick(i)) for i in range(40)]

edge[0].place(x=30, y=22, height=7, width=42)
edge[1].place(x=81, y=22, height=7, width=42)
edge[2].place(x=132, y=22, height=7, width=42)
edge[3].place(x=183, y=22, height=7, width=42)
edge[4].place(x=22, y=30, height=42, width=7)
edge[5].place(x=73, y=30, height=42, width=7)
edge[6].place(x=124, y=30, height=42, width=7)
edge[7].place(x=175, y=30, height=42, width=7)
edge[8].place(x=226, y=30, height=42, width=7)
edge[9].place(x=30, y=73, height=7, width=42)
edge[10].place(x=81, y=73, height=7, width=42)
edge[11].place(x=132, y=73, height=7, width=42)
edge[12].place(x=183, y=73, height=7, width=42)
edge[13].place(x=22, y=81, height=42, width=7)
edge[14].place(x=73, y=81, height=42, width=7)
edge[15].place(x=124, y=81, height=42, width=7)
edge[16].place(x=175, y=81, height=42, width=7)
edge[17].place(x=226, y=81, height=42, width=7)
edge[18].place(x=30, y=124, height=7, width=42)
edge[19].place(x=81, y=124, height=7, width=42)
edge[20].place(x=132, y=124, height=7, width=42)
edge[21].place(x=183, y=124, height=7, width=42)
edge[22].place(x=22, y=132, height=42, width=7)
edge[23].place(x=73, y=132, height=42, width=7)
edge[24].place(x=124, y=132, height=42, width=7)
edge[25].place(x=175, y=132, height=42, width=7)
edge[26].place(x=226, y=132, height=42, width=7)
edge[27].place(x=30, y=175, height=7, width=42)
edge[28].place(x=81, y=175, height=7, width=42)
edge[29].place(x=132, y=175, height=7, width=42)
edge[30].place(x=183, y=175, height=7, width=42)
edge[31].place(x=22, y=183, height=42, width=7)
edge[32].place(x=73, y=183, height=42, width=7)
edge[33].place(x=124, y=183, height=42, width=7)
edge[34].place(x=175, y=183, height=42, width=7)
edge[35].place(x=226, y=183, height=42, width=7)
edge[36].place(x=30, y=226, height=7, width=42)
edge[37].place(x=81, y=226, height=7, width=42)
edge[38].place(x=132, y=226, height=7, width=42)
edge[39].place(x=183, y=226, height=7, width=42)

box = dict()
coords = (30.5, 81.5, 132.5, 183.5)
k = 0
for i in coords:
    for j in coords:
        b = tk.Label(frame, text="")
        b.place(x=j, y=i, height="41", width="41")
        box[str(k)] = b
        k += 1
    k += 5
root.mainloop()
