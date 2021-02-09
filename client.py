from __future__ import print_function

import random
import logging

import grpc

import keyval_pb2
import keyval_pb2_grpc

# Read: For a given key, return the corresponding value and version stored in the dictionary. Return an error if the key does not exist in the table. It is also an error to not specify the key in the Read request.

def get_value(stub,key):
    request = keyval_pb2.ReadRequest(key=key)
    response = stub.Read(request)
    if response:
        print("value is {} and version stored is {}".format(response.value, response.current_version))

def write_value(stub, key, value):
    request = keyval_pb2.WriteRequest(key= key, value = value, current_version = 1)
    response = stub.Write(request)
    if response:
        print('Sucessfully added key value pair({}:{})'.format(key,value))
    else:
        print('Error')

def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = keyval_pb2_grpc.KeyValueStub(channel)
        print("-------------- GetValue --------------")
        get_value(stub,'1')
        write_value(stub, 'a12', '1')
        # print("-------------- ListFeatures --------------")
        # guide_list_features(stub)
        # print("-------------- RecordRoute --------------")
        # guide_record_route(stub)
        # print("-------------- RouteChat --------------")
        # guide_route_chat(stub)


if __name__ == '__main__':
    logging.basicConfig()
    run()
