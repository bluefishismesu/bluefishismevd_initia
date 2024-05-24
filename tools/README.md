# peerscheck_with_height.py
# Network Connection and Block Height Checker

This script checks the connectivity and block height of nodes specified in a given URL. It attempts to connect to each node, measures the connection time, and retrieves the latest block height if the connection is successful. The top nodes with the highest block heights are then saved to a specified file.

## Dependencies

Ensure you have the required Python libraries installed:

```bash
pip install requests
```

### Main Script Execution

The script reads the URL, processes the connections, and saves the top N connections to a file.

```python
try:
    top_n = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    output_filename = sys.argv[2] if len(sys.argv) > 2 else 'top_ips_ports.txt'
    connections = parse_and_check('https://rpc-initia-testnet.trusted-point.com/peers.txt')
    save_top_connections(connections, output_filename, top_n)
    logging.info("Processing completed successfully.")
except Exception as e:
    logging.error(f"An error occurred: {e}")
```

### Usage

Run the script with optional command-line arguments for the number of top connections to save and the output file name.

```bash
python3 peerscheck_with_height.py [top_n] [output_filename]
```

### Example

Run the script with optional command-line arguments to parse a URL, keep the top 40 connections with the highest block heights, and save the results to a file named 'top_ips_ports.txt'.

```bash
python3 script_name.py 40 top_ips_ports.txt
```


This will parse the URL 'https://rpc-initia-testnet.trusted-point.com/peers.txt', retrieve the connections, save the top 40 connections to the file 'top_ips_ports.txt', and log the processing status.


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
```


## Usage

1. Clone the repository or download the script.
2. Run the script:

```bash
python3 peerscheck.py
```



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
