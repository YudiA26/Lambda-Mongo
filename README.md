# Lambda Function

This AWS Lambda function manages credentials for a MongoDB database. It provides an interface to retrieve the encrypted credentials for a specific database, given its domain URL.

## Function Description

The `lambda_function.py` file contains the implementation of the Lambda function. This function accepts events in the format of a JSON dictionary, where an "action" key is expected indicating the action to be performed. If the action is 1, the function will search and return the encrypted credentials for the provided domain. If the domain is not provided, or if no credentials are found for the given domain, the function will return a corresponding error.

## Dependencies

- `json`: For JSON data manipulation.
- `mongo`: Custom `mongo.py` module for interacting with MongoDB.
- `pymongo`: MongoDB client for Python.
- `cryptography`: Library for encrypting and decrypting data.

## Usage

The `lambda_handler` function is the main entry point of the Lambda function. It expects to be passed an event in the form of a JSON dictionary containing an "action" key and optionally a "domain" key. The "action" key should have a value of 1 to retrieve the encrypted database credentials for the provided domain.

## Example Usage

```python
response = lambda_handler({"action": 1, "domain": "example.com"}, None)
print(response)
