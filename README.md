# alx-backend-python
📁 0x03-Unittests_and_integration_tests
This directory contains unit and integration tests for utility functions used in the project.

✅ test_utils.py
This file contains unit tests for the access_nested_map function located in utils.py.

Functionality Tested: Accessing nested dictionary values using a tuple of keys.

Testing Approach:

Uses unittest for structuring tests.

Uses parameterized to test multiple input/output pairs.

Test Cases Include:

Retrieving a direct key.

Accessing nested dictionaries.

Multi-level key paths.

Example test case:

python
Copy
Edit
({"a": {"b": 2}}, ("a", "b")) → returns 2
🧪 Run Tests
bash
Copy
Edit
python3 -m unittest discover 0x03-Unittests_and_integration_tests
Make sure you have parameterized installed:

bash
Copy
Edit
pip install parameterized