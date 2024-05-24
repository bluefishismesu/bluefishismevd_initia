# peerscheck.py
# PEERS Checker Tool

This Python tool is designed to check the connectivity and response times of a list of IP addresses and ports provided in a text file. It will then keep the top 40 connections with the lowest response times and save them to a new file.

## Features

- Checks connectivity to a list of IP addresses and ports.
- Measures the response time for each connection.
- Logs the progress and results.
- Keeps the top 40 connections with the lowest response times.
- Saves the filtered connections to a new file.

## Requirements

- Python 3.x
- Requests library
- Logging library

You can install the required library using pip:

```bash
pip install requests


## Usage

1. Clone the repository or download the script.
2. Run the script:

```bash
python connection_checker.py



## Main Functions

### `check_connection(ip, port, timeout=5)`

Checks if the given IP and port can be connected to and measures the connection time.

**Parameters:**
- `ip` (str): IP address
- `port` (int): Port number
- `timeout` (int, optional): Timeout in seconds. Default is 5.

**Returns:**
- `bool`: Whether the connection is successful
- `float`: Connection time in seconds

### `parse_and_check(url)`

Parses the file from the URL and checks the connectivity and response time of each IP and port.

**Parameters:**
- `url` (str): URL of the file to be parsed

**Returns:**
- `list`: List of successfully connected IP and port with their response times

### `save_top_connections(connections, output_filename, top_n=40)`

Saves the top N connections with the lowest response times to the specified file.

**Parameters:**
- `connections` (list): List of IP and port with their response times
- `output_filename` (str): Output file name
- `top_n` (int, optional): Number of connections to save. Default is 40.
