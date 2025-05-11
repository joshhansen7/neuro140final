These are four iterations of the working code for my Trump Turing Test project for Neuro 140/240.

TTTtinyllama_1 was my first functional trained model, originally meant to be a test run, producing
surprisingly solid results, some of which made it into the final survey. I was limited to TinyLlama
at the beginning because of a delay in receiving a Llama2 license.

Once I received access to Llama2, I retrofitted the existing architecture to work for the new model,
and went through a few iterations of troubleshooting and finetuning to get something working.
TTTllama2_1 was the first functional Llama2 model, but the instance crashed due to a WiFi disconnection
fairly early on, so I re-loaded the trained model weights in TTTllama2_2.py and generated most of the
final Llama2 spoofed Tweets there.

Over time, I actually found that I preferred the snappiness of the TinyLlama model—it felt more
"impressionable," taking on more of Trump's personality from the dataset, and was also less reluctant
to talk about sensitive topics—so I eventually switched back to the TinyLlama infrastructure, with 
some changes to streamline code and more thoroughly train the model. This is TTTtinyllama_2.py.
