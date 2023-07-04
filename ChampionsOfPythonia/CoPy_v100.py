"""
Champions of Pythonia
Version: 1.0.0
"""

# Imports requisite modules.
import random
import tkinter


player_name_tuple = ("Anais", "Bertha", "Chuck", "Duke", "Emery", "Franco",
                     "Greta", "Hale", "Imani", "Itzel", "Juan", "Jet", "Kobe",
                     "Lottie", "Marco", "Megumi", "Nigel", "Noriko", "Oscar",
                     "Olu", "Petunia", "Poe", "Quetzal", "Roland", "Saki",
                     "Tam", "Uther", "Vinny", "Walter", "Xavi", "Ysabel",
                     "Zainab")

foe_name_tuple = ("Aamyn", "Alrud", "Bort", "Crimeo", "Despo", "Eckoze",
                  "Frant", "Girn", "Hemra", "Ichabod", "Junta", "Lumk",
                  "Mizmos", "Morgoth", "Nulj", "Omolg", "Ququi", "Raoful",
                  "Smiggit", "Tusk", "Ungol", "Vorry", "Whelp", "Xebon", "Yog",
                  "Zuinth")

player_fight_tuple = ("You swing!  Sparks fly as your\nweapon's tip scrapes the cobblestones!",
                      "Rules be damned.  You drop your\nweapon and lunge at your opponent!",
                      "With a dancer's grace, you spin\nand strike at your foe!",
                      "You lock blades with the enemy,\npressing for advantage!",
                      "With a mighty roar, you hurtle towards\nyour opponent like a streaking comet!",
                      "You charge, ready to cut down your\nenemy with deadly precision!")

foe_fight_tuple = ("With a piercing screech, your enemy\npounces onto your back!",
                   "The enemy's attacks are ferocious!\nFangs glisten!  Blood flows!",
                   "Your opponent bum-rushes you!  You\nboth collapse in a tangled melee.",
                   "Your foe thrashes wildly, a crazed\ngleam in their eye!",
                   "Cackling, your foe hurls a fiery orb\nat your chest!",
                   "With a sturdy grunt, your opponent heaves\ntheir weapon high.  It crashes down at you!")

fight_wrap_tuple = ("The fight is brutal beyond telling.",
                    "This is a battle for the ages!",
                    "Bards will sing of this confrontation!",
                    "As the dust settles, a victor stands tall.",
                    "The fight is short, crude, and vicious.",
                    "Suddenly, one combatant falters...and falls!")

winner = "winner"


