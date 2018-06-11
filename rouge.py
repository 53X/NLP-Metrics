from nltk.util import ngrams
from nltk.tokenize import TreebankWordTokenizer,PunktSentenceTokenizer
import numpy as np

tokenizer=TreebankWordTokenizer()
sentence_tokenizer=PunktSentenceTokenizer()


class Rouge():


    #Function for the ROUGE-N score , where N is the user-defined length of the ngram

    def rouge_n(references, candidate, n, averaging=True):

        ngram_cand = ngrams(tokenizer.tokenize(candidate), n)
        ng_cand=list(ngram_cand)
        rouge_recall = []
        for ref in references:
            count = 0
            ngram_ref = ngrams(tokenizer.tokenize(ref), n)
            ng_ref = list(ngram_ref)
            for ngr in ng_cand:
                if ngr in ng_ref:
                    count+=1
            rouge_recall.append(count/len(ng_ref))

        #averaging using Jacknifing procedure

        if(len(references)==1):
            return(np.mean(rouge_recall))
        elif((len(references) > 1) and (averaging == False)):
            return(rouge_recall)
        else:
            for i in range(len(rouge_recall)):
                average=[]
                dummy=list(rouge_recall)
                dummy.remove(dummy[i])
                average.append(max(dummy))
            return(np.mean(average))    

    

    # Code for LCS of 2 strings and it's length. 
    
    def lcs(X, Y, m, n):
        
        L = [[0 for x in range(n+1)] for x in range(m+1)]
        for i in range(m+1):
            for j in range(n+1):
                if i == 0 or j == 0:
                    L[i][j] = 0
                elif X[i-1] == Y[j-1]:
                    L[i][j] = L[i-1][j-1] + 1
                else:
                    L[i][j] = max(L[i-1][j], L[i][j-1])
        index = L[m][n]
        lcs = [""] * (index+1)
        lcs[index] = ""
        i = m
        j = n
        while i > 0 and j > 0:
            if X[i-1] == Y[j-1]:
                lcs[index-1] = X[i-1]
                i-=1
                j-=1
                index-=1

            elif L[i-1][j] > L[i][j-1]:
                i-=1
            else:
                j-=1

        s=" ".join(lcs)
        return(len(s.split()),s)




    #Function for ROUGE-L Score . This uses the concept of LCS and it is evaluated at Sentence level
    

    def rouge_l_sentence(references,candidate,beta,averaging=True):

        rouge_l_list=[]
        for ref in references:
            arg1=tokenizer.tokenize(ref)
            arg2=tokenizer.tokenize(candidate)
            r_lcs=Rouge.lcs(arg1, arg2, len(arg1), len(arg2))[0]/len(arg1)
            p_lcs=Rouge.lcs(arg1, arg2, len(arg1), len(arg2))[0]/len(arg2)
            score=((1+beta**2)*r_lcs*p_lcs)/(r_lcs+(beta**2)*p_lcs)
            rouge_l_list.append(score)
        
        #averaging using the Jacknifing procedure

        if len(references)==1:
            return(np.mean(rouge_l_list))
        elif (len(references)>1) and (averaging==False):
            return(rouge_l_list)
        else:
            for i in range(len(rouge_l_list)):
                average=[]
                dummy=list(rouge_l_list)
                dummy.remove(dummy[i])
                average.append(max(dummy))
            return(np.mean(average))    

    
    # Summary level ROUGE-L score

    def rouge_l_summary(references,candidate,beta,averaging=True):

        rouge_l_list=[]
        cand_sent_list=sentence_tokenizer.tokenize(candidate)
        print('cand_sent_list:',cand_sent_list)
        for ref in references:
            ref_sent_list=sentence_tokenizer.tokenize(ref)
            print('ref_sent_list:',ref_sent_list)
            sum_value=0
            for ref_sent in ref_sent_list:
                l=[]
                arg1=tokenizer.tokenize(ref_sent)
                print('arg1:',arg1)
                for cand_sent in cand_sent_list:
                    arg2=tokenizer.tokenize(cand_sent)
                    print('arg2:',arg2)
                    d=tokenizer.tokenize(Rouge.lcs(arg1,arg2,len(arg1),len(arg2))[1])
                    print("d:",d)
                    l+=d
                sum_value=sum_value+len(np.unique(l))
                print('sum_value:',sum_value)
            
            r_lcs=sum_value/len(tokenizer.tokenize(ref))
            print('r_lcs:',r_lcs)
            p_lcs=sum_value/len(tokenizer.tokenize(candidate))
            print('p_lcs:',p_lcs)
            score=((1+beta**2)*r_lcs*p_lcs)/(r_lcs+(beta**2)*p_lcs)
            rouge_l_list.append(score)
            
            if len(references)==1:
                return(np.mean(rouge_l_list))
            elif (len(references)>1) and (averaging==False):
                return(rouge_l_list)
            else:
                for i in range(len(rouge_l_list)):
                    average=[]
                    dummy=list(rouge_l_list)
                    dummy.remove(dummy[i])
                    average.append(max(dummy))
                return(np.mean(average))



print(Rouge.rouge_l_summary(['police killed the gunman'], 'police kill the gunman', 1,averaging=True))




        


            




















