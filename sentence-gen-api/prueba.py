import ollama
response = ollama.chat(model='llama-custom', messages=[
  {
    'role': 'user',
    'content': 'Why is the sky blue?',
  },
])
print(response['message']['content'])
