import pytest
from exchange_money import calculate_cross_exchange, check_aml_limit
from Cash_desk.add_money import calculate_new_balance
from Cash_desk.withdraw_money import calculate_withdrawal


def test_calculate_withdrawal():
    # Arrange
    current_balance = 100.0
    withdraw_amount = 30.0
    
    # Act
    new_balance = calculate_withdrawal(current_balance, withdraw_amount)
    
    # Assert
    assert new_balance == 70.0
    
    
def test_calculate_withdrawal_insufficient_funds():
    # Arrange
    current_balance = 100.0
    withdraw_amount = 150.0
    
    # Act & Assert
    with pytest.raises(ValueError, match="Nedostatečný zůstatek v pokladně."):
        calculate_withdrawal(current_balance, withdraw_amount)
        
        
def test_calculate_withdrawal_negative_amount():
    # Arrange
    current_balance = 100.0
    withdraw_amount = -20.0
    
    # Act & Assert
    with pytest.raises(ValueError, match="Částka musí být vyšší než 0."):
        calculate_withdrawal(current_balance, withdraw_amount)


def test_calculate_new_balance():
    
    # Arrange
    current_balance = 100.0
    deposit_amount = 50.0
    
    # Act
    new_balance = calculate_new_balance(current_balance, deposit_amount)
    
    # Assert
    assert new_balance == 150.0


def test_calculate_new_balance_negative():
    # Arrange
    current_balance = 100.0
    deposit_amount = -20.0
    
    # Act & Assert (u chyb se to píše dohromady pomocí context managera)
    with pytest.raises(ValueError, match="Částka musí být vyšší než 0."):
        calculate_new_balance(current_balance, deposit_amount)


def test_exchange_eur_to_usd():
    # Arrange
    amount = 100
    rate_buy = 25.0
    rate_sell = 20.0
    
    # Act - Tady voláme tu správnou malou funkci!
    result = calculate_cross_exchange(amount, rate_buy, rate_sell, "USD")
    
    # Assert
    assert result == 125.0

def test_exchange_to_czk_rounding():
    # EN: Testing that exchange to CZK rounds to whole numbers
    # CZ: Testujeme, že převod do CZK zaokrouhluje
    result = calculate_cross_exchange(10, 25.45, 1.0, "CZK")
    assert result == 255.0

def test_exchange_negative_amount():
    # EN: Testing that negative amount raises an error
    # CZ: Testujeme, že záporná částka vyhodí chybu
    with pytest.raises(ValueError, match="Částka musí být kladná."):
        calculate_cross_exchange(-100, 25, 20, "USD")

def test_aml_trigger():
    # EN: Testing AML function (1000 EUR limit)
    # CZ: Testujeme AML funkci (1000 EUR limit)
    # EN: 25000 CZK / 25 (EUR rate) = 1000 EUR -> should return True
    # CZ: 25000 CZK / 25 (EUR kurz) = 1000 EUR -> mělo by vrátit True
    fake_rates = [{"name": "EUR", "sell_rate": 25.0}]
    assert check_aml_limit(1000, 25.0, fake_rates) is True