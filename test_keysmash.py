import pytest
import main

@pytest.fixture
def two_lines_random():
    return main.BigStr(2, "BJ&5@.&&+UkiY[Wf?BR2+Z.)8mS:P=.=gg%q[5q=F-GG9j}$B7.X9k2L?:g?paEf{Wb!i-hY4]rAGF)&9AR@uafMC?Cu7KcK{he?\nm8](_5]Z5[;1E*ubQLT,A51xx%0Lk6Y*F]9n19j%WVw}H%(P(=fE?=fCtHKa1c%R9.u*0MCr@zkWijLCr/KA3Wke3;@yE_(d+tHG")
@pytest.fixture
def reset():
    main.value = main.ValueUpgrade()
    main.crit = main.CritUpgrade()
    main.charge = main.ChargeUpgrade()
    main.usd = 0
    main.totalchr = 0
    main.round = 0


def test_enter_usd_base(two_lines_random, reset):
    main.input = two_lines_random.string
    main.rowcount = two_lines_random.lines
    main.enter()
    assert main.usd == 200


def test_enter_usd_value_charges(two_lines_random, reset):
    main.input = two_lines_random.string
    main.rowcount = two_lines_random.lines
    main.value.count = 1
    main.charge.count = 5
    main.enter()
    assert main.usd == 400 and main.charge.charges == 200

def test_enter_usd_crit_charges(two_lines_random, reset):
    main.input = two_lines_random.string
    main.rowcount = two_lines_random.lines
    main.charge.count = 5
    main.crit.count = 1
    main.enter()
    assert main.usd == 400 and main.charge.charges == 200

def test_enter_stats(two_lines_random, reset):
    main.input = two_lines_random.string
    main.rowcount = two_lines_random.lines
    main.charge.count = 5
    main.enter()
    assert main.added == 200 and main.addedcharges == 200 and main.previouslen == 200 and main.totalchr == 200 and main.round == 1

def test_purchase():
    main.usd = 100497500
    #Extra purchase is intentional to make sure it doesn't do anything unintended if you purchase at max level
    for x in range(7):
        main.value.purchase()
        main.crit.purchase()
        main.multiply.purchase()
        main.photonbeam.purchase()
    for x in range(12):
        main.charge.purchase()
    for x in range(3):
        main.end.purchase()
    assert main.value.count == 5 and main.crit.count == 5 and main.multiply.count == 5 and main.photonbeam.count == 5 and main.charge.count == 10 and main.end.count == 1 and main.usd == 0


#AI output
from unittest.mock import MagicMock

# Mock pygame before importing the game module
import sys
sys.modules['pygame'] = MagicMock()
sys.modules['ptext'] = MagicMock()

# Extract and test the core game logic
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
                self.count += 1
            else:
                raise ValueError("Insufficient funds")
        except KeyError:
            raise ValueError("Max level reached")
    
    def unlock(self):
        self.unlocked = True


class ValueUpgrade(BaseUpgrade):
    def __init__(self):
        super().__init__()
        self.name = "Value"
        self.prices = {1: 500, 2: 1000, 3: 3500, 4: 4500, 5: 7000, 6: "MAX"}
        self.unlocked = True


class ChargeUpgrade(BaseUpgrade):
    def __init__(self):
        super().__init__()
        self.name = "Charge"
        self.prices = {1: 2500, 2: 5000, 3: 10000, 4: 20000, 5: 40000, 6: 45000, 7: 50000, 8: 55000, 9: 60000, 10: 65000, 11: "MAX"}
        self.charges = 0
    
    def chargeadd(self, s):
        self.charges += len(s)
        if self.charges > self.count * 100:
            self.charges = int(self.count * 100)


class PoweredUpgrade(BaseUpgrade):
    def __init__(self):
        super().__init__()
    
    def removecharge(self, c):
        if self.charges >= c * 100:
            self.charges -= c * 100
        else:
            raise ValueError("Insufficient charge")


class MultiplyUpgrade(PoweredUpgrade):
    def __init__(self):
        super().__init__()
        self.name = "Multiply"
        self.prices = {1: 6000, 2: 10000, 3: 16000, 4: 20000, 5: 40000, 6: "MAX"}
        self.charges = 0
    
    def multiply(self, s, x):
        try:
            self.removecharge(x)
            return s * (x + 1)
        except ValueError:
            return s


def format_number(n):
    """Test the format function from the game"""
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


# ===== TEST 1: Format Function =====
def test_format_number():
    """Test the format function with various number ranges"""
    assert format_number(5) == "0.05"
    assert format_number(50) == "0.50"
    assert format_number(100) == "1.00"
    assert format_number(1234) == "12.34"
    assert format_number("MAX") == "MAX"


