TEST_PAYLOAD = [
    (
        {"repos_url": "https://api.github.com/orgs/google/repos"},
        [
            {
                "id": 1,
                "name": "repo1",
                "license": {"key": "apache-2.0"},
            },
            {
                "id": 2,
                "name": "repo2",
                "license": {"key": "mit"},
            },
        ],
    )
]
