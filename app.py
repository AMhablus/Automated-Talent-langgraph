import streamlit as st
import os
import tempfile
import shutil
from pathlib import Path
from src.agent.graph import SharedState, graph
from src.agent.nodes import process_user_inputs

# Page configuration
st.set_page_config(
    page_title="CV Analysis Agent",
    page_icon="📄",
    layout="wide"
)

def main():
    st.title("📄 CV Analysis Agent")
    st.markdown("Upload your CV (PDF) and provide a job description to get an AI-powered analysis.")
    
    # Sidebar for inputs
    with st.sidebar:
        st.header("Inputs")
        
        # File upload for CV
        uploaded_file = st.file_uploader(
            "Upload your CV (PDF)",
            type=['pdf'],
            help="Upload your CV in PDF format"
        )
        
        # Text area for job description
        jd_text = st.text_area(
            "Job Description",
            height=300,
            placeholder="Paste the job description here...",
            help="Enter or paste the complete job description"
        )
        
        # Analysis button
        analyze_button = st.button("🚀 Analyze CV", type="primary", use_container_width=True)
    
    # Main content area
    if uploaded_file is not None and jd_text.strip():
        st.success("✅ Both CV and job description are ready!")
        
        if analyze_button:
            with st.spinner("Analyzing your CV..."):
                try:
                    # Save uploaded file temporarily
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_file_path = tmp_file.name
                    
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
                            "jd_text": jd_text
                        }
                        
                        # Process user inputs
                        shared_state = SharedState(**initial_state)
                        shared_state = process_user_inputs(tmp_file_path, jd_text, shared_state)
                        
                        # Run the analysis
                        result = graph.invoke(shared_state)
                        
                        # Display results
                        st.success("Analysis Complete! 🎉")
                        
                        # Create columns for better layout
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.subheader("📋 Candidate Information")
                            st.write(f"**Name:** {result['name']}")
                            st.write(f"**Email:** {result['email']}")
                            st.write(f"**Phone:** {result['phone']}")
                            st.write(f"**Experience:** {result['years_of_experience']} years")
                            
                            st.subheader("🎯 Skills")
                            skills = result['skills']
                            if isinstance(skills, list):
                                for skill in skills:
                                    st.write(f"• {skill}")
                            else:
                                st.write(skills)
                        
                        with col2:
                            st.subheader("📊 Analysis Results")
                            st.write(f"**Pre-screening Status:** {result['pre_screening_status']}")
                            st.write(f"**Final Decision:** {result['final_decision']}")
                            
                            # Skills analysis
                            if result.get('skills_analysis'):
                                skills_analysis = result['skills_analysis']
                                st.subheader("🔍 Skills Analysis")
                                
                                # Score with progress bar
                                score = skills_analysis.get('score', 0)
                                st.metric("Overall Score", f"{score}/100")
                                st.progress(score / 100)
                                
                                # Skills breakdown
                                if skills_analysis.get('matched'):
                                    st.write("**✅ Matched Skills:**")
                                    for skill in skills_analysis['matched']:
                                        st.write(f"• {skill}")
                                
                                if skills_analysis.get('missing'):
                                    st.write("**❌ Missing Skills:**")
                                    for skill in skills_analysis['missing']:
                                        st.write(f"• {skill}")
                                
                                if skills_analysis.get('additional'):
                                    st.write("**➕ Additional Skills:**")
                                    for skill in skills_analysis['additional']:
                                        st.write(f"• {skill}")
                        
                        # Rejection reason if applicable
                        if result.get('rejection_reason'):
                            st.subheader("📝 Rejection Reason")
                            st.warning(result['rejection_reason'])
                        
                        # Download results
                        st.subheader("💾 Download Results")
                        results_text = f"""
CV Analysis Results

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
                        
                        st.download_button(
                            label="📥 Download Results as Text",
                            data=results_text,
                            file_name=f"cv_analysis_{result['name'].replace(' ', '_')}.txt",
                            mime="text/plain"
                        )
                        
                    finally:
                        # Clean up temporary file
                        if os.path.exists(tmp_file_path):
                            os.unlink(tmp_file_path)
                            
                except Exception as e:
                    st.error(f"❌ Error during analysis: {str(e)}")
                    st.info("Please check your inputs and try again.")
    
    elif uploaded_file is not None:
        st.warning("⚠️ Please provide a job description to continue.")
    elif jd_text.strip():
        st.warning("⚠️ Please upload a CV (PDF) to continue.")
    else:
        st.info("👈 Use the sidebar to upload your CV and provide a job description.")
        
        # Show example
        with st.expander("📖 How to use this tool"):
            st.markdown("""
            **Step 1:** Upload your CV in PDF format using the file uploader in the sidebar.
            
            **Step 2:** Enter or paste the complete job description in the text area.
            
            **Step 3:** Click the "Analyze CV" button to start the AI-powered analysis.
            
            **What you'll get:**
            - Candidate information extraction
            - Skills analysis and matching
            - Pre-screening status
            - Final recommendation (Interview/Phone Screen/Rejected)
            - Detailed skills breakdown
            - Downloadable results
            """)
        
        # Show sample data
        with st.expander("🔍 Sample Analysis"):
            st.markdown("""
            This tool analyzes your CV against a job description to provide:
            
            **Skills Matching:** Identifies which skills from your CV match the job requirements
            **Gap Analysis:** Shows what skills you might be missing
            **Additional Skills:** Highlights extra skills that could be beneficial
            **Overall Score:** Provides a numerical assessment of your fit
            **Recommendation:** Suggests next steps (Interview, Phone Screen, or Rejection)
            """)

if __name__ == "__main__":
    main()
