import gensim, logging
import os,sys

#logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

class MySentences(object):
    def __init__(self, dirname):
        self.dirname = dirname
 
    def __iter__(self):
        for fname in os.listdir(self.dirname):
            for line in open(os.path.join(self.dirname, fname)):
                yield line.split()

traindir=sys.argv[1]
window_size=sys.argv[2]
lingosize = sys.argv[3]

sentences = MySentences(traindir) # a memory-friendly iterator
model = gensim.models.Word2Vec(sentences, size=100, window=window_size, min_count=1, sample=1e-4, negative=5, iter=20, sg=1, hs=0,  workers=4) 
#sg=1 skip-gram
model.wv.save_word2vec_format("drug.can.2M.l"+ str(lingosize)+".ws" +str(window_size) +".txt", fvocab=None, binary=False)
