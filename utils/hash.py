import hashlib

def hash_sha256_then_md5_then_sha1_and_sha512(data: str) -> str:
    sha256_hash = hashlib.sha256(data.encode()).hexdigest()
    md5_hash = hashlib.md5(sha256_hash.encode()).hexdigest()    
    sha1_hash = hashlib.sha1(md5_hash.encode()).hexdigest()
    sha512_hash = hashlib.sha512(sha1_hash.encode()).hexdigest()
    
    return sha512_hash


#print(hash_sha256_then_md5_then_sha1_and_sha512("123"))
