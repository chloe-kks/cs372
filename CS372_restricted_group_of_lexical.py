import re
from word2number import w2n
from nltk.corpus import wordnet
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))
adj_word = []

for i in wordnet.all_synsets():
    if i.pos() in ['a', 's']:
        adj_word.append(i.lemmas()[0].name())

restrict_list = [
        "absolutely",
        "amazingly",
        "awfully",
        "completely",
        "considerably",
        "decidedly",
        "deeply",
        "effing",
        "enormously",
        "entirely",
        "especially",
        "exceptionally",
        "extremely",
        "fabulously",
        "flipping",
        "flippin",
        "fricking",
        "frickin",
        "frigging",
        "friggin",
        "fully",
        "fucking",
        "greatly",
        "hella",
        "highly",
        "hugely",
        "incredibly",
        "intensely",
        "majorly",
        "more",
        "most",
        "particularly",
        "purely",
        "quite",
        "really",
        "remarkably",
        "substantially",
        "thoroughly",
        "totally",
        "tremendously",
        "unbelievably",
        "unusually",
        "utterly",
        "very",
        "almost",
        "barely",
        "hardly",
        "just enough",
        "kind of",
        "kinda",
        "kindof",
        "kind-of",
        "less",
        "little",
        "marginally",
        "occasionally",
        "partly",
        "scarcely",
        "slightly",
        "somewhat",
        "lacking"]


# start preprocessing
pre_list = []

for l in adj_word:
    for s in wordnet.synsets(l):
        for lm in s.lemmas():
            temp = lm.name()
            if '-' in temp and len(temp.split('-')) == 2 and '_' not in temp:
                pre_list.append(temp)

# 1. remove duplicated expressions             
pre_list1 = list(set(pre_list))

# 2. remove number expressions(include one, two, three...)
pre_list2 = []
pre_list3 = []

for word in pre_list1:
    check_list = word.split('-')
    try:
        w2n.word_to_num(check_list[0])
    except ValueError:
        pre_list2.append(word)

for word in pre_list2:
    check_list = word.split('-')
    try:
        w2n.word_to_num(check_list[1])
    except ValueError:
        pre_list3.append(word)

# 3. remove stopwords

for word in pre_list3:
    check_list = word.split('-')
    if check_list[0] in stop_words or check_list[1] in stop_words:
        #print(check_list)
        pre_list3.remove(word)

        
# 4. extract that has higher accuracy synset(first & second word should be included in the synset name)
pre_list4 = []

for word in pre_list3:
    syn = wordnet.synsets(word)
    temp1 = word.split('-')[0]
    temp2 = word.split('-')[1]
    for s in syn:
        if temp1 in s.name() and temp2 in s.name():
            pre_list4.append(word)
            break

# 5. divide according to standards(the standards are written at the end of the code and the report)
ranking_dict = {0: [], 1: [], 2:[]}
            
for word in pre_list4:
    res_flag = False
    syn = wordnet.synsets(word)
    temp1 = word.split('-')[0]
    temp2 = word.split('-')[1]
    for s in syn:
        if temp1 in s.name() and temp2 in s.name():
            def_temp = s.definition()
            break
            
    if '(' in def_temp:
        def_temp = re.sub(r'\([^)]*\)', '', def_temp)

    for res_word in restrict_list:
        if res_word in def_temp:
            #print(res_word)
            res_flag = True
            break

    if res_flag:
        ranking_dict[0].append(word)
    else:
        if temp2 in def_temp:
            ranking_dict[1].append(word)
        else:
            ranking_dict[2].append(word)

# 6. count uniqueness and make ranking
rank = []
for l in ranking_dict.values():
    count_dict = {}
    fin_dict = {}
    for w in l:
        key = w.split('-')[0]
        if key in count_dict:
            count_dict[key] += 1
        else:
            count_dict[key] = 1  
    
    for w in l:
        key = w.split('-')[0]
        order_key = count_dict[key]
        if order_key in fin_dict:
            fin_dict[order_key].append(w)
        else:
            fin_dict[order_key] = [w]
    
    for a in fin_dict.values():
        rank += a

# save the result[:100] in csv file.
count = 0
f = open('CS372_HW2_output_20150076.csv', 'w')
for i in range (0, len(rank)):
    if(count == 100): break
    print(rank[i])
    temp = rank[i]+"\n"
    f.write(temp)
    count+=1
    
f.close()

"""
ranking dictionary
0: Does the expression's definition include restrictive words?
1: Does the expression's definition include the second word without restrictive words?
2: etc...

counting uniqueness
1. The count dictionary stores how many times the first word occurs from the each ranking dictionary.
2. It stores to the rank list in the order of less frequency(=higher uniqueness).
""" 
