git checkout -b log_feature
git rebase -i HEAD~6
git log --oneline > SOLUTION_4.md




e9c4421 restructured code
b00017b Refactored status code logic for daily records from July 1st to July 7th and added endpoint for /status_codes
199f044 URL /status_codes added
775352a fixed:TypeError: bytes-like object
6c793f0 Ip match and pending error TypeError: bytes-like object
1ab537b Initial commit
