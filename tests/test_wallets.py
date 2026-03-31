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


@pytest.mark.asyncio
async def test_get_wallet_balance(client, db_session):
    wallet_uuid = uuid.uuid4()
    db_session.add(Wallet(uuid=wallet_uuid, balance=100))
    await db_session.commit()

    response = await client.get(f"/api/v1/wallets/{wallet_uuid}")
    assert response.status_code == 200
    assert float(response.json()["balance"]) == 100


@pytest.mark.asyncio
async def test_get_wallet_not_found(client):
    response = await client.get(f"/api/v1/wallets/{uuid.uuid4()}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Wallet not found"


@pytest.mark.asyncio
async def test_deposit(client, db_session):
    wallet_uuid = uuid.uuid4()
    db_session.add(Wallet(uuid=wallet_uuid, balance=100))
    await db_session.commit()

    response = await client.post(
        f"/api/v1/wallets/{wallet_uuid}/operation",
        json={"operation_type": "DEPOSIT", "amount": 50},
    )
    assert response.status_code == 200
    assert float(response.json()["balance"]) == 150


@pytest.mark.asyncio
async def test_withdraw_success(client, db_session):
    wallet_uuid = uuid.uuid4()
    db_session.add(Wallet(uuid=wallet_uuid, balance=100))
    await db_session.commit()

    response = await client.post(
        f"/api/v1/wallets/{wallet_uuid}/operation",
        json={"operation_type": "WITHDRAW", "amount": 30},
    )
    assert response.status_code == 200
    assert float(response.json()["balance"]) == 70


@pytest.mark.asyncio
async def test_withdraw_insufficient_funds(client, db_session):
    wallet_uuid = uuid.uuid4()
    db_session.add(Wallet(uuid=wallet_uuid, balance=10))
    await db_session.commit()

    response = await client.post(
        f"/api/v1/wallets/{wallet_uuid}/operation",
        json={"operation_type": "WITHDRAW", "amount": 50},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Insufficient funds"


@pytest.mark.asyncio
async def test_operation_wallet_not_found(client):
    response = await client.post(
        f"/api/v1/wallets/{uuid.uuid4()}/operation",
        json={"operation_type": "DEPOSIT", "amount": 10},
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Wallet not found"
