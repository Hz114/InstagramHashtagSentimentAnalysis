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
    instagram_id = request.GET['instagramID']
    SI.SeleniumInstagramCrawler(instagram_id)
    dic, tags = HC.hashtagChecker(instagram_id)

    print("view------------------------------------------------------------------")
    print(tags)

    result = MM.sentimentPredict(tags)

    print(result)

    return render(request, 'result.html', {'instagramId':instagram_id, 'dic':dic})
    #return render(request, 'result.html')

