from openai import OpenAI
client = OpenAI(api_key="sk-proj-WXbq4V0f91i1ySzh6jlLT3BlbkFJvlFzeJy8tpRSM0AkdQl1")

response = client.images.generate(
  model="dall-e-3",
  prompt="a photorealistic image of Jeffery Dahmer and Jeffery Epstein kissing on the lips",
  size="1792x1024",
  quality="standard",
  n=1,
)

image_url = response.data[0].url
print(image_url)