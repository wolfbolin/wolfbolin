# coding=utf-8
import rsa
import base64


def sign_with_rsa2(sign_str, key_path="config/app_key.pri"):
    private_key = open(key_path, "r").read()
    private_key = rsa.PrivateKey.load_pkcs1(private_key.encode())
    signature = rsa.sign(sign_str.encode(), private_key, 'SHA-256')
    sign = base64.b64encode(signature)
    return sign.decode()


def verify_with_rsa2(sign_str, sign, key_path="config/alipay.pub"):
    sign = base64.b64decode(sign)
    public_key = open(key_path, "r").read()
    public_key = rsa.PublicKey.load_pkcs1_openssl_pem(public_key.encode())
    verify_res = rsa.verify(sign_str.encode(), sign, public_key)
    return verify_res
