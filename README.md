# Own-NetCat-BHP Python Script

A Python-based NetCat utility for network communication, enabling command execution, file uploads, and interactive shell access over TCP connections. This project is a great starting point for understanding network programming, socket connections, and multi-threading in Python.

## Features

- **TCP Client/Server Communication**: Connect as a client or listen as a server.
- **Command Execution**: Run system commands on the remote server.
- **File Uploads**: Transfer files to a remote server.
- **Interactive Shell**: Use an interactive shell on the remote host.
- **Multi-threaded Listener**: Handles multiple clients concurrently.

## Requirements

- Python 3.x
- Basic understanding of Python, networking, and command-line usage

## Getting Started

Clone this repository or download the script to get started.

```bash
git clone https://github.com/yourusername/netcat-python.git
cd netcat-python
```

## Usage

This script uses `argparse` for command-line arguments, allowing flexible use cases depending on the options provided.

### Running the Script

Basic syntax:

```bash
python netcat.py -t <target_ip> -p <port> [options]
```

### Arguments and Options

| Argument            | Description                                                      |
|---------------------|------------------------------------------------------------------|
| `-t`, `--target`    | Target IP address for client connection (default: 192.168.1.203) |
| `-p`, `--port`      | Target port (default: 5555)                                      |
| `-l`, `--listen`    | Listen on specified IP and port for incoming connections         |
| `-c`, `--command`   | Initialize a command shell on the remote server                  |
| `-e`, `--execute`   | Execute a specified command on the remote server                 |
| `-u`, `--upload`    | Upload a file to the server with specified filename              |

> Note: When listening (`-l`), the script runs as a server and waits for client connections. Without `-l`, the script connects as a client to the target IP and port.

### Examples

#### 1. Starting a Command Shell (Server Mode)

Run this command to set up an interactive command shell:

```bash
python netcat.py -t 192.168.1.108 -p 5555 -l -c
```

- **Explanation**: Listens on IP `192.168.1.108`, port `5555`, and allows the client to execute commands on the server.

#### 2. Executing a Command on the Remote Server

Run a single command on the remote server:

```bash
python netcat.py -t 192.168.1.108 -p 5555 -l -e "ls -la"
```

- **Explanation**: Listens on IP `192.168.1.108`, port `5555`, and executes `ls -la`. This example can help verify server connectivity and check directory contents.

#### 3. Uploading a File to the Server

To upload a file to the remote server:

```bash
python netcat.py -t 192.168.1.108 -p 5555 -l -u="received_file.txt"
```

- **Explanation**: Listens on `192.168.1.108`, port `5555`, and saves uploaded file contents as `received_file.txt` on the server. The client sends file data, and the server writes it to `received_file.txt`.

#### 4. Sending Messages as a Client

To send text or commands to a server:

```bash
echo "Hello, server!" | python netcat.py -t 192.168.1.108 -p 5555
```

- **Explanation**: Connects to a listening server at IP `192.168.1.108` and port `5555` and sends the message `"Hello, server!"`.

## Code Overview

Here’s a high-level overview of the script's structure and functionality:

1. **Argument Parsing**: Uses `argparse` to handle and parse command-line arguments.
  
2. **Command Execution** (`execute` function): Runs shell commands provided by the user and returns the output. Commands are split securely with `shlex.split`.

3. **NetCat Class**: Implements the core functionality:
   - **`__init__`**: Initializes the socket and other parameters.
   - **`run`**: Determines whether to act as a server (`listen`) or client (`send`).
   - **`send`**: Connects to a server and allows interactive communication.
   - **`listen`**: Sets up the server to handle incoming connections.
   - **`handle`**: Manages file uploads, command execution, and interactive shells.

4. **Multi-threading**: When listening, each client connection is handled in a new thread, allowing simultaneous connections.

## How It Works

- **Client Mode**: Connects to a specified IP and port, sending data if a buffer is provided and waiting for server responses.
- **Server Mode**: Accepts connections from clients. If configured, can execute commands, provide a shell, or handle file uploads.
- **Communication Loop**: The `send` method contains a loop that continuously receives data from the server, making it ideal for long-running sessions.
- **Error Handling**: Captures keyboard interrupts and closes the socket cleanly if the user terminates the script.

## Example Scenarios

- **Command Shell Access**: Connect to remote servers and use the command shell to run remote commands.
- **File Transfer**: Transfer files between systems, especially useful in restricted network environments.
- **Remote System Administration**: Run custom commands on remote machines to gather information or troubleshoot.
  
> **Note**: Ensure you have permission to connect to and interact with remote machines.

## Security Considerations

Since this script opens a TCP connection and allows remote command execution, use it responsibly. Ensure that:

1. **Access is Restricted**: Only allow trusted IPs to connect.
2. **Permissions are Set**: Ensure that the script has appropriate permissions and cannot be accessed publicly.
3. **Usage is Monitored**: Track usage to avoid unintended access or misuse.

## Future Improvements

Here are some potential enhancements to consider:

- **Encryption**: Add SSL/TLS encryption for secure communication.
- **Authentication**: Require a password to establish a connection or execute commands.
- **Logging**: Log all commands, file transfers, and connections for auditing.
- **Error Handling**: Enhance error handling to manage dropped connections gracefully.

## License

This project is open-source under the MIT License. Feel free to use and modify it.

## Credits
The ideas presented in this project are based on the Black Hat Python Book Chapter 1 written by Julian Seitz. Special thanks are in order!
