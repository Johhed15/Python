#!/usr/bin/env python3

# importing sys , os, text_stats and random
import sys
import text_stats as ts
import random as rd
import string as stri
from collections import Counter
import ast


# Also added the argument for punctations here
def read_txt_file(path,punc=False):
    text = ts.read_txt(path,punc) # using the txt reader function from ts
    return text

# terminal 
def provide_txt_terminal():
# Trying to see if there is a txt file or not in the command
    if len(sys.argv) > 3:
        
        # running try to see if the file exists and is of the correct sort
        try:
            with open(sys.argv[1], 'r',encoding='utf-8')  as file:# opening the file
                text = file.read().lower() # saving the conent in text and to lower
                translator = str.maketrans('','',stri.punctuation)
                text = text.translate(translator) # removing punctations
                text = text.replace('”','')
                text = text.replace('“','')
                return text

        except FileNotFoundError: # error if the file isnt found
            print('The first file isnt found:',sys.argv[1])
            sys.exit(0) # exiting the program
            
        except Exception as e:
            print('An error occurred while reading the file:', e)
            sys.exit(0)  
            
    elif len(sys.argv) == 1: # if only the 
        print('File_Error: You need to provide a txt file, a starting word and how many generated words you want')
        sys.exit(0) # exiting the program
        
    elif len(sys.argv) == 2: # if only the 
          print('You need to provide a starting word and the number of generated words you want')
          sys.exit(0) # exiting the program
        
    else:
        print('You need to provide how many words to be generated')
        sys.exit(0) # exiting the program


def create_neighbors(filename):
    split_string = filename.split() # splitting the string
    count = Counter(split_string) # create counter object
    most_frequent = count.most_common() # picking out the most common words
    
    successor = {}
    
    for key, value in most_frequent:
        successor[key] = ts.following_word(filename, key)
    
    with open('neighbors.txt','w') as f:
        f.write(str(successor))



def generate_text(filename, word, max_amount):  
    max_amount = int(max_amount)
    if word.lower() not in filename:
        raise ValueError("The word does not occur in the text provided")

    cur_word = word.lower()
    msg = cur_word 
    
    try:
        with open('neighbors.txt', 'r', encoding= 'cp1252') as file:
        
                successor = file.read()# all neighbors to lower and saving the text
        successor = ast.literal_eval(successor)
        
    except:
        print('Add the neighbours.txt to the directory, or create it with the create_neighbours function')
        sys.exit(0) 
        
    while len(msg.split()) <= max_amount: 
        neighbors = successor[cur_word]
        if len(neighbors) == 0:
               print("The chosen word is a terminal node and has no successor, the generetaded text looks as follows:\n")
               print("-"*50,'\n')
               break
        total = sum([value[1] for value in neighbors])
        relative = [previous_tuple[1]/total for previous_tuple in neighbors] # all weights in a list
        list_words = [value[0] for value in neighbors] # all succsessive word in a list
        cur_word = str(rd.choices(list_words, relative, k = 1))
        cur_word = cur_word.strip("['']")
        cur_word = cur_word.replace("'","")
        msg = str(msg + " " + cur_word)
        
    print(msg)
    
    


# code that will be run if the program is running through a terminal     
if __name__ == "__main__":
    text_file = provide_txt_terminal()
    generate_text(text_file,sys.argv[2], sys.argv[3])


