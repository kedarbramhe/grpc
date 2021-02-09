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

def delete_key(stub, key):
    request = keyval_pb2.DeleteRequest(key= key, current_version = 1)
    response = stub.Delete(request)
    if response:
        print('Sucessfully deleted key {}'.format(response.key))
    else:
        print('Error')

def list_entries(stub):
    request = keyval_pb2.ListRequest()
    response = stub.List(request)
    if response:
        print("Entries: {}".format(response.entries))




def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = keyval_pb2_grpc.KeyValueStub(channel)
        print("-------------- GetValue --------------")
        write_value(stub, 'a1', '1')
        write_value(stub, 'a2', '11')
        write_value(stub, 'a3', '111')
        list_entries(stub)
        delete_key(stub, 'a3')
        delete_key(stub, 'a2')
        list_entries(stub)


if __name__ == '__main__':
    logging.basicConfig()
    run()
