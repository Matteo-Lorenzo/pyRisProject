from django.contrib import admin
from .forms import UtenteCreationForm
from django.contrib.auth.admin import UserAdmin

from store.models import AziendaRefertazione, Radiologia, Metodica, SalaDiagnostica, Frase, \
    Organo, Apparato, Frasario, OrganoFrase, Revisione, Prestazione, Esame, \
    NomenclatorePrestazioni, Preparazione, Paziente, Utente, Attrezzatura


class SalaDiagnosticaLista(admin.TabularInline):
    model = SalaDiagnostica


class ApparatoLista(admin.TabularInline):
    model = Apparato
    fields = ('codice', 'descrizione')
    readonly_fields = ('codice', 'descrizione')


class OrganoLista(admin.TabularInline):
    model = Organo
    fields = ('codice', 'descrizione')
    readonly_fields = ('codice', 'descrizione')


class NomenclatoreLista(admin.TabularInline):
    model = NomenclatorePrestazioni
    fields = ('esame', 'descrizione')
    readonly_fields = ('esame', 'descrizione')


class EsameLista(admin.TabularInline):
    model = Esame


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
                    'flag_cartella_radiologica',
                )
            }
        )
    )


@admin.register(AziendaRefertazione)
class AziendeRefertazioneAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ragione_sociale')


@admin.register(Radiologia)
class RadiologiaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ragione_sociale')

    inlines = [
        SalaDiagnosticaLista,
    ]


@admin.register(Metodica)
class ModalityAdmin(admin.ModelAdmin):
    list_display = ('codice', 'descrizione')

    inlines = [
        ApparatoLista,
    ]


@admin.register(Apparato)
class ApparatoAdmin(admin.ModelAdmin):
    list_display = ('codice', 'descrizione')

    inlines = [
        OrganoLista,
    ]


@admin.register(Organo)
class OrganoAdmin(admin.ModelAdmin):
    list_display = ('codice', 'descrizione')

    inlines = [
        NomenclatoreLista,
    ]


@admin.register(NomenclatorePrestazioni)
class NomenclatorePrestazioniAdmin(admin.ModelAdmin):
    list_display = ('esame', 'descrizione')


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


@admin.register(Paziente)
class PazienteAdmin(admin.ModelAdmin):
    list_display = ('codice_paziente', 'cognome', 'nome', 'data_nascita')
    inlines = [
        EsameLista,
    ]


@admin.register(Preparazione)
class PreparazioneAdmin(admin.ModelAdmin):
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


@admin.register(OrganoFrase)
class OrganoFraseAdmin(admin.ModelAdmin):
    pass


@admin.register(Frase)
class FraseAdmin(admin.ModelAdmin):
    pass
