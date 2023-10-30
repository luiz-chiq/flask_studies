from flask_jwt_extended import get_jwt_identity

def verifyIfIsLoggedUserByLogin(login):
    identity = get_jwt_identity()
    loggedUserLogin = identity.get("login")
    if loggedUserLogin != login:
        return False
    return True

def verifyIfIsLoggedUserById(id):
    identity = get_jwt_identity()
    loggedUserId = identity.get("id")
    if loggedUserId != id:
        return False
    return True
