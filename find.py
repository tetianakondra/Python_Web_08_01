import json

from mongoengine import disconnect
import redis
from redis_lru import RedisLRU

from models import Author, Quote

client = redis.StrictRedis(host = "localhost", port = 6379, password=None)
cache = RedisLRU(client)

@cache
def find_author(name):
    print("the first call")
    authors = Author.objects(fullname__contains=(name))
    for auth in authors:
        quotes = Quote.objects(author=auth.id)
        list_quotes = []
        for quote in quotes:
            list_quotes.append(f"Author with symbols in name {name} said: {quote.quote}")
        return list_quotes
        

@cache
def find_tag(searching_tag):
    print("the first call")
    quotes = Quote.objects()
    quote_ids = set()
    quote_list = []
    for quo in quotes:
        for tag in quo.tags:
            if searching_tag in tag:
                quote_ids.add(quo.id)
    for el in quote_ids:
        quote = Quote.objects(id=el)
        quote_list.append(quote[0].quote)
    return quote_list


@cache
def find_tags(searching_tags):
    print("the first call")
    tags = (searching_tags).split(",")
    quotes = Quote.objects()
    quote_ids = set()  
    quote_list = [] 
    for quo in quotes:
        for tag in tags:
            if tag in quo.tags:
                quote_ids.add(quo.id)
    for el in quote_ids:
        quote = Quote.objects(id=el)
        quote_list.append(quote[0].quote)
    return quote_list


def  main():
        
    while True:
        user_command = input("Enter <command>: <data for serching> or 'exit' to end the programm ")
        user_search = user_command.find(": ")
        
        if user_command.lower() == "exit":
            print("Goodbye")
            disconnect()
            break

        if user_command[0:user_search] == "name":
            print(find_author(user_command[user_search+2:]))


        if user_command[0:user_search] == "tag":
            print(find_tag(user_command[user_search+2:]))


        if user_command[0:user_search] == "tags":
            print(find_tags(user_command[user_search+2:]))


    disconnect()
    

if __name__ == "__main__":
    main()
