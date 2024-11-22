
import streamlit as st
import location.es as vars

#main Db
registroAprendices="1WCl-0xzjea88aFdilbcXyKoYF9_N5JkOm0co4Cez8D0"
feedbackSheets="1_d0aGSzQ4xB0FIkVikWBii3n3tF7l3it4GmNrDZw61s"
agendaSheets="1OJ7tinHw7K-fx_kiK3r7pAHPXVf-PO8b0o8FDhXpGwg"
connectionGeneral="gsheets"
connectionFeedbacks="gsheets_feedback"
connectionFeedbackPerfilTutor="gsheets_feedback_perfil_tutor"
worksheetPerfilTutor="formTutor"
connectionUsuarios="usuarios"
worksheetUsuarios="Usuarios"
worksheetPulse1Semana="formularioPulse1Semana"
worksheetCambioArea="formularioCambioArea"
worksheetFormulario1Mes="formulario1Mes"
worksheetFormulario4Mes="formularioCuatroMes"
worksheetFormularioAprendizCierre1Ciclo="formularioAprendizCierre1Ciclo"
worksheetFormularioAprendizCierre2Ciclo="formularioAprendizCierre2Ciclo"
worksheetFormularioTutorCierre1Ciclo="formularioTutorCierre1Ciclo"
worksheetFormularioTutorCierre2Ciclo="formularioTutorCierre2Ciclo"
formAprendiz="formAprendiz"
rotationSheet="Rotación"
costeSheet = ""
formsSheet = ""
#branding colors 
aquamarine="#3AA597"
amarillo="#FECA1D"
azul="#002855"
orange="#FF6B35"
celeste="#007EA7"
teal="#00A6A6"
gris="#8D99AE"

#login
username=vars.username
password=vars.password
forgotPassword=vars.forgotPassword
loginButton=vars.loginButton
logoutButton=vars.logoutButton
errorRedirection=vars.errorRedirection
IncorrectPassword=vars.IncorrectPassword
logoutMessage=vars.logoutMessage
loginMessage=vars.loginMessage
loginDescription=vars.loginDescription
noDatosDisponibles="No hay datos disponibles"

page_icon="./images/icon.ico"
companyIcon="./images/smallIcon.png"
title= vars.title
#tutor dashboard 
preOnboardingImage="https://github.com/user-attachments/assets/7dd8d62d-b5ce-44ac-bda9-5eca1459a8b3"
onboardingImage="https://github.com/user-attachments/assets/2234162c-6c63-4ea4-9565-69206f7870fa"
seguimientoImage="https://github.com/user-attachments/assets/e55e814d-2b7c-4b7b-a8f6-e0c6927e06ca"
cierreImage="https://github.com/user-attachments/assets/c7609f53-4bb7-4b1b-8d1f-44bdbd24f379"
recursosUtiles=vars.recursosUtiles
documentacionTitle=vars.documentacionTitle
tabPreOnboarding=vars.tabPreOnboarding
tabOnboarding=vars.tabOnboarding
tabSeguimiento=vars.tabSeguimiento
tabCierre=vars.tabCierre
tabFeedback="Formularios"

#menu pages
tutorDashboard=vars.tutorDashboard
aprendizDashboard=vars.aprendizDashaboard
adminRecursosTutorDashboard=vars.adminRecursosTutorDashboard
adminTutorDashboard=vars.adminTutorDashboard
preOnboardingLinks = ["Guía Express para el Tutor/a!", "https://docs.google.com/document/d/1XB9LdMoVHBC5zxhtQE38S6cnUMw_1LAUYg-qTcKhjMI/edit?tab=t.0"]
onboardingLinks = ["Manual 1: Consejos Claves Primer día", "https://docs.google.com/document/d/1f1QN7PlVTcpcXLk-ELx37Ulb7dOCTbDDcMqHWQ3UNk0/edit?tab=t.0#heading=h.f6elu9z606tn"]
seguimientoLinks = ["Manual 2: Consejos Claves Cambio de área", "https://docs.google.com/document/d/1Yjh1DlffuTeq5PZNVSgUZ_WyYOMfb7IolpYFl4qYbDw/edit?tab=t.0#heading=h.yvse9tfgikrc"]
cierreLinks = ["Manual 4: Consejos claves Cierre", "https://docs.google.com/document/d/1hn37K1A9O1Yr1jFyLfhp8zKNUdGqU5uEzX4mquRj_gE/edit#heading=h.p2j4qotp1ckv"]
formsLinks = ["Formulario 1º semana", "https://fpdual-dashboard.streamlit.app/pulse_primera_semana",
"Cambio Area","https://fpdual-dashboard.streamlit.app/formulario_cambio_area",
"Formulario 1º mes Aprendiz", "https://fpdual-dashboard.streamlit.app/formulario_primer_mes",
"Formulario 4º mes Aprendiz", "https://fpdual-dashboard.streamlit.app/formulario_cuarto_mes",
"Formulario Aprendiz - Cierre 1er Ciclo","https://fpdual-dashboard.streamlit.app/formulario_aprendiz_cierre_primer_ciclo",
"Formulario Aprendiz - Cierre 2do Ciclo","https://fpdual-dashboard.streamlit.app/formulario_aprendiz_cierre_segundo_ciclo",
"Formulario Tutor - Cierre 1er Ciclo","https://fpdual-dashboard.streamlit.app/formulario_tutor_cierre_primer_ciclo",
"Formulario Tutor - Cierre 2do Ciclo","https://fpdual-dashboard.streamlit.app/formulario_tutor_cierre_segundo_ciclo"
              ]

#admin dashboard
aprendiz_looker_url = "https://lookerstudio.google.com/embed/reporting/a240d7c8-63aa-405e-b320-4aff88c57547/page/XQXmD"
presupuesto_looker_url="https://lookerstudio.google.com/embed/reporting/a98142e9-3679-4dc5-b4c7-a201853d976f/page/p_fq1n4ahhjd"
aprendiz_2025_looker_url="https://lookerstudio.google.com/embed/reporting/8da6524c-03a4-4f30-9998-d2087e9c115e/page/XQXmD"

#forms
folderIdAprendriz="1ipDPOh8RhBMQF6SpA9nKglcvavZKHh-E"
folderIdTutor="1qQZGjDTukHla-_pbhLeppLHxogNKSmML"
smileFacePath="https://github.com/user-attachments/assets/dd9fe972-19e1-46c0-bff6-bb2df20716ef"
rocketPath="https://github.com/user-attachments/assets/75b1a65f-6416-4366-b54e-ba3b56c49333"
camaraPath="https://github.com/user-attachments/assets/50d2c611-8a03-42c5-81da-1f6cf1820942"
autocompletarTutor="=IFERROR(VLOOKUP($A3,Base_datos!$A:$C,3,0))"
autocompletarNombre="=IFERROR(VLOOKUP($A3,Base_datos!$A:$D,4,0))"