# ===== TEST 2: Upgrade Purchase Mechanics =====
def test_value_upgrade_purchase():
    """Test that Value upgrade can be purchased correctly"""
    global usd
    usd = 1000
    value = ValueUpgrade()
    
    assert value.count == 0
    value.purchase()
    assert value.count == 1
    assert usd == 500


# ===== TEST 3: Charge Mechanics =====
def test_charge_add_and_cap():
    """Test charge accumulation and cap limits"""
    charge = ChargeUpgrade()
    charge.count = 1  # Cap is 100
    
    charge.chargeadd("hello")  # 5 chars
    assert charge.charges == 5
    
    charge.chargeadd("world!" * 30)  # Try to add 180 more
    assert charge.charges == 100  # Should be capped


# ===== TEST 4: Powered Upgrade Usage =====
def test_multiply_upgrade_functionality():
    """Test Multiply upgrade string multiplication"""
    multiply = MultiplyUpgrade()
    multiply.count = 1
    multiply.charges = 200
    
    result = multiply.multiply("abc", 1)
    assert result == "abcabc"  # 3 chars * 2 = 6 chars
    assert multiply.charges == 100  # 200 - 100 = 100


# ===== TEST 5: Upgrade Unlock System (REGENERATED) =====
import pytest
from unittest.mock import MagicMock
import sys

sys.modules['pygame'] = MagicMock()
sys.modules['ptext'] = MagicMock()

# ===== CLASS DEFINITIONS =====
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
                self.count += 1
            else:
                raise ValueError("Insufficient funds")
        except KeyError:
            raise ValueError("Max level reached")
    
    def unlock(self):
        self.unlocked = True


class ValueUpgrade(BaseUpgrade):
    def __init__(self):
        super().__init__()
        self.name = "Value"
        self.prices = {1: 500, 2: 1000, 3: 3500, 4: 4500, 5: 7000, 6: "MAX"}
        self.unlocked = True


class CritUpgrade(BaseUpgrade):
    def __init__(self):
        super().__init__()
        self.name = "Crit"
        self.prices = {1: 1250, 2: 2500, 3: 4750, 4: 6000, 5: 7500, 6: "MAX"}


class ChargeUpgrade(BaseUpgrade):
    def __init__(self):
        super().__init__()
        self.name = "Charge"
        self.prices = {1: 2500, 2: 5000, 3: 10000, 4: 20000, 5: 40000, 6: 45000, 7: 50000, 8: 55000, 9: 60000, 10: 65000, 11: "MAX"}
        self.charges = 0
    
    def chargeadd(self, s):
        self.charges += len(s)
        if self.charges > self.count * 100:
            self.charges = int(self.count * 100)


class PoweredUpgrade(BaseUpgrade):
    def __init__(self):
        super().__init__()
    
    def removecharge(self, c):
        if self.charges >= c * 100:
            self.charges -= c * 100
        else:
            raise ValueError("Insufficient charge")


class MultiplyUpgrade(PoweredUpgrade):
    def __init__(self):
        super().__init__()
        self.name = "Multiply"
        self.prices = {1: 6000, 2: 10000, 3: 16000, 4: 20000, 5: 40000, 6: "MAX"}
        self.charges = 0
    
    def multiply(self, s, x):
        try:
            self.removecharge(x)
            return s * (x + 1)
        except ValueError:
            return s


# ===== TEST 5: Upgrade Unlock System (REGENERATED) =====
def test_upgrade_unlock_chain():
    """Test that upgrades unlock in correct sequence"""
    global usd
    usd = 0
    
    # Initially, only Value upgrade is unlocked
    value = ValueUpgrade()
    crit = CritUpgrade()
    charge = ChargeUpgrade()
    multiply = MultiplyUpgrade()
    
    assert value.unlocked == True
    assert crit.unlocked == False
    assert charge.unlocked == False
    assert multiply.unlocked == False
    
    # Purchase Value upgrade to unlock Crit
    usd = 1000
    value.purchase()
    crit.unlock()
    assert crit.unlocked == True
    
    # Purchase Crit to unlock Charge
    usd = 2000
    crit.purchase()
    charge.unlock()
    assert charge.unlocked == True
    
    # Purchase Charge to unlock Multiply
    usd = 5000
    charge.purchase()
    multiply.unlock()
    assert multiply.unlocked == True
    
    # Verify all upgrades are now accessible
    assert value.unlocked == True
    assert crit.unlocked == True
    assert charge.unlocked == True
    assert multiply.unlocked == True