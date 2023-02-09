
def activate(request, namespace=None, namespace_id=None):
    try:
        del request.session["namespace"]
    except:
        pass
    request.session["namespace"] = namespace
    if namespace_id is not None:
        request.session["namespace_id"] = namespace_id
    return 

def clear(request):
    activate(request, namespace=None)