This project covers the fundamentals of unit testing and integration testing in Python, using the unittest framework, parameterized, and unittest.mock.

📚 Learning Objectives
By the end of this project, you should be able to:

✅ Explain the difference between unit tests and integration tests

✅ Use mocking, parameterization, and fixtures

✅ Write and run tests using Python’s built-in unittest framework

✅ Apply test-driven development concepts

✅ Understand the purpose and structure of memoization

🧪 Project Structure
File	Description
utils.py	Contains utility functions like access_nested_map, get_json, and memoize
client.py	Defines GithubOrgClient, which fetches data from the GitHub API
fixtures.py	Contains sample GitHub API responses used for mocking
test_utils.py	Unit tests for utils.py, using parameterized and mock
test_client.py	Unit and integration tests for client.py, using fixtures and mocking

🧪 Types of Testing
✅ Unit Testing
Tests individual functions in isolation.

Focuses only on the logic within the function

Mocks any dependencies (e.g., network, DB)

Example: access_nested_map, memoize

✅ Integration Testing
Tests the interaction between multiple components.

End-to-end execution paths

Mocks only low-level external calls (e.g., HTTP)

Example: GitHub API client (GithubOrgClient)

🧰 Tools & Libraries
unittest

unittest.mock

parameterized

Install dependencies:

bash
Copy
Edit
pip install parameterized
🚀 Run Tests
You can run tests using:

bash
Copy
Edit
python3 -m unittest 0x03-Unittests_and_integration_tests/test_utils.py
python3 -m unittest 0x03-Unittests_and_integration_tests/test_client.py
To run all tests in the directory:

bash
Copy
Edit
python3 -m unittest discover 0x03-Unittests_and_integration_tests
🧼 Style & Documentation Requirements
All code follows Pycodestyle (v2.5)

Every file must be executable

Each module, class, and function is documented with a complete sentence

All functions and coroutines are type-annotated

✅ Example: Unit Test for access_nested_map
python
Copy
Edit
@parameterized.expand([
    ({"a": 1}, ("a",), 1),
    ({"a": {"b": 2}}, ("a",), {"b": 2}),
    ({"a": {"b": 2}}, ("a", "b"), 2),
])
def test_access_nested_map(self, nested_map, path, expected):
    self.assertEqual(access_nested_map(nested_map, path), expected)
