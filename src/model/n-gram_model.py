import os
from dotenv import load_dotenv

load_dotenv("config/.env")
class NGramModel:
    def __init__(self):
        self.vocab=[]
        self.model={}
        self.ngram_order=int(os.getenv("NGRAM_ORDER"))

    def build_vocab(self,token_file):
        pass

    def build_count_and_prob(self,token_file):
        pass

    def lookup(self,context):
        pass

    def save_model(self,model_path):
        pass

    def save_vocab(self,vocab_path):
        pass

    def load(self,model_path,vocab_path):
        pass