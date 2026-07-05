import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load local environment variables for security
load_dotenv()

def analyze_incident(raw_log_data):
    # Ensure API Key is configured before running execution blocks
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Missing critical configuration: GEMINI_API_KEY environment variable not set.")
    
    # Initialize the modern Google GenAI Client
    client = genai.Client(api_key=api_key)
    
    # Explicit architectural system rules to prevent AI hallucinations
    system_prompt = (
        "You are an elite, Senior L2 Cloud Operations Engineer working for a premier Managed Service Provider (MSP). "
        "Your task is to analyze raw text logs or customer tickets from web hosting/cloud systems. "
        "Provide a highly analytical, brief response containing exactly four parts:\n"
        "1. CATEGORY (e.g., DNS, SSL, Database, File Permissions)\n"
        "2. SEVERITY LEVEL (Low, Medium, Critical)\n"
        "3. ROOT CAUSE ANALYSIS (Technical assessment of what broke)\n"
        "4. REMEDIATION STEP (Exact commands or fixes required)\n"
        "5. CLIENT-FACING DRAFT (A polite, clear email explanation summarizing the resolution for a non-technical client)."
    )
    
    print("[⚙️] Forwarding log telemetry payloads to Gemini core processing engines...")
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=f"Please analyze this incident log:\n\n{raw_log_data}",
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.2 # Lower temperature guarantees factual, analytical consistency
        )
    )
    
    return response.text

if __name__ == "__main__":
    # Simulated high-pressure production system failure payload
    sample_incident_log = """
    [2026-07-05 08:12:44] [ERROR] [client 192.168.1.45] SEC_ERROR_EXPIRED_CERTIFICATE: TLS handshake failed. 
    Target server domain backend: production-sales-portal.com. Connection refused by system lifecycle loop.
    Nginx webstack terminated state on subprocess worker fork.
    """
    
    try:
        triage_report = analyze_incident(sample_incident_log)
        print("\n=================== GENERATED MSP INCIDENT REPORT ===================\n")
        print(triage_report)
        print("\n=====================================================================")
    except Exception as e:
        print(f"[❌] Incident analysis engine execution faulted: {e}")
