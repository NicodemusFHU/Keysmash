
usd = 0
#Recurrent input loop
while usd < 1000000:
    string = input()

    #Dev loop escape
    if string == "esc":
        break
    
    #Purchase input handling
    '''if string == purchasexyz:
        if usd >= upgradexyz.cost:
            upgradexyz.purchase()
    elif string == purchaseabc:
        if usd >= upgradeabc.cost:
            upgradeabc.purchase()'''
    
    #Multiply/Beam trigger
    last = "no"
    last2 = "no"
    #One used check
    if string[-1].isdigit() and string[-2] == "p" or "x":
        last = string[-2:]
        string = string[:-2]
        #Test
        print(f"{string}, {last}")
    #Both used check
    if string[-3].isdigit() and string[-1].isdigit() and string[-2] == "p" or "x" and string[-4] == "p" or "x":
        last = string[-2:]
        last2 = string[-4:]
        string = string[:-4]
        #Test
        print(f"{string}, {last}")

    #Multiply first handling
    '''if last[0] == "x" and last[1].isdigit():
        multcount = int(last[2])
        if multcount < 0:
            multcount -= 1
        string = string + string*(multcount)
        if last2[0] == "p" and last2[1].isdigit():
            string.append("unfinished, add the random alphanumeric function call")
    #Beam first handling
    if last[0] == "p" and last[1].isdigit():
        string.append("unfinished, add the random alphanumeric function call")
        if last2[0] == "x" and last2[1].isdigit():
            multcount = int(last[2])
            if multcount < 0:
                multcount -= 1
            string = string + string*(multcount)'''     

#Ending (test)
print("You win")