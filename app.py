# This example assumes you are using the OpenAI Python SDK (>=1.0.0) and Streamlit
# to build your sales tool generator.

import openai
import streamlit as st
import os

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
    prompt = f"""
    Using the following business background:

    ---
    {info}
    ---

    And targeting the following buyer personas:

    ---
    {personas}
    ---

    Generate a full sales sequence that starts with a cold email and ends with a closed deal, including tips and guidance at each stage.
    """
    return generate_content(prompt)

def main():
    st.title("🧠 Sales Tool Generator - AI Co-Pilot")

    with st.form("info_form"):
        business_info = st.text_area("Briefly describe your product or service:", height=100)
        target_personas = st.text_area("Describe your target audience or personas:", height=100)
        submitted = st.form_submit_button("Generate Sales Tools")

    if submitted:
        with st.spinner("Creating your custom sales walkthrough..."):
            deliverables = create_deliverables(business_info, target_personas)

        st.markdown("---")
        st.markdown("### 🧩 Your Step-by-Step Sales Toolkit")
        st.markdown(deliverables, unsafe_allow_html=True)

        # Optional download as PDF
        from io import BytesIO
        from xhtml2pdf import pisa

        def create_pdf_from_html(html):
            pdf = BytesIO()
            pisa.CreatePDF(BytesIO(html.encode("utf-8")), dest=pdf)
            return pdf

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
