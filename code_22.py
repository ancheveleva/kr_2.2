import re
import collections
import json

def clean_punc(string):
    punc = r'[!\"#$%&\'()*+,-./:;<=>?@\[\\\]^_`{|}~]'
    clean_string1 = re.sub(punc, '', string)
    clean_string2 = re.sub(r' – ', ' ', clean_string1)
    return clean_string2
#0
def get_classes_of_block(r_block, html):
    raw_classes = re.findall(r_block, html)
    true_classes = []
    for raw_class in raw_classes:
        true_classes.extend(raw_class.split()) #забила на уникальность
    return true_classes

with open('Commits · pykili_pykili.github.io.html', encoding='utf-8') as f0:
    html = f0.read()

r_class_all = r'<.*?class="(.+?)".*?>'
#print(get_classes_of_block(r_class_all, html)) #выведет ответ на первую подзадачу

r_class_ol = r'<ol.*?class="(.+?)".*?>'
#print(get_classes_of_block(r_class_ol, html)) #выведет ответ на вторую подзадачу

r_class_ul = r'<ul.*?class="(.+?)".*?>'
#print(get_classes_of_block(r_class_ul, html)) #выведет ответ на третью подзадачу

#1
with open("pos.txt", encoding='utf-8') as f1:
    pos = f1.read().splitlines()

with open("powerpoint.txt", encoding='utf-8') as f11:
    raw_text = f11.read().splitlines()

word_list = []
for line in raw_text:
    if line != '':
        words = clean_punc(line).lower().split()
        word_list.extend(words)

nouns = []
for word in word_list:
    for line in pos:
        r_word_and_tags = r'^(.+?) -> (.+?)$'
        line_word = re.search(r_word_and_tags, line).group(1)
        tags = re.search(r_word_and_tags, line).group(2)
        if word == line_word and "NOUN" in tags:
            nouns.append({'word': word,
                          'tags': tags.split(',')})
#print(len(nouns)) #выведет число существительных

tags_with_noun = []
for word in nouns:
    tags_with_noun.extend(word['tags'])
most_fr = list(sorted(collections.Counter(tags_with_noun).items(),
                                    reverse=True, key=lambda kv_pair: kv_pair[1]))[1]
#print(most_fr) #выведет самый частотный тег у существительных

#2
with open('result.json', encoding='utf-8') as f2:
    tg = json.load(f2)

prep = [{"name":'Nikita Sapunov', 'id':'3571087'},{"name":'Oleg Serikov', 'id':'292749902'},{"name":'Anna Klezovich', 'id':'333418928'}]

name = 'Oleg Serikov'
words_prep = []
for mes in tg['messages']:
    if 'from' in mes.keys() and mes['from'] == name:
        for line in mes['text']: #Есть в text списки...
            if line is str: #И среди элементов списка не все строки, а кто-то словари...
                for line_s in line.splitlines(): #И ещё некотрые строки содержат переносы сторк...
                    words_prep.extend(clean_punc(line_s).lower().split())
mst_frq = collections.Counter(words_prep)
#print(mst_frq) #оно должно было выводить частотный список слов, но из-за всяких проблем, которые могут быть в text, тут пусто...
# Так что в итоге та же проблема, что и в прошлый раз - разбираться в json это долго, особенно, если он не тривиальный
# Ну или я глупенькая просто, потому что не успела отсмотреть ВСЕ проблемы, и запилить функцию тем более...