class MPGUI1:
    def __init__(self):
        """
        Creates the first window & sets configurations.
        Selects & displays a player name.
        """
        self.main_window = tkinter.Tk()
        positionRight = int(self.main_window.winfo_screenwidth()/2)
        positionDown = int(self.main_window.winfo_screenheight()/2)
        self.main_window.geometry("600x300+{}+{}".format(positionRight-300, positionDown-300))
        self.main_window.title("Champions of Pythonia")
        self.main_window.option_add( "*font", "lucida 20 bold italic" )
        self.main_window.resizable(False, False)

        self.main_window.iconbitmap("BG_icon.ico")
        self.background_image = tkinter.PhotoImage(file="BG_04C.png")
        self.background_label = tkinter.Label(image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.label1 = tkinter.Label(self.main_window, text="Hail & well met, "
                                   "brave hero!", bg="#624434", fg="#f6dbb7")
        self.label1.pack(padx=0, pady=10, ipadx=150)
        self.label2 = tkinter.Label(self.main_window, text="Pick up your "
                                    "weapon and prepare for battle!", bg="#624434", fg="#f6dbb7")
        self.label2.pack(padx=0, pady=(0, 10), ipadx=150)      
        self.name = random.choice(player_name_tuple)
        self.label4 = tkinter.Label(self.main_window, text=f"Kismet favors you.\nYou shall be known as {self.name}!", bg="#624434", fg="#f6dbb7")
        self.label4.pack(padx=0, pady=(0, 10), ipadx=150)
        self.ok_button = tkinter.Button(self.main_window, text="Forsooth!", bg="#624434", fg="#f6dbb7", activeforeground="#f6dbb7", activebackground="#624434", relief="groove",
                                        command = self.main_window.destroy)
        self.ok_button.pack(padx=0, pady=10, ipadx=0, ipady=0, side="bottom")
        tkinter.mainloop()

    def prname(self):
        return self.name

class MPGUI4:
    def __init__(self, pname):
        """
        Creates the second window & sets configurations.
        Flavor text.
        """
        self.name = pname
        self.main_window = tkinter.Tk()
        positionRight = int(self.main_window.winfo_screenwidth()/2)
        positionDown = int(self.main_window.winfo_screenheight()/2)
        self.main_window.geometry("600x300+{}+{}".format(positionRight-300, positionDown-300))
        self.main_window.title("Champions of Pythonia")
        self.main_window.option_add( "*font", "lucida 20 bold italic" )
        self.main_window.resizable(False, False)

        self.main_window.iconbitmap("BG_icon.ico")
        self.background_image = tkinter.PhotoImage(file="BG_04C.png")
        self.background_label = tkinter.Label(image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        
        self.label1 = tkinter.Label(self.main_window, text=f"May your name become legend, {self.name}!", bg="#624434", fg="#f6dbb7")
        self.label1.pack(padx=0, pady=(60, 10), ipadx=150)
        self.label2 = tkinter.Label(self.main_window, text=f"Now, we must enumerate your attributes...", bg="#624434", fg="#f6dbb7")
        self.label2.pack(padx=0, pady=(0, 10), ipadx=150)
        self.roll_button = tkinter.Button(self.main_window, text="Roll for stats!", bg="#624434", fg="#f6dbb7", activeforeground="#f6dbb7", activebackground="#624434", relief="groove",
                                          command=self.main_window.destroy)
        self.roll_button.pack(padx=0, pady=10, ipadx=0, ipady=0, side="bottom")
        tkinter.mainloop()

class MPGUI5:
    def __init__(self):
        """
        Creates the third window & sets configurations.
        Generates & displays player stats.
        """
        self.p_health = []
        self.p_strength = []
        self.p_defense = []
        self.t_p_stat = 0
        self.main_window = tkinter.Tk()
        positionRight = int(self.main_window.winfo_screenwidth()/2)
        positionDown = int(self.main_window.winfo_screenheight()/2)
        self.main_window.geometry("600x300+{}+{}".format(positionRight-300, positionDown-300))
        self.main_window.title("Champions of Pythonia")
        self.main_window.option_add( "*font", "lucida 20 bold italic" )
        self.main_window.resizable(False, False)

        self.main_window.iconbitmap("BG_icon.ico")
        self.background_image = tkinter.PhotoImage(file="BG_04C.png")
        self.background_label = tkinter.Label(image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.main_window.columnconfigure(0, weight=1)
        self.main_window.columnconfigure(1, weight=1)
       
        self.rollA()
        self.p_health = self.t_p_stat
        self.label1 = tkinter.Label(self.main_window, text=f"Your health:     {self.p_health:02d}", bg="#624434", fg="#f6dbb7", justify="left")
        self.label1.grid(column=1, row=0, padx=(0, 65), pady=(10, 0), ipadx=13, ipady=8)
        self.rollB()
        self.p_strength = self.t_p_stat
        self.label2 = tkinter.Label(self.main_window, text=f"Your strength: {self.p_strength:02d}", bg="#624434", fg="#f6dbb7", justify="left")
        self.label2.grid(column=1, row=1, padx=(0, 65), pady=0, ipadx=15, ipady=8)
        self.rollC()
        self.p_defense = self.t_p_stat
        self.label3 = tkinter.Label(self.main_window, text=f"Your defense:  {self.p_defense:02d}", bg="#624434", fg="#f6dbb7", justify="left")
        self.label3.grid(column=1, row=2, padx=(0, 65), pady=0, ipadx=14, ipady=8)
        self.roll_button = tkinter.Button(self.main_window, text="Onward!", bg="#624434", fg="#f6dbb7", activeforeground="#f6dbb7", activebackground="#624434", relief="groove",
                                          command=self.main_window.destroy)
        self.roll_button.grid(column=0, columnspan=2, row=3, padx=0, pady=(62, 10), ipadx=0, ipady=0, sticky="s")
        tkinter.mainloop()
        
    def rollA(self):
        """
        Displays generated numbers.
        Flavor text.
        """
        p_stat = []
        for i in range(0,4):
            n = random.randint(1,6)
            p_stat.append(n)
        self.labela = tkinter.Label(self.main_window, text=f"The rolls are {p_stat}.\nDiscarding lowest number...", bg="#624434", fg="#f6dbb7", font=('lucida 12 italic'), justify="left")
        self.labela.grid(column=0, row=0, padx=(65, 0), pady=(10, 0), ipadx=15, ipady=5)
        p_stat.remove(min(p_stat))
        self.t_p_stat = sum(p_stat)

    def rollB(self):
        """
        Displays generated numbers.
        Flavor text.
        """
        p_stat = []
        for i in range(0,4):
            n = random.randint(1,6)
            p_stat.append(n)
        self.labela = tkinter.Label(self.main_window, text=f"The rolls are {p_stat}.\nDiscarding lowest number...", bg="#624434", fg="#f6dbb7", font=('lucida 12 italic'), justify="left")
        self.labela.grid(column=0, row=1, padx=(65, 0), pady=0, ipadx=15, ipady=5)
        p_stat.remove(min(p_stat))
        self.t_p_stat = sum(p_stat)

    def rollC(self):
        """
        Displays generated numbers.
        Flavor text.
        """
        p_stat = []
        for i in range(0,4):
            n = random.randint(1,6)
            p_stat.append(n)
        self.labela = tkinter.Label(self.main_window, text=f"The rolls are {p_stat}.\nDiscarding lowest number...", bg="#624434", fg="#f6dbb7", font=('lucida 12 italic'), justify="left")
        self.labela.grid(column=0, row=2, padx=(65, 0), pady=0, ipadx=15, ipady=5)
        p_stat.remove(min(p_stat))
        self.t_p_stat = sum(p_stat)


    def prhealth(self):
        return self.p_health

    def prstrength(self):
        return self.p_strength

    def prdefense(self):
        return self.p_defense

class MPGUI6:
    def __init__(self, pname):
        """
        Creates the forth window & sets configurations.
        Generates & displays enemy name & stats.
        """
        self.name = pname
        self.f_health = []
        self.f_strength = []
        self.f_defense = []
        self.t_f_stat = 0
        self.main_window = tkinter.Tk()
        positionRight = int(self.main_window.winfo_screenwidth()/2)
        positionDown = int(self.main_window.winfo_screenheight()/2)
        self.main_window.geometry("600x300+{}+{}".format(positionRight-300, positionDown-300))
        self.main_window.title("Champions of Pythonia")
        self.main_window.option_add( "*font", "lucida 20 bold italic" )
        self.main_window.resizable(False, False)
        
        self.main_window.iconbitmap("BG_icon.ico")
        self.background_image = tkinter.PhotoImage(file="BG_04C.png")
        self.background_label = tkinter.Label(image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.main_window.columnconfigure(0, weight=1)
        self.main_window.columnconfigure(1, weight=1)
        self.main_window.columnconfigure(2, weight=1)
        
        self.label2 = tkinter.Label(self.main_window, text="It is time to summon your opponent...", bg="#624434", fg="#f6dbb7")
        self.label2.grid(column=0, row=0, columnspan=4, padx=0, pady=10, ipadx=150, ipady=0)
        self.foe_name = random.choice(foe_name_tuple)
        self.label3 = tkinter.Label(self.main_window, text=f"You shall face the dreaded {self.foe_name}!", bg="#624434", fg="#f6dbb7")
        self.label3.grid(column=0, row=1, columnspan=4, padx=0, pady=(0, 10), ipadx=150, ipady=0)
        self.roll()
        self.f_health = self.t_f_stat
        self.label4 = tkinter.Label(self.main_window, text=f"{self.foe_name}'s health:     {self.f_health:02d}", bg="#624434", fg="#f6dbb7")
        self.label4.grid(column=1, row=2, columnspan=1, padx=0, pady=0, ipadx=13, ipady=0)
        self.roll()
        self.f_strength = self.t_f_stat
        self.label5 = tkinter.Label(self.main_window, text=f"{self.foe_name}'s strength: {self.f_strength:02d}", bg="#624434", fg="#f6dbb7")
        self.label5.grid(column=1, row=3, columnspan=1, padx=0, pady=0, ipadx=15, ipady=1)
        self.roll()
        self.f_defense = self.t_f_stat
        self.label6 = tkinter.Label(self.main_window, text=f"{self.foe_name}'s defense:  {self.f_defense:02d}", bg="#624434", fg="#f6dbb7")
        self.label6.grid(column=1, row=4, columnspan=1, padx=0, pady=(0, 10), ipadx=14, ipady=0)
        self.roll_button = tkinter.Button(self.main_window, text="I fear no foe!", bg="#624434", fg="#f6dbb7", activeforeground="#f6dbb7", activebackground="#624434", relief="groove",
                                          command=self.main_window.destroy)
        self.roll_button.grid(column=1, row=5, padx=0, pady=(1, 10), ipadx=0, ipady=0, sticky="s")
        tkinter.mainloop()
        
    def roll(self):
        """
        Rolls for stats.
        """
        f_stat = []
        for i in range(0,4):
            n = random.randint(1,6)
            f_stat.append(n)
        f_stat.remove(min(f_stat))
        self.t_f_stat = sum(f_stat)
        return self.t_f_stat

    def frname(self):
        return self.foe_name

    def frhealth(self):
        return self.f_health

    def frstrength(self):
        return self.f_strength

    def frdefense(self):
        return self.f_defense

class MPGUI7:
    def __init__(self, pname, phealth, pstrength, pdefense, fname, fhealth, fstrength,
                 fdefense):
        """
        Creates the fifth window & sets configurations.
        Displays player & enemy information.
        Flavor text to simulate combat.
        """
        self.name = pname
        self.pheal = phealth
        self.pstr = pstrength
        self.pdef = pdefense
        self.foe = fname
        self.fheal = fhealth
        self.fstr = fstrength
        self.fdef = fdefense
        self.main_window = tkinter.Tk()
        positionRight = int(self.main_window.winfo_screenwidth()/2)
        positionDown = int(self.main_window.winfo_screenheight()/2)
        self.main_window.geometry("600x506+{}+{}".format(positionRight-300, positionDown-300))
        self.main_window.title("Champions of Pythonia")
        self.main_window.option_add( "*font", "lucida 20 bold italic")
        self.main_window.resizable(False, False)

        self.main_window.iconbitmap("BG_icon.ico")
        self.background_image = tkinter.PhotoImage(file="BG_04C.png")
        self.background_label = tkinter.Label(image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.main_window.columnconfigure(0, weight=1)
        self.main_window.columnconfigure(1, weight=2)
        self.main_window.columnconfigure(2, weight=1)

        self.labelA = tkinter.Label(self.main_window, text="All is prepared...for combat!", bg="#624434", fg="#f6dbb7")
        self.labelA.grid(column=0, row=0, columnspan=3, padx=0, pady=(10, 10), ipadx=150)

        self.labelLeft2 = tkinter.Label(self.main_window, text=f"{self.name:<s}", font=('lucida 24 bold italic underline'), bg="#624434", fg="#f6dbb7")
        self.labelLeft2.grid(column=0, row=1, padx=0, pady=0, ipadx=79, ipady=5)
        self.labelLeft3 = tkinter.Label(self.main_window, text=f"Health:     {self.pheal:>02d}\nStrength:  {self.pstr:>02d}\nDefense:   {self.pdef:>02d}", justify="right", bg="#624434", fg="#f6dbb7")
        self.labelLeft3.grid(column=0, row=2, padx=0, pady=0, ipadx=36, ipady=5)

        self.labelVS = tkinter.Label(self.main_window, text="VS", font= ('lucida 28 bold italic'), bg="#624434", fg="#f6dbb7", justify="center")
        self.labelVS.grid(column=1, row=1, pady=0, ipadx=100, ipady=2)

        self.buttonF = tkinter.Button(self.main_window, text="FIGHT!", bg="#624434", fg="#f6dbb7", activeforeground="#f6dbb7", activebackground="#b24534", relief="groove", command = lambda:[self.fight_click(), self.callback_and_hide()])
        self.buttonF.grid(column=1, row=2, padx=0, pady=0, ipadx=8, ipady=18)

        self.labelRight2 = tkinter.Label(self.main_window, text=f"{self.foe:>s}", font= ('lucida 24 bold italic underline'), bg="#624434", fg="#f6dbb7")
        self.labelRight2.grid(column=2, row=1, padx=0, pady=0, ipadx=79, ipady=5)
        self.labelRight3 = tkinter.Label(self.main_window, text=f"Health:     {self.fheal:>02d}\nStrength:  {self.fstr:>02d}\nDefense:   {self.fdef:>02d}", justify="right", bg="#624434", fg="#f6dbb7")
        self.labelRight3.grid(column=2, row=2, padx=0, pady=0, ipadx=36, ipady=5)

        tkinter.mainloop()

    def fight_click(self):
        """
        Flavor text to simulate combat.
        """
        self.pfight = random.choice(player_fight_tuple)
        self.labelD = tkinter.Label(self.main_window, text=f"{self.pfight}", font= ('lucida 16 bold italic'), bg="#624434", fg="#f6dbb7")
        self.labelD.grid(column=0, row=3, columnspan=3, padx=0, pady=10, ipadx=140, ipady=10)
        self.main_window.after(3000, lambda : self.foe_fight_click())

    def foe_fight_click(self):
        """
        Flavor text to simulate combat.
        """
        self.ffight = random.choice(foe_fight_tuple)
        self.labelE = tkinter.Label(self.main_window, text=f"{self.ffight}", font= ('lucida 16 bold italic'), bg="#624434", fg="#f6dbb7")
        self.labelE.grid(column=0, row=4, columnspan=3, padx=0, pady=(0, 10), ipadx=140, ipady=0)
        self.main_window.after(3000, lambda : self.wrapup_click())

    def wrapup_click(self):
        """
        Flavor text to simulate combat.
        """
        self.wrapup = random.choice(fight_wrap_tuple)
        self.labelF = tkinter.Label(self.main_window, text=f"{self.wrapup}", font= ('lucida 16 bold italic'), bg="#624434", fg="#f6dbb7")
        self.labelF.grid(column=0, row=5, columnspan=3, padx=0, pady=(0, 10), ipadx=170, ipady=10)
        self.main_window.after(2000, lambda : self.won_click())

    def won_click(self):
        """
        Moves to next window.
        """
        self.buttonG = tkinter.Button(self.main_window, text="By the Gods, who won?!", bg="#624434", fg="#f6dbb7", activeforeground="#f6dbb7", activebackground="#624434", relief="groove", command=self.main_window.destroy)
        self.buttonG.grid(column=0, row=6, columnspan=3, padx=0, pady=(0, 10), ipadx=0, ipady=0, sticky="s")

    def callback_and_hide(self):
        self.buttonF.grid_forget()



class MPGUI8:
    def __init__(self, pname, phealth, pstrength, pdefense, fname, fhealth, fstrength,
                 fdefense):
        """
        Creates the sixth window & sets configurations.
        """
        self.name = pname
        self.pheal = phealth
        self.pstr = pstrength
        self.pdef = pdefense
        self.foe = fname
        self.fheal = fhealth
        self.fstr = fstrength
        self.fdef = fdefense
        self.winner = "winner"
        self.main_window = tkinter.Tk()
        positionRight = int(self.main_window.winfo_screenwidth()/2)
        positionDown = int(self.main_window.winfo_screenheight()/2)
        self.main_window.geometry("600x300+{}+{}".format(positionRight-300, positionDown-300))
        self.main_window.title("Champions of Pythonia")
        self.main_window.option_add( "*font", "lucida 20 bold italic" )
        self.main_window.resizable(False, False)

        self.main_window.iconbitmap("BG_icon.ico")
        self.background_image = tkinter.PhotoImage(file="BG_04C.png")
        self.background_label = tkinter.Label(image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.combat(pname, phealth, pstrength, pdefense, fname, fhealth, fstrength,
                  fdefense, winner)
        tkinter.mainloop()

    def combat(self, pname, phealth, pstrength, pdefense, fname, fhealth, fstrength,
                  fdefense, winner):
        """
        Simulates combat between characters.
        Declares the winner & loser.
        """
        while phealth >= 0 and fhealth >= 0:
            attack_roll = random.randint(1, 20)
            if attack_roll >= fdefense:
                dmg = pstrength // 3
                fhealth = fhealth - dmg
                if fhealth <= 0:
                    break
            else:
                attack_roll = random.randint(1, 20)
                if attack_roll >= pdefense:
                    dmg = fstrength // 3
                    phealth = phealth - dmg
                    if phealth <= 0:
                        break

        if phealth <= 0:
            self.winner = fname
            self.label1 = tkinter.Label(self.main_window, text=f"Exalt the triumphant: {self.winner}!", bg="#624434", fg="#f6dbb7")
            self.label1.pack(padx=0, pady=(60, 10), ipadx=150)
            self.labelx = tkinter.Label(self.main_window, text=f"May {pname} find rest, eternal.", bg="#624434", fg="#f6dbb7")
            self.labelx.pack(padx=0, pady=(0, 10), ipadx=150)
            self.again_button = tkinter.Button(self.main_window, text="Play again?", bg="#624434", fg="#f6dbb7", activeforeground="#f6dbb7", activebackground="#624434", relief="groove", command = lambda:[self.quit(), self.main()])
            self.again_button.pack(padx=10, pady=(80, 10), ipadx=53, ipady=0, side="left")
            self.quit_button = tkinter.Button(self.main_window, text="Quit!", bg="#624434", fg="#f6dbb7", activeforeground="#f6dbb7", activebackground="#624434", relief="groove", command=self.main_window.destroy)
            self.quit_button.pack(padx=10, pady=(80, 10), ipadx=96, ipady=0, side="right")
        else:
            self.winner = pname
            self.label1 = tkinter.Label(self.main_window, text=f"Exalt the triumphant: {self.winner}!", bg="#624434", fg="#f6dbb7")
            self.label1.pack(padx=0, pady=(60, 10), ipadx=150)
            self.again_button = tkinter.Button(self.main_window, text="Play again?", bg="#624434", fg="#f6dbb7", activeforeground="#f6dbb7", activebackground="#624434", relief="groove", command = lambda:[self.quit(), self.main()])
            self.again_button.pack(padx=10, pady=(130, 10), ipadx=53, ipady=0, side="left")
            self.quit_button = tkinter.Button(self.main_window, text="Quit!", bg="#624434", fg="#f6dbb7", activeforeground="#f6dbb7", activebackground="#624434", relief="groove", command=self.main_window.destroy)
            self.quit_button.pack(padx=10, pady=(130, 10), ipadx=96, ipady=0, side="right")

    def quit(self):
        self.main_window.destroy()

    def main(self):
        main()

def main():
    '''The main function.'''
    mp_gui_1 = MPGUI1()

    pname = mp_gui_1.prname()

    mp_gui_4 = MPGUI4(pname)
    mp_gui_5 = MPGUI5()
    mp_gui_6 = MPGUI6(pname)

    phealth = mp_gui_5.prhealth()
    pstrength = mp_gui_5.prstrength()
    pdefense = mp_gui_5.prdefense()

    fname = mp_gui_6.frname()
    fhealth = mp_gui_6.frhealth()
    fstrength = mp_gui_6.frstrength()
    fdefense = mp_gui_6.frdefense()

    mp_gui_7 = MPGUI7(pname, phealth, pstrength, pdefense, fname, fhealth, fstrength,
                  fdefense)
    mp_gui_8 = MPGUI8(pname, phealth, pstrength, pdefense, fname, fhealth, fstrength,
                  fdefense)

main()
