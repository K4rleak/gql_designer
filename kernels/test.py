# https://discourse.jupyter.org/t/how-can-i-do-a-basic-hello-world-using-the-jupyter-client-api/20707
import time
from jupyter_client import KernelManager

def main():
    # Create a new kernel manager
    km = KernelManager(kernel_name='python3')
    km.start_kernel()

    # Create a client to interact with the kernel
    kc = km.client()
    kc.start_channels()

    # Ensure the client is connected before executing code
    kc.wait_for_ready()

    # Execute the code
    code = 'print("Hello, World!")'
    msg_id = kc.execute(code)

    # Wait for the result and display it
    while True:
        try:
            msg = kc.get_iopub_msg(timeout=1)
            content = msg["content"]

            # When a message with the text stream comes and it's the result of our execution
            if msg["msg_type"] == "stream" and content["name"] == "stdout":
                print(content["text"])
                break
        except KeyboardInterrupt:
            print("Interrupted by user.")
            break
        except:
            # If no messages are available, we'll end up here, but we can just continue and try again.
            pass

    # Cleanup
    kc.stop_channels()
    km.shutdown_kernel()

if __name__ == '__main__':
    main()