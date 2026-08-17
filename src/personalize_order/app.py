import json
import os

import boto3


def lambda_handler(event, _context):
    customer = event.get("customer", {}).get("name", "cliente")
    items = ", ".join(item.get("name", "item") for item in event.get("items", []))
    prompt = f"Crie uma mensagem curta, simpática e em português para {customer}. Pedido: {items}. Não invente tempo de entrega."
    client = boto3.client("bedrock-runtime")
    response = client.converse(
        modelId=os.environ["BEDROCK_MODEL_ID"],
        messages=[{"role": "user", "content": [{"text": prompt}]}],
        inferenceConfig={"maxTokens": 120, "temperature": 0.5},
    )
    message = response["output"]["message"]["content"][0]["text"]
    return {**event, "customerMessage": message}
