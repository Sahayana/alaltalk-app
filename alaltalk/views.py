from django.shortcuts import render


def landing_home(request):
    return render(request, 'landing/landing_page.html', {})
