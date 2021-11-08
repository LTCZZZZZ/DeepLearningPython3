import collections
import re
from d2l import tensorflow as d2l

# @save
d2l.DATA_HUB['time_machine'] = (d2l.DATA_URL + 'timemachine.txt',
                                '090b5e7e70c295757f55df93cb0a180b9691891a')


# print(d2l.DATA_HUB)

def read_time_machine():  # @save
    """Load the time machine dataset into a list of text lines."""
    with open(d2l.download('time_machine'), 'r') as f:
        lines = f.readlines()
    return [re.sub('[^A-Za-z]+', ' ', line).strip().lower() for line in lines]


lines = read_time_machine()
print(f'# text lines: {len(lines)}')
print(lines[0])
print(lines[10])


def tokenize(lines, token='word'):  # @save
    """将文本行拆分为单词或字符词元。"""
    if token == 'word':
        return [line.split() for line in lines]
    elif token == 'char':
        return [list(line) for line in lines]
    else:
        print('错误：未知词元类型：' + token)


tokens = tokenize(lines)
print(tokens[:10])
# for i in range(11):
#     print(tokens[i])

class Vocab:  # @save
    """Vocabulary for text."""

    def __init__(self, tokens=None, min_freq=0, reserved_tokens=None):
        if tokens is None:
            tokens = []
        if reserved_tokens is None:
            reserved_tokens = []
        # Sort according to frequencies
        counter = count_corpus(tokens)
        self._token_freqs = sorted(counter.items(), key=lambda x: x[1],
                                   reverse=True)
        # The index for the unknown token is 0
        self.idx_to_token = ['<unk>'] + reserved_tokens
        self.token_to_idx = {
            token: idx for idx, token in enumerate(self.idx_to_token)}
        for token, freq in self._token_freqs:
            if freq < min_freq:
                break
            if token not in self.token_to_idx:
                self.idx_to_token.append(token)
                self.token_to_idx[token] = len(self.idx_to_token) - 1

    def __len__(self):
        return len(self.idx_to_token)

    def __getitem__(self, tokens):
        if not isinstance(tokens, (list, tuple)):
            return self.token_to_idx.get(tokens, self.unk)
        return [self.__getitem__(token) for token in tokens]

    def to_tokens(self, indices):
        if not isinstance(indices, (list, tuple)):
            return self.idx_to_token[indices]
        return [self.idx_to_token[index] for index in indices]

    @property
    def unk(self):  # Index for the unknown token
        return 0

    @property
    def token_freqs(self):  # Index for the unknown token
        return self._token_freqs


def count_corpus(tokens):  # @save
    """Count token frequencies."""
    # Here `tokens` is a 1D list or 2D list
    if len(tokens) == 0 or isinstance(tokens[0], list):
        # Flatten a list of token lists into a list of tokens
        tokens = [token for line in tokens for token in line]
    return collections.Counter(tokens)


vocab = Vocab(tokens)
print(list(vocab.token_to_idx.items())[:10])

# 这两行是Copilot的代码，后续待考察
# 下面的注释也是，我惊了，
# 在这里，我们发现，
# 如果我们把tokens改成了list，
# 那么就会发现，
# 在这里，
# 如果我们把tokens改成了list，
# 那么就会发现，
# 在这里，
# 如果我们把tokens改成了list，
# 那么就会发现，
# 在这里，
# 如果我们把tokens改成了list，
# 这个vocab的token_to_idx是什么？
# 其实是一个字典，key是token，value是token对应的idx
# 其实这个vocab的idx_to_token是一个list，里面的元素是token，这个list的第一个元素是<unk>，其实是一个token
# 其实这个vocab的token_to_idx是一个字典，key是token，value是token对应的idx
# 其实这个vocab的token_freqs是一个list，里面的元素是一个tuple，第一个元素是token，第二个元素是token对应的频率
print(vocab.to_tokens([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]))
print(vocab.token_freqs[:10])



for i in [0, 10]:
    print('words:', tokens[i])
    print('indices:', vocab[tokens[i]])
