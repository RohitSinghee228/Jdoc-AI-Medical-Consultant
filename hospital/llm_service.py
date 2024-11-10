import requests
import json

class OllamaService:
    @staticmethod
    def get_symptom_analysis(symptoms):
        """
        Use Ollama to analyze symptoms and generate medical insights
        """
        prompt = f"""
        You are a medical AI assistant. Analyze the following symptoms and provide:
        1. Possible diseases
        2. Recommended initial medicines
        3. Severity assessment

        Symptoms: {symptoms}

        Response Format (STRICT JSON):
        {{
            "possible_diseases": ["Disease1", "Disease2"],
            "recommended_medicines": [
                {{
                    "name": "Medicine Name",
                    "dosage": "Dosage instructions",
                    "purpose": "Why prescribed"
                }}
            ],
            "severity": "Low/Medium/High",
            "additional_notes": "Any important medical advice"
        }}
        """
        
        try:
            response = requests.post('http://localhost:11434/api/chat', 
                json={
                    'model': 'llama2',
                    'messages': [
                        {
                            'role': 'user',
                            'content': prompt
                        }
                    ],
                    'format': 'json'
                })
            
            # Process the response
            json_resp = response.json()
            
            # Parse the JSON response
            return json_resp['messages'][0]['content']
        except Exception as e:
            print(f"LLM Error: {e}")
            return None