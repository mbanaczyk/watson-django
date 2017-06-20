from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from .models import Environment, Collection, Google_Contact, Document
from .forms import QueryForm, ResultsForm
from . import services

def contacts(request):
    contact_list = services.get_contacts()
    #create new Contacts
    for person in contact_list:
        #first see if Contact already exists
        crn = person.get('resourceName')
        
        #displayname
        names = person.get('names', [])
        if len(names) > 0:
            name = names[0].get('displayName')
        else:
            name = "No Display Name"
            
        #emailaddress
        emailaddresses = person.get('emailAddresses', [])
        if len(emailaddresses) > 0:
            email_address = emailaddresses[0].get('value')
        else:
            email_address = ""
            
        #phonenumber
        phonenumbers = person.get('phoneNumbers', [])
        if len(phonenumbers) > 0:
            phone_no = phonenumbers[0].get('value')
        else:
            phone_no = ""
        

        try:
            gc = Google_Contact.objects.get(contact_resource_name=crn)
        except Google_Contact.DoesNotExist:
            gc = Google_Contact(contact_resource_name=crn, contact_name=name)
            
        gc.contact_name = name
        gc.contact_email = email_address
        gc.contact_phone_no = phone_no
        gc.save()
    
    alpha_contact_list = Google_Contact.objects.order_by('contact_name')
    context = {
        'alpha_contact_list': alpha_contact_list,
    }
    return render(request, 'environment/contacts.html', context)

def query(request, environment_id):
    request.session["queryText"] = None
    request.session["collections"] = None
    form = QueryForm()
    return render(request, 'environment/query.html', {'form':form, 'environ_id':environment_id})
        
def results(request, environment_id):
    
    query_text = request.session["queryText"]
    collections = request.session["collections"]
    
    if query_text == None:
        form = QueryForm(request.POST)
        if form.is_valid():
            request.session["queryText"] = form.cleaned_data['queryText']
            collections = []
            for collection in form.cleaned_data['collection']:
                collections.append(collection.collectionIDString)
        request.session["collections"] = collections
        form = ResultsForm(request.POST)
    else:
        form = ResultsForm(request.POST)
        if form.is_valid():
            request.session["queryText"] = form.cleaned_data['queryText']

    query_text = request.session["queryText"]

    environ = Environment.objects.get(pk=environment_id)
    results = services.query_environ(query_text,environ.environmentIDString,collections)

    collectionObjs = []
    for collection in collections:
        c = Collection.objects.get(collectionIDString=collection)
        collectionObjs.append(c)
        
        
    languages = []
    for result in results:
        json_field_language = result['enriched_text'].get('language')
        if json_field_language not in languages:
            languages.append(json_field_language)
            
    return render(request, 'environment/results.html', {'results':results,'form':form, 'environ_id':environment_id, 'collectionObjs' : collectionObjs, 'languages':languages}) 
            
    #return render(request, 'environment/results.html', {'results':results,'form':form, 'environ_id':environment_id, 'collections':collections})
    

def index(request):
    all_environs = Environment.objects.all()
    return render(request, 'environment/index.html', {'all_environs': all_environs,})

def env_detail(request, environment_id):
    environ = get_object_or_404(Environment, pk=environment_id)
    return render(request, 'environment/env_detail.html', {'environ': environ,})
    
# def document_detail(request, document_id):
#     doc = get_object_or_404(Document, pk=document_id)
#     #perhaps do something to the html content so it renders right
#     return render(request, 'environment/doc_detail.html', {'html_content': doc.documentContent, 'document_id' : document_id})
    
def document_detail(request, environment_id, document_id):
    doc = get_object_or_404(Document, pk=document_id)
    #perhaps do something to the html content so it renders right
    return render(request, 'environment/doc_detail.html', {'html_content': doc.documentContent, 'document_id' : document_id})
    
#NOT CURRENTLY in URLS TODO
def col_documents(request, environment_id ,collection_id):
    environ = get_object_or_404(Environment, pk=environment_id)
    collect = get_object_or_404(Collection, pk=collection_id)
    return render(request, 'environment/documents.html', {'environ': environ,'collect': collect})
    
#TODO: Add view for adding collections
#TODO: Add view for adding documents to a collection
#TODO: Add view to call forms.py QueryForm and hook up Michael's html and css
#TODO: Add view to display results of QueryForm after API is called