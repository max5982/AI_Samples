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
import argparse

from transformers import AutoModelForCausalLM, AutoTokenizer
from ipex_llm import optimize_model
from ipex_llm.optimize import low_memory_init, load_low_bit

from time import time

# you could tune the prompt based on your own model,
# here the prompt tuning refers to https://huggingface.co/microsoft/Phi-3-mini-4k-instruct#chat-format
PHI3_PROMPT_FORMAT = "<|user|>\n{prompt}<|end|>\n<|assistant|>"

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Predict Tokens using `generate()` API for phi-3 model')
    parser.add_argument('--repo-id-or-model-path', type=str, default="microsoft/Phi-3-mini-4k-instruct",
                        help='The huggingface repo id for the phi-3 model to be downloaded'
                             ', or the path to the huggingface checkpoint folder')
    parser.add_argument('--prompt', type=str, default="What is AI?",
                        help='Prompt to infer')
    parser.add_argument('--low-bit', type=str, default="sym_int4",
                        choices=['sym_int4', 'asym_int4', 'sym_int5', 'asym_int5', 'sym_int8'],
                        help='The quantization type the model will convert to.')
    parser.add_argument('--save-path', type=str, default=None,
                        help='The path to save the low-bit model.')
    parser.add_argument('--load-path', type=str, default=None,
                        help='The path to load the low-bit model.')
    parser.add_argument('--n-predict', type=int, default=32,
                        help='Max tokens to predict')

    args = parser.parse_args()
    model_path = args.repo_id_or_model_path
    low_bit = args.low_bit
    load_path = args.load_path

    # Load model
    st = time()
    if load_path:
        # Fast and low cost by loading model on meta device
        with low_memory_init():
            model = AutoModelForCausalLM.from_pretrained(load_path, torch_dtype="auto", trust_remote_code=True)
        model = load_low_bit(model, load_path)
        tokenizer = AutoTokenizer.from_pretrained(load_path)
    else:
        model = AutoModelForCausalLM.from_pretrained(model_path, trust_remote_code=True)
        model = optimize_model(model, low_bit=low_bit)
        tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)

    #model = AutoModelForCausalLM.from_pretrained(model_path,
    #                                             trust_remote_code=True,
    #                                             torch_dtype='auto',
    #                                             low_cpu_mem_usage=True,
    #                                             use_cache=True)
    print(f"model loading time = {time() - st}")

    save_path = args.save_path
    if save_path:
        model.save_low_bit(save_path)
        tokenizer.save_pretrained(save_path)
        print(f"Model and tokenizer are saved to {save_path}")

    # With only one line to enable IPEX-LLM optimization on model
    # When running LLMs on Intel iGPUs for Windows users, we recommend setting `cpu_embedding=True` in the optimize_model function.
    # This will allow the memory-intensive embedding layer to utilize the CPU instead of iGPU.
    st = time()
    # please save/load model before you run it on GPU
    model = model.to('xpu')
    print(f"model optimization time = {time() - st}")
    
    # Generate predicted tokens
    with torch.inference_mode():
        prompt = PHI3_PROMPT_FORMAT.format(prompt=args.prompt)
        input_ids = tokenizer.encode(prompt, return_tensors="pt").to('xpu')

        # ipex_llm model needs a warmup, then inference time can be accurate
        st = time()
        output = model.generate(input_ids,
                                max_new_tokens=args.n_predict)
        print(f"inference warmup time = {time() - st}")
        # start inference
        st = time()

        output = model.generate(input_ids,
                                do_sample=False,
                                max_new_tokens=args.n_predict)
        torch.xpu.synchronize()
        end = time()
        output_str = tokenizer.decode(output[0], skip_special_tokens=False)
        print(f'Inference time: {end-st} s')
        print('-'*20, 'Prompt', '-'*20)
        print(prompt)
        print('-'*20, 'Output', '-'*20)
        print(output_str)
