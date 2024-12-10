# Password Manager

This project is a simple and secure password manager built using Python's `Tkinter`, `cryptography`, and `MySQL`. It allows users to generate strong passwords, save them securely in a MySQL database, retrieve them when needed, and delete passwords.

## Features

- **Password Generation**: Generates random passwords with a mix of lowercase, uppercase, digits, and special characters.
- **Password Encryption**: Utilizes `cryptography.fernet` for encrypting passwords before storing them in the database.
- **Password Decryption**: Decrypts passwords when needed and displays them securely.
- **Database Management**: Saves, fetches, and deletes passwords from a MySQL database.
- **User Interface**: Simple and interactive GUI built using `Tkinter`.

## Requirements


- `cryptography` library (for encryption and decryption)
- `mysql-connector-python` library (for interacting with the MySQL database)


### Install dependencies

You can install the required libraries using `pip`:

```bash
pip3 install cryptography mysql-connector-python
```

### Key Generation
To ensure secure encryption, a secret key file key.key is required. You can generate this using the generate_key.py
> **Note:** Make sure to generate the `key.key` file before running the application.


### Recording

https://github.com/user-attachments/assets/1be22a9c-3c12-49c6-9b8c-d2b99ea9ff05




