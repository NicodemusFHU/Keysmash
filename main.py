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

class ChargeManager:
    def __init__(self):
        self._count = 0
        self._capacity = 1

    def chargeadd(self, s):
        self._count += len(s)
        if self._count > self._capacity:
            self._count = self._capacity

    def __str__(self):
        if self._count == 1:
            return f"{format(self._count)} charge"
        return f"{format(self._count)} charges"
    
charge_manager = ChargeManager()

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

class ChargedUpgrade(BaseUpgrade):
    def removecharge(self, c):
        charge_manager._count -= (c * 100)
        if charge_manager._count < 0:
            charge_manager._count = 0

class ValueUpgrade(BaseUpgrade):
    def __init__(self):
        super().__init__()
        self.name = "Value"
        self.prices = {1:500, 2:1000, 3:3500, 4: 4500, 5: 7000}
        self.unlocked = True
    def purchase(self):
        global usd
        try:
            if usd >= self.prices[self.count+1]:
                usd -= self.prices[self.count+1]
                self.count +=1
                crit.unlock()
            else:
                print(f"You do not have enough $ to purchase this upgrade.")
        except:
            print(f"Cannot purchase {self.name} upgrade, max level already reached.")
        if self.count == 0:
            crit.unlock
value = ValueUpgrade()

class CritUpgrade(BaseUpgrade):
    def __init__(self):
        super().__init__()
        self.name = "Crit"
        self.prices = {1:1250, 2:2500, 3:4750, 4: 6000, 5:7500}
crit = CritUpgrade()

class MultiplyUpgrade(ChargedUpgrade):
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

class PhotonBeamUpgrade(ChargedUpgrade):
    def __init__(self):
        super()._init_()
        self.name = "Photon Beam"
        self.prices = {1: 3000, 2: 6000, 3: 9000, 4: 13000, 5: 18000}
        self.unlocked = False
    
    def beam(self, b):
        if (b * 100) <= charge_manager.count:
            chars = strlib.ascii_letters + strlib.digits
            out = "".join(random.choice(chars) for _ in range(50 * (b + 1)))
            self.removecharge(b)
            return out
        return ""

class BigStr():
    def __init__(self, lines=0, string=str()):
        self.lines = lines
        self.string = string

def help():
    return(BigStr(3, "Type \"shop\" to view the shop.\nType \"$\" or \"balance\" to view your current $.\nType \"help\" to repeat the available commands.\nType \"quit\" to return to your terminal."))

previous = (BigStr(),BigStr(),BigStr(),BigStr(),BigStr(),BigStr(),BigStr(),BigStr(),BigStr(),BigStr(0, "Welcome to Keysmash, spam keys on your keyboard to make $."))
previous = list(previous)
def enter():
    global previous
    global string
    global input
    global rowcount

    if len(previous) == 10:
        previous.pop(0)
    string = str(input)
    previous.append(BigStr(rowcount, string))
    input = str()
    rowcount = 0

print("Welcome to Keysmash, spam keys on your keyboard to make $.")
help()
string = str()
input = str()
rowcount = 0
#Game loop
running = True
while running == True:
    #Input textbox/quit
    for event in pygame.event.get():
        screen
        #Input handling
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE and pygame.key.get_mods() & pygame.KMOD_CTRL:
                input = str()
            elif event.key == pygame.K_BACKSPACE:
                input = input[:-1]
            elif event.key == pygame.K_RETURN:
                enter()
                if string != "help" and string != "":
                    if len(string) % 100 == 0 and crit.count != 0 and string != "":
                        added = ((len(string) * (value.count+1)) * (crit.count+1))
                        usd += ((len(string) * (value.count+1)) * (crit.count+1))
                    else:
                        added = (len(string) * (value.count+1))
                        usd += (len(string) * (value.count+1))
                elif string.lower() == "help":
                    if len(previous) == 10:
                        previous.pop(0)
                        previous.append(help())
                        string = str()
            else:
                if len(input.split("\n")[-1]) > 100:
                    input +="\n"
                    rowcount +=1
                input += event.unicode
        if event.type == pygame.QUIT:
            running = False
            pygame.quit
            sys.exit

    screen.fill(black)
    #Textbox rendering
    pygame.draw.rect(screen, green, pygame.Rect(0, 870-rowcount*26, 1225, 30+rowcount*26), 2)
    ptext.draw(input, (5, 870-rowcount*26), color=green, fontname="inconsolata.ttf")

    #Previous entry rendering
    pygame.draw.rect(screen, green, pygame.Rect(0, 840-previous[-1].lines*26-rowcount*26, 1225, 30+previous[-1].lines*26), 2)
    ptext.draw(previous[-1].string, (5, 840-previous[-1].lines*26-rowcount*26), color=green, fontname="inconsolata.ttf")

    #Balance
    screen.blit(font.render(f"${format(usd)}", True, green), (1579-len(format(usd))*12, 5))

    #Frame advancing, window title
    pygame.display.set_caption(f"Keysmash: ${format(usd)}")
    pygame.display.flip()
    clock.tick()

    added = 0

    #Shop menu
    #if string.lower() == "shop":
    #    string = ""
    #    print(f"===== Shop: =====")
    #    command = ""
    #    while command.lower() != "esc":
    #        print(f"{value.name} ({value.count}): ${format(value.prices[value.count+1])} ", end="")
    #        if crit.unlocked:
    #            print(f"| {crit.name} ({crit.count}): ${format(crit.prices[crit.count+1])} ", end="")
    #        print("")
    #        print(f"Type \"purchase [upgrade name]\" to purchase an upgrade. Type \"esc\" to leave the shop.")
    #        command = input
    #        if command.lower() == "purchase value":
    #            value.purchase()
    #        elif command.lower() == "purchase crit":
    #            if crit.unlocked == False:
    #                print("Spoilers...")
    #            crit.purchase()
    #        else:
    #            if len(command) % 100 == 0 and command.lower() != "esc" and crit.unlocked == True:
    #                print("Crit!\n... but you were still in the shop.")
    #            elif command.lower() != "esc":
    #                print("You're still in the shop...")

#Ending (test)
#if string.lower() != "quit":
#    print("You win!")
#else:
#    print("Quitting...")

#Crit test string
#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa

#Notes
'''

Max characters per input is 4095

Potential upgrade: every character printed in the console counts for $ and charge calculations.

Todo:
Add round counter
Add save files

'''
