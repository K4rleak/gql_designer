import socket
import json

def send_expression_to_server(expression, host='localhost', port=12345):
    # Create a TCP/IP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the server
        client_socket.connect((host, port))
        print(f"Connected to server at {host}:{port}")

        # Prepare the JSON request
        request = json.dumps({"expression": expression})

        # Send the JSON-encoded expression to the server
        client_socket.send(request.encode('utf-8'))

        # Receive the result from the server
        response = client_socket.recv(1024)
        result = json.loads(response.decode('utf-8'))
        print(f"Result from server: {result}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the connection
        client_socket.close()

if __name__ == "__main__":
    # Example expression to evaluate
    a = 5
    b = 10
    expression = f"{a} + {b}"
    
    send_expression_to_server(expression)
