import re
from main import LoggerSetup
import inflect
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer 
class Cleaning:
    """
    Main Exposed Function for Cleaning
    Is : run(self , cv_content : str) -> str 
    """
    def __init__(self):
        self.logger = LoggerSetup.get_logger(__name__)
        self.logger.info("Cleaning instance initialized")
        self.inflector = inflect.engine()
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('wordnet')
        self.stop_words = set(stopwords.words('english'))
        self.porter_stemmer = PorterStemmer()
        self.lemmatizer = WordNetLemmatizer()

    def __remove_special_characters(self , content : str) -> str:
        """
        Private Function for Removing Special Characters
        Removes unwanted special characters while preserving important punctuation
        Is : __remove_special_characters(self , content : str) -> str 
        """
        try:
            # Remove non-printable characters except newlines, tabs, and carriage returns
            content = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', content)
            
            # Remove excessive special characters (keeping common punctuation)
            # This preserves: letters, numbers, spaces, newlines, basic punctuation (.,;:!?-()[]{}@#$%&*+=/)
            content = re.sub(r'[^\w\s.,;:!?\-()\[\]{}@#$%&*+=/\n\r\t\'"°•·]', ' ', content)
            
            # Remove bullet points and special list markers
            content = re.sub(r'[►▪▫■□●○◆◇★☆✓✔✗✘➢➣➤]', '', content)
            
            # Remove multiple consecutive special characters (except spaces and newlines)
            content = re.sub(r'([.,;:!?\-]){2,}', r'\1', content)
            
            self.logger.debug(f"Special characters removed. Length after: {len(content)}")
            return content
        except Exception as e:
            self.logger.error(f"Error removing special characters: {str(e)}", exc_info=True)
            raise    

    def __remove_extra_spaces(self , content : str) -> str:
        """
        Private Function for Removing Extra Spaces
        Normalizes whitespace by removing extra spaces, tabs, and trailing spaces
        Is : __remove_extra_spaces(self , content : str) -> str 
        """
        try:
            # Replace tabs with single space
            content = content.replace('\t', ' ')
            
            # Replace multiple spaces with single space
            content = re.sub(r' {2,}', ' ', content)
            
            # Remove spaces at the beginning of lines
            content = re.sub(r'^[ ]+', '', content, flags=re.MULTILINE)
            
            # Remove spaces at the end of lines
            content = re.sub(r'[ ]+$', '', content, flags=re.MULTILINE)
            
            # Remove space before punctuation
            content = re.sub(r'\s+([.,;:!?)])', r'\1', content)
            
            # Ensure space after punctuation (if not already present)
            content = re.sub(r'([.,;:!?])([^\s\d])', r'\1 \2', content)
            
            self.logger.debug(f"Extra spaces removed. Length after: {len(content)}")
            return content
        except Exception as e:
            self.logger.error(f"Error removing extra spaces: {str(e)}", exc_info=True)
            raise        

    def __remove_extra_newlines(self , content : str) -> str:
        """
        Private Function for Removing Extra Newlines
        Normalizes line breaks by removing excessive blank lines
        Is : __remove_extra_newlines(self , content : str) -> str 
        """
        try:
            # Normalize different line ending styles to \n
            content = content.replace('\r\n', '\n').replace('\r', '\n')
            
            # Remove more than 2 consecutive newlines (keep max 1 blank line between sections)
            content = re.sub(r'\n{3,}', '\n\n', content)
            
            # Remove newlines that appear after certain punctuation followed by space
            # This helps merge lines that were incorrectly split
            content = re.sub(r'([a-z,])\n([a-z])', r'\1 \2', content)
            
            # Remove leading and trailing newlines from the entire content
            content = content.strip()
            
            self.logger.debug(f"Extra newlines removed. Length after: {len(content)}")
            return content
        except Exception as e:
            self.logger.error(f"Error removing extra newlines: {str(e)}", exc_info=True)
            raise    

    def __remove_headers_footers(self, content: str, header_patterns=None, footer_patterns=None) -> str:
        """
        Private Function for Removing Headers and Footers
        Removes common header and footer patterns from documents
        Is : __remove_headers_footers(self, content: str, header_patterns=None, footer_patterns=None) -> str
        """
        try:
            if header_patterns is None:
                header_patterns = [r'^.*Header.*$']
            if footer_patterns is None:
                footer_patterns = [r'^.*Footer.*$']

            for pattern in header_patterns + footer_patterns:
                content = re.sub(pattern, '', content, flags=re.MULTILINE)

            self.logger.debug(f"Headers and footers removed. Length after: {len(content)}")
            return content.strip()
        except Exception as e:
            self.logger.error(f"Error removing headers/footers: {str(e)}", exc_info=True)
            raise

    def __remove_repeated_substrings(self, content: str, pattern=r'\.{2,}') -> str:
        """
        Private Function for Removing Repeated Substrings
        Removes repeated patterns like multiple dots, dashes, etc.
        Is : __remove_repeated_substrings(self, content: str, pattern=r'\.{2,}') -> str
        """
        try:
            # Remove repeated dots
            content = re.sub(pattern, '.', content)
            
            # Remove repeated dashes
            content = re.sub(r'-{3,}', '-', content)
            
            # Remove repeated underscores
            content = re.sub(r'_{3,}', '_', content)
            
            # Remove repeated equals signs
            content = re.sub(r'={3,}', '', content)
            
            self.logger.debug(f"Repeated substrings removed. Length after: {len(content)}")
            return content.strip()
        except Exception as e:
            self.logger.error(f"Error removing repeated substrings: {str(e)}", exc_info=True)
            raise
    
    def __text_lowercase(self , content : str) -> str:
        """
        Private Function for Lowercasing Text
        Converts all text to lowercase
        Is : __text_lowercase(self , content : str) -> str 
        """
        try:
            content = content.lower()
            self.logger.debug(f"Text lowercased. Length after: {len(content)}")
            return content
        except Exception as e:
            self.logger.error(f"Error lowercasing text: {str(e)}", exc_info=True)
            raise

    def __convert_numbers_to_words(self , content : str) -> str:
        """
        Private Function for Converting Numbers to Words
        Converts numeric digits to their word representation
        Is : __convert_numbers_to_words(self , content : str) -> str 
        """
        try:
            def replace_number(match):
                number = match.group(0)
                return self.inflector.number_to_words(number)

            content = re.sub(r'\b\d+\b', replace_number, content)
            self.logger.debug(f"Numbers converted to words. Length after: {len(content)}")
            return content
        except Exception as e:
            self.logger.error(f"Error converting numbers to words: {str(e)}", exc_info=True)
            raise   

    def  __remove_stopwords(self , content : str) -> str:
        """
        Private Function for Removing Stopwords
        Removes common stopwords from the text
        Is : __remove_stopwords(self , content : str) -> str 
        """
        try:
            words = word_tokenize(content)
            filtered_words = [word for word in words if word.lower() not in self.stop_words]
            content = ' '.join(filtered_words)
            self.logger.debug(f"Stopwords removed. Length after: {len(content)}")
            return content
        except Exception as e:
            self.logger.error(f"Error removing stopwords: {str(e)}", exc_info=True)
            raise     

    def __stem_words(self , content : str) -> str:
        """
        Private Function for Stemming Words
        Reduces words to their root form using Porter Stemmer
        Is : __stem_words(self , content : str) -> str 
        """
        try:
            words = word_tokenize(content)
            stemmed_words = [self.porter_stemmer.stem(word) for word in words]
            content = ' '.join(stemmed_words)
            self.logger.debug(f"Words stemmed. Length after: {len(content)}")
            return content
        except Exception as e:
            self.logger.error(f"Error stemming words: {str(e)}", exc_info=True)
            raise        

    def __lemmatize_words(self , content : str) -> str: 
        """
        Private Function for Lemmatizing Words
        Reduces words to their base form using WordNet Lemmatizer
        Is : __lemmatize_words(self , content : str) -> str 
        """
        try:
            words = word_tokenize(content)
            lemmatized_words = [self.lemmatizer.lemmatize(word) for word in words]
            content = ' '.join(lemmatized_words)
            self.logger.debug(f"Words lemmatized. Length after: {len(content)}")
            return content
        except Exception as e:
            self.logger.error(f"Error lemmatizing words: {str(e)}", exc_info=True)
            raise   
    def __remove_repetitive_words(self , content : str) -> str:
        """
        Private Function for Removing Repetitive Words from Text
        Removes ALL duplicate words from entire text, keeping only first occurrence
        Is : __remove_repetitive_words(self , content : str) -> str 
        """
        try:
            tokens = word_tokenize(content)
            
            # Remove all duplicate words while preserving order of first occurrences
            seen_words = set()
            filtered_tokens = []
            
            for token in tokens:
                # Only add if we haven't seen this word before (case-insensitive)
                token_lower = token.lower()
                if token_lower not in seen_words:
                    filtered_tokens.append(token)
                    seen_words.add(token_lower)
            
            content = ' '.join(filtered_tokens)
            self.logger.debug(f"Repetitive words removed. Length after: {len(content)}")
            return content
        except Exception as e:
            self.logger.error(f"Error removing repetitive words: {str(e)}", exc_info=True)
            raise
    def run(self , content : str , translation_callback=None) -> str:
        """
        Main Exposed Function for Cleaning
        Is : run(self , content : str , translation_callback=None) -> str 
        Args:
            content: The text content to be cleaned
            translation_callback: Optional function to translate text to English
        """
        self.logger.info(f"Starting Cleaning process. Content length: {len(content)} characters")
        
        try:
            # Remove headers and footers
            content = self.__remove_headers_footers(content)
            self.logger.debug("Headers and footers removed")
            
            # Remove special characters
            content = self.__remove_special_characters(content)
            self.logger.debug("Special characters removed")
            
            # Remove repeated substrings like dots
            content = self.__remove_repeated_substrings(content)
            self.logger.debug("Repeated substrings removed")
            
            # Remove extra spaces between lines and within lines
            content = self.__remove_extra_spaces(content)
            self.logger.debug("Extra spaces removed")
            
            # Remove extra newlines
            content = self.__remove_extra_newlines(content)
            self.logger.debug("Extra newlines removed")
            
            # Convert text to lowercase
            content = self.__text_lowercase(content)
            self.logger.debug("Text converted to lowercase")
            
            content = translation_callback(content) if translation_callback else content
            # Convert numbers to words
            content = self.__convert_numbers_to_words(content)
            self.logger.debug("Numbers converted to words")
            
            # Remove stopwords
            content = self.__remove_stopwords(content)
            self.logger.debug("Stopwords removed")
            
            # Stem words
            content = self.__stem_words(content)
            self.logger.debug("Words stemmed")
            
            # Lemmatize words
            content = self.__lemmatize_words(content)
            self.logger.debug("Words lemmatized")
            
            # Remove repetitive words
            content = self.__remove_repetitive_words(content)
            self.logger.debug("Repetitive words removed")
            
            self.logger.info(f"Cleaning completed. Final content length: {len(content)} characters")
            return content
        except Exception as e:
            self.logger.error(f"Error during Cleaning: {str(e)}", exc_info=True)
            raise