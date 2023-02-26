import nltk
from gingerit.gingerit import GingerIt

# nltk.download('punkt')

def correct_text(text):
    """Corrects the grammar of the inputted text using the GingerIt library

    Args:
        text (str): The text to be corrected

    Returns:
        str: The corrected text
    """
    correct_text = ''
    sentences = nltk.sent_tokenize(text)
    
    for sentence in sentences:
        parser = GingerIt()
        corrected_sentence = parser.parse(sentence)
        correct_text += corrected_sentence['result'] + ' '

    return correct_text

