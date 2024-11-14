import serial


class UsartInterface:
    """Class to handle USART communication"""

    def __init__(self, port="/dev/ttyUSB0", baudrate=115200, timeout_s=10000) -> None:
        """Initialize the USART interface.
        Args:
            port (str): The port to connect to.
            baudrate (int): The baudrate to use.
            timeout_s (int): The timeout in seconds.
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout_s = timeout_s
        self.serial_connection = None

    def open_connection(self) -> bool:
        """Open a connection to the USART port.
        Returns:
            bool: True if the connection was successful, False otherwise.
        """
        try:
            self.serial_connection = serial.Serial(
                port=self.port, baudrate=self.baudrate, timeout=self.timeout_s
            )
            print(f"Connection to {self.port} opened successfully.")
            return True
        except serial.SerialException as e:
            print(f"Error opening connection to {self.port}: {e}")
            return False

    def close_connection(self) -> None:
        """Close the connection to the USART port."""
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
            print(f"Connection to {self.port} closed.")

    def send_data(self, data) -> None:
        """Send data over the USART connection.
        Args:
            data (str): The data to send.
        """
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.write(data)

    def receive_data(self) -> str:
        """Receive data from the USART connection.
        Returns:
            str: The received data.
        """
        if self.serial_connection and self.serial_connection.is_open:
            try:
                data = self.serial_connection.readline().decode()
                return data
            except UnicodeDecodeError:
                return None

    def receive_data_raw(self, number_of_bytes) -> bytes:
        """Receive raw data from the USART connection.
        Args:
            number_of_bytes (int): The number of bytes to read.
        Returns:
            str: The received data as a byte array.
        """
        if self.serial_connection and self.serial_connection.is_open:
            data = self.serial_connection.read(number_of_bytes)
            return data
