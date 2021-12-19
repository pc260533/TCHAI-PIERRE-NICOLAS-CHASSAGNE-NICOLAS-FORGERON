from exceptions.ExceptionSerializable import ExceptionSerializable;

class ExceptionParsageJson(ExceptionSerializable):
    """description of class"""
    
    def __init__(self, previous: Exception):
        super().__init__("Une exception c'est produite lors du parsage des paramètres JSON de la requête.", "Exception générale du parsage JSON", "500", previous);