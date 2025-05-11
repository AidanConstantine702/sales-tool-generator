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

    advanced = {}
    with st.expander("🔧 Advanced Setup (Optional)"):
        advanced["action_goal"] = st.text_input("What action do you want the prospect to take after the first email?")
        advanced["top_objection"] = st.text_input("What's the #1 reason people hesitate to buy from you?")
        advanced["customer_quote"] = st.text_area("What do your happiest customers say about working with you?")
        advanced["delivery_method"] = st.selectbox("How do you deliver your product or service?", ["Online", "In-person", "Phone call", "Hybrid"])
        advanced["b2b_or_b2c"] = st.radio("Do you sell to individuals or companies?", ["B2B", "B2C"])
        advanced["sales_cycle"] = st.selectbox("How long is your typical sales cycle?", ["Under a week", "1–4 weeks", "1–3 months", "Longer"])
        advanced["competitor_edge"] = st.text_input("What makes you better than your competitors?")
        advanced["fallback_rebuttal"] = st.text_input("What do you say when someone says 'We already use something for this'?")
        advanced["conversation_style"] = st.selectbox("Preferred conversation style?", ["Conversational", "Professional", "Assertive", "Casual"])
        advanced["comfort_level"] = st.slider("How comfortable are you speaking with leads?", 0, 10, 5)

    if st.button("Generate Sales Tools"):
        if all([company_name, products_services, target_audience, top_problems, value_prop]):
            return {
                "company_name": company_name,
                "products_services": products_services,
                "target_audience": target_audience,
                "top_problems": top_problems,
                "value_prop": value_prop,
                "tone": tone,
                "advanced": advanced
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
You are a B2B sales strategist generating a complete sales toolkit, including detailed scripts and a step-by-step walkthrough. Assume the user has little sales experience but high motivation. Your goal is to guide them from the first cold email to a closed deal with practical tools and brief educational guidance along the way.

Company Name: {info['company_name']}
Products/Services: {info['products_services']}
Target Audience: {info['target_audience']}
Top Problems: {info['top_problems']}
Value Proposition: {info['value_prop']}
Tone: {info['tone']}

Create a full set of sales tools in this order, with each section containing:
- A script or template (for email or call)
- A short explanation of when and how to use it
- 1–2 quick tips for using it well

Sales toolkit should include:
1. Cold outreach email (initial prospecting)
2. Follow-up email (if no response)
3. Breakup email (final message in thread)
4. Warm intro phone script (for referrals/inbound interest)
5. Discovery call script (assuming prospect replied positively to the email — acknowledge the email connection)
6. Elevator pitch (one short, one descriptive)
7. Sales presentation talking points
8. Objection handling (list 3–5 common objections with responses)
9. Closing script (language for confirming the sale and outlining next steps)
10. 5–7 discovery/needs assessment questions

Additionally, include a high-level step-by-step walkthrough of the sales journey:
- What happens between each stage
- What to look out for
- What mindset to keep

Use Dale Carnegie (trust & empathy), Sandler (qualify & diagnose), and Challenger (insight & control) principles throughout. Keep tone helpful, human, and encouraging.
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
        st.markdown("""
## 📘 Your Sales Toolkit
Below is your step-by-step sales journey. Follow the stages in order. Look for:
- **🧠 Explanation**: Why this step matters
- **✅ Script**: What to say or send
- **💡 Tips**: How to make it more effective

---
""")

        st.markdown(deliverables, unsafe_allow_html=True)

        if st.button("Download as PDF"):
            filename = save_to_pdf(deliverables)
            with open(filename, "rb") as f:
                st.download_button("📥 Download PDF", f, file_name="sales_tools.pdf")
# Run app
if __name__ == "__main__":
    main()
