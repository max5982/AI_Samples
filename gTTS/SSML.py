# Speech Synthesis Markup Language (SSML)
from google.cloud import texttospeech

client = texttospeech.TextToSpeechClient()
synthesis_input = texttospeech.SynthesisInput(
    ssml='<speak>I want to have <emphasis level="strong">apples</emphasis>.</speak>'
)

voice = texttospeech.VoiceSelectionParams(
    language_code="en-US",
    ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
)

audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
)

response = client.synthesize_speech(
    input=synthesis_input, voice=voice, audio_config=audio_config
)

with open('output.mp3', 'wb') as out:
    out.write(response.audio_content)

"""
text1 = "Wow~ amazing! I look forward to showcasing our readiness at CES 2025, and I will immediately fund this project with three million dollars."


text2 = "Incredible! [3 second pause] I'm thrilled to see this at CES 2025. Consider the project funded with three million dollars."

tts = gTTS(text1, lang='en', tld='us')
tts.save('text1.mp3')

tts = gTTS(text2, lang='en', tld='us')
tts.save('text2.mp3')
"""

