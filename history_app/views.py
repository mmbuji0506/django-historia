from django.shortcuts import render
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import HistoricalEvent
from urllib.parse import quote_plus
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
        try:
            data = json.loads(request.body)
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            search_query = data.get('search_query') #get the search query.

            print(f"received latitude: {latitude}, longitude: {longitude}")

            history_data = get_historical_data(latitude, longitude)

            # Save to database
            HistoricalEvent.objects.create(
                latitude=latitude,
                longitude=longitude,
                event_description=history_data,
                search_query = search_query, #save the search query.
            )

            return JsonResponse({'history': history_data})
        except Exception as e:
            print(f"error in get_history: {e}")
            return JsonResponse({'error': 'Invalid request'}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def get_historical_data(latitude, longitude):
    try:
        page = wikipedia.geosearch(latitude, longitude, results=1)
        if page:
            page_title = page[0]
            page_content = wikipedia.summary(page_title, sentences=100)
            try:
                images = wikipedia.page(page_title).images
                image_urls = [img for img in images if img.lower().endswith(('.jpg', '.jpeg', '.png'))][:3]
            except wikipedia.exceptions.PageError:
                image_urls = []
        else:
            page = wikipedia.geosearch(latitude, longitude, radius=5000, results=1)
            if page:
                page_title = page[0]
                page_content = wikipedia.summary(page_title, sentences=100)
                try:
                    images = wikipedia.page(page_title).images
                    image_urls = [img for img in images if img.lower().endswith(('.jpg', '.jpeg', '.png'))][:3]
                except wikipedia.exceptions.PageError:
                    image_urls = []
            else:
                return "<h2>Historical Narrative:</h2><p>No historical data found for this location.</p>"
        prompt = f"Provide a brief historical narrative about the area described in the following text: '{page_content}'. Please keep it under 100 words."
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150,
            temperature=0.7,
        )
        narrative = response.choices[0].text.strip()
        image_html = "".join([f'<img src="{url}" alt="Historical Image" style="max-width: 200px; margin: 10px;">' for url in image_urls])

        # YouTube video embed (basic search)
        youtube_query = quote_plus(page_title + " history")  # URL encode the search query
        youtube_embed = f'<iframe width="560" height="315" src="https://www.youtube.com/embed?listType=search&list={youtube_query}" frameborder="0" allowfullscreen></iframe>'

        return f"<h2>Historical Narrative:</h2><p>{narrative}</p>{image_html}<br>{youtube_embed}"

    except wikipedia.exceptions.PageError:
        return "<h2>Historical Narrative:</h2><p>No historical data found for this location.</p>"
    except wikipedia.exceptions.DisambiguationError as e:
        return f"<h2>Historical Narrative:</h2><p>Multiple results found, please be more specific. {e}</p>"
    except Exception as e:
        return f"<h2>Historical Narrative:</h2><p>An error occurred: {e}</p>"

def get_historical_data(latitude, longitude):
    try:
        page = wikipedia.geosearch(latitude, longitude, results=1)
        if page:
            page_title = page[0]
            page_content = wikipedia.summary(page_title, sentences=100)
            return page_content
        else:
            page = wikipedia.geosearch(latitude, longitude, radius = 5000, results = 1) #5km radius
            if page:
                page_title = page[0]
                page_content = wikipedia.summary(page_title, sentences=100)
                return page_content
            else:
                return "No historical data found for this location."

    except wikipedia.exceptions.PageError:
        return "No historical data found for this location."
    except wikipedia.exceptions.DisambiguationError as e:
        return "Multiple results found, please be more specific. " + str(e)
    except Exception as e:
        return f"An error occurred: {e}"