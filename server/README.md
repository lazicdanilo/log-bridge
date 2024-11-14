# Log Bridge - server

This is a Python script that usually runs on Raspberry Pi or user PC. It will communicate with the client (MCU) via USART.

## Build server and client

Below are the steps to install the required packages and build the server and client.

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## server.py

When the `server.py` script is running, it will receive data from the client (MCU) using USART, log it to a file and display it in console. This is a used for debugging and monitoring the server.

## transmit.py

> [!NOTE]
> Before running the `transmit.py` script, make sure the server is running.

The `transmit.py` script is used to send data to the client (MCU) using USART. This script communicates with the `server.py` script which sends the data to the client (MCU).
