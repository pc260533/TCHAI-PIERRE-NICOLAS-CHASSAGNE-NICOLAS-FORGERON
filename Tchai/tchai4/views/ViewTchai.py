from flask.views import View;
from flask import request, render_template;
from stockage.StockageBaseDeDonnees import StockageBaseDeDonnees;

class ViewTchai(View):
    """description of class"""

    def __init__(self, nomTemplate: str, stockageBaseDeDonnees: StockageBaseDeDonnees):
        self.nomTemplate = nomTemplate;
        self.stockageBaseDeDonnees = stockageBaseDeDonnees;

    def getParametresTemplate(self):
        raise NotImplementedError();

    def getRequeteJsonObject(self):
        return request.get_json();

    def dispatch_request(self):
        return render_template(self.nomTemplate, **self.getParametresTemplate());