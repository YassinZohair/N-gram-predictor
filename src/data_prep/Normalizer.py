from pathlib import Path
import re
class Normalizer:
    """Loads, cleans, tokenizes and saves raw Gutenberg text files for use in the N-gram model."""
    def __init__ (self):
        pass

    def load(self,folder_path):
        """ This function loops over all files in the folderpath
        passed to the function and returns a string of all the text concatinated into one variable """

        text=str()
        for file in Path(folder_path).glob('*.txt'):
            text+=file.read_text(encoding='utf-8')
        return text 
            
    def strip_gutenberg(self,text):
        """ This function for now only returns the 1st book cleaned as we are only focused on using 100 or so words, 
        later will be changed to return the full 3 training books cleaned and concatinated"""
    
        removed_start=text.split('''*** START OF THE PROJECT GUTENBERG EBOOK THE ADVENTURES OF SHERLOCK
HOLMES ***''')[1]
        removed_end = removed_start.split('''*** END OF THE PROJECT GUTENBERG EBOOK THE ADVENTURES OF SHERLOCK
HOLMES ***''')[0]
        return removed_end
    
    def lowercase(self,text):
        """ Returns all text lowercase"""
        return text.lower()
    
    def remove_punctuation(self,text):
        """ Returns text without punctiuation or any symbol not in a-z"""
        return re.sub(r'[^a-z ]','',text)
    
    def remove_numbers(self,text):
        """ extra function if remove_punctuation is called before it and 
        removes specifically any character within and including 0-9"""
        return re.sub(r'[0-9]','',text)
    
    def remove_whitespace(self,text):
        """ removes any extra whitespace or blank line and only replaces with one space """
        return re.sub(r'\s+',' ',text)
    
    def normalize(self,text):
        """ calls all normalization funtions in order on the string variable passed and returns the normalized text """
        normalized_text= self.lowercase(text)
        normalized_text=self.remove_punctuation(normalized_text)
        normalized_text=self.remove_numbers(normalized_text)
        normalized_text=self.remove_whitespace(normalized_text)
        return normalized_text

        
    def sentence_tokenize(self,text):
        """ returnes a list of sentences split only by full stop"""
        return [sentences for sentences in text.split('.') if sentences != '']

    def word_tokenize(self,sentence):
        """returns a list of tokenized words from the sentence passed to the function"""
        return sentence.split(' ')
    
    def save(self,sentences,file_path):
        """assume that the sentences passed on is a list of lists with each inner
          list consisting of a sentence tokenized into words"""
        p=open(file_path,'w')
        for sentence in sentences:
            for word in sentence:
                p.write(word+" ")
            p.write('\n')
        p.close()
