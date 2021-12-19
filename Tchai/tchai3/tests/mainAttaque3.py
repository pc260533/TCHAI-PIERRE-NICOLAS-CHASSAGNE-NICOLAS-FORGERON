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
    stockageBaseDeDonnee = StockageBaseDeDonnees("tchai3_attaque3.db");

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

    ## Attaque 3
    ## On insère une transaction de test1 vers test2.
    ## On suppose que l'attaquant connait la méthode de calcul de hash et peut enregistrer des transactions.
    ## Ici, l'utilisateur test2 utilise l'utilisateur test1 pour faire une transaction.
    try:
        transaction = Transaction();
        transaction.utilisateur1 = utilisateur1;
        transaction.utilisateur2 = utilisateur2;
        transaction.montantTransaction = 20.0;
        transaction.dateTransaction = datetime.now();
        stockageBaseDeDonnee.enregistrerTransaction(transaction);
    except ExceptionGestionBaseDeDonnees as exceptionGestionBaseDeDonnees:
        print("Une erreur s'est produite lors de l'ajout de la transaction entre test1 et test2.");
        print(exceptionGestionBaseDeDonnees.getTraceback());

    ## Après l'attaque, on ne peut pas détecter les transactions qui ont été supprimé
    ## La vérification d'intégrité se base uniquement sur le clacul de hash.
    ## Cependant, l'attquant connait la méhtode de calcul de hash.
    ## L'attaque consite à ce que test2 falsifie l'identité de test1
    ## On doit donc dans la version 4 prouver que ce sont bien les utilisateurs qui effectue des transaction avec la cryptographie assymétrique.
    listeTransactionNonVerifiees = stockageBaseDeDonnee.chargerListeTransactionsNonVerifiees();
    if (listeTransactionNonVerifiees):
        print("L'attaque a été détecté grâce à la vérification des hashs de chaque transaction.\nLes transactions qui ont été modifiés sont :");
        [print(transactionNonVerifiee) for transactionNonVerifiee in listeTransactionNonVerifiees];

    stockageBaseDeDonnee.fermerConnexion();
    os.remove("tchai3_attaque3.db");

if __name__ == "__main__":
    main();
