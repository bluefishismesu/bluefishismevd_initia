import socket
import time
import logging
import requests

# Set up logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def check_connection(ip, port, timeout=5):
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
                        logging.info(f"Successfully connected to {ip}:{port} with response time {response_time:.4f} seconds.")
                        successful_connections.append((line, response_time))
                    else:
                        logging.warning(f"Failed to connect to {ip}:{port}.")
            # Print progress information
            logging.info(f"Processed {index + 1}/{total_lines} entries.")
    else:
        logging.error("Failed to retrieve the file from the URL.")
    return successful_connections

def save_top_connections(connections, output_filename, top_n=40):
    """
    Save the top N connections with the lowest response times to the specified file.
    :param connections: List of IP and port with their response times
    :param output_filename: Output file name
    :param top_n: Number of connections to save
    """
    # Sort by response time
    connections.sort(key=lambda x: x[1])
    # Keep the top N connections
    top_connections = connections[:top_n]
    # Write to file
    with open(output_filename, 'w') as file:
        file.write(','.join([conn[0] for conn in top_connections]))
    logging.info(f"Saved top {top_n} connections to {output_filename}.")

def get_moniker_from_json(json_str):
    try:
        data = json.loads(json_str)
        moniker = data.get('result', {}).get('node_info', {}).get('moniker')
        if moniker is not None:
            return moniker
        else:
            return "Moniker not found"
    except json.JSONDecodeError:
        return "Invalid JSON"
# Example: Read from the URL, keep the top 40 with the lowest response times, and save to 'top_ips_ports.txt'
try:
    connections = parse_and_check('https://rpc-initia-testnet.trusted-point.com/peers.txt')
    save_top_connections(connections, 'top_ips_ports.txt', top_n=40)
    logging.info("Processing completed successfully.")
except Exception as e:
    logging.error(f"An error occurred: {e}")
