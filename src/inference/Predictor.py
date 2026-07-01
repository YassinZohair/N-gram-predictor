import os,logging
from dotenv import load_dotenv
load_dotenv("config/.env")
class Predictor :

    def __init__(self,model, normalizer):
        self.logger = logging.getLogger(__name__)
        self.model=model
        self.normalizer=normalizer
        self.ngram_order=int(os.getenv('NGRAM_ORDER'))
        self.logger.debug(f'predictor initalized with n-gram order{self.ngram_order}')


    def normalize(self,text):
        clean_text=self.normalizer.normalize(text)
        text_list=[w for w in clean_text.split(' ') if w != '']
        context=text_list[-(self.ngram_order-1):]
        self.logger.debug(f'normalized context:{context}')
        return context
    
    def map_oov(self,context):
        vocab=self.model.vocab
        for i in range(len(context)):
            if context[i] not in vocab:
                context[i]='<UNK>'
                self.logger.warning(f'OOV word encountered at inference time: "{context[i]}" -> <UNK>')
        return context


    def predict_next(self, text,k):
        if not text or not text.strip():
            self.logger.error('Input text is empty. Please type at least one word.')
            raise ValueError('Input text is empty. Please type at least one word.')
        context = self.normalize(text)
        context = self.map_oov(context)
        predictions = self.model.lookup(context)
        sorted_predictions = sorted(predictions, key=lambda w: predictions[w], reverse=True)
        self.logger.debug(f'predict_next returning top {k} predictions')
        return sorted_predictions[:k]
