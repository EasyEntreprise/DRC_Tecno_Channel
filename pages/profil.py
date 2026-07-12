from dash import html
from datetime import datetime
import dash_mantine_components as dmc
from datetime import datetime
from dash_iconify import DashIconify

####################
## Date
start_year   = 2019
start_extrat = 2023
start_IT = 2026

experience  = datetime.now().year - start_year
exper_extrat = datetime.now().year - start_extrat
exper_it = datetime.now().year - start_IT

def layout():
    return dmc.Container(
        fluid= True, 
        children=[

        dmc.Title("ABOUT ME", order= 1, style={"marginTop": 20}), # order = 1, correspond a H1
        html.Hr(),

        # Un espaceur vertical pour aerer (optionnel mais tres propre avec Mantine)
        dmc.Space(h= "xl"),

        dmc.Grid(
            children=[
                # Colonne gauche
                dmc.GridCol(
                    span= 4,
                    children=[
                        dmc.Center(
                            dmc.Avatar(
                                src= "/assets/Rodrigue folio-1.png",
                                radius= 150,
                                size= 250
                            )
                        ),

                        dmc.Space(h=30),
                        dmc.Title("Experience and Qualifications", order= 2),
                        dmc.List([
                            dmc.ListItem(f"{experience} yers of experience in  the business of selling Tecno brand phone ;"),
                            dmc.ListItem(f"{exper_extrat} years experience extracting actionable insights from data"),
                            dmc.ListItem("Strong hands-on experience and knowledge in Python and Excel"),
                            dmc.ListItem("Good understanding of statistical principles and their respective application ;"),
                            dmc.ListItem("Excellent team-player and displaying a strong sense of initiative on tasks ;"),
                            dmc.ListItem(f"{exper_it} Years in CyberSecurity domain"),
                        ])
                    ]
                ), 

                # Colonne de droite
                dmc.GridCol(
                    span= 8,
                    children= [
                        dmc.Title("NSINSULU MAYANZA Rodrigue", order= 1),
                        dmc.Text(" Junior Data Analyst, Data Engener, Data Scientist, Machine and Deep Learning and  IT Cyber-security.",
                                 "C.E.O at Easy Holding"
                                 ),

                        html.Br(),
                        html.Div(
                            [
                                DashIconify(
                                    icon = "mdi:email",
                                    width = 20,
                                    color= "#4dabf7",
                                ),

                                html.A("rodriguensinsulu@gmail.com", href= "mailoto:rodriguensinsulu@gmail.com", style={"color":"white", "textDecoration":"none", "marginleft": "8px"},),

                                html.Span("   |   "),

                                DashIconify(
                                    icon = "mdi:phone",
                                    width= 20
                                ),

                                html.Span("(+243) 89 666 3756 - 81 365 3093"),

                                html.Span("   |   "),

                                DashIconify(
                                    icon= "mdi:map-marker",
                                    width= 20
                                ),

                                html.Span("Kinshasa, DRC"),

                                
                            ], style= {"display":"flex", "alignItems": "center",}
                        ),


                        #dmc.Anchor("Mail", href="mailto:rodriguensinsulu@gmail.com", underline="hover"),
                        dmc.Space(h=30),
                        dmc.Title("Hard Skills", order=2),
                        dmc.List([
                            dmc.ListItem("Software Engineer      : Python (Scikit-learn, Pandas, Numpy, PySide, django), C++, Desktop, Mobile and full-stack developer ;"),
                            dmc.ListItem("Data Visualisation     : Plotly, Dash, Streamlit, PowerBI, Ms Excel ;"),
                            dmc.ListItem("Modeling               : Logistic regression, linear regression, decision trees ;"),
                            dmc.ListItem("Database Administrator : MySQL, MongoDB, Postgres and NO-SQL ;"),
                            dmc.ListItem("Data Engineer          : Data Engineer, Data Analyst, Data Science and Machine-Deep Learning ;"),
                            dmc.ListItem("Security               : CyberSecurity Engineer."),
                        ])
                    ]
                )
            ]
        )
    ])



