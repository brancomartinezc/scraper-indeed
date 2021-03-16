import re
import requests
from bs4 import BeautifulSoup

""" From a txt file file creates a dictionary with techs to search """
def create_techs_dict():
    techs = {}
    file = open('search.txt', 'r')
    techs_list = file.read().split(" ")

    for tech in techs_list:
        techs.update({tech:0})

    file.close()

    return techs


""" Generates the url from position """
def get_url(position):
    template = 'https://www.indeed.com/jobs?q={}&start=00'
    url = template.format(position)

    return url


""" Generates a string with the desciption of the job post """
def get_job_description(post):
    job_url = 'https://www.indeed.com' + post.h2.a.get('href')
    response = requests.get(job_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    try:
        job_desc = soup.find('div', 'jobsearch-jobDescriptionText').text
    except AttributeError:
        print("job_desc NONE") #debugger
        job_desc = None
    
    return job_desc


""" count the techs that are in the job description """
def count_techs(description,techs):
    job_desc = re.split(r'[-,.\s]\s*',description)
    techs_to_add_one = []

    for word in job_desc:
        word_lower = word.lower()
        for tech in techs:
            if word_lower == tech:
                if tech not in techs_to_add_one:
                    techs_to_add_one.append(tech)

    for tech in techs_to_add_one:
        techs[tech] += 1


def main(position):
    techs = create_techs_dict()
    url = get_url(position)

    while True:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        posts = soup.find_all('div', 'jobsearch-SerpJobCard')
        i=1 #debugger
        for post in posts:
            job_desc = get_job_description(post)
            if job_desc != None:
                count_techs(job_desc,techs)
            print(f"{i}: {techs}") #debugger
            i += 1 #debugger

        #Next page
        try:
            url = 'https://www.indeed.com' + soup.find('a', {'aria-label': 'Next'}).get('href')
            print(url) #debugger
        except AttributeError:
            print("URL ERROR") #debugger
            break
    
    print(f"final: {techs}") #debugger

if __name__ == '__main__':
    main('backend') #change the position to search
