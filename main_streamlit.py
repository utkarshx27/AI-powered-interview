import streamlit as st
import pandas as pd
import os
from cryptography.fernet import Fernet
from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
import os
from dotenv import load_dotenv

# os.environ["OPENAI_API_KEY"] = "Apikey here"

load_dotenv()


# Encryption setup to  gen or check the key
def get_or_create_key():
    key_env_var= "INTERVIEW_ENCRYPTION_KEY"
    if key_env_var in os.environ:
        return os.environ[key_env_var].encode()
    
    key_file= "secret.key"
    if not os.path.exists(key_file):
        key = Fernet.generate_key()
        with open(key_file, "wb") as key_file:
            key_file.write(key)
        os.chmod(key_file, 0o400)
    with open(key_file, "rb") as f:
        return f.read()


# Definign the cipher suite
cipher_suite= Fernet(get_or_create_key())

# Encrypt and decrypt the data
def encrypt_data(data):
    return cipher_suite.encrypt(data.encode()).decode()

# def decrypt_data(encrypted_data):
#     return cipher_suite.decrypt(encrypted_data.encode()).decode()

def store_candidate_data(user_info, chat_history):
    encrypted_info = {
        'Full Name': encrypt_data(user_info.get('Full Name', '')),
        'Email Address': encrypt_data(user_info.get('Email Address', '')),
        'Phone Number': encrypt_data(user_info.get('Phone Number', '')),
        'Years of Experience': user_info.get('Years of Experience', ''),
        'Desired Position': user_info.get('Desired Position', ''),
        'Tech Stack': str(user_info.get('Tech Stack', [])),
        'Interview Date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'Chat History': str(chat_history)
    }
    
    # storage dir
    os.makedirs("secure_data", exist_ok=True)
    file_path = "secure_data/candidates.csv"
    df= pd.DataFrame([encrypted_info])
    if os.path.exists(file_path):
        df.to_csv(file_path, mode='a', header=False, index=False)
    else:
        df.to_csv(file_path, index=False)
    
    os.chmod(file_path, 0o600)


model = ChatOpenAI(temperature=0.2)

# System prompt for the interviewer
SYSTEM_PROMPT = """You are a highly intelligent and professional interviewer conducting a job interview. 
Your role is to ask questions and evaluate the candidate's responses. 
You must NEVER answer on behalf of the candidate. 
Start by greeting the candidate and ask for their details one by one in a conversational manner: 
- Full Name 
- Email Address 
- Phone Number 
- Years of Experience 
- Desired Position(s) 
- Tech Stack (list of technologies they are skilled in) 
Verify the format of the information provided by the candidate.
Once the candidate shares their tech stack and desired position(s), generate 5 technical questions tailored to their all skills provided but ask one question at a time 
Ask only one question at a time and wait for their response before moving forward.
If they struggle with a question, provide follow-up questions for clarification before moving to the next topic. 
If their answer is incomplete, ask for elaboration. If still unsatisfactory, proceed to the next question. 
You should only ask questions, acknowledge responses, and encourage further elaboration—DO NOT provide answers or explanations. 
End the interview by thanking the candidate for their time and interest in the position. Inform them that they will be contacted regarding the outcome of the interview."""


# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'interview_started' not in st.session_state:
    st.session_state.interview_started = False

def initialize_interview():
    """Initialize the interview process with system message"""
    system_message = SystemMessage(content=SYSTEM_PROMPT)
    st.session_state.chat_history = [system_message]
    with st.spinner("Interviewer is preparing..."):
        response = model.invoke(st.session_state.chat_history)
    st.session_state.chat_history.append(AIMessage(content=response.content))
    st.session_state.interview_started = True

# Streamlit UI components
st.title("AI Powered Job Interviewer")
st.markdown("---")

# Chat container
chat_container = st.container()

# Start interview button
if not st.session_state.interview_started:
    st.markdown("### Welcome to your job interview!")
    st.markdown("Click the button below to start your interview. \n Instruction to follow blow.")
    st.markdown("If you want to leave the interview, simple write 'exit' in the chat box")
    st.markdown("Do Not Refresh the page during the interview. Answer the question with clearity")
    if st.button("Start Interview"):
        initialize_interview()
        st.rerun()

# Display chat massages
with chat_container:
    for message in st.session_state.chat_history:
        if isinstance(message, SystemMessage):
            continue
        with st.chat_message("assistant" if isinstance(message, AIMessage) else "user"):
            st.markdown(message.content)

# Handle user input and interview flow
if st.session_state.interview_started:
    # Check if interview has concluded
    last_message= st.session_state.chat_history[-1]
    interview_ended= isinstance(last_message, AIMessage) and any(
    keyword in last_message.content.lower() 
    for keyword in ["will be contacted", "outcome of the interview"]
    )

    if not interview_ended:
        if user_input := st.chat_input("Type your response here..."):
            # Add user message to history
            st.session_state.chat_history.append(HumanMessage(content=user_input))
            # Get interviewer res
            with st.spinner("Interviewer is thinking..."):
                response = model.invoke(st.session_state.chat_history)
            # Add and display res
            st.session_state.chat_history.append(AIMessage(content=response.content))
            st.rerun()
    else:
        st.success("🎉 Interview completed! Thank you for your participation.")
        st.balloons()


        user_info = {}
        info_fields = [
            "Full Name", "Email Address", "Phone Number",
            "Years of Experience", "Desired Position", "Tech Stack"
        ]
        
        current_field = None
        for msg in st.session_state.chat_history:
            if isinstance(msg, AIMessage):
                for field in info_fields:
                    if field.lower() in msg.content.lower():
                        current_field = field
                        break
            elif isinstance(msg, HumanMessage) and current_field:
                user_info[current_field] = msg.content
                current_field = None

        store_candidate_data(user_info, st.session_state.chat_history)


# we can also use mongoDB to store the data session wise and SQL for the final data,
# I have used langchian so that we can use any model in future (maybe models like deepseek will be cost effective and efficient).
# We can Intergrate compiler to check the code of the candidate.
# Also we can use RAG model to check the answers of the candidate which are out of model scope.
# We can use vector search to check the Resuem of the candidate.
# We can use Computer Vision to check the body language of the candidate. Mainly the eye contact.
# Text to Speech model can be used to interact with the candidate in voice.
# A Fine TUned model on the interview data can be used to conduct human like interview.
# Adding a Input Validator like pydantic to validate the input of the candidate will be better imo.

