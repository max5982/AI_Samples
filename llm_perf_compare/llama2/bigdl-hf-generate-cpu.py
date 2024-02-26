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

from bigdl.llm.transformers import AutoModelForCausalLM
from transformers import LlamaTokenizer

# you could tune the prompt based on your own model,
# Refer to https://huggingface.co/TheBloke/Llama-2-70B-Chat-GGML#prompt-template-llama-2-chat
LLAMA2_PROMPT_FORMAT = """
[INST] <<SYS>>
You are a helpful assistant.
<</SYS>>
{prompt}[/INST]
"""

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Predict Tokens using `generate()` API for Llama2 model')
    parser.add_argument('--repo-id-or-model-path', type=str, default="meta-llama/Llama-2-7b-chat-hf",
                        help='The huggingface repo id for the Llama2 (e.g. `meta-llama/Llama-2-7b-chat-hf` and `meta-llama/Llama-2-13b-chat-hf`) to be downloaded'
                             ', or the path to the huggingface checkpoint folder')
    parser.add_argument('--prompt', type=str, default="What is AI?",
                        help='Prompt to infer')
    parser.add_argument('--n-predict', type=int, default=32,
                        help='Max tokens to predict')

    args = parser.parse_args()
    model_path = args.repo_id_or_model_path

    # Load model in 4 bit,
    # which convert the relevant layers in the model into INT4 format
    model = AutoModelForCausalLM.from_pretrained(model_path,
                                                 load_in_4bit=True,
                                                 trust_remote_code=True)

    # Load tokenizer
    tokenizer = LlamaTokenizer.from_pretrained(model_path, trust_remote_code=True)
    
    # Generate predicted tokens
    with torch.inference_mode():
        input1 = "Who am I?"
        input2 = "What is pros and cons of OpenVINO?"

        prompt = LLAMA2_PROMPT_FORMAT.format(prompt=input1)
        input_ids = tokenizer.encode(prompt, return_tensors="pt")
        st = time.time()
        output = model.generate(input_ids,
                                max_new_tokens=args.n_predict)
        end = time.time()
        output_str = tokenizer.decode(output[0], skip_special_tokens=True)
        tok_cnt = len(tokenizer.encode(output_str))

        print('-'*20, 'Measurement', '-'*20)
        print(f'Inference time: {end-st} s')
        print(f'tok_cnt = {tok_cnt}, tok/ms = {tok_cnt / (end-st)}')
        print('-'*20, 'Output', '-'*20)
        print(output_str)

        prompt = LLAMA2_PROMPT_FORMAT.format(prompt=input2)
        input_ids = tokenizer.encode(prompt, return_tensors="pt")
        st = time.time()
        output = model.generate(input_ids,
                                max_new_tokens=args.n_predict)
        end = time.time()
        output_str = tokenizer.decode(output[0], skip_special_tokens=True)
        tok_cnt = len(tokenizer.encode(output_str))

        print('-'*20, 'Measurement', '-'*20)
        print(f'Inference time: {end-st} s')
        print(f'tok_cnt = {tok_cnt}, tok/ms = {tok_cnt / (end-st)}')
        print('-'*20, 'Output', '-'*20)
        print(output_str)
