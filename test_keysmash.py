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


#AI generated tests
