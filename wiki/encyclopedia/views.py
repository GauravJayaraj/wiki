from django.shortcuts import render

from . import util
import encyclopedia

app_name = encyclopedia

# for mardown to HTML
import markdown 

md = markdown.Markdown()

def index(request):
    return render(request, "encyclopedia\index.html", {
        "entries": util.list_entries()
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
    
