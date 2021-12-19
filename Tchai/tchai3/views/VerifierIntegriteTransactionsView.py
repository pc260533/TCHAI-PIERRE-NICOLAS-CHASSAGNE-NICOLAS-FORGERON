from exceptions.ExceptionGestionBaseDeDonnees import ExceptionGestionBaseDeDonnees
from exceptions.ExceptionParsageJson import ExceptionParsageJson
from views.ViewTchai import ViewTchai;
from stockage.StockageBaseDeDonnees import StockageBaseDeDonnees;
from modele.Utilisateur import Utilisateur;
from modele.Transaction import Transaction;

class VerifierIntegriteTransactionsView(ViewTchai):
    """description of class"""
    
    methods = ["GET"];

    def __init__(self, nomTemplate: str, stockageBaseDeDonnees: StockageBaseDeDonnees):
        super().__init__(nomTemplate, stockageBaseDeDonnees);

    def getParametresTemplate(self):
        try:
            listeTransactionsNonVerifiees = self.stockageBaseDeDonnees.chargerListeTransactionsNonVerifiees();
            return {"listeTransactionsNonVerifiees" : [transactionNonVerifiee.__dict__() for transactionNonVerifiee in listeTransactionsNonVerifiees]}
        except ExceptionGestionBaseDeDonnees:
            raise;
        except Exception as exception:
           raise ExceptionParsageJson(exception);