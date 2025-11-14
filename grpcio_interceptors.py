import grpc
from contracts.services.gateway.users.rpc_get_user_pb2 import GetUserRequest
from contracts.services.gateway.users.users_gateway_service_pb2_grpc import UsersGatewayServiceStub



class SimpleLoggingInterceptor(grpc.UnaryUnaryClientInterceptor):
    def intercept_unary_unary(self, continuation, client_call_details, request):
        print(client_call_details, type(client_call_details))
        print(f"Calling method: {client_call_details.method}")
        response = continuation(client_call_details, request)
        return response

channel = grpc.insecure_channel("localhost:9003")
intercept_channel = grpc.intercept_channel(channel, SimpleLoggingInterceptor())

stub = UsersGatewayServiceStub(intercept_channel)

request = GetUserRequest(id="63bc6c94-3b69-419d-949a-1c21efc304e7")
response = stub.GetUser(request)

print(response)