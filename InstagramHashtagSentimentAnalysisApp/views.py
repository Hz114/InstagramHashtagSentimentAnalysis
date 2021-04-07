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

# Create your views here.
def main(request):
    return render(request, 'main.html')

def result(request):
    instagram_id = request.GET['instagramID']
    SI.SeleniumInstagramCrawler(instagram_id)
    dic = HC.hashtagChecker(instagram_id)
    return render(request, 'result.html', {'instagramId':instagram_id, 'dic':dic})
    #return render(request, 'result.html')

