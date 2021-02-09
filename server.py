import keyval_pb2_grpc
import keyval_pb2
from concurrent import futures
import time
import math
import logging
import grpc
import utils

class KeyValueServicer(keyval_pb2_grpc.KeyValueServicer):

    def __init__(self):
        self.db = utils.read_keyval_database()





    def Read(self,request,context):
        #request in the key value
        #message Status {
        #          int32 server_id = 1; // Id of the server that is responding
        #            bool ok = 2; // If the request executed successfully at the server
        #              string error = 3; // if ok == False, a human-readable eror string
        #              }
        statusObject = keyval_pb2.Status(server_id=1,ok=True,error='none')
        item  = self.db[request.key]
        print(item)
        return keyval_pb2.ReadResponse(status=statusObject,key='0',value='0',current_version=0)
        #return keyval_pb2.Entry(key=item['key'],value=item['value'],current_version=item['current_version'])
        #print(self.db[request.key])
        # for entry in self.db:
        #     print(entry)
        #     print(request)
        #     if entry == request:
        #         return entry
        #     else :
        #         return keyval_pb2.Entry(key='0',value='0',current_version=0)
    
def serve():
            server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
            keyval_pb2_grpc.add_KeyValueServicer_to_server(KeyValueServicer(), server)
            server.add_insecure_port('[::]:50051')
            server.start()
            server.wait_for_termination()

if __name__ == '__main__':
            logging.basicConfig()
            serve()
          
