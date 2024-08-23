import os
import subprocess
import jwt
import pytest
from datetime import datetime, timezone, timedelta

from server import generate_ssl_cert, verify_token, SECRET_KEY


def test_generate_ssl_cert_files_exist(mocker):
    if os.getenv("CI", "false") == "true":
        print("Skipping SSL generation in CI environment")
        return

    mocker.patch("os.path.exists", returns_value=True)

    mock_run = mocker.patch("subprocess.run")
    mock_remove = mocker.patch("os.remove")

    cert_path = "/path/to/cert.pem"
    key_path = "/path/to/key.pem"
    config_path = "/path/to/config.cnf"

    generate_ssl_cert(cert_path, key_path, config_path)

    mock_run.assert_not_called()
    mock_remove.assert_not_called()


def test_generate_ssl_cert_files_not_exist(mocker):
    if os.getenv("CI", "false") == "true":
        print("Skipping SSL generation in CI environment")
        return

    mocker.patch(
        "os.path.exists",
        side_effect=lambda path: False
        if path in ["/path/to/cert.pem", "/path/to/key.pem"]
        else True,
    )

    mock_run = mocker.patch("subprocess.run")
    mock_remove = mocker.patch("os.remove")

    cert_path = "/path/to/cert.pem"
    key_path = "/path/to/key.pem"
    config_path = "/path/to/config.cnf"

    generate_ssl_cert(cert_path, key_path, config_path)

    assert mock_run.call_count == 3

    mock_remove.assert_called_once_with("csr.pem")


def test_subprocess_failure(mocker):
    if os.getenv("CI", "false") == "true":
        print("Skipping SSL generation in CI environment")
        return

    mocker.patch(
        "os.path.exists",
        side_effect=lambda path: False
        if path in ["/path/to/cert.pem", "/path/to/key.pem"]
        else True,
    )

    mocker.patch(
        "subprocess.run", side_effect=subprocess.CalledProcessError(1, "openssl")
    )
    mock_remove = mocker.patch("os.remove")

    cert_path = "/path/to/cert.pem"
    key_path = "/path/to/key.pem"
    config_path = "/path/to/config.cnf"

    with pytest.raises(subprocess.CalledProcessError):
        generate_ssl_cert(cert_path, key_path, config_path)

    mock_remove.assert_not_called()

def test_generate_token():
    exp_condition = datetime.now(tz=timezone.utc) + timedelta(hours=1)

    exp_time = int(exp_condition.timestamp())

    pay_load = {"user_id": 123, "exp": exp_time}
    token = jwt.encode(pay_load, SECRET_KEY, algorithm="HS256")

    decoded = jwt.decode(
        token, SECRET_KEY, algorithms=["HS256"], options={"verify_exp": False}
    )

    assert decoded["user_id"] == 123
    assert decoded["exp"] == exp_time


def test_verify_token_valid():
    payload = {
        "user_id": 123,
        "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=5),
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    user_id = verify_token(token)

    assert user_id == 123


def test_verify_token_invalid():
    invalid_token = "this.is.not.a.jwt.token"

    result = verify_token(invalid_token)

    assert result == "Invalid token"


def test_verify_token_unexpected_error(mocker):
    mocker.patch("server.jwt.decode", side_effect=Exception("Unexpected error"))

    token = jwt.encode(
        {"user_id": 123, "exp": datetime.now(tz=timezone.utc) + timedelta(minutes=5)},
        SECRET_KEY,
        algorithm="HS256",
    )

    result = verify_token(token)

    assert result is None
