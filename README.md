# Ethereum Key Generator

This Django-based application allows you to generate Ethereum keys (public and private keys) and convert a given public key to an Ethereum address.

## Features

- **Generate Random Keys**: Generates a new Ethereum private key and its corresponding public key and Ethereum address.
- **Convert Public Key to Ethereum Address**: Converts a given public key (in hexadecimal format) into an Ethereum address.
- **Download Keys**: Download the generated keys as a `.txt` file.
- **Clear Keys**: Clears all generated keys stored in the session.

## Requirements

- Python 3.6+
- Django 3.0+
- eth-utils
- eth-hash
- ecdsa

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/ethereum-key-generator.git
   cd ethereum-key-generator
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver
   ```

## Usage

### Generate Random Keys:
Click the "Generate Random Keys" button to create a new set of keys (private key, public key, and Ethereum address).

### Convert Key:
Enter a public key in the input field and click "Convert Key" to get the corresponding Ethereum address.

### Download Keys:
After generating keys, you can download them as a `.txt` file by clicking the "Download Keys" button.

### Clear Keys:
Click the "Clear Keys" button to clear all stored keys in the session.
