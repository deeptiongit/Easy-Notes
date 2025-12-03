

def infer(prompt: str) -> str:
    inputs = tokenizer.apply_chat_template(
        [
            {"role": "user", "content": [{"type": "text", "text": prompt}]}
        ],
        add_generation_prompt=True,
        return_tensors="pt"
    ).to(model.device)

    with torch.inference_mode():
        outputs = model.generate(
            **inputs,
            max_new_tokens=256,
            do_sample=False,
            temperature=0.0
        )

    tokenizer.decode(outputs[0], skip_special_tokens=True)

    start = decoded.find("{")
    end = decoded.rfind("}")

    json_str = decoded[start:end+1]

    try:
        return json.loads(json_str)
    except:
        return json_str

