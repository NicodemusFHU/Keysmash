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

def test_enter_usd_value(two_lines_random, reset):
    main.input = two_lines_random.string
    main.rowcount = two_lines_random.lines
    main.value.count = 1
    main.enter()
    assert main.usd == 400

def test_enter_usd_crit(two_lines_random, reset):
    main.input = two_lines_random.string
    main.rowcount = two_lines_random.lines
    main.crit.count = 1
    main.enter()
    assert main.usd == 400

def test_enter_stats(two_lines_random, reset):
    main.input = two_lines_random.string
    main.rowcount = two_lines_random.lines
    main.charge.count = 5
    main.enter()
    assert main.added == 200 and main.addedcharges == 200 and main.previouslen == 200 and main.totalchr == 200 and main.round == 1

def test_guiprint(two_lines_random):
    main.guiprint(two_lines_random.lines, two_lines_random.string)
    assert main.previous[-1].string == two_lines_random.string and main.previous[-1].lines == two_lines_random.lines


#AI output
usd = main.usd

# ===== TEST 1: Format Function =====
def test_format():
    """Test the format function with various number ranges"""
    assert main.format(5) == "0.05"
    assert main.format(50) == "0.50"
    assert main.format(100) == "1.00"
    assert main.format(1234) == "12.34"
    assert main.format("MAX") == "MAX"


# ===== TEST 2: Upgrade Purchase Mechanics =====
def test_value_upgrade_purchase():
    """Test that Value upgrade can be purchased correctly"""
    main.usd = 500
    value = main.ValueUpgrade()
    
    assert value.count == 0
    value.purchase()
    assert value.count == 1
    assert usd == 0


# ===== TEST 3: Charge Mechanics =====
def test_charge_add_and_cap():
    """Test charge accumulation and cap limits"""
    charge = main.ChargeUpgrade()
    charge.count = 1  # Cap is 100
    
    charge.chargeadd("hello")  # 5 chars
    assert charge.charges == 5
    
    charge.chargeadd("world!" * 30)  # Try to add 180 more
    assert charge.charges == 100  # Should be capped


# ===== TEST 4: Powered Upgrade Usage =====
def test_multiply_upgrade_functionality():
    """Test Multiply upgrade string multiplication"""
    multiply = main.MultiplyUpgrade()
    multiply.count = 1
    main.charge.count = 1
    main.charge.charges = 200
    
    result = multiply.multiply("abc", 1)
    assert result == "abcabc"  # 3 chars * 2 = 6 chars
    assert main.charge.charges == 100  # 200 - 100 = 100


# ===== TEST 5: Upgrade Unlock System =====
def test_upgrade_unlock_chain():
    """Test that upgrades unlock in correct sequence"""
    global usd
    usd = 0
    
    # Initially, only Value upgrade is unlocked
    value = main.ValueUpgrade()
    crit = main.CritUpgrade()
    charge = main.ChargeUpgrade()
    multiply = main.MultiplyUpgrade()
    
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