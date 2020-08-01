from django.shortcuts import render


#function for rendering the Homepage(index.html)
def index(request):
	return render(request,'index.html')

