from exceptions.ExceptionMontantTransaction import ExceptionMontantTransaction
from exceptions.ExceptionParsageJson import ExceptionParsageJson;
from exceptions.ExceptionGestionBaseDeDonnees import ExceptionGestionBaseDeDonnees;
from views.ViewTchai import ViewTchai;
from stockage.StockageBaseDeDonnees import StockageBaseDeDonnees;
from modele.Utilisateur import Utilisateur;
from modele.Transaction import Transaction;
from datetime import datetime;
from Crypto.Signature import pkcs1_15;
from Crypto.Hash import SHA256;
from Crypto.PublicKey import RSA;
import base64;
import binascii;

class SignerTransactionView(ViewTchai):
    """description of class"""
    
    methods = ["GET"];

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

            clePrivee = RSA.import_key(base64.b64decode(self.getRequeteJsonObject()["clePriveeUtilisateur1"]));
            messageHash = SHA256.new(transaction.getTransactionPourHashageSignature().encode("utf-8"));
            signature = binascii.hexlify(pkcs1_15.new(clePrivee).sign(messageHash)).decode("utf-8");

            return {"transaction" : transaction.__dict__(),
                    "signature": signature};
        except KeyError as keyErrorException:
           raise ExceptionParsageJson(keyErrorException);
        except ValueError as valueErrorException:
            raise ExceptionMontantTransaction(valueErrorException);
        except ExceptionMontantTransaction:
            raise;
        except Exception as exception:
           raise ExceptionParsageJson(exception);