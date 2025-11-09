import grpc.experimental.gevent as grpc_gevent

from grpc import Channel

grpc_gevent.init_gevent()

class GRPCClient:
    def __init__(self, channel: Channel):
        self.channel = channel


