from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import wikipedia
import openai
import os

openai.api_key = os.getenv("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")

def index(request):
    return render(request, 'history_app/index.html')

@csrf_exempt
def get_history(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        # Here you would call your AI and history logic.
        history_data = get_historical_data(latitude, longitude)

        return JsonResponse({'history': history_data})
    return JsonResponse({'error': 'Invalid request'}, status=400)

def get_historical_data(latitude, longitude):
    try:
        page = wikipedia.geosearch(latitude, longitude, results=1)
        if page:
            page_title = page[0]
            page_content = wikipedia.summary(page_title, sentences=50)
        else:
            page = wikipedia.geosearch(latitude, longitude, radius=5000, results=1)
            if page:
                page_title = page[0]
                page_content = wikipedia.summary(page_title, sentences=50)
            else:
                return "No historical data found for this location."
        prompt = f"Provide a brief historical narrative about the area described in the following text: '{page_content}'. Please keep it under 100 words."
        response = openai.Completion.create(
            engine="text-davinci-003",  # Or another suitable engine
            prompt=prompt,
            max_tokens=150,
            temperature=0.7,
        )
        return response.choices[0].text.strip()

    except wikipedia.exceptions.PageError:
        return "No historical data found for this location."
    except wikipedia.exceptions.DisambiguationError as e:
        return "Multiple results found, please be more specific. " + str(e)
    except Exception as e:
        return f"An error occurred: {e}"

def get_historical_data(latitude, longitude):
    try:
        page = wikipedia.geosearch(latitude, longitude, results=1)
        if page:
            page_title = page[0]
            page_content = wikipedia.summary(page_title, sentences=50)
            return page_content
        else:
            page = wikipedia.geosearch(latitude, longitude, radius = 5000, results = 1) #5km radius
            if page:
                page_title = page[0]
                page_content = wikipedia.summary(page_title, sentences=50)
                return page_content
            else:
                return "No historical data found for this location."

    except wikipedia.exceptions.PageError:
        return "No historical data found for this location."
    except wikipedia.exceptions.DisambiguationError as e:
        return "Multiple results found, please be more specific. " + str(e)
    except Exception as e:
        return f"An error occurred: {e}"