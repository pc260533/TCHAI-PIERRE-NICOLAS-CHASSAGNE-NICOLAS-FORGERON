from exceptions.ExceptionParsageJson import ExceptionParsageJson
from exceptions.ExceptionGestionBaseDeDonnees import ExceptionGestionBaseDeDonnees
from views.ViewTchai import ViewTchai;
from stockage.StockageBaseDeDonnees import StockageBaseDeDonnees;
from modele.Utilisateur import Utilisateur;
from modele.Transaction import Transaction;

class AfficherSoldeCompteView(ViewTchai):
    """description of class"""
    
    methods = ["GET"];

    def __init__(self, nomTemplate: str, stockageBaseDeDonnees: StockageBaseDeDonnees):
        super().__init__(nomTemplate, stockageBaseDeDonnees);

    def getParametresTemplate(self):
        try:
            return {"soldeCompte" : self.stockageBaseDeDonnees.getSoldeCompte(self.getRequeteJsonObject()["nomUtilisateur"]),
                    "nomUtilisateur": self.getRequeteJsonObject()["nomUtilisateur"]};
        except KeyError as keyErrorException:
           raise ExceptionParsageJson(keyErrorException);
        except ExceptionGestionBaseDeDonnees:
           raise;
        except Exception as exception:
           raise ExceptionParsageJson(exception);