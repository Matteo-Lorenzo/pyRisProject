from app.ges_login.login_model import LoginModel
from ..utils import Ambiente


class LoginController():

    def __init__(self, model: LoginModel):
        self.model = model

    def login(self, utente, password):
        Ambiente.utente_corrente = None  # per sicurezza
        try:
            Ambiente.utente_corrente = self.model.utente.objects.get(username=utente)
            return Ambiente.utente_corrente.check_password(password)
        except:
            return False
