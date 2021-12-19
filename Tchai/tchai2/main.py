from exceptions.ExceptionSerializable import ExceptionSerializable;
from stockage.StockageBaseDeDonnees import StockageBaseDeDonnees
from views.AfficherSoldeCompteView import AfficherSoldeCompteView;
from views.AfficherTransactionsAvecUtilisateurView import AfficherTransactionsAvecUtilisateurView;
from views.AfficherTransactionsView import AfficherTransactionsView;
from views.AjouterUtilisateurView import AjouterUtilisateurView;
from views.EnregistrerTransactionView import EnregistrerTransactionView;
from views.VerifierIntegriteTransactionsView import VerifierIntegriteTransactionsView;
from flask import Flask, render_template;

def handle_bad_request(exceptionSerializable: ExceptionSerializable):
    return render_template("exceptionMessage.html", **exceptionSerializable.__dict__()), exceptionSerializable.status;

def main():
    stockageBaseDeDonnee = StockageBaseDeDonnees("tchai2.db");
    app = Flask(__name__);
    app.add_url_rule("/ajouterUtilisateur", view_func = AjouterUtilisateurView.as_view("ajouterUtilisateur", "ajouterUtilisateurConfirmation.html", stockageBaseDeDonnee));
    app.add_url_rule("/enregistrerTransaction", view_func = EnregistrerTransactionView.as_view("enregistrerTransaction", "enregistrerTransactionConfirmation.html", stockageBaseDeDonnee));
    app.add_url_rule("/afficherTransactions", view_func = AfficherTransactionsView.as_view("afficherTransactions", "afficherTransactionsConfirmation.html", stockageBaseDeDonnee));
    app.add_url_rule("/afficherTransactionsAvecUtilisateur", view_func = AfficherTransactionsAvecUtilisateurView.as_view("afficherTransactionsAvecUtilisateur", "afficherTransactionsAvecUtilisateurConfirmation.html", stockageBaseDeDonnee));
    app.add_url_rule("/afficherSoldeCompte", view_func = AfficherSoldeCompteView.as_view("afficherSoldeCompte", "afficherSoldeCompteConfirmation.html", stockageBaseDeDonnee));
    app.add_url_rule("/verifierIntegriteTransactions", view_func = VerifierIntegriteTransactionsView.as_view("verifierIntegriteTransactions", "verifierIntegriteTransactionsConfirmation.html", stockageBaseDeDonnee));
    app.register_error_handler(ExceptionSerializable, handle_bad_request);

    app.run(debug = True);

if __name__ == "__main__":
    main();