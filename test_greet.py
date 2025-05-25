from concurrent import futures

import grpc
import pytest

import greet_pb2
import greet_pb2_grpc


@pytest.mark.asyncio
async def test_greet_unary_unary():
    with grpc.insecure_channel('localhost:50051') as channel:
        client = greet_pb2_grpc.GreeterStub(channel)
        hello_request = greet_pb2.HelloRequest(salutation="Bonjour")
        hello_reply = client.SayHello(hello_request)
        assert hello_reply.retort == "Hola!"
