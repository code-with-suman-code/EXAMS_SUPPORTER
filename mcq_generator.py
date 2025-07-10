from utils.ocr_reader import extract_text_from_pdf, extract_text_from_image

def extract_mcqs(file_bytes):
    try:
        text = extract_text_from_pdf(file_bytes)
    except:
        text = extract_text_from_image(file_bytes)

    # 👇 Dummy logic: Future me yaha se keywords match karke MCQs banao
    if "capital" in text.lower():
        return [
            {
                "question": "What is the capital of India?",
                "options": ["Mumbai", "Delhi", "Kolkata", "Chennai"],
                "answer": 1
            }
        ]
    else:
        return [
            {
                "question": "Sample Question?",
                "options": ["A", "B", "C", "D"],
                "answer": 0
            }
        ]
      
