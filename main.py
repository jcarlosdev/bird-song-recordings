import config
import recordings


data = recordings.get_recordings(config.API_URL, config.MIN_RECORDING_LENGTH_IN_MINUTES)

print(f'Total results: {len(data)}')

print('Recordings by type:')
recordings_by_type = recordings.count_recordings_by_type(data)
for k, v in recordings_by_type.items():
    print(f'{k}: {v}')
