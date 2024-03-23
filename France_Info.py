# -*- coding: utf-8 -*-
"""
@author: Riboulet Ronan
@Date: 08.03.2024

Web Scraping Self Taught Course
First project - Newsletter from FranceInfo

"""

########## Importation of librairies ##########
import requests # Library that scrapes HTML content from a web page
from bs4 import  BeautifulSoup # Library that parses HTML content from a web page
from urllib.parse import urljoin # Library to parse an url to the content of the retrieved links
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


########## Global variables ##########
URLHomePage = "https://www.francetvinfo.fr/" # URL of FranceInfo Home Page
HomePage = requests.get(URLHomePage) # Retrieve the HTML content of the webpage
soup = BeautifulSoup(HomePage.text, "html.parser") # Parsing the content of the HTML
Main = soup.find("main", id="base-page__main-content") # Getting only the information from the main content base page part of the HTML
AllLinks = Main.find_all('a') # Scraping only the content with the 'a' tag


def LinkScanner():
    # List to store the Themes, URLs, and Titles
    ThemesURLsTitle = []

    for link in AllLinks:
        if 'href' in link.attrs and link['href'].startswith('/'): # Check if the lines of the HTML has the href tag (used for links)
            URL = link['href']
            Theme = URL.split('/')[1] # Retrieve the theme of the news for the link
            HTMLTitle = link.find('p', class_=lambda text: text and "m__title" and "article" in text)   # Find the title of the article
            if HTMLTitle:
                Title = HTMLTitle.get_text()
                ThemesURLsTitle.append(((Theme, URL, Title)))   # Store the three infos in a list
    
    #print(ThemesURLsTitle)  # Debugging print statement
    return ThemesURLsTitle # Return the list created above


def LinksSaver(Topics):
    Topics = set() # List set
    
    ListOfLinks = {DicTheme:[] for DicTheme in Topics} # Creation of the dictionnary storing the Themes, URLs and Titles of the news
    
    
    ThemesURLs = LinkScanner() # Call of the LinkScanner function
    
    for Theme, URL, Title in ThemesURLs:    
        UsableURL = urljoin(URLHomePage, URL) # Join the URL of the news with the URL of the main to create a usable URL 
        
        if Theme in ListOfLinks:
            ListOfLinks[Theme].append({UsableURL, Title}) # Store the infos  in the dictionnary
        else:
            ListOfLinks[Theme] = [{UsableURL, Title}] # Create the theme category that doesn't already exist
                 
    #print(ListOfLinks.keys()) # Debugging print statement
    return(ListOfLinks) # Return the dictionnary

def UI():
    Topics = LinkScanner()
    dic = LinksSaver(Topics)
    Themes = list(dic.keys())
    
    Answers = []
    
    for Theme in Themes:
        while True:  # Loop until a valid answer is provided
            print("-", Theme)
            Answer = input("Est-ce que ce thème vous intéresse ?: y/n\n")
            if Answer.lower() in ['y', 'n']:  # Check if the input is either 'y' or 'n'
                Answers.append(Answer.lower())  # Add the answer to the list
                break  # Exit the loop if a valid answer is provided
            else:
                print("Erreur: Veuillez répondre par 'y' ou 'n'")  # Print an error message
    return Answers
            
def Questionnaire():
    Answers = UI() # Get the return value of UI()
    Topics = LinkScanner()
    dic = LinksSaver(Topics)
    InfosToSend = []
    ThemesChosen = []
    URLToSend = []
    TitleToSend = []
    
    for index, key in enumerate(dic):
        if Answers[index] == "y":
            InfosToSend.append(dic[key])
            ThemesChosen.append(key)
    
    # Debugging print statements
    #print(len(InfosToSend))
    
    # Iterate over each dictionary in InfosToSend
    for item in InfosToSend:
        # Iterate over key-value pairs in the dictionary
        for key, value in item:
            if (key.startswith("https://www.francetvinfo.fr/")) and ((key not in URLToSend) or (value not in TitleToSend)):
                URLToSend.append(key)
                TitleToSend.append(value)
            elif (value.startswith("https://www.francetvinfo.fr/")) and ((key not in TitleToSend) or (value not in URLToSend)):
                URLToSend.append(value)
                TitleToSend.append(key)
    #print(URLToSend, TitleToSend) # Debugging print statements
    
    return TitleToSend, URLToSend, ThemesChosen

def Mail():
    TitleToSend, URLToSend, ThemesChosen = Questionnaire()

    
    answ = "n"    
    while answ != "y":
        MailToSend = input("Veuillez entrer votre adresse e-mail: \n")  
        answ = input("Êtes-vous sûr de votre mail ? y/n: ")
        
   # Construct the message body
    message = f"""\
    Bonjour,    
        
    Merci d'avoir choisi d'utiliser cet outil de création de Newsletter !!! <3
    
    Vous avez choisi comme thème(s) de news à recevoir:
    """
    for theme in ThemesChosen:
        message += f"\n- {theme}\n"
    

    for i in range(len(TitleToSend)):
        message += f"\nThème: {URLToSend[i].split('/')[3].capitalize()}\n"
        message += f"Titre : {TitleToSend[i]}\nURL : {URLToSend[i]}\n\n"    

     
    # Set up the SMTP server
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587  # For Gmail
    
    # Create a message object
    msg = MIMEMultipart()
    msg['From'] = 'Python Script'
    msg['To'] = MailToSend
    msg['Subject'] = 'Newsletter Python FranceInfo'

    # Attach the message body
    msg.attach(MIMEText(message, 'plain'))

    # Connect to the SMTP server
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # Secure the connection
    server.login('newsletterpython13@gmail.com', 'dias vsgw zokr whsv')

    # Send the email
    server.send_message(msg)

    # Close the connection
    server.quit()
    
    print("\n\n\nMail envoyé !!!")
    

    
########## Main ##########    
Mail()


