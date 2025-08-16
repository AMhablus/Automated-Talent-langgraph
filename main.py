import os
import tempfile
import shutil
from pathlib import Path
from src.agent.graph import SharedState, graph
from src.agent.nodes import process_user_inputs

def get_user_inputs():
    """Get CV file path and job description from user"""
    print("=== CV Analysis Agent ===")
    print("This agent will analyze your CV against a job description.")
    print()
    
    # Get CV file path
    while True:
        cv_path = input("Enter the path to your CV (PDF file): ").strip()
        if not cv_path:
            print("Please provide a valid file path.")
            continue
            
        # Expand user path and check if file exists
        cv_path = os.path.expanduser(cv_path)
        if not os.path.exists(cv_path):
            print(f"File not found: {cv_path}")
            continue
            
        if not cv_path.lower().endswith('.pdf'):
            print("Please provide a PDF file.")
            continue
            
        break
    
    # Get job description
    print("\nEnter the job description (press Enter twice to finish):")
    jd_lines = []
    while True:
        line = input()
        if line == "" and jd_lines and jd_lines[-1] == "":
            break
        jd_lines.append(line)
    
    jd_text = "\n".join(jd_lines[:-1])  # Remove the last empty line
    
    if not jd_text.strip():
        print("Job description cannot be empty. Using default example...")
        from src.agent.examples import jd_ai
        jd_text = jd_ai
    
    return cv_path, jd_text

def run_analysis(cv_path: str, jd_text: str):
    """Run the CV analysis with user inputs"""
    print("\n=== Starting Analysis ===")
    
    # Create initial state
    initial_state = {
        "name": "",
        "email": "",
        "phone": "",
        "years_of_experience": 0,
        "skills": [],
        "pre_screening_status": "Fail",
        "skills_analysis": {
            "matched": [],
            "missing": [],
            "additional": [],
            "score": 0.0
        },
        "final_decision": "Rejected",
        "rejection_reason": "",
        "jd_text": jd_text
    }
    
    try:
        # Process user inputs first
        print("Processing CV and job description...")
        shared_state = SharedState(**initial_state)
        
        # Process the user inputs to populate the state
        shared_state = process_user_inputs(cv_path, jd_text, shared_state)
        
        print("Running agent analysis...")
        result = graph.invoke(shared_state)
        
        print("\n=== Analysis Complete! ===")
        print(f"Name: {result['name']}")
        print(f"Email: {result['email']}")
        print(f"Phone: {result['phone']}")
        print(f"Experience: {result['years_of_experience']} years")
        print(f"Skills: {', '.join(result['skills']) if isinstance(result['skills'], list) else result['skills']}")
        print(f"Pre-screening Status: {result['pre_screening_status']}")
        print(f"Final Decision: {result['final_decision']}")
        
        # Display skills analysis if available
        if result.get('skills_analysis'):
            skills_analysis = result['skills_analysis']
            print(f"\nSkills Analysis:")
            print(f"  Matched Skills: {', '.join(skills_analysis.get('matched', []))}")
            print(f"  Missing Skills: {', '.join(skills_analysis.get('missing', []))}")
            print(f"  Additional Skills: {', '.join(skills_analysis.get('additional', []))}")
            print(f"  Overall Score: {skills_analysis.get('score', 0)}/100")
        
        if result.get('rejection_reason'):
            print(f"\nRejection Reason: {result['rejection_reason']}")
            
    except Exception as e:
        print(f"Error during analysis: {e}")
        print("Please check your inputs and try again.")

def main():
    """Main function with user interface"""
    try:
        cv_path, jd_text = get_user_inputs()
        run_analysis(cv_path, jd_text)
        
    except KeyboardInterrupt:
        print("\n\nAnalysis cancelled by user.")
    except Exception as e:
        print(f"\nUnexpected error: {e}")

if __name__ == "__main__":
    main()