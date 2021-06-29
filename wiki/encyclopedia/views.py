from django.shortcuts import render

from . import util
import encyclopedia

app_name = encyclopedia

# for mardown to HTML
import markdown 

md = markdown.Markdown()

def index(request):
    return render(request, "encyclopedia\templates\encyclopedia\entry.html", {
        "entries": util.list_entries()
    })


def entry(request,title):
    entries = util.list_entries()
    if title not in entries:
        return render(request, "encylopedia/error.html",{
            "title":title,
            "message":"No such entry exits!"
        })
        
    content = util.get_entry(title)     # gets markdown as it is
    content = md.convert(content)       # converts markdown to HTML

    print(content)
    context = {
        "title":title,
        "content":content,
    }

    return render(request, "encycopedia/entry.html",context)
    
