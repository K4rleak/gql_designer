import socket
import json
from ipykernel.kernelapp import IPKernelApp
from jupyter_client import BlockingKernelClient

def start_kernel_server(host='localhost', port=12345):
    # Start an IPython kernel in the background
    app = IPKernelApp.instance()
    app.initialize()
    
    # Create a kernel client to communicate with the kernel
    kernel_client = BlockingKernelClient()
    kernel_client.load_connection_file(app.connection_file)
    kernel_client.start_channels()

    # Create a TCP/IP socket for communication with the client
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Kernel server listening on {host}:{port}")

    while True:
        # Accept incoming connections
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")

        try:
            # Receive the data from the client
            data = client_socket.recv(1024)
            if not data:
                break

            # Deserialize the JSON data
            request = json.loads(data.decode('utf-8'))
            expression = request.get('expression', '')
            print(f"Received expression: {expression}")

            # Execute the code in the kernel
            kernel_client.execute(expression)
            reply = kernel_client.get_shell_msg()
            result = reply['content'].get('status', 'error')
            if result == 'ok':
                result = kernel_client.get_iopub_msg()['content']['text']
            else:
                result = "Error in execution"

            # Send the result back to the client
            response = json.dumps({"result": result})
            client_socket.send(response.encode('utf-8'))

        except Exception as e:
            error_response = json.dumps({"error": str(e)})
            client_socket.send(error_response.encode('utf-8'))

        finally:
            # Close the client connection
            client_socket.close()

if __name__ == "__main__":
    start_kernel_server()
