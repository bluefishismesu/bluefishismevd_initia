import socket
import time
import logging
import requests
import sys
import json

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

def get_peer_info(ip, rpc_port):
    """
    Get the peer information from the specified IP address and RPC port.
    :param ip: IP address
    :param rpc_port: RPC port
    :return: List of peer info dictionaries
    """
    url_http = f"http://{ip}:{rpc_port}/net_info"
    try:
        response = requests.get(url_http, timeout=1)
        if response.status_code == 200:
            result = response.json()
            peers = result["result"]["peers"]
            peer_info = []
            for peer in peers:
                node_id = peer["node_info"]["id"]
                remote_ip = peer["remote_ip"]
                rpc_address = peer["node_info"]["other"]["rpc_address"]
                rpc_port_str = rpc_address.split(":")[-1]
                if rpc_port_str:  # Check if rpc_port_str is not empty
                    rpc_port = int(rpc_port_str)
                else:
                    logging.error(f"Invalid RPC port received for peer {node_id} at {remote_ip}. Skipping.")
                    continue                
                listen_addr = peer["node_info"]["listen_addr"]
                if listen_addr:  # Check if rpc_port_str is not empty
                    p2p_port_str = listen_addr.split(":")[-1]
                    if p2p_port_str:  # Check if rpc_port_str is not empty
                        p2p_port = int(p2p_port_str)
                    else:
                        logging.error(f"Invalid p2p port received for peer {node_id} at {remote_ip}. Skipping.")
                        continue                
                else:
                    logging.error(f"Invalid p2p port received for peer {node_id} at {remote_ip}. Skipping.")
                    continue                
                peer_info.append((node_id, remote_ip, rpc_port, p2p_port))
            logging.info(f"Number of peers for {ip}:{rpc_port} is {len(peer_info)}")  # Add this line to print the number of peers
            return peer_info
    except requests.RequestException as e:
        pass
    return []

def parse_and_check(file_path):
    """
    Parse the file and check the connectivity and response time of each IP and port.
    :param file_path: Path to the file to be parsed
    :return: List of successfully connected IP and port with their response times
    """
    successful_connections = []
    seen_peers = set()
    failed_connections = []
    with open(file_path, 'r') as file:
        lines = file.read().split(',')
    total_lines = len(lines)
    unique_lines = list(set(lines))  # Remove duplicates
    for index, line in enumerate(unique_lines):
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
                    block_height, moniker = get_latest_block_height(ip, port + 1)
                    if block_height is not None:
                        logging.info(f"block_height {moniker}   {ip}:{port} with {block_height}")
                        if line not in seen_peers:
                            successful_connections.append((line, block_height))
                            seen_peers.add(line)
                        # Get peer information and check their connectivity
                        peer_info = get_peer_info(ip, port + 1)
                        for node_id, remote_ip, rpc_port, p2p_port in peer_info:
                            peer_key = f"{node_id}@{remote_ip}:{p2p_port}"
                            
                            if peer_key not in seen_peers:
                                peer_success, peer_response_time = check_connection(remote_ip, rpc_port)
                                if peer_success:
                                    peer_block_height, peer_moniker = get_latest_block_height(remote_ip, rpc_port)
                                    if peer_block_height is not None:
                                        logging.info(f"block_height {peer_moniker}   {remote_ip}:{rpc_port} with {peer_block_height}")
                                        successful_connections.append((f"{node_id}@{remote_ip}:{p2p_port}", peer_block_height))
                                        seen_peers.add(peer_key)
                                else:
                                    failed_connections.append(f"{node_id}@{remote_ip}:{p2p_port}")
                else:
                    failed_connections.append(line)
        logging.info(f"Processed {index + 1}/{total_lines} entries.")
    # Write failed connections to file
    with open('failed_connections.txt', 'w') as file:
        for line in failed_connections:
            file.write(line + '\n')
    return successful_connections

def get_latest_block_height(ip, rpc_port):
    """
    Get the latest block height from the specified IP address and RPC port.
    :param ip: IP address
    :param rpc_port: RPC port
    :return: Latest block height (int) or None if failed
    """
    url_http = f"http://{ip}:{rpc_port}/status"
    try:
        response = requests.get(url_http, timeout=1)
        if response.status_code == 200:
            result = response.json()
            latest_block_height = int(result["result"]["sync_info"]["latest_block_height"])
            moniker = result["result"]["node_info"]["moniker"]
            return latest_block_height, moniker
    except requests.RequestException as e:
        pass   
    return None, ""

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
    with open(output_filename, 'w') as file:
        first_entry = True
        for conn in top_connections:
            logging.info(f"Connection: {conn[0]}, Block Height: {conn[1]}")
            if first_entry:
                file.write(conn[0])
                first_entry = False
            else:
                file.write(',' + conn[0])

# Example: Read from the URL, keep the top 40 with the highest block heights, and save to 'top_ips_ports.txt'
try:
    top_n = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    output_filename = sys.argv[2] if len(sys.argv) > 2 else 'top_ips_ports_nodinfo.txt'    
    connections = parse_and_check('top_ips_ports.txt')
    save_top_connections(connections, output_filename, top_n)
    logging.info("Processing completed successfully.")
except Exception as e:
    logging.error(f"An error occurred: {e}")
