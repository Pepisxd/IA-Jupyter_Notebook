from transformers import pipeline, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("modelo_finetune_tinyllama")
generator = pipeline(
    "text-generation",
    model="modelo_finetune_tinyllama",
    tokenizer=tokenizer,
    device=0
)

prompt = "Genera un ejercicio de dificultad Avanzado sobre Recursión."
output = generator(
    prompt,
    max_new_tokens=80,
    temperature=0.7,
    top_p=0.9,
    do_sample=True,
    eos_token_id=tokenizer.eos_token_id
)

print("\n💡 Ejercicio generado:")

print(output[0]['generated_text'])
