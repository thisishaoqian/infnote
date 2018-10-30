# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import manage_server_pb2 as manage__server__pb2


class ManageStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.run_command = channel.unary_stream(
        '/build.Manage/run_command',
        request_serializer=manage__server__pb2.Command.SerializeToString,
        response_deserializer=manage__server__pb2.Result.FromString,
        )


class ManageServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def run_command(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_ManageServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'run_command': grpc.unary_stream_rpc_method_handler(
          servicer.run_command,
          request_deserializer=manage__server__pb2.Command.FromString,
          response_serializer=manage__server__pb2.Result.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'build.Manage', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))


class BlockchainStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.create_block = channel.unary_unary(
        '/build.Blockchain/create_block',
        request_serializer=manage__server__pb2.Payload.SerializeToString,
        response_deserializer=manage__server__pb2.Block.FromString,
        )


class BlockchainServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def create_block(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_BlockchainServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'create_block': grpc.unary_unary_rpc_method_handler(
          servicer.create_block,
          request_deserializer=manage__server__pb2.Payload.FromString,
          response_serializer=manage__server__pb2.Block.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'build.Blockchain', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))