import pygame
import sys
import ptext
import random
import string as strlib

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode([1600, 900])
font = pygame.font.Font("inconsolata.ttf", 24)
green = pygame.Color("green")
black = pygame.Color("black")

usd = 0
questioncount = 0
def format(n):
    if n < 10:
        stringnum = "0.0" + str(n)
    elif n < 100:
        stringnum = "0." + str(n)
    else:
        stringnum = str(n)
        decimals = stringnum[-2:]
        stringnum = stringnum[:-2]
        stringnum = stringnum + "." + decimals
    return stringnum

class BaseUpgrade:
    def __init__(self):
        self.name = ""
        self.count = 0
        self.prices = dict()
        self.unlocked = False
    def purchase(self):
        global usd
        try:
            if usd >= self.prices[self.count+1]:
                usd -= self.prices[self.count+1]
                self.count +=1
            else:
                print(f"You do not have enough $ to purchase this upgrade.")
        except:
            print(f"Cannot purchase {self.name} upgrade, max level already reached.")
    def unlock(self):
        self.unlocked = True

class ValueUpgrade(BaseUpgrade):
    def __init__(self):
        super().__init__()
        self.name = "Value"
        self.prices = {1:500, 2:1000, 3:3500, 4: 4500, 5: 7000, 6:"MAX"}
        self.unlocked = True
    def purchase(self):
        global usd
        try:
            if usd >= self.prices[self.count+1]:
                usd -= self.prices[self.count+1]
                self.count +=1
                crit.unlock()
            else:
                guiprint(0, f"You do not have enough $ to purchase this upgrade.")
        except:
            guiprint(0, f"Cannot purchase {self.name} upgrade, max level already reached.")
value = ValueUpgrade()

class CritUpgrade(BaseUpgrade):
    def __init__(self):
        super().__init__()
        self.name = "Crit"
        self.prices = {1:1250, 2:2500, 3:4750, 4: 6000, 5:7500, 6:"MAX"}
    def purchase(self):
        global usd
        try:
            if usd >= self.prices[self.count+1]:
                usd -= self.prices[self.count+1]
                self.count +=1
                charge.unlock()
            else:
                guiprint(0, f"You do not have enough $ to purchase this upgrade.")
        except:
            guiprint(0, f"Cannot purchase {self.name} upgrade, max level already reached.")
crit = CritUpgrade()

class ChargeUpgrade(BaseUpgrade):
    def __init__(self):
        super().__init__()
        self.name = "Charge"
        self.prices = {1:2500, 2:5000, 3:10000, 4: 20000, 5:40000, 6:"MAX"}
        self.charges = 0

    def chargeadd(self, s):
        global addedcharges
        self.charges += len(s)
        addedcharges = len(s)
        if self.charges > self.count*100:
            self.charges = int(self.count*100)

charge = ChargeUpgrade()

class PoweredUpgrade(BaseUpgrade):
    def removecharge(self, c):
        charge._count -= (c * 100)
        if charge._count < 0:
            charge._count = 0

class MultiplyUpgrade(PoweredUpgrade):
    def __init__(self):
        super().__init__()
        self.name = "Multiply"
        self.prices = {1: 2000, 2: 4000, 3: 7000, 4: 10000, 5: 15000}
        self.unlocked = False
    def multiply(self, s, x):
        if x <= self.count:
            self.removecharge(1)
            return s * x
        return s
multiply = MultiplyUpgrade()

class PhotonBeamUpgrade(PoweredUpgrade):
    def __init__(self):
        super()._init_()
        self.name = "Photon Beam"
        self.prices = {1: 3000, 2: 6000, 3: 9000, 4: 13000, 5: 18000}
        self.unlocked = False
    
    def beam(self, b):
        if (b * 100) <= charge.count:
            chars = strlib.ascii_letters + strlib.digits
            out = "".join(random.choice(chars) for _ in range(50 * (b + 1)))
            self.removecharge(b)
            return out
        return ""

class BigStr():
    def __init__(self, lines=0, string=str()):
        self.lines = lines
        self.string = string

previous = (BigStr(),BigStr(),BigStr(),BigStr(),BigStr(),BigStr(),BigStr(),BigStr(),BigStr(),BigStr(0, "Welcome to Keysmash, spam keys on your keyboard to make $."))
previous = list(previous)
added = 0
previouslen = 0
addedcharges = 0
totalchr = 0
def guiprint(rc, s):
    global previous
    if len(previous) == 10:
        previous.pop(0)
    previous.append(BigStr(rc, s))
def enter():
    global previous
    global string
    global input
    global rowcount
    global added
    global value
    global crit
    global previouslen
    global round
    global addedcharges
    global totalchr

    if len(previous) == 10:
        previous.pop(0)
    string = input.replace("\n", "")
    previous.append(BigStr(rowcount, input))
    input = str()
    previouslen = len(string)
    if len(string) % 100 == 0 and crit.count != 0 and string != "":
        added = ((len(string) * (value.count+1)) * (crit.count+1))
        totalchr += len(string)
    else:
        added = (len(string) * (value.count+1))
        totalchr += len(string)
    rowcount = 0
    round += 1
    if charge.unlocked:
        charge.chargeadd(string)

