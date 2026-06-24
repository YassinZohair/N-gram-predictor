import os
from dotenv import load_dotenv
load_dotenv("config/.env")
class Predictor :

    def __init__(self,model, normalizer):
        self.model=model
        self.normalizer=normalizer
        self.ngram_order=int(os.getenv('NGRAM_ORDER'))


    def normalize(self,text):
        clean_text=self.normalizer.normalize(text)
        text_list=clean_text.split(' ')
        context=text_list[-(self.ngram_order-1):]
        return context
    def map_oov(self,context):
        vocab=self.model.vocab
        for i in range(len(context)):
            if context[i] not in vocab:
                context[i]='<UNK>'
        return context


    def predict_next(self, text,k):
        context=self.normalize(text)
        context=self.map_oov(context)
        predictions=self.model.lookup(context)
        sorted_predictions=sorted(predictions,key=lambda w:predictions[w],reverse=True)
        return sorted_predictions[:k]
    
