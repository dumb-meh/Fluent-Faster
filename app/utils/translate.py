from fastapi import APIRouter, HTTPException, Form

router = APIRouter()

@router.post("/translate")
async def translate_text(
    text: str = Form(...),
    language: str = Form(...)
):
    try:
        prompt = (
            f"You are a translation assistant.\n"
            f"Translate the following sentence to {language}.\n"
            f"Return ONLY the translation in JSON format like this:\n"
            f'{{"translated": "<translated sentence>"}}'
        )

        content = f"Translate this: {text}"

        completion = self.client.chat.completions.create(
            model="gemini-2.5-flash",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": content}
            ],
            temperature=0.5
        )
        response_text = completion.choices[0].message.content

        import json
        response_json = json.loads(response_text)

        return response_json

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
