class Utilisateur(object):
    """description of class"""

    @property
    def nomUtilisateur(self):
        return self.__nomUtilisateur;

    @nomUtilisateur.setter
    def nomUtilisateur(self, nomUtilisateur):
        self.__nomUtilisateur = nomUtilisateur;

    @property
    def montantInitialUtilisateur(self):
        return self.__montantInitialUtilisateur;

    @montantInitialUtilisateur.setter
    def montantInitialUtilisateur(self, montantInitialUtilisateur):
        self.__montantInitialUtilisateur = montantInitialUtilisateur;

    def __init__(self, nomUtilisateur: str = None, montantInitialUtilisateur: float = None):
        self.nomUtilisateur = nomUtilisateur;
        self.montantInitialUtilisateur = montantInitialUtilisateur;

    def __dict__(self):
        return {"nomUtilisateur": self.nomUtilisateur,
                "montantInitialUtilisateur": self.montantInitialUtilisateur};