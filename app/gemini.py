import google.generativeai as genai
genai.configure(api_key="YOUR_API_KEY")
model = genai.GenerativeModel("gemini-pro")
response = model.generate_content("Write a catchy title for a mountain bike listing")
print(response.text)
