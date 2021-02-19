from __future__ import print_function

import random
import logging

import grpc

import keyval_pb2
import keyval_pb2_grpc
import time
import argparse
# Read: For a given key, return the corresponding value and version stored in the dictionary. Return an error if the key does not exist in the table. It is also an error to not specify the key in the Read request.



def get_value(stub,key):
    request = keyval_pb2.ReadRequest(key=key)
    response = stub.Read(request)
    return response
    # print(response)
    # if response:
    #     print("value is"+response.value+" and version stored is"+response.current_version)

def read_value(stub,entry):
    response = get_value(stub,entry['key'])
    if response.status.ok!=True:
        # non existence key read 
        return (response)
    else :
        #  normal read
        return (response)

def write_value(stub,entry,delay):
    if delay==None:
        delay = 0
    # check if the key already exists 
    if(entry['current_version']<0):
        #blind write
        try:
            response_  = stub.Write(keyval_pb2.WriteRequest(key=entry['key'],value=entry['value'],current_version=1),timeout=delay)
        except grpc.RpcError as exception:
            return exception
        return (response_)
        # return
    
    # check if value already exist
    response = get_value(stub,entry['key'])
    
    if response.status.ok!=True:
        # the values does not exist
        # we can write the new pair with current_version =1
        if(entry['current_version']==1):
            response_  = Stub.Write(keyval_pb2.WriteRequest(key=entry['key'],value=entry['value'],current_version=1))
            if response_.status.ok!=True:
                return (response_.status.error)
            else:
                return (response_)
        else:
            # new value but version mismatch
            errorMessage = 'Write aborted. Record missing but Write expected value to exist at version 1'
            statusObject = keyval_pb2.Status(server_id=1,ok=False,error=errorMessage)
            response___ = keyval_pb2.WriteResponse(status=statusObject,key=entry['key'],new_version=entry['current_version'])
            return (response___)
    else :
        # the values exists
        #  now we have check if the version number matches
        if response.current_version == entry['current_version']:
            # we can change the value
            new_version = entry['current_version']+1
            response_  = stub.Write(keyval_pb2.WriteRequest(key=entry['key'],value=entry['value'],current_version=new_version))
            return response_
        else:
            # show error that the current version does not match
            errorMessage = 'Write aborted. Record version mismatch. Expected = '+str(response.current_version)+', Actual = '+str(entry['current_version'])
            statusObject = keyval_pb2.Status(server_id=1,ok=False,error=errorMessage)
            response___ = keyval_pb2.WriteResponse(status=statusObject,key=entry['key'],new_version=entry['current_version'])
            return (response___)

def get_list(stub):
    response = stub.List(keyval_pb2.ListRequest())
    return (response)

def delete_value(stub,entry): #only key and current_version is passed for the delete operation
    # check for the value
    if entry['current_version'] == 0:
        # throw error
        errorMessage = 'Delete aborted . current_version cannot be 0'
        statusObject = keyval_pb2.Status(server_id=1,ok=False,error=errorMessage)
        return keyval_pb2.WriteResponse(status=statusObject)
        
    response = get_value(stub,entry['key'])
    if response.status.ok!=True:
        # values does not exist
        errorMessage = 'Key not present '+entry['key']
        statusObject = keyval_pb2.Status(server_id=1,ok=False,error=errorMessage)
        return keyval_pb2.WriteResponse(status=statusObject)
    else:
        # value present 
        # check for the version mismatch
        if response.current_version == entry['current_version']:
            # perform delete operation
            response_ = stub.Delete(keyval_pb2.DeleteRequest(key=entry['key'],current_version=entry['current_version']))  
            return (response_)
        else:
            # show the error message of version mismatch
            errorMessage = 'Delete aborted. Record version mismatch: Expected = '+str(response.current_version)+', Actual = '+str(entry['current_version'])
            statusObject = keyval_pb2.Status(server_id=1,ok=False,error=errorMessage)
            response___ = keyval_pb2.WriteResponse(status=statusObject,key=entry['key'],new_version=entry['current_version'])
            return (response___)  



