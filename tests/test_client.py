from github_connector import client
from requests.exceptions import HTTPError

import requests
import pytest

from github_connector.custom_exceptions import ResourceNotFound

github_client = client.GitHubClient()

def test_200_ok(mocker):
    """Tests that function returns normal response"""
    
    mock_response = mocker.Mock()
    mock_response.json.return_value = {"repo": "playport"}
    
    mock_response.raise_for_status.return_value = None
    
    mocker.patch("github_connector.client.requests.request", return_value=mock_response)
    
    result = github_client.get_repo("Kenn-stack", "PlayPort")
    
    assert result == {"repo": "playport"}
    
    
def test_404_not_found(mocker):
    """Tests if function raises 404"""
    
    mock_response = mocker.Mock()
    mock_response.status_code = 404
    mock_response.json.return_value = None
    
    http_error = HTTPError("404 Error")
    http_error.response = mock_response
    
    mock_response.raise_for_status.side_effect = http_error
   
    mocker.patch("github_connector.client.requests.request", return_value=mock_response) 
    
    
    with pytest.raises(ResourceNotFound):
        github_client.get_repo("GET", "PlayBoy")
    
    
    
def test_make_request_rate_limit_retry(mocker):
    """Tests retry logic"""

    mock_429 = mocker.Mock()
    mock_429.status_code = 429
    mock_429.headers = {"Retry-After": "1"} 
    mock_429.raise_for_status.side_effect = HTTPError(response=mock_429)

    mock_200 = mocker.Mock()
    mock_200.status_code = 200
    mock_200.headers = {}
    mock_200.raise_for_status.return_value = None

    mocker.patch(
        "github_connector.client.requests.request",
        side_effect=[mock_429, mock_429, mock_200]
    )

    mocker.patch("time.sleep", return_value=None)

    response = github_client._make_request("GET", "toby")

    assert response.status_code == 200


