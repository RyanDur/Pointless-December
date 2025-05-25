from concurrent import futures
from unittest.mock import patch

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

@pytest.mark.asyncio
def test_greet_unary_stream():
    with grpc.insecure_channel('localhost:50051') as channel:
        client = greet_pb2_grpc.GreeterStub(channel)
        hello_request = greet_pb2.HelloRequest(salutation="Bonjour")
        hello_replies = client.ParrotSayHello(hello_request)
        replies = [reply.retort for reply in hello_replies]
        assert replies == ["Server says: Chirp Chirp! 0", "Server says: Chirp Chirp! 1", "Server says: Chirp Chirp! 2"]

def test_greet_stream_unary():
    with grpc.insecure_channel('localhost:50051') as channel:
        client = greet_pb2_grpc.GreeterStub(channel)

        def get_client_stream_function():
            for name in ["Alice", "Bob", "Charlie"]:
                yield greet_pb2.HelloRequest(salutation=name)

        delayed_reply = client.ChattyClientSaysHello(get_client_stream_function())
        assert delayed_reply.message == "You have sent 3 messages. Please expect a delayed response."
        assert len(delayed_reply.request) == 3
        assert delayed_reply.request[0].salutation == "Alice"
        assert delayed_reply.request[1].salutation == "Bob"
        assert delayed_reply.request[2].salutation == "Charlie"