def run():


    with grpc.insecure_channel('localhost:500051') as channel:
        stub = keyval_pb2_grpc.KeyValueStub(channel)

        parser = argparse.ArgumentParser(description='ArgumentParser')
        parser.add_argument('--write_timeout', action="store", dest='timeout', default=0)
        args = parser.parse_args()
        timeout = float(args.timeout)
        # print("-------------------------------------------------------------------") 
        # print("EXPERIMENT 1")
        
        # # send 5 blind writes with timeouts 0.5 seconds
        # print('Sending write request')
        # for i in [0,1,2,3,4]:
        #     keyName = "Key"+str(i)
        #     valueName = "Value"+str(i)
        #     print(write_value(stub,{'key':keyName,'value':valueName,'current_version':-1},timeout))

        # # sleep for 5 seconds

        # time.sleep(5)

        # #  List results 

        # print("List result:")
        # print(get_list(stub))
        
        # print('Sending delete request')
        # for i in [0,1,2,3,4]:
        #     keyName = "Key"+str(i)
        #     valueName = "Value"+str(i)
        #     print(delete_value(stub,{'key':keyName,'current_version':-1})) 

        print("-------------------------------------------------------------------") 
        print("EXPERIMENT 2")
        keyName = "Key1"
        valueName = "Value1"
        print(write_value(stub,{'key':keyName,'value':valueName,'current_version':-1},timeout))
        print(delete_value(stub,{'key':keyName,'current_version':-1})) 
        time.sleep(1)
        print("List result:")
        print(get_list(stub))

        
        # # operations to be performed
        # # Blind write: Write Key1, Value1 with no version check
        # print("Write result:")
        # print(write_value(stub,{'key':'Key1','value':'Value1','current_version':-1}))
        
        # # Normal write: Write Key1, Value1 expecting the current version to be 1                                                                                                                
        # print("-------------------------------------------------------------------")
        # print("Write result:")
        # print(write_value(stub,{'key':'Key1','value':'Value1','current_version':1}))
        
        # # Version check failure: Write Key1, Value3 expecting the current version to be 1                                                                                                                                                                                          
        # print("-------------------------------------------------------------------")
        # print("Write result:")
        # print(write_value(stub,{'key':'Key1','value':'Value3','current_version':1}))
        
        # # Version failure with key missing: Write Key2, Value3, 1                                                                                                
        # print("-------------------------------------------------------------------")
        # print("Write result:")
        # print(write_value(stub,{'key':'Key2','value':'Value3','current_version':2}))
        
        # # Normal read: Read Key1     
        # print("-------------------------------------------------------------------")
        # print("Read result:")
        # print(read_value(stub,{'key':'Key1'}))
                                                                                                                  
        # # Non-existing key read: Read Key2
        # print("-------------------------------------------------------------------")
        # print("Read result:")
        # print(read_value(stub,{'key':'Key2'}))

        # # Get full state with List: List
        # print("-------------------------------------------------------------------")
        # print("List result:")
        # print(get_list(stub))
                                                                                                                       
        # # Add new element as a blind write: Write Key3, Value3                                                                                       
        # print("-------------------------------------------------------------------")
        # print("Write result:")
        # print(write_value(stub,{'key':'Key3','value':'Value3','current_version':-1}))
        
        # # Get full state with List: List                                                                                                                       
        # print("-------------------------------------------------------------------")
        # print("List result:")
        # print(get_list(stub))
        
        # # Delete with version check failure: Delete Key1 with current_version stated as 1
        # print("-------------------------------------------------------------------")
        # print("Delete result:")
        # print(delete_value(stub,{'key':'Key1','current_version':1}))
        
        # # Normal delete: Delete Key1 with current_version stated as 2                                                                                                   
        # print("-------------------------------------------------------------------")
        # print("Delete result:")
        # print(delete_value(stub,{'key':'Key1','current_version':2}))
        
        # # Delete of a non-existent key: Delete Key1 with current_version as 2                                                                                                  
        # print("-------------------------------------------------------------------")
        # print("Delete result:")
        # print(delete_value(stub,{'key':'Key1','current_version':2}))
        
        # # Delete last element: Delete Key3 with current_version as 1
        # print("-------------------------------------------------------------------")
        # print("Delete result:")
        # print(delete_value(stub,{'key':'Key3','current_version':1}))
        
        # # Get full state with List: List
        # print("-------------------------------------------------------------------")
        # print("List result:")
        # print(get_list(stub))
            

if __name__ == '__main__':
    logging.basicConfig()
    run()
