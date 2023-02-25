import os
import openai
openai.api_key = "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"

response  = openai.Image.create(
  prompt="An attractive and professional Landing Page for a Blockchain Data Analytics webpage that has a great team behind and offers analysis dashboards for wallets, DEFIs and Tokens", 
  n=2,
  size="1024x1024"
)

image_url = response['data'][0]['url']
  print(image_url)