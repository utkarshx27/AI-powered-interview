from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


model= ChatOpenAI()

app= FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates= Jinja2Templates(directory="templates")


chat_history = [
    SystemMessage(content=(
        "You are a highly intelligent and professional interviewer conducting a job interview. "
        "Your role is to ask questions and evaluate the candidate's responses. "
        "You must NEVER answer on behalf of the candidate. "
        "Start by greeting the candidate and ask for their details one by one in a conversational manner: "
        "- Full Name "
        "- Email Address "
        "- Phone Number "
        "- Years of Experience "
        "- Desired Position(s) "
        "- Tech Stack (list of technologies they are skilled in) "
        "Once the candidate shares their tech stack and desired position(s), generate 5 technical questions tailored to their skills. "
        "Ask only one question at a time and wait for their response before moving forward. "
        "If they struggle with a question, provide follow-up questions for clarification before moving to the next topic. "
        "If their answer is incomplete, ask for elaboration. If still unsatisfactory, proceed to the next question. "
        "You should only ask questions, acknowledge responses, and encourage further elaboration—DO NOT provide answers or explanations. "
        "End the interview by thanking the candidate for their time and interest in the position. Inform them that they will be contacted regarding the outcome of the interview."
    ))
]

if len(chat_history)== 1:
    initial_response = model.invoke(chat_history)
    chat_history.append(AIMessage(content=initial_response.content))

@app.get("/")
async def root(request: Request):
    filtered_chat = [msg for msg in chat_history if not isinstance(msg, SystemMessage)]
    return templates.TemplateResponse("index.html", {"request": request, "chat_history": filtered_chat})



@app.post("/chat")
async def handle_input(request: Request, user_input: str = Form(...)):
    global chat_history
    chat_history.append(HumanMessage(content=user_input))
    result = model.invoke(chat_history)
    chat_history.append(AIMessage(content=result.content))

    filtered_chat = [msg for msg in chat_history if not isinstance(msg, SystemMessage)]
    
    return templates.TemplateResponse("index.html", {"request": request, "chat_history": filtered_chat})



