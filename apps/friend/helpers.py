from gensim.models import word2vec


class W2V:

    model = "alaltalk/word2vec/kor_word2vec.model"

    @classmethod
    def load(self):
        return word2vec.Word2Vec.load(self.model)
