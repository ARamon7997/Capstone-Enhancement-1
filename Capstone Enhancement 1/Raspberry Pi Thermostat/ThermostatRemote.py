# ThermostatRemote.py - This is the Python code that will be used
# from the thermostat end, to connect ThermostatClient to the thermostat.
# the interaction commands sent through the client will then be processed
# to the thermostat, where the command will be processed as if the corresponding
# button has been pressed.
#
#------------------------------------------------------------------
# Change History
#------------------------------------------------------------------
# Version   |   Description
#------------------------------------------------------------------
#    1          Initial Development
#------------------------------------------------------------------

# Socket and SSL import for connection and authentication systems
import socket
import ssl

# Importing Path to detect certificate and key files
from pathlib import Path
from urllib import response

# Test connection variables
HOST = "0.0.0.0"
PORT = 5050

# Finds the current path to the crt and key files
CON_DIR = Path(__file__).resolve().parent

# TLS configuration
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile= str(CON_DIR / "Thermostat.crt"),keyfile=str(CON_DIR / "thermostat.key"))

# Authorized client certificate required
context.verify_mode = ssl.CERT_REQUIRED

# Trust the client certificate
context.load_verify_locations(cafile= str(CON_DIR / "Client.crt"))

# Server initialization
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Forwards command to the thermostat proper
def forward_command(command):

    try:
        with socket.create_connection(("127.0.0.1", 5051), timeout=5) as connection:

            connection.sendall((command + "\n").encode("utf-8"))

            response = connection.recv(128)
            return response.decode().strip() or "ERROR"

    except OSError as e:
        print("Thermostat connection error:", e)
        return "ERROR: Thermostat offline"

try:
    # Listens for a connection
    server.bind((HOST, PORT))
    server.listen(1)

    print ("Waiting for connection")

    #Accepts the client connection
    connection, address = server.accept()
    connection.settimeout(5)

    #Establishes TLS encrypted connection
    with context.wrap_socket(connection, server_side=True) as secure_connection:
        secure_connection.settimeout(None)

        # Receives commands from the client


        while True:
            # Reads the command from the client
            command = secure_connection.recv(1024).decode().strip()

            if not command:
                break


            command = command.strip()
            print("Received command: " + command)

            # Ping test response
            if command == "PING":
                response = "PONG"

            # State change response
            elif command == "STATE":
                response = forward_command(command)

            # Increase setpoint response
            elif command == "INCREASE":
                response = forward_command(command)

            # Decrease setpoint response
            elif command == "DECREASE":
                response = forward_command(command)

            else:
                response = "ERROR"

            secure_connection.sendall((response + "\n").encode("utf-8"))

except OSError as e:
    print ("Connection error:", e)


finally:
    server.close()
    print ("Connection closed")