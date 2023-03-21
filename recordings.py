import requests

from collections import defaultdict
from collections.abc import Iterator


def get_api_data(url: str) -> Iterator[dict]:  
    response = requests.get(url)
    response.raise_for_status()    
        
    data = response.json()
    for recording in data.get('recordings'):
        yield recording

    num_pages = data.get('numPages')        
    
    if(num_pages > 1):
        for num_page in range(2, num_pages + 1):                
            response = requests.get(f'{url}&page={num_page}')
            response.raise_for_status()            

            data = response.json()

            for recording in data.get('recordings'):
                yield recording
                            

def is_recording_longer_than(rec_length: str, len_mins: int) -> bool:
    try:
        minutes, seconds = rec_length.split(':')
        total_length = int(minutes) * 60 + int(seconds)
    except ValueError:
        raise ValueError(f'Invalid input: {rec_length}')
    
    return total_length > len_mins * 60


def get_recordings(url: str, len_mins: int) -> list[dict]:
    data = get_api_data(url)
    return [d for d in data if is_recording_longer_than(d.get('length'), len_mins)]


def count_recordings_by_type(recordings: list[dict]) -> dict:
    count_by_type = defaultdict(int)
    
    try:
        for recording in recordings:
            recording_type = recording.get('type')        
            count_by_type[recording_type] += 1

        return dict(count_by_type)
    except ValueError:
        raise ValueError(f'Invalid input: {recordings}')
