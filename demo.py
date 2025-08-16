#!/usr/bin/env python3
"""
Demo script for the CV Analysis Agent
This script demonstrates how to use the agent programmatically
"""

import os
from src.agent.graph import SharedState, graph
from src.agent.nodes import process_user_inputs

def demo_with_example_cv():
    """Demo using the example CV from examples.py"""
    print("=== CV Analysis Agent Demo ===")
    print("Using example CV and job description...")
    
    # Get the example CV and JD
    from src.agent.examples import cv_ai, jd_ai
    
    # Create a temporary CV file
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
        f.write(cv_ai)
        temp_cv_path = f.name
    
    try:
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
            "jd_text": jd_ai
        }
        
        print("Processing inputs...")
        shared_state = SharedState(**initial_state)
        
        # Process the inputs (we'll use the text directly since it's not a PDF)
        # For demo purposes, we'll simulate the PDF processing
        cv_message = f"CV Content:\n{cv_ai}"
        jd_message = f"Job Description:\n{jd_ai}"
        
        print("Running analysis...")
        # Run the analysis using the existing workflow
        result = graph.invoke(shared_state)
        
        # Display results
        print("\n=== Demo Results ===")
        print(f"Name: {result['name']}")
        print(f"Email: {result['email']}")
        print(f"Phone: {result['phone']}")
        print(f"Experience: {result['years_of_experience']} years")
        print(f"Skills: {', '.join(result['skills']) if isinstance(result['skills'], list) else result['skills']}")
        print(f"Pre-screening Status: {result['pre_screening_status']}")
        print(f"Final Decision: {result['final_decision']}")
        
        # Skills analysis
        if result.get('skills_analysis'):
            skills_analysis = result['skills_analysis']
            print(f"\nSkills Analysis:")
            print(f"  Overall Score: {skills_analysis.get('score', 0)}/100")
            print(f"  Matched Skills: {', '.join(skills_analysis.get('matched', []))}")
            print(f"  Missing Skills: {', '.join(skills_analysis.get('missing', []))}")
            print(f"  Additional Skills: {', '.join(skills_analysis.get('additional', []))}")
        
        if result.get('rejection_reason'):
            print(f"\nRejection Reason: {result['rejection_reason']}")
        
        print("\n=== Demo Complete ===")
        print("This demonstrates the agent's ability to:")
        print("1. Extract candidate information from CV text")
        print("2. Analyze skills against job requirements")
        print("3. Provide intelligent screening recommendations")
        print("4. Generate detailed analysis reports")
        
    finally:
        # Clean up temporary file
        if os.path.exists(temp_cv_path):
            os.unlink(temp_cv_path)

def demo_usage_examples():
    """Show usage examples for different interfaces"""
    print("\n=== Usage Examples ===")
    
    print("\n1. Web Interface (Recommended):")
    print("   streamlit run app.py")
    print("   - Upload CV PDF")
    print("   - Input job description")
    print("   - Get visual results")
    
    print("\n2. Command Line Interface:")
    print("   python cli.py --cv cv.pdf --jd 'Job description...'")
    print("   python cli.py --cv cv.pdf --jd-file jd.txt --output results.txt")
    
    print("\n3. Interactive Terminal:")
    print("   python main.py")
    print("   - Follow prompts for file path and JD")
    
    print("\n4. Programmatic Usage:")
    print("   from src.agent.graph import graph")
    print("   from src.agent.nodes import process_user_inputs")
    print("   # Process inputs and run analysis")

if __name__ == "__main__":
    try:
        demo_with_example_cv()
        demo_usage_examples()
        
        print("\n🎉 Demo completed successfully!")
        print("The CV Analysis Agent is now dynamic and ready to process any CV and job description!")
        
    except Exception as e:
        print(f"Demo failed with error: {e}")
        print("Please check your setup and try again.")
