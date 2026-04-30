"""Test handler person-stream"""
import json
from src.handler import lambda_handler


def test_lambda_handler_success():
    event = {}
    context = {}
    response = lambda_handler(event, context)
    assert response["statusCode"] == 200
