from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from store.forms import UtenteCreationForm
from store.models import Radiologia, Modality, SalaDiagnostica, Frase, Organo, Frasario, Revisione, Prestazione, Esame, \
    NomenclatorePrestazioni, Preparazione, Paziente, Utente, Attrezzatura


class SalaDiagnosticaLista(admin.TabularInline):
    model = SalaDiagnostica


@admin.register(Radiologia)
class RadiologiaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ragione_sociale')

    inlines = [
        SalaDiagnosticaLista,
    ]


@admin.register(Modality)
class ModalityAdmin(admin.ModelAdmin):
    list_display = ('sigla', 'descrizione')


@admin.register(SalaDiagnostica)
class SalaDiagnosticaAdmin(admin.ModelAdmin):
    pass


@admin.register(Attrezzatura)
class AttrezzaturaAdmin(admin.ModelAdmin):
    pass

'''
@admin.register(TipologiaUtente)
class TipologiaUtenteAdmin(admin.ModelAdmin):
    pass
'''

@admin.register(Utente)
class UtenteAdmin(UserAdmin):
    model = Utente
    add_form = UtenteCreationForm

    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Informazioni Utente',
            {
                'fields': (
                    'tipo',
                    'titolo',
                    'radiologia',
                    'sale_diagnostiche',
                )
            }
        ),
        (
            'Skills Utente',
            {
                'fields': (
                    'skill_anagrafica_pazienti',
                    'skill_referti',
                )
            }
        ),
        (
            'Flags Utente',
            {
                'fields': (
                    'flag_firma_referto',
                    'flag_revisione_referto',
                    'flag_schedulazione_esame',
                    'flag_accettazione_clinica',
                    'flag_completamento_esame',
                )
            }
        )
    )


@admin.register(Paziente)
class PazienteAdmin(admin.ModelAdmin):
    pass


@admin.register(Preparazione)
class PreparazioneAdmin(admin.ModelAdmin):
    pass


@admin.register(NomenclatorePrestazioni)
class NomenclatorePrestazioniAdmin(admin.ModelAdmin):
    pass


@admin.register(Esame)
class EsameAdmin(admin.ModelAdmin):
    pass


@admin.register(Prestazione)
class PrestazioneAdmin(admin.ModelAdmin):
    pass


@admin.register(Revisione)
class RevisioneAdmin(admin.ModelAdmin):
    pass


@admin.register(Frasario)
class FrasarioAdmin(admin.ModelAdmin):
    pass


@admin.register(Organo)
class OrganoAdmin(admin.ModelAdmin):
    pass


@admin.register(Frase)
class FraseAdmin(admin.ModelAdmin):
    pass