import hashlib
import uuid

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
