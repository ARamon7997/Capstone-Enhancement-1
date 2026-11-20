# ThermostatClient.py - This is the Python code that will be used
# to connect to and interact with the thermostat from an external computer,
# via either WLAN, or Bluetooth. Once the connection is verified and connected,
# you can send commands, whether that will be setting the setpoint, or the cycle.
# the client can also ping the thermostat to test the connection, using ping.
# Pressing Q disconnects and exits the client.
#
#------------------------------------------------------------------
# Change History
#------------------------------------------------------------------
# Version   |   Description
#------------------------------------------------------------------
#    1          Initial Development
#------------------------------------------------------------------


# Imports that will be needed for remote connectivity
import socket
import ssl

import certifi


#from urllib import response

#from zeroconf import Zeroconf, ServiceInfo


class ThermostatClient:


    # Initializes the connection
    def __init__(self):

        # Connection settings
        HOST = input("Enter the IP address of the Thermostat: ")
        PORT = 5050

        self.connection = None


        try:
            # Thermostat authentication
            context = ssl.create_default_context(cafile="Thermostat.crt")

            # Client authentication
            context.load_cert_chain("Client.crt", keyfile="client.key")

            # Establishes the connection
            connection = socket.create_connection((HOST, PORT), 5)

            # Securing the connection
            self.connection = context.wrap_socket(connection, server_hostname=HOST)

            print("Connected to Thermostat")

        except OSError as e:
            print("Could not connect to thermostat:", e)


    # Allows the user to input a command
    def send_command(self, command):

        # Returns false if there is no connection
        if self.connection is None:
            print("Could not connect to Thermostat")
            return False

        try:
            self.connection.sendall((command + "\n").encode("utf-8"))




            # Command response
            response = self.connection.recv(1024)
            response = response.decode().strip()

            # Ping test response
            if command == "PING":
                return response == "PONG"

            # Message if the command is successful
            print("Response from Thermostat: " + response)
            return response == command + " Successful"

        except OSError as e:
            print("Could not execute command")

    # Sends a test ping to the thermostat to determine if there is a connection between client and thermostat.
    def ping_test(self):
        return self.send_command("PING")

    ## Sends the state change command, which will change the state of the thermostat
    ## Which goes from off to heat to cool back to off
    def change_state(self):
        return self.send_command("STATE")

    ## Sends the set increase command, which will increase the setpoint on the thermostat by a degree
    def increase_set(self):
        return self.send_command("INCREASE")

    ## Sends the set decrease command, which will decrease the setpoint on the thermostat by a degree
    def decrease_set(self):
        return self.send_command("DECREASE")

    # Closes the connection
    def disconnect(self):

        if self.connection:
            self.connection.close()
            self.connection = None
            print("Disconnected from Thermostat")


client = ThermostatClient()

# Client key commands, to interface with the thermometer
if client.ping_test():

    #Instructions for using the client
    print("Instructions ** 1: Cycle, 2: Setpoint +1, 3: Setpoint -1, Q: Quit **")

    while True:

        # Command input
        key = input("Enter Command: ").upper()

        # 1 for the state change command
        if key == "1":
            client.change_state()

        # 2 for the setpoint increase command
        elif key == "2":
            client.increase_set()

        # 3 for the setpoint decrease command
        elif key == "3":
            client.decrease_set()

        # Q to quit out of the client
        elif key == "Q":
            break


        else:
            print("Invalid Command")

client.disconnect()


