import os 
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from src.agent.state import SharedState
from src.agent.prompts import skills_analysis_system_msg, rejected_system_msg, prescreen_system_msg
import json
from pydantic import SecretStr
from langchain_community.document_loaders import PyPDFLoader
from src.agent.examples import cv_ai, jd_ai
import tempfile
import shutil


load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LLM = ChatGroq(model="openai/gpt-oss-120b", temperature=0, api_key=SecretStr(OPENAI_API_KEY) if OPENAI_API_KEY else None)


def extract_pdf_txt(pdf_path: str, state: SharedState) -> str:
    """Extract text from uploaded PDF file"""
    try:
        loader = PyPDFLoader(pdf_path)
        pages = loader.load()
        cv_text = "\n\n".join([p.page_content for p in pages]) 
        return cv_text
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")

def process_user_inputs(cv_file_path: str, jd_text: str, state: SharedState) -> SharedState:
    """Process user uploaded CV (PDF) and JD (text) for analysis"""
    # Extract text from CV PDF
    cv_text = extract_pdf_txt(cv_file_path, state)
    
    # Create messages for the LLM
    cv_message = HumanMessage(content=cv_text)
    jd_message = HumanMessage(content=jd_text)
    sys_message = SystemMessage(content=prescreen_system_msg)
    
    messages = [sys_message, cv_message, jd_message]
    
    response = LLM.invoke(messages)
    
    try:
        data = json.loads(str(response.content))
        
        # Update the shared state
        state["name"] = data["name"]
        state["email"] = data["email"]
        state["phone"] = data["phone"]
        state["years_of_experience"] = data["years_of_experience"]
        state["skills"] = data["skills"]
        state["pre_screening_status"] = data["pre_screening_status"]
        state["skills_analysis"] = data["skills_analysis"]
        state["final_decision"] = data["final_decision"]
        state["rejection_reason"] = data["rejection_reason"]
        
    except json.JSONDecodeError as e:
        raise Exception(f"Error parsing LLM response: {str(e)}")
    except KeyError as e:
        raise Exception(f"Missing required field in response: {str(e)}")

    return state

def input_and_prescreening(state: SharedState) -> SharedState:
    """Legacy function for hardcoded examples - kept for backward compatibility"""
    cv_message = HumanMessage(content=cv_ai)
    jd_message = HumanMessage(content=jd_ai)
    sys_message = SystemMessage(content=prescreen_system_msg)
    
    messages = [sys_message, cv_message, jd_message]
    
    response = LLM.invoke(messages)
    
    data = json.loads(str(response.content))
    
    # Update the shared state
    state["name"] = data["name"]
    state["email"] = data["email"]
    state["phone"] = data["phone"]
    state["years_of_experience"] = data["years_of_experience"]
    state["skills"] = data["skills"]
    state["pre_screening_status"] = data["pre_screening_status"]
    state["skills_analysis"] = data["skills_analysis"]
    state["final_decision"] = data["final_decision"]
    state["rejection_reason"] = data["rejection_reason"]

    return state


def skills_analysis(state: SharedState) -> SharedState:
    sys_message = SystemMessage(content=skills_analysis_system_msg)
    cv_skills = state["skills"]
    cv_message = HumanMessage(content=", ".join(cv_skills) if isinstance(cv_skills, list) else str(cv_skills))
    
    # Use the JD text from state if available, otherwise fall back to hardcoded example
    jd_text = state.get("jd_text", jd_ai)
    jd_message = HumanMessage(content=jd_text)
    
    messages = [sys_message, cv_message, jd_message]
    
    response = LLM.invoke(messages)
    data = json.loads(str(response.content))
    state["skills_analysis"] = data["skills_analysis"]
    return state


def router1(state: SharedState) -> str:
    """
    Route the state to the appropriate function based on the final decision.
    """ 
    pre_screening_status = state["pre_screening_status"]

    if pre_screening_status == "Pass":
        return "skills_analysis"
    elif pre_screening_status == "Fail":
        return "reject"
    else:
        raise ValueError(f"Invalid pre-screening status: {pre_screening_status}")


def router2(state: SharedState):
    """
    Route the state to the appropriate function based on the final decision.
    """ 
    score = state["skills_analysis"]["score"]
    if score > 80:
        return "Interview"
    elif 50 <= score <= 80:
        return "Phone Screen"
    elif score < 50:
        return "Rejected"
    else:
        raise ValueError(f"Invalid score: {score}")
    
    
def interview(state: SharedState) -> SharedState:
    state["final_decision"] = "Interview"
    return state
    

def phone_screen(state: SharedState) -> SharedState:
    state["final_decision"] = "Phone Screen"
    return state
    

def reject(state: SharedState) -> SharedState:
    state["final_decision"] = "Rejected"
    sys_message = SystemMessage(content=rejected_system_msg)
    messages = [sys_message, HumanMessage(content=json.dumps(state["skills_analysis"], indent=2))]
    response = LLM.invoke(messages)
    state["rejection_reason"] = str(response.content)
    return state
    

