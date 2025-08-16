#!/usr/bin/env python3
"""
Command Line Interface for CV Analysis Agent
"""

import os
import sys
import argparse
from pathlib import Path
from src.agent.graph import SharedState, graph
from src.agent.nodes import process_user_inputs

def validate_pdf_file(file_path):
    """Validate that the file exists and is a PDF"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    
    if not file_path.lower().endswith('.pdf'):
        raise ValueError(f"File must be a PDF: {file_path}")
    
    return file_path

def read_jd_from_file(file_path):
    """Read job description from a text file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except Exception as e:
        raise Exception(f"Error reading JD file: {str(e)}")

def run_analysis(cv_path, jd_text, output_file=None):
    """Run the CV analysis"""
    print("=== CV Analysis Agent ===")
    print(f"CV File: {cv_path}")
    print(f"Job Description Length: {len(jd_text)} characters")
    print()
    
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
        print("Processing CV and job description...")
        shared_state = SharedState(**initial_state)
        
        # Process the user inputs
        shared_state = process_user_inputs(cv_path, jd_text, shared_state)
        
        print("Running agent analysis...")
        result = graph.invoke(shared_state)
        
        # Display results
        print("\n=== Analysis Complete! ===")
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
        
        # Save to output file if specified
        if output_file:
            results_text = f"""CV Analysis Results

Candidate: {result['name']}
Email: {result['email']}
Phone: {result['phone']}
Experience: {result['years_of_experience']} years

Skills: {', '.join(result['skills']) if isinstance(result['skills'], list) else result['skills']}

Pre-screening Status: {result['pre_screening_status']}
Final Decision: {result['final_decision']}

Skills Analysis:
- Overall Score: {result.get('skills_analysis', {}).get('score', 0)}/100
- Matched Skills: {', '.join(result.get('skills_analysis', {}).get('matched', []))}
- Missing Skills: {', '.join(result.get('skills_analysis', {}).get('missing', []))}
- Additional Skills: {', '.join(result.get('skills_analysis', {}).get('additional', []))}

Rejection Reason: {result.get('rejection_reason', 'N/A')}
"""
            try:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(results_text)
                print(f"\nResults saved to: {output_file}")
            except Exception as e:
                print(f"Warning: Could not save results to {output_file}: {str(e)}")
        
        return result
        
    except Exception as e:
        print(f"Error during analysis: {str(e)}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="CV Analysis Agent - Analyze CV against job description",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze CV with JD from command line
  python cli.py --cv path/to/cv.pdf --jd "Software Engineer position..."

  # Analyze CV with JD from file
  python cli.py --cv path/to/cv.pdf --jd-file path/to/jd.txt

  # Save results to file
  python cli.py --cv path/to/cv.pdf --jd "Job description..." --output results.txt
        """
    )
    
    parser.add_argument(
        '--cv', 
        required=True,
        help='Path to CV PDF file'
    )
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '--jd',
        help='Job description text'
    )
    group.add_argument(
        '--jd-file',
        help='Path to job description text file'
    )
    
    parser.add_argument(
        '--output',
        help='Output file to save results (optional)'
    )
    
    args = parser.parse_args()
    
    try:
        # Validate CV file
        cv_path = validate_pdf_file(args.cv)
        
        # Get job description
        if args.jd:
            jd_text = args.jd
        else:
            jd_text = read_jd_from_file(args.jd_file)
        
        if not jd_text.strip():
            print("Error: Job description cannot be empty")
            sys.exit(1)
        
        # Run analysis
        run_analysis(cv_path, jd_text, args.output)
        
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
