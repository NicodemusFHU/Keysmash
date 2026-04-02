usd = 0
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
        self.prices = {1:1250, 2:2500, 3:4750, 4: 6000}
crit = CritUpgrade()


print("Welcome to Keysmash, spam keys on your keyboard to make $.")
print("Type shop to view the shop.")
#Recurrent input loop
while usd < 1000000:
    string = input()
    added = 0

    #Quit
    if string == "quit":
        break
    
    #Upgrade purchase handling
    if string == "shop":
        string = ""
        print(f"Shop")
        command = ""
        while command != "esc":
            print(f"{value.name} ({value.count}): {value.prices[value.count+1]} ", end="")
            if crit.unlocked:
                print(f"| {crit.name} ({crit.count}): {crit.prices[crit.count+1]} ", end="")
            print("")
            print(f"Type purchase [upgrade name] to purchase an upgrade. Type esc to leave the shop.")
            command = input()
            if command == "purchase value":
                value.purchase()
            elif command == "purchase crit":
                crit.purchase()
            else:
                if command != "esc":
                    print("You're still in the shop...")

    #Calculate charge

    #Multiply/Beam trigger
    last = "no"
    last2 = "no"
    #One used check
    try:
        if string[-1].isdigit() and (string[-2] == "p" or string[-2] == "x"):
            last = string[-2:]
            string = string[:-2]
            #Test
            print(f"{string}, {last}")
    #Both used check
        if string[-3].isdigit() and string[-1].isdigit() and (string[-2] == "p" or string[-2] == "x") and (string[-4] == "p" or string[-4] == "x"):
            last = string[-2:]
            last2 = string[-4:]
            string = string[:-4]
            #Test
            print(f"{string}, {last}")
    except:
        pass

    #Calculate $
    if len(string) % 100 == 0 and crit.count != 0 and string != "":
        added = ((len(string) * (value.count+1)) * (crit.count+1))
        usd += ((len(string) * (value.count+1)) * (crit.count+1))
        print("Crit!")
    else:
        added = (len(string) * (value.count+1))
        usd += (len(string) * (value.count+1))

    if string != "":
        print(f"+{added}, now ${usd}")

#Ending (test)
if string != "quit":
    print("You win!")
else:
    print("Quitting...")

#Crit test string
#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa

#Notes
'''

Max characters per input is 4095

'''