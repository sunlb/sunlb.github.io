from vllm import LLM, SamplingParams

# 1. 定义采样参数
sampling_params = SamplingParams(
    temperature=0.8,
    top_p=0.95,
    max_tokens=100,
)

# 2. 初始化 LLM 实例（这会加载模型）
# 提示：首次运行会自动从 Hugging Face 下载模型
llm = LLM(
    model="meta-llama/Meta-Llama-3-8B-Instruct",
    tensor_parallel_size=2,  # 使用 2 张 GPU
    gpu_memory_utilization=0.9,
)

# 3. 准备提示词列表（vLLM 为批量推理优化）
prompts = [
    "What is the capital of France?",
    "Explain the theory of relativity in simple terms.",
]

# 4. 生成文本
outputs = llm.generate(prompts, sampling_params)

# 5. 打印结果
for output in outputs:
    prompt = output.prompt
    generated_text = output.outputs[0].text
    print(f"Prompt: {prompt!r}\nGenerated text: {generated_text!r}\n")
