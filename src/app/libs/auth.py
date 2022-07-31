import hashlib
import config
import random
import string

def password_hash(password: str) -> str:
    try:
        md5 = hashlib.md5(config.PASSWORD_SALT.encode('utf8'))
        md5.update(password.encode('utf8'))
        hashed_password = md5.hexdigest()
        return hashed_password
    except Exception as e:
        print('[Error] ', e)

def new_token() -> str:
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32)).lower()