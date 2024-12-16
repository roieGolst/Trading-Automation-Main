import pytest
from app.db.RedisDB import RedisDB, RedisConnectionParams

from app.service.grpc.model.types import Brokerage


@pytest.fixture
def redis_db():
    # Set up the RedisDB instance and clear the database before each test
    connection_params = RedisConnectionParams(host="localhost", port=6379)
    db_instance = RedisDB(connection_params)
    db_instance.init()
    db_instance._RedisDB__redis.flushdb()  # Clear Redis for clean start
    return db_instance

def test_create_group(redis_db):
    group_name = "TestGroup"
    redis_db.create_group(group_name)
    assert group_name in redis_db.get_all_groups()

def test_create_account(redis_db):
    # Create group and account, and assert that the account is in the group
    group_name = "TestGroup"
    account_name = "TestAccount"
    details = {"email": "test@example.com"}
    redis_db.create_group(group_name)
    redis_db.add_account(group_name, account_name, Brokerage.Chase, details)
    assert account_name in redis_db.get_group_accounts(group_name)

def test_get_account(redis_db):
    # Create an account and then retrieve it
    group_name = "TestGroup"
    account_name = "TestAccount"
    details = {"email": "test@example.com"}
    redis_db.create_group(group_name)
    redis_db.add_account(
        group_name=group_name,
        account_name=account_name,
        brokerage=Brokerage.Chase,
        account_details=details
    )

    account_data = redis_db.get_account(account_name)
    assert account_data.get("account_name") == account_name

def test_deactivate_account(redis_db):
    # Delete an account and ensure it's no longer in the group
    group_name = "TestGroup"
    account_name = "acc123"
    redis_db.create_group(group_name)
    redis_db.add_account(group_name, account_name, Brokerage.Chase, {})
    redis_db.deactivate_account(account_name)
    assert "0" == redis_db.get_account(account_name).get("status")

def test_get_account_details(redis_db):
    # Retrieve account details and check a field
    group_name = "TestGroup"
    account_name = "TestAccount"
    details = {"email": "test@example.com"}
    redis_db.create_group(group_name)
    redis_db.add_account(
        group_name=group_name,
        brokerage=Brokerage.Chase,
        account_name=account_name,
        account_details=details
    )
    retrieved_details = redis_db.get_account_details(account_name)
    assert retrieved_details.get("email") == "test@example.com"