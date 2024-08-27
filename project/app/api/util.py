import httpx

SPELLCHECKER_API_URL = "https://speller.yandex.net/services/spellservice.json/checkText"


async def check_spelling(text: str) -> str:
    spell_check_data = {
        "text": text,
        "lang": "ru"
    }

    # Make an async request to the spell checker API
    async with httpx.AsyncClient() as client:
        response = await client.post(SPELLCHECKER_API_URL, data=spell_check_data)

    if response.status_code == 200:
        corrected_text = text
        spell_check_results = response.json()

        # Apply corrections to the text
        for error in spell_check_results:
            word = error['word']
            suggestions = error.get('s')
            if suggestions:
                corrected_word = suggestions[0]  # Taking the first suggestion
                corrected_text = corrected_text.replace(word, corrected_word)

        return corrected_text
    else:
        # Handle API errors (optional)
        raise Exception("Failed to perform spell check")
