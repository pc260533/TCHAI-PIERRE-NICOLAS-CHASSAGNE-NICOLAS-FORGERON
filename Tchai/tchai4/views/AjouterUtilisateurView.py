from exceptions.ExceptionParsageJson import ExceptionParsageJson;
from exceptions.ExceptionGestionFichiers import ExceptionGestionFichiers;
from exceptions.ExceptionMontantTransaction import ExceptionMontantTransaction;
from exceptions.ExceptionGestionBaseDeDonnees import ExceptionGestionBaseDeDonnees;
from views.ViewTchai import ViewTchai;
from stockage.StockageBaseDeDonnees import StockageBaseDeDonnees;
from modele.Utilisateur import Utilisateur;
from Crypto.PublicKey import RSA;
import base64;

class AjouterUtilisateurView(ViewTchai):
    """description of class"""
    
    methods = ["POST"];

    def __init__(self, nomTemplate: str, stockageBaseDeDonnees: StockageBaseDeDonnees):
        super().__init__(nomTemplate, stockageBaseDeDonnees);

    def getParametresTemplate(self):
        try:
            utilisateur = Utilisateur();
            utilisateur.nomUtilisateur = self.getRequeteJsonObject()["nomUtilisateur"];
            utilisateur.montantInitialUtilisateur = float(self.getRequeteJsonObject()["montantInitialUtilisateur"]);
            if (utilisateur.montantInitialUtilisateur < 0):
                raise ExceptionMontantTransaction(None, " : le montant initiale de l'utilisateur doit être positif ou nul.");
            
            key = RSA.generate(2048);
            clePrivee = key.exportKey();
            clePublique = key.publickey().exportKey();
            utilisateur.clePubliqueUtilisateur = clePublique.decode("utf-8"); 
            with open(utilisateur.nomUtilisateur + ".pem", "wb") as stream:
                stream.write(base64.b64encode(clePrivee));

            self.stockageBaseDeDonnees.ajouterUtilisateur(utilisateur);
            return {"utilisateur" : utilisateur.__dict__(),
                    "clePriveeUtilisateur": base64.b64encode(clePrivee).decode("utf-8")};
        except IOError as ioError:
            raise ExceptionGestionFichiers(ioError);
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