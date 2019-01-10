import random

from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from . import models
from .models import Constants
from django import forms

class Bienvenida(Page):
    pass

class Consentimiento(Page):
    form_model = models.Player
    form_fields = ['nombre','doc']

class AllGroupsWaitPage(WaitPage):
    wait_for_all_groups = True
    body_text = "Esperando a que todos los participantes firmen el consentimiento informado."

class Preguntas(Page):
    form_model = models.Player
    form_fields = ['gender','age','estado','neighborhood','estrato']

class AllGroupsWaitPage2(WaitPage):
    wait_for_all_groups = True
    body_text = "Esperando a que todos los participantes llenen la encuesta."

class Instructions(Page):
    pass

class Question(Page):
    form_model = 'player'
    form_fields = ['q1','q2','q3','q4']

class Results(Page):
    pass

class Primed(Page):
    form_model = 'player'
    form_fields = ['recall']
    timeout_seconds = 310

class AllGroupsWaitPage3(WaitPage):
    wait_for_all_groups = True
    body_text = "Esperando a todos los participantes para realizar el sorteo de la dotación inicial."

class Treatment(Page):
    pass

class Decisiones(Page):
    form_model = 'player'

    def get_form_fields(self):
        return ['p{}'.format(i) for i in range(1, 20)]

class AllGroupsWaitPage4(WaitPage):
    wait_for_all_groups = True
    body_text = "Esperando a todos los participantes para tomar la segunda decisión."

class Elicitation(Page):
    form_model = 'player'
    form_fields = ['elicitation']

class AllGroupsWaitPage5(WaitPage):
    wait_for_all_groups = True
    body_text = "Esperando a todos los participantes para tomar la tercera decisión."

class Dictator(Page):
    form_model = 'player'
    form_fields = ['dic','ong']

    def ong_choices(self):
        choices = [
                      'Colombia con Memoria (brindan asistencia jurídica a personas que hayan sido víctimas del conflicto armado interno en Colombia).',
                      'Cruz Roja Bogotá (buscan prevenir y aliviar, en todas las circunstancias, el sufrimiento humano; proteger la vida y la salud, y hacer respetar a la persona humana).',
                      'Médicos sin frontera - Colombia (asisten a personas amenazadas por conflictos armados, violencia, epidemias o enfermedades olvidadas).',
                      'Un Techo para mi País - Colombia (buscan superar la situación de pobreza de las personas brindando acceso a vivienda).',
                      'Colombia Crece (organización católica que crea espacios educativos para los más necesitados).',
                      'Ecosueños (protegen a niños y adolescentes de Bogotá quienes sus derechos han sido vulnerados, amenazados o inobservados).',
                      'No deseo donar.']
        random.shuffle(choices)
        return choices

class ResultsWaitPage(WaitPage):
    def after_all_players_arrive(self):
        for p in self.group.get_players():
            p.set_pd_payoff()
        for p in self.group.get_players():
            p.set_elicitation_payoff()
        for p in self.group.get_players():
            p.set_dictador_payoff()
    body_text = "Realizando el emparejamiento con otro participante y calculando los resultados de las tres decisiones"

class PDresults(Page):
    pass

class eliResults(Page):
    pass

class dicResults(Page):
   pass


class sorteo (WaitPage):
    def after_all_players_arrive(self):
        for p in self.group.get_players():
            p.set_random_payoff()
        for p in self.group.get_players():
            p.set_payoffs()
    body_text = "Estamos esperando a que todos lleguen a esta página para que el " \
                "computador realice el sorteo para decidir si se paga la segunda decisión o la " \
                "tercera decisión. Este sorteo se hará para cada participante. También se está" \
                " calculando su pago total en el día de hoy."

class PayoffResults(Page):
    def before_next_page(self):
        for p in self.group.get_players():
            p.payoff_set_admin()

class AdminReport(Page):
    def is_displayed(self):
        return False

    def before_next_page(self):
        for p in self.group.get_players():
            p.payoff_set_admin()


class Questionnaire3(Page):
    form_model = models.Player
    form_fields = ['estrato_fut', 'political','s22','s23','s24','s25','un']


class Questionnaire(Page):
    form_model = models.Player
    form_fields = ['s1',
                   's2',
                   's3',
                   's4',
                   's5',
                   's6',
                   's7',
                   's8',
                   's9',
                   's10',
                   's11',
                   's12',
                   's13',
                       ]

class Questionnaire2(Page):
    form_model = models.Player
    form_fields = ['s14',
                   's15',
                   's15',
                   's16',
                   's17',
                   's18',
                   's19',
                   's20',
                   's21'
                   ]




class Fin(Page):
    pass


page_sequence = [
    Bienvenida,
    Consentimiento,
    AllGroupsWaitPage,
    Preguntas,
    AllGroupsWaitPage2,
    Instructions,
    Question,
    Results,
    Primed,
    AllGroupsWaitPage3,
    Treatment,
    Decisiones,
    AllGroupsWaitPage4,
    Elicitation,
    AllGroupsWaitPage5,
    Dictator,
    ResultsWaitPage,
    PDresults,
    eliResults,
    dicResults,
    sorteo,
    PayoffResults,
    Questionnaire3,
    Questionnaire,
    Questionnaire2,
    Fin

]


