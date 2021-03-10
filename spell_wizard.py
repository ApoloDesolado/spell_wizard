import pickle
from collections import Counter
class Corrections:
    def __init__(self):
        self.languages={
                "en":"english",
                "es":"spanish"}
        self.load_language("en")
    def is_language(self, language):
        if language in self.languages:
            self.load_language(language)
            return True
        else:
            print("Language codes are:")
            [print(i, self.languages[i]) for i in self.languages]
            return False
    def load_language(self, language): self.words = pickle.loads(open(f"language_dicts/{self.languages[language]}.bin", "rb").read())
    def add_word(self):
        pass
    def candidates(self, word):
        return set(self.existent(self.generated_short(word))),  (self.existent(self.generated_medium(word)) or self.existent([word]))
        #return set(self.existent(self.generated_short(word)) or self.existent(self.generated_medium(word)) or self.existent([word]))
    def generated_short(self, word):
        letters= 'abcdefghijklmnopqrstuvwxyz'
        splits =      [ (word[:i], word[i:])              for i    in range(len(word)+1) ]
        deletes =     [ (x + y[1:])                       for x, y in splits if x and y ]
        transposes1 = [ (f"{x[-1]}{y[0]}{x[:-1]}{y[0:]}") for x, y in splits if x and y ]
        transposes2 = [ (f"{x[:-1]}{y[0]}{x[-1]}{y[1:]}") for x, y in splits if x and y ]
        replaces =    [ f"{x[:-1]}{l}{y}"                 for x, y in splits if x for l in letters ]
        inserts =     [ f"{x}{l}{y}"                      for x, y in splits for l in letters ]
        return set(deletes + transposes1 + transposes2 + replaces + inserts)
    def generated_medium(self, word):
        return (e2 for e1 in self.generated_short(word) for e2 in self.generated_short(e1))
    def generated_long(self):
        pass
    def existent(self, words): return set(filter(lambda x : x in self.words, words))
    def correction_data(self, word):
       candidates, two=self.candidates(word)
       candidates1=sorted(two, reverse=True, key=lambda x:self.words[x])
       candidates=sorted(candidates, reverse=True, key=lambda x:self.words[x])
       candidates=(candidates, candidates1)
       definitive = ""
       #candidates=self.candidates(word)
       #candidates=sorted(candidates, reverse=True, key=lambda x:self.words[x])
       #definitive=max(candidates, key=lambda x:self.words[x])
       return definitive, candidates

correction=Corrections()
x=correction.is_language("en")
while True:
    word=input("Write out your word: ")
    corrected, candidates=correction.correction_data(word)
    print()
    print(f"Corrected: {corrected}\nOptions: {candidates}")
