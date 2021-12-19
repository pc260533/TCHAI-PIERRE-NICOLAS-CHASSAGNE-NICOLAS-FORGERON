from exceptions.ExceptionSerializable import ExceptionSerializable;

class ExceptionMontantTransaction(ExceptionSerializable):
    """description of class"""
    
    def __init__(self, previous: Exception, ajoutMessage: str = ""):
        super().__init__("Une exception lors de la récupération du montant de la transaction" + ajoutMessage, "Exception montant transaction", "500", previous);