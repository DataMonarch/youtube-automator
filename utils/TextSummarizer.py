# summarize a body of text by extracting the most information dense sentences

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

def summaize(text: str, num_resultatnt_sentences: int = None):

    # Load text
    if not num_resultatnt_sentences:
        num_resultatnt_sentences = len(text.split('.'))

    # Initialize parser and tokenizer
    parser = PlaintextParser.from_string(text, Tokenizer("english"))

    # Initialize summarizer
    summarizer = LexRankSummarizer()

    # Summarize text
    summary = summarizer(parser.document, num_resultatnt_sentences) # 3 is the number of sentences to select

    # Print summary
    return summary