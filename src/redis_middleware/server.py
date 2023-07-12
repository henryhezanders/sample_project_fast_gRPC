# gRPC microservice
import hmac
from redis_middleware.common.settings import settings
import redis
from concurrent import futures
import grpc
from proto import token_service_pb2
from proto import token_service_pb2_grpc

class TokenServiceServicer(token_service_pb2_grpc.TokenServiceServicer):
    def __init__(self):
        self.redis_client = redis.Redis(host=settings.redis_host, port=settings.redis_port, db=settings.redis_db)

    def StoreToken(self, request, context):
        # Create token
        token = ""

        # Store in Redis with expiration
        self.redis_client.setex(request.token_uuid, 86400, token)

        return token_service_pb2.StoreTokenResponse(success=True)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    token_service_pb2_grpc.add_TokenServiceServicer_to_server(TokenServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()