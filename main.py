import argparse, os, dotenv
from src.data_prep.Normalizer import Normalizer
from src.model.ngram_model import NGramModel
from src.inference.Predictor import Predictor

from dotenv import load_dotenv 
load_dotenv('config/.env')


def data_prep():
    print("data_prep called")
    n=Normalizer()
    text=n.load(os.getenv('SAMPLE_DATA_PATH'))
    sentences=n.sentence_tokenize(text)
    tokenized=[]
    for sentence  in sentences:
        normalized=n.normalize(sentence)
        words=n.word_tokenize(normalized)
        tokenized.append(words)
      
    n.save(tokenized,os.getenv('TRAIN_TOKENS_PATH'))
    print("Data preperation complete")
def model():
    print(' model function called')
    m=NGramModel()
    m.build_vocab(os.getenv('TRAIN_TOKENS_PATH'))
    m.build_count_and_prob(os.getenv('TRAIN_TOKENS_PATH'))
    m.save_model(os.getenv('MODEL_PATH'))
    m.save_vocab(os.getenv('VOCAB_PATH'))
    print('model building completed')
def inference():
    print ('inference started')
    n = Normalizer()
    m = NGramModel()
    m.load(os.getenv('MODEL_PATH'), os.getenv('VOCAB_PATH'))
    p = Predictor(m, n)
    k = int(os.getenv('TOP_K'))
    
    while True:
        print('enter input :')
        text = input('> ')
        if text == 'quit':
            print('Goodbye')
            break
        predictions = p.predict_next(text, k)
        print(f'Predictions: {predictions}')
    print ('inference run completed')

def run_all():
    data_prep()
    model()
    inference()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--step', type=str, required=True)
    args = parser.parse_args()

    if args.step == "data_prep":
        data_prep()
    elif args.step == "model":
        model()
    elif args.step == "inference":
        inference()
    elif args.step == "all":
        run_all()
    else:
        print(f"Unknown step: {args.step}. Choose from: dataprep, model, inference, all")
