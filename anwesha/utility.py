import hashlib
import uuid
import jwt

def hashpassword(password):
    return hashlib.sha256(password.encode()).hexdigest()

def createId(prefix, length):
    """
        Utility function to create a random id of given length
        prefix : prefix of the id ( ex : "TEAM", "ANW" )
        length : length of the id excluding the prefix
    """

    id = str(uuid.uuid4()).replace("-", "")
    return prefix + id[:length]
    

def checkPhoneNumber(phone_number : str):
    """
        Utility function to check if the given phone number is valid or not
    """
    pass


def isemail( email_id : str):
    """
        Utility function to check if the given email id is valid or not
    """
    if "@" in email_id:
        return True
    return False

def get_anwesha_id(request):
    """
        Utility function to get the anwesha_id of the user from the cookie
    """
    token = request.COOKIES.get('jwt')
    if not token:
        return None
    try:
        payload = jwt.decode(token, "ufdhufhufgefef", algorithms = 'HS256')
        id = payload["id"]
        return id
    except jwt.ExpiredSignatureError:
        return None