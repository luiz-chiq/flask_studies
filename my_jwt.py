import jwt
from cryptography.hazmat.primitives import serialization

payload_data = {
    "sub": "4242",
    "name": "Jessica Temporal",
    "nickname": "Jess"
}

# read and load the key
private_key = open('.ssh/id_rsa', 'r').read()
key = serialization.load_ssh_private_key(private_key.encode(), password=b'')

my_secret = 'my_super_secret'


token = jwt.encode(
    payload=payload_data,
    key=my_secret
)
print(token)

# jwt.decode(token, "secret", algorithms=["HS256"])