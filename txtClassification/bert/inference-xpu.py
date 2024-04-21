import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from time import time
from ipex_llm import optimize_model

#model_name = 'bert-base-uncased'
#model_name = 'roberta-base'
#model_name = 'distilbert-base-uncased'
model_name = 'distilroberta-base'
model_path = 'best_model/' + model_name
tokenizer_path = 'best_model/' + model_name
device = 'xpu'

# Load the model
model = AutoModelForSequenceClassification.from_pretrained(model_path)
model = optimize_model(model)
model = model.to(device)

# Load the tokenizer
tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)

def classify_text(text):
    # Encode the text using the tokenizer
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512).to('xpu')

    # Get the model predictions
    with torch.no_grad():
        outputs = model(**inputs)

    # Convert logits to probabilities
    probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)

    # Get the highest probability index
    predicted_label_index = probabilities.argmax(dim=-1).item()

    return predicted_label_index


text = "how to open rear trunk?"
st = time()
predicted_label = classify_text(text)
print(f"Predicted Label: {predicted_label}, time: {time()-st}")

text = "stop audio?"
st = time()
predicted_label = classify_text(text)
print(f"Predicted Label: {predicted_label}, time: {time()-st}")

while True:
    input_txt = input("input: (exit:q) ")
    if input_txt == 'q':
        break
    st = time()
    predicted_label = classify_text(input_txt)
    print(f"Predicted Label: {predicted_label}, time: {time()-st}")
