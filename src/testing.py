import os
import subprocess
import pytest
import pytest_mock


from server import generate_ssl_cert

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