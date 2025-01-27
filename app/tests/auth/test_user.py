from unittest import mock

import bcrypt
import pytest

from app.auth.schemas import UserIn, UserRegister, User
from app.auth.services import create_access_token, get_password_hash, authenticate_user, get_user, register_user, \
    verify_password, create_refresh_token, authorize_user
from app.common import Database


def test_get_password_hash():
    password = "my_password"
    hashed_password = get_password_hash(password)
    assert bcrypt.checkpw(password.encode(), hashed_password.encode())


def test_verify_password():
    correct_password = "my_password"
    incorrect_password = "wrong_password"
    hashed_password = get_password_hash(correct_password)

    assert verify_password(correct_password, hashed_password) is True
    assert verify_password(incorrect_password, hashed_password) is False


@pytest.mark.asyncio
async def test_register_user():
    user = UserRegister(username="test_user", password="test_password", confirm_password="test_password")
    mock_db = mock.MagicMock(spec=Database)
    mock_add_user = mock.AsyncMock()

    with mock.patch('app.auth.repository.add_user', mock_add_user):
        await register_user(user, mock_db)

    mock_add_user.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_user():
    mock_db = mock.MagicMock(spec=Database)
    mock_get_user_by_username = mock.AsyncMock(return_value={'username': 'test_user'})

    with mock.patch('app.auth.repository.get_user_by_username', mock_get_user_by_username):
        user = await get_user("test_user", mock_db)

    mock_get_user_by_username.assert_awaited_once()
    assert user['username'] == 'test_user'


@pytest.mark.asyncio
async def test_authenticate_user():
    user_data = UserIn(username="test_user", password="test_password")
    mock_db = mock.MagicMock(spec=Database)
    mock_get_user = mock.AsyncMock(
        return_value={'username': 'test_user', 'password': get_password_hash("test_password")})

    with mock.patch('app.auth.services.get_user', mock_get_user):
        result = await authenticate_user(user_data, mock_db)

    mock_get_user.assert_awaited_once()
    assert result['username'] == 'test_user'


@pytest.mark.asyncio
async def test_create_access_token():
    data = {"sub": "test_user"}
    token = await create_access_token(data)
    assert isinstance(token, str)


@pytest.mark.asyncio
async def test_create_refresh_token():
    data = {"sub": "test_user"}
    token = await create_refresh_token(data)
    assert isinstance(token, str)


@pytest.mark.asyncio
async def test_authorize_user():
    user = User(username="test_user", password=get_password_hash("test_password"))
    mock_db = mock.MagicMock(spec=Database)
    mock_update_user_last_login = mock.MagicMock()

    with mock.patch('your_module.update_user_last_login', mock_update_user_last_login):
        result = await authorize_user(user, mock_db)

    mock_update_user_last_login.assert_called_once()
    assert 'access_token' in result
    assert 'refresh_token' in result
