import requests
from random import choice
from bs4 import BeautifulSoup
from csv import DictReader
# import os.path
# import scraper.py 

BASE_URL = 'http://quotes.toscrape.com'

# if not os.path.isfile('quotes.csv'):


def read_quotes(filename):
    with open(filename, 'r') as file:
        csv_reader = DictReader(file)
        return list(csv_reader)

def start_game(quotes): 
    quote = choice(quotes)
    remaining_guesses = 4
    print("Here's a quote:")
    print(quote['text'])
    guess = ''   

    while guess.lower() != quote['author'].lower() and remaining_guesses > 0:
        guess = input('Who said this quote? Guesses remaining: ' + str(remaining_guesses) + ' ')
        if guess.lower() == quote['author'].lower():
            print('Congrats! You Win!')
            break
        remaining_guesses -= 1
        if remaining_guesses == 3:
            res = requests.get(BASE_URL + quote['bio-link'])
            soup = BeautifulSoup(res.text, 'html.parser')
            birth_date = soup.find(class_='author-born-date').get_text()
            birth_place = soup.find(class_='author-born-location').get_text()
            print("Here's a hint: The author was born on " + birth_date + ' ' + birth_place)
        elif remaining_guesses == 2:
            print("Here's a hint: The author's first name starts with " + quote['author'][0])
        elif remaining_guesses == 1:
            last_initial = quote['author'].split(' ')[1][0]
            print("Here's a hint: =The author's last name starts with " + last_initial)
        else:
            print('No more guesses remaining. The answer is ' + quote['author'])

    again = ''
    while again.lower() not in ('y', 'yes', 'n', 'no'):
        again = input("Would you like to play again (y/n) ")
    if again.lower() in ('yes', 'y'):
        return start_game(quotes)
    else:
        print('Good Bye!')

quotes = read_quotes('quotes.csv')
start_game(quotes)
