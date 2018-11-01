import hashlib


def encrypt(text):
    _md5 = hashlib.md5()
    _md5.update(text.encode(encoding='utf-8'))
    return _md5.hexdigest()


def encrypt_user_password(pwd):
    _ = "yehrg2iu3b34"
    return encrypt(_ + pwd)


# make new password

# your password
# pwd = "123456"
#
# print(encrypt_user_password(pwd))
