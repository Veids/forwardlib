# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: clientpb/client.proto
# Protobuf Python Version: 4.25.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from tools.commonpb import common_pb2 as commonpb_dot_common__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x15\x63lientpb/client.proto\x12\x08\x63lientpb\x1a\x15\x63ommonpb/common.proto\"!\n\x0c\x45ndpointList\x12\x11\n\tendpoints\x18\x01 \x03(\t\"T\n\x13\x46ileTransferRequest\x12\x1d\n\x05input\x18\x01 \x01(\x0b\x32\x0e.clientpb.Path\x12\x1e\n\x06output\x18\x02 \x01(\x0b\x32\x0e.clientpb.Path\"\x14\n\x04Path\x12\x0c\n\x04path\x18\x01 \x01(\t\"\x19\n\x08\x46ileList\x12\r\n\x05\x66iles\x18\x01 \x03(\t2\xb6\x04\n\tClientRpc\x12-\n\nSocksStart\x12\x0e.commonpb.Addr\x1a\x0f.commonpb.Empty\x12,\n\tSocksStop\x12\x0e.commonpb.Addr\x1a\x0f.commonpb.Empty\x12\x33\n\x0cReverseStart\x12\x12.commonpb.AddrPack\x1a\x0f.commonpb.Empty\x12.\n\x0bReverseStop\x12\x0e.commonpb.Addr\x1a\x0f.commonpb.Empty\x12\x33\n\x0c\x46orwardStart\x12\x12.commonpb.AddrPack\x1a\x0f.commonpb.Empty\x12.\n\x0b\x46orwardStop\x12\x0e.commonpb.Addr\x1a\x0f.commonpb.Empty\x12/\n\x04List\x12\x0f.commonpb.Empty\x1a\x16.clientpb.EndpointList\x12/\n\tListFiles\x12\x0e.clientpb.Path\x1a\x12.clientpb.FileList\x12*\n\x04Glob\x12\x0e.clientpb.Path\x1a\x12.clientpb.FileList\x12:\n\x08\x44ownload\x12\x1d.clientpb.FileTransferRequest\x1a\x0f.commonpb.Empty\x12\x38\n\x06Upload\x12\x1d.clientpb.FileTransferRequest\x1a\x0f.commonpb.EmptyB/Z-github.com/Veids/forwardlib/protobuf/clientpbb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'clientpb.client_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  _globals['DESCRIPTOR']._options = None
  _globals['DESCRIPTOR']._serialized_options = b'Z-github.com/Veids/forwardlib/protobuf/clientpb'
  _globals['_ENDPOINTLIST']._serialized_start=58
  _globals['_ENDPOINTLIST']._serialized_end=91
  _globals['_FILETRANSFERREQUEST']._serialized_start=93
  _globals['_FILETRANSFERREQUEST']._serialized_end=177
  _globals['_PATH']._serialized_start=179
  _globals['_PATH']._serialized_end=199
  _globals['_FILELIST']._serialized_start=201
  _globals['_FILELIST']._serialized_end=226
  _globals['_CLIENTRPC']._serialized_start=229
  _globals['_CLIENTRPC']._serialized_end=795
# @@protoc_insertion_point(module_scope)
