# Speech Synthesis Markup Language (SSML)
from google.cloud import texttospeech

# How to use
# <break time="200ms"/>  (e.g. "3s" or "250ms")
# <break strength="weak"/>  "x-weak", weak", "medium", "strong", and "x-strong"
# <say-as interpret-as='currency' language='en-US'>$42.01</say-as>
# <say-as interpret-as="characters">can</say-as> -----> The following example is spoken as "C A N"
# <p><s>This is sentence one.</s><s>This is sentence two.</s></p>
# <emphasis level="moderate">aaa</emphasis> ------> strong / moderate / none / reduced



client = texttospeech.TextToSpeechClient()
synthesis_input = texttospeech.SynthesisInput(
    ssml='<speak> <break time=\"300ms\"/>Wow <break time=\"200ms\"/> amazing! <break time=\"300ms\"/> I look forward to showcasing our <emphasis level=\"strong\"> readiness at CES 2025,</emphasis> <break time=\"300ms\"/> and I will immediately fund this project with at least <break time=\"300ms\" strength=\"strong\"/> <emphasis level=\"strong\"> <say-as interpret-as=\"currency\" language=\"en-US\">$3000000</say-as>  </emphasis>  </speak>'
)
    #ssml='<speak>I want to have <emphasis level="strong">apples</emphasis>. do you know me? do you <break time=\"3s\"/> know <emphasis level="strong">me?</emphasis></speak>'

voice = texttospeech.VoiceSelectionParams(
    language_code="en-US",
    #name="en-US-Standard-B", # for Pat
    name="en-US-Polyglot-1",
    ssml_gender=texttospeech.SsmlVoiceGender.MALE
)

audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
)

response = client.synthesize_speech(
    input=synthesis_input, voice=voice, audio_config=audio_config
)

with open('3output.mp3', 'wb') as out:
    out.write(response.audio_content)

"""
text1 = "Wow~ amazing! I look forward to showcasing our readiness at CES 2025, and I will immediately fund this project with three million dollars."


text2 = "Incredible! [3 second pause] I'm thrilled to see this at CES 2025. Consider the project funded with three million dollars."

tts = gTTS(text1, lang='en', tld='us')
tts.save('text1.mp3')

tts = gTTS(text2, lang='en', tld='us')
tts.save('text2.mp3')
"""

