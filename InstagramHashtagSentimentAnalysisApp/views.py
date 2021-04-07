from django.shortcuts import render

# Create your views here.
def main(request):
    return render(request, 'main.html')

def home(request):
    return render(request, 'home.html')

def new(request):
    full_text = request.GET['fulltext']

    word_list = full_text.split()

    word_d={}

    for word in word_list:
        if word in word_d:
            word_d[word]+=1
        else:
            word_d[word]=1

    return render(request, 'new.html', { 'fulltext' : full_text, 'total': len(word_list) ,
                                         'dictionary': word_d.items()})
