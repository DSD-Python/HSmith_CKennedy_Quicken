from pathlib import Path
import platform
import base64
from subprocess import CalledProcessError, run

import keyring
# import nacl.secret
from nacl.secret import SecretBox
from nacl.signing import SigningKey


def b_2_s(b):
    return str(base64.urlsafe_b64encode(b))[2:-1]


def s_2_b(s):
    return base64.urlsafe_b64decode(s)


def read_secret_string():
    """Returns the secret string."""
    if platform.system() == "Darwin":
        return from_keychain()
    elif platform.system() == "Windows":
        return from_locker()


def write_secret_string(secret_string):
    """Writes the secret string."""
    if platform.system() == "Darwin":
        to_keychain(secret_string)
    elif platform.system() == "Windows":
        to_locker(secret_string)
    return 


def create_secret_and_save():
    b = bytes(SigningKey.generate())
    secret_key_string = b_2_s(b)
    write_secret_string(secret_key_string)


def to_locker(secret_key_string):
    """Save a secret key string to Windows Credential locker."""
    try:
        keyring.set_password(
        "symetric_encryption_secret",
        "test",
        secret_key_string,
        )
        return True
    except:
        print("""
Key creation failed. One possible cause is that there already 
exists a key in the Credential Locker with these identifiers. 
If there is such a key and you want to replace it, use the
Credential Manager to delete the one that is there and try again."""
        )
        return
        

def from_locker():
    """Retrieve secret key string from Windows Credential locker."""
    try:
        return keyring.get_password("symetric_encryption_secret", "test")
    except:
        print(
            "The key doesn't exist. If you haven't done so, "
            "generate keys first."
            "If you have lost your keys, generate a new key pair."
        )
        return


def to_keychain(secret_key_string):
    """Save secret key string to keychain"""
    arg_list = [
        "/usr/bin/security",
        "add-generic-password",
        "-s",
        "key_for_symmetric_encryption",
        "-a",
        "test",
        "-w",
        secret_key_string,
        "login.keychain-db",
    ]
    try:
        run(arg_list, check=True, text=True, capture_output=True)
        return True
    except CalledProcessError as e:
        print("""
Key creation failed. One possible cause is that there already 
exists a key in your Login Keychain with the sepcified identifiers. 
If there is such a key and you want to replace it, use the
Credential Manager to delete the one that is there and try again.""")
        return


def from_keychain():
    """ """
    arg_list = [
        "/usr/bin/security",
        "find-generic-password",
        "-w",
        "-s",
        "key_for_symmetric_encryption",
        "-a",
        "test",
        "login.keychain-db",
    ]
    try:
        cp = run(arg_list, check=True, text=True, capture_output=True)
        key_str = cp.stdout.rstrip()
        return key_str
    except CalledProcessError as e:
        print("""
No key with these identifiers exists in your Login Keychain. 

If you haven't already done so, generate a key. 
If you had a key but have lost it, you can generate 
a new one but you will not be able to recover anything 
encrypted with the lost key.""")
        return


def encrypt(p):
    box = SecretBox(s_2_b(read_secret_string()))
    if p.suffix == ".secret":
        q = p.parent / (p.stem + ".box")
    else:
        q = p.parent / (p.name + ".box")
    message = box.encrypt(p.read_bytes())
    q.write_bytes(message)
    return


def decrypt(r):
    box = SecretBox(s_2_b(read_secret_string()))
    t = r.parent / (r.stem + ".secret")
    t.write_bytes(box.decrypt(r.read_bytes()))
    return