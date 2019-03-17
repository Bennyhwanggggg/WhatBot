# WhatBot Backend

## Testing
Pytest is the chosen testing module for our backend. All test cases are inside the `tests` folder.

### How to test?
First ensure that pytest is installed. If not use:
```
pip install pytest
```
To test you can use either the call script that has being set up in this root folder
```
./start_test.sh
```
or call pytest in the command line in this root folder
```
pytest
```
To specify a specific test case:
```
pytest -k {test case name}
```