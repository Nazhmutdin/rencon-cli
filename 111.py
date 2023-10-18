from hashlib import sha256


message = "Hello, world!"


print(sha256(message.encode()).hexdigest())