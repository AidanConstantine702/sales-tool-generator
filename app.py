import streamlit as st
from openai import OpenAI
import json
import pdfkit
import os

# Initialize OpenAI client (for openai>=1.x)
client = OpenAI(api_key=st.secrets["openai_api_key"])

# Define company input prompts
def get_company_info():
    st.header("🚀 Sales Script & Tools Generator")

    company_name = st.text_input("Company Name")
    products_services = st.text_area("Describe your Products or Services")
    target_audience = st.text_input("Who is your target audience?")
    top_problems = st.text_area("What top 3 problems do you solve?")
    value_prop = st.text_area("What is your unique value proposition?")
    tone = st.selectbox("What tone fits your brand?", ["Friendly", "Formal", "Bold", "Consultative"])

    if st.button("Generate Sales Tools"):
        if all([company_name, products_services, target_audience, top_problems, value_prop]):
            return {
                "company_name": company_name,
                "products_services": products_services,
                "target_audience": target_audience,
                "top_problems": top_problems,
                "value_prop": value_prop,
                "tone": tone
            }
        else:
            st.warning("Please complete all fields.")
            return None
    return None

# Load persona scenarios safely
def load_personas():
    if os.path.exists("prospects.json"):
        with open("prospects.json") as f:
            return json.load(f)
    else:
        st.warning("⚠️ Warning: prospects.json not found. Continuing without personas.")
        return []

# Generate content with OpenAI v1+ client
def generate_content(prompt):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a B2B sales expert trained on Dale Carnegie, Sandler, and Challenger frameworks."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content

# Generate all deliverables
def create_deliverables(info, personas):
    persona_summary = "\n".join(
        [f"- {p['industry']} {p['persona']} with pain points: {', '.join(p['pain_points'])}" for p in personas]
    ) if personas else "No personas provided."

    prompt = f"""
You are a B2B sales strategist generating customer-facing tools in order of a standard sales timeline. Begin with outreach and end with closing steps. Make the tone human, conversational, and encouraging—avoid robotic or overly formal language.

Company Name: {info['company_name']}
Products/Services: {info['products_services']}
Target Audience: {info['target_audience']}
Top Problems: {info['top_problems']}
Value Proposition: {info['value_prop']}
Tone: {info['tone']}

Create the following sales tools in logical sales order:

1. Cold outreach email (initial prospecting)
2. Follow-up email (non-response)
3. Breakup email (final no-response email)
4. Warm intro phone script (referral or inbound inquiry)
5. Discovery call script that assumes the prospect responded positively to the cold email and agreed to a call—reference that context in tone and flow.
6. Elevator pitch (short and descriptive versions)
7. Sales presentation talking points
8. Handling objections (3–5 common concerns and responses)
9. Closing script (confirmation of deal and next steps)
10. 5-7 discovery/needs assessment questions

Use principles from Dale Carnegie (trust and empathy), Sandler (qualification and pain), and Challenger (teach, tailor, take control).
If personas are provided, tailor tone and content to those pain points:

{persona_summary}
"""
    return generate_content(prompt)

# Save deliverables to PDF
def save_to_pdf(content, filename="sales_tools.pdf"):
    html_content = f"<pre>{content}</pre>"
    pdfkit.from_string(html_content, filename)
    return filename

# Main app
def main():
    info = get_company_info()
    if info:
        st.info("Generating sales tools... Please wait ⏳")
        personas = load_personas()
        deliverables = create_deliverables(info, personas)
        st.success("✅ Sales tools generated!")
        st.text_area("Generated Sales Tools", deliverables, height=400)

        if st.button("Download as PDF"):
            filename = save_to_pdf(deliverables)
            with open(filename, "rb") as f:
                st.download_button("📥 Download PDF", f, file_name="sales_tools.pdf")

# Run app
if __name__ == "__main__":
    main()

