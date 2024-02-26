from transformers import AutoModelForCausalLM, AutoConfig
from optimum.intel.openvino import OVModelForCausalLM
import openvino as ov
from pathlib import Path
import shutil
import torch
import logging
import nncf
import gc

model_path = '/home/intel/PAE/6.Max/git/AI_Samples/llama2/llama-2-7b-chat-hf'
fp16_model_dir = 'model/fp16'
int4_model_dir = 'model/int4'
int8_model_dir = 'model/int8'

model_kwargs = {}

# FP16
ov_model = OVModelForCausalLM.from_pretrained(
    model_path, export=True, compile=False, load_in_8bit=False, **model_kwargs
)
ov_model.half()
ov_model.save_pretrained(fp16_model_dir)
del ov_model


# INT8
ov_model = OVModelForCausalLM.from_pretrained(
    model_path, export=True, compile=False, load_in_8bit=True, **model_kwargs
)
ov_model.save_pretrained(int8_model_dir)
del ov_model


# INT4
model_compression_params = {
            "mode": nncf.CompressWeightsMode.INT4_SYM,
            "group_size": 128,
            "ratio": 0.8,
        }
ov_model = ov.Core().read_model(fp16_model_dir + "/openvino_model.xml")
shutil.copy(fp16_model_dir + "/config.json", int4_model_dir + "/config.json")
compressed_model = nncf.compress_weights(ov_model, **model_compression_params)
ov.save_model(compressed_model, int4_model_dir + "/openvino_model.xml")
del ov_model
del compressed_model



