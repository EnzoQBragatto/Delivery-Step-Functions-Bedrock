import importlib.util
from pathlib import Path


ROOT = Path(__file__).parents[1]


def load_handler(name):
    path = ROOT / "src" / name / "app.py"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.lambda_handler


def test_valid_order_is_accepted():
    handler = load_handler("validate_order")
    result = handler({"orderId": "1", "items": [{"name": "Pizza"}], "total": 10, "deliveryAddress": "Rua A"}, None)
    assert result["isValid"] is True


def test_missing_address_is_rejected():
    handler = load_handler("validate_order")
    result = handler({"orderId": "1", "items": [{"name": "Pizza"}], "total": 10}, None)
    assert result["isValid"] is False
    assert "deliveryAddress" in result["validationErrors"]


def test_payment_requires_explicit_approval():
    handler = load_handler("process_payment")
    result = handler({"total": 10, "payment": {"method": "PIX", "approved": False}}, None)
    assert result["paymentApproved"] is False
