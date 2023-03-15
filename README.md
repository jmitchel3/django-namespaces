# django-namespaces

Use namespaces in requests using Django.


## Motivation

Google Cloud has an interest feature for namespacing projects. Namespacing can enable assets to be isolated from each other without needing to leverage subdomains and/or multiple databases (although you can use those too).


## Installation

Use a virtual environment whenever using Python packages. The built-in [venv](https://docs.python.org/3/library/venv.html) module is great.
```
python3 -m venv venv
source venv/bin/activate
$(venv) python -m pip install django-namespaces --upgrade
```

## Configure your Django Project

### Create a Django Project
```
$(venv) mkdir -p src && cd src
$(venv) django-admin startproject cfehome .
```

### Installed Apps
Add `django_namespaces` to your `INSTALLED_APPS` in `settings.py`:
```python
INSTALLED_APPS = [
    ...
    'django_namespaces',
]
```

### Update Middelware
Update `MIDDLEWARE` in `settings.py` to include `NamespaceMiddleware`:
```python
MIDDLEWARE = [
    ...
    'django_namespaces.middleware.NamespaceMiddleware',
]
```


This gives us access to the `request.namespace` object in our views.


## Basic Usage

```python
import django_namespaces
django_namespaces.activate("hello-world")
```
This will add a namespace to the request object.

```python

def my_hello_world_view(request):
    print(request.namespace) # <Namespace: hello-world>
    print(request.namespace.value) # hello-world
    return HttpResponse("Hello World") 
```


### Optional Views
Using views are optional. You can also use the `activate` function to activate a namespace.

#### Update URLconf
Update `urls.py` to include `namespaces.urls`:
```python
urlpatterns = [
    ...
    path('namespaces/', include('django_namespaces.urls')),
]
```


#### Create a Namespace
Create a namespace by visiting `http://localhost:8000/namespaces/create/` and filling out the form.


#### Activate a Namespace
Activate a namespace by visiting `http://localhost:8000/namespaces/` and hitting `activate` on your newly created namespace.

You can also use:


#### Update URLconf


