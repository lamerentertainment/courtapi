import json

from django.http import JsonResponse
from .converters import als_aussage_formatieren
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def transform_text(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            input_text = data.get('text', '')
            transformed_text = als_aussage_formatieren(input_text)  # Example transformation: converting text to uppercase
            response_data = {'transformed_text': transformed_text}
            return JsonResponse(response_data)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)