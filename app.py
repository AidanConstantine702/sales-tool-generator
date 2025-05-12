# This example assumes you are using the OpenAI Python SDK (>=1.0.0) and Streamlit
# to build your sales tool generator.

import openai
import streamlit as st
import os
from io import BytesIO
from xhtml2pdf import pisa

# Load OpenAI API key from Streamlit secrets or environment variable
api_key = st.secrets.get("openai_api_key") or os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=api_key)

def generate_content(prompt):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": (
                "You are an expert business sales assistant. You will generate highly actionable, human-sounding, and psychologically persuasive sales tools."
                " You must follow the combined principles from Dale Carnegie's Human Relations, the Sandler Sales System, and the Challenger Sale methodology."
                " Base everything you generate strictly on the guidance, language, and psychology found in the documents titled 'Dale Carnegie 30 principles for modern business' and 'The Modern Sales Pipeline.'"
                " Your goal is to help ambitious but inexperienced users build trust, uncover needs, teach insights, and close deals across a complete timeline."
                " Deliver your output in a clearly formatted walkthrough style:"
                "\n\n1. Start with a Cold Email\n2. Assume a positive email reply, then generate a follow-up call script that builds on that context.\n3. Next, outline the discovery call script/questions.\n4. Then provide a solution presentation structure with tailored insights.\n5. Handle 2 common objections related to the user’s industry.\n6. End with a closing plan (what to say, what to do, what to expect).\n\nBetween each of these steps, insert bold section headers and quick tips. Add 1-2 short sentences helping the user understand what to expect, what mindset to have, or what outcome to aim for."
            )},
            {"role": "user", "content": prompt},
        ]
    )
    return response.choices[0].message.content

def create_deliverables(info, personas):
    advanced = info.get("advanced", {})
    prompt = f"""
You are building a sales toolkit for a motivated founder or business owner.

Company Name: {info['company_name']}
Products/Services: {info['products_services']}
Target Audience: {info['target_audience']}
Top Problems Solved: {info['top_problems']}
Value Proposition: {info['value_prop']}
Preferred Tone: {info['tone']}

# Advanced Insights
Desired Prospect Action: {advanced.get('action_goal', 'Not specified')}
Common Objection: {advanced.get('top_objection', 'Not specified')}
Customer Testimonial Snippet: {advanced.get('customer_quote', 'Not specified')}
Delivery Method: {advanced.get('delivery_method', 'Not specified')}
Sales Model: {advanced.get('b2b_or_b2c', 'Not specified')}
Sales Cycle: {advanced.get('sales_cycle', 'Not specified')}
Competitive Advantage: {advanced.get('competitor_edge', 'Not specified')}
Objection Rebuttal: {advanced.get('fallback_rebuttal', 'Not specified')}
Conversation Style: {advanced.get('conversation_style', 'Not specified')}
Speaking Comfort Level (0–10): {advanced.get('comfort_level', 'Not specified')}

Buyer Personas:
{personas}

Generate a complete, step-by-step sales walkthrough with realistic, usable tools and tips — starting from first contact and ending with a closed deal.
"""
    return generate_content(prompt)

def create_pdf_from_html(html):
    pdf = BytesIO()
    pisa.CreatePDF(BytesIO(html.encode("utf-8")), dest=pdf)
    return pdf

def main():
    st.title("🧠 Sales Tool Generator - AI Co-Pilot")

    with st.form("info_form"):
        st.subheader("📋 Basic Information")
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

        submitted = st.form_submit_button("Generate Sales Tools")

    if submitted:
        with st.spinner("Creating your custom sales walkthrough..."):
            inputs = {
                "company_name": company_name,
                "products_services": products_services,
                "target_audience": target_audience,
                "top_problems": top_problems,
                "value_prop": value_prop,
                "tone": tone,
                "advanced": advanced
            }
            personas = "Custom input from advanced fields or default buyer types."
            deliverables = create_deliverables(inputs, personas)

        st.markdown("---")
        st.markdown("### 🧩 Your Step-by-Step Sales Toolkit")
        st.markdown(deliverables, unsafe_allow_html=True)

        if st.button("Download as PDF"):
            pdf_data = create_pdf_from_html(deliverables)
            st.download_button(
                label="📥 Download Sales Toolkit as PDF",
                data=pdf_data.getvalue(),
                file_name="sales_toolkit.pdf",
                mime="application/pdf"
            )

if __name__ == "__main__":
    main()
