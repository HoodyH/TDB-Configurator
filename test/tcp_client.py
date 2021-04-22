
import socket

# hostname, sld, tld, port = 'www', 'integralist', 'co.uk', 80
# target = '{}.{}.{}'.format(hostname, sld, tld)
port = 8080
target = "172.20.0.34"

# create an ipv4 (AF_INET) socket object using the tcp protocol (SOCK_STREAM)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect the client
client.connect((target, port))
# client.connect(('0.0.0.0', 9999))

# send some data
URI_REG = "/api/devices/tdbase/tag/"
HTTP_PROTOCOL = "HTTP/1.0\r\nContent-type: application/json\r\n"
content_length = 128
serial_number = "S123456789012"
x_encription = 1
body = '"2019/05/14 09:04:01;0011024402;1;0000;1""2019/05/14 09:04:03;0011056143;1;0000;1"'

client.send("POST {} {}Content-Length: {}\r\nX-Serial-Number: {}\r\nX-Encription: {}\r\n\r\n{}".format(
    URI_REG,
    HTTP_PROTOCOL,
    content_length,
    serial_number,
    x_encription,
    body).encode("Latin1"))

# receive the response data
response = client.recv(4096)

print(response)
