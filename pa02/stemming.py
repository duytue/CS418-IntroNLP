from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
import re

vowel = ['a', 'e', 'i', 'o', 'u', 'y']
consonant = ['b','c','d','f','g','h','j','k','l','m','n','p','q','r','s','t','v','w','x','z']
double = ['pp','nn','ll','ss', 'zz', 'bb','gg','mm','rr', 'tt', 'dd']

step2_old = ['ational','tional','enci','anci','izer','abli','alli','entli','eli','ousli','ization','ation','ator','alism','iveness','fulness','ousness','ality','iviti','biliti']
step2_new = ['ate','tion','ence', 'ance', 'ize', 'able' ,'al', 'ent' ,'e' ,'ous' ,'ize', 'ate', 'ate', 'al', 'ive', 'ful' ,'ous' ,'al', 'ive' ,'ble']

step3_old = ['icate', 'ative', 'alize' ,'iciti' ,'ical' ,'ful' ,'ness']
step3_new = ['ic', '', 'al' ,'ic' ,'ic', '' ,'']

step4_old = ['al', 'ance', 'ence' ,'er' ,'ic' ,'able' ,'ible', 'ant' ,'ement', 'ment', 'ent' ,'ion', 'ou' ,'ism', 'ate', 'iti', 'ous', 'ive', 'ize']
#step4_new = ['','','','','','','','','','','','ion',]

years = '(\d+)'
m_expr = '([aeiouy][^aeiouy])'
v_expr = '([aeiouy])'
cvc_expr = '([^aeiouy][aeiouy][^aeiouy])'

def contain_vowel(word):
	match = re.findall(v_expr, word)
	if len(match) > 0:
		return True
	return False

def end_double(word):
	for i in double:
		if word.endswith(i):
			return True
	return False

def shortword(word):
	match = re.findall(cvc_expr, word)
	for i in match:
		if word.endswith(i):
			if word[len(word)-1] in ['w', 'x', 'y']:
				return True
	return False

def step1b_helper(ret):
	if ret.endswith('at') or ret.endswith('bl') or ret.endswith('iz'):
		ret = ret + 'e'
	elif end_double(ret):
		if ret.endswith('l') or ret.endswith('s') or ret.endswith('z'):
			return ret
		else:
			ret = ret[:-1]
	else:
		match = re.findall(m_expr, ret)
		if len(match)==1 and shortword(ret):
			ret = ret + 'e'
	return ret


#0.68
def step0(word):
	if word.endswith("'"):
		return word[:-1]
	elif word.endswith("'s"):
		return word[:-2]
	elif word.endswith("'s'"):
		return word[:-3]
	else:
		return word

#0.73
def step1a(word):
	if word.endswith('sses'):
		return word[:-2]
	elif word.endswith('ied') or word.endswith('ies'):
		if len(word) > 4:
			return word[:-2]
		else:
			return word[:-1]
	elif word.endswith('us') or word.endswith('ss'):
		return word
	elif word.endswith('s'):
		precede = word[:-1]
		match = re.findall(years, precede)
		if len(match) == 1:
			return precede
		if precede[-1] in consonant:
			precede = precede[:-1]
			for i in range(0, len(precede)):
				if precede[i] in vowel:
					return word[:-1]
		return word
	else:
		return word

#0.77
def step1b(word):
	ret = word
	delete = False
	if word.endswith('eed'):
		match = re.findall(m_expr, word[:-3])
		if len(match) > 0:
			return word[:-1]
	elif word.endswith('ed'):
		precede = word[:-2]
		if contain_vowel(precede):
			ret = word[:-2]
			delete = True
	elif word.endswith('edly') or word.endswith('ing'):
		precede = word[:-3]
		if contain_vowel(precede):
			ret = word[:-3]
			delete = True
	elif word.endswith('ingly'):
		precede = word[:-4]
		if contain_vowel(precede):
			ret = word[:-4]
			delete = True
	
	
	if delete:
		ret = step1b_helper(ret)

	return ret

#0.68
def step1c(word):
	# if word.endswith('y'):
	# 	precede = word[:-1]
	# 	if contain_vowel(precede):
	# 		word = precede + 'i'
	# return word
	ret = word
	if word.endswith('y'):
		precede = word[:-1]
		x = precede[len(precede)-1]
		if x in consonant:
			if x != precede[0]:
				word = precede + 'i'
	return word
			

#0.66
def step2(word):
	# match = re.findall(m_expr, word)
	# if len(match) > 0:
	# 	for i in range(0, len(step2_old)):
	# 		if word.endswith(step2_old[i]):
	# 			word = word[:-(len(step2_old[i]))]
	# 			word = word + step2_new[i]
	# return word
	for i in range(0, len(step2_old)):
		match = re.findall(m_expr, word[:-(len(step2_old[i]))])
		if len(match) > 0:
			if word.endswith(step2_old[i]):
				word = word[:-(len(step2_old[i]))]
				word = word + step2_new[i]
	if word.endswith('ogi'):
		if word[:-3].endswith('l'):
			word = word[:-3] + 'og'
	return word

#0.66
def step3(word):
	# match = re.findall(m_expr, word)
	# if len(match) > 0:
	for i in range(0, len(step3_old)):
		match = re.findall(m_expr, word[:-(len(step3_old[i]))])
		if len(match) > 0:
			if word.endswith(step3_old[i]):
				word = word[:-(len(step3_old[i]))]
				word = word + step3_new[i]
	return word

#0.73
def step4(word):
	# match = re.findall(m_expr, word)
	# if len(match) > 1:
	for i in range(0, len(step4_old)):
		match = re.findall(m_expr, word[:-(len(step4_old[i]))])
		if len(match) > 1:
			if word.endswith(step4_old[i]):
				if i != 11:
					word = word[:-(len(step4_old[i]))]
				else:
					# ION -> *S or *T
					precede = word[:-3]
					if precede.endswith('s') or precede.endswith('t'):
						word = precede
	return word

#0.64
def step5a(word):
	match = re.findall(m_expr, word[:-1])
	if (len(match) > 1):
		if word.endswith('e'):
			word = word[:-1]
			return word
	elif len(match) == 1:
		# True -> not *o
		condition = True
		match = re.findall(cvc_expr, word)
		for i in match:
			if word.endswith(i):
				# *o
				condition = False
		if not condition:
			if word.endswith('e'):
				word = word[:-1]
	return word

#0.66
def step5b(word):
	match = re.findall(m_expr, word[:-2])
	ret = word
	if (len(match) > 1):
		if end_double(word):
			if word.endswith('l'):
				word = word[:-1]
	return word

def stemming(word):
	#0.68
	stemmed_word = step0(word)
	#0.73
	stemmed_word = step1a(stemmed_word)
	#0.78
	stemmed_word = step1b(stemmed_word)
	#0.8
	stemmed_word = step1c(stemmed_word)
	#0.81
	stemmed_word = step2(stemmed_word)
	#0.81
	stemmed_word = step3(stemmed_word)
	#0.9
	stemmed_word = step4(stemmed_word)
	#0.92
	stemmed_word = step5a(stemmed_word)
	#0.92
	stemmed_word = step5b(stemmed_word)
	return stemmed_word

def main():
	lst_stem = []
	auth_lst_stem = []
	with open('test.txt', 'r') as file:
		for line in file:
			line_stem = [stemming(w.lower()) for w in line.split()]
			lst_stem.append(line_stem)
			#score
			#auth porter stemming:
			ps = PorterStemmer()
			auth_line_stem = [ps.stem(w.lower()) for w in line.split()]
			auth_lst_stem.append(auth_line_stem)
		stem_right = 0
		len_input = 0
		for i,j in enumerate(lst_stem):
			len_input+=len(j)
			for x,y in enumerate(j):
				if lst_stem[i][x] == auth_lst_stem[i][x]:
					stem_right +=1
		acc = stem_right*1.0/len_input

	print acc
	return acc

if __name__ == '__main__':
	main()