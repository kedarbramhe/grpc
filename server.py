import keyval_pb2_grpc
import keyval_pb2
from concurrent import futures
import time
import math
import logging
import grpc

class KeyValueServicer(keyval_pb2_grpc.KeyValueServicer):
    def Read(self,request,context):
        #request in the key value
        for entry in self.db:
            if entry.key == request:
                return entry
            else :
                return keyval_pb2.Entry(key='0',value='0',current_version=0)
    
def serve():
            server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
            keyval_pb2_grpc.add_KeyValueServicer_to_server(KeyValueServicer(), server)
            server.add_insecure_port('[::]:50051')
            server.start()
            server.wait_for_termination()

if __name__ == '__main__':
            logging.basicConfig()
            serve()
          
