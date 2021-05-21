import os
from django.http import HttpResponse, JsonResponse, Http404


def download(request):
    if request.method == "GET":
        filepath = request.GET.get('filepath')
        with open(filepath, 'rb') as f:
            try:
                response = HttpResponse(f)
                response['content_type'] = "application/octet-stream"
                response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(filepath)
                return response
            except Exception:
                raise Http404