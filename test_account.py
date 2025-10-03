# test_account.py

import pytest
from Account_class import account

def test_account_creation():
    acc = account("TestUser", 1000)
    assert acc.holder_name == "TestUser"
    assert acc.balance == 1000
    assert isinstance(acc.account_number, int)

def test_deposit():
    acc = account("TestUser", 1000)
    acc.deposit(500)
    assert acc.balance == 1500

def test_withdraw_success():
    acc = account("TestUser", 1000)
    acc.withdraw(400)
    assert acc.balance == 600

def test_withdraw_insufficient_funds(capfd):
    acc = account("TestUser", 1000)
    acc.withdraw(1500)
    out, _ = capfd.readouterr()
    assert "Fonds insuffisants" in out
    assert acc.balance == 1000
