from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods, require_POST
from .detector import analyze
from .forms import ScanForm
from .models import Scan


@login_required
@require_http_methods(["GET", "POST"])
def home(request):
    form = ScanForm(request.POST if request.method == "POST" else None)
    if request.method == "POST" and form.is_valid():
        result = analyze(form.cleaned_data["message"])
        scan = Scan.objects.create(owner=request.user, **result)
        return redirect("detail", pk=scan.pk)
    return render(request, "home.html", {"form": form, "scans": Scan.objects.filter(owner=request.user)[:50]})


@login_required
@require_http_methods(["GET"])
def detail(request, pk):
    scan = get_object_or_404(Scan, pk=pk, owner=request.user)
    return render(request, "detail.html", {"scan": scan})


@login_required
@require_POST
def delete(request, pk):
    scan = get_object_or_404(Scan, pk=pk, owner=request.user)
    scan.delete()
    return redirect("home")
