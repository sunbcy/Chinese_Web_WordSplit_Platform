from collections import Counter
from math import log10
from re import split
from jieba.posseg import dt

FLAGS = set('a an b f i j l n nr nrfg nrt ns nt nz s t v vi vn z eng'.split())

"""
a 形容词 取英语形容词 adjective的第1个字母。
an 名形词 具有名词功能的形容词。形容词代码 a和名词代码n并在一起。
b 区别词 取汉字“别”的声母。
f 方位词 取汉字“方”
i 成语 取英语成语 idiom的第1个字母。
j 简称略语 取汉字“简”的声母。
l 习用语 习用语尚未成为成语，有点“临时性”，取“临”的声母。
n 名词 取英语名词 noun的第1个字母。
nr 人名 名词代码 n和“人(ren)”的声母并在一起。
nrfg   古近代人名   刘备 关羽 张飞 赵云 任弼时 …
nrt 音译人名    米尔科 达尼丁 三世 五丁 塞拉 埃克尔斯 贝当 …
ns 地名 名词代码 n和处所词代码s并在一起。
nt 机构团体 “团”的声母为 t，名词代码n和t并在一起。
nz 其他专名 “专”的声母的第 1个字母为z，名词代码n和z并在一起。
s 处所词 取英语 space的第1个字母。
t 时间词 取英语 time的第1个字母。
v 动词 取英语动词 verb的第一个字母。
vi  动词  沉溺于 等同于 沉缅于 徜徉于
vn  名动词 审查 相互毗连 销蚀 对联 劳工 漫游 …
z   状态词 歪曲 飘飘 慢慢儿 急地 沉迷在 晕呼呼 …
"""


def cut(text):
    for sentence in split('[^a-zA-Z0-9\u4e00-\u9fa5]+', text.strip()):
        for w in dt.cut(sentence):
            print(w.word, w.flag)
            if len(w.word) > 1 and w.flag in FLAGS:
                yield w.word


class TFIDF:
    def __init__(self):
        self.idf = None
        self.idf_max = None

    def fit(self, texts):
        texts = [set(cut(text)) for text in texts]
        lent = len(texts)
        words = set(w for t in texts for w in t)
        self.idf = {w: log10(lent / (sum((w in t) for t in texts) + 1)) for w in words}
        self.idf_max = log10(lent)
        return self

    def get_idf(self, word):
        return self.idf.get(word, self.idf_max)

    def extract(self, text, top_n=10):
        counter = Counter()
        for w in cut(text):
            counter[w] += self.get_idf(w)
        return [i[0] for i in counter.most_common(top_n)]


tfidf = TFIDF().fit(['奶茶', '巧克力奶茶', '巧克力酸奶', '巧克力', '巧克力'] * 2)
print(tfidf.extract('酸奶巧克力奶茶'))
