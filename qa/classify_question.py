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
        if (q[1] in ['is']):
            # wiki will handle
            return 'DEFINITION'
        return 'PERSON'

    elif q[0] == 'what':
        if q[1] in ['time']:
            if q[2] in ['did', 'is']:
                return 'TIME'
	if q[1] in ['is']:
            if q[2] in ['the']:
                if q[3] in ['name']:
                    if q[5] in ['book', 'film', 'movie', 'story']:
                        return 'TITLE'
                    elif if q[5] in ['city', 'capital']:
                        return 'CITY'

        return 'DEFINITION'

    elif q[0] == 'how':
        if q[1] in ['few', 'little', 'much', 'many']:
            return 'NUMBER'
        elif q[1] in ['young', 'long', 'old']:
            return 'TIME'
            # return 'DURATION'

    elif q[0] == 'which':
	if q[1] in ['book', 'film', 'movie', 'story']:
		return 'TITLE'
	elif q[1] in ['city']:
		return 'CITY'
	elif q[1] in ['person']:
		return 'PERSON'
        # TODO. May consider using ordinal.
        return 'None'
    else:
        return 'None'