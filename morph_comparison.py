# -*- coding: utf-8 -*-
import timeit, time
from random import randint
from konlpy.tag import Hannanum, Kkma, Komoran, Mecab, Okt
from khaiii import KhaiiiApi

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

f = open('dataset/sample-context.txt','r')
lines = f.readlines()
print('total lines : ',len(lines))
n = randint(0, len(lines))

def measure_time(analyzer, n, lines, name):
    y = []
    print('=== ',name,' ===')
    print('Original Sentence : ',lines[n])
    print('Random Analyze Result : ', analyzer.morphs(lines[n]))
    start = time.time()
    analyzer.morphs(''.join(lines[:11]))
    y.append(time.time()-start)
    start = time.time()
    analyzer.morphs(''.join(lines[:101]))
    y.append(time.time()-start)
    start = time.time()
    analyzer.morphs(''.join(lines[:1001]))
    y.append(time.time()-start)
    start = time.time()
    analyzer.morphs(''.join(lines))
    y.append(time.time()-start)
    print('Measured time : ',y)
    draw_plot(y, name)

def measure_khaiii_time(analyzer, n, lines):
    y = []
    print('=== Khaiii ===')
    print('Original Sentene : ',lines[n])
    print('Random Analyze Result : ', end='')
    for word in analyzer.analyze(lines[n]):
        for morph in word.morphs:
            res = str(morph)
            idx = res.find('/')
            print(res[:idx], end=',')
    print()
    start = time.time()
    analyzer.analyze(''.join(lines[:11]))
    y.append(time.time()-start)
    start = time.time()
    analyzer.analyze(''.join(lines[:101]))
    y.append(time.time()-start)
    start = time.time()
    analyzer.analyze(''.join(lines[:1001]))
    y.append(time.time()-start)
    start = time.time()
    analyzer.analyze(''.join(lines))
    y.append(time.time()-start)
    print('Measured time : ',y)
    draw_plot(y, 'Khaiii')

def draw_plot(y, name):
    x = [10, 100, 1000, 10000]
    plt.plot(x, y, label=name)

measure_time(Hannanum(), n, lines, 'Hannanum')

measure_time(Kkma(), n, lines, 'Kkma')

measure_time(Komoran(), n, lines, 'Komoran')

measure_time(Mecab(), n, lines, 'Mecab')

measure_time(Okt(), n, lines, 'Okt')

measure_khaiii_time(KhaiiiApi(), n, lines)

plt.legend()
plt.savefig('morph_result.png')