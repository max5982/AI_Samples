from datasets import load_dataset
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification, TrainingArguments, Trainer
from transformers import TrainerCallback, TrainerState, TrainerControl


# Load the dataset
dataset = load_dataset(
    'csv',
    data_files='data/dataset.csv',
    split={
        'train': 'train[:80%]',   # Use 80% of the data for training
        'validation': 'train[80%:]'  # Use the remaining 20% for validation
    }
)

# Example of dataset structure
print(dataset['train'][0])
print(dataset['validation'][0])

#model_name = 'bert-base-uncased'
model_name = 'distilbert-base-uncased'
#model_name = 'roberta-base'
#model_name = 'distilroberta-base'

# Load a tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Tokenize the data
def tokenize_function(examples):
    return tokenizer(examples['text'], padding="max_length", truncation=True, max_length=128)  # Ensure all inputs have the same length
    #return tokenizer(examples['text'], padding="max_length", truncation=True)

tokenized_datasets = dataset.map(tokenize_function, batched=True)

# Load a pre-trained model
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=3)

# Define training arguments
training_args = TrainingArguments(
    output_dir='./results',
    evaluation_strategy="epoch",
    save_strategy="no",  # Turn off default saving
    num_train_epochs=10,
    per_device_train_batch_size=8,
    logging_dir='./logs',
    logging_steps=10,
)

class SaveBestModelCallback(TrainerCallback):
    """A custom callback to save the model when it achieves a new best loss on validation."""

    def __init__(self):
        super().__init__()
        self.best_loss = float('inf')

    def on_evaluate(self, args: TrainingArguments, state: TrainerState, control: TrainerControl, **kwargs):
        # Check if the current evaluation loss is lower than the previous best
        current_loss = kwargs.get('metrics', {}).get('eval_loss', float('inf'))
        if current_loss < self.best_loss:
            self.best_loss = current_loss
            # Save the model
            model.save_pretrained('./best_model/' + model_name)
            tokenizer.save_pretrained('./best_model/' + model_name)
            print(f"New best model saved with loss {current_loss}")

# Initialize the Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets['train'],
    eval_dataset=tokenized_datasets['validation'],
    callbacks=[SaveBestModelCallback]  # Add custom callback
)

# Train the model
trainer.train()
