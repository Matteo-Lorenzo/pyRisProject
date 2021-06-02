from ..utils import Stati


class MainWindowModel():

    def __init__(self):
        # Possibili stati: aperto | chiuso | modificato
        self.stati = {
            'gestionepazienti': Stati.CHIUSO,
            'prenotazioni': Stati.CHIUSO,
            'consegna': Stati.CHIUSO,
            'preferenze': Stati.CHIUSO,
            'esecuzioneesame': Stati.CHIUSO,
            'refertazione': Stati.CHIUSO,
            'firma': Stati.CHIUSO,
            'controllo': Stati.CHIUSO,
        }
