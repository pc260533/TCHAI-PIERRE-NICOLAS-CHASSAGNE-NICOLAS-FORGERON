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

    @property
    def clePubliqueUtilisateur(self):
        return self.__clePubliqueUtilisateur;

    @clePubliqueUtilisateur.setter
    def clePubliqueUtilisateur(self, clePubliqueUtilisateur):
        self.__clePubliqueUtilisateur = clePubliqueUtilisateur;

    def __init__(self, nomUtilisateur: str = None, montantInitialUtilisateur: float = None, clePubliqueUtilisateur: str = None):
        self.nomUtilisateur = nomUtilisateur;
        self.montantInitialUtilisateur = montantInitialUtilisateur;
        self.clePubliqueUtilisateur = clePubliqueUtilisateur;

    def __dict__(self):
        return {"nomUtilisateur": self.nomUtilisateur,
                "montantInitialUtilisateur": self.montantInitialUtilisateur,
                "clePubliqueUtilisateur": self.clePubliqueUtilisateur};