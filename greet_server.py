from concurrent import futures
import time

import grpc
import greet_pb2
import greet_pb2_grpc


class GreeterServicer(greet_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        print(f"Received request {request}")
        time.sleep(2)  # Simulate a long-running process
        return greet_pb2.HelloReply(retort="Hola!")

    def ParrotSayHello(self, request, context):
        print(f"Received request: {request}")
        for i in range(3):
            print(f"Sending reply {i + 1}")
            yield greet_pb2.HelloReply(retort=f"Server says: Chirp Chirp! {i}")
            time.sleep(1)

    def ChattyClientSaysHello(self, request_iterator, context):
        delayed_reply = greet_pb2.DelayedReply()
        for request in request_iterator:
            print(f"Received request from {request.salutation}")
            print(request)
            delayed_reply.request.append(request)

        delayed_reply.message = f"You have sent {len(delayed_reply.request)} messages. Please expect a delayed response."
        return delayed_reply

    def InteractingHello(self, request_iterator, context):
        for request in request_iterator:
            yield print(f"Received request from {request.salutation}")
            time.sleep(2)
        print("Finished processing all requests.")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    greet_pb2_grpc.add_GreeterServicer_to_server(GreeterServicer(), server)
    server.add_insecure_port('localhost:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    print("Starting gRPC server...")
    serve()
