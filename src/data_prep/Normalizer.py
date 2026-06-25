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
        p=Path(folder_path)
        if p.is_file():
            raw = p.read_text(encoding='utf-8-sig')
            return raw.replace('\n',' ')
        for file in p.glob('*.txt'):
            raw=file.read_text(encoding='utf-8-sig')
            cleaned=self.strip_gutenberg(raw)
            text += cleaned +'.'
        return text
            
    def strip_gutenberg(self,text):
        """ This function is run during the loading of the data to strip the start and end markers as well as other non book text"""
        start_marker='*** START OF THE PROJECT GUTENBERG EBOOK'
        end_marker='*** END OF THE PROJECT GUTENBERG EBOOK'
        if start_marker in text:
            text = text.split(start_marker)[1]
        if end_marker in text:
            text = text.split(end_marker)[0]
        return text
    
    def lowercase(self,text):
        """ Returns all text lowercase"""
        return text.lower()
    
    def remove_punctuation(self,text):
        """ Returns text without punctiuation or any symbol not in a-z"""
        return re.sub(r'[^a-z ]',' ',text)
    
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
        return [sentences.strip() for sentences in text.split('.') if sentences != '']

    def word_tokenize(self,sentence):
        """returns a list of tokenized words from the sentence passed to the function"""
        return [word for word in sentence.split(' ') if word !='']
    
    def save(self,sentences,file_path):
        """assume that the sentences passed on is a list of lists with each inner
          list consisting of a sentence tokenized into words"""
        p=open(file_path,'w')
        for sentence in sentences:
            for word in sentence:
                p.write(word+" ")
            p.write('\n')
        p.close()
