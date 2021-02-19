from keyval_client_group01 import get_list, get_value, write_value
import random
import logging

import grpc

import keyval_pb2
import keyval_pb2_grpc

def run_sharder():
    channel1 = grpc.insecure_channel('localhost:50050')
    channel2 = grpc.insecure_channel('localhost:50051')

    stub1 = keyval_pb2_grpc.KeyValueStub(channel1)
    stub2 = keyval_pb2_grpc.KeyValueStub(channel2)
    for i in range(0,10):
        key = 'ShardKey{}'.format(i)
        value = 'Value{}'.format(i)
        if i % 2 == 0:
            response = write_value(stub2,{'key':key,'value': value,'current_version': -1})
            print('Write result:')
            print(response)
            print('-------------------------------------------------------------------')
        else:
            response  = write_value(stub1,{'key':key,'value':value,'current_version': -1})
            print('Write result:')
            print(response)
            print('-------------------------------------------------------------------')
    print('List result:')
    print(get_list(stub1))
    print('-------------------------------------------------------------------')
    print('List result:')
    print(get_list(stub2))
    print('-------------------------------------------------------------------')


if __name__ == '__main__':
    logging.basicConfig()
    run_sharder()