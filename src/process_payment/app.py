def lambda_handler(event, _context):
    payment = event.get("payment", {})
    approved = payment.get("approved") is True and event.get("total", 0) > 0
    return {**event, "paymentApproved": approved, "paymentMethod": payment.get("method", "UNKNOWN")}