string = str()
input = str()
rowcount = 0
round = 0
#Game loop
running = True
while running == True:
    #Input textbox/quit
    for event in pygame.event.get():
        screen
        #Input handling
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                input = str()
                rowcount = 0
            elif event.key == pygame.K_RETURN:
                if input != "":
                    enter()
                    if len(string) % 100 == 0 and crit.count != 0 and string != "":
                        usd += ((len(string) * (value.count+1)) * (crit.count+1))
                    else:
                        usd += (len(string) * (value.count+1))
            elif event.key != pygame.K_TAB:
                if len(input.split("\n")[-1]) == 100:
                    input +="\n"
                    rowcount +=1
                input += event.unicode
        #External quit handling
        if event.type == pygame.QUIT:
            running = False
            pygame.quit
            sys.exit
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if mouse[0] > 1209 and mouse[1] >= 30 and mouse[1] < 100:
                    value.purchase()
                if mouse[0] > 1209 and mouse[1] > 115 and mouse[1] < 195:
                    crit.purchase()
                if mouse[0] > 1209 and mouse[1] > 200 and mouse[1] < 280:
                    charge.purchase()


    #Mouse position
    mouse = pygame.mouse.get_pos()
    
    screen.fill(black)
    #Textbox rendering
    pygame.draw.rect(screen, green, pygame.Rect(0, 870-rowcount*26, 1209, 30+rowcount*26), 2)
    ptext.draw(input, (5, 870-rowcount*26), color=green, fontname="inconsolata.ttf")

    #Previous entry rendering
    ptext.draw(previous[-1].string, (5, 840-previous[-1].lines*26-rowcount*26), color=green, fontname="inconsolata.ttf")

    #Stats rendering
    if previous[-1].string != "Welcome to Keysmash, spam keys on your keyboard to make $." and previous[-1]:
        if charge.count > 0:
            screen.blit(font.render(f"+${format(added)}, +*{format(addedcharges)}", True, green), (1211, 870))
        else:
            screen.blit(font.render(f"+${format(added)}", True, green), (1211, 870))
        screen.blit(font.render(f"Last: {previouslen} characters,", True, green), (1211, 840))
        screen.blit(font.render(f"Total characters: {totalchr}", True, green), (1211, 810))
        screen.blit(font.render(f"Round: {round}", True, green), (1211, 780))

    #Balance rendering
    if charge.count > 0:
        screen.blit(font.render(f"*{format(charge.charges)}/{charge.count}, ${format(usd)}", False, True, green), (1600-len(f"*{format(charge.charges)}/{charge.count}, ${format(usd)}")*12, 0))
    else:
        screen.blit(font.render(f"${format(usd)}", False, True, green), (1600-len(f"${format(usd)}")*12, 0))

    #Shop rendering
    #Value
    screen.blit(font.render(f"({value.count}/5) ${format(value.prices[value.count+1])}", False, True, green), (1210, 30))
    ptext.draw(f"\t\t\t\t\t- Value -\nIncreases base earnings\nper character", (1210, 30), color=green, fontname="inconsolata.ttf")
    if mouse[0] > 1209 and mouse[1] > 25 and mouse[1] < 110: 
        pygame.draw.rect(screen, green, pygame.Rect(1209, 30, 390, 80), 2)
    #Crit
    if crit.unlocked:
        screen.blit(font.render(f"({crit.count}/5) ${format(crit.prices[crit.count+1])}", False, True, green), (1210, 115))
        ptext.draw(f"\t\t\t\t\t- Crit -\nMultiplies value by {crit.count+1}\nif exact line(s) are input", (1210, 115), color=green, fontname="inconsolata.ttf")
        if mouse[0] > 1209 and mouse[1] > 115 and mouse[1] < 195: 
            pygame.draw.rect(screen, green, pygame.Rect(1209, 115, 390, 80), 2)
    #Charge
    if charge.unlocked:
        screen.blit(font.render(f"({charge.count}/5) ${format(charge.prices[charge.count+1])}", False, True, green), (1210, 200))
        ptext.draw(f"\t\t\t\t\t- Charge -\nStores kinetic energy\nfor use by powered upgrades", (1210, 200), color=green, fontname="inconsolata.ttf")
        if mouse[0] > 1209 and mouse[1] > 200 and mouse[1] < 280:
            pygame.draw.rect(screen, green, pygame.Rect(1209, 200, 390, 80), 2)

    #Frame advancing, window title
    pygame.display.set_caption(f"Keysmash: ${format(usd)}")
    pygame.display.flip()
    clock.tick()

#Notes
'''

Max characters per input is 4095

Potential upgrade: every character printed in the console counts for $ and charge calculations.

Todo:
Add round counter
Add save files

'''
