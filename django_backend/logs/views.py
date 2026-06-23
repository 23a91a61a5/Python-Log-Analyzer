from django.http import JsonResponse
from django.shortcuts import render
from analyzer.core import analyze_log


def analyze_view(request):
    # JSON API endpoint
    result = analyze_log("Hello from Django")
    return JsonResponse(result)


def dashboard(request):
    context = {}
    if request.method == "POST":
        log_file = request.FILES.get("logfile")
        if log_file:
            content = log_file.read().decode("utf-8", errors="ignore")
            result = analyze_log(content)
            context["result"] = result
    return render(request, "logs/dashboard.html", context)