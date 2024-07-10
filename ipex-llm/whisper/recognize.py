#
# Copyright 2016 The BigDL Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import torch
import time
import argparse
import librosa
import soundfile as sf

from ipex_llm.transformers import AutoModelForSpeechSeq2Seq
from ipex_llm.optimize import low_memory_init, load_low_bit
from transformers import WhisperProcessor
from datasets import load_dataset


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Recognize Tokens using `generate()` API for Whisper model')
    parser.add_argument('--repo-id-or-model-path', type=str, default="openai/whisper-small",#"openai/whisper-tiny",
                        help='The huggingface repo id for the Whisper model to be downloaded'
                             ', or the path to the huggingface checkpoint folder')
    parser.add_argument('--audio-file-path', type=str, required=True,
                        help='The path to the audio file to be transcribed')
    parser.add_argument('--language', type=str, default="english",
                        help='language to be transcribed')
    parser.add_argument('--save-path', type=str, default=None,
                        help='The path to save the low-bit model.')
    parser.add_argument('--load-path', type=str, default=None,
                        help='The path to load the low-bit model.')

    args = parser.parse_args()
    model_path = args.repo_id_or_model_path
    audio_file_path = args.audio_file_path
    language = args.language
    load_path = args.load_path
    save_path = args.save_path

    # Load model in 4 bit,
    # which convert the relevant layers in the model into INT4 format
    st = time.time()
    if load_path:
        model = AutoModelForSpeechSeq2Seq.load_low_bit(load_path)
    else:
        model = AutoModelForSpeechSeq2Seq.from_pretrained(model_path,
                                                          load_in_4bit=True,
                                                          optimize_model=False,
                                                          use_cache=True)

    if save_path:
        model.save_low_bit(save_path)
        print(f"Model is saved to {save_path}")

    model.to('xpu')
    #model.config.forced_decoder_ids = None
    end = time.time()
    print(f"model loading time = {end-st} s")

    # Load processor
    processor = WhisperProcessor.from_pretrained(model_path)
    forced_decoder_ids = processor.get_decoder_prompt_ids(language=language, task="transcribe")

    # Load audio file
    audio_array, sampling_rate = librosa.load(audio_file_path, sr=None)
    if sampling_rate != 16000:
        audio_array = librosa.resample(audio_array, orig_sr=sampling_rate, target_sr=16000)
        sampling_rate = 16000

    # Generate predicted tokens
    with torch.inference_mode():
        input_features = processor(audio_array,
                                   sampling_rate=sampling_rate,
                                   return_tensors="pt").input_features.to('xpu')
        st = time.time()
        # if your selected model is capable of utilizing previous key/value attentions
        # to enhance decoding speed, but has `"use_cache": false` in its model config,
        # it is important to set `use_cache=True` explicitly in the `generate` function
        # to obtain optimal performance with IPEX-LLM INT4 optimizations
        predicted_ids = model.generate(input_features)

        end = time.time()
        output_str = processor.batch_decode(predicted_ids, skip_special_tokens=True)
        print(f'Warm-up Inference time: {end-st} s')
        print('-'*20, 'Output', '-'*20)
        print(output_str)

        st = time.time()
        # if your selected model is capable of utilizing previous key/value attentions
        # to enhance decoding speed, but has `"use_cache": false` in its model config,
        # it is important to set `use_cache=True` explicitly in the `generate` function
        # to obtain optimal performance with IPEX-LLM INT4 optimizations
        predicted_ids = model.generate(input_features)

        end = time.time()
        output_str = processor.batch_decode(predicted_ids, skip_special_tokens=True)
        print(f'Inference time: {end-st} s')
        print('-'*20, 'Output', '-'*20)
        print(output_str)
