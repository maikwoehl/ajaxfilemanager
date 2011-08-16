# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect, Http404
import ajaxfilemanager
import os
import subprocess

def findpath(path):
    above = path[::-1]
    above_int = above.find("/")
    above_pp = above.split(above[above_int])
    above_pp.remove(above_pp[0])
    output = ""
    for tail in above_pp:
        output += "/"+tail

    above = output[::-1]
    return above



def upload(request):
    return render_to_response('ajaxfilemanager/upload.html', { 'ajaxfilemanager': ajaxfilemanager  })

def index(request):
    try:
        path = request.GET['path']
        currentpath = path
    except (KeyError):
        return HttpResponseRedirect("/ajaxfilemanager/?path=/")
    else:        
        above = findpath(path)
        path = ajaxfilemanager.settings.file_directory+"/"+path
        resultdirlist = []        
        filelist = []
        filenames = []
        mimetypes = []        
        dirlist = os.listdir(path)
        for item in dirlist:
            if os.path.isfile(os.path.join(path, item)) == False:
                resultdirlist.append(item)
            else:
                filelist.append(item)
                filenames.append(item)
        
        for item in filelist:
            if ".html" in item or ".htm" in item:
                mimetypes.append("text/html")
            elif ".css" in item:
                mimetypes.append("text/css")
            elif ".js" in item:
                mimetypes.append("text/javascript")            
            else:            
                filepath = os.path.join(path, item)
                mime = subprocess.Popen(["/usr/bin/file", "-i", filepath], shell=False, stdout=subprocess.PIPE).communicate()
                mime = mime[0].split(";")
                mime = mime[0].split(":")
                mimetypes.append(mime[1])
        

        for i in range(len(filelist)):
            filelist[i] += " - ["+mimetypes[i]+"]"    
            

        return render_to_response('ajaxfilemanager/index.html', { 'ajaxfilemanager': ajaxfilemanager, 'resultdirlist': resultdirlist, 'filelist': filelist, 'currentpath': currentpath, 'path': path, 'above': above, 'filenames': filenames })

def newfolder(request, folder):
    try:
        path = request.GET['path']
    except (KeyError):
        return HttpResponse("No path exist")
    else:
        currentpath = path
        path = ajaxfilemanager.settings.file_directory+"/"+path
        if os.access(path, os.W_OK):
            os.chdir(path)
            os.mkdir(folder)
            return HttpResponse("Folder successfully created")


def rmfile(request, filename):
    try:
        path = request.GET['path']
    except (KeyError):
        return HttpResponse("No path exist")
    else:
        currentpath = path
        path = ajaxfilemanager.settings.file_directory+"/"+path
        if os.access(path, os.W_OK):
            os.chdir(path)
            os.remove(filename)
            return HttpResponse("File successfully deleted");        

def rmfolder(request, folder):
    try:
        path = request.GET['path']
    except (KeyError):
        return HttpResponse("No path exist")
    else:
        currentpath = path
        path = ajaxfilemanager.settings.file_directory+"/"+path
        if os.access(path, os.W_OK):
            os.chdir(path)
            os.rmdir(folder)
            return HttpResponse("Folder successfully deleted"); 
        

    
            

    
