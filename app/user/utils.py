import hashlib

def hash_password(p: str) -> str:
    # TODO: salt?
    return hashlib.sha1(p.encode()).hexdigest()
