import streamlit as st
import os
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# Reference knowledge to inform GPT generation
REFERENCE_KNOWLEDGE = """
The Modern Sales Pipeline is a structured sales methodology that integrates three leading frameworks:

1. Dale Carnegie’s Relationship-Based Selling: Emphasizes trust, sincerity, and listening. Core principles include showing genuine interest in others, building rapport before pitching, and influencing people through empathy, appreciation, and shared goals. Carnegie advocates for active listening, remembering details about prospects, and letting others feel the idea is theirs. These techniques humanize the sales process and increase the chance of long-term client relationships.

2. The Sandler Selling System: A qualification-heavy approach focused on understanding the buyer’s pain, budget, and decision process before pitching. It begins with building equal business stature and upfront contracts (i.e., setting clear expectations). It emphasizes asking structured questions (the “Pain Funnel”) to uncover deep business issues and latent needs. Sandler sellers avoid free consulting, never push features too early, and present only when the prospect is emotionally and logically invested.

3. The Challenger Sale: Based on the idea that top-performing salespeople teach, tailor, and take control. Challenger reps lead with insight, reframe how buyers view their problems, and aren’t afraid to push back if needed. They tailor messages to individual buyer roles and use commercial teaching to lead prospects toward new ways of thinking that align with their product or service.

Together, these models form a six-stage process:
1. Prospecting – Identify ideal leads using insight and relevance.
2. Building Rapport – Establish credibility and comfort quickly.
3. Discovery – Ask smart, layered questions to reveal needs.
4. Presenting Solutions – Personalize the presentation to the buyer’s context and pain.
5. Handling Objections – Use empathy, insight, and logic to address concerns.
6. Closing – Gain commitment in a natural, pressure-free way, often by reinforcing agreed value.

This blended pipeline teaches reps to be consultative, respectful, insight-driven, and structured – allowing for predictable, high-value outcomes.

Dale Carnegie’s 30 Principles, updated for modern business, underpin this human-centered approach:
- Don’t criticize, condemn, or complain – handle objections calmly.
- Give honest and sincere appreciation – especially when a prospect shares information.
- Arouse in the other person an eager want – use value propositions that resonate with their goals.
- Become genuinely interested in other people – research and listen actively.
- Smile (in tone and presence) – maintain warmth even in email or video.
- Remember names and key facts – reflect understanding.
- Be a good listener – let them do most of the talking.
- Talk in terms of the other person’s interests – avoid product dumping.
- Let the other person feel the idea is theirs – use collaborative language.
- Dramatize your ideas – use stories or examples to make your point memorable.

These principles build trust, encourage cooperation, and reduce resistance throughout the sales process, whether during prospecting, negotiation, or onboarding.
"""
The Modern Sales Pipeline is a structured sales methodology that integrates three leading frameworks:

1. Dale Carnegie’s Relationship-Based Selling: Emphasizes trust, sincerity, and listening. Core principles include showing genuine interest in others, building rapport before pitching, and influencing people through empathy, appreciation, and shared goals. Carnegie advocates for active listening, remembering details about prospects, and letting others feel the idea is theirs. These techniques humanize the sales process and increase the chance of long-term client relationships.

2. The Sandler Selling System: A qualification-heavy approach focused on understanding the buyer's pain, budget, and decision process before pitching. It begins with building equal business stature and upfront contracts (i.e., setting clear expectations). It emphasizes asking structured questions (the "Pain Funnel") to uncover deep business issues and latent needs. Sandler sellers avoid free consulting, never push features too early, and present only when the prospect is emotionally and logically invested.

3. The Challenger Sale: Based on the idea that top-performing salespeople teach, tailor, and take control. Challenger reps lead with insight, reframe how buyers view their problems, and aren’t afraid to push back if needed. They tailor messages to individual buyer roles and use commercial teaching to lead prospects toward new ways of thinking that align with their product or service.

Together, these models form a six-stage process:
1. Prospecting – Identify ideal leads using insight and relevance.
2. Building Rapport – Establish credibility and comfort quickly.
3. Discovery – Ask smart, layered questions to reveal needs.
4. Presenting Solutions – Personalize the presentation to the buyer’s context and pain.
5. Handling Objections – Use empathy, insight, and logic to address concerns.
6. Closing – Gain commitment in a natural, pressure-free way, often by reinforcing agreed value.

This blended pipeline teaches reps to be consultative, respectful, insight-driven, and structured – allowing for predictable, high-value outcomes.

Dale Carnegie’s 30 Principles, updated for modern business, underpin this human-centered approach:
- Don’t criticize, condemn, or complain – handle objections calmly.
- Give honest and sincere appreciation – especially when a prospect shares information.
- Arouse in the other person an eager want – use value propositions that resonate with their goals.
- Become genuinely interested in other people – research and listen actively.
- Smile (in tone and presence) – maintain warmth even in email or video.
- Remember names and key facts – reflect understanding.
- Be a good listener – let them do most of the talking.
- Talk in terms of the other person’s interests – avoid product dumping.
- Let the other person feel the idea is theirs – use collaborative language.
- Dramatize your ideas – use stories or examples to make your point memorable.

These principles build trust, encourage cooperation, and reduce resistance throughout the sales process, whether during prospecting, negotiation, or onboarding.
"""
The Modern Sales Pipeline integrates Dale Carnegie's relationship-building approach, Sandler's structured discovery and qualification, and the Challenger Sale's insight-led teaching and assertive closing. The six core stages are: Prospecting, Rapport, Discovery, Presenting Solutions, Handling Objections, and Closing.

Dale Carnegie's 30 principles emphasize empathy, human dignity, and effective communication. In sales and leadership, they foster rapport, influence without pressure, and build loyalty through sincere interest and appreciation.
"""

The Modern Sales Pipeline integrates Dale Carnegie's relationship-building approach, Sandler's structured discovery and qualification, and the Challenger Sale's insight-led teaching and assertive closing. The six core stages are: Prospecting, Rapport, Discovery, Presenting Solutions, Handling Objections, and Closing.

Dale Carnegie's 30 principles emphasize empathy, human dignity, and effective communication. In sales and leadership, they foster rapport, influence without pressure, and build loyalty through sincere interest and appreciation.
"""

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
    return f"""Using the context below, create a short and medium-length elevator pitch for a B2B company.

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
    return f"""Using the reference information below, write a consultative B2B sales call script with a {data['tone']} tone.

Reference:
{REFERENCE_KNOWLEDGE}

Target Company: {data['company']}
Product: {data['product']}
Ideal Customer: {data['ideal_customer']}
Problem Solved: {data['problem']}
Unique Value: {data['unique']}
"""

def build_prompt_cold_email(data):
    return f"""Using the context below, write a cold outreach email introducing {data['company']} to a prospect in {data['ideal_customer']}. Keep it concise and persuasive.

Reference:
{REFERENCE_KNOWLEDGE}

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



