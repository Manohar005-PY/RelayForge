class ApplicatonException(Exception):
    pass


class MismatchPasswordException(ApplicatonException):
    def __init__(self):
        super().__init__("mismatch password")

class UserAlreadyExistsException(ApplicatonException):
    def __init__(self):
        super().__init__("user already exists")

class InvaildCredentialsException(ApplicatonException):
    def __init__(self):
        super().__init__("invaild credentials")
        
class UserNotFoundExeption(ApplicatonException):
    def __init__(self):
        super().__init__("user not found")