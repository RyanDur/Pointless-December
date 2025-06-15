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

def get_person_1_client_stream_function():
    responses = ["Alice 1", "Bob 1", "Charlie 1"]
    for response in responses:
        yield greet_pb2.HelloRequest(salutation=response)
        time.sleep(1)

def get_person_2_client_stream_function():
    responses = ["Dave 2", "Eve 2", "Frank 2"]
    for response in responses:
        yield greet_pb2.HelloRequest(salutation=response)
        time.sleep(2)



def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = greet_pb2_grpc.GreeterStub(channel)
        print("1. Say Hello - Unary RPC")
        print("2. Parrot Says Hello - Server Side Streaming RPC")
        print("3. Chatty client Say Hello - Client Side RPC")
        print("4. Interacting Hello - Bidirectional RPC")
        print("5. More Interacting Hello - Bidirectional RPC")
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

        elif rpc_call == 5:
            responses_1 = stub.InteractingHello(get_person_1_client_stream_function())
            responses_2 = stub.InteractingHello(get_person_2_client_stream_function())

            for _ in range(3):
                response = next(responses_1)
                print(f"Received InteractingHello reply: {response.retort}")
                input("Press Enter to continue...")
                response = next(responses_2)
                print(f"Received InteractingHello reply: {response.retort}")
                input("Press Enter to continue...")


        return None


if __name__ == '__main__':
    try:
        while True:
            run()
            print('\n\nPress Ctrl+C to stop the program.\n\n')
    except KeyboardInterrupt:
        print("\nProgram stopped by user.")

