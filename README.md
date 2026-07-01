# N-gram Predictor Project 
This project is a N-gram language model, The corpus is four Sherlock Holmes novels by Arthur Conan Doyle, sourced from Project Gutenberg. The model is trained on all four novels. With a fifth novel being used as the evaluation corpus.
At inference time, the system takes the last NGRAM-ORDER − 1 words typed by the user and returns the top-k most probable next words using an n-gram model.(current model is using additive or laplace smoothing add-1 smoothing is applied in the ngram_model.py file)

#### Reference:
 Chen, S. F., & Goodman, J. (1999). An empirical study of smoothing techniques for language modeling. Computer Speech & Language, 13(4), 359–394. https://people.eecs.berkeley.edu/~klein/cs294-5/chen_goodman.pdf


## Requierments 
- python version 3.13.13
- Other dependancies included in requierments.txt for installation



## setup 
1) Clone the repo
2) create and activate an anaconda enviroment with the listed dependacies 
3) populate config/.env
4) download and properly sort the raw.txt files


## usage 

---------- To be filled in ---------------

## Project structure 

- ngram-predictor/

   - data/
       - raw/
           - train/
           - eval/
       - processed/
       -  model/
   - src/
        - data_prep/
       -  model/
       -  inference/
        - evaluation/
   -  main.py
   -  requirements.txt
   -  .gitignore
