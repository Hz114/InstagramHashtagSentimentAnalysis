# -*- coding: utf-8 -*-

import csv
import multiprocessing as mp
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.python.keras.models import load_model


def sentiment_predict(tags):
    print("Start process")
    stopwords = ['의', '가', '이', '은', '들', '는', '좀', '잘', '걍', '과', '도', '를', '으로', '자', '에', '와', '한', '하다']
    loaded_model = load_model('./InstagramHashtagSentimentAnalysisApp/data/model/best_model_50000.h5')
    max_len = 30
    tokenizer = Tokenizer()
    total = 0
    X_train = []
    f = open("./InstagramHashtagSentimentAnalysisApp/data/model/X_train.csv", 'r')
    csvfile = csv.reader(f)
    for row in csvfile:
        X_train.append(row)
    okt = Okt()
    tokenizer.fit_on_texts(X_train)
    tokenizer.texts_to_sequences(X_train)
    for tag in tags:
        tag = okt.morphs(tag, stem=True) # 토큰화
        tag = [word for word in tag if not word in stopwords] # 불용어 제거
        encoded = tokenizer.texts_to_sequences([tag]) # 정수 인코딩
        pad_new = pad_sequences(encoded, maxlen = max_len) # 패딩
        score = float(loaded_model.predict(pad_new)) # 예측
        print("Tag ",tag,"는")
        if (score > 0.5):
            print("{:.2f}% 확률로 긍정 리뷰입니다.\n".format(score * 100))
            total += 1
        else:
            print("{:.2f}% 확률로 부정 리뷰입니다.\n".format((1 - score) * 100))
            total -= 1
    return total

def sentimentPredictPool(input_datas):
    pool = mp.Pool(processes=8)
    result = pool.map(sentiment_predict, input_datas)
    return sum(result)

if __name__ == '__main__':
    l = ['개판', '광화문맛집', '종각맛집', '삼겹살맛집', '교대이층집', '광화문이층집', '일산탄현제니스', '제니스맛집', '라멘맛집', '제주흑돼지맛집', '히노아지', '광화문맛집',
         '종각맛집', '삼겹살맛집', '교대 이층집', '광화문이층집', '일산탄현제니스', '제니스맛집', '라멘맛집', '제주흑돼지맛집', '히노아지']
    print(sentimentPredictPool(l))