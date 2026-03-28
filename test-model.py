from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained("./model")
tokenizer = AutoTokenizer.from_pretrained("./model")