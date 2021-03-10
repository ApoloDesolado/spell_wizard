import re
from collections import Counter
import string
import pickle
from timeit import timeit
class loader:
    def __init__(self, language, feed_with, allowed_symbols):
        self.language=language
        punctuation=set(allowed_symbols)
        other=set(string.punctuation)
        symbols=(other - punctuation)

        text=open(feed_with, "r").read().lower()
        rem = ("\t", "\n", "\r", "\x0b", "\x0c")
        for i in rem: text=text.replace(i, " ")
        words=text.split(" ")
        specials=[]
        _:[specials.append(word) for word in words for letter in word if letter in punctuation and letter in word[1:-1]]
        def hassymbols(word):
            for i in word:
                if i in symbols:
                    return False
            if word != '':
                return True
        new_words=list(filter(hassymbols, words))
        new_words.extend(specials)
        del words, text, specials
        words=Counter(new_words)
        many_words=len(new_words)
        self.final_dic=self.frequency(words, many_words)
        self.save_database()

    def frequency(self, words, many):
        dic={}
        for i in words:
            dic[i] = words[i]/many
        return dic
    def save_database(self):
        with open(f"language_dicts/{self.language}.bin", "wb") as file: file.write(pickle.dumps(self.final_dic))


loader=loader("english", "big.txt", "'´ ¨`")

#with open("database.pickle", "rb") as file: x=pickle.loads(file.read())
#file.close()
#words=["hello", "i'm", "your", "new", "teacher", "you", "puto", "little", "asshole", "the"]
#def frequency(word):
#    if word in final_dic:
#        print(word, final_dic[word])
#        return final_dic[word]
#    else:
#        return 0
#x=sorted(words, reverse=True, key=frequency)
#print(x)
