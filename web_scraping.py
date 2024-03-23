# -*- coding: utf-8 -*-
"""
@author: Riboulet Ronan
@Date: 08.03.2024

Web Scraping Self Taught Course

"""

#Importation of librairies
import requests # Library that scrapes HTML content from a web page
from bs4 import  BeautifulSoup # Library that parses HTML content from a web page

#Variables
URL = "https://realpython.github.io/fake-jobs/"
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

results = soup.find("div", id="ResultsContainer") # We filter the results with the content of the web page that we are interested in

job_loc = results.find_all("p", class_="location") # We look for the jobs locations
job_descr = results.find_all("h2", class_="title is-5") # We look for the jobs descriptions
job_comp = results.find_all("h3", class_="subtitle is-6 company") # We look for the jobs descriptions
job_elements = results.find_all("div", class_="card-content") # List of all the job offers and their infos = Parent element where all the content is

job_python = results.find_all("h2", string=lambda text: "python" in text.lower()) #The lambda function = anonymous function that can take an indefinite number of arguments but can have just one expression
                                                                                   #The lambda function looks at the text of each <h2> element, converts it to lowercase, and checks whether the substring 
                                                                                   #"python" is found anywhere

# We have to access the parent elements of h2 in order to get all the elements
job_python_elements = [
    h2_elem.parent.parent.parent for h2_elem in job_python
    ]

#HTML source code retriever function
def html_source_print():                     
    print(page.text) # Print the HTML content of the source page
    
def filter_location():
    #print(soup)
    #print(results.prettify())
    for loc in job_loc:
        print(loc.text, end="\n") # Raw listing of the locations

def filter_descr():
    for descr in job_descr:
        print(descr.text, end="\n")    
        
def filter_comp():
    for comp in job_comp:
        print(comp.text, end="\n") 

def list_offers():
    for job_element in job_elements:
        descr = job_element.find("h2", class_="title is-5")
        comp = results.find("h3", class_="subtitle is-6 company")
        loc = results.find("p", class_="location")
        print("Job description: " + descr.text + "\n" + "Company name: " 
        + comp.text + "\n" + "Job's location: " + loc.text + "\n"*2)
        
def python_offer(): # Learn how to pass functions into BeautifulSoup method + learn to research occurences of a string   

    for job in job_python_elements:                                                           
        python_loc = job.find("h2", class_="title is-5")
        python_descr = job.find("h3", class_="subtitle is-6 company")
        python_comp = job.find("p", class_="location")
        print(python_loc.text.strip() + "\n" + python_descr.text.strip() + "\n" + python_comp.text.strip() + "\n") #Error with this print if we don't access the parent elements


def html_fetch(): # Fetch URL links 
     for html_link in job_python_elements:                                                    
        links = html_link.find_all("a", string=lambda text: "apply" in text.lower()) # Just fetch the second link
        for link in links:
            link_url = link["href"]
            print(f"Apply here: {link_url}\n")
        


#Main for function calls
    
def main(choice):
  
    if(choice == 1):
        html_source_print()
    if(choice == 2):
        filter_location()
        html_source_print()
    if(choice == 3):
        filter_descr()
    if(choice == 4):
        filter_comp()
    if(choice == 5):
        list_offers()
    if(choice == 6):
        python_offer()
    if(choice == 7):
        html_fetch()
   
        
########## Main ##########   
#Chose the function to use in the main   
main(7)

