import numpy
import unicodedata
import wolframalpha
from nltk.tag.stanford import CoreNLPNERTagger
from google import google
import wikipedia
import collections


# stanford_dir = 'stanford-ner-2018-02-27/'
# jarfile = stanford_dir + 'stanford-ner.jar'
# modelfile = stanford_dir + 'classifiers/english.muc.7class.distsim.crf.ser.gz'
#tagger = StanfordNERTagger(modelfile, jarfile)

tagger =  CoreNLPNERTagger(url='http://localhost:9000')



def classify_question(question):
    print '--QUESTION--: ',question

    ques_tag = tagger.tag(tagger.tokenize(question))
    ques_tag = get_ne_chunk_tag(ques_tag)
    
    q = question.lower().split()
    if q[0] == 'where':
        city = False
        for tag in ques_tag:
            if tag[1] == 'CITY':
                city = True
        if city:
            return 'COUNTRY'

        return 'LOCATION'

    elif 'year' in q or 'when' in q:
            return 'DATE'

    elif 'country' in q:
        return 'COUNTRY'

    elif q[0] in ['who', 'whose', 'whom']:
        # for question who is...
        if (q[1] in ['is', 'are']):
            # wiki will handle
            return 'DEFINITION'
        return 'PERSON'

    elif q[0] == 'what':
        return 'DEFINITION'

    elif q[0] == 'how':
        if q[1] in ['few', 'little', 'much', 'many', 'hot']:
            return 'NUMBER'
        elif q[1] in ['young', 'long', 'old']:
            return 'TIME'
            # return 'DURATION'

    elif q[0] == 'which':
        # TODO
        return 'None'
    else:
        return 'None'

def google_search(question):
    print 'google search'
    first_page = google.search(question,1, lang ='en')
    #print first_page
    top_three_result = []
    i = 0
    while i<5:
        if ('vi' in first_page[i].link):
            # skip vietnamese pages
            pass
        else:
            top_three_result.append(first_page[i].description)
        i+=1

    first_search = '\n'.join(top_three_result).encode('ascii','replace')
    print first_search

    ret = tagger.tag(tagger.tokenize(first_search))
    ret = get_ne_chunk_tag(ret)
    print ret
   
    question_type = classify_question(question)
    print '--QUESTION TYPE--: ',question_type
    if question_type == 'None':
        ans = "Oops! I don't know (Question Type Exception)."
    else:
        google_answer = []
        ret_len = len(ret)
        question_type = [question_type]

        # TODO:ADD SUPPORT FOR DIFFERENT TYPE HERE
        if 'LOCATION' in question_type:
            question_type.append('STATE_OR_PROVINCE')


        for i in range(ret_len):
            if ret[i][1] in question_type:
                if ret[i][0] not in google_answer:
                    google_answer.append(ret[i][0])

        # print '--Google--: ',google_answer
        if not google_answer:
            ans = "I don't know! "
        else:
            candidate_answer = []

            for i in range(len(google_answer)):
                if (google_answer[i] in ['currently', 'current']):
                    pass
                else:
                    candidate_answer.append('Candidate Answer: '+ google_answer[i])
            candidate_answer = '\n'.join(candidate_answer)
            ans = candidate_answer
            
    return ans

def wiki_search(question):
    print 'wiki search'
    l = question.split(' ')
    if len(l) > 2:
        ques = " ".join(l[2:])
    try:
        #wikipedia.set_lang("en")
        ans = (wikipedia.summary(question, sentences=1)).encode('ascii', 'ignore')

        link = wikipedia.page(ques)
        ans = ans + '\n For more information: '+link.url

    except:
        google_search(question)
    return ans

def answer_question(question):
    print 'answer'
    try:
        app_id = '4WP6Y5-A3UHEW2EY5'
        if not app_id:
            print 'Add your app id'
        #client = wolframalpha.Client(app_id)
        #res = client.query(question)
        #ans = str(next(res.results).text).replace('.', '.\n')
        ans = 'None'

        if ans == 'None':
            q_type = classify_question(question)
            if q_type == 'DEFINITION':# or q_type == 'LOCATION':
                print '--QUESTION TYPE--: ', q_type
                ans = wiki_search(question)
            else:
                ans = google_search(question)
        print '--ANSWER--: '
        return ans

    except:
        return "EXCEPTION: I don't know. Try something else"


# https://stackoverflow.com/a/30666949
def get_continuous_chunks(tagged_sent):
    continuous_chunk = []
    current_chunk = []

    for token, tag in tagged_sent:
        if tag != "O":
            current_chunk.append((token, tag))
        else:
            if current_chunk: # if the current chunk is not empty
                continuous_chunk.append(current_chunk)
                current_chunk = []
    # Flush the final current_chunk into the continuous_chunk, if any.
    if current_chunk:
        continuous_chunk.append(current_chunk)
    return continuous_chunk

def get_ne_chunk_tag(ne_tagged_sent):

    named_entities = get_continuous_chunks(ne_tagged_sent)
    # print named_entities
    # [[(u'Donald', u'PERSON'), (u'Trump', u'PERSON')], [(u'1997', u'DATE')]]
    # named_entities = get_continuous_chunks(ne_tagged_sent)

    # unused
    named_entities_str = [" ".join([token for token, tag in ne]) for ne in named_entities]
    # print named_entities_str
    # [u'Donald Trump', u'1997']

    named_entities_str_tag = [(" ".join([token for token, tag in ne]), ne[0][1]) for ne in named_entities]
    # print named_entities_str_tag
    # [(u'Donald Trump', u'PERSON'), (u'1997', u'DATE')]

    return named_entities_str_tag


if __name__ == '__main__':
    queries = []
    with open('query2.txt', 'r') as file:
        count = 5
        for line in file:
            question = line.strip()
            queries.append(question)
            count -= 1
            if (count == 0):
                break

    for question in queries:
        print 
        print answer_question(question)
        print

    # question = 'Where is Stonehenge?'
    # print
    # print answer_question(question)
    # print