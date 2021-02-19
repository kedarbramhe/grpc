import keyval_pb2_grpc
import keyval_pb2
from concurrent import futures
import time
import math
import logging
import grpc
import utils
import argparse
import time

class KeyValueServicer(keyval_pb2_grpc.KeyValueServicer):

    def __init__(self, server_id, delay) :
        self.server_id = int(server_id)
        self.delay = int(delay)
        self.filename = 'keyval-{}.json'.format(server_id)
        self.db = utils.read_keyval_database(filename= self.filename) 

    def Read(self,request,context):
        if request.key not in self.db.keys():
            return keyval_pb2.ReadResponse(status=keyval_pb2.Status(server_id=self.server_id,
                                            ok=False,
                                            error='Read aborted. Key not present {}'.format(request.key)),
                                        key=None,
                                        value= None,
                                        current_version= None)
                                        
        statusObject = keyval_pb2.Status(server_id=self.server_id,ok=True) #,error='none'
        item  = self.db[request.key]
        return keyval_pb2.ReadResponse(status=statusObject,
                                        key=item.key,
                                        value= item.value,
                                        current_version= item.current_version)

    def Write(self, request, context):
        print('write_started')
        # adding the write-delay passed as an argument
        time.sleep(self.delay)
        statusObject = keyval_pb2.Status(server_id=self.server_id,ok=True) #,error='none'
        self.db[request.key] = keyval_pb2.Entry(key= request.key,
                                                value= request.value,
                                                current_version=request.current_version)
        # utils.save_keyval_database(self.db, self.filename)
        print('write_done')
        return keyval_pb2.WriteResponse(status=statusObject,
                                        key=request.key,new_version=request.current_version)

    def Delete(self, request, context):
        statusObject = keyval_pb2.Status(server_id=self.server_id,ok=True) #,error='none'
        item  = self.db[request.key]
        del self.db[request.key]
        # utils.save_keyval_database(self.db, self.filename)
        return keyval_pb2.DeleteResponse(status=statusObject,
                                        key=request.key, 
                                        deleted_value = item.value,
                                        deleted_version = item.current_version)

    def List(self, request, context):
        statusObject = keyval_pb2.Status(server_id=self.server_id,ok=True)  #,error='none'
        entries = []
        for key,val in self.db.items():
            entries.append({"key": key, 
                            "value":val.value,
                            "current_version":val.current_version})
        
        return keyval_pb2.ListResponse(status = statusObject, entries = entries)

def serve(port, server_id, delay):
    print('server port:{} server_id : {}'.format(port, server_id))
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    keyval_pb2_grpc.add_KeyValueServicer_to_server(KeyValueServicer(server_id=server_id,
                                                                    delay = delay),
                                                         server)
    server.add_insecure_port('[::]:{}'.format(port))
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='ArgumentParser')
    parser.add_argument('--server_id', action="store", dest='server_id', default=1)
    parser.add_argument('--write_delay', action="store", dest='delay', default=0)
    parser.add_argument('--port ', action="store", dest='port', default='50050')
    args = parser.parse_args()
    logging.basicConfig()
    serve(port = args.port, 
        server_id = args.server_id,
        delay = args.delay)
          
