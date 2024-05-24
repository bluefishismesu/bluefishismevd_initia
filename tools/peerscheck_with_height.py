import socket
import time
import logging
import requests
import sys

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def check_connection(ip, port, timeout=2):
    """
    Check if the given IP and port can be connected to and measure the connection time.
    :param ip: IP address
    :param port: Port number
    :param timeout: Timeout in seconds
    :return: Whether the connection is successful and the connection time in seconds
    """
    start_time = time.time()
    try:
        with socket.create_connection((ip, port), timeout):
            end_time = time.time()
            return True, end_time - start_time
    except (socket.timeout, socket.error) as e:
        return False, None

def parse_and_check(url):
    """
    Parse the file from the URL and check the connectivity and response time of each IP and port.
    :param url: URL of the file to be parsed
    :return: List of successfully connected IP and port with their response times
    """
    successful_connections = []
    response = requests.get(url)
    if response.status_code == 200:
        lines = response.text.split(',')
        total_lines = len(lines)
        for index, line in enumerate(lines):
            # Extract IP and port
            parts = line.split('@')
            if len(parts) == 2:
                ip_port = parts[1].split(':')
                if len(ip_port) == 2:
                    ip = ip_port[0]
                    port = int(ip_port[1])
                    # Check connectivity and response time
                    success, response_time = check_connection(ip, port)
                    if success:
                        #logging.info(f"Successfully connected to {ip}:{port} with response time {response_time:.4f} seconds.")
                        block_height,moniker = get_latest_block_height(ip, port+1)
                        if block_height is not None:
                            #logging.info(f"block_height {moniker}    {ip}:{port} with {block_height}")
                            logging.info(f"block_height {moniker}   {ip}:{port} with {block_height}")
                            successful_connections.append((line,block_height))
                    #else:
                        #logging.warning(f"Failed to connect to {ip}:{port}.")
            # Print progress information
            logging.info(f"Processed {index + 1}/{total_lines} entries.")
    else:
        logging.error("Failed to retrieve the file from the URL.")
    return successful_connections

def get_latest_block_height(ip, rpc_port):
    """
    Get the latest block height from the specified IP address and RPC port.
    Try HTTPS POST request first, and fallback to HTTP GET request if it fails.
    :param ip: IP address
    :param rpc_port: RPC port
    :return: Latest block height (int) or None if failed
    """
    url_https = f"https://{ip}:{rpc_port}/status"
    url_http = f"http://{ip}:{rpc_port}/status"
    
    # Try HTTPS POST request
    #try:
    #    response = requests.post(url_https, timeout=2)
    #    if response.status_code == 200:
    #        result = response.json()
    #        latest_block_height = int(result["result"]["sync_info"]["latest_block_height"])
            #logging.info(f"Successfully retrieved latest block height from {ip}:{rpc_port} using HTTPS.")
    #        return latest_block_height
        #else:
            #logging.error(f"Failed to retrieve latest block height from {ip}:{rpc_port} using HTTPS. Status code: {response.status_code}")
    #except requests.RequestException as e:
        #logging.error(f"HTTPS request error occurred: {e}")
     #   aaa=0
    
    # Fallback to HTTP GET request
    try:
        response = requests.get(url_http, timeout=1)
        if response.status_code == 200:
            result = response.json()
            latest_block_height = int(result["result"]["sync_info"]["latest_block_height"])
            moniker = result["result"]["node_info"]["moniker"]
            #node_info = result["result"].get("node_info")
            #moniker = node_info.get("moniker") if node_info else None
            #logging.info(f"Successfully retrieved latest block height from {ip}:{rpc_port} using HTTP.")
            return latest_block_height,moniker
            #return latest_block_height
        #else:
            #logging.error(f"Failed to retrieve latest block height from {ip}:{rpc_port} using HTTP. Status code: {response.status_code}")
    except requests.RequestException as e:
        #logging.error(f"HTTP request error occurred: {e}")
        pass   
    return None,""

def save_top_connections(connections, output_filename, top_n=40):
    """
    Save the top N connections with the highest block heights to the specified file.
    :param connections: List of IP and port with their block heights
    :param output_filename: Output file name
    :param top_n: Number of connections to save
    """
    # Sort by block height in descending order
    connections.sort(key=lambda x: x[1], reverse=True)
    # Keep the top N connections
    top_connections = connections[:top_n]
    # Write to file
    logging.info(f"Saved top {top_n} connections to {output_filename}.")
    #with open(output_filename, 'w') as file:
    #    file.write(','.join([conn[0] for conn in top_connections]))
    # Write to file and log to console
    with open(output_filename, 'w') as file:
        first_entry = True
        for conn in top_connections:
            logging.info(f"Connection: {conn[0]}, Block Height: {conn[1]}")
            if first_entry:
                file.write(conn[0] )
                first_entry = False
            else:             
                file.write(','+conn[0] )
# Example: Read from the URL, keep the top 40 with the lowest response times, and save to 'top_ips_ports.txt'
try:
    top_n = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    output_filename = sys.argv[2] if len(sys.argv) > 2 else 'top_ips_ports.txt'    
    connections = parse_and_check('https://rpc-initia-testnet.trusted-point.com/peers.txt')
    save_top_connections(connections, output_filename, top_n)
    logging.info("Processing completed successfully.")
except Exception as e:
    logging.error(f"An error occurred: {e}")













