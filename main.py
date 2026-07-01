import argparse, os, dotenv ,logging
from dotenv import load_dotenv 
load_dotenv('config/.env')
def setup_logging():
    """configures logging once for the entire program. all other modules just
    call logging.getLogger(__name__) and inherit this setup automatically."""
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.FileHandler('ngram_model.log')]
    )

setup_logging()

from src.data_prep.Normalizer import Normalizer
from src.model.ngram_model import NGramModel
from src.inference.Predictor import Predictor

logger = logging.getLogger(__name__)

def data_prep():
    logger.info('Data_prep started')
    n=Normalizer()
    text=n.load(os.getenv('SAMPLE_DATA_PATH'))
    sentences=n.sentence_tokenize(text)
    tokenized=[]
    for sentence  in sentences:
        normalized=n.normalize(sentence)
        words=n.word_tokenize(normalized)
        tokenized.append(words)
      
    n.save(tokenized,os.getenv('TRAIN_TOKENS_PATH'))
    logger.info('Data prep completed')

def model():
    logger.info('model creation started')
    try:
        train_tokens_path = os.environ['TRAIN_TOKENS_PATH']
        model_path = os.environ['MODEL_PATH']
        vocab_path = os.environ['VOCAB_PATH']
    except KeyError as e:
        logger.error(f'Missing config variable: {e}. Check config/.env')
        raise
    m = NGramModel()
    m.build_vocab(train_tokens_path)
    m.build_count_and_prob(train_tokens_path)
    m.save_model(model_path)
    m.save_vocab(vocab_path)
    logger.info('model building complete')

def inference():
    logger.info('Inference run started')
    try:
        model_path = os.environ['MODEL_PATH']
        vocab_path = os.environ['VOCAB_PATH']
        top_k = int(os.environ['TOP_K'])
    except KeyError as e:
        logger.error(f'Missing config variable: {e}. Check config/.env')
        raise


    n = Normalizer()
    m = NGramModel()
    m.load(os.getenv('MODEL_PATH'), os.getenv('VOCAB_PATH'))
    p = Predictor(m, n)
    k = int(os.getenv('TOP_K'))

    print('select mode:')
    print('1 - next word predictor')
    print('2 - generate n words')
    mode = input('> ')

    if mode == '1':
        text = ''
        while True:
            if text == '':
                word = input('> ')
            else:
                word = input(f'> {text} ')

            if word == 'quit':
                print('Goodbye')
                break
            if word == 'reset':
                text = ''
                continue

            text = (text + ' ' + word).strip()
            predictions = p.predict_next(text, k)
            print(f'Predictions: {predictions}')

    elif mode == '2':
        while True:
            print('enter number of words to generate (or "quit"):')
            n_words = input('> ')
            if n_words == 'quit':
                print('Goodbye')
                break
            if not n_words.isdigit():
                print('please enter a valid number')
                continue
            n_words = int(n_words)

            print('enter starting input:')
            text = input('> ')
            if text == 'quit':
                print('Goodbye')
                break

            print(f'\n{text}', end=' ')
            for _ in range(n_words):
                predictions = p.predict_next(text, k)
                if not predictions:
                    print('\nno predictions found, stopping early')
                    break
                next_word = next((w for w in predictions if w != '<UNK>'), None)
                if not next_word:
                    print('\nno valid predictions found, stopping early')
                    break
                print(next_word, end=' ', flush=True)
                text = text + ' ' + next_word

            print('\n')
    else:
        print('invalid mode selected')
    logger.info('inference run completed')

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
