import os
from datetime import datetime, timezone

import boto3


def lambda_handler(event, _context):
    order_id = event["orderId"]
    item = {
        "orderId": order_id,
        "status": event["status"],
        "updatedAt": datetime.now(timezone.utc).isoformat(),
        "customer": event.get("customer", {}),
        "total": str(event.get("total", 0)),
    }
    if event.get("customerMessage"):
        item["customerMessage"] = event["customerMessage"]
    boto3.resource("dynamodb").Table(os.environ["ORDERS_TABLE"]).put_item(Item=item)
    return {"orderId": order_id, "status": item["status"], "customerMessage": item.get("customerMessage")}
