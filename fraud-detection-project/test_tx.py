import sys
import os

sys.path.append(os.path.dirname(__file__))

from backend.services.transaction_service import process_transaction

tx_data = {
    "sender_id": "user_123",
    "receiver_id": "merchant_456",
    "amount": 100,
    "device_id": "DEVICE_X",
    "location": "Mumbai",
}

try:
    print("Testing process_transaction...")
    result = process_transaction(tx_data)
    print("SUCCESS")
except Exception as e:
    import traceback
    with open("crash_log.txt", "w") as f:
        traceback.print_exc(file=f)
