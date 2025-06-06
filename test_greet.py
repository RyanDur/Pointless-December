import grpc
import pytest

import greet_pb2
import greet_pb2_grpc


@pytest.fixture()
def client():
    with grpc.insecure_channel('localhost:50051') as channel:
        yield greet_pb2_grpc.GreeterStub(channel)


@pytest.mark.asyncio
async def test_greet_unary_unary(client):
    hello_request = greet_pb2.HelloRequest(salutation="Bonjour")
    hello_reply = client.SayHello(hello_request)
    assert hello_reply.retort == "Hola!"


def test_greet_unary_stream(client):
    hello_request = greet_pb2.HelloRequest(salutation="Bonjour")
    hello_replies = client.ParrotSayHello(hello_request)
    replies = [reply.retort for reply in hello_replies]
    assert replies == ["Server says: Chirp Chirp! 0", "Server says: Chirp Chirp! 1", "Server says: Chirp Chirp! 2"]


def test_greet_stream_unary(client):
    def get_client_stream_function():
        for name in ["Alice", "Bob", "Charlie"]:
            yield greet_pb2.HelloRequest(salutation=name)

    delayed_reply = client.ChattyClientSaysHello(get_client_stream_function())
    assert delayed_reply.message == "You have sent 3 messages. Please expect a delayed response."
    assert len(delayed_reply.request) == 3
    assert delayed_reply.request[0].salutation == "Alice"
    assert delayed_reply.request[1].salutation == "Bob"
    assert delayed_reply.request[2].salutation == "Charlie"


def test_greet_stream_stream(client):
    def get_client_stream_function():
        for name in ["Alice", "Bob", "Charlie"]:
            yield greet_pb2.HelloRequest(salutation=name)

    responses = client.InteractingHello(get_client_stream_function())
    expected_responses = [
        "Hello Alice, how are you?",
        "Hello Bob, how are you?",
        "Hello Charlie, how are you?"
    ]
    for response, expected in zip(responses, expected_responses):
        assert response.retort == expected
