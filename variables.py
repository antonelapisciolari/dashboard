
import streamlit as st
import location.es as vars

#main Db
registroAprendices="1WCl-0xzjea88aFdilbcXyKoYF9_N5JkOm0co4Cez8D0"
feedbackSheets="1_d0aGSzQ4xB0FIkVikWBii3n3tF7l3it4GmNrDZw61s"
connectionGeneral="gsheets"
connectionFeedbacks="gsheets_feedback"
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

page_icon="https://assets4.cdn.iberostar.com/assets/favicon-aed60cf99a80a69e437a1476d22eea0d083d788070b7f4ac4c6c53595cf0687c.ico"
companyIcon="./images/logoCreciendoJuntos.png"
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

#menu pages
tutorDashboard=vars.tutorDashboard
aprendizDashboard=vars.aprendizDashaboard
adminRecursosTutorDashboard=vars.adminRecursosTutorDashboard
adminTutorDashboard=vars.adminTutorDashboard
preOnboardingLinks = ["Guía Express para el Tutor/a!", "https://docs.google.com/document/d/1XB9LdMoVHBC5zxhtQE38S6cnUMw_1LAUYg-qTcKhjMI/edit?tab=t.0"]
onboardingLinks = ["Meeting Tips – ¡Primer Día del Aprendiz!", "https://docs.google.com/document/d/1f1QN7PlVTcpcXLk-ELx37Ulb7dOCTbDDcMqHWQ3UNk0/edit?tab=t.0#heading=h.f6elu9z606tn"]
seguimientoLinks = ["Meeting Tips - Seguimiento", "https://docs.google.com/document/d/1Yjh1DlffuTeq5PZNVSgUZ_WyYOMfb7IolpYFl4qYbDw/edit?tab=t.0#heading=h.yvse9tfgikrc"]
cierreLinks = ["Meeting de Cierre", "https://docs.google.com/document/d/1hn37K1A9O1Yr1jFyLfhp8zKNUdGqU5uEzX4mquRj_gE/edit#heading=h.p2j4qotp1ckv"]
