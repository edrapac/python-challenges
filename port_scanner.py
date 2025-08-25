from marshmallow import Schema, fields, validate, ValidationError, post_load
# we will want to deserialize - take a dict, validate, and then turn it into a Scan object 
# we can then call the Scan methods which will be the bulk of the actual scanning logic

import socket
import concurrent.futures
import sys
from ipaddress import ip_address
def validate_ip(value):
    try:
        ip_address(value)  # accepts IPv4 or IPv6
    except ValueError as e:
        raise ValidationError("Not a valid IP address") from e

class RequestSchema(Schema):
    target = fields.String(required=True, 
                           # we can use validate.Regexp to validate an object is correct before serializing
                           validate =validate_ip)
    start_port = fields.Integer(required=True,
                                validate = validate.Range(min=1,max=65535))
    end_port = fields.Integer(required=True,
                                validate = validate.Range(min=1,max=65535))
    thread_count = fields.Integer(validate = validate.Range(min=1,max=100))


    @post_load
    def makeRequest(self,data,**kwargs):
        return Scan(**data)

class OutputSchema(Schema):
    host = fields.Str()
    port = fields.Int()
    output = fields.Str()

class ScanSchema(Schema):
    output = fields.List(fields.Nested(OutputSchema))
    
    @post_load
    def makeScan(self,data,**kwargs):
        return Scan(**data)



class Scan:
    def __init__(self, target, start_port,end_port,thread_count):
        self.target = target
        self.start_port = start_port
        self.end_port = end_port
        self.thread_count = thread_count
    
    def run__pool(self):
        result_output = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.thread_count) as pool:
            if self.start_port < self.end_port:
                scan_range = list(range(self.start_port,(self.end_port+1)))
                result_output = list(pool.map(self.scan,scan_range))
            else:
                print('Error, start port must be less than endport')
                sys.exit(1)
        return result_output

            

    
    def scan(self,port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)
        output = s.connect_ex((self.target, port))
        if output ==0:
            output = 'Open'
        else:
            output ='Closed'
        result = {"host":self.target,"port":port,"output":output}
        return result

scan_data = {'target':'127.0.0.1','start_port':8080,'end_port':8083,'thread_count':3}
request_schema = RequestSchema()
newRequest = request_schema.load(scan_data)
print(newRequest.run__pool())