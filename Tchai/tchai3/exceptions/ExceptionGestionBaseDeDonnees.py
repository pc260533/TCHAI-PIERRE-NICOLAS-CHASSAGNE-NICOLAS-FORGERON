from exceptions.ExceptionSerializable import ExceptionSerializable;

class ExceptionGestionBaseDeDonnees(ExceptionSerializable):
    """description of class"""
    
    def __init__(self, previous: Exception, ajoutMessage: str = ""):
        super().__init__("Une erreur générale de la base de données est survenue" + ajoutMessage, "Erreur générale de la base de données", "500", previous);