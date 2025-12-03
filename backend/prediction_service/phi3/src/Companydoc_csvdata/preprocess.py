import os
import re
import json
import torch
import pandas as pd
from tqdm import tqdm
from peft import PeftModel
from transformers import AutoTokenizer, AutoModelForCausalLM



BASE_DIR = os.path.dirname(__file__)
INPUT_FOLDER = os.path.join(BASE_DIR, "invoices")
OUTPUT_FILE = os.path.join(BASE_DIR, "results.csv")

base_model_id = "microsoft/Phi-3-mini-128k-instruct"
adapter_path = os.path.join(BASE_DIR, "fine_tuned_model")

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"



SCHEMA1 = """
{
  "Order ID": "string",
  "Customer ID": "string",
  "Order Date": "string",
  "Customer Details": {
    "Contact Name": "string",
    "Address": "string",
    "City": "string",
    "Postal Code": "string",
    "Country": "string",
    "Phone": "string",
    "Fax": "string"
  },
  "Products": [
    {
      "Product ID": "string",
      "Product Name": "string",
      "Quantity": "string",
      "Unit Price": "string"
    }
  ],
  "Total": 0.0
}
"""

SCHEMA2 = """
{
  "Order ID": "string",
  "Shipping Details": {
    "Ship Name": "string",
    "Ship Address": "string",
    "Ship City": "string",
    "Ship Region": "string",
    "Ship Postal Code": "string",
    "Ship Country": "string"
  },
  "Order Details": {
    "Order Date": "string",
    "Shipped Date": "string"
  },
  "Products": [
    {
      "Product": "string",
      "Quantity": 0.0,
      "Unit Price": 0.0,
      "Total": 0.0
    }
  ]
}
"""



base_model = AutoModelForCausalLM.from_pretrained(base_model_id, device_map="auto")
model = PeftModel.from_pretrained(base_model, adapter_path).eval()
tokenizer = AutoTokenizer.from_pretrained(base_model_id)




def preprocess_report(ocr_text):

    prompt = f"""
You are a document extraction agent.
Use the following schemas:

Invoice Schema:
{SCHEMA1}

Shipping Schema:
{SCHEMA2}

Extract the correct JSON from this document:

{ocr_text}

Return ONLY JSON:
"""

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    with torch.inference_mode():
        outputs = model.generate(
            **inputs,
            max_new_tokens=600,
            temperature=0.0,
            do_sample=False
        )

    decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)

    start = decoded.find("{")
    end = decoded.rfind("}")

    json_text = decoded[start:end + 1]

    try:
        return json.loads(json_text)
    except:
        return {"error": json_text}


