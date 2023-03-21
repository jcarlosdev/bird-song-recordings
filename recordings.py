import requests

from collections import defaultdict
from collections.abc import Iterator


def get_api_data(url: str) -> Iterator[dict]:
    '''
    Fetch JSON data from the specified URL.    
    In order to avoid loading a big amount of data in memory, we return a generator
    to fetch the results on demand.
    
        Arguments:
            url: API URL to consume the requested data

        Returns:
            Generator to retrieve the requested data
    '''
    response = requests.get(url)
    response.raise_for_status()    
        
    data = response.json()
    for recording in data.get('recordings'):
        yield recording

    num_pages = data.get('numPages')        
    
    # Validate if the API provides pagination and fetch pages if it does
    if(num_pages > 1):
        for num_page in range(2, num_pages + 1):                
            response = requests.get(f'{url}&page={num_page}')
            response.raise_for_status()            

            data = response.json()

            for recording in data.get('recordings'):
                yield recording
                            

def is_recording_longer_than(rec_length: str, len_mins: int) -> bool:
    """
    Determines if a recording is longer than the specified duration.

        Arguments:
            rec_length: Length property from a recording
            len_mins: Duration, in minutes, used to validate if a recording length is greater

        Returns:
            True if the recording length is greater than the specified duration, False otherwise
    """
    try:
        minutes, seconds = rec_length.split(':')
        total_length = int(minutes) * 60 + int(seconds)
    except ValueError:
        raise ValueError(f'Invalid input: {rec_length}')
    
    return total_length > len_mins * 60


def get_recordings(url: str, len_mins: int) -> list[dict]:
    """
    Fetches the recordings from the specfied API URL, filtering by the provided duration

        Arguments:
            url: API URL to fetch the recordings
            len_mins: Duration, in minutes, used to filter recordings

        Returns:
            List of recordings filtered by the specified duration
    """
    data = get_api_data(url)
    return [d for d in data if is_recording_longer_than(d.get('length'), len_mins)]


def count_recordings_by_type(recordings: list[dict]) -> dict:
    """
    Counts the types of recordings from a recordings list

        Arguments:
            recordings: List of recordings to get the types from

        Returns:
            Dictionary containing the count of every recording type
    """
    count_by_type = defaultdict(int)
    
    try:
        for recording in recordings:
            recording_type = recording.get('type')        
            count_by_type[recording_type] += 1

        return dict(count_by_type)
    except ValueError:
        raise ValueError(f'Invalid input: {recordings}')
