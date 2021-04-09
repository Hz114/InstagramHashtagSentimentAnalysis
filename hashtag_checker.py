
import os
import csv

# CSV 파일 read
def openCsv(id):
    path = "./InstagramHashtagSentimentAnalysisApp/data/csv/" + id + ".csv"
    f = open(path,"r",encoding='utf-8')
    rdr = csv.reader(f)
    tags = []
    for line in rdr:
        if line[0].isdigit(): # 첫 번째 인수의 값이 숫자면
            new_string = ''.join(filter(str.isalnum, line[-1])) # 특수문자 제거
            tags.append(new_string)
        # 한 줄 읽고, 0번이 숫자면 해당 리스트의 마지막 내용을 읽어온다.

    return tags

def hashtag():
    path_hash_utf8 = "./InstagramHashtagSentimentAnalysisApp/data/hash/utf-8"
    path_hash_cp949 = "./InstagramHashtagSentimentAnalysisApp/data/hash/cp949"

    # 파일 읽어오기
    file_list = os.listdir(path_hash_utf8)

    Middle = [i for i in range(0,24)] # 단어 체크용
    count = 0 # 인덱싱용
    file_order = [] # 순서용
    for file in file_list:
        file_order.append(file)
        path = path_hash_utf8 + "\\" + file
        f = open(path,"r", encoding = 'utf-8')
        Middle[count] = f.read()
        count += 1
        f.close()

    # 인코딩 오류나는 나머지 파일 읽어들이기
    
    path = path_hash_cp949 + "\\" + "T셀카.txt"
    f = open(path,"r",encoding="cp949")
    file_order.append("T셀카.txt")
    Middle[count] = f.read()
    count += 1
    f.close()
    
    path = path_hash_cp949 + "\\" + "T일상.txt"
    f = open(path,"r",encoding="cp949")
    file_order.append("T일상.txt")
    Middle[count] = f.read()
    count += 1
    f.close()
    
    path = path_hash_cp949 + "\\" + "T데일리코디.txt"
    f = open(path,"r",encoding="cp949")
    file_order.append("T데일리코디.txt")
    Middle[count] = f.read()
    f.close()
    
    # 영어부분 추가
    Middle[-1] = 'eng'
    file_order.append('eng')

    return Middle, file_order

def comparison(tags, Middle, file_order):
    light_on = [ 0 for i in range(len(file_order))] # 일치하는 문장이나 구절이 있으면 +1, 인덱스는 file_order 따라감
    for tag in tags:
        if tag.encode().isalpha():
            light_on[-1] += 1
        for i in range(len(Middle)):
            if tag in Middle[i]:
                light_on[i] += 1
            #--- '비' tag도 육아에 잡힘.
    return  light_on

def hashtagTop3(dic):
    sortDic = sorted(dic.items(), key=lambda x: x[1], reverse=True)
    sortDic = sortDic[:3]

    print(sortDic)
    result = []
    for key, value in sortDic:
        if value != 0:
            if key == 'eng':
                result.append('외국인')
            else:
                result.append(key[1:-4])

    while len(result) != 3:
        if '감정' not in result:
            result.append('감정')
        elif '일상' not in result:
            result.append('일상')
        elif '취미' not in result:
            result.append('취미')
    return result

def hashtagChecker(id):
    id = str(id)
    tags = openCsv(id)
    Middle, file_order = hashtag()
    light_on = comparison(tags, Middle, file_order)

    dic = {name: value for name, value in zip(file_order, light_on)}
    top3 = hashtagTop3(dic)

    print(top3)

    return top3, tags

if __name__ == '__main__':
    id = "jjunlovee"
    hashtagChecker(id)

