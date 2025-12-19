import ollama 

#Initialise the Ollama Client
client= ollama.Client()

#Define The Model and the input prompt
model= "gemma3:1b"
prompt="What is AWS?"

#Send Query to the Model 
response= client.generate(model=model, prompt=prompt)

#Print the response from the model
print("Response from Ollama:")
print(response.response)