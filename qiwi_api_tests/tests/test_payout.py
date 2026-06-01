import uuid
import pytest
from pydantic import ValidationError
from schemas import PaymentInfo, BalanceInfo

def test_service_availability(api_client):
    response = api_client.get_all_payments(limit=5)
    assert response.status == 200, f"Expected 200, got {response.status}: {response.text()}"
    
    data = response.json()
    assert isinstance(data, list)
    
    for item in data:
        try:
            PaymentInfo.model_validate(item)
        except ValidationError as e:
            pytest.fail(f"Response validation failed for payment item: {e}")

def test_get_balance(api_client):
    response = api_client.get_balance()
    assert response.status == 200, f"Expected 200, got {response.status}: {response.text()}"
    
    try:
        balance_info = BalanceInfo.model_validate(response.json())
    except ValidationError as e:
        pytest.fail(f"Balance response schema mismatch: {e}")
        
    assert balance_info.balance.float_value > 0.0, f"Balance is {balance_info.balance.value}, which is not > 0"

def test_payout_lifecycle(api_client):
    payment_id = str(uuid.uuid4())
    payload = {
        "recipientDetails": {
            "providerCode": "qiwi-wallet",
            "fields": {
                "account": "79123456789"
            }
        },
        "amount": {
            "value": "1.00",
            "currency": "RUB"
        },
        "source": {
            "paymentType": "NO_EXTRA_CHARGE",
            "paymentToolType": "BANK_ACCOUNT",
            "paymentTerminalType": "INTERNET_BANKING"
        }
    }
    
    create_resp = api_client.create_payment(payment_id, payload)
    assert create_resp.status == 200, f"Failed to register payout: {create_resp.text()}"
    
    try:
        created_payment = PaymentInfo.model_validate(create_resp.json())
    except ValidationError as e:
        pytest.fail(f"Created payment payload schema mismatch: {e}")
        
    assert created_payment.status.value == "READY"
    
    exec_resp = api_client.execute_payment(payment_id)
    assert exec_resp.status == 200, f"Failed to execute payout: {exec_resp.text()}"
    
    try:
        executed_payment = PaymentInfo.model_validate(exec_resp.json())
    except ValidationError as e:
        pytest.fail(f"Executed payment payload schema mismatch: {e}")
        
    assert executed_payment.status.value in ["IN_PROGRESS", "COMPLETED"]
