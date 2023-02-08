
def activate(request, namespace=None):
    request.session["namespace"] = namespace
    return 

def clear(request):
    activate(request, namespace=None)