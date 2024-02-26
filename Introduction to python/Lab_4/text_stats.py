#!/usr/bin/env python3


#__Student I:__ johed883 (Johannes Hedström)

#__Student II:__ mikmo937 (Mikael Montén)


# importing sys , os and counter 
import sys
import os
from collections import Counter
from contextlib import redirect_stdout
import string as stri


"""

A word does not contain any special characters as a default, names and numbers
will be counted as words as they will be counted in the office package.


[1]

We make use of .lower() when we import the text to not differentiate words
between lower and upper case letters. Then we used maketrans with punctuation()
from string module to be able to translate punctuations to nothing ("").
Along with replacing weird citation marks with nothing. This was to normalize
the words to only alphanumerical characters.


[2]

We are using dictionaries with lists or tuples as its easy to use the words 
as keys to then fill the list/tuple with several following words or with values.

We also used set to remove duplicates when looking for unique words. 



"""

# load txt file if its used as a module, we added an argument to remove punctations


def read_txt(path,punctations=False):

    try:
        with open(path, 'r', encoding='utf-8') as file:
        
            text = file.read().lower() # all words to lower and saving the text
            if punctations==False:
                translator = str.maketrans('','',stri.punctuation)
                text = text.translate(translator) # removing punctations
                text = text.replace('”','')
                text = text.replace('“','')
            return text
    except FileNotFoundError: # error if the file isnt found
        print('The  file isnt found:',path)
    
    except Exception as e: # if an error occur while reading the file
        print('An error occurred while reading the file:', e)
    
    




# terminal 
def provide_txt_terminal():
   
        # running try to see if the file exists and is of the correct sort
    try:
        with open(sys.argv[1], 'r',encoding='utf-8')  as file:# opening the file
            text = file.read().lower() # saving the conent in text and to lower
            translator = str.maketrans('','',stri.punctuation)
            text = text.translate(translator) # removing punctations
            text = text.replace('”','')    
            text = text.replace('“','')
            return text
            
    except Exception as e:
           print('An error occurred while reading the file:', e)
           sys.exit(0)              




 
 
def freq_letters(string):
    # picking out letters in the string
    string = [element for element in string if element.isalpha()]
    # empty dicionary
    counts = {}
    
    for idx in string: # counting the letters
        counts[idx] = counts.get(idx,0) + 1
        
    # sorting them in decreasing order
    counts = sorted(counts.items(), key = lambda x:x[1], reverse = True)
    
    # creating the prints
    print("\nEach letter occurs the following amount of times: \n")
    print( "Letter \t", "Frequency")
    print("-" * 22)
    for letter, count in counts: # looping over letter and number of times
        print(letter,'\t',count)
    print("-" * 22, "\n")
    
    return counts
    
    
    
def count_words(string):
    # counting number of words
    split_words = len(string.split())
    
    # printing results
    print("The text contains", split_words, "different words \n")

 
def count_unique_words(string):
    
    unique_split_words = set(string.split()) # picking out unique words
    count_words = len(unique_split_words) # counting numer of unique words
    
    # printing results
    print("The text contains", count_words, "different unique words \n")
 


 
def common_words(string):
    split_string = string.split() # splitting the string
    count = Counter(split_string) # create counter object
    most_frequent = count.most_common(5) # picking out the most common words
    # creating printout
    print("The five most common words are: \n")
    print( "Word \t \t", "Frequency")
    print("-" * 22)
    for word, count in most_frequent:
        print(f'{word:<20}{count}')
    return most_frequent # returning the most common words to use later
 
 
def following_word(string, common_word):
    following_word = {} # empty dictionary to fill with neigbours for each common word
    if len(common_word[0]) > 1 :
        frequent_combinations = [word[0] for word in common_word] # picking out the words from the lsit
        for word in frequent_combinations:
            following_word[word] = [] # Each word is a key in the dictionary
    else:
        frequent_combinations = [common_word]
        following_word[common_word] = []

    split_string = string.split() # splitting the string to a list
    
    
    # looping over each word and when its a common word we save the following word
    for index, word in enumerate(split_string): 
        if word in frequent_combinations and index < (len(split_string)-1):
            following_word[word].append(split_string[index+1])

    # Counting the following words for each common word 
    for key, next_word in following_word.items():
        following_count = Counter(next_word)
        most_frequent = following_count.most_common()
        most_frequent3 = following_count.most_common(3)
        # Creating prints
        if len(common_word[0]) > 1:
            print(f'\nThe word "{key}" occurs {common_word[frequent_combinations.index(key)][1]} times, and is followed most commonly by the following:')
 
            print("-" * 22)
            for word, count in most_frequent3:
                print(f'{word:<20}{count}')
            print("-" * 22)
    return most_frequent
            
        
# function to write in a txt file if its used as a module
def write_txt(text_file, new_file):
    # checking that the new file exists
    
    if not os.path.exists(new_file): 
        print('The file does not exist!:',new_file)
        sys.exit(0) # exiting the program
    
    # Writing our results in the file
    with open(new_file,'w') as f:
        with redirect_stdout(f): # running our functions
            freq_letters(text_file)
            count_words(text_file)
            count_unique_words(text_file)
            common = common_words(text_file)
            following_word(text_file, common)





 # code that will be run if the program is running through a terminal     
if __name__ == "__main__":
    # saving the output in the file
    # Trying to see if there is a txt file or not in the command
    if len(sys.argv) > 2:
        # Cheking if the second file exists before reading the first 
        if not os.path.exists(sys.argv[2]):
            print('This function requires an output file which does not exist. Create one!:',sys.argv[2] )
            sys.exit(0) # exiting the program

         
        if not os.path.exists(sys.argv[1]):
            print('The input text file does not exist:',sys.argv[1] )
            sys.exit(0) # exiting the program
            
    
        with open(sys.argv[2],'w') as f:
             with redirect_stdout(f): # running our functions
                 text_file = provide_txt_terminal()
                 freq_letters(text_file)
                 count_words(text_file)
                 count_unique_words(text_file)
                 common = common_words(text_file)
                 following_word(text_file, common)
                 
    elif len(sys.argv) == 1: # if only the 
        print('File_Error: You need to provide a txt file to be read and one to be written')
        sys.exit(0) # exiting the program
        
    else:
        print('File_Error: You need to provide a txt file to be written on')
        sys.exit(0) # exiting the program


