# LLM
# For Gemini models, a token is equivalent to about 4 characters. 100 tokens is equal to about 60-80 English words.
#



# Context Window
The models available through the Gemini API have context windows that are measured in tokens. The context window defines how much input you can provide and how much output the model can generate.
In the following example, 
you can see that the gemini-1.0-pro-001 model has an input limit of about 30K tokens and an output limit of about 2K tokens, which means a context window of about 32K tokens.

gemini 1.5 pro 2MB
gemini 1.5 pro for high frequency tasks

model_info = genai.get_model("models/gemini-1.0-pro-001")
# Returns the "context window" for the model,
# which is the combined input and output token limits.
print(f"{model_info.input_token_limit=}")
print(f"{model_info.output_token_limit=}")
# ( input_token_limit=30720, output_token_limit=2048 )
-------------
 Gemma 2 is higher-performing and more efficient at #inference# than the first generation, with significant safety advancements built in. In fact, at 27B, it offers competitive alternatives to models more than twice its size, delivering the kind of performance that was only possible with proprietary models as recently as December. And that’s now achievable on a single NVIDIA H100 Tensor Core GPU or TPU host, significantly reducing deployment costs.

