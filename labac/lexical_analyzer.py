import re

class LexicalAnalyzer:

	def __init__(self,path):
		self.path = path
		self.token = []

	def tokenize(self):
		#replace // with gap
		#replace / with child and [num] with index num
		path = self.path
		path = re.sub("//"," gap ",path)
		path = re.sub("/"," child ",path)
		path = re.sub(r'\[([0-9]+)\]',r' index \1 ',path)
		#remove empty string ('') from the token lists.
		return [i for i in path.split(" ") if len(i)>0]

	def token_pair(self):
		#put tokens in pair. input: [child, a, child,b], output: [(child,a),(child,b)]
		tokens = self.tokenize()
		tp=[]
		for index in range(0,len(tokens),2):
			t = (tokens[index],tokens[index+1])
			tp.append(t)
		return tp	