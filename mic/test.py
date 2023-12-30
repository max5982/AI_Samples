#!/usr/bin/python3


# 오디오 시스템과 상호작용하기 위해 PyAudio 모듈을 임포트합니다
import pyaudio
# WAV 파일을 다루기 위해 wave 모듈을 임포트합니다
import wave


# 녹음에 사용될 장치의 ID를 설정합니다. Depending on your system
# You might use the index of "USB2.0 PC CAMERA: Audio (hw:2,0)"
DEVICE_ID = 5

# 녹음의 형식을 설정합니다 (이 경우 16비트 PCM)
FORMAT = pyaudio.paInt16
# 채널 수를 설정합니다 (모노의 경우 1)
CHANNELS = 1
# 샘플 레이트를 설정합니다 (Hz 단위)
#RATE = 48000
RATE = 44100
# 버퍼당 프레임 수를 설정합니다
CHUNK = 1024
# 녹음 시간을 초 단위로 설정합니다
RECORD_SECONDS = 10
# 출력 WAV 파일의 이름입니다
WAVE_OUTPUT_FILENAME = "output.wav"

# PyAudio 인스턴스를 다시 생성합니다
audio = pyaudio.PyAudio()

for i in range(audio.get_device_count()):
    dev = audio.get_device_info_by_index(i)
    print(f"Device {i}: {dev['name']}")

# 녹음을 위한 스트림을 엽니다
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
#                    input_device_index=DEVICE_ID)
print("recording...")
frames = []

# 녹음된 오디오를 청크로 녹음하여 리스트에 저장합니다
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)
print("finished recording")

# 스트림을 닫고 PyAudio 인스턴스를 종료합니다
stream.stop_stream()
stream.close()
audio.terminate()

# 쓰기 모드로 출력 WAV 파일을 엽니다
waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
# WAV 파일의 채널 수를 설정합니다
waveFile.setnchannels(CHANNELS)
# 샘플 폭을 설정합니다 (바이트 단위)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
# 프레임 레이트를 설정합니다 (Hz 단위)
waveFile.setframerate(RATE)
# 녹음된 프레임을 파일에 씁니다
waveFile.writeframes(b''.join(frames))
# WAV 파일을 닫습니다
waveFile.close()

