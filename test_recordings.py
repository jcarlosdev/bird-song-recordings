import pytest
from requests import HTTPError

import config
import test_data
from recordings import get_api_data, get_recordings, count_recordings_by_type, is_recording_longer_than


def mock_multi_page_api(mocker) -> None:
    """Create an API mock that contains two results pages."""
    mocker.get(config.API_URL, json=test_data.api_data_page_1, status_code=200)
    mocker.get(f'{config.API_URL}&page=2', json=test_data.api_data_page_2, status_code=200)


def mock_single_page_api(mocker) -> None:
    """Create an API mocj that contains only one results page."""
    mocker.get(config.API_URL, json=test_data.api_data_single_page, status_code=200)


def mock_api_error(mocker) -> None:
    """Create an API mock that returns a Bad Request status code."""
    mocker.get(config.API_URL, json={}, status_code=400)


def mock_empty_api(mocker) -> None:
    """Create an API mock that returns an empty response."""
    mocker.get(config.API_URL, json=test_data.api_data_empty_response, status_code=200)


def test_get_api_data_multi_page(requests_mock) -> None:
    """Validate that correct data is returned from all result pages."""
    mock_multi_page_api(requests_mock)
    data = get_api_data(config.API_URL)
    assert list(data) == test_data.api_expected_data_multi_page


def test_get_api_data_single_page(requests_mock) -> None:
    """Validate that correct data is returned from a single result page."""
    mock_single_page_api(requests_mock)
    data = get_api_data(config.API_URL)
    assert list(data) == test_data.api_expected_data_single_page


def test_get_api_data_status_code_not_200(requests_mock) -> None:
    """Validate that an exception is raised when a non 200 (in this case Bad Request) status code is returned"""
    mock_api_error(requests_mock)
    with pytest.raises(HTTPError):
        data = get_api_data(config.API_URL)
        list(data)


def test_get_api_data_empty_response(requests_mock) -> None:
    """Validate that fetching data from an empty response works properly."""
    mock_empty_api(requests_mock)
    data = get_api_data(config.API_URL)
    assert list(data) == []


def test_get_recordings(requests_mock) -> None:
    """Validate that recordings data is correctly fecthed and filtered by length greater than one minute."""
    mock_multi_page_api(requests_mock)
    recordings = get_recordings(config.API_URL, config.MIN_RECORDING_LENGTH_IN_MINUTES)
    assert recordings == test_data.expected_recordings


def test_get_recordings_empty_response(requests_mock) -> None:
    """Validate that recordings data is empty when the API returns an empty response."""
    mock_empty_api(requests_mock)
    recordings = get_recordings(config.API_URL, config.MIN_RECORDING_LENGTH_IN_MINUTES)
    assert recordings == []


def test_is_recording_longer_than_one_minute() -> None:
    """Validate that a recording with length of 1:01 minutes is matched."""
    input = '1:01'
    result = is_recording_longer_than(input, config.MIN_RECORDING_LENGTH_IN_MINUTES)
    assert result == True


def test_is_recording_less_than_one_minute() -> None:
    """Validate that a recording with length of 0:45 minutes is not matched."""
    input = '0:45'
    result = is_recording_longer_than(input, config.MIN_RECORDING_LENGTH_IN_MINUTES)
    assert result == False


def test_is_recording_equals_one_minute() -> None:
    """Validate that a recording with length of 1:00 minutes is not matched."""
    input = '1:00'
    result = is_recording_longer_than(input, config.MIN_RECORDING_LENGTH_IN_MINUTES)
    assert result == False
    

def test_count_recordings_by_type() -> None:
    """Validate that recording types are grouped and counted correctly."""
    recordings_by_type = count_recordings_by_type(test_data.api_expected_data_multi_page)
    assert recordings_by_type == test_data.expected_recordings_by_type

def test_count_recordings_by_type_empty_input() -> None:
    """Validate that recording types counting returns an empty response when provided an empty input."""
    recordings_by_type = count_recordings_by_type([])
    assert recordings_by_type == {}
