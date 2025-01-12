import bcrypt
import time

def hash_password(usr_password : str) -> str:
    generate_salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(usr_password.encode('utf-8'), generate_salt)
    return hashed_password.decode('utf-8')

def verify_password(stored_password : str, provided_password : str) -> bool:
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password.encode('utf-8'))


def get_transaction_id(name) -> str:
    return f"TNX-{name}-{str(int(time.time()))}"