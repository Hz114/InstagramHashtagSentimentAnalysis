# -*- coding: utf-8 -*-

import csv
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.python.keras.models import load_model

'''
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding = 'utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding = 'utf-8')

import tensorflow as tf

physical_devices = tf.config.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(physical_devices[0], enable=True)


reload(sys)
sys.setdefaultencoding('utf-8')
'''

def sentimentPredict(tags):
    loaded_model = None

    stopwords = ['의', '가', '이', '은', '들', '는', '좀', '잘', '걍', '과', '도', '를', '으로', '자', '에', '와', '한', '하다']
    loaded_model = load_model('./InstagramHashtagSentimentAnalysisProject/data/model/best_model.h5')
    max_len = 30
    tokenizer = Tokenizer()
    X_train = []
    f = open("./InstagramHashtagSentimentAnalysisProject/data/model/X_train.csv", 'r')
    csvfile = csv.reader(f)
    for row in csvfile:
        X_train.append(row)
    okt = Okt()
    tokenizer.fit_on_texts(X_train)
    tokenizer.texts_to_sequences(X_train)
    total = 0
    pads = []
    # 위에는 모델 학습 기준에 맞추는 작업
    # 아래는 확인하고 싶은 데이터를 쪼개서 모델에 넣어보는 작업
    for tag in tags:
        tag = okt.morphs(tag, stem=True)  # 토큰화
        tag = [word for word in tag if not word in stopwords]  # 불용어 제거
        encoded = tokenizer.texts_to_sequences([tag])  # 정수 인코딩
        pad_new = pad_sequences(encoded, maxlen=max_len)  # 패딩
        pads.append(pad_new)
    for pad in pads:
        score = float(loaded_model.predict(pad))  # 예측
        print("Tag ", tag, "는")
        if (score > 0.5):
            print("{:.2f}% 확률로 긍정 리뷰입니다.\n".format(score * 100))
            total += 1
        else:
            print("{:.2f}% 확률로 부정 리뷰입니다.\n".format((1 - score) * 100))
            total -= 1
    return total


if __name__ == '__main__':
    l = ['광화문맛집', '종각맛집', '삼겹살맛집', '교대이층집', '광화문이층집', '일산탄현제니스', '제니스맛집', '라멘맛집', '제주흑돼지맛집', '히노아지', '광화문맛집', '종각맛집', '삼겹살맛집', '교대 이층집', '광화문이층집', '일산탄현제니스', '제니스맛집', '라멘맛집', '제주흑돼지맛집', '히노아지']
    EQ = sentimentPredict(l)

    print(EQ)
    print("error안남")