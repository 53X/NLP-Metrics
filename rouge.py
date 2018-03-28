#This is an implementation of the ROUGE score introduced in a paper by Lin et. al(2004)

#ROUGE - Recall -Oriented Understudy for Gisting Evaluation


#Library dependencies

from nltk import ngrams
from nltk.tokenize import word_tokenize



#Function for the ROUGE-N score , where N is the user-defined length of the ngram

def rouge_n(candidate,references,n,averaging=True):

	ngram_candidate=ngrams(word_tokenize(candidate),n)
	total_ngrams_matched=[]
	total_ngrams_summary=[]
	rouge_recall=[]
		
	for ref in references:
		count=0
		ngram_reference=ngrams(word_tokenize(ref),n)
		total_ngrams_summary.append(ngram_reference)
		for n in ngram_candidate:
			if n in ngram_reference:
				count+=1
		total_ngrams_matched.append(count)

	if(len(references)==1):
		averaging=False
		
		
	if(averaging==True):
		for i in range(len(total_ngrams_summary)):
			rouge_recall.append((np.sum(total_ngrams_matched)-total_ngrams_matched[i])/(np.sum(total_ngrams_summary)-total_ngrams_summary[i]))
	else:
		rouge_recall.append(np.sum(total_ngrams_matched)/np.sum(total_ngrams_summary))
		

 	return np.mean(rouge_recall)












