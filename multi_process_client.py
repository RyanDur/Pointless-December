import multiprocessing
import time

import grpc

import greet_pb2
import greet_pb2_grpc


def get_person_1_client_stream_function():
    responses = ["Alice 1", "Bob 1", "Charlie 1"]
    for response in responses:
        yield greet_pb2.HelloRequest(salutation=response)


def get_person_2_client_stream_function():
    responses = ["Dave 2", "Eve 2", "Frank 2"]
    for response in responses:
        yield greet_pb2.HelloRequest(salutation=response)


def make_grpc_call(stream_function):
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = greet_pb2_grpc.GreeterStub(channel)
        responses = stub.InteractingHello(stream_function())

        for response in responses:
            print("Received reply:")
            print(response)


if __name__ == '__main__':
    request_data_list = [
        get_person_1_client_stream_function,
        get_person_2_client_stream_function,
        # ... more requests
    ]

    with multiprocessing.Pool(processes=4) as pool:
        results = pool.map(make_grpc_call, request_data_list)

    print(results)
