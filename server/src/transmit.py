import struct
import os

FIFO_PATH = "/tmp/log-bridge-tx-fifo"
COMMAND_MSG_SIZE = 32  # Size of the command message struct


def get_new_speed():
    """Prompt the user for a new motor speed"""
    while True:
        try:
            cmd_id = int(input("Enter motor speed (-100 - 100): "))
            if -100 <= cmd_id <= 100:
                return cmd_id
            else:
                print("Motor speed must be between -100 and 100.")
        except ValueError:
            print("Please enter a valid integer between -100 and 100.")


def pack_command_msg(mot_speed):
    """Pack the command message into a struct format compatible with command_msg.
    Args:
        mot_speed (int): The motor speed to pack.
    Returns:
        bytes: The packed struct data.
    """
    # First byte is the motor speed as a signed 8-bit integer, remaining bytes are zero-filled
    struct_format = "b" + "x" * (COMMAND_MSG_SIZE - 1)
    packed_data = struct.pack(struct_format, mot_speed)
    
    return packed_data


def send_to_fifo(data):
    """Write the packed command message to the FIFO for USART transmission.
    Args:
        data (bytes): The packed struct data to send.
    """
    if not os.path.exists(FIFO_PATH):
        print(f"FIFO {FIFO_PATH} does not exist. Ensure the server script is running.")
        return
    with open(FIFO_PATH, "wb") as fifo:
        fifo.write(data)
        print("Command message sent to FIFO.")


def main():
    """Main function to handle user input, packing, and FIFO transmission."""

    if not os.path.exists(FIFO_PATH):
        print(f"FIFO '{FIFO_PATH}' does not exist. Ensure the server script is running.")
        return

    mot_speed = get_new_speed()
    packed_msg = pack_command_msg(mot_speed)
    send_to_fifo(packed_msg)


if __name__ == "__main__":
    main()
