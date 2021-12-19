import traceback;

class ExceptionSerializable(Exception):
    """description of class"""

    @property
    def message(self):
        return self.__message;

    @message.setter
    def message(self, message):
        self.__message = message;

    @property
    def titre(self):
        return self.__titre;

    @titre.setter
    def titre(self, titre):
        self.__titre = titre;

    @property
    def status(self):
        return self.__status;

    @status.setter
    def status(self, status):
        self.__status = status;

    @property
    def previous(self):
        return self.__previous;

    @previous.setter
    def previous(self, previous):
        self.__previous = previous;

    def getTraceback(self) -> str:
        tracebackString = "";
        if (self.previous != None):
            tracebackString = tracebackString.join(traceback.format_exception(type(self.previous), self.previous, self.previous.__traceback__))
        return tracebackString;

    def __init__(self, message: str, titre: str, status: str, previous: Exception,):
        self.message = message;
        self.titre = titre;
        self.status = status;
        self.previous = previous;
        super().__init__();


    def __dict__(self):
        return {"message": self.message,
                "titre": self.titre,
                "status": self.status,
                "traceback": self.getTraceback()};