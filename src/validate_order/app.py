def lambda_handler(event, _context):
    required = ("orderId", "items", "total", "deliveryAddress")
    missing = [field for field in required if not event.get(field)]
    is_valid = not missing and isinstance(event["items"], list) and event["total"] > 0
    return {**event, "isValid": is_valid, "validationErrors": missing}
