import numpy as np
from gensim.corpora import Dictionary
from gensim.similarities import MatrixSimilarity


class Pipline:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer

    def duplidelete(self, texts: list, score: float):
        tokens = self.tokenizer(texts)
        dct = Dictionary(tokens)
        corpus = [dct.doc2bow(item) for item in tokens]
        index = MatrixSimilarity(corpus, num_features=len(dct))
        sims = index[corpus]
        filtred_scores = np.where(sims >= score)
        paraphrases = set([tuple(sorted((i, j))) for i, j in zip(filtred_scores[0], filtred_scores[1])])
        not_similar_indexes = []
        for t1 in paraphrases:
            temp = set()
            for t2 in [x for x in paraphrases if x != t1]:
                if set(t1) & set(t2):
                    temp |= set(t2)
            if temp:
                not_similar_indexes.append(tuple(temp))

            if not set(t1) & temp:
                not_similar_indexes.append(tuple(set(t1)))

        unique_not_similar_indexes = [x[0] for x in set(not_similar_indexes)]
        not_similar_texts = [texts[i] for i in unique_not_similar_indexes]
        return not_similar_texts


if __name__ == "__main__":
    from src.start import tokenizer

    pl = Pipline(tokenizer)
    texts = ["самолет летит в небе", "папа у васи силен в математике", "папа у васи силен в физике", "летит в небе самолет", "мама мыла окно папа держал ее за ноги", "летит в небе самолет", "силен папа у васи в математике"]
    inx = pl.duplidelete(texts, 0.7)
    print(inx)
