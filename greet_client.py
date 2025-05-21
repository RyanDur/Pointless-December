import time

import grpc

import greet_pb2
import greet_pb2_grpc


def get_client_stream_function():
    while True:
        name = input("Enter your name: ")
        if name == "":
            break
        yield greet_pb2.HelloRequest(salutation="elo")


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
            print(f"Received ChattyClientSaysHello reply: {delayed_reply}")
            # for reply in delayed_reply:
            #     print(f"Received ParrotSayHello reply: {reply.retort}")

        elif rpc_call == 4:
            print("Not implemented yet")
            return greet_pb2.HelloRequest(salutation="Bonjour")

        return None


if __name__ == '__main__':
    run()
