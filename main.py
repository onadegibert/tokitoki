# http://tokipona.alinome.net/dic_tp_raices.es.html
import random 

def append_to_pos(key, pos, word, list):
    if key == pos:
        list.append(word)
    return list

#TODO preprocess sentence to get pos
#TODO beautify
def get_possible_syntax():
    pro_vi = ['n','vi']
    pro_vt = ['n','vt', 'e', 'n']
    pro_vt_adj = ['n','vt', 'e', 'n', 'adj']
    pro_vt_art = ['n','vt', 'e', 'n', 'poss']
    n_vi = ['n','li','vi']
    n_adj_vi = ['n','adj','li','vi']
    n_art_vi = ['n','poss','li','vi']
    n_vt = ['n','li','vt','e', 'n'] 
    n_vt_adj = ['n','li','vt','e', 'n', 'adj'] 
    n_vt_art = ['n','li','vt', 'e', 'n', 'poss']
    possible_syntax = [pro_vi, pro_vt, pro_vt_adj, pro_vt_art, n_vi, n_adj_vi, n_art_vi, n_vt, n_vt_adj,n_vt_art]
    return possible_syntax

def get_sentence_syntax():
    possible_syntax = get_possible_syntax()
    sentence_syntax = random.choice(possible_syntax)
    return sentence_syntax

def load_dict():
    dict_list = open('dict.txt','r').read().splitlines()
    words = list()
    processed_dict = dict()
    nouns = list()
    adjs = list()
    vts = list()
    vis = list()
    poss = ['mi', 'sina', 'jan', 'ona']
    for entry in dict_list:
        word = entry.split(' --> ')[0]
        words.append(word)
        meanings = entry.split(' --> ')[1].split('[')[1:]
        meanings_dict = dict()
        for each_entry in meanings:
            meanings_dict[each_entry.split(']')[0]] = each_entry.split(']')[1]
        processed_dict[word] = meanings_dict
        for key in meanings_dict.keys():
            nouns = append_to_pos(key, 'n', word, nouns)
            if word not in ['sina','mi']:
                adjs = append_to_pos(key, 'm', word, adjs)
            vts = append_to_pos(key, 'vt', word, vts)
            vis = append_to_pos(key, 'vi', word, vis)
    return words, processed_dict, nouns, adjs, vts, vis, poss

def get_sentence(sentence_syntax, nouns, vis, vts, adjs, poss):
    sentence = list()
    for pos in sentence_syntax:
        if pos == 'n':
            sentence.append(random.choice(nouns))
        if pos == 'vt':
            sentence.append(random.choice(vts))
        if pos == 'vi':
            sentence.append(random.choice(vis))
        if pos == 'adj':
            sentence.append(random.choice(adjs))
        if pos == 'poss':
            sentence.append(random.choice(poss))
        if pos == 'li':
            sentence.append('li')
        if pos == 'e':
            sentence.append('e')
    sentence_str = ' '.join(sentence)
    return sentence_str, sentence_syntax

def adj_or_poss(words, index, pos):
    if words[index] in ['mi', 'sina', 'jan', 'ona']:
        pos.extend(['poss'])
    else:
        pos.extend(['adj'])
    return pos

def guess_possible_syntax(sentence, meanings_dict):
    possible_syntax = get_possible_syntax()
    words = sentence.split()
    n_words = len(words)
    possible_sentence_syntax = [syn for syn in possible_syntax if len(syn) == n_words]
    if len(possible_sentence_syntax) == 1:
        pos = possible_sentence_syntax[0]
    else: #if there are cases where more than one syntax is possible
        pos = ['n']
        if words[1] == 'li':
            pos.extend(['li','vt','e','n'])
            if len(words) == 6:
                pos = adj_or_poss(words,5,pos)
        elif 'vt' in meanings_dict[words[1]].keys():
            pos.extend(['vt','e','n'])
            if len(words) == 5:
                pos = adj_or_poss(words,3,pos)
        else:
            pos = adj_or_poss(words,1,pos)
            pos.extend(['li','vi'])
    return pos

def analyse_sentence(sentence, meanings_dict, pos):
    words_meanings = list()
    if pos == '':
        pos = guess_possible_syntax(sentence, meanings_dict)
    word_index = 0
    for word in sentence.split():
        if word in meanings_dict.keys() and word not in ['li','e']:
            word_pos = pos[word_index]
            if word_pos in ['adj', 'poss']:
                word_pos = 'm'
            sense = meanings_dict[word][word_pos]
            words_meanings.append('\t'.join([word,word_pos, sense]))
        word_index += 1
    return(sentence, words_meanings)

if __name__ == "__main__":
    mode = input("Vols crear una frase (1) o interpretar una (2)?\n")
    words, meanings_dict, nouns, adjs, vts, vis, poss = load_dict()
    if mode == '1':
        sentence_syntax = get_sentence_syntax()
        sentence, pos = get_sentence(sentence_syntax, nouns, vis, vts, adjs, poss)
    if mode == '2':
        sentence = input("Escriu la teva frase:\n")
        pos = ''
    sentence, words_meanings = analyse_sentence(sentence, meanings_dict, pos)
    print(sentence)
    for word_sense in words_meanings:
        print(word_sense)