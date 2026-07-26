from vllm import LLM

prompts = ["Hello, my name is", "The capital of France is"]  # Sample prompts.
llm = LLM(model="Qwen3/Qwen3-8b")  # Create an LLM.
outputs = llm.generate(prompts)  # Generate texts from the prompts.