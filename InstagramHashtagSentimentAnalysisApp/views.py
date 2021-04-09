from django.shortcuts import render
'''
import sys
sys.path.insert(0, "/data/python/b.py")
'''

import os
import sys
sys.path.append(os.path.dirname(__file__))
import selenium_instagram as SI
import hashtag_checker as HC
import moduled_model as MM

# Create your views here.
def main(request):
    return render(request, 'main.html')


def result(request):
    return render(request, 'result.html')
'''

def result(request):
    instagram_id = request.GET['instagramID']
    SI.SeleniumInstagramCrawler(instagram_id)
    dic, tags = HC.hashtagChecker(instagram_id)

    model_result = 0
    for tag in tags:
        result = MM.sentimentPredict(tag)
        model_result += result
    # result = MM.sentimentPredict(tags)

    return render(request, 'result.html', {'instagramId':instagram_id, 'dic':dic, 'modelResult':model_result})
'''
