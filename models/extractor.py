import re
import google.generativeai as genai
import json
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

def ai_check_red_flag(email_text):
    """
    Use Gemini AI to detect red flags in job-related emails.
    Returns dict: {"is_red_flag": true/false, "reason": "..."}
    """
    prompt = (
        "Analyze the following job application email. "
        "Tell me if it contains any signs of scam, fraud, or risky requests (such as asking for money, sensitive personal data, or suspicious offers). "
        "Reply ONLY with this JSON format:\n"
        "{\n"
        '  "is_red_flag": true/false,\n'
        '  "reason": "Brief explanation or warning if true, otherwise empty"\n'
        "}\n\n"
        f"Email:\n{email_text}"
    )
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(prompt)
    match = re.search(r'\{.*?\}', response.text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except Exception:
            return {"is_red_flag": False, "reason": ""}
    else:
        return {"is_red_flag": False, "reason": ""}

def extract_job_info(email_text):
    """
    Extract structured job application info (company, position, status) using Gemini AI,
    and detect red flags via AI model.
    Returns a dict with: company, position, status, is_red_flag, red_flag_reason
    """
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
    match = re.search(r'\{.*?\}', response.text, re.DOTALL)
    if match:
        try:
            info = json.loads(match.group(0))
        except Exception:
            info = {"company": "Unknown", "position": "Unknown", "status": "Unknown"}
    else:
        info = {"company": "Unknown", "position": "Unknown", "status": "Unknown"}

    # Use AI model to detect red flags
    red_flag_result = ai_check_red_flag(email_text)
    info["is_red_flag"] = red_flag_result["is_red_flag"]
    info["red_flag_reason"] = red_flag_result["reason"]
    return info