from django.contrib.auth.forms import UserCreationForm

from store.models import Utente


class UtenteCreationForm(UserCreationForm):

    class Meta:
        model = Utente
        fields = '__all__'
