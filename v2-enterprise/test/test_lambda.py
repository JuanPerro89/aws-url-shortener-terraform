import importlib
import json
import os
import sys

import boto3
import pytest
from moto import mock_aws

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


@pytest.fixture
def lm(monkeypatch):
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "test")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "test")
    monkeypatch.setenv("AWS_DEFAULT_REGION", "eu-west-3")
    with mock_aws():
        boto3.client("dynamodb").create_table(
            TableName="url-shortener",
            KeySchema=[{"AttributeName": "shortId", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "shortId", "AttributeType": "S"}],
            BillingMode="PAY_PER_REQUEST",
        )
        import lambda_function
        importlib.reload(lambda_function)
        yield lambda_function


def event(method, path="/", body=None):
    ev = {
        "requestContext": {"http": {"method": method}},
        "rawPath": path,
        "headers": {"host": "example.test"},
    }
    if body is not None:
        ev["body"] = body if isinstance(body, str) else json.dumps(body)
    return ev


def test_create_and_redirect(lm):
    r = lm.lambda_handler(event("POST", body={"url": "https://example.com"}), None)
    assert r["statusCode"] == 200
    short_id = json.loads(r["body"])["shortUrl"].rsplit("/", 1)[1]

    r2 = lm.lambda_handler(event("GET", "/" + short_id), None)
    assert r2["statusCode"] == 301
    assert r2["headers"]["Location"] == "https://example.com"


@pytest.mark.parametrize("bad", [
    "javascript:alert(1)", "hola", "", "https://", "ftp://example.com",
    "https://" + "a" * 2050 + ".com", None, 123,
])
def test_invalid_url_is_rejected(lm, bad):
    r = lm.lambda_handler(event("POST", body={"url": bad}), None)
    assert r["statusCode"] == 400


def test_missing_url_field(lm):
    assert lm.lambda_handler(event("POST", body={}), None)["statusCode"] == 400


def test_invalid_json(lm):
    assert lm.lambda_handler(event("POST", body="no soy json"), None)["statusCode"] == 400


def test_unknown_id_is_404(lm):
    assert lm.lambda_handler(event("GET", "/noexiste"), None)["statusCode"] == 404


def test_root_get_is_400(lm):
    assert lm.lambda_handler(event("GET", "/"), None)["statusCode"] == 400


def test_duplicate_id_returns_409(lm, monkeypatch):
    monkeypatch.setattr(lm, "generate_short_id", lambda: "fixed1")
    ok = lm.lambda_handler(event("POST", body={"url": "https://a.com"}), None)
    dup = lm.lambda_handler(event("POST", body={"url": "https://b.com"}), None)
    assert ok["statusCode"] == 200
    assert dup["statusCode"] == 409