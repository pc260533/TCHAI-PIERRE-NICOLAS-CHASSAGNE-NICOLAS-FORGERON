import os, sys;
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))));
from exceptions.ExceptionGestionBaseDeDonnees import ExceptionGestionBaseDeDonnees;
from modele.Transaction import Transaction;
from modele.Utilisateur import Utilisateur;
from stockage.StockageBaseDeDonnees import StockageBaseDeDonnees;
from datetime import datetime;
import sqlite3;
import os;

def main():
    ## Conditions préalables à l'attaque dans la base de données. 
    stockageBaseDeDonnee = StockageBaseDeDonnees("tchai1_attaque1.db");

    ## L'utilisateur test1 doit exister.
    try:
        utilisateur1 = Utilisateur();
        utilisateur1.nomUtilisateur = "test1";
        utilisateur1.montantInitialUtilisateur = 0;
        stockageBaseDeDonnee.ajouterUtilisateur(utilisateur1);
    except ExceptionGestionBaseDeDonnees as exceptionGestionBaseDeDonnees:
        print("Une erreur s'est produite lors de l'ajout de l'utilisateur test1. Celui-ci existe probablement déjà.");
        print(exceptionGestionBaseDeDonnees.getTraceback());

    ## L'utilisateur test2 doit exister.
    try:
        utilisateur2 = Utilisateur();
        utilisateur2.nomUtilisateur = "test2";
        utilisateur2.montantInitialUtilisateur = 0;
        stockageBaseDeDonnee.ajouterUtilisateur(utilisateur2);
    except ExceptionGestionBaseDeDonnees as exceptionGestionBaseDeDonnees:
        print("Une erreur s'est produite lors de l'ajout de l'utilisateur test2. Celui-ci existe probablement déjà.");
        print(exceptionGestionBaseDeDonnees.getTraceback());

    ## Au moins une transaction de test1 vers test2 doit exister pour qu'elle soit modifiée par l'attaque.
    try:
        transaction = Transaction();
        transaction.utilisateur1 = utilisateur1;
        transaction.utilisateur2 = utilisateur2;
        transaction.montantTransaction = 20;
        transaction.dateTransaction = datetime.now();
        stockageBaseDeDonnee.enregistrerTransaction(transaction);
    except ExceptionGestionBaseDeDonnees as exceptionGestionBaseDeDonnees:
        print("Une erreur s'est produite lors de l'ajout de la transaction entre test1 et test2.");
        print(exceptionGestionBaseDeDonnees.getTraceback());

    ## Attaque 1
    ## On modifie le montant de toutes les transactions test1 vers test2.
    sql = "UPDATE transactionUtilisateurs SET montantTransaction = :montantTransaction WHERE nomutilisateur1 = :nomUtilisateur1 AND nomUtilisateur2 = :nomUtilisateur2";
    stockageBaseDeDonnee.cursor.execute(sql, {"montantTransaction": 1000,
                                              "nomUtilisateur1": "test1",
                                              "nomUtilisateur2": "test2"});
    stockageBaseDeDonnee.connection.commit();

    ## Après l'attaque, il est impossible de savoir si le montant d'une transaction a été modifié.
    ## On doit donc dans la version 2 calculer le hash de la transaction en cours pour tester si elle a été modifié.

    stockageBaseDeDonnee.fermerConnexion();
    os.remove("tchai1_attaque1.db");

if __name__ == "__main__":
    main();