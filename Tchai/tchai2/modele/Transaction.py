from modele.Utilisateur import Utilisateur;
from datetime import datetime;

class Transaction(object):
    """description of class"""

    @property
    def utilisateur1(self):
        return self.__utilisateur1;

    @utilisateur1.setter
    def utilisateur1(self, utilisateur1):
        self.__utilisateur1 = utilisateur1;

    @property
    def utilisateur2(self):
        return self.__utilisateur2;

    @utilisateur2.setter
    def utilisateur2(self, utilisateur2):
        self.__utilisateur2 = utilisateur2;

    @property
    def montantTransaction(self):
        return self.__montantTransaction;

    @montantTransaction.setter
    def montantTransaction(self, montantTransaction):
        self.__montantTransaction = montantTransaction;
    
    @property
    def dateTransaction(self):
        return self.__dateTransaction;

    @dateTransaction.setter
    def dateTransaction(self, dateTransaction):
        self.__dateTransaction = dateTransaction;

    @property
    def hashTransaction(self):
        return self.__hashTransaction;

    @hashTransaction.setter
    def hashTransaction(self, hashTransaction):
        self.__hashTransaction = hashTransaction;

    def __init__(self, utilisateur1: Utilisateur = None, utilisateur2: Utilisateur = None, montantTransaction: float = None, dateTransaction: datetime = None, hashTransaction: str = None):
        self.utilisateur1 = utilisateur1;
        self.utilisateur2 = utilisateur2;
        self.montantTransaction = montantTransaction;
        self.dateTransaction = dateTransaction;
        self.hashTransaction = hashTransaction;

    def getTransactionPourHashage(self) -> str:
        res = "";
        if (self.utilisateur1 != None and self.utilisateur2 != None):
            res = self.utilisateur1.nomUtilisateur + self.utilisateur2.nomUtilisateur + str(self.montantTransaction) + self.dateTransaction.strftime("%Y-%m-%d %H:%M:%S");
        return res;

    def __dict__(self) -> dict:
        return {"nomUtilisateur1": self.utilisateur1.nomUtilisateur,
                "nomUtilisateur2": self.utilisateur2.nomUtilisateur,
                "montantTransaction": self.montantTransaction,
                "dateTransaction": self.dateTransaction,
                "hashTransaction": self.hashTransaction};

    def __str__(self) -> str:
        return "{nomUtilisateur1} a donné {montantTransaction} à {nomUtilisateur2} le {dateTransaction} -> hash : {hashTransaction}".format(nomUtilisateur1 = self.utilisateur1.nomUtilisateur,
                                                                                                                                            montantTransaction = self.montantTransaction,
                                                                                                                                            nomUtilisateur2 = self.utilisateur2.nomUtilisateur,
                                                                                                                                            dateTransaction = self.dateTransaction,
                                                                                                                                            hashTransaction = self.hashTransaction);