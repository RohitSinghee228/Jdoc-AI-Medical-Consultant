import json
import ollama
from django.shortcuts import get_object_or_404
from .models import Diagnosis, Patient  # Assuming models are in the same app
import time
import re
# Initialize an empty messages list to keep the conversation history
messages = []

def generate_response(prompt, user):
    # Append the user message to the conversation history
    json_detected = False
    messages.append({'role': 'user', 'content': prompt})
    
    # Stream the response from Ollama
    stream = ollama.chat(
        model='jdoc',
        messages=messages,
        stream=False
    )
    
    # Initialize a variable to collect the full AI response
    ai_response = ""
    json_data = None  # Variable to store extracted JSON if present
    chunks = []  # List to collect response chunks for streaming
    
    # Collect the full response or stream based on JSON presence
    # for chunk in stream:
    #     message_content = chunk['message']['content']
    #     ai_response += message_content  # Collecting full response
        
    #     # If no JSON data detected yet, continue streaming
    #     chunks.append(message_content)

    ai_response = stream['message']['content']
    # Check if the final AI response contains JSON format data
    try:
        # Attempt to extract JSON data between curly braces
        print(ai_response)
        # Save ai response to file

        with open('ai_response.txt', 'w') as file:
            file.write(ai_response)
        
        with open('ai_response.txt', 'r') as file:
            data_json = file.read()
        match = re.search(r"\{(.*)\}", data_json, re.DOTALL)

        print("match", match)
        if match:
            json_content = match.group(0)
            print("loading json content")
            json_data = json.loads(json_content)
            print("json content detected",json_content)
            print("Json data detected")
        else:
            print("No JSON content found.")
                    # Remove JSON part from the final response message
    except json.JSONDecodeError as ex:
        # If JSON parsing fails, json_data remains None
        print("EXCEPTION",ex)

    # Append the modified AI response (without JSON) to the conversation history
    messages.append({'role': 'assistant', 'content': ai_response})

    # If JSON data is found, save the diagnosis and return the confirmation message
    if json_data:
        # Retrieve the patient associated with the current user
        patient = get_object_or_404(Patient, user_id=user.id)
        
        # Create a Diagnosis entry from the JSON data
        Diagnosis.create_diagnosis_from_json(patient, json_data)
        
        # Yield the confirmation message once diagnosis is saved
        yield "Your diagnosis has been recorded and will be reviewed by our senior doctor soon."
    else:
        # If no JSON data, stream the chunks as the AI response
        for chunk in ai_response.split():
            chunk = chunk + " "
            time.sleep(.1)
            yield chunk  # Streaming AI response in chunks

