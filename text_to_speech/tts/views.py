from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from gtts import gTTS
from usercredits.models import *
def index(request):
    if request.method == 'POST':
        text = request.POST.get('text', '')
        lang = request.POST.get('lang', 'en')
        if (request.user == None and request.user == ""):
            return render(request , "userauth/signin.html")
        try:
            user_allowed_charecters = UserCredits.objects.get(pk = request.user.id)
        except UserCredits.DoesNotExist:
            return HttpResponse("UserCredits.DoesNotExist")
        length_of_string = len(text)
        if(length_of_string  > user_allowed_charecters):
            return HttpResponse("Limit exceeded your limit is " + str(user_allowed_charecters))
        # Generate TTS
        tts = gTTS(text, lang=lang)
        
        from io import BytesIO
        tts = gTTS(text, lang=lang)
        speech_file = BytesIO()
        tts.write_to_fp(speech_file)
        speech_file.seek(0)

        # Send the file directly to the client
        response = HttpResponse(speech_file.read(), content_type='audio/mpeg')
        response['Content-Disposition'] = 'attachment; filename="output.mp3"'
        return response


    return render(request, 'tts/index.html')