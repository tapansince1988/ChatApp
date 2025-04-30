from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

def chatPage(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login-user")
    context = {}
    return render(request, "chat/chatPage.html", context)

class VideoUploadView(View):
    def post(self, request):
        video_file = request.FILES.get('video')
        if video_file:
            path = default_storage.save(f'videos/{video_file.name}', ContentFile(video_file.read()))
            return JsonResponse({'video_url': default_storage.url(path), 'username': request.user.username})
        return JsonResponse({'error': 'No video uploaded'}, status=400)