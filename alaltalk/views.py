from django.shortcuts import redirect, render


def landing_home(request):
    user = request.user
    if user.is_authenticated:
        return redirect("accounts:mypage")  
    return render(request, "landing/landing_page.html", {})
