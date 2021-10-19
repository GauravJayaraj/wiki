from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render

# for forms
from django import forms

from . import util
import encyclopedia

app_name = encyclopedia

# for mardown to HTML
import markdown 

md = markdown.Markdown()

class Search(forms.Form):
    item = forms.CharField(widget=forms.TextInput(attrs={'class' : 'search', 'placeholder': 'Search'}))


def index(request):
    entries = util.list_entries()       # list of all entries

    lookingFor = []             # list of hints/possible/related entries for search result page

    if request.method == 'POST':
        form = Search(request.POST)        # get the posted object and it's data
        
        if form.is_valid():                 # check the CSRF validation (cros site request forgery)
            item = form.cleaned_data['item']

            
            if item in entries:
                page = md.convert(util.get_entry(item))
                return render(request,"encyclopedia/entry.html",{
                    "page" : page,
                    "title": item
                })

            else:                       # if searched entry not found either return the search page or redired to error page
                for i in entries:
                    if item.lower() in i.lower():
                        lookingFor.append(i)
                    
                return render(request, "encyclopedia/search.html",{
                    "searEntries":lookingFor,
                    "form": Search()
                })
        
        else:
            return render(request, "encyclopedia/index.html", {
                "entries": entries, 
                "form":form
            })

    else:           # GET request
        return render(request, "encyclopedia/index.html", {         
            "entries": entries, 
            "form":Search()  
        })


def entry(request,title):
    entries = util.list_entries()
    if title not in entries:
        return render(request, "encyclopedia/error.html",{
            "title":title,
            "message":"No such entry exits!"
        })
        
    page = util.get_entry(title)
    page_converted = md.convert(page) 

    context = {
        'page': page_converted,
        'title': title,
    }

    return render(request, "encyclopedia/entry.html", context)
    
