from exceptions.ExceptionSerializable import ExceptionSerializable;

class ExceptionGestionFichiers(ExceptionSerializable):
    """description of class"""
    
    def __init__(self, previous: Exception):
        super().__init__("Une erreur générale de la sauvegarde de fichier est survenue.", "Exception générale de la gestion de fichier", "500", previous);