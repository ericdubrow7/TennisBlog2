from flask import Blueprint, request, jsonify
import openai
import os
#from dotenv import load_dotenv

# Load environment variables from .env file
#load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Create a Blueprint for ask routes
ask_bp = Blueprint('ask', __name__)

# Define the ask_question route
@ask_bp.route('/ask', methods=['POST'])
def ask_question():
    data = request.get_json()
    user_question = data.get('question')

    # Call the OpenAI API with the user's question
    completion = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", 
             "content": user_question}
        ]
    )

    # Get the response from the API
    response = completion.choices[0].message.content
    # Send the response back to the front-end
    print(response)
    return jsonify({'response': response})