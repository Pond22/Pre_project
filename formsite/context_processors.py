from django.template import Library
from formsite.templatetags import custom_filters

def custom_filters_processor(request):
    return {'custom_filters': custom_filters}
