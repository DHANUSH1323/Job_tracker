# import google.generativeai as genai
# import json
# from config import GEMINI_API_KEY

# genai.configure(api_key=GEMINI_API_KEY)

# def extract_job_info(email_text):
#     prompt = (
#         "Extract ONLY the following as JSON from the job-related email below:\n"
#         "company: Name of the company.\n"
#         "position: Job title.\n"
#         "status: One of these - Applied, Rejected, Interview, Offer, or Other.\n"
#         "If anything is not present, reply 'Unknown'.\n"
#         "Respond ONLY with valid JSON, with NO explanation or extra text.\n"
#         "Email:\n"
#         f"{email_text}"
#     )
#     model = genai.GenerativeModel('gemini-1.5-flash')
#     response = model.generate_content(prompt)
#     try:
#         print("Gemini output:", response.text)
#         info = json.loads(response.text)
#     except Exception:
#         info = {"company": "Unknown", "position": "Unknown", "status": "Unknown"}
#     return info





import re
import google.generativeai as genai
import json
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

def extract_job_info(email_text):
    prompt = (
        "Extract ONLY the following as JSON from the job-related email below:\n"
        "company: Name of the company.\n"
        "position: Job title.\n"
        "status: One of these - Applied, Rejected, Interview, Offer, or Other.\n"
        "If anything is not present, reply 'Unknown'.\n"
        "Respond ONLY with valid JSON, with NO explanation or extra text.\n"
        "Email:\n"
        f"{email_text}"
    )
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    print("Gemini output:", response.text)  # DEBUG
    # Extract JSON from the output
    match = re.search(r'\{.*?\}', response.text, re.DOTALL)
    if match:
        try:
            info = json.loads(match.group(0))
        except Exception:
            info = {"company": "Unknown", "position": "Unknown", "status": "Unknown"}
    else:
        info = {"company": "Unknown", "position": "Unknown", "status": "Unknown"}
    return info