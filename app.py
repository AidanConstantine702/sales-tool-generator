import streamlit as st
from fpdf import FPDF
import datetime

# Function to generate elevator pitch

def generate_elevator_pitch(data):
    short = f"We help {data['ideal_customer']} solve {data['problem']} by offering {data['product']}. Unlike others, we {data['unique']}."
    medium = f"At {data['company']}, we serve {data['ideal_customer']} who are facing {data['problem']}. Our solution, {data['product']}, stands out because we {data['unique']}. With a {data['tone']} tone, we help clients achieve better outcomes, faster." 
    return short, medium

# Function to generate sales call script

def generate_call_script(data):
    return f"""
--- Sales Call Script ---

Hi, this is [Your Name] from {data['company']}. I work with companies in {data['ideal_customer']} who are struggling with {data['problem']}.

I’m reaching out because our solution, {data['product']}, helps solve that problem by {data['unique']}.

Can I ask you a few quick questions to see if this might be a fit?

1. How do you currently handle this issue?
2. What challenges are you facing with your current process?
3. Would it help to have a more cost-effective, streamlined way?

If you're open to it, I’d love to schedule a deeper conversation.

Thanks for your time!
"""

# Function to generate cold email

def generate_cold_email(data):
    return f"""
Subject: Solving {data['problem']} for {data['ideal_customer']}

Hi [First Name],

I’m reaching out from {data['company']}. We help businesses like yours solve {data['problem']} using {data['product']}.

What makes us different? We {data['unique']}.

Would you be open to a quick 15-minute call to explore if this is a fit?

Best,
[Your Name]
"""

# Function to generate needs assessment questions

def generate_assessment():
    return [
        "How do you currently handle drug and alcohol testing?",
        "Are you using multiple vendors or a centralized platform?",
        "What compliance challenges are you facing?",
        "When was the last time your policy was updated?",
        "How many employees do you hire annually?",
        "Would consolidating background checks, testing, and policy help reduce costs?",
        "Do you require testing across multiple states or regions?"
    ]

# Function to export to PDF

def export_to_pdf(data, short_pitch, medium_pitch, script, email, assessment):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, f"Sales Tools Generated - {datetime.date.today()}\n\n")

    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Elevator Pitch (Short):", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, short_pitch)

    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Elevator Pitch (Medium):", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, medium_pitch)

    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Sales Call Script:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, script)

    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Cold Email:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, email)

    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Needs Assessment Questions:", ln=True)
    pdf.set_font("Arial", size=12)
    for q in assessment:
        pdf.multi_cell(0, 10, f"- {q}")

    filepath = "/tmp/sales_toolkit.pdf"
    pdf.output(filepath)
    return filepath

# Streamlit UI
st.title("B2B Sales Training Chatbot")
st.write("Answer the questions below to generate your sales toolkit.")

company = st.text_input("1. What is your company name?")
product = st.text_input("2. What does your company sell?")
ideal_customer = st.text_input("3. Who is your ideal customer?")
problem = st.text_input("4. What problem does your product solve?")
unique = st.text_input("5. What makes your product/service different?")
tone = st.selectbox("6. Preferred tone of voice?", ["Professional", "Friendly", "Confident", "Bold"])

if st.button("Generate Sales Toolkit"):
    inputs = {
        "company": company,
        "product": product,
        "ideal_customer": ideal_customer,
        "problem": problem,
        "unique": unique,
        "tone": tone
    }

    short_pitch, medium_pitch = generate_elevator_pitch(inputs)
    call_script = generate_call_script(inputs)
    email = generate_cold_email(inputs)
    assessment = generate_assessment()
    pdf_file = export_to_pdf(inputs, short_pitch, medium_pitch, call_script, email, assessment)

    st.success("Sales toolkit generated!")
    with open(pdf_file, "rb") as f:
        st.download_button("📄 Download PDF", f, file_name="sales_toolkit.pdf")
