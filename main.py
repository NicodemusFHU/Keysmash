import pygame
import sys
import ptext
import random

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode([1600, 900])
font = pygame.font.Font("inconsolata.ttf", 24)
green = pygame.Color("green")
black = pygame.Color("black")

usd = 0
questioncount = 0
def format(n):
    if n == "MAX":
        return n
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
        self.prices = {1:2500, 2:5000, 3:10000, 4: 20000, 5:40000, 6:45000, 7:50000, 8:55000, 9:60000, 10:65000, 11:"MAX"}
        self.charges = 0

    def chargeadd(self, s):
        global addedcharges
        self.charges += len(s)
        addedcharges = len(s)
        if self.charges > self.count*100:
            self.charges = int(self.count*100)

    def purchase(self):
        global usd
        try:
            if usd >= self.prices[self.count+1]:
                usd -= self.prices[self.count+1]
                self.count +=1
                multiply.unlock()
                photonbeam.unlock()
                if self.count == 10:
                    end.unlock()
            else:
                guiprint(0, f"You do not have enough $ to purchase this upgrade.")
        except:
            guiprint(0, f"Cannot purchase {self.name} upgrade, max level already reached.")

charge = ChargeUpgrade()

class PoweredUpgrade(BaseUpgrade):
    def __init__(self):
        super().__init__()
    def removecharge(self, c):
        if charge.charges >= c * 100:
            charge.charges -= c * 100
        else:
            raise ValueError

class MultiplyUpgrade(PoweredUpgrade):
    def __init__(self):
        super().__init__()
        self.name = "Multiply"
        self.prices = {1: 6000, 2: 10000, 3: 16000, 4: 20000, 5: 40000, 6:"MAX"}

    def multiply(self, s, x):
        try:
            self.removecharge(x)
            return s * (x+1)
        except ValueError:
            guiprint(0, "Insufficient charge to use Multiply")
            return s
multiply = MultiplyUpgrade()

class PhotonBeamUpgrade(PoweredUpgrade):
    def __init__(self):
        super().__init__()
        self.name = "Photon Beam"
        self.prices = {1: 6000, 2: 10000, 3: 16000, 4: 20000, 5: 40000, 6:"MAX"}
    
    def beam(self, s, b):
        try:
            self.removecharge(b)
            return s.join(random.choice("`~1!2@3#4$5%6^7&8*9(0)qQwWeErRtTyYuUiIoOpP[{]}\\|aAsSdDfFgGhHjJkKlL;:\'\"zZxXcCvVbBnNmM,<.>/?") for _ in range(50 * (b+1)))
        except ValueError:
            guiprint(0, "Insufficient charge to use Photon Beam")
            return s
photonbeam = PhotonBeamUpgrade()

class End(BaseUpgrade):
    def __init__(self):
        super().__init__()
        self.name = "Ending"
        self.prices = {1:10000000, 2:"MAX"}
    def purchase(self):
        global usd
        try:
            if usd >= self.prices[self.count+1]:
                usd -= self.prices[self.count+1]
                self.count +=1
                guiprint(0, f"Now that you've split from the company, each character has a base value of $1.00")
            else:
                guiprint(0, f"You do not have enough $.")
        except:
            guiprint(0, f"Ending already attained.")
