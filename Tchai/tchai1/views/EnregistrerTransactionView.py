from exceptions.ExceptionGestionBaseDeDonnees import ExceptionGestionBaseDeDonnees
from exceptions.ExceptionParsageJson import ExceptionParsageJson;
from exceptions.ExceptionMontantTransaction import ExceptionMontantTransaction;
from views.ViewTchai import ViewTchai;
from stockage.StockageBaseDeDonnees import StockageBaseDeDonnees;
from modele.Utilisateur import Utilisateur;
from modele.Transaction import Transaction;
from datetime import datetime;

class EnregistrerTransactionView(ViewTchai):
    """description of class"""
    
    methods = ["POST"];

    def __init__(self, nomTemplate: str, stockageBaseDeDonnees: StockageBaseDeDonnees):
        super().__init__(nomTemplate, stockageBaseDeDonnees);

    def getParametresTemplate(self):
        try:
            transaction = Transaction();
            transaction.utilisateur1 = self.stockageBaseDeDonnees.chargerUtilisateurAvecNom(self.getRequeteJsonObject()["nomUtilisateur1"]);
            transaction.utilisateur2 = self.stockageBaseDeDonnees.chargerUtilisateurAvecNom(self.getRequeteJsonObject()["nomUtilisateur2"]);
            transaction.montantTransaction = float(self.getRequeteJsonObject()["montantTransaction"]);
            if (transaction.montantTransaction < 0):
                raise ExceptionMontantTransaction(None, " : le montant de la transaction doit être positif ou nul.");
            transaction.dateTransaction = datetime.now();
            self.stockageBaseDeDonnees.enregistrerTransaction(transaction);
            return transaction.__dict__();
        except KeyError as keyErrorException:
           raise ExceptionParsageJson(keyErrorException);
        except ValueError as valueErrorException:
            raise ExceptionMontantTransaction(valueErrorException);
        except ExceptionMontantTransaction:
            raise;
        except ExceptionGestionBaseDeDonnees:
           raise;
        except Exception as exception:
           raise ExceptionParsageJson(exception);