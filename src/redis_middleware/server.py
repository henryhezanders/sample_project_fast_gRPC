# gRPC microservice
import hmac
from common.settings import settings
import redis
from concurrent import futures
import grpc
from proto import token_service_pb2
from proto import token_service_pb2_grpc
import logging

# Create a handler
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()

# Set the level of logging you want
handler.setLevel(logging.INFO)

# Set the logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(handler)

class TokenServiceServicer(token_service_pb2_grpc.TokenServiceServicer):
    def __init__(self):
        self.redis_client = redis.Redis(host=settings.redis_host, port=settings.redis_port, db=settings.redis_db)

    def StoreToken(self, request, context):
        # Create token
        logger.info("storing token")
        token = ""

        # Store in Redis with expiration
        self.redis_client.setex(request.token_uuid, 86400, token)

        return token_service_pb2.StoreTokenResponse(success=True)

def serve():
    logger.info("starting server")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    token_service_pb2_grpc.add_TokenServiceServicer_to_server(TokenServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()