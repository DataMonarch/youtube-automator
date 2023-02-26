import nltk
from gingerit.gingerit import GingerIt

# nltk.download('punkt')

# def correct_text(text):
#     correct_text = ''
#     for sentence in sentences:
#     parser = GingerIt()
#     corrected_sentence = parser.parse(sentence)
#     return corrected_text['result']

text = "I is a engeneer. I can has cheezburger?"
sentences = nltk.sent_tokenize(text)

for sentence in sentences:
    parser = GingerIt()
    corrected_sentence = parser.parse(sentence)
    print(corrected_sentence['result'])
