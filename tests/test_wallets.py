import uuid

import pytest

from app.models.wallet import Wallet


@pytest.mark.asyncio
async def test_create_wallet(client):
    response = await client.post("/api/v1/wallets/")
    assert response.status_code == 201
    data = response.json()
    assert "uuid" in data
    assert "balance" in data
    assert data["balance"] == 0.0


@pytest.mark.asyncio
async def test_list_wallets_empty(client):
    response = await client.get("/api/v1/wallets/")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.asyncio
async def test_list_wallets_with_data(client, db_session):
    uuid1 = uuid.uuid4()
    uuid2 = uuid.uuid4()
    db_session.add_all(
        [
            Wallet(uuid=uuid1, balance=100),
            Wallet(uuid=uuid2, balance=200),
        ]
    )
    await db_session.commit()

    response = await client.get("/api/v1/wallets/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert {w["uuid"] for w in data} == {str(uuid1), str(uuid2)}
