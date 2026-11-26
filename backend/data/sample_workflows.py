
SAMPLE_WORKFLOWS = {
    "banking_customer_service": {
        "application_name": "Banking Customer Service AI",
        "business_use_case": "Handles banking queries, transaction status and payment issues.",
        "workflow_description": "Classifies customer queries, retrieves banking information, generates responses and validates them.",
        "model_name": "gpt-4o-mini",
        "expected_monthly_executions": 50000,
        "forecast_scenarios": {
            "low": {"input_multiplier": 0.75, "output_multiplier": 0.75, "calls_multiplier": 1.0},
            "expected": {"input_multiplier": 1.0, "output_multiplier": 1.0, "calls_multiplier": 1.0},
            "high": {"input_multiplier": 1.5, "output_multiplier": 1.5, "calls_multiplier": 1.25}
        },
        "agents": [
            {
                "name": "Customer Intent Classification Agent",
                "workflow_step": "Classify customer intent",
                "responsibility": "Classifies banking customer queries.",
                "system_prompt": "You are a banking intent classification agent. Identify the customer's banking query and classify its intent.",
                "representative_input": "I transferred Rs. 25,000 through NEFT yesterday, but the amount has not been credited.",
                "representative_output": "Intent: Transaction Status. Category: Fund Transfer. Priority: Normal."
            },
            {
                "name": "Banking Information Retrieval Agent",
                "workflow_step": "Retrieve relevant banking information",
                "responsibility": "Retrieves banking information and transaction details.",
                "system_prompt": "You are a banking information retrieval agent. Identify and retrieve relevant banking information.",
                "representative_input": "Customer query: NEFT transfer of Rs. 25,000 not credited. Intent: Transaction Status.",
                "representative_context": "Transaction ID: TXN10245. Status: Processing. Transfer Type: NEFT."
            },
            {
                "name": "Customer Response Generation Agent",
                "workflow_step": "Generate customer response",
                "responsibility": "Generates helpful banking customer responses.",
                "system_prompt": "You are a professional banking customer service assistant. Generate an accurate and helpful response using the customer query and banking context.",
                "representative_input": "Customer query: NEFT transfer not credited. Retrieved context: Transaction status is Processing.",
                "representative_output": "Your NEFT transaction is currently being processed. Please check again later."
            },
            {
                "name": "Response Validation Agent",
                "workflow_step": "Validate response",
                "responsibility": "Validates accuracy and compliance of banking responses.",
                "system_prompt": "You are a banking response validation agent. Check response accuracy, relevance and data privacy.",
                "representative_input": "Generated response: Your NEFT transaction is being processed. Transaction status: Processing.",
                "representative_output": "Validation: Passed. Response is relevant and does not expose sensitive information."
            }
        ],
        "representative_inputs": [
            {"customer_query": "I transferred Rs. 25,000 through NEFT yesterday, but the amount has not been credited. Can you check the status?"}
        ],
        "tools": ["Banking Knowledge Base", "Transaction Status API", "Customer Account Service", "LLM API"],
        "execution_flow": [
            "Receive customer query",
            "Classify customer intent",
            "Retrieve relevant banking information",
            "Check transaction status",
            "Generate customer response",
            "Validate response",
            "Return final response"
        ]
    },

    "ecommerce_shopping_assistant": {
        "application_name": "E-commerce Shopping Assistant",
        "business_use_case": "Helps customers discover products, compare prices, check availability and place orders.",
        "workflow_description": "Understands shopping queries, retrieves product information, recommends products and validates recommendations.",
        "model_name": "gpt-4o-mini",
        "expected_monthly_executions": 80000,
        "forecast_scenarios": {
            "low": {"input_multiplier": 0.75, "output_multiplier": 0.75, "calls_multiplier": 1.0},
            "expected": {"input_multiplier": 1.0, "output_multiplier": 1.0, "calls_multiplier": 1.0},
            "high": {"input_multiplier": 1.5, "output_multiplier": 1.5, "calls_multiplier": 1.25}
        },
        "agents": [
            {
                "name": "Shopping Intent Agent",
                "workflow_step": "Identify shopping intent",
                "responsibility": "Identifies product requirements and shopping preferences.",
                "system_prompt": "You are an e-commerce shopping intent agent. Understand the customer's product requirements, budget and preferences.",
                "representative_input": "I need wireless headphones under Rs. 5,000 with good battery life.",
                "representative_output": "Category: Headphones. Budget: Rs. 5,000. Preference: Long battery life."
            },
            {
                "name": "Product Discovery Agent",
                "workflow_step": "Retrieve product information",
                "responsibility": "Finds relevant products, prices and availability.",
                "system_prompt": "You are a product discovery agent. Identify suitable products based on customer requirements and available catalog information.",
                "representative_input": "Find wireless headphones under Rs. 5,000 with long battery life.",
                "representative_context": "Product A: Rs. 3,499, battery life 40 hours. Product B: Rs. 4,499, battery life 50 hours."
            },
            {
                "name": "Product Recommendation Agent",
                "workflow_step": "Generate product recommendations",
                "responsibility": "Recommends products based on customer preferences.",
                "system_prompt": "You are an e-commerce recommendation agent. Compare the available products and recommend the most suitable options.",
                "representative_input": "Customer budget: Rs. 5,000. Products: A at Rs. 3,499 with 40-hour battery; B at Rs. 4,499 with 50-hour battery.",
                "representative_output": "Product B is recommended for its longer battery life while remaining within the customer's budget."
            },
            {
                "name": "Recommendation Validation Agent",
                "workflow_step": "Validate product recommendations",
                "responsibility": "Checks that recommendations match customer requirements and available product data.",
                "system_prompt": "You are a recommendation validation agent. Verify product prices, availability and relevance to customer preferences.",
                "representative_input": "Recommendation: Product B at Rs. 4,499 with 50-hour battery life. Customer budget: Rs. 5,000.",
                "representative_output": "Validation: Passed. Recommendation satisfies the customer's budget and battery requirements."
            }
        ],
        "representative_inputs": [
            {"customer_query": "I need wireless headphones under Rs. 5,000 with good battery life."}
        ],
        "tools": ["Product Catalog", "Inventory API", "Pricing Service", "Recommendation Engine", "LLM API"],
        "execution_flow": [
            "Receive shopping query",
            "Identify shopping intent",
            "Retrieve product information",
            "Check product availability",
            "Generate product recommendations",
            "Validate product recommendations",
            "Return recommendations"
        ]
    },

    "insurance_claims_processing": {
        "application_name": "Insurance Claims Processing AI",
        "business_use_case": "Assists with insurance claim submission, document understanding and preliminary claim assessment.",
        "workflow_description": "Understands claim requests, extracts information from documents, evaluates claim details and generates preliminary assessment summaries.",
        "model_name": "gpt-4o-mini",
        "expected_monthly_executions": 30000,
        "forecast_scenarios": {
            "low": {"input_multiplier": 0.75, "output_multiplier": 0.75, "calls_multiplier": 1.0},
            "expected": {"input_multiplier": 1.0, "output_multiplier": 1.0, "calls_multiplier": 1.0},
            "high": {"input_multiplier": 1.5, "output_multiplier": 1.5, "calls_multiplier": 1.25}
        },
        "agents": [
            {
                "name": "Claim Understanding Agent",
                "workflow_step": "Understand claim request",
                "responsibility": "Identifies claim type and reason for submission.",
                "system_prompt": "You are an insurance claim understanding agent. Identify the claim type, incident and information required.",
                "representative_input": "My car was damaged in an accident yesterday. I want to submit an insurance claim.",
                "representative_output": "Claim Type: Motor Insurance. Incident: Vehicle Accident. Status: New Claim."
            },
            {
                "name": "Document Extraction Agent",
                "workflow_step": "Extract claim document information",
                "responsibility": "Extracts relevant information from submitted claim documents.",
                "system_prompt": "You are an insurance document extraction agent. Extract relevant policy, claimant, incident and expense details from the supplied documents.",
                "representative_input": "Extract details from a motor insurance claim form and repair estimate.",
                "representative_output": "Policy Number: POL10234. Incident Date: 25 November 2026. Estimated Repair Cost: Rs. 45,000."
            },
            {
                "name": "Claim Assessment Agent",
                "workflow_step": "Assess claim information",
                "responsibility": "Reviews extracted information against the available policy details.",
                "system_prompt": "You are an insurance claim assessment assistant. Compare claim information with the supplied policy details and identify missing information or potential issues. Do not make final approval decisions.",
                "representative_input": "Claim amount: Rs. 45,000. Policy: Active. Incident: Vehicle accident.",
                "representative_output": "Preliminary assessment: Claim information is available for further review. Human approval is required."
            },
            {
                "name": "Claim Summary Agent",
                "workflow_step": "Generate claim assessment summary",
                "responsibility": "Generates a concise summary of the preliminary claim assessment.",
                "system_prompt": "You are an insurance claim summary agent. Generate a clear summary of the claim details, extracted information and outstanding requirements.",
                "representative_input": "Motor claim, estimated repair cost Rs. 45,000, policy active, human review pending.",
                "representative_output": "Claim received successfully. Preliminary information is available and the claim is pending further review."
            }
        ],
        "representative_inputs": [
            {"customer_query": "My car was damaged in an accident yesterday. I want to submit an insurance claim."}
        ],
        "tools": ["Document Processing Service", "OCR Engine", "Policy Database", "Claims Management API", "LLM API"],
        "execution_flow": [
            "Receive claim request",
            "Understand claim request",
            "Extract claim document information",
            "Verify policy information",
            "Assess claim information",
            "Generate claim assessment summary",
            "Return preliminary assessment"
        ]
    },

    "it_helpdesk_assistant": {
        "application_name": "IT Helpdesk AI Assistant",
        "business_use_case": "Resolves employee IT support queries, diagnoses common issues and recommends troubleshooting steps.",
        "workflow_description": "Understands employee issues, retrieves troubleshooting information, generates resolution steps and validates the response.",
        "model_name": "gpt-4o-mini",
        "expected_monthly_executions": 60000,
        "forecast_scenarios": {
            "low": {"input_multiplier": 0.75, "output_multiplier": 0.75, "calls_multiplier": 1.0},
            "expected": {"input_multiplier": 1.0, "output_multiplier": 1.0, "calls_multiplier": 1.0},
            "high": {"input_multiplier": 1.5, "output_multiplier": 1.5, "calls_multiplier": 1.25}
        },
        "agents": [
            {
                "name": "Issue Classification Agent",
                "workflow_step": "Classify IT support issue",
                "responsibility": "Classifies IT support issues by category and urgency.",
                "system_prompt": "You are an IT helpdesk classification agent. Identify the employee's issue, category and priority.",
                "representative_input": "I cannot connect to the office VPN. It keeps showing authentication failed.",
                "representative_output": "Category: Network Access. Issue: VPN Authentication. Priority: Medium."
            },
            {
                "name": "Troubleshooting Retrieval Agent",
                "workflow_step": "Retrieve troubleshooting information",
                "responsibility": "Retrieves relevant troubleshooting instructions from the IT knowledge base.",
                "system_prompt": "You are an IT troubleshooting retrieval agent. Identify the relevant support documentation and troubleshooting procedures.",
                "representative_input": "Issue: VPN authentication failed. Retrieve relevant VPN troubleshooting guidance.",
                "representative_context": "Check network connectivity, verify credentials, confirm MFA and restart the VPN client."
            },
            {
                "name": "Resolution Generation Agent",
                "workflow_step": "Generate troubleshooting solution",
                "responsibility": "Creates step-by-step troubleshooting instructions.",
                "system_prompt": "You are an IT helpdesk assistant. Generate clear, safe and practical troubleshooting steps using the supplied knowledge base information.",
                "representative_input": "Employee cannot connect to VPN. Suggested checks: credentials, MFA, network connectivity and VPN client.",
                "representative_output": "Please verify your credentials, complete MFA authentication, check your network connection and restart the VPN client."
            },
            {
                "name": "Ticket Summary Agent",
                "workflow_step": "Generate support ticket summary",
                "responsibility": "Summarizes the issue and suggested resolution for ticket records.",
                "system_prompt": "You are an IT support ticket summarization agent. Create a concise ticket summary containing the issue, troubleshooting performed and current status.",
                "representative_input": "Employee reported VPN authentication failure. Troubleshooting guidance has been provided.",
                "representative_output": "Issue: VPN authentication failure. Suggested resolution: Verify credentials, MFA and connectivity. Status: Awaiting employee confirmation."
            }
        ],
        "representative_inputs": [
            {"customer_query": "I cannot connect to the office VPN. It keeps showing authentication failed."}
        ],
        "tools": ["IT Knowledge Base", "Ticket Management System", "Identity Management API", "Network Monitoring", "LLM API"],
        "execution_flow": [
            "Receive employee support query",
            "Classify IT support issue",
            "Retrieve troubleshooting information",
            "Check system status",
            "Generate troubleshooting solution",
            "Generate support ticket summary",
            "Return resolution to employee"
        ]
    }
}
