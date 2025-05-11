import streamlit as st
import os
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# Reference knowledge to inform GPT generation
REFERENCE_KNOWLEDGE = """
The Modern Sales Pipeline is a structured sales methodology that blends three respected frameworks:

1. Dale Carnegie's Relationship-Based Selling: Focuses on building trust, showing sincere interest in others, and communicating with empathy. Sales reps using this approach listen actively, appreciate others genuinely, and seek mutual understanding to influence decisions.

2. The Sandler Selling System: A qualification-first process that emphasizes asking strategic questions, identifying pain points, and establishing upfront agreements. Salespeople avoid pitching too early and instead gain agreement on budget and decision-making processes before presenting solutions.

3. The Challenger Sale: Encourages salespeople to teach prospects new insights, tailor communications to the buyer's role, and take control of the sales conversation. Challenger reps reframe customer thinking and guide buyers toward recognizing problems they didn't realize they had.

Together, these approaches support a six-stage pipeline: Prospecting, Building Rapport, Discovery, Presenting Solutions, Handling Objections, and Closing.

Dale Carnegie's 30 Principles—such as avoiding criticism, giving sincere appreciation, becoming genuinely interested in others, and dramatizing ideas—underpin effective relationship-building and influence in every sales stage.
"""

# GPT call function
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
    return f"""
Using the context below, create a short and medium-length elevator pitch for a B2B company.

Reference:
{REFERENCE_KNOWLEDGE}

Company: {data['company']}
Product: {data['product']}
Ideal Customer: {data['ideal_customer']}
Problem Solved: {data['problem']}
What Makes Us Unique: {data['unique']}
Tone: {data['tone']}
"""

def build_prompt_call_script(data):
    return f"""
Using the reference below, write a consultative B2B sales call script with a {data['tone']} tone.

Reference:
{REFERENCE_KNOWLEDGE}

Target Company: {data['company']}
Product: {data['product']}
Ideal Customer: {data['ideal_customer']}
Problem Solved: {data['problem']}
Unique Value: {data['unique']}
"""

def build_prompt_cold_email(data):
    return f"""
Using the reference below, write a cold outreach email introducing {data['company']} to a prospect in {data['ideal_customer']}. Keep it concise and persuasive.

Reference:
{REFERENCE_KNOWLEDGE}

Product: {data['product']}
Problem it solves: {data['problem']}
Unique benefit: {data['unique']}
Tone: {data['tone']}
"""

def generate_assessment():
    return [
        "How do you currently handle customer acquisition?",
        "What challenges do you face in your current sales pipeline?",
        "How are your reps trained on objection handling?",
        "What percentage of deals stall before closing?",
        "Do you use a formal sales framework or methodology?",
        "Who are your target decision-makers in the buying process?",
        "What would improve conversion rates most in your opinion?"
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
