import hashlib
import os

def check_admin_password(input_password: str, stored_hash: str = None) -> bool:
    """Cek input password match dengan hash di .env."""
    if stored_hash is None:
        stored_hash = os.getenv("ADMIN_HASH")
        if not stored_hash:
            raise ValueError("ADMIN_HASH belum diset di .env~ 😔")
    
    # Hitung hash sama persis seperti generator
    layer1 = hashlib.sha512(input_password.encode('utf-8')).hexdigest()
    layer2 = hashlib.sha3_512(layer1.encode('utf-8')).hexdigest()
    computed_hash = hashlib.blake2b(layer2.encode('utf-8'), digest_size=64).hexdigest()
    
    return computed_hash == stored_hash