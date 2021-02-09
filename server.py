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
        statusObject = keyval_pb2.Status(server_id=1,ok=True,error='none')
        item  = self.db[request.key]
        return keyval_pb2.ReadResponse(status=statusObject,
                                        key=item.key,
                                        value= item.value,
                                        current_version= item.current_version)

    def Write(self, request, context):
        statusObject = keyval_pb2.Status(server_id=1,ok=True,error='none')
        self.db[request.key] = keyval_pb2.Entry(key= request.key,
                                                value= request.value,
                                                current_version=request.current_version)
        utils.save_keyval_database(self.db)
        return keyval_pb2.WriteResponse(status=statusObject,
                                        key=request.key)

    def Delete(self, request, context):
        statusObject = keyval_pb2.Status(server_id=1,ok=True,error='none')
        item  = self.db[request.key]
        del self.db[request.key]
        utils.save_keyval_database(self.db)
        return keyval_pb2.DeleteResponse(status=statusObject,
                                        key=request.key, 
                                        deleted_value = item.value,
                                        deleted_version = item.current_version)

    def List(self, request, context):
        statusObject = keyval_pb2.Status(server_id=1,ok=True,error='none')
        entries = []
        for key,val in self.db.items():
            entries.append({"key": key, 
                            "value":val.value,
                            "current_version":val.current_version})
        
        return keyval_pb2.ListResponse(status = statusObject, entries = entries)

def serve():
            server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
            keyval_pb2_grpc.add_KeyValueServicer_to_server(KeyValueServicer(), server)
            server.add_insecure_port('[::]:50051')
            server.start()
            server.wait_for_termination()

if __name__ == '__main__':
            logging.basicConfig()
            serve()
          
