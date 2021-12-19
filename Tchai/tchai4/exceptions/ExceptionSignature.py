from exceptions.ExceptionSerializable import ExceptionSerializable;

class ExceptionSignature(ExceptionSerializable):
    """description of class"""
    
    def __init__(self, previous: Exception):
        super().__init__("Une erreur s'est produite lors du controle de la signature.", "Exception validité de la signature", "500", previous);