from django.shortcuts import render,redirect
from django.http import HttpResponse
from . import util
import markdown2
import random


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry_page(request,title):
    content=util.get_entry(title)
    if content:
        html_content = markdown2.markdown(content)
        return render(request,"encyclopedia/entry.html",{
            "title":title,
            "content":html_content
        })
    else:
        return render(request,"encyclopedia/error.html",{
            "message":"page not found"
        })

def search(request):
    query=request.GET.get("q","").strip()
    entries=util.list_entries()
    if query in entries:
        return redirect("entry_page",title=query)
    
    matches=[]
    for entry in entries:
        if query.lower() in entry.lower():
            matches.append(entry)
    
    return render(request,"encyclopedia/search_results.html",{
        "query":query,
        "matches":matches
    })


def new_page(request):
    if request.method=="POST":
        title=request.POST.get("title").strip()
        content=request.POST.get("content").strip()

        if title in util.list_entries():
            return render(request,"encyclopedia/new_page.html",{
                "error":"An entry with the title already exist",
                "title":title,
                "content":content
            })

        util.save_entry(title,content)
        return redirect("entry_page",title=title)

    return render(request,"encyclopedia/new_page.html")


def edit_page(request,title):
    if request.method=="POST":
        content=request.POST.get("content").strip()

        util.save_entry(title,content)
        return redirect("entry_page",title=title)
    
    content=util.get_entry(title)
    if content is None:
        return render(request,"encyclopedia.error.html",{
            "message":"Page not found"
        })
    return render(request,"encyclopedia/edit_page.html",{
        "title":title,
        "content":content
    })

def random_page(request):
    entries=util.list_entries()
    if entries:
        random_entry=random.choice(entries)
        return redirect("entry_page",title=random_entry)
    else:
        return render(request,"encyclopedia/error.html",{
            "message":"no page found"
        })