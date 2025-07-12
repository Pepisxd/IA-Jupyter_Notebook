from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer, DataCollatorForLanguageModeling
from peft import get_peft_model, LoraConfig, TaskType
import torch

MODEL_ID = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
DATA_PATH = "dataset.json"

# Cargar tokenizer y modelo base
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    device_map="auto",
    load_in_8bit=True,
    torch_dtype=torch.float16
)

# Dataset
dataset = Dataset.from_json(DATA_PATH)

def tokenize(example):
    texto = f"{example['prompt']}\n{example['completion']}{tokenizer.eos_token}"
    return tokenizer(texto, truncation=True, padding="max_length", max_length=512)


tokenized_dataset = dataset.map(tokenize)

# Configurar LoRA
lora_config = LoraConfig(
    r=8,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type=TaskType.CAUSAL_LM,
)

model = get_peft_model(model, lora_config)

# Argumentos de entrenamiento
training_args = TrainingArguments(
    output_dir="./tinyllama-lora",
    per_device_train_batch_size=4,
    gradient_accumulation_steps=2,
    num_train_epochs=3,
    learning_rate=2e-4,
    fp16=True,
    logging_steps=10,
    save_strategy="no"
)

# Entrenador
trainer = Trainer(
    model=model,
    train_dataset=tokenized_dataset,
    tokenizer=tokenizer,
    args=training_args,
    data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False)
)

trainer.train()

# Guardar modelo ajustado
model.save_pretrained("modelo_finetune_tinyllama")
tokenizer.save_pretrained("modelo_finetune_tinyllama")
