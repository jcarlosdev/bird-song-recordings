# API test response with a single page of results
api_data_single_page = {
    'page': 1,
    'numPages': 1,
    'recordings': [
        {
            'id': '257429',
            'type': 'song',
            'length': '0:13'
        },
        {
            'id': '257430',
            'type': 'song',
            'length': '1:13'
        },
        {
            'id': '257431',
            'type': 'call',
            'length': '1:00'
        }
    ]
}

# API test response for the first page in a multi-results response
api_data_page_1 = {
    'page': 1,
    'numPages': 2,
    'recordings': [
        {
            'id': '257429',
            'type': 'song',
            'length': '0:13'
        },
        {
            'id': '257430',
            'type': 'song',
            'length': '1:49'
        },
        {
            'id': '257431',
            'type': 'call',
            'length': '1:00'
        }
    ]
}

# API test response for the second page in a multi-results response
api_data_page_2 = {
    'page': 2,
    'numPages': 2,
    'recordings': [
        {
            'id': '257429',
            'type': 'call',
            'length': '11:11'
        },
        {
            'id': '257430',
            'type': 'duet',
            'length': '5:27'
        },
        {
            'id': '257431',
            'type': 'subsong',
            'length': '21:00'
        }
    ]
}

# Expected recordings data when processing the multi-page response
api_expected_data_multi_page = [
    {
        'id': '257429',
        'type': 'song',
        'length': '0:13'
    },
    {
        'id': '257430',
        'type': 'song',
        'length': '1:49'
    },
    {
        'id': '257431',
        'type': 'call',
        'length': '1:00'
    },
    {
        'id': '257429',
        'type': 'call',
        'length': '11:11'
    },
    {
        'id': '257430',
        'type': 'duet',
        'length': '5:27'
    },
    {
        'id': '257431',
        'type': 'subsong',
        'length': '21:00'
    }
]

# Expected recordings data when processing the single page response
api_expected_data_single_page = [
    {
        'id': '257429',
        'type': 'song',
        'length': '0:13'
    },
    {
        'id': '257430',
        'type': 'song',
        'length': '1:13'
    },
    {
        'id': '257431',
        'type': 'call',
        'length': '1:00'
    }
]

# API test response for empty results
api_data_empty_response = {
    'numRecordings': '0',
    'numSpecies': '0',
    'page': 1,
    'numPages': 1,
    'recordings': []
}

# Expected recording counts after processing a multi-page response
expected_recordings_by_type = {
    'song': 2,
    'call': 2,
    'duet': 1,
    'subsong': 1
}

# Expected recordings after processing a multi-page response and filtering recordings
# whose length is greater than one minute
expected_recordings = [
    {
        'id': '257430',
        'type': 'song',
        'length': '1:49'
    },
    {
        'id': '257429',
        'type': 'call',
        'length': '11:11'
    },
    {
        'id': '257430',
        'type': 'duet',
        'length': '5:27'
    },
    {
        'id': '257431',
        'type': 'subsong',
        'length': '21:00'
    }
]
