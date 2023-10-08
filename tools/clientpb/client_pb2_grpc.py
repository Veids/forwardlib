# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from tools.clientpb import client_pb2 as clientpb_dot_client__pb2
from tools.commonpb import common_pb2 as commonpb_dot_common__pb2


class ClientRpcStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SocksStart = channel.unary_unary(
                '/clientpb.ClientRpc/SocksStart',
                request_serializer=commonpb_dot_common__pb2.Addr.SerializeToString,
                response_deserializer=commonpb_dot_common__pb2.Empty.FromString,
                )
        self.SocksStop = channel.unary_unary(
                '/clientpb.ClientRpc/SocksStop',
                request_serializer=commonpb_dot_common__pb2.Addr.SerializeToString,
                response_deserializer=commonpb_dot_common__pb2.Empty.FromString,
                )
        self.ReverseStart = channel.unary_unary(
                '/clientpb.ClientRpc/ReverseStart',
                request_serializer=commonpb_dot_common__pb2.AddrPack.SerializeToString,
                response_deserializer=commonpb_dot_common__pb2.Empty.FromString,
                )
        self.ReverseStop = channel.unary_unary(
                '/clientpb.ClientRpc/ReverseStop',
                request_serializer=commonpb_dot_common__pb2.Addr.SerializeToString,
                response_deserializer=commonpb_dot_common__pb2.Empty.FromString,
                )
        self.List = channel.unary_unary(
                '/clientpb.ClientRpc/List',
                request_serializer=commonpb_dot_common__pb2.Empty.SerializeToString,
                response_deserializer=clientpb_dot_client__pb2.EndpointList.FromString,
                )
        self.ListFiles = channel.unary_unary(
                '/clientpb.ClientRpc/ListFiles',
                request_serializer=clientpb_dot_client__pb2.Path.SerializeToString,
                response_deserializer=clientpb_dot_client__pb2.FileList.FromString,
                )
        self.Glob = channel.unary_unary(
                '/clientpb.ClientRpc/Glob',
                request_serializer=clientpb_dot_client__pb2.Path.SerializeToString,
                response_deserializer=clientpb_dot_client__pb2.FileList.FromString,
                )
        self.Download = channel.unary_unary(
                '/clientpb.ClientRpc/Download',
                request_serializer=clientpb_dot_client__pb2.DownloadRequest.SerializeToString,
                response_deserializer=commonpb_dot_common__pb2.Empty.FromString,
                )


class ClientRpcServicer(object):
    """Missing associated documentation comment in .proto file."""

    def SocksStart(self, request, context):
        """*** Socks ***
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SocksStop(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ReverseStart(self, request, context):
        """*** Reverse ***
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ReverseStop(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def List(self, request, context):
        """*** Common ***
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListFiles(self, request, context):
        """*** SFTP ***
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Glob(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Download(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ClientRpcServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SocksStart': grpc.unary_unary_rpc_method_handler(
                    servicer.SocksStart,
                    request_deserializer=commonpb_dot_common__pb2.Addr.FromString,
                    response_serializer=commonpb_dot_common__pb2.Empty.SerializeToString,
            ),
            'SocksStop': grpc.unary_unary_rpc_method_handler(
                    servicer.SocksStop,
                    request_deserializer=commonpb_dot_common__pb2.Addr.FromString,
                    response_serializer=commonpb_dot_common__pb2.Empty.SerializeToString,
            ),
            'ReverseStart': grpc.unary_unary_rpc_method_handler(
                    servicer.ReverseStart,
                    request_deserializer=commonpb_dot_common__pb2.AddrPack.FromString,
                    response_serializer=commonpb_dot_common__pb2.Empty.SerializeToString,
            ),
            'ReverseStop': grpc.unary_unary_rpc_method_handler(
                    servicer.ReverseStop,
                    request_deserializer=commonpb_dot_common__pb2.Addr.FromString,
                    response_serializer=commonpb_dot_common__pb2.Empty.SerializeToString,
            ),
            'List': grpc.unary_unary_rpc_method_handler(
                    servicer.List,
                    request_deserializer=commonpb_dot_common__pb2.Empty.FromString,
                    response_serializer=clientpb_dot_client__pb2.EndpointList.SerializeToString,
            ),
            'ListFiles': grpc.unary_unary_rpc_method_handler(
                    servicer.ListFiles,
                    request_deserializer=clientpb_dot_client__pb2.Path.FromString,
                    response_serializer=clientpb_dot_client__pb2.FileList.SerializeToString,
            ),
            'Glob': grpc.unary_unary_rpc_method_handler(
                    servicer.Glob,
                    request_deserializer=clientpb_dot_client__pb2.Path.FromString,
                    response_serializer=clientpb_dot_client__pb2.FileList.SerializeToString,
            ),
            'Download': grpc.unary_unary_rpc_method_handler(
                    servicer.Download,
                    request_deserializer=clientpb_dot_client__pb2.DownloadRequest.FromString,
                    response_serializer=commonpb_dot_common__pb2.Empty.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'clientpb.ClientRpc', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ClientRpc(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def SocksStart(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/clientpb.ClientRpc/SocksStart',
            commonpb_dot_common__pb2.Addr.SerializeToString,
            commonpb_dot_common__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SocksStop(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/clientpb.ClientRpc/SocksStop',
            commonpb_dot_common__pb2.Addr.SerializeToString,
            commonpb_dot_common__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ReverseStart(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/clientpb.ClientRpc/ReverseStart',
            commonpb_dot_common__pb2.AddrPack.SerializeToString,
            commonpb_dot_common__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ReverseStop(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/clientpb.ClientRpc/ReverseStop',
            commonpb_dot_common__pb2.Addr.SerializeToString,
            commonpb_dot_common__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def List(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/clientpb.ClientRpc/List',
            commonpb_dot_common__pb2.Empty.SerializeToString,
            clientpb_dot_client__pb2.EndpointList.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ListFiles(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/clientpb.ClientRpc/ListFiles',
            clientpb_dot_client__pb2.Path.SerializeToString,
            clientpb_dot_client__pb2.FileList.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Glob(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/clientpb.ClientRpc/Glob',
            clientpb_dot_client__pb2.Path.SerializeToString,
            clientpb_dot_client__pb2.FileList.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Download(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/clientpb.ClientRpc/Download',
            clientpb_dot_client__pb2.DownloadRequest.SerializeToString,
            commonpb_dot_common__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)