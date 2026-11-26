from backend.llm.groq_client import test_groq_connection

try:
    result = test_groq_connection()
    print("Groq response:", result)

except Exception as error:
    print("Groq connection failed:", error)
