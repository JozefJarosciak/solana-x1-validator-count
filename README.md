# Blockchain Validator Count Script
=============================

A Python script to fetch and display active and inactive validator counts for Solana and X1 blockchains.

## Features
------------

* Supports multiple blockchain networks (Solana, X1)
* Calculates active and inactive validator counts for each network
* Displays results in a formatted table using the `tabulate` library
* Implements retry logic to handle temporary connection issues or API errors

## Example Output
-------------------

The script will display a table with active and inactive validator counts for each network:
![image](https://github.com/user-attachments/assets/66e79e68-9334-4709-993f-c1d6a7ed4e9a)

Note: The actual values will depend on the current validator counts for each network.

## Requirements
------------

* Python 3.x (tested with 3.9.x)
* RPC client libraries for Solana (`solana-rpc-api`) and X1 (`x1-rpc-client`)
* `pandas` library for data manipulation
* `tabulate` library for formatting tables

## Usage
--------

1. Clone this repository to your local machine.
2. Run the script using `python blockchain-validator-count.py`.


## Contributing
------------

Contributions are welcome! If you'd like to add support for additional blockchains or fix any issues, feel free to submit a pull request.

## License
--------

This script is released under the MIT license. 

