# including libraries
import nltk
from nltk.corpus import wordnet as wn

# define adjective word list, empty list, empty dictionary
word_list = ['absolutely', 'profoundly', 'incredibly', 'exceedingly', 'extremely', 'hugely', 'immensly', 'supremely']
adj_word = []
result = dict()

# search all synsets and appending adjectives
for i in wn.all_synsets():
    if i.pos() in ['a', 's']:
        adj_word.append(i)

# in all adj_word,
for w in adj_word:
    for word in word_list:
        # if extend word is included the definition,
        if word in w.definition():
            simple_word = str(w.definition()).split(' ')
            # find a main word
            j = simple_word.index(word)
            # remove ';', some word have a semicolon
            if ';' in simple_word[j+1]:
                a = simple_word[j+1].split(';')
                result[a[0]] = w.name()[:-5]
                continue
            # the word added to the key of result dictionary
            result[simple_word[j+1]] = w.name()[:-5]
            
# save the result[:50] in csv file.
count = 0
f = open('CS372_HW1_output_20150076.csv', 'w')
for key in result:
    if(count == 50): break
    val = result[key]
    print("%s, %s" % (val, key))
    temp = val+","+key+"\n"
    f.write(temp)
    count+=1
    
f.close()
