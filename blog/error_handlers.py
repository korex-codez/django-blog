from django.shortcuts import render
from django.http import JsonResponse

def handler404(request, exception):
    """Custom 404 error handler"""
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'error': 'Not Found'}, status=404)
    return render(request, 'blog/404.html', status=404)

def handler500(request):
    """Custom 500 error handler"""
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'error': 'Internal Server Error'}, status=500)
    return render(request, 'blog/500.html', status=500)

def handler403(request, exception):
    """Custom 403 error handler"""
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'error': 'Forbidden'}, status=403)
    return render(request, 'blog/403.html', status=403)

def handler400(request, exception):
    """Custom 400 error handler"""
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'error': 'Bad Request'}, status=400)
    return render(request, 'blog/400.html', status=400)