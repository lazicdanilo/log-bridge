import struct
import os
import select
from usart_interface import UsartInterface


class Server:
    """Server class to handle USART communication with the client (MCU)"""

    """ Depends on struct log_msg from client/src/log-bridge.c """
    RX_DATA_COUNT = 165

    """ Adjust based on struct log_msg from client/src/log-bridge.c """
    THREAD_NAME_SIZE = 32

    """ Adjust based on struct log_msg from client/src/log-bridge.c """
    LOG_MESSAGE_SIZE = 128

    """ Adjust based on struct command_msg from client/src/log-bridge.c """
    FIFO_MESSAGE_SIZE = 32

    FIFO_PATH = "/tmp/log-bridge-tx-fifo"  # Path to FIFO file

    def __init__(self, port="/dev/ttyUSB0", baudrate=115200) -> None:
        """Initialize the server.
        Args:
            port (str): The port to connect to.
            baudrate (int): The baudrate to use.
        """
        self.interface = UsartInterface(port=port, baudrate=baudrate)

        if not self.interface.open_connection():
            raise ValueError("Error opening USART connection.")

        self._create_fifo()

    def _create_fifo(self) -> None:
        """Create a FIFO file in /tmp/ directory if it does not already exist."""
        if not os.path.exists(self.FIFO_PATH):
            os.mkfifo(self.FIFO_PATH)

    def parse_log_msg(self, data) -> dict:
        """Parse the log message data.
        Args:
            data (bytes): The raw data to parse.
        Returns:
            dict: The parsed log message data.
        """
        # Define struct format with little-endian byte order and packed fields
        struct_format = f"<B I {self.THREAD_NAME_SIZE}s {self.LOG_MESSAGE_SIZE}s"

        # Unpack the data according to the struct format
        lvl, timestamp_ms, thread_name, msg = struct.unpack(struct_format, data)
        thread_name = thread_name.decode("utf-8").strip("\x00")
        msg = msg.decode("utf-8").strip("\x00")
        return {
            "level": lvl,
            "timestamp_ms": timestamp_ms,
            "thread_name": thread_name,
            "message": msg,
        }

    def transmit_data(self) -> None:
        """Transmit data from the FIFO to the USART interface."""
        with open(self.FIFO_PATH, "rb") as fifo:
            while True:
                # Use select to handle non-blocking read from FIFO
                ready, _, _ = select.select([fifo], [], [], 0.5)
                if fifo in ready:
                    data = fifo.read(self.FIFO_MESSAGE_SIZE)
                    if data:
                        self.interface.send_data(data)
                        print("Command message sent to USART.")

    def run(self) -> None:
        """Run the server."""
        while True:
            data = self.interface.receive_data_raw(self.RX_DATA_COUNT)
            if data:
                log_data = self.parse_log_msg(data)
                print(log_data) # TODO: Implement nicer print on server side

    def start(self) -> None:
        """Start the server with both RX and TX capabilities."""
        import threading

        # Start the RX server in a separate thread
        rx_thread = threading.Thread(target=self.run, daemon=True)
        rx_thread.start()

        try:
            # Start the TX function
            self.transmit_data()
        except KeyboardInterrupt:
            self.interface.close_connection()
            print("Closing UART connection...")
            # Delete fifo
            os.remove(self.FIFO_PATH)
            print("Removing FIFO...")


if __name__ == "__main__":
    server = Server(baudrate=921600)
    server.start()
