import streamlit as st
import os
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# Function to call GPT-4 via OpenAI API
def gpt_generate(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"GPT API Error: {str(e)}")
        return ""

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
    return f"""Write a consultative B2B sales call script using a {data['tone']} tone.
Company: {data['company']}
Customer: {data['ideal_customer']}
Problem: {data['problem']}
Solution: {data['product']}
Unique Value: {data['unique']}
"""

def build_prompt_cold_email(data):
    return f"""Write a cold outreach email introducing {data['company']} to a prospect in {data['ideal_customer']}. Keep it concise and persuasive.
Product: {data['product']}
Problem it solves: {data['problem']}
Unique benefit: {data['unique']}
Tone: {data['tone']}
"""

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

# Streamlit UI
st.title("🧠 B2B Sales Toolkit Generator (GPT-4 Powered)")
st.write("Answer a few quick questions and get your sales toolkit generated instantly.")

company = st.text_input("1. Company name?")
product = st.text_input("2. What does your company sell?")
ideal_customer = st.text_input("3. Who is your ideal customer?")
problem = st.text_input("4. What problem does your product solve?")
unique = st.text_input("5. What makes your company different?")
tone = st.selectbox("6. Preferred tone?", ["Professional", "Friendly", "Confident", "Bold"])

if st.button("🚀 Generate Sales Toolkit"):
    if not all([company, product, ideal_customer, problem, unique]):
        st.error("Please complete all fields before generating.")
    else:
        inputs = {
            "company": company,
            "product": product,
            "ideal_customer": ideal_customer,
            "problem": problem,
            "unique": unique,
            "tone": tone
        }

        with st.spinner("Generating elevator pitch..."):
            elevator_output = gpt_generate(build_prompt_elevator(inputs)).split("\n")
            short_pitch = elevator_output[0] if elevator_output else ""
            medium_pitch = "\n".join(elevator_output[1:]) if len(elevator_output) > 1 else ""

        with st.spinner("Generating call script..."):
            call_script = gpt_generate(build_prompt_call_script(inputs))

        with st.spinner("Generating cold email..."):
            cold_email = gpt_generate(build_prompt_cold_email(inputs))

        assessment = generate_assessment()

        st.success("✅ Sales Toolkit Generated")

        st.subheader("📢 Elevator Pitch")
        st.markdown(f"**Short:**\n{short_pitch}")
        st.markdown(f"**Medium:**\n{medium_pitch}")

        st.subheader("📞 Sales Call Script")
        st.text_area("Call Script", call_script, height=250)

        st.subheader("✉️ Cold Outreach Email")
        st.text_area("Cold Email", cold_email, height=200)

        st.subheader("🧩 Needs Assessment Questions")
        for q in assessment:
            st.markdown(f"- {q}")
