import itertools

from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random

doc = """
This is a one-shot "Prisoner's Dilemma". Two players are asked separately
whether they want to cooperate or defect. Their choices directly determine the
payoffs.
"""


class Constants(BaseConstants):
    name_in_url = 'thesis'
    players_per_group = 2
    num_rounds = 1
    instructions_template = 'thesis/instruccionespd.html'
    primed = 'Sí'
    no_primed = 'No'
    fee = c(2)

    # dotación inicial para cada jugador en Prisoners' Dilemma
    endowmentpd = c(20)
    negative_wealth_shock = 0.5
    # dotación inicial para cada jugador en dictador
    endowmentd = c(4)
    elicitation_fee = c(4)
    elicitation_no_fee = c(0)
    # ganancia si 1 jugador elije verde y el otro azul,
    green_payoff = c(0)
    blue_payoff = c(-10)

    # ganancia si ambos jugadores elijen azul o verde
    both_green_payoff = c(-6)
    both_blue_payoff = c(-2)

 #para quiz
    # perdida si 1 jugador elije verde y el otro azul,
    blue_payoff_p = c(10)

    # perdida si ambos jugadores elijen azul o verde
    both_green_payoff_p = c(6)
    both_blue_payoff_p = c(2)

class Subsession(BaseSubsession):
    def creating_session(self):
        self.group_randomly()

        if self.round_number == 1:
            treatment = itertools.cycle(['NRV-CI','NVR-NCI','RV-CI','RV-NCI'])
            for p in self.get_players():
                p.participant.vars['treatment'] = next(treatment)
                print("@@@@@@@@@@@@---------------@@@@@@@@@@@ treatment is", p.participant.vars['treatment'])
                print("")

        for p in self.get_players():
            if p.participant.vars['treatment'] == 'NVR-NCI':
                p.treatment = p.participant.vars.get('treatment')
                p.primed = 'Estamos interesados en comprender sus experiencias cotidianas. Puede ser cualquier ' \
                           'evento. ¿Puede describir un acontecimiento de este último año?'
                p.endowment = Constants.endowmentpd
            elif p.participant.vars['treatment'] == 'NRV-CI':
                p.treatment = p.participant.vars.get('treatment')
                p.primed = 'Estamos interesados en comprender sus experiencias cotidianas. Puede ser cualquier ' \
                           'evento. ¿Puede describir un acontecimiento de este último año?'
                p.endowment = Constants.endowmentpd * Constants.negative_wealth_shock
            elif p.participant.vars['treatment'] == 'RV-NCI':
                p.treatment = p.participant.vars.get('treatment')
                p.primed = 'Estamos interesados en comprender las experiencias cotidianas que le puedan generar ' \
                           'ansiedad o miedo. Puede ser cualquier cosa, por ejemplo enfermarse, ser víctima de ' \
                           'la violencia, perder el trabajo… ¿Puede describir un acontecimiento de este último ' \
                           'año pasado que le haya causado miedo o ansiedad?'
                p.endowment = Constants.endowmentpd
            elif p.participant.vars['treatment'] == 'RV-CI':
                p.treatment = p.participant.vars.get('treatment')
                p.primed = 'Estamos interesados en comprender las experiencias cotidianas que le puedan generar ' \
                           'ansiedad o miedo. Puede ser cualquier cosa, por ejemplo enfermarse, ser víctima de ' \
                           'la violencia, perder el trabajo… ¿Puede describir un acontecimiento de este último ' \
                           'año pasado que le haya causado miedo o ansiedad?'
                p.endowment = Constants.endowmentpd * Constants.negative_wealth_shock

    def vars_for_admin_report(self):
        table_rows = []
        for player in self.get_players():
            row = player.participant.vars
            row['treatment'] = player.participant.vars.get('treatment')
            row['nombre'] = player.participant.vars.get('nombre')
            row['doc'] = player.participant.vars.get('doc')
            row['dilemma_payoff'] = player.participant.vars.get('dilemma_payoff')
            row['elicitation_payoff'] = player.participant.vars.get('elicitation_payoff')
            row['dictador_payoff'] = player.participant.vars.get('dictador_payoff')
            row['fee'] = player.participant.vars.get('fee')
            row['random_payoff'] = player.participant.vars.get('random_payoff')
            row['total_payoff'] = player.participant.vars.get('total_payoff')
            row['player'] = player.participant.vars.get('player')


            table_rows.append(row)
        return {'table_rows': table_rows}


class Group(BaseGroup):
   pass

def survey(label):
    return models.IntegerField(
        choices=[
            [0, 'No'],
            [1, 'Sí'],
        ],
        label=label,
        widget=widgets.RadioSelect,
    )

def cooperate(label):
    return models.BooleanField(
        choices=[
            [False, 'Verde'],
            [True, 'Azul'],
        ],
        label=label,
        widget=widgets.RadioSelect,
    )

NEIGHCHOICES = [
    (1, 'Kennedy'),
    (2, 'Suba'),
    (3, 'Engativá'),
    (4, 'Ciudad Bolívar'),
    (5, 'Bosa'),
    (6, 'Usaquén'),
    (7, 'San Cristobal'),
    (8, 'Rafael Uribe'),
    (9, 'Fontibón'),
    (10, 'Usme'),
    (11, 'Puente Aranda'),
    (12, 'Barrios Unidos'),
    (13, 'Tunjuelito'),
    (14, 'Teusaquillo'),
    (15, 'Chapinero'),
    (16, 'Antonio Nariño'),
    (17, 'Santa Fe'),
    (18, 'Los Mártires'),
    (19, 'La Candelaria'),
]

class Player(BasePlayer):
    nombre = models.StringField(label="Nombre y apellido:")
    doc = models.IntegerField(label="Cédula de Ciudadanía:")
    treatment = models.StringField()
    endowment = models.CurrencyField()
    primed = models.StringField()
    dilemma_payoff = models.CurrencyField()
    elicitation_payoff = models.CurrencyField()
    dictador_payoff = models.CurrencyField()
    random_payoff = models.CurrencyField()
    neighborhood = models.IntegerField(choices=NEIGHCHOICES, label='¿Cuál es la localidad en la que usted vive?')
    age = models.PositiveIntegerField(
        verbose_name='¿Cuál es su edad?',
        min=18, max=125)
    gender = models.CharField(
        choices=['Masculino', 'Femenino', 'Otro'],
        verbose_name='¿Cuál es su sexo?',
        widget=widgets.RadioSelect())
    estado = models.CharField(
        choices=['Soltera/o', 'Casada/o', 'Unión Marital de Hecho (Unión libre)', 'Viuda/o'],
        verbose_name='¿Cuál es su estado civil?',
        widget=widgets.RadioSelect())
    estrato = models.IntegerField(
        choices=[1, 2, 3, 4, 5, 6],
        verbose_name='De acuerdo a las facturas de sus servicios públicos, ¿cuál es el estrato de la vivienda actual donde reside?',
        widget=widgets.RadioSelect())
    estrato_fut = models.IntegerField(
        choices=[1, 2, 3, 4, 5, 6],
        verbose_name='¿Cuál es el estrato de la vivienda donde usted espera vivir a lo largo de su vida?',
        widget=widgets.RadioSelectHorizontal)

    q1 = models.CurrencyField(
        min=0,
        verbose_name='''
                  1. Si ambos eligen el color azul, ¿cuántos puntos pierde el otro participante?'''
    )
    q2 = models.CurrencyField(
        min=0,
        verbose_name='''
                  2. Si usted elige el color azul y el otro participante el color verde, 
                  ¿cuántos puntos pierde usted?'''
    )
    q3 = models.CurrencyField(
        min=0,
        verbose_name='''
                  3. Si usted elige el color verde y el otro participante el color azul, 
                  ¿cuántos puntos pierde el otro paricipante?'''
    )
    q4 = models.CurrencyField(
        min=0,
        verbose_name='''
                  4. Si ambos eligen el color verde, ¿cuántos puntos pierde usted?'''
    )

    def payoff_set_admin(self):
        self.participant.vars['treament'] = self.treatment
        self.participant.vars['nombre'] = self.nombre
        self.participant.vars['doc'] = self.doc
        self.participant.vars['dilemma_payoff'] = self.dilemma_payoff
        self.participant.vars['elicitation_payoff'] = self.elicitation_payoff
        self.participant.vars['dictador_payoff'] = self.dictador_payoff
        self.participant.vars['fee'] = Constants.fee
        self.participant.vars['random_payoff'] = self.activity_random_payoff()
        self.participant.vars['total_payoff'] = self.total_payoff()
        self.participant.vars['player'] = self.participant.id_in_session

    def correctq1(self):
        if self.q1 == -(Constants.both_blue_payoff):
            return 'Correcto.'
        else:
            return 'Incorrecto: Si ambos eligen el color azul, los dos pierden 2 puntos.'

    def correctq2(self):
        if self.q2 == -(Constants.blue_payoff):
            return 'Correcto.'
        else:
            return 'Incorrecto: Si usted elige el color azul y el otro participante el color verde,' \
                   ' usted pierde 10 puntos y el otro participante pierde 0 puntos.'

    def correctq3(self):
        if self.q3 == -(Constants.blue_payoff):
            return 'Correcto.'
        else:
            return 'Incorrecto: Si usted elige el color verde y el otro participante el color azul, usted pierde 0 puntos' \
                   ' y el otro participante pierde 10 puntos.'

    def correctq4(self):
        if self.q4 == -(Constants.both_green_payoff):
            return 'Correcto.'
        else:
            return 'Incorrecto: Si ambos eligen el color verde, los dos pierden 6 puntos.'

    def report_vars_for_database(self):
        vars_fields = [
            'treatment',
            'nombre',
            'doc',
            'dilemma_payoff',
            'elicitation_payoff',
            'dictador_correct',
            'fee',
            'random_payoff',
            'total_payoff',
            'player'
        ]

        for field in vars_fields:
            setattr(self, 'report_{}'.format(field), self.participant.vars.get(field))

    elicitation = models.IntegerField(
        choices=[
            (0, 'Verde'),
            (1, 'Azul')],
        label='¿Cuál cree que fue la decisión del otro participante?',
        widget=widgets.RadioSelect
    )

    def get_other(self):
        return self.get_others_in_group()[0]

    def get_other_choice_on_ego(self):
        other = self.get_other()
        return getattr(other, 'p{}'.format(self.neighborhood))

    def get_other_choice_on_ego_display(self):
        other = self.get_other()
        return getattr(other, 'get_p{}_display'.format(self.neighborhood))()

    def get_ego_choice_on_other_display(self):
        other = self.get_other()
        return getattr(self, 'get_p{}_display'.format(other.neighborhood))()

    def my_belief(self):
        if self.elicitation == 0:
            return 'Verde'
        else:
            return 'Azul'

    def set_pd_payoff(self):
        if self.get_ego_choice_on_other_display() == 'Azul' and \
                self.get_other_choice_on_ego_display() == 'Azul':
            self.dilemma_payoff = self.endowment + Constants.both_blue_payoff
        elif self.get_ego_choice_on_other_display() == 'Azul' and \
                self.get_other_choice_on_ego_display() == 'Verde':
            self.dilemma_payoff = self.endowment + Constants.blue_payoff
        elif self.get_ego_choice_on_other_display() == 'Verde' and \
                self.get_other_choice_on_ego_display() == 'Azul':
            self.dilemma_payoff = self.endowment + Constants.green_payoff
        elif self.get_ego_choice_on_other_display() == 'Verde' and \
                self.get_other_choice_on_ego_display() == 'Verde':
            self.dilemma_payoff = self.endowment + Constants.both_green_payoff

    def set_elicitation_payoff(self):
        if self.my_belief() == self.get_other_choice_on_ego_display():
            self.elicitation_payoff = Constants.elicitation_fee
        else:
            self.elicitation_payoff = Constants.elicitation_no_fee

    def set_dictador_payoff(self):
        self.dictador_payoff = Constants.endowmentd - self.dic

    def set_random_payoff(self):
        self.random_payoff = random.choice([self.elicitation_payoff, self.dictador_payoff])

    def set_payoffs(self):
        self.payoff = self.dilemma_payoff + self.random_payoff

    def activity_random_payoff(self):
        if self.random_payoff == self.elicitation_payoff:
            return 'Decisión dos'
        elif self.random_payoff == self.dictador_payoff:
            return 'Decisión tres'

    def money_payoff(self):
        return self.total_payoff().to_real_world_currency(self.session)

    def total_payoff(self):
        return self.participant.payoff_plus_participation_fee()

    recall = models.TextField(label='Escriba su respuesta en este recuadro:')
    dic = models.CurrencyField(
        min=0, max=Constants.endowmentd,
        label='Por favor indique cuántos puntos desea donar'
    )
    ong = models.CharField(
        choices=[
            'Colombia con Memoria (brindan asistencia jurídica a personas que hayan sido víctimas del conflicto armado interno en Colombia).',
            'Cruz Roja Bogotá (buscan prevenir y aliviar, en todas las circunstancias, el sufrimiento humano; proteger la vida y la salud, y hacer respetar a la persona humana).',
            'Médicos sin frontera - Colombia (asisten a personas amenazadas por conflictos armados, violencia, epidemias o enfermedades olvidadas).',
            'Un Techo para mi País - Colombia (buscan superar la situación de pobreza de las personas brindando acceso a vivienda).',
            'Colombia Crece (organización católica que crea espacios educativos para los más necesitados).',
            'Ecosueños (protegen a niños y adolescentes de Bogotá quienes sus derechos han sido vulnerados, amenazados o inobservados).',
            'No deseo donar.'],
        widget=widgets.RadioSelect(),
        label='Fundaciones'
    )

    s1 = survey('Robo no armado')
    s2 = survey('Robo armado')
    s3 = survey('Violencia sexual')
    s4 = survey('Secuestro')
    s5 = survey('Pelea callejera')
    s6 = survey('Violencia doméstica')
    s7 = survey('Daños a sus propiedades')
    s8 = survey('Extorsión')
    s9 = survey('Agresión verbal')
    s10 = survey('Acoso')
    s11 = survey('Persecusión')
    s12 = survey('Abuso psicológico')
    s13 = survey('Amenaza de muerte')


    s14 = models.IntegerField(
        choices=[
            1, 2, 3, 4,])
    s15 = models.IntegerField(
        choices=[
            1, 2, 3, 4,])
    s16 = models.IntegerField(
        choices=[
            1, 2, 3, 4,])
    s17 = models.IntegerField(
        choices=[
            1, 2, 3, 4,])
    s18 = models.IntegerField(
        choices=[
            1, 2, 3, 4,])
    s19 = models.IntegerField(
        choices=[
            1, 2, 3, 4,])
    s20 = models.IntegerField(
        choices=[
            1, 2, 3, 4,])
    s21 = models.IntegerField(
        choices=[
            1, 2, 3, 4,])
    s22 = models.IntegerField(
        choices=[
            1, 2, 3, 4, 5, ])
    s23 = models.IntegerField(
        choices=[
            1, 2, 3, 4, 5, ])
    s24 = models.IntegerField(
        choices=[
            (0, 'No'),
            (1, 'Sí')
        ],
        label='¿Usted nació en Bogotá?',
        widget=widgets.RadioSelect
    )
    un = models.IntegerField(
        choices=[
            (0, 'No'),
            (1, 'Sí')
        ],
        label='¿Usted estudia en la Universidad Nacional de Colombia?',
        widget=widgets.RadioSelect
    )
    political = models.IntegerField(
        choices=[
            [1, 'Nunca'],
            [2, 'Raramente'],
            [3, 'Casi siempre'],
            [4, 'Todas las veces'],
        ],
        label= '¿Con qué frecuencia vota en elecciones políticas?',
        widget=widgets.RadioSelect,)
    s25 = models.IntegerField(
        choices=[
            [1, 'Primaria'],
            [2, 'Secundaria'],
            [3, 'Técnico/Tecnólogo'],
            [4, 'Universidad'],
            [5, 'Posgrado'],
        ],
        verbose_name='Indique cuál es el nivel más alto de educación alcanzado por usted:'
    )


for i, label in NEIGHCHOICES:
    Player.add_to_class('p{}'.format(i), cooperate(label))








