import os
import requests
import json
import logging
import csv
from time import time, sleep
from stem import Signal
from stem.control import Controller

# Configure logging
current_dir = os.path.dirname(os.path.abspath(__file__))
csv_file_path = os.path.join(current_dir, 'vpn.csv')

# Create the CSV file if it doesn't exist and add headers
if not os.path.exists(csv_file_path):
    with open(csv_file_path, 'a', newline='') as csvfile:
        vpn_log_writer = csv.writer(csvfile)
        vpn_log_writer.writerow(['Old IP', 'New IP', 'Start Time', 'End Time'])

class IPChanger:
    """
    Manages IP changes using the Tor network, providing anonymity for network requests.

    This class utilizes the Tor network to dynamically change the user's IP address, facilitating
    anonymity for activities such as web scraping and browsing. It also logs VPN changes for
    monitoring and analysis.

    Attributes:
        logger (logging.Logger): A logging instance to log information, errors, and warnings.
    """

    def __init__(self):
        """Initializes the IPChanger class with logging configuration."""
        self.configure_logger()

    def configure_logger(self):
        """Configures a logger to log information and errors."""
        log_file_path = os.path.join(current_dir, 'ipchanger.log')
        if not os.path.exists(log_file_path):
            open(log_file_path, 'a').close()
        os.chmod(log_file_path, 0o600)
        self.logger = logging.getLogger(__name__)
        if not self.logger.handlers:
            file_handler = logging.FileHandler(log_file_path)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s')
            file_handler.setFormatter(formatter)
            file_handler.setLevel(logging.ERROR)
            self.logger.addHandler(file_handler)
            self.logger.setLevel(logging.ERROR)

    def get_current_ip(self):
        """
        Retrieves the current external IP address through the Tor network.

        Returns:
            str: The current external IP address, or None if an error occurs.
        """
        try:
            response = requests.get('http://checkip.amazonaws.com', proxies={'http': 'socks5://127.0.0.1:9050', 'https': 'socks5://127.0.0.1:9050'})
            return response.text.strip()
        except requests.RequestException as e:
            self.logger.error(f"Failed to fetch IP address: {e}")
            return None

    def change_ip(self, switch_ip: bool, max_attempts=5):
        """
        Attempts to change the external IP address through the Tor network.

        Args:
            switch_ip (bool): Whether to attempt an IP switch.
            max_attempts (int): Maximum number of attempts to change the IP address.

        Returns:
            str: The new IP address if successful, or None otherwise.
        """
        if switch_ip:
            old_ip = self.get_current_ip()
            for attempt in range(max_attempts):
                try:
                    with Controller.from_port(port=9051) as controller:
                        # controller.authenticate('add sudo password in here and remove hash')  
                        controller.signal(Signal.NEWNYM)
                        new_ip = self.get_current_ip()
                        if new_ip and new_ip != old_ip:
                            self.logger.info(f"IP changed from {old_ip} to {new_ip}.")
                            return new_ip
                except Exception as e:
                    self.logger.error(f"Error while changing IP on attempt {attempt + 1}: {e}")

            self.logger.error("Failed to change IP after multiple attempts.")
            return None

    def log_vpn_change(self, old_ip, new_ip, start_time, end_time):
        """
        Logs details of a VPN change to a CSV file.

        Args:
            old_ip (str): The previous IP address.
            new_ip (str): The new IP address.
            start_time (float): The start time of the IP change process.
            end_time (float): The end time when the new IP was obtained.
        """
        with open(csv_file_path, 'a', newline='') as csvfile:
            vpn_log_writer = csv.writer(csvfile)
            vpn_log_writer.writerow([old_ip, new_ip, start_time, end_time])

    def get_geolocation(self, ip_address): # Geo Tag is not accurate city is not accurate but country is
        """
        Fetches geolocation data for a specified IP address.

        Args:
            ip_address (str): The IP address to lookup.

        Returns:
            dict: Geolocation data, or None if an error occurs.
        """
        request_url = 'https://geolocation-db.com/jsonp/' + ip_address
        try:
            response = requests.get(request_url)
            if response.status_code == 200:
                result = response.content.decode()
                result = result.split("(")[1].strip(")")
                return json.loads(result)
            else:
                return None
        except requests.RequestException:
            return None

    def terminate(self):
        """
        Terminates the current Tor circuit, disconnecting from the Tor network.
        """
        try:
            with Controller.from_port(port=9051) as controller:
                # controller.authenticate('izzie197')  # Replace with your control port password
                controller.signal(Signal.NEWNYM)
                controller.close()
                self.logger.info("Terminated the Tor circuit and disconnected from the Tor network.")
        except Exception as e:
            self.logger.error(f"Error while terminating Tor circuit: {e}")


if __name__ == "__main__":
    changer = IPChanger()
    old_ip = changer.get_current_ip()
    print(f"Current IP: {old_ip}")
    new_ip = changer.change_ip(True)
    print(f"IP changed from {old_ip} to {new_ip}" if new_ip else "Failed to change IP.")
    changer.terminate()
    sleep(10)
    ip = changer.get_current_ip()
    print(ip)

