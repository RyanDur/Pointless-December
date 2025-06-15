import time

import grpc

import greet_pb2
import greet_pb2_grpc


def get_client_stream_function():
    while True:
        name = input("Enter your name: ")
        if name == "":
            break
        yield greet_pb2.HelloRequest(salutation=name)
        time.sleep(1)


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = greet_pb2_grpc.GreeterStub(channel)
        print("1. Say Hello - Unary RPC")
        print("2. Parrot Says Hello - Server Side Streaming RPC")
        print("3. Chatty client Say Hello - Client Side RPC")
        print("4. Interacting Hello - Bidirectional RPC")
        rpc_call = int(input("Enter RPC number: "))

        if rpc_call == 1:
            hello_request = greet_pb2.HelloRequest(salutation="Bonjour")
            hello_reply = stub.SayHello(hello_request)
            print(f"Received SayHello reply: {hello_reply.retort}")
            return hello_request

        elif rpc_call == 2:
            hello_request = greet_pb2.HelloRequest(salutation="Bonjour")
            hello_replies = stub.ParrotSayHello(hello_request)
            for reply in hello_replies:
                print(f"Received ParrotSayHello reply: {reply.retort}")
            return hello_request

        elif rpc_call == 3:
            delayed_reply = stub.ChattyClientSaysHello(get_client_stream_function())

            print("Received ChattyClientSaysHello reply:")
            print(delayed_reply)

        elif rpc_call == 4:
            responses = stub.InteractingHello(get_client_stream_function())

            for response in responses:
                print("Received InteractingHello reply:")
                print(response)


        return None


if __name__ == '__main__':
    try:
        while True:
            run()
            print('\n\nPress Ctrl+C to stop the program.\n\n')
    except KeyboardInterrupt:
        print("\nProgram stopped by user.")

