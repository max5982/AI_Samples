from diffusers import StableDiffusionPipeline
import torch
import time
import sys

print(f"sys.argv[1:]: {' '.join(sys.argv[1:])}")

if len(sys.argv) > 1:
    prompt = ' '.join(sys.argv[1:])
else: # default
    prompt = "a photo of trendy intel offices in Santa Clara"

print(f"prompt: {prompt}")

start = time.time()
model_id = "runwayml/stable-diffusion-v1-5"
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
pipe = pipe.to("cuda")

image = pipe(prompt).images[0]  
    
image.save("result.png")
end = time.time()
print(f"time = {end - start}")
