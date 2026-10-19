# Local LLM Evaluation

Initial local-model screening for the Chargeback Agent.

| Model | Instruction following | Multi-step reasoning | Stopping behavior |
| --- | --- | --- | --- |
| Llama 3.2 3B | Good | Weak | Good |
| Qwen3 4B | Weak | Stronger | Poor; severe overthinking |
| Phi-4 Mini | Weak | Weak | Fast |
| Qwen3 4B Instruct | Mixed | Can solve after prompting | Poor; repetitive |
| Granite 4 3B | Good output control | Weak | Good |
| Qwen3.5 4B | Mixed | Can reach correct solution | Poor; may exhaust generation before final answer |

Current conclusion: no tested local model yet satisfies the combined requirements of reliable reasoning, strict instruction following, tool-oriented control, and robust stopping behavior.
