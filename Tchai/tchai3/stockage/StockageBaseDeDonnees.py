from exceptions.ExceptionGestionBaseDeDonnees import ExceptionGestionBaseDeDonnees;
from modele.Utilisateur import Utilisateur;
from modele.Transaction import Transaction;
from typing import List;
from datetime import datetime;
import sqlite3;
import hashlib;

class StockageBaseDeDonnees(object):
    """description of class"""

    def __init__(self, nomBaseDeDonnee: str):
        self.connection = sqlite3.connect(nomBaseDeDonnee, check_same_thread = False);
        self.cursor = self.connection.cursor();
        ## On crée les tables utilisateur et transaction si elles n'existent pas.
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS utilisateur (
                                nomUtilisateur TEXT PRIMARY KEY,
                                montantInitialUtilisateur REAL NOT NULL);""");
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS transactionUtilisateurs (
                               identifiantTransaction INTEGER PRIMARY KEY,
                               nomUtilisateur1 TEXT NOT NULL,
                               nomUtilisateur2 TEXT NOT NULL,
                               montantTransaction REAL NOT NULL,
                               dateTransaction TEXT NOT NULL,
                               hashTransaction TEXT NOT NULL);""");
        self.connection.commit();

    def fermerConnexion(self):
        self.connection.close();

    def calculerHash(self, transaction: Transaction, transactionPrecedente: Transaction = None) -> str:
        hashTransactionPrecedente = "";
        if (transactionPrecedente is not None):
            hashTransactionPrecedente = transactionPrecedente.hashTransaction;
        ## On calcule le hash de la transaction.
        return hashlib.md5((transaction.getTransactionPourHashage() + hashTransactionPrecedente).encode("utf-8")).hexdigest();

    def ajouterUtilisateur(self, utilisateur: Utilisateur):
        try:
            sql = "INSERT INTO utilisateur (nomUtilisateur, montantInitialUtilisateur) VALUES (:nomUtilisateur, :montantInitialUtilisateur);";
            self.cursor.execute(sql, {"nomUtilisateur": utilisateur.nomUtilisateur, "montantInitialUtilisateur": utilisateur.montantInitialUtilisateur});
            self.connection.commit();
        except sqlite3.Error as errorSqlite3:
            raise ExceptionGestionBaseDeDonnees(errorSqlite3);
        
    def verifierUtilisateurExiste(self, nomUtilisateur: str) -> bool:
        try:
            res = True;
            sql = "SELECT count(*) FROM utilisateur WHERE nomUtilisateur = :nomUtilisateur";
            self.cursor.execute(sql, {"nomUtilisateur": nomUtilisateur});
            nombreUtilisateur = self.cursor.fetchone()[0];
            if (nombreUtilisateur == 0):
                res = False;
            return res;
        except sqlite3.Error as errorSqlite3:
            raise ExceptionGestionBaseDeDonnees(errorSqlite3);

    def chargerUtilisateurAvecNom(self, nomUtilisateur: str) -> Utilisateur:
        try:
            utilisateur = Utilisateur();
            sql = "SELECT nomUtilisateur, montantInitialUtilisateur FROM utilisateur WHERE nomUtilisateur = :nomUtilisateur";
            self.cursor.execute(sql, {"nomUtilisateur": nomUtilisateur});
            utilisateurLigne = self.cursor.fetchone();
            if (utilisateurLigne == None):
                raise ExceptionGestionBaseDeDonnees(None, " : l'utilisateur n'existe pas.");
            utilisateur.nomUtilisateur = utilisateurLigne[0];
            utilisateur.montantInitialUtilisateur = utilisateurLigne[1];
            return utilisateur;
        except sqlite3.Error as errorSqlite3:
            raise ExceptionGestionBaseDeDonnees(errorSqlite3);

    def enregistrerTransaction(self, transaction: Transaction):
        ## On récupère la dernière transaction enregistrée si elle existe et on calcule le hash.
        transaction.hashTransaction = self.calculerHash(transaction, self.chargerDerniereTransaction());
        try:
            sql = "INSERT INTO transactionUtilisateurs (nomUtilisateur1, nomUtilisateur2, montantTransaction, dateTransaction, hashTransaction) VALUES (:nomUtilisateur1, :nomUtilisateur2, :montantTransaction, :dateTransaction, :hashTransaction);";
            self.cursor.execute(sql, {"nomUtilisateur1": transaction.utilisateur1.nomUtilisateur,
                                      "nomUtilisateur2": transaction.utilisateur2.nomUtilisateur,
                                      "montantTransaction": transaction.montantTransaction,
                                      "dateTransaction": transaction.dateTransaction.strftime("%Y-%m-%d %H:%M:%S"),
                                      "hashTransaction": transaction.hashTransaction});
            self.connection.commit();
        except sqlite3.Error as errorSqlite3:
            raise ExceptionGestionBaseDeDonnees(errorSqlite3);

    def chargerListeTransactions(self) -> List[Transaction]:
        try:
            listeTransactions: List[Transaction] = [];
            sql = "SELECT nomUtilisateur1, nomUtilisateur2, montantTransaction, dateTransaction, hashTransaction FROM transactionUtilisateurs ORDER BY dateTransaction ASC";
            self.cursor.execute(sql);
            lignesTransactions = self.cursor.fetchall();
            for ligneTransaction in lignesTransactions:
                transaction: Transaction = Transaction();
                utilisateur1: Utilisateur = Utilisateur();
                utilisateur1.nomUtilisateur = ligneTransaction[0];
                transaction.utilisateur1 = utilisateur1;
                utilisateur2: Utilisateur = Utilisateur();
                utilisateur2.nomUtilisateur = ligneTransaction[1];
                transaction.utilisateur2 = utilisateur2;
                transaction.montantTransaction = ligneTransaction[2];
                transaction.dateTransaction = datetime.strptime(ligneTransaction[3], "%Y-%m-%d %H:%M:%S");
                transaction.hashTransaction = ligneTransaction[4];
                listeTransactions.append(transaction);
            return listeTransactions;
        except sqlite3.Error as errorSqlite3:
            raise ExceptionGestionBaseDeDonnees(errorSqlite3);

    def chargerListeTransactionsAvecUtilisateur(self, nomUtilisateur: str) -> List[Transaction]:
        try:
            if (not self.verifierUtilisateurExiste(nomUtilisateur)):
                raise ExceptionGestionBaseDeDonnees(None, " : l'utilisateur n'existe pas.");
            listeTransactions: List[Transaction] = [];
            sql = "SELECT nomUtilisateur1, nomUtilisateur2, montantTransaction, dateTransaction, hashTransaction FROM transactionUtilisateurs WHERE nomUtilisateur1 = :nomUtilisateur OR nomUtilisateur2 = :nomUtilisateur ORDER BY dateTransaction ASC";
            self.cursor.execute(sql, {"nomUtilisateur": nomUtilisateur});
            lignesTransactions = self.cursor.fetchall();
            for ligneTransaction in lignesTransactions:
                transaction: Transaction = Transaction();
                utilisateur1: Utilisateur = Utilisateur();
                utilisateur1.nomUtilisateur = ligneTransaction[0];
                transaction.utilisateur1 = utilisateur1;
                utilisateur2: Utilisateur = Utilisateur();
                utilisateur2.nomUtilisateur = ligneTransaction[1];
                transaction.utilisateur2 = utilisateur2;
                transaction.montantTransaction = ligneTransaction[2];
                transaction.dateTransaction = datetime.strptime(ligneTransaction[3], "%Y-%m-%d %H:%M:%S");
                transaction.hashTransaction = ligneTransaction[4];
                listeTransactions.append(transaction);
            return listeTransactions;
        except sqlite3.Error as errorSqlite3:
            raise ExceptionGestionBaseDeDonnees(errorSqlite3);

    def chargerListeTransactionsNonVerifiees(self) -> List[Transaction]:
        try:
            listeTransactionsNonVerifies: List[Transaction] = [];
            sql = "SELECT nomUtilisateur1, nomUtilisateur2, montantTransaction, dateTransaction, hashTransaction FROM transactionUtilisateurs ORDER BY dateTransaction ASC";
            self.cursor.execute(sql);
            lignesTransactions = self.cursor.fetchall();
            ## On ajoute None car la première transaction n'a pas de prédecesseur.
            for ligneTransaction, ligneTransactionPrecedente in zip(lignesTransactions, [None] + lignesTransactions[:-1]):
                transaction: Transaction = Transaction();
                utilisateur1: Utilisateur = Utilisateur();
                utilisateur1.nomUtilisateur = ligneTransaction[0];
                transaction.utilisateur1 = utilisateur1;
                utilisateur2: Utilisateur = Utilisateur();
                utilisateur2.nomUtilisateur = ligneTransaction[1];
                transaction.utilisateur2 = utilisateur2;
                transaction.montantTransaction = ligneTransaction[2];
                transaction.dateTransaction = datetime.strptime(ligneTransaction[3], "%Y-%m-%d %H:%M:%S");
                transaction.hashTransaction = ligneTransaction[4];
                transactionPrecedente: Transaction = None;
                if (ligneTransactionPrecedente is not None):
                    transactionPrecedente = Transaction();
                    transactionPrecedente.hashTransaction = ligneTransactionPrecedente[4];
                if (transaction.hashTransaction != self.calculerHash(transaction, transactionPrecedente)):
                    listeTransactionsNonVerifies.append(transaction);
            return listeTransactionsNonVerifies;
        except sqlite3.Error as errorSqlite3:
            raise ExceptionGestionBaseDeDonnees(errorSqlite3);

    def chargerDerniereTransaction(self) -> Transaction:
        try:
            transaction = None;
            sql = "SELECT nomUtilisateur1, nomUtilisateur2, montantTransaction, dateTransaction, hashTransaction FROM transactionUtilisateurs ORDER BY identifiantTransaction DESC LIMIT 1";
            self.cursor.execute(sql);
            ligneTransaction = self.cursor.fetchone();
            if (ligneTransaction):
                transaction = Transaction();
                utilisateur1 = Utilisateur();
                utilisateur1.nomUtilisateur = ligneTransaction[0];
                transaction.utilisateur1 = utilisateur1;
                utilisateur2: Utilisateur = Utilisateur();
                utilisateur2.nomUtilisateur = ligneTransaction[1];
                transaction.utilisateur2 = utilisateur2;
                transaction.montantTransaction = ligneTransaction[2];
                transaction.dateTransaction = datetime.strptime(ligneTransaction[3], "%Y-%m-%d %H:%M:%S");
                transaction.hashTransaction = ligneTransaction[4];
            return transaction;
        except sqlite3.Error as errorSqlite3:
            raise ExceptionGestionBaseDeDonnees(errorSqlite3);

    def getSoldeCompte(self, nomUtilisateur: str) -> float:
        try:
            ## On charge l'utilisateur pour récupérer le montant initiale de l'utilisateur et on throw une exception s'il n'existe pas.
            utilisateur: Utilisateur = self.chargerUtilisateurAvecNom(nomUtilisateur);
            soldeCompte = utilisateur.montantInitialUtilisateur;
            listeTransactions: List[Transaction] = self.chargerListeTransactionsAvecUtilisateur(nomUtilisateur);
            for transaction in listeTransactions:
                ## On diminue le montant initial du montant de la transaction.
                if (transaction.utilisateur1.nomUtilisateur == nomUtilisateur):
                    soldeCompte -= transaction.montantTransaction;
                ## On augmente le montant initial du montant de la transaction.
                elif (transaction.utilisateur2.nomUtilisateur == nomUtilisateur):
                    soldeCompte += transaction.montantTransaction;
            return soldeCompte;
        except sqlite3.Error as errorSqlite3:
            raise ExceptionGestionBaseDeDonnees(errorSqlite3);