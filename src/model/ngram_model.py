import os
from dotenv import load_dotenv
import json
load_dotenv("config/.env")
class NGramModel:
    """ this class is responsible for creating and saving the model including 
    counts of words and probabilites across the mutliple ngram windows and context frames"""
    def __init__(self):
        """ initalizes all empty data stuctures used by the class as well as 
        retreiving the ngram order and threshold from config.csv"""
        self.vocab=[]
        self.vocab_counts={}
        self.model={}
        self.ngram_order=int(os.getenv("NGRAM_ORDER"))
        self.unk_threshold=int(os.getenv("UNK_THRESHOLD"))

    def build_vocab(self,token_file_path):
        """splits the token file into a list of sentences then a list of words and loops over them counting the 
        individual words then replaces words that do not meet the threshold with <UNK> token and stores its count as 
        well and updates the unique and non unique variables in self with the vocab and vocab counts """
        vocab_counts={}
        token_file=open(token_file_path)
        content=token_file.read()
        lines=content.split('\n')
        for line in lines:
            if line == '':
                 continue
            words=[w for w in line.split(' ') if w != '']
            for word in words:
                if word in vocab_counts:
                    vocab_counts[word]+=1
                else:
                    vocab_counts[word]=1
        for word in list(vocab_counts):
            if vocab_counts[word]>=self.unk_threshold:
                self.vocab.append(word)
            else:
                if '<UNK>' not in vocab_counts:
                    vocab_counts['<UNK>']=1
                else:
                    vocab_counts['<UNK>']+=1
                if '<UNK>' not in self.vocab:
                    self.vocab.append('<UNK>')
        for key, count in vocab_counts.items():
            if key in self.vocab:
                self.vocab_counts[key]=count
        token_file.close()
        
    
    def build_count_and_prob(self,token_file_path):
        """counts the instances of words and context for different n-gram orders from 1 upto the
          limit and calculates probabilites for the words and context windows based on the n-gram 
          orders and saves to the self.model dictionary to be copied to the model.json file later on"""
        token_file=open(token_file_path)
        content= token_file.read()
        lines=content.split('\n')
        counts={}
        for order in range(1,self.ngram_order +1):
            key = str(order) + "gram"
            counts[key] = {}

            for line in lines:
                if line == '':
                    continue
                words = [w for w in line.split(' ') if w != '']
                for i in range (len(words)):
                    if words[i] not in self.vocab:
                        words[i]='<UNK>'
                    
                for i in range(len(words) - order + 1):
                    ngram = words[i:i+order]
                    if order==1:
                        context=ngram[0]
                        if context not in counts[key]:
                            counts[key][context]=1
                        else:
                            counts[key][context]+=1
                    else:
                        context=' '.join(ngram[:-1])
                        target=ngram[-1]
                        if context not in counts[key]:
                            counts[key][context]={}
                        if target not in counts[key][context]:
                            counts[key][context][target]=1
                        else:
                            counts[key][context][target]+=1

        for key in counts:
            self.model[key]={}
            for context in counts[key]:
                if key =='1gram':
                    self.model[key][context]= counts[key][context]/sum(counts[key].values())
                else:
                    self.model[key][context]={}
                    for target in counts[key][context]:
                        self.model[key][context][target]=counts[key][context][target]/sum(counts[key][context].values())
        token_file.close()



    def lookup(self,context):
        """searches for a specific context / word and returns a dictionary of the most likely 
        word to follow the input as well as a probaility of occurance using a backoff technuique 
        starting with ngram order max and going down to 1 , if nothing is found it returns and empty dict"""
        for order in range(self.ngram_order,0,-1):
            key=str(order)+'gram'
            if order==1:
                return self.model[key]
            ctx=' '.join(context[-(order-1):])
            if ctx in self.model[key]:
                return self.model[key][ctx]
        return {}

    def save_model(self,model_path):
        """save model to json file"""
        p=open(model_path, 'w')
        json.dump(self.model,p)
        p.close()

    def save_vocab(self,vocab_path):
        """save vocab to json file"""
        p=open(vocab_path, 'w')
        json.dump(self.vocab,p)
        p.close()

    def load(self,model_path,vocab_path):
        """loads specific model and vocab to the object data structure """
        model_file=open(model_path,'r')
        vocab_file=open(vocab_path,'r')
        self.model=json.load(model_file)
        self.vocab=json.load(vocab_file)
        model_file.close()
        vocab_file.close()