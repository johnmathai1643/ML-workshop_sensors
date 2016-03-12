import json
import string
import os
from collections import Counter

dict_ham = []
dict_spam = []
#remove_words = ['on','it','am', 'an', 'as', 'at', 'the', 'you', 'her', 'this', 'that', 'these', 'those', 'my', 'your', 'his', 'its', 'our', 'their', 'we', 'them', 'me', 'a', 'no', 'yes', 'will', 'can', 'may', 'I', 'not', 'is', 'under', 'over', 'in', 'The', 'A', 'want', 'No', 'Yes', 'i', 'bottom', 'We', 'us', 'who' , 'whose', 'then', 'mine', 'ours', 'of', 'or', 'be', 'nor', 'As', 'Now', 'now', 'what', 'why', 'when', 'which', 'U', 'How','how','had','have','has','You', 'well', 'Have', 'lose', 'shes', 'home', 'Ur', 'UP', 'hi', 'eat', 'he', 'else','sorry', 'look', 'even', 'new', 'ever', 'never', 'Also', 'call', 'type', 'tell', 'room', 'give', 'All', 'before', 'better', 'went', 'mean', 'forgot', 'open', 'little', 'stop', 'bad', 'decided', 'said', 'cant', 'im', 'id', 'if', 'make', 'youre', 'left', 'just', 'yet','Why', 'so','all','to','On','It','Am', 'An', 'As', 'At', 'The', 'You', 'Her', 'This', 'That', 'These', 'Those', 'My', 'Your', 'His', 'Its', 'Our', 'Their', 'we', 'them', 'me', 'a', 'no', 'yes', 'will', 'can', 'may', 'I', 'not', 'is', 'under', 'over', 'in', 'The', 'A', 'Want', 'No', 'Yes', 'Bottom', 'We', 'us', 'who' , 'whose', 'then', 'mine', 'ours', 'of', 'Or', 'Be', 'nor', 'As', 'Now', 'now', 'What', 'Why', 'When', 'Which', 'U', 'How','how','had','have','has','You', 'well', 'Have', 'lose', 'Shes', 'Home', 'ur', 'up', 'Hi', 'Eat', 'He', 'Else', 'Look', 'Even', 'New', 'Ever', 'Never', 'Also', 'Call', 'Type', 'Tell', 'Room', 'Give', 'All', 'Before', 'Better', 'Went', 'Mean', 'Forgot', 'open', 'little', 'Stop', 'Bad', 'Decided', 'Said', 'Cant', 'Im', 'Id', 'If', 'Make', 'Youre', 'Left', 'Just', 'Yet','Why', 'So','All','To', 'from', 'go', 'also', 'Also', 'and', 'get']

remove_words = ['on','it','am', 'an', 'as', 'at', 'the', 'you', 'her', 'this', 'that', 'these', 'those', 'my', 'your', 'his', 'its', 'our', 'their', 'we', 'them', 'me', 'a', 'no', 'yes', 'will', 'can', 'may', 'I', 'not', 'is', 'under', 'over', 'in', 'The', 'A', 'want', 'No', 'Yes', 'i', 'bottom', 'We', 'us', 'who' , 'whose', 'then', 'mine', 'ours', 'of', 'or', 'be', 'nor', 'As', 'Now', 'now', 'what', 'why', 'when', 'which', 'U', 'How','how','had','have','has','You', 'well', 'Have', 'lose', 'shes', 'home', 'Ur', 'UP', 'hi', 'eat', 'he', 'else','sorry', 'look', 'even', 'new', 'ever', 'never', 'Also', 'call', 'type', 'tell', 'room', 'give','and','get']


if os.path.exists('important_ham_words.json') or os.path.exists('important_spam_words.json') or os.path.exists('important_words.json'): 
	os.remove('important_ham_words.json')
	os.remove('important_spam_words.json')
	os.remove('important_words.json')

def remove_punctuation(text):
    return text.translate(None, string.punctuation)

with open('email_ham_messages_1953','r') as f:
    for line in f:
        line = remove_punctuation(line)
        for word in line.split():
           dict_ham.append(word)

with open('email_spam_messages_1953','r') as f:
    for line in f:
        line = remove_punctuation(line)
        for word in line.split():
           dict_spam.append(word)

def unique_words(seq):
   keys = {}
   for e in seq:
       keys[e] = 1
   return keys.keys()

def int_filter( someList ):
    for v in someList:
        try:
            int(v)
            continue # Skip these
        except ValueError:
            yield v # Keep these

#dict_ham = unique_words(dict_ham)
#dict_spam = unique_words(dict_spam)

#print Counter(dict_ham)
#print Counter(dict_spam)

dict_ham = [item for item in dict_ham if item not in remove_words]
dict_spam = [item for item in dict_spam if item not in remove_words]

dict_ham = list( int_filter( dict_ham ))
dict_spam = list( int_filter( dict_spam ))

dict_ham = [i for i in dict_ham if len(i) > 1]
dict_spam = [i for i in dict_spam if len(i) > 1]

dict_ham_count = Counter(dict_ham)
dict_spam_count = Counter(dict_spam)


dict_spam_filter = []
dict_ham_filter = []
dict_filter = []

for key,val in dict_ham_count.items():
    if val >= 4:
    	dict_ham_filter.append(key)

for key,val in dict_spam_count.items():
    if val >= 4:
    	dict_spam_filter.append(key)

dict_ham_filter = unique_words(dict_ham_filter)
dict_spam_filter = unique_words(dict_spam_filter)

json_ham_string = json.dumps(dict_ham_filter)
json_spam_string = json.dumps(dict_spam_filter)

dict_filter = list(set(dict_ham_filter).union(dict_spam_filter))
json_string = json.dumps(dict_filter)

with open('important_ham_words.json', 'w') as f:
      f.write(json_ham_string.decode('unicode_escape').encode('ascii','ignore'))
      f.close()

with open('important_spam_words.json', 'w') as f:
      f.write(json_spam_string.decode('unicode_escape').encode('ascii','ignore'))
      f.close()

with open('important_words.json', 'w') as f:
      f.write(json_string.decode('unicode_escape').encode('ascii','ignore'))
      f.close()
