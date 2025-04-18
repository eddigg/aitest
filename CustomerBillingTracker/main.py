
from langchain.prompts import PromptTemplate
from langchain_community.llms import OpenAI
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import Optional
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

class Intent(BaseModel):
    action: str = Field(description="The type of action to perform")
    time: Optional[str] = Field(description="The time for the action, if specified")
    details: Optional[str] = Field(description="Additional details about the action")
    confidence: float = Field(default=1.0, description="Model's confidence in the prediction")

class IntentParser:
    def __init__(self):
        self.parser = PydanticOutputParser(pydantic_object=Intent)
        template = """Convert the user input into a structured intent.
        {format_instructions}
        User input: {query}
        """
        self.prompt = PromptTemplate(
            template=template,
            input_variables=["query"],
            partial_variables={"format_instructions": self.parser.get_format_instructions()}
        )
        
    def parse_intent(self, text):
        try:
            # Basic rule-based fallback when no LLM is available
            if "schedule" in text.lower():
                confidence = 0.9 if "3 pm" in text.lower() else 0.7
                return Intent(
                    action="schedule",
                    time="15:00" if "3 pm" in text.lower() else None,
                    details=text,
                    confidence=confidence
                ).dict()
            return Intent(
                action="unknown",
                details=text,
                confidence=0.5
            ).dict()
        except Exception as e:
            return {
                "error": str(e),
                "action": "error",
                "confidence": 0.0
            }

parser = IntentParser()

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"})

@app.route('/parse', methods=['POST'])
def parse_intent():
    try:
        data = request.json
        if not data or 'text' not in data:
            return jsonify({"error": "Missing text field"}), 400
        
        result = parser.parse_intent(data['text'])
        if result.get("confidence", 0) < 0.8:
            # Flag for human review
            result["needs_review"] = True
            
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
