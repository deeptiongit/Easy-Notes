import os
import re
import json
from click import prompt
import torch
import pandas as pd
from tqdm import tqdm
from transformers import AutoTokenizer, AutoModelForCausalLM



BASE_DIR = os.path.dirname(__file__)
INPUT_FOLDER = os.path.join(BASE_DIR, "invoices")
OUTPUT_FILE = os.path.join(BASE_DIR, "results.csv")
model = "microsoft/Phi-3-mini-128k-instruct"

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


tokenizer = AutoTokenizer.from_pretrained(model)
model = AutoModelForCausalLM.from_pretrained(
    model,
    device_map="auto",
    dtype=torch.float16,
    low_cpu_mem_usage=True,
    offload_folder="./offload")

model.config.use_cache = True
model.eval()




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
    assert isinstance(prompt, str)
    assert len(prompt.strip()) > 0
    inputs = tokenizer(
    prompt,
    return_tensors="pt",
    truncation=True,
    max_length=512,
    ).to(model.device)

    with torch.inference_mode():
        outputs = model.generate(
            **inputs,
            max_new_tokens=200,
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