end = End()

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
multiplyuses = 0
photonbeamuses = 0
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
    global totalchr
    global multiplyuses
    global photonbeamuses

    if len(previous) == 10:
        previous.pop(0)
    string = input.replace("\n", "")
    previous.append(BigStr(rowcount, input))
    input = str()
    if charge.count > 0:
        charge.chargeadd(string)
    if photonbeamuses > 0:
        string = photonbeam.beam(string, photonbeamuses)
        if previous[-1].string != "Insufficient charge to use Photon Beam":
            previous[-1].string += f"\n+{photonbeamuses*50}"
            previous[-1].lines += 1
        photonbeamuses = 0
    if multiplyuses > 0:
        string = multiply.multiply(string, multiplyuses)
        if previous[-1].string != "Insufficient charge to use Multiply":
            previous[-1].string += f"\nX{multiplyuses+1}"
            previous[-1].lines += 1
        multiplyuses = 0
    previouslen = len(string)
    if len(string) % 100 == 0 and crit.count != 0 and string != "":
        added = ((len(string) * (value.count+1)) * (crit.count+1))
        totalchr += len(string)
    else:
        added = (len(string) * (value.count+1))
        totalchr += len(string)
    rowcount = 0
    round += 1

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
                    if end.count > 0:
                        if len(string) % 100 == 0 and crit.count != 0 and string != "":
                            usd += ((len(string) * 100 * (value.count+1)) * (crit.count+1))
                        else:
                            usd += (len(string) * 100 * (value.count+1))
                    else:
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
                if crit.unlocked:
                    if mouse[0] > 1209 and mouse[1] > 115 and mouse[1] < 195:
                        crit.purchase()
                if charge.unlocked:
                    if mouse[0] > 1209 and mouse[1] > 200 and mouse[1] < 280:
                        charge.purchase()
                if multiply.unlocked:
                    if mouse[0] > 1209 and mouse[1] > 285 and mouse[1] < 365:
                        multiply.purchase()
                if photonbeam.unlocked:
                    if mouse[0] > 1209 and mouse[1] > 370 and mouse[1] < 450:
                        photonbeam.purchase()
                if end.unlocked:
                    if mouse[0] > 1209 and mouse[1] > 455 and mouse[1] < 535:
                        end.purchase()
                if multiply.count > 0:
                    if mouse[0] > 1211 and mouse[0] < 1237 and mouse[1] > 750 and mouse[1] < 776:
                        if multiply.count > multiplyuses:
                            multiplyuses += 1
                if photonbeam.count > 0:
                    if mouse[0] > 1211 and mouse[0] < 1237 and mouse[1] > 720 and mouse[1] < 746:
                        if photonbeam.count > photonbeamuses:
                            photonbeamuses += 1
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:
                if multiply.count > 0:
                    if mouse[0] > 1211 and mouse[0] < 1237 and mouse[1] > 750 and mouse[1] < 776:
                        if multiplyuses > 0:
                            multiplyuses -= 1
                if photonbeam.count > 0:
                    if mouse[0] > 1211 and mouse[0] < 1237 and mouse[1] > 720 and mouse[1] < 746:
                        if photonbeamuses > 0:
                            photonbeamuses -= 1


    #Mouse position
    mouse = pygame.mouse.get_pos()
    
    screen.fill(black)
    #Textbox rendering
    pygame.draw.rect(screen, green, pygame.Rect(0, 870-rowcount*26, 1209, 30+rowcount*26), 2)
    ptext.draw(input, (5, 870-rowcount*26), color=green, fontname="inconsolata.ttf")

    #Previous entry rendering
    ptext.draw(previous[-1].string, (5, 840-previous[-1].lines*26-rowcount*26), color=green, fontname="inconsolata.ttf")

    #Powered upgrade button rendering
    if multiply.count > 0:
        pygame.draw.rect(screen, green, pygame.Rect(1211, 750, 26, 26))
        screen.blit(font.render(f"X{multiplyuses}", False, True, green), (1211, 750))
    if photonbeam.count > 0:
        pygame.draw.rect(screen, green, pygame.Rect(1211, 720, 26, 26))
        screen.blit(font.render(f"+{photonbeamuses*50}", False, True, green), (1211, 720))

    #Stats rendering
    if previous[-1].string != "Welcome to Keysmash, spam keys on your keyboard to make $." and previous[-1]:
        if charge.count > 0:
            screen.blit(font.render(f"+${format(added)}, +*{format(addedcharges)}", True, green), (1211, 870))
        else:
            screen.blit(font.render(f"+${format(added)}", True, green), (1211, 870))
        if previouslen > 1:
            screen.blit(font.render(f"Last: {previouslen} characters,", True, green), (1211, 840))
        else:
            screen.blit(font.render(f"Last: {previouslen} character,", True, green), (1211, 840))
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
    ptext.draw(f"\t\t\t\t- {value.name} -\nIncreases base earnings\nper character", (1210, 30), color=green, fontname="inconsolata.ttf")
    if mouse[0] > 1209 and mouse[1] > 25 and mouse[1] < 110: 
        pygame.draw.rect(screen, green, pygame.Rect(1209, 30, 390, 80), 2)
    #Crit
    if crit.unlocked:
        screen.blit(font.render(f"({crit.count}/5) ${format(crit.prices[crit.count+1])}", False, True, green), (1210, 115))
        ptext.draw(f"\t\t\t\t- {crit.name} -\nMultiplies value by {crit.count+1}\nif exact line(s) are input", (1210, 115), color=green, fontname="inconsolata.ttf")
        if mouse[0] > 1209 and mouse[1] > 115 and mouse[1] < 195: 
            pygame.draw.rect(screen, green, pygame.Rect(1209, 115, 390, 80), 2)
    #Charge
    if charge.unlocked:
        screen.blit(font.render(f"({charge.count}/10) ${format(charge.prices[charge.count+1])}", False, True, green), (1210, 200))
        ptext.draw(f"\t\t\t\t- {charge.name} -\nStores kinetic energy\nfor use by powered upgrades", (1210, 200), color=green, fontname="inconsolata.ttf")
        if mouse[0] > 1209 and mouse[1] > 200 and mouse[1] < 280:
            pygame.draw.rect(screen, green, pygame.Rect(1209, 200, 390, 80), 2)
    #Multiply
    if multiply.unlocked:
        screen.blit(font.render(f"({multiply.count}/5) ${format(multiply.prices[multiply.count+1])}", False, True, green), (1210, 285))
        ptext.draw(f"\t\t\t\t- {multiply.name} -\nUses up to *{multiply.count} to multiply\ninput characters by up to {multiply.count}", (1210, 285), color=green, fontname="inconsolata.ttf")
        if mouse[0] > 1209 and mouse[1] > 285 and mouse[1] < 365:
            pygame.draw.rect(screen, green, pygame.Rect(1209, 285, 390, 80), 2)
    #Photon Beam
    if photonbeam.unlocked:
        screen.blit(font.render(f"({photonbeam.count}/5) ${format(photonbeam.prices[photonbeam.count+1])}", False, True, green), (1210, 370))
        ptext.draw(f"\t\t\t\t- {photonbeam.name} -\nUses up to *{photonbeam.count} to\nadd 50 characters per * used", (1210, 370), color=green, fontname="inconsolata.ttf")
        if mouse[0] > 1209 and mouse[1] > 370 and mouse[1] < 450:
            pygame.draw.rect(screen, green, pygame.Rect(1209, 370, 390, 80), 2)
    #End
    if end.unlocked:
        screen.blit(font.render(f"({end.count}/1) ${format(end.prices[end.count+1])}", False, True, green), (1210, 455))
        ptext.draw(f"\t\t\t\t- {end.name} -\nSplit off from The Company,\nends the game", (1210, 455), color=green, fontname="inconsolata.ttf")
        if mouse[0] > 1209 and mouse[1] > 455 and mouse[1] < 535:
            pygame.draw.rect(screen, green, pygame.Rect(1209, 455, 390, 80), 2)

    #Frame advancing, window title
    pygame.display.set_caption(f"Keysmash: ${format(usd)}")
    pygame.display.flip()
    clock.tick()