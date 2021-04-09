from django.shortcuts import render
import os
import sys
sys.path.append(os.path.dirname(__file__))
import selenium_instagram as SI
import hashtag_checker as HC
import moduled_model as MM

# Create your views here.
def main(request):
    return render(request, 'main.html')

'''
def result(request):
    return render(request, 'result.html')
'''

def result(request):
    instagram_id = request.GET['instagramID']
    SI.SeleniumInstagramCrawler(instagram_id)
    top3, tags = HC.hashtagChecker(instagram_id)

    result_emo = MM.startModel(tags)

    return render(request, 'result.html', {'instagramId':instagram_id, 'top1Tag':top3[0],'top2Tag':top3[1],'top3Tag':top3[2], 'resultEmo':result_emo})

