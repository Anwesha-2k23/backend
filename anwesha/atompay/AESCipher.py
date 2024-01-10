#!C:\Python310\python.exe -u

#Developed by Sagar Gopale, Senior Software Engineer Atom Technologies Ltd


import cgi
import hmac
import hashlib
import binascii


from hashlib import pbkdf2_hmac
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

class AESCipher:
    def __init__( self, key ):
        listdata = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        self.byteArrayObject = bytearray(listdata)
        self.requestEncypritonKey = b'A4476C2062FFA58980DC8F79EB6A799E'
        self.requestSaltkey = b'A4476C2062FFA58980DC8F79EB6A799E'
        self.responseSaltkey = b'75AEF0FA1B94B3C10D4F5B268F757F11'
        self.responseDecypritonKey = b'75AEF0FA1B94B3C10D4F5B268F757F11'
        
    def encrypt( self, message ):    
        pbkdf2_hmac_key = hashlib.pbkdf2_hmac('sha512', self.requestEncypritonKey, self.requestSaltkey, 65536, dklen=32)
        cipher = AES.new(pbkdf2_hmac_key, AES.MODE_CBC, self.byteArrayObject)
        cipher_enc = cipher.encrypt(pad(message, 16))
        return cipher_enc.hex().upper()
    
    def decrypt( self, message ):    
        binary_string = binascii.unhexlify(message.strip())
        pbkdf2_hmac_key = hashlib.pbkdf2_hmac('sha512', self.responseDecypritonKey, self.responseSaltkey, 65536, dklen=32)
        cipher = AES.new(pbkdf2_hmac_key, AES.MODE_CBC, self.byteArrayObject)
        cipher_dec = cipher.decrypt(binary_string)
        return self._unpad(cipher_dec).decode('utf-8')
    
    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]

