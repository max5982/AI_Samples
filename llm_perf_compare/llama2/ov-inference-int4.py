from transformers import AutoModelForCausalLM, AutoConfig, AutoTokenizer, LlamaTokenizer
from optimum.intel.openvino import OVModelForCausalLM
#from ov_llm_model importmodel_classes
import openvino as ov
import time

model_path = "model/llama-2-7b-chat-hf"
model_dir = "model/int4"
#device = "CPU"

ov_config = {"PERFORMANCE_HINT": "LATENCY", "NUM_STREAMS": "1", "CACHE_DIR": model_dir}
#ov_config = {"PERFORMANCE_HINT": "THROUGHPUT", "NUM_STREAMS": "10", "CACHE_DIR": ""}

core = ov.Core()

print(f"available device: {core.available_devices}")
for device in core.available_devices:
    print(f'')
    print(f'================================')
    print(f'================================')
    print("Inference with device: {device}")

    ov_model = OVModelForCausalLM.from_pretrained(
        model_dir,
        device=device,
        ov_config=ov_config,
        config=AutoConfig.from_pretrained(model_dir, trust_remote_code=False),
        trust_remote_code=False,
        load_in_4bit=True,
        use_cache=True,
        optimize_model=True,
    )

    tok = LlamaTokenizer.from_pretrained(model_path, trust_remote_code=True)
    #tokenizer_kwargs = {"return_token_type_ids": False}
    tokenizer_kwargs = {"add_special_tokens": False}

    input1 = "Who am I?"
    input2 = "What is pros and cons of OpenVINO?"
    input_tokens = tok(input1, return_tensors="pt", **tokenizer_kwargs)

    print(f"Model = {model_dir}")
    ov_model.to("GPU.1")

    st = time.time()
    answer = ov_model.generate(**input_tokens, max_new_tokens=256)
    end = time.time()
    output_str = tok.batch_decode(answer, skip_prompt=True, skip_special_tokens=True)[0]
    total_tokens_generated = len(tok.encode(output_str))
    print(f'Inference time: {end-st} s')
    print(f'Tokens: {total_tokens_generated}, Tokens per Second: {total_tokens_generated / (end-st)}')
    print(output_str)
    print(f'-------------------------------------------')

    input_tokens = tok(input2, return_tensors="pt", **tokenizer_kwargs)
    st = time.time()
    answer = ov_model.generate(**input_tokens, max_new_tokens=256)
    end = time.time()
    output_str = tok.batch_decode(answer, skip_prompt=True, skip_special_tokens=True)[0]
    total_tokens_generated = len(tok.encode(output_str))
    print(f'Inference time: {end-st} s')
    print(f'Tokens: {total_tokens_generated}, Tokens per Second: {total_tokens_generated / (end-st)}')
    print(output_str)
    print(f'-------------------------------------------')

