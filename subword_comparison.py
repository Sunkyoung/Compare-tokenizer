from tokenizers import CharBPETokenizer, ByteLevelBPETokenizer, SentencePieceBPETokenizer, BertWordPieceTokenizer
from tokenizers.decoders import ByteLevel
import time
from random import randint
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

# https://github.com/huggingface/tokenizers/tree/master/bindings/python
# - CharBPETokenizer: The original BPE
# - ByteLevelBPETokenizer: The byte level version of the BPE
# - SentencePieceBPETokenizer: A BPE implementation compatible with the one used by SentencePiece
# - BertWordPieceTokenizer

f = open('dataset/sample-context.txt','r')
lines = f.readlines()
print('total lines : ',len(lines))
n = randint(0, len(lines))

def tokenizer_train(tokenizer):
    restart = time.time()
    tokenizer.train(["Compare-tokenizer/dataset/sample-context.txt"], vocab_size=16000)
    print('Training Time : ', time.time()-restart)
    return tokenizer

def tokenizer_output(tokenizer, name):
    y = []
    print('Original Sentence : ',lines[n])
    output = tokenizer.encode(lines[n]).tokens
    if name == 'ByteLevelBPE':
        decoder = ByteLevel()
        output = [ decoder.decode([o]) for o in output ]
    print('Random Analyze Result : ', output)

    start = time.time()
    output = tokenizer.encode(''.join(lines[:11]))
    y.append(time.time()-start)
    start = time.time()
    output = tokenizer.encode(''.join(lines[:101]))
    y.append(time.time()-start)
    start = time.time()
    output = tokenizer.encode(''.join(lines[:1001]))
    y.append(time.time()-start)
    start = time.time()
    output = tokenizer.encode(''.join(lines))
    y.append(time.time()-start)

    print('Measured time : ', y)
    draw_plot(y, name)

def draw_plot(y, name):
    x = [10, 100, 1000, 10000]
    plt.plot(x, y, label=name)

# Initialize a tokenizer
start = time.time()
tokenizer = CharBPETokenizer()
print('CharBPE Loading Time : ', time.time()-start)
tokenizer_output(tokenizer_train(tokenizer), 'CharBPE')

start = time.time()
tokenizer = SentencePieceBPETokenizer()
print('SentencePiece Loading Time : ', time.time()-start)
tokenizer_output(tokenizer_train(tokenizer), 'SentencePiece')

start = time.time()
tokenizer = ByteLevelBPETokenizer()
print('ByteLevelBPE Loading Time : ', time.time()-start)
tokenizer_output(tokenizer_train(tokenizer), 'ByteLevelBPE')

start = time.time()
tokenizer = BertWordPieceTokenizer(lowercase=False)
print('BertWordPiece Loading Time : ', time.time()-start)
tokenizer_output(tokenizer_train(tokenizer), 'BertWordPiece')

plt.legend()
plt.savefig('subword_result.png')
