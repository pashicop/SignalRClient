import logging
import sys
from time import sleep

from signalrcore.hub_connection_builder import HubConnectionBuilder


def get_signalR_con():
    print('enter')
    hub_connection = HubConnectionBuilder() \
        .with_url("ws://"+server_url,
                  options={
                      # "access_token_factory": login_function,
                      # "verify_ssl": False,
                      "skip_negotiation": True,
                      # "InvocationType": 0,
                      "headers": {
                          "Authorization": "Bearer " + TOKEN
                      }
                  }) \
        .configure_logging(logging.DEBUG, socket_trace=True, handler=handler) \
        .with_automatic_reconnect({
        "type": "raw",
        "keep_alive_interval": 10,
        "reconnect_interval": 5,
        "max_attempts": 5
    }).build()
    print('exit')
    return hub_connection

if __name__ == '__main__':
    server_url = "10.1.4.140:5000/mainHub"
    TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1bmlxdWVfbmFtZSI6InR0IiwibmFtZWlkIjoiY2Q5OGNjZWItZTE3Zi00MDI2LTliNDktZDE0MzU3ZjFkZmZjIiwicm9sZSI6WyJQcml2YXRlQ2FsbGVyIiwiUHJpdmF0ZU1lc3NhZ2VzIiwiVXNlcnMiXSwibmJmIjoxNzAwMTI0MjEwLCJleHAiOjE3MDA3MjkwMTAsImlhdCI6MTcwMDEyNDIxMH0.sFYdZmzJdJBGS9R8WqATmRwgwp5qDlR4FfJ1iwYL5qk"
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    hc = get_signalR_con()
    hc.start()
    hc.on_open(lambda: print("connection opened and handshake received ready to send messages"))
    hc.on_close(lambda: print("connection closed"))
    hc.on("ReceiveMessage", print)
    hc.on_error(lambda data: print(f"An exception was thrown closed{data.error}"))
    i = 0
    while True:
        print(i)
        sleep(1)
        i += 1
    hc.stop()

    sys.exit(0)


