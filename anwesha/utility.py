import hashlib

def hashpassword(password):
    return hashlib.sha256(password.encode()).hexdigest()

