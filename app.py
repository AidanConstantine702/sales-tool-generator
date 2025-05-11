import streamlit as st
from fpdf import FPDF
import datetime
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Function to call ChatGPT for content generation
def gpt_generate(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

# Prompt builders
def build_prompt_elevator(data):
    return f"""Create a short and medium-length elevator pitch for the following:
Company: {data['company']}
Product: {data['product']}
Ideal Customer: {data['ideal_customer']}
Problem Solved: {data['problem']}
What Makes Us Unique: {data['unique']}
Tone: {data['tone']}
"""

def build_prompt_call_script(data):
    return f"""Write a consultative B2B sales call script using a friendly tone.
Company: {data['company']}
Customer: {data['ideal_customer']}
Problem: {data['problem']}
Solution: {data['product']}
Unique Value: {data['unique']}
"""

def build_prompt_cold_email(data):
    return f"""Write a cold outreach email introducing {data['company']} to a prospect in {data['ideal_customer']}. Keep it concise, persuasive, and friendly.
Product: {data['product']}
Problem it solves: {data['problem']}
Unique benefit: {data['unique']}
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

# Export content to PDF
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
st.write("Answer the questions below to generate your sales toolkit using GPT.")

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

    # GPT generation
    elevator_output = gpt_generate(build_prompt_elevator(inputs)).split("\n")
    short_pitch = elevator_output[0] if elevator_output else ""
    medium_pitch = "\n".join(elevator_output[1:]) if len(elevator_output) > 1 else ""
    call_script = gpt_generate(build_prompt_call_script(inputs))
    cold_email = gpt_generate(build_prompt_cold_email(inputs))
    assessment = generate_assessment()

    pdf_file = export_to_pdf(inputs, short_pitch, medium_pitch, call_script, cold_email, assessment)

    st.success("Sales toolkit generated with GPT!")
    with open(pdf_file, "rb") as f:
        st.download_button("📄 Download PDF", f, file_name="sales_toolkit.pdf")

