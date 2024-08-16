import os
import subprocess
import jwt
import pytest
import pytest_mock
import datetime

from server import generate_ssl_cert,generate_token,verify_token,SECRET_KEY



def test_generate_ssl_cert_files_exist(mocker):
    # Mock os.path.exists to return True for both cert and key paths
    mocker.patch('os.path.exists',returns_value=True)

   # Mock subprocess.run and os.remove
    mock_run=mocker.patch('subprocess.run')
    mock_remove=mocker.patch('os.remove')

    cert_path = '/path/to/cert.pem'
    key_path = '/path/to/key.pem'
    config_path = '/path/to/config.cnf'

    generate_ssl_cert(cert_path,key_path,config_path)

    mock_run.assert_not_called()
    mock_remove.assert_not_called()

def test_generate_ssl_cert_files_not_exist(mocker):
    mocker.patch('os.path.exists',side_effect= lambda path: False if path in ['/path/to/cert.pem','/path/to/key.pem'] else True)

    mock_run = mocker.patch('subprocess.run')
    mock_remove = mocker.patch('os.remove')

    cert_path = '/path/to/cert.pem'
    key_path = '/path/to/key.pem'
    config_path = '/path/to/config.cnf'

    generate_ssl_cert(cert_path, key_path, config_path)

    assert mock_run.call_count==3

    mock_remove.assert_called_once_with('csr.pem')


def test_subprocess_failure(mocker):
    # Mock os.path.exists to return False for cert and key paths, True otherwise
    mocker.patch('os.path.exists',
                 side_effect=lambda path: False if path in ['/path/to/cert.pem', '/path/to/key.pem'] else True)

    # Mock subprocess.run to raise an exception
    mock_run = mocker.patch('subprocess.run', side_effect=subprocess.CalledProcessError(1, 'openssl'))
    mock_remove = mocker.patch('os.remove')

    cert_path = '/path/to/cert.pem'
    key_path = '/path/to/key.pem'
    config_path = '/path/to/config.cnf'

    # Expect the function to raise a CalledProcessError
    with pytest.raises(subprocess.CalledProcessError):
        generate_ssl_cert(cert_path, key_path, config_path)

    # Assert that os.remove was never called
    mock_remove.assert_not_called()

    #JWT TESTING

def test_generate_token():
    exp_condition=datetime.datetime.utcnow() + datetime.timedelta(hours=1)

    exp_time=int(exp_condition.timestamp())

    pay_load= {
            "user_id": 123,
            "exp":exp_time
        }
    token=jwt.encode(pay_load,SECRET_KEY, algorithm="HS256")

    decoded =jwt.decode(token,SECRET_KEY,algorithms=['HS256'],options={"verify_exp": False})

    assert decoded["user_id"]==123
    assert decoded["exp"]==exp_time


def test_verify_token_valid():
    payload = {
        "user_id": 123,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    user_id = verify_token(token)

    assert user_id == 123


def test_verify_token_invalid():
    invalid_token = "this.is.not.a.jwt.token"

    result = verify_token(invalid_token)

    assert result == "Invalid token"

def test_verify_token_unexpected_error(mocker):
    # Simulate an unexpected error during jwt.decode
    mocker.patch('server.jwt.decode', side_effect=Exception("Unexpected error"))

    token = jwt.encode({"user_id": 123, "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=5)}, SECRET_KEY, algorithm="HS256")

    result = verify_token(token)

    assert result is None
