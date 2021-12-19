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
    stockageBaseDeDonnee = StockageBaseDeDonnees("tchai2_attaque2.db");

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

    ## Des transactions de test1 vers test2 doivent exister pour l'attaque en supprime au moins une.
    try:
        for i in range(3):
            transaction = Transaction();
            transaction.utilisateur1 = utilisateur1;
            transaction.utilisateur2 = utilisateur2;
            transaction.montantTransaction = 20.0;
            transaction.dateTransaction = datetime.now();
            stockageBaseDeDonnee.enregistrerTransaction(transaction);
    except ExceptionGestionBaseDeDonnees as exceptionGestionBaseDeDonnees:
        print("Une erreur s'est produite lors de l'ajout de la transaction entre test1 et test2.");
        print(exceptionGestionBaseDeDonnees.getTraceback());

    ## Attaque 2
    ## On supprime la première transaction de test1 vers test2.
    sql = "DELETE FROM transactionUtilisateurs WHERE identifiantTransaction IN (SELECT identifiantTransaction FROM transactionUtilisateurs WHERE nomutilisateur1 = :nomUtilisateur1 AND nomUtilisateur2 = :nomUtilisateur2 LIMIT 1)";
    stockageBaseDeDonnee.cursor.execute(sql, {"nomUtilisateur1": "test1",
                                              "nomUtilisateur2": "test2"});
    stockageBaseDeDonnee.connection.commit();

    ## Après l'attaque, on ne peut pas détecter la transaction qui a été supprimé grâce au hash de chaque transaction car la vérification se base sur le hash de chaque transaction de manière unitaire.
    ## On doit donc dans la version 3 calculer le hash avec la transaction en cours et les valeurs de la transaction précédente.
    listeTransactionNonVerifiees = stockageBaseDeDonnee.chargerListeTransactionsNonVerifiees();
    if (listeTransactionNonVerifiees):
        print("L'attaque a été détecté grâce à la vérification des hashs de chaque transaction.\nLes transactions qui ont été modifiés sont :");
        [print(transactionNonVerifiee) for transactionNonVerifiee in listeTransactionNonVerifiees];

    stockageBaseDeDonnee.fermerConnexion();
    os.remove("tchai2_attaque2.db");

if __name__ == "__main__":
    main();