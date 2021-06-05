from typing import Dict
from fastapi.testclient import TestClient

import pytest

from konoha.api.server import create_app


app = create_app()
client = TestClient(app)


@pytest.mark.parametrize(
    "tokenizer_params", [
        {"tokenizer": "mecab"},
        {"tokenizer": "mecab", "system_dictionary_path": "s3://konoha-demo/mecab/ipadic"},
        {"tokenizer": "sudachi", "mode": "A"},
        {"tokenizer": "sudachi", "mode": "B"},
        {"tokenizer": "sudachi", "mode": "C"},
        {"tokenizer": "sentencepiece", "model_path": "data/model.spm"},
        {"tokenizer": "kytea", "model_path": "data/model.knm"},
        {"tokenizer": "character"},
        {"tokenizer": "nagisa"},
        {"tokenizer": "janome"},
    ]
)
def test_tokenization(tokenizer_params: Dict):
    headers = {"Content-Type": "application/json"}
    params = dict(tokenizer_params, texts=["私は猫", "あなたは犬"])
    response = client.post("/api/v1/batch_tokenize", headers=headers, json=params)
    assert response.status_code == 200
    assert "tokens_list" in response.json()