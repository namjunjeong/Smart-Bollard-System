# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import result_pb2 as result__pb2


class ResultStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Require = channel.unary_stream(
                '/result.Result/Require',
                request_serializer=result__pb2.Req.SerializeToString,
                response_deserializer=result__pb2.Res.FromString,
                )
        self.Option = channel.unary_stream(
                '/result.Result/Option',
                request_serializer=result__pb2.Req.SerializeToString,
                response_deserializer=result__pb2.OptVal.FromString,
                )


class ResultServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Require(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Option(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ResultServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Require': grpc.unary_stream_rpc_method_handler(
                    servicer.Require,
                    request_deserializer=result__pb2.Req.FromString,
                    response_serializer=result__pb2.Res.SerializeToString,
            ),
            'Option': grpc.unary_stream_rpc_method_handler(
                    servicer.Option,
                    request_deserializer=result__pb2.Req.FromString,
                    response_serializer=result__pb2.OptVal.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'result.Result', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Result(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Require(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/result.Result/Require',
            result__pb2.Req.SerializeToString,
            result__pb2.Res.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def Option(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(request, target, '/result.Result/Option',
            result__pb2.Req.SerializeToString,
            result__pb2.OptVal.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
