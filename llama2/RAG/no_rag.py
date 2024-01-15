import torch
from transformers import LlamaForCausalLM, LlamaTokenizer


"""
    Args:
        ckpt_dir (str): The directory containing checkpoint files for the pretrained model.
        tokenizer_path (str): The path to the tokenizer model used for text encoding/decoding.
        temperature (float, optional): The temperature value for controlling randomness in generation.
            Defaults to 0.6.
        top_p (float, optional): The top-p sampling parameter for controlling diversity in generation.
            Defaults to 0.9.
        max_seq_len (int, optional): The maximum sequence length for input prompts. Defaults to 512.
        max_batch_size (int, optional): The maximum batch size for generating sequences. Defaults to 8.
        max_gen_len (int, optional): The maximum length of generated sequences. If None, it will be
            set to the model's max sequence length. Defaults to None.
"""

model_name = "llama-2-7b-chat-hf"
model_id = '../' + model_name


tokenizer = LlamaTokenizer.from_pretrained(model_id)
model =LlamaForCausalLM.from_pretrained(model_id, load_in_4bit=True, device_map='auto', torch_dtype='auto', cache_dir=model_id)


while True:
    user_input = input("Query: ")

    if user_input == "exit":
        break

    model_input = tokenizer(user_input, return_tensors="pt").to("cuda")

    model.eval()
    print("==============================================")
    print(f"[query]: {user_input}")
    print(f"[answer]:")

    with torch.no_grad():
        print(tokenizer.decode(model.generate(**model_input, max_new_tokens=200)[0], skip_special_tokens=True))

    print("==============================================")
    

