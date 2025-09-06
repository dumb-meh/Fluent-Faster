from fastapi import APIRouter, HTTPException, Body
import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

router = APIRouter()
load_dotenv()

@router.post("/regenerate_sentence")
async def regenerate_sentence(request_data: str = Body(..., media_type="text/plain")):
    try:
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        model = genai.GenerativeModel('gemini-2.0-flash-exp')

        prompt = (
            "You will be given a sentence in a foreign language.\n"
            "Your task is to rewrite the sentence to make it more advanced or complex, and then provide an English translation of the new version.\n"
            "Respond ONLY with a valid JSON object using this exact structure:\n"
            '{ "foreign": "New sentence in original language", "english": "Translation in English" }'
        )

        full_prompt = f"{prompt}\n\nInput: {request_data}"
        response = model.generate_content(full_prompt)

        # Clean up output from code fences like ```json ... ```
        output = response.text.strip()
        if output.startswith("```"):
            # Remove Markdown code fence
            output = output.strip("`")  # Removes all backticks
            lines = output.splitlines()
            if lines[0].startswith("json"):
                lines = lines[1:]  # Remove the "json" language identifier
            output = "\n".join(lines).strip()

        # Attempt to parse cleaned JSON
        try:
            response_json = json.loads(output)
        except json.JSONDecodeError:
            raise HTTPException(status_code=500, detail=f"Could not parse model output as JSON: {output}")

        return response_json

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
