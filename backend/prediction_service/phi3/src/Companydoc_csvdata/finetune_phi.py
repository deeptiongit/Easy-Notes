import os
import json
import torch
from datasets import Dataset
from trl import SFTTrainer, SFTConfig
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training

BASE_DIR = os.path.dirname(__file__)
preprocessed_data_dir = os.path.join(BASE_DIR,  "train.jsonl")
output_dir = os.path.join(BASE_DIR, "results_lora")

os.makedirs(output_dir, exist_ok=True)

model_name = "microsoft/Phi-3-mini-128k-instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name)

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    llm_int8_enable_fp32_cpu_offload=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
)

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    dtype=torch.float16,
    quantization_config=bnb_config,
    device_map="auto",
)

model = prepare_model_for_kbit_training(model)


lora_config = LoraConfig(
    r=8,
    lora_alpha=8,
    lora_dropout=0.1,
    bias="none",
    task_type="CAUSAL_LM",
    target_modules=[
    "q_proj", "k_proj", "v_proj", "o_proj",
    "gate_proj", "up_proj", "down_proj"
],
)

model = get_peft_model(model, lora_config)
model.print_trainable_parameters()

def load_dataset(jsonl_file):
    with open(jsonl_file, "r", encoding="utf-8") as f:
        data = [json.loads(line) for line in f]

    system_prompt = "Summarize the following text."
    texts = []
    for item in data:
        text = f"""### Instruction: {system_prompt}

{item['text'].strip()[:1000]}

{item['label']}
""".strip()
        texts.append(text)

    dataset = Dataset.from_dict({"text": texts})
    return dataset

train_data = load_dataset(preprocessed_data_dir)

train_params = SFTConfig(
    output_dir=output_dir,
    num_train_epochs=3,
    per_device_train_batch_size=1,
    gradient_accumulation_steps=1,
    optim="adamw_torch_fused",
    save_steps=500,
    logging_steps=50,
    learning_rate=1e-4,
    weight_decay=0.001,
    fp16=True,
    bf16=False,
    bf16_full_eval=False,
    fp16_opt_level="O2",            
    max_grad_norm=0.3,
    warmup_ratio=0.03,
    group_by_length=True,
    lr_scheduler_type="constant",
    report_to="tensorboard",
    dataset_text_field="text",
    max_length=512
)



fine_tuning = SFTTrainer(
    model=model,
    train_dataset=train_data,
    args=train_params
)

print("Starting fine-tuning...")
fine_tuning.train()

save_dir = os.path.join(BASE_DIR, "fine_tuned_model")
os.makedirs(save_dir, exist_ok=True)
model.save_pretrained(save_dir)
tokenizer.save_pretrained(save_dir)
print(f"Fine-tuned model saved at '{save_dir}'")