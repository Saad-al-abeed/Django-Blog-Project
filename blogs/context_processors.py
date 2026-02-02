from .models import Category
from assignments.models import Social

def get_categories(request):
    categories = Category.objects.all()
    return dict(categories=categories)

def get_socials(request):
    socials = Social.objects.all()
    return dict(socials=socials)
