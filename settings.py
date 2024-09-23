from os import environ

ROOMS = [
    {
        'name': 'lab',
        'display_name': 'VSEEL (KRAN 701)',
        'participant_label_file': '_rooms/VSEEL701.txt',
    },
]


SESSION_CONFIGS = [
    dict(
        name="Dynamic_Power_Test",
        display_name="Dynamic Power Inequality Experiment",
        num_demo_participants=4,
        app_sequence=[
            'DynamicPower_01_Consent',
            'DynamicPower_02_Introduction',
            'DynamicPower_02a_RiskAversionElicitation',
            'DynamicPower_02b_LossAversionElicitation',
            'DynamicPower_02c_SocialPreference',
            'DynamicPower_02d_IQ',
            'DynamicPower_03_Instructions',
            'DynamicPower_04_Quiz',
            'DynamicPower_05_Experiment',
            'DynamicPower_06_PayoffScreen',
            'DynamicPower_07_Demographics',
            'DynamicPower_08_FeedbackQuestions',
            'DynamicPower_09_Feedback',
        ],
        Benefit= 109,
        Size = 2,
        Contest = "endogenous",
        Half_Effort_normalized =0.812 ,
        Sequence=3,
        Matches= 10,
        # Parameters for random termination, keep variations for now
        CutoffRoll=10,
        # Second Year
        Faction_Size = 1,
        # Third Year
        Shock = "None",
        use_browser_bots=False,
        
        
        # Unchanged Parameters
        R0 = 60,
        Cost = 20.4,
        Ratio = 0.1,
        kappa = 12,

        doc="""
            
            <br> <b>'Benefit' </b> parameter determines the underlying benefit to cooperation (high is  218; low is 109 ) </br>
            <br> <b> 'Size' </b> parameter determines the size of the environment/number of factions (2, 4) </br>
            <br> <b> 'Contest' </b> parameter determines the nature of the revision of power: ('exogenous'=proportional to payoff, 'endogenous'=Tullock contest format) </br>
            <br> <b> 'Half_Effort_normalized' </b> parameter has values of  .812 or 0.406. Note here it is the lower case x0 </br>
         
            <br> <b> 'Sequence'</b> parameter determines which sequence of supergame lengths is used. </br>
            <br> <b> 'Matches' </b> parameter determines how many matches are played. </br>
            
            <br>*** Parameters for random termination: </br>
            <br> <b> 'CutoffRoll' </b> parameter determines the continuation probability (10 sided dice,  .9-> cutoff=10, ). </br>
            
            <br> *** Later parameters: </br>
            <br> <b>'Faction_Size' </b> parameter determines the composition of faction ('individual'=1, 'group'=2, each faction consists 2 subjects) </br>
            <br> <b> 'Shock' </b> parameter determines the payoff shocks ('None', 'whole' = shock impacting the total payoff as a whole, 'independent' = shocks impacting each faction independently) </br>
            
            
            <br> *** Unchanged parameters: </br>
            <br> <b>'R0' </b>  Amount gained for not cooperating </br>
            <br> <b> Cost </b> Cost of cooperation   </br>
            <br> <b>  Ratio  </b>  Only for Exogenous , effort is a ratio of the payoff， </br>
            <br> <b>  kappa </b>   Steepness </br>

            """
    ),

]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=0.002, participation_fee=5.00, doc=""
)

PARTICIPANT_FIELDS = []
SESSION_FIELDS = []


# INSTALLED_APPS = ['otree', 'django.contrib.staticfiles']
# STATIC_URL = '/static/'


# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '4552513837123'
