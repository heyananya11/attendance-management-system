import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# Load environment variables
load_dotenv()

token = os.getenv("HF_TOKEN")

if not token:
    print("ERROR: HF_TOKEN not found in .env file.")

else:
    try:
        # Connect to Hugging Face
        client = InferenceClient(
            api_key=token
        )

        print("Connecting to Hugging Face AI...")

        response = client.chat.completions.create(
            model="meta-llama/Llama-3.1-8B-Instruct",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful AI assistant "
                        "for a student attendance management system."
                    )
                },
                {
                    "role": "user",
                    "content": (
                        "Reply with exactly: "
                        "AI connection successful!"
                    )
                }
            ],
            max_tokens=50
        )

        answer = response.choices[0].message.content

        print("\nAI Response:")
        print(answer)

    except Exception as error:
        print("\nAI connection failed.")
        print("Error type:", type(error).__name__)
        print("Error details:", error)