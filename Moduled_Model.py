import csv
import time
import multiprocessing as mp
from multiprocessing import Lock, Queue

def sentimentpredict(tags, q, lock):
    from konlpy.tag import Okt
    from tensorflow.keras.preprocessing.text import Tokenizer
    from tensorflow.keras.preprocessing.sequence import pad_sequences
    from tensorflow.python.keras.models import load_model

    proc = mp.current_process() # 현재(지금) 돌아가고 있는 프로세스 아이디
    stopwords = ['의', '가', '이', '은', '들', '는', '좀', '잘', '걍', '과', '도', '를', '으로', '자', '에', '와', '한', '하다']
    loaded_model = load_model('./InstagramHashtagSentimentAnalysisApp/data/model/best_model_50000.h5')
    max_len = 30
    tokenizer = Tokenizer()
    a = 0 # 한 프로세스당 감정 지수 합
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
        # print("Tag ",tag,"는")
        if(score > 0.5):
            # print("{:.2f}% 확률로 긍정 태그입니다.\n".format(score * 100))
            a = a + 1
        else:
            # print("{:.2f}% 확률로 부정 태그입니다.\n".format((1 - score) * 100))
            a = a - 1
    with lock:
        print("프로세스 id : ", proc.pid)
        q.put(a)
        print("total : ", a)

def list_chunk(lst, n):
    return [lst[i:i + n] for i in range(0, len(lst), n)]

def resultModel(total):
    if total >= 0:
        result = '긍정적'
    else:
        result = '부정적'

    return result

def startModel(tags):
    Dis = int(len(tags) / 4)
    input_data = []

    process_list = []
    lock = Lock()
    q = Queue()
    total = 0

    # 프로세스 4개 기준으로, 분할하기
    if Dis != 0:
        input_datas = list_chunk(tags, Dis + 1)
    else:
        input_datas = list_chunk(tags, Dis)

    # 멀티 시작
    for input_data in input_datas:
        p = mp.Process(target=sentimentpredict, args=(input_data, q, lock))
        process_list.append(p)
        p.start()

    # 프로세스 종료 기다리기
    for proc in process_list:
        proc.join()
    for i in range(q.qsize()):
        total += q.get()
    print("전체 감정지수 : ", total)

    resultEmo = resultModel(total)

    return resultEmo



if __name__ == '__main__':
    l = ['개판', '광화문맛집', '종각맛집', '삼겹살맛집', '교대이층집', '광화문이층집', '일산탄현제니스', '제니스맛집', '라멘맛집', '제주흑돼지맛집', '히노아지', '광화문맛집',
         '종각맛집', '삼겹살맛집', '교대 이층집', '광화문이층집', '일산탄현제니스', '제니스맛집', '라멘맛집', '제주흑돼지맛집', '히노아지']
    # l을 수정하면 됩니다.
    Dis = int(len(l) / 4)
    input_data = []

    process_list = []
    lock = Lock()
    q = Queue()
    total = 0

    #프로세스 4개 기준으로, 분할하기
    if Dis != 0:
        input_datas = list_chunk(l, Dis + 1)
    else:
        input_datas = list_chunk(l, Dis)

    # 멀티 시작
    for input_data in input_datas:
        # print(input_data)
        p = mp.Process(target=sentimentpredict, args=(input_data, q, lock))
        process_list.append(p)
        # print("process start")
        p.start()

    # 프로세스 종료 기다리기
    for proc in process_list:
        proc.join()
    # print("\nover")
    for i in range(q.qsize()):
        total += q.get()
    print("전체 감정지수 : ",total)