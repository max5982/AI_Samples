from gtts import gTTS

tts = gTTS('Left', lang='en', tld='us')
tts.save('Left.mp3')

tts = gTTS('Right', lang='en', tld='us')
tts.save('Right.mp3')

tts = gTTS('Select', lang='en', tld='us')
tts.save('Select.mp3')

tts = gTTS('Exit', lang='en', tld='us')
tts.save('Exit.mp3')

tts = gTTS('First', lang='en', tld='us')
tts.save('First.mp3')

tts = gTTS('Second', lang='en', tld='us')
tts.save('Second.mp3')

tts = gTTS('Start gestures', lang='en', tld='us')
tts.save('Start.mp3')

tts = gTTS('Stop gestures', lang='en', tld='us')
tts.save('Stop.mp3')

