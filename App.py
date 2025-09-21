import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
import os
import json
import sqlite3
from datetime import datetime, date
import plotly.express as px
import plotly.graph_objects as go
import time
from typing import List, Dict, Any, Tuple
import requests
from streamlit_lottie import st_lottie
import re

# Set page configuration
st.set_page_config(
    page_title="Personalized Career & Skills Advisor",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Lottie animations
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Load Lottie animations
lottie_career = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_vybwn7df.json")
lottie_skills = load_lottieurl("https://assets4.lottiefiles.com/packages/lf20_yo4yviaj.json")
lottie_learning = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_ik9zazrq.json")
lottie_ai = load_lottieurl("https://assets4.lottiefiles.com/packages/lf20_gn0tojcq.json")
lottie_money = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_6xf51jge.json")
lottie_compare = load_lottieurl("https://assets7.lottiefiles.com/packages/lf20_sycynqqu.json")
lottie_roi = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_6gqqcyzu.json")

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #4A90E2;
        text-align: center;
        margin-bottom: 2rem;
        padding: 2rem;
        background: linear-gradient(135deg, #1a2980 0%, #26d0ce 100%);
        border-radius: 16px;
        color: white;
    }
    .sub-header {
        font-size: 1.8rem;
        color: #4A90E2;
        border-bottom: 2px solid #4A90E2;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .feature-card {
        background-color: #f0f7ff;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease;
    }
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
    }
    .role-card {
        background-color: #f9f9f9;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 5px solid #4A90E2;
    }
    .skill-badge {
        background-color: #e6f2ff;
        color: #4A90E2;
        padding: 5px 10px;
        border-radius: 15px;
        margin: 4px;
        display: inline-block;
        font-size: 0.8rem;
    }
    .chat-bubble {
        background-color: #e6f2ff;
        padding: 12px 18px;
        border-radius: 18px;
        margin: 8px 0;
        max-width: 80%;
    }
    .user-bubble {
        background-color: #d9f0d1;
        margin-left: 20%;
    }
    .progress-bar {
        height: 8px;
        background: #e9ecef;
        border-radius: 4px;
        overflow: hidden;
        margin: 10px 0;
    }
    .progress-fill {
        height: 100%;
        background: linear-gradient(135deg, #1a2980 0%, #26d0ce 100%);
        border-radius: 4px;
    }
    .assessment-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
    }
    .salary-tag {
        background: linear-gradient(135deg, #00b09b 0%, #96c93d 100%);
        color: white;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 600;
    }
    .growth-tag {
        background: linear-gradient(135deg, #3498db 0%, #2ecc71 100%);
        color: white;
        padding: 4px 10px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 600;
    }
    .timeline {
        border-left: 3px solid #4A90E2;
        border-bottom-right-radius: 4px;
        border-top-right-radius: 4px;
        margin: 0 auto;
        position: relative;
        padding: 50px;
        list-style: none;
    }
    .event {
        margin-bottom: 50px;
        position: relative;
    }
    .event:before {
        content: "";
        position: absolute;
        width: 20px;
        height: 20px;
        left: -41px;
        top: 0;
        border-radius: 50%;
        background: #4A90E2;
    }
    .date {
        color: #4A90E2;
        font-weight: bold;
    }
    .cert-badge {
        background: linear-gradient(135deg, #f5af19 0%, #f12711 100%);
        color: white;
        padding: 5px 10px;
        border-radius: 15px;
        font-size: 0.8rem;
        display: inline-block;
        margin: 5px;
    }
    .mentor-card {
        background: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 10px 0;
        text-align: center;
    }
    .gamification-badge {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        background: linear-gradient(135deg, #FFE53B 0%, #FF2525 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
        margin: 0 auto 10px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    .industry-card {
        background: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 10px 0;
        transition: transform 0.3s ease;
    }
    .industry-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.2);
    }
    .roi-metric {
        background: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 10px 0;
        text-align: center;
    }
    .comparison-table {
        width: 100%;
        border-collapse: collapse;
        margin: 15px 0;
    }
    .comparison-table th, .comparison-table td {
        border: 1px solid #ddd;
        padding: 8px;
        text-align: left;
    }
    .comparison-table tr:nth-child(even) {
        background-color: #f2f2f2;
    }
    .comparison-table th {
        padding-top: 12px;
        padding-bottom: 12px;
        background-color: #4A90E2;
        color: white;
    }
    .side-hustle-card {
        background: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 10px 0;
        transition: transform 0.3s ease;
    }
    .side-hustle-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state variables
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_email' not in st.session_state:
    st.session_state.user_email = None
if 'current_page' not in st.session_state:
    st.session_state.current_page = "Home"
if 'skills' not in st.session_state:
    st.session_state.skills = []
if 'career_interest' not in st.session_state:
    st.session_state.career_interest = ""
if 'education_level' not in st.session_state:
    st.session_state.education_level = ""
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'learning_path_progress' not in st.session_state:
    st.session_state.learning_path_progress = {}
if 'earned_badges' not in st.session_state:
    st.session_state.earned_badges = []
if 'saved_jobs' not in st.session_state:
    st.session_state.saved_jobs = []
if 'mentor_connections' not in st.session_state:
    st.session_state.mentor_connections = []
if 'selected_career_1' not in st.session_state:
    st.session_state.selected_career_1 = ""
if 'selected_career_2' not in st.session_state:
    st.session_state.selected_career_2 = ""
if 'side_hustle_progress' not in st.session_state:
    st.session_state.side_hustle_progress = {}

# Parse and structure the career data from the PDF
def parse_career_data():
    careers = []
    
    # This is a simplified version - in a real implementation, you would parse the actual PDF content
    # For now, I'll create a structured representation based on the PDF content
    
    career_data = [
        {
            "title": "B.Tech in Artificial Intelligence & Data Science",
            "type": "Engineering",
            "duration": "4 years",
            "eligibility": "Class 11-12 with Physics, Mathematics, and Chemistry/Computer Science",
            "entrance_exams": "JEE Main/Advanced, State CETs, or private university entrance exams",
            "skills": ["Python", "R", "SQL", "Machine Learning", "Deep Learning", "NLP", "Computer Vision"],
            "salary_range": {"starting": "₹4-7 LPA", "mid": "₹10-25 LPA", "senior": "₹30-60 LPA+"},
            "growth_outlook": "Very High",
            "demand": "High",
            "job_roles": ["Data Analyst", "ML Engineer", "AI Developer", "Research Assistant", "Data Scientist", "AI Engineer"],
            "future_trends": ["AI + Robotics", "Generative AI", "Autonomous Systems", "AI in Healthcare"],
            "automation_risk": "Low",
            "stress_level": "Medium",
            "investment_cost": "High",
            "roi_timeline": "3-5 years"
        },
        {
            "title": "B.Sc in Artificial Intelligence & Data Science",
            "type": "Science",
            "duration": "3 years",
            "eligibility": "Class 12 with Mathematics (mandatory) + Physics/Computer Science recommended",
            "entrance_exams": "Mostly merit-based (12th marks), some private universities conduct entrance tests",
            "skills": ["Python", "R", "SQL", "Statistics", "Machine Learning", "Data Visualization"],
            "salary_range": {"starting": "₹3-6 LPA", "mid": "₹8-18 LPA", "senior": "₹20-35 LPA"},
            "growth_outlook": "High",
            "demand": "Medium-High",
            "job_roles": ["Data Analyst", "AI Programmer", "ML Engineer", "Junior Data Scientist"],
            "future_trends": ["Data Analytics", "AI Ethics", "Generative AI", "Cloud AI"],
            "automation_risk": "Low",
            "stress_level": "Medium",
            "investment_cost": "Medium",
            "roi_timeline": "2-4 years"
        },
        {
            "title": "B.Tech in Computer Science (Cybersecurity)",
            "type": "Engineering",
            "duration": "4 years",
            "eligibility": "Class 11-12 with Physics, Mathematics, Chemistry/Computer Science",
            "entrance_exams": "JEE Main/Advanced, State CETs, or university-specific exams",
            "skills": ["Networking", "Linux", "Python", "Cryptography", "Ethical Hacking", "Cloud Security"],
            "salary_range": {"starting": "₹4-8 LPA", "mid": "₹10-25 LPA", "senior": "₹30-60 LPA+"},
            "growth_outlook": "Very High",
            "demand": "High",
            "job_roles": ["Cybersecurity Analyst", "SOC Analyst", "Ethical Hacker", "Security Consultant"],
            "future_trends": ["Cloud Security", "AI in Cybersecurity", "IoT Security", "Zero Trust Architecture"],
            "automation_risk": "Low",
            "stress_level": "High",
            "investment_cost": "High",
            "roi_timeline": "3-5 years"
        },
        {
            "title": "B.Tech in Computer Science (IoT)",
            "type": "Engineering",
            "duration": "4 years",
            "eligibility": "Class 11-12 with Physics, Mathematics, Chemistry/Computer Science/Electronics",
            "entrance_exams": "JEE Main/Advanced, State CETs, or private university tests",
            "skills": ["Python", "C/C++", "Embedded Systems", "Cloud IoT", "Networking", "Data Analytics"],
            "salary_range": {"starting": "₹3.5-7 LPA", "mid": "₹10-20 LPA", "senior": "₹25-45 LPA"},
            "growth_outlook": "High",
            "demand": "Medium-High",
            "job_roles": ["IoT Developer", "Embedded Engineer", "Firmware Developer", "IoT Solutions Architect"],
            "future_trends": ["5G", "Smart Wearables", "Autonomous Vehicles", "Edge IoT"],
            "automation_risk": "Medium",
            "stress_level": "Medium",
            "investment_cost": "High",
            "roi_timeline": "4-6 years"
        },
        {
            "title": "B.Tech in Computer Science (Blockchain)",
            "type": "Engineering",
            "duration": "4 years",
            "eligibility": "Class 11-12 with Physics, Mathematics, Chemistry/Computer Science",
            "entrance_exams": "JEE Main/Advanced, State CETs, or private entrance exams",
            "skills": ["Solidity", "Ethereum", "Smart Contracts", "Cryptography", "Node.js", "Web3.js"],
            "salary_range": {"starting": "₹5-9 LPA", "mid": "₹12-25 LPA", "senior": "₹30-60 LPA+"},
            "growth_outlook": "Very High",
            "demand": "High",
            "job_roles": ["Blockchain Developer", "Smart Contract Engineer", "Crypto Analyst", "Web3 Architect"],
            "future_trends": ["Web3", "DeFi", "NFTs", "Metaverse", "CBDCs"],
            "automation_risk": "Low",
            "stress_level": "Medium-High",
            "investment_cost": "High",
            "roi_timeline": "3-5 years"
        },
        {
            "title": "B.Tech in Computer Science (Cloud Computing)",
            "type": "Engineering",
            "duration": "4 years",
            "eligibility": "Class 11-12 with Physics, Mathematics, and Chemistry/Computer Science",
            "entrance_exams": "JEE Main/Advanced, State CETs, or university-specific entrance exams",
            "skills": ["AWS", "Azure", "GCP", "Kubernetes", "Docker", "Linux", "Networking"],
            "salary_range": {"starting": "₹4-8 LPA", "mid": "₹12-25 LPA", "senior": "₹30-60 LPA+"},
            "growth_outlook": "Very High",
            "demand": "High",
            "job_roles": ["Cloud Engineer", "DevOps Specialist", "Solutions Architect", "Cloud Security Expert"],
            "future_trends": ["Cloud + AI", "Cloud + Blockchain", "Edge Computing", "Multi-Cloud Solutions"],
            "automation_risk": "Medium",
            "stress_level": "Medium",
            "investment_cost": "High",
            "roi_timeline": "3-5 years"
        },
        {
            "title": "B.Sc in Data Analytics",
            "type": "Science",
            "duration": "3 years",
            "eligibility": "Class 12 with Mathematics (mandatory) + Statistics/Computer Science preferred",
            "entrance_exams": "Mostly merit-based, some private universities conduct entrance tests",
            "skills": ["Python", "R", "SQL", "Excel", "Statistics", "Data Visualization"],
            "salary_range": {"starting": "₹3-6 LPA", "mid": "₹8-15 LPA", "senior": "₹18-30 LPA"},
            "growth_outlook": "High",
            "demand": "High",
            "job_roles": ["Data Analyst", "Business Intelligence Specialist", "Reporting Analyst", "Junior Data Scientist"],
            "future_trends": ["Data-Driven Decision Making", "AI", "Big Data Analytics", "Cloud Analytics"],
            "automation_risk": "Medium",
            "stress_level": "Medium",
            "investment_cost": "Medium",
            "roi_timeline": "2-4 years"
        },
        {
            "title": "BCA in Data Analytics",
            "type": "Computer Applications",
            "duration": "3 years",
            "eligibility": "Class 12 with Mathematics or Computer Science/Applications",
            "entrance_exams": "Usually merit-based; some private universities hold entrance tests",
            "skills": ["Python", "R", "SQL", "Java", "Excel", "Big Data basics"],
            "salary_range": {"starting": "₹3-6 LPA", "mid": "₹8-15 LPA", "senior": "₹18-28 LPA"},
            "growth_outlook": "High",
            "demand": "Medium-High",
            "job_roles": ["Data Analyst", "BI Developer", "Junior Data Scientist", "SQL Developer"],
            "future_trends": ["Data Engineering + Analytics fusion", "Cloud Analytics", "AI-driven BI"],
            "automation_risk": "Medium",
            "stress_level": "Medium",
            "investment_cost": "Medium",
            "roi_timeline": "2-4 years"
        },
        {
            "title": "MBA (General / Global / Executive)",
            "type": "Management",
            "duration": "2 years",
            "eligibility": "Graduation (any stream) with 50-60% marks",
            "entrance_exams": "CAT, XAT, GMAT, GRE, MAT, SNAP, NMAT, or institute-level",
            "skills": ["Leadership", "Business Strategy", "Financial Analysis", "Marketing", "Operations"],
            "salary_range": {"starting": "₹8-25 LPA", "mid": "₹15-40 LPA", "senior": "₹30-80 LPA+"},
            "growth_outlook": "High",
            "demand": "High",
            "job_roles": ["Management Trainee", "Business Analyst", "Consultant", "Product Manager"],
            "future_trends": ["Tech + Business blend", "Digital transformation", "Global leadership roles"],
            "automation_risk": "Low",
            "stress_level": "High",
            "investment_cost": "Very High",
            "roi_timeline": "4-7 years"
        },
        {
            "title": "BBA (General)",
            "type": "Management",
            "duration": "3 years",
            "eligibility": "Class 12 (any stream, commerce preferred)",
            "entrance_exams": "CUET, IPU-CET, SET, Christ University Test, or direct admission",
            "skills": ["MS Office", "Communication", "Leadership", "Basic Accounting", "Business Fundamentals"],
            "salary_range": {"starting": "₹3-5 LPA", "mid": "₹7-12 LPA", "senior": "₹15-30 LPA"},
            "growth_outlook": "Medium",
            "demand": "Medium",
            "job_roles": ["Management Trainee", "HR Assistant", "Marketing Executive", "Business Analyst"],
            "future_trends": ["Digital marketing", "E-commerce management", "Business analytics"],
            "automation_risk": "Medium",
            "stress_level": "Medium",
            "investment_cost": "Medium",
            "roi_timeline": "3-5 years"
        }
    ]
    
    return career_data

# Sample data for careers (using the parsed data)
CAREERS_DATA = parse_career_data()

# Sample industry trends data
INDUSTRY_TRENDS = {
    "Technology": {
        "growth": "Very High",
        "trends": ["AI/ML Integration", "Cloud Migration", "Remote Work Tools", "Cybersecurity Focus"],
        "in_demand_skills": ["Python", "Cloud Computing", "Machine Learning", "DevOps", "React"],
        "future_outlook": "Continued rapid growth with digital transformation across all sectors"
    },
    "Healthcare": {
        "growth": "High",
        "trends": ["Telemedicine", "Health Tech", "Personalized Medicine", "AI Diagnostics"],
        "in_demand_skills": ["Data Analysis", "Healthcare IT", "Regulatory Knowledge", "Patient Care Systems"],
        "future_outlook": "Strong growth with aging populations and health tech innovation"
    },
    "Finance": {
        "growth": "Medium",
        "trends": ["FinTech", "Blockchain", "Digital Banking", "Automated Investing"],
        "in_demand_skills": ["Financial Modeling", "Data Analysis", "Risk Management", "Python/R"],
        "future_outlook": "Transformation through technology with focus on digital services"
    },
    "Marketing": {
        "growth": "High",
        "trends": ["AI-Personalization", "Influencer Marketing", "Video Content", "Data-Driven Campaigns"],
        "in_demand_skills": ["Digital Marketing", "Data Analysis", "Content Creation", "SEO/SEM"],
        "future_outlook": "Evolution toward data-driven, personalized marketing approaches"
    },
    "Education": {
        "growth": "Medium",
        "trends": ["EdTech", "Online Learning", "Personalized Education", "Skills-Based Training"],
        "in_demand_skills": ["Instructional Design", "E-Learning Platforms", "Data Analysis", "Curriculum Development"],
        "future_outlook": "Transformation through technology with focus on lifelong learning"
    }
}

# Sample mentors data
MENTORS = [
    {
        "name": "Rajesh Kumar",
        "role": "Senior Data Scientist",
        "company": "TechCorp India",
        "experience": "8 years",
        "skills": ["Python", "Machine Learning", "Data Visualization", "Big Data"],
        "availability": "Weekends",
        "rating": 4.8,
        "sessions": 45
    },
    {
        "name": "Priya Sharma",
        "role": "Lead UX Designer",
        "company": "DesignStudio",
        "experience": "10 years",
        "skills": ["UI/UX Design", "Figma", "User Research", "Product Strategy"],
        "availability": "Weekdays evenings",
        "rating": 4.9,
        "sessions": 32
    },
    {
        "name": "Amit Patel",
        "role": "Cloud Architect",
        "company": "CloudSolutions Inc",
        "experience": "12 years",
        "skills": ["AWS", "Azure", "DevOps", "Kubernetes", "Infrastructure"],
        "availability": "Flexible",
        "rating": 4.7,
        "sessions": 28
    },
    {
        "name": "Sneha Reddy",
        "role": "Product Manager",
        "company": "TechStartup",
        "experience": "6 years",
        "skills": ["Product Strategy", "Agile", "Market Research", "Data Analysis"],
        "availability": "Weekdays",
        "rating": 4.6,
        "sessions": 19
    }
]

# Sample job postings
JOB_POSTINGS = [
    {
        "title": "Frontend Developer",
        "company": "WebTech Solutions",
        "location": "Bangalore",
        "experience": "2-4 years",
        "skills": ["React", "JavaScript", "CSS", "HTML5"],
        "salary": "₹6-10 LPA",
        "posted": "2 days ago"
    },
    {
        "title": "Data Scientist",
        "company": "DataInsights Pvt Ltd",
        "location": "Hyderabad",
        "experience": "3-5 years",
        "skills": ["Python", "Machine Learning", "SQL", "Statistics"],
        "salary": "₹8-15 LPA",
        "posted": "5 days ago"
    },
    {
        "title": "DevOps Engineer",
        "company": "CloudInfra Services",
        "location": "Pune",
        "experience": "4-6 years",
        "skills": ["AWS", "Docker", "Kubernetes", "CI/CD"],
        "salary": "₹10-18 LPA",
        "posted": "1 week ago"
    },
    {
        "title": "UX Designer",
        "company": "CreativeMinds",
        "location": "Mumbai",
        "experience": "2-5 years",
        "skills": ["Figma", "UI/UX", "Wireframing", "User Research"],
        "salary": "₹5-12 LPA",
        "posted": "3 days ago"
    }
]

# Side hustle data
SIDE_HUSTLES = [
    {
        "title": "Freelance Web Development",
        "skills": ["HTML", "CSS", "JavaScript", "React"],
        "earning_potential": "₹15,000 - ₹50,000/month",
        "time_commitment": "10-20 hours/week",
        "platforms": ["Upwork", "Fiverr", "Freelancer.com"],
        "career_relevance": ["Frontend Developer", "Full Stack Developer", "Web Developer"],
        "description": "Build websites and web applications for clients on freelance platforms."
    },
    {
        "title": "Data Analysis Projects",
        "skills": ["Python", "Pandas", "Data Visualization", "Excel"],
        "earning_potential": "₹10,000 - ₹40,000/month",
        "time_commitment": "5-15 hours/week",
        "platforms": ["Kaggle", "Upwork", "Toptal"],
        "career_relevance": ["Data Analyst", "Data Scientist", "Business Analyst"],
        "description": "Take on data analysis projects to help businesses make data-driven decisions."
    },
    {
        "title": "Content Writing",
        "skills": ["Writing", "Research", "SEO", "Grammar"],
        "earning_potential": "₹8,000 - ₹30,000/month",
        "time_commitment": "5-20 hours/week",
        "platforms": ["Contentfly", "Upwork", "Blogging"],
        "career_relevance": ["Digital Marketing", "Content Marketing", "Technical Writing"],
        "description": "Create blog posts, articles, and website content for businesses and publications."
    },
    {
        "title": "Social Media Management",
        "skills": ["Social Media", "Content Creation", "Analytics", "Marketing"],
        "earning_potential": "₹12,000 - ₹45,000/month",
        "time_commitment": "10-15 hours/week",
        "platforms": ["Upwork", "Fiverr", "Local Businesses"],
        "career_relevance": ["Digital Marketing", "Social Media Marketing", "Brand Management"],
        "description": "Manage social media accounts for businesses and create engaging content."
    },
    {
        "title": "Tutoring",
        "skills": ["Teaching", "Subject Expertise", "Communication", "Patience"],
        "earning_potential": "₹200 - ₹500/hour",
        "time_commitment": "5-15 hours/week",
        "platforms": ["Chegg", "Vedantu", "Byju's", "Private Tutoring"],
        "career_relevance": ["Education", "Teaching", "Subject Matter Expert"],
        "description": "Teach subjects you're proficient in to students of various levels."
    },
    {
        "title": "Graphic Design",
        "skills": ["Adobe Photoshop", "Illustrator", "Design Principles", "Creativity"],
        "earning_potential": "₹15,000 - ₹50,000/month",
        "time_commitment": "10-20 hours/week",
        "platforms": ["99designs", "Fiverr", "Upwork"],
        "career_relevance": ["Graphic Designer", "UI/UX Designer", "Visual Designer"],
        "description": "Create logos, banners, and other visual content for clients."
    }
]

# Gamification badges
BADGES = [
    {"name": "Skill Master", "description": "Achieved proficiency in 10+ skills", "icon": "🏆"},
    {"name": "Career Explorer", "description": "Explored 5+ career paths", "icon": "🔍"},
    {"name": "Learning Champion", "description": "Completed 3 learning paths", "icon": "📚"},
    {"name": "Assessment Guru", "description": "Completed all skill assessments", "icon": "📊"},
    {"name": "Mentorship Seeker", "description": "Connected with a mentor", "icon": "👥"},
    {"name": "Job Hunter", "description": "Applied to 5+ jobs", "icon": "💼"},
    {"name": "ROI Analyst", "description": "Analyzed ROI for 3+ careers", "icon": "📈"},
    {"name": "Comparison Pro", "description": "Compared 5+ career paths", "icon": "⚖️"},
    {"name": "Side Hustler", "description": "Started 2+ side hustles", "icon": "💰"}
]

# Authentication functions
def show_login_page():
    st.markdown("""
    <style>
    .auth-container {
        max-width: 400px;
        margin: 2rem auto;
        padding: 2rem;
        background: white;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .auth-header {
        text-align: center;
        color: #4A90E2;
        margin-bottom: 2rem;
    }
    .auth-button {
        background-color: #4A90E2;
        color: white;
        border: none;
        padding: 0.75rem 1rem;
        border-radius: 6px;
        cursor: pointer;
        font-size: 1rem;
        margin-top: 1rem;
        width: 100%;
    }
    .auth-button:hover {
        background-color: #3a80d2;
    }
    .auth-switch {
        text-align: center;
        margin-top: 1.5rem;
        color: #666;
    }
    .auth-switch a {
        color: #4A90E2;
        text-decoration: none;
        cursor: pointer;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="auth-header"><h1>🔐 Login</h1></div>', unsafe_allow_html=True)
    
    with st.form("login_form"):
        email = st.text_input("📧 Email", placeholder="Enter your email")
        password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
        
        login_btn = st.form_submit_button("Login", use_container_width=True)
        
        if login_btn:
            # Simple authentication for demo
            if email and password:
                st.session_state.logged_in = True
                st.session_state.user_email = email
                st.success("Login successful! Redirecting...")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Please enter both email and password")
    
    st.markdown(
        '<div class="auth-switch">Don\'t have an account? <a>Sign up here</a></div>', 
        unsafe_allow_html=True
    )

def show_signup_page():
    st.markdown("""
    <style>
    .auth-container {
        max-width: 400px;
        margin: 2rem auto;
        padding: 2rem;
        background: white;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .auth-header {
        text-align: center;
        color: #4A90E2;
        margin-bottom: 2rem;
    }
    .auth-button {
        background-color: #4A90E2;
        color: white;
        border: none;
        padding: 0.75rem 1rem;
        border-radius: 6px;
        cursor: pointer;
        font-size: 1rem;
        margin-top: 1rem;
        width: 100%;
    }
    .auth-button:hover {
        background-color: #3a80d2;
    }
    .auth-switch {
        text-align: center;
        margin-top: 1.5rem;
        color: #666;
    }
    .auth-switch a {
        color: #4A90E2;
        text-decoration: none;
        cursor: pointer;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="auth-header"><h1>👤 Sign Up</h1></div>', unsafe_allow_html=True)
    
    with st.form("signup_form"):
        name = st.text_input("👤 Full Name", placeholder="Enter your full name")
        email = st.text_input("📧 Email", placeholder="Enter your email")
        password = st.text_input("🔒 Password", type="password", placeholder="Create a password")
        confirm_password = st.text_input("🔒 Confirm Password", type="password", placeholder="Confirm your password")
        
        signup_btn = st.form_submit_button("Create Account", use_container_width=True)
        
        if signup_btn:
            # Simple validation for demo
            if name and email and password and password == confirm_password:
                st.success("Account created successfully! You can now login.")
                st.session_state.auth_page = "login"
                time.sleep(1)
                st.rerun()
            else:
                st.error("Please fill all fields correctly and ensure passwords match")
    
    st.markdown(
        '<div class="auth-switch">Already have an account? <a>Login here</a></div>', 
        unsafe_allow_html=True
    )

# Navigation function
def navigate_to(page):
    st.session_state.current_page = page

# Home Page
def home_page():
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="main-header">🎯 Personalized Career & Skills Advisor</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h3>Your AI-powered career guidance platform</h3>
            <p>Discover your career path, develop in-demand skills, and achieve your professional goals</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if lottie_career:
            st_lottie(lottie_career, height=200, key="career-lottie")
    
    # Quick actions
    st.markdown("### Quick Access")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📊 Skills Assessment", use_container_width=True):
            navigate_to("Skills Assessment")
    with col2:
        if st.button("💼 Career Matches", use_container_width=True):
            navigate_to("Career Matches")
    with col3:
        if st.button("📚 Learning Paths", use_container_width=True):
            navigate_to("Learning Paths")
    with col4:
        if st.button("🤖 Career Coach", use_container_width=True):
            navigate_to("Career Coach")
    
    # New features highlights
    st.markdown("### 🚀 New Features")
    
    new_features = [
        {
            "title": "ROI Analysis",
            "description": "Calculate Return on Investment for different career paths",
            "icon": "📈",
            "action": "ROI Analysis"
        },
        {
            "title": "Career Comparison",
            "description": "Compare different careers side-by-side",
            "icon": "⚖️",
            "action": "Career Comparison"
        },
        {
            "title": "Side Hustles",
            "description": "Find part-time jobs and gigs to earn while learning",
            "icon": "💰",
            "action": "Side Hustles"
        }
    ]
    
    cols = st.columns(3)
    for i, feature in enumerate(new_features):
        with cols[i]:
            st.markdown(f"""
            <div class="feature-card">
                <div style="font-size: 2rem; margin-bottom: 1rem;">{feature['icon']}</div>
                <h3>{feature['title']}</h3>
                <p>{feature['description']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Explore", key=f"feature_{i}", use_container_width=True):
                navigate_to(feature['action'])
    
    # Features
    st.markdown("### How We Help You")
    
    features = [
        {
            "title": "Personalized Career Matching",
            "description": "Discover careers that align with your skills, interests, and goals",
            "icon": "🎯"
        },
        {
            "title": "Skills Gap Analysis",
            "description": "Identify the skills you need to develop for your target roles",
            "icon": "📊"
        },
        {
            "title": "Learning Roadmaps",
            "description": "Get customized learning paths with recommended resources",
            "icon": "🛣️"
        },
        {
            "title": "AI Career Coaching",
            "description": "Get answers to your career questions from our AI assistant",
            "icon": "🤖"
        },
        {
            "title": "Industry Insights",
            "description": "Stay updated with the latest industry trends and job market data",
            "icon": "📈"
        },
        {
            "title": "Mentor Connections",
            "description": "Connect with experienced professionals in your field of interest",
            "icon": "👥"
        }
    ]
    
    cols = st.columns(3)
    for i, feature in enumerate(features):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="feature-card">
                <div style="font-size: 2rem; margin-bottom: 1rem;">{feature['icon']}</div>
                <h3>{feature['title']}</h3>
                <p>{feature['description']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Stats
    st.markdown("### Our Impact")
    stats_cols = st.columns(4)
    stats = [
        {"number": "10,000+", "label": "Users Helped"},
        {"number": "50+", "label": "Career Paths"},
        {"number": "100+", "label": "Skills Tracked"},
        {"number": "95%", "label": "Satisfaction Rate"}
    ]
    
    for i, stat in enumerate(stats):
        with stats_cols[i]:
            st.markdown(f"""
            <div style="text-align: center; padding: 1rem;">
                <div style="font-size: 2rem; font-weight: bold; color: #4A90E2;">{stat['number']}</div>
                <div style="color: #666;">{stat['label']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Testimonials
    st.markdown("### Success Stories")
    testimonials = [
        {
            "text": "The career matching helped me transition from marketing to product management seamlessly!",
            "name": "Priya S.",
            "role": "Product Manager"
        },
        {
            "text": "The skills assessment identified exactly what I needed to learn to advance my career.",
            "name": "Rahul K.",
            "role": "Data Scientist"
        },
        {
            "text": "The learning paths saved me months of research and helped me focus on what really matters.",
            "name": "Anjali M.",
            "role": "UX Designer"
        }
    ]
    
    testimonial_cols = st.columns(3)
    for i, testimonial in enumerate(testimonials):
        with testimonial_cols[i]:
            st.markdown(f"""
            <div style="background: #f9f9f9; padding: 1.5rem; border-radius: 10px; height: 200px;">
                <p style="font-style: italic;">"{testimonial['text']}"</p>
                <div style="margin-top: 1rem;">
                    <strong>{testimonial['name']}</strong><br>
                    <span style="color: #666;">{testimonial['role']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

# Skills Assessment Page
def skills_assessment():
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("### 📊 Skills Assessment")
        st.info("Evaluate your current skills and identify areas for development")
    
    with col2:
        if lottie_skills:
            st_lottie(lottie_skills, height=150, key="skills-lottie")
    
    # Initialize session state for assessment results
    if 'assessment_results' not in st.session_state:
        st.session_state.assessment_results = {}
    
    # Skills categories
    skill_categories = {
        "Programming Languages": ["Python", "JavaScript", "Java", "C++", "C#", "Ruby", "Go", "Rust", "TypeScript", "PHP"],
        "Frontend Development": ["HTML", "CSS", "React", "Vue", "Angular", "Svelte", "Bootstrap", "Tailwind CSS", "jQuery"],
        "Backend Development": ["Node.js", "Django", "Flask", "Spring", "Express", "Ruby on Rails", "Laravel", ".NET", "FastAPI"],
        "Database": ["SQL", "MySQL", "PostgreSQL", "MongoDB", "Redis", "Oracle", "SQLite", "Cassandra", "Firebase"],
        "DevOps & Cloud": ["Docker", "Kubernetes", "AWS", "Azure", "GCP", "CI/CD", "Terraform", "Ansible", "Jenkins", "Linux"],
        "Data Science & AI": ["Pandas", "NumPy", "TensorFlow", "PyTorch", "Scikit-learn", "ML", "Data Visualization", "NLP", "Computer Vision"],
        "Soft Skills": ["Communication", "Teamwork", "Problem Solving", "Leadership", "Time Management", "Adaptability", "Creativity"]
    }
    
    # Skills assessment form
    with st.form("skills_form"):
        st.markdown("#### Rate your proficiency for each skill (1-5)")
        st.caption("1 = Beginner, 3 = Intermediate, 5 = Expert")
        
        skills_assessment = {}
        
        for category, skills in skill_categories.items():
            st.markdown(f"##### {category}")
            for skill in skills:
                skills_assessment[skill] = st.slider(
                    skill, 1, 5, 3,
                    key=f"skill_{skill}",
                    help=f"Rate your proficiency in {skill}"
                )
        
        submitted = st.form_submit_button("Submit Assessment", type="primary")
        
        if submitted:
            st.session_state.assessment_results = skills_assessment
            st.success("Assessment submitted successfully!")
            
            # Calculate scores by category
            category_scores = {}
            for category, skills in skill_categories.items():
                category_score = sum(skills_assessment[skill] for skill in skills) / len(skills)
                category_scores[category] = category_score
            
            # Display results
            st.markdown("### Assessment Results")
            
            # Overall score
            overall_score = sum(skills_assessment.values()) / len(skills_assessment)
            st.metric("Overall Skills Score", f"{overall_score:.1f}/5.0")
            
            # Category scores chart
            category_df = pd.DataFrame({
                "Category": list(category_scores.keys()),
                "Score": list(category_scores.values())
            })
            
            fig = px.bar(category_df, x="Category", y="Score", title="Skills by Category",
                        color="Score", color_continuous_scale="Blues")
            st.plotly_chart(fig, use_container_width=True)
            
            # Top skills
            top_skills = sorted(skills_assessment.items(), key=lambda x: x[1], reverse=True)[:5]
            st.markdown("#### Your Top Skills")
            for skill, score in top_skills:
                st.markdown(f"- {skill}: {score}/5")
            
            # Skills to improve
            improve_skills = sorted(skills_assessment.items(), key=lambda x: x[1])[:5]
            st.markdown("#### Skills to Improve")
            for skill, score in improve_skills:
                st.markdown(f"- {skill}: {score}/5")
            
            # Save to session state
            st.session_state.skills = [skill for skill, score in skills_assessment.items() if score >= 3]
            
            # Check for badges
            if len(st.session_state.skills) >= 10 and "Skill Master" not in st.session_state.earned_badges:
                st.session_state.earned_badges.append("Skill Master")
                st.success("🎉 You earned the Skill Master badge!")
            
            if "Assessment Guru" not in st.session_state.earned_badges:
                st.session_state.earned_badges.append("Assessment Guru")
                st.success("🎉 You earned the Assessment Guru badge!")

# Career Matches Page
def career_matches():
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("### 💼 Career Matches")
        st.info("Discover careers that match your skills and interests")
    
    with col2:
        if lottie_career:
            st_lottie(lottie_career, height=150, key="career-matches-lottie")
    
    # Get user skills from session state or use default
    user_skills = st.session_state.get('skills', [])
    
    if not user_skills:
        st.warning("Please complete the skills assessment first to get personalized career matches")
        if st.button("Take Skills Assessment"):
            navigate_to("Skills Assessment")
        return
    
    # Career matching algorithm
    def calculate_match_score(career, user_skills):
        career_skills = career['skills']
        matched_skills = set(user_skills) & set(career_skills)
        return len(matched_skills) / len(career_skills) * 100
    
    # Calculate match scores for all careers
    career_matches = []
    for career in CAREERS_DATA:
        match_score = calculate_match_score(career, user_skills)
        career_matches.append({
            'role': career['title'],
            'description': career.get('description', 'No description available'),
            'skills': career['skills'],
            'salary_range': career['salary_range']['starting'],
            'growth_outlook': career['growth_outlook'],
            'experience_level': career.get('experience_level', 'Varies'),
            'demand': career['demand'],
            'industry': career.get('industry', 'Technology'),
            'future_trend': career.get('future_trends', ['Emerging field'])[0] if career.get('future_trends') else 'Emerging field',
            'match_score': match_score,
            'full_data': career
        })
    
    # Sort by match score
    career_matches.sort(key=lambda x: x['match_score'], reverse=True)
    
    # Display top matches
    st.markdown(f"#### Top Career Matches for Your Skills")
    
    for career in career_matches[:5]:
        st.markdown(f"""
        <div class="role-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h3>{career['role']}</h3>
                <div style="background: #4A90E2; color: white; padding: 5px 10px; border-radius: 15px;">
                    {career['match_score']:.0f}% Match
                </div>
            </div>
            <p>{career['description']}</p>
            <div style="display: flex; gap: 10px; margin-bottom: 10px;">
                <span class="salary-tag">Salary: {career['salary_range']}</span>
                <span class="growth-tag">Growth: {career['growth_outlook']}</span>
                <span class="skill-badge">Demand: {career['demand']}</span>
                <span class="skill-badge">Industry: {career['industry']}</span>
            </div>
            <div>
                <p style="margin-bottom: 5px;"><strong>Key Skills:</strong></p>
                <div>{"".join([f'<span class="skill-badge">{skill}</span>' for skill in career['skills'][:5]])}</div>
            </div>
            {f'<p style="margin-top: 10px;"><strong>Future Trend:</strong> {career["future_trend"]}</p>' if career.get("future_trend") else ""}
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            if st.button("View Learning Path", key=f"path_{career['role']}"):
                st.session_state.selected_career = career['role']
                navigate_to("Learning Paths")
        with col2:
            if st.button("ROI Analysis", key=f"roi_{career['role']}"):
                st.session_state.selected_career = career['role']
                navigate_to("ROI Analysis")
        with col3:
            if st.button("Save Career", key=f"save_{career['role']}"):
                if career['role'] not in st.session_state.saved_jobs:
                    st.session_state.saved_jobs.append(career['role'])
                    st.success(f"Saved {career['role']} to your profile!")
        with col4:
            if st.button("Find Mentor", key=f"mentor_{career['role']}"):
                navigate_to("Mentor Connect")
        st.markdown("---")
    
    # Career exploration
    st.markdown("### 🔍 Explore All Careers")
    
    # Filter options
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        industry_filter = st.selectbox("Industry", ["All"] + list(set([c.get('industry', 'Technology') for c in CAREERS_DATA])))
    with col2:
        growth_filter = st.selectbox("Growth Outlook", ["All", "Very High", "High", "Medium"])
    with col3:
        demand_filter = st.selectbox("Demand", ["All", "High", "Medium-High", "Medium"])
    with col4:
        type_filter = st.selectbox("Program Type", ["All"] + list(set([c.get('type', 'Engineering') for c in CAREERS_DATA])))
    
    # Filter careers
    filtered_careers = career_matches
    if industry_filter != "All":
        filtered_careers = [c for c in filtered_careers if c['industry'] == industry_filter]
    if growth_filter != "All":
        filtered_careers = [c for c in filtered_careers if c['growth_outlook'] == growth_filter]
    if demand_filter != "All":
        filtered_careers = [c for c in filtered_careers if c['demand'] == demand_filter]
    if type_filter != "All":
        filtered_careers = [c for c in filtered_careers if c['full_data'].get('type') == type_filter]
    
    # Display filtered careers
    for career in filtered_careers:
        with st.expander(f"{career['role']} ({career['match_score']:.0f}% Match)"):
            st.markdown(f"**Description:** {career['description']}")
            st.markdown(f"**Salary Range:** {career['salary_range']}")
            st.markdown(f"**Growth Outlook:** {career['growth_outlook']}")
            st.markdown(f"**Demand:** {career['demand']}")
            st.markdown(f"**Industry:** {career['industry']}")
            st.markdown(f"**Program Type:** {career['full_data'].get('type', 'N/A')}")
            st.markdown(f"**Duration:** {career['full_data'].get('duration', 'N/A')}")
            
            if career.get('future_trend'):
                st.markdown(f"**Future Trend:** {career['future_trend']}")
            
            st.markdown("**Key Skills:**")
            cols = st.columns(3)
            for i, skill in enumerate(career['skills']):
                with cols[i % 3]:
                    st.markdown(f"- {skill}")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("View Learning Path", key=f"path2_{career['role']}"):
                    st.session_state.selected_career = career['role']
                    navigate_to("Learning Paths")
            with col2:
                if st.button("ROI Analysis", key=f"roi2_{career['role']}"):
                    st.session_state.selected_career = career['role']
                    navigate_to("ROI Analysis")

# Learning Paths Page
def learning_paths():
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("### 📚 Learning Paths")
        st.info("Customized learning roadmaps for your target career")
    
    with col2:
        if lottie_learning:
            st_lottie(lottie_learning, height=150, key="learning-lottie")
    
    # Get selected career from session state or let user choose
    selected_career = st.session_state.get('selected_career', "")
    
    if not selected_career:
        st.markdown("#### Select a career to view its learning path")
        career_options = [career['title'] for career in CAREERS_DATA]
        selected_career = st.selectbox("Choose a career", career_options)
    
    if selected_career:
        # Find the career data
        career_data = next((career for career in CAREERS_DATA if career['title'] == selected_career), None)
        
        if career_data:
            st.markdown(f"### Learning Path for {selected_career}")
            st.markdown(f"**Description:** {career_data.get('description', 'No description available')}")
            
            # Display career info
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Salary Range", career_data['salary_range']['starting'])
            with col2:
                st.metric("Growth Outlook", career_data['growth_outlook'])
            with col3:
                st.metric("Demand", career_data['demand'])
            with col4:
                st.metric("Duration", career_data.get('duration', 'N/A'))
            
            # Initialize progress tracking
            if selected_career not in st.session_state.learning_path_progress:
                st.session_state.learning_path_progress[selected_career] = {
                    "Foundation": 0,
                    "Core Skills": 0,
                    "Specialization": 0,
                    "Projects & Portfolio": 0
                }
            
            # Learning path
            st.markdown("#### 📖 Learning Roadmap")
            
            # Sample learning path (in a real app, this would be more detailed)
            path_stages = [
                {
                    "stage": "Foundation",
                    "duration": "1-2 months",
                    "topics": ["Basic programming concepts", "Version control with Git", "Introduction to algorithms"],
                    "resources": ["Codecademy: Learn to Code", "freeCodeCamp: Responsive Web Design", "Coursera: Programming Fundamentals"]
                },
                {
                    "stage": "Core Skills",
                    "duration": "3-4 months",
                    "topics": career_data['skills'][:4],
                    "resources": ["Udacity: Full Stack Developer", "edX: Computer Science", "Pluralsight: Paths"]
                },
                {
                    "stage": "Specialization",
                    "duration": "2-3 months",
                    "topics": career_data['skills'][4:8] if len(career_data['skills']) > 4 else career_data['skills'],
                    "resources": ["LinkedIn Learning: Career Paths", "Udemy: Master Classes", "Official documentation and tutorials"]
                },
                {
                    "stage": "Projects & Portfolio",
                    "duration": "1-2 months",
                    "topics": ["Build real-world projects", "Contribute to open source", "Create portfolio website"],
                    "resources": ["GitHub: Open Source Projects", "Behance/Dribbble for design inspiration", "Personal blog to document learning"]
                }
            ]
            
            for i, stage in enumerate(path_stages):
                with st.expander(f"Stage {i+1}: {stage['stage']} ({stage['duration']})"):
                    st.markdown("**Topics to cover:**")
                    for topic in stage['topics']:
                        st.markdown(f"- {topic}")
                    
                    st.markdown("**Recommended resources:**")
                    for resource in stage['resources']:
                        st.markdown(f"- {resource}")
                    
                    # Progress tracking for each stage
                    progress = st.slider(f"Progress for {stage['stage']}", 0, 100, 
                                        st.session_state.learning_path_progress[selected_career][stage['stage']],
                                        key=f"progress_{selected_career}_{stage['stage']}")
                    
                    st.session_state.learning_path_progress[selected_career][stage['stage']] = progress
                    st.progress(progress / 100)
            
            # Overall progress
            total_progress = sum(st.session_state.learning_path_progress[selected_career].values()) / 4
            st.metric("Overall Progress", f"{total_progress:.1f}%")
            st.progress(total_progress / 100)
            
            # Check for badge
            if total_progress >= 70 and "Learning Champion" not in st.session_state.earned_badges:
                st.session_state.earned_badges.append("Learning Champion")
                st.success("🎉 You earned the Learning Champion badge!")
            
            # Skills comparison
            st.markdown("#### 📊 Skills Comparison")
            
            user_skills = st.session_state.get('skills', [])
            career_skills = career_data['skills']
            
            # Calculate skills gap
            missing_skills = set(career_skills) - set(user_skills)
            strong_skills = set(career_skills) & set(user_skills)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("##### ✅ Your Strong Skills")
                if strong_skills:
                    for skill in list(strong_skills)[:5]:
                        st.markdown(f"- {skill}")
                else:
                    st.info("Complete the skills assessment to see your strong skills")
            
            with col2:
                st.markdown("##### 📝 Skills to Develop")
                if missing_skills:
                    for skill in list(missing_skills)[:5]:
                        st.markdown(f"- {skill}")
                else:
                    st.success("You have all the required skills for this career!")
            
            # Resource recommendations
            st.markdown("#### 🎯 Recommended Learning Resources")
            
            resources = [
                {"name": "Coursera", "description": "Professional certificates from top universities", "url": "https://www.coursera.org"},
                {"name": "edX", "description": "University courses from Harvard, MIT, and more", "url": "https://www.edx.org"},
                {"name": "Udacity", "description": "Nanodegree programs in tech fields", "url": "https://www.udacity.com"},
                {"name": "freeCodeCamp", "description": "Free coding curriculum with certifications", "url": "https://www.freecodecamp.org"},
                {"name": "LinkedIn Learning", "description": "Video courses on business, tech, and creative skills", "url": "https://www.linkedin.com/learning"},
                {"name": "Udemy", "description": "Affordable courses on a wide range of topics", "url": "https://www.udemy.com"}
            ]
            
            resource_cols = st.columns(2)
            for i, resource in enumerate(resources):
                with resource_cols[i % 2]:
                    st.markdown(f"""
                    <div style="padding: 1rem; background: #f9f9f9; border-radius: 10px; margin-bottom: 1rem;">
                        <strong>{resource['name']}</strong>
                        <p style="margin: 0.5rem 0; color: #666;">{resource['description']}</p>
                        <a href="{resource['url']}" target="_blank">Visit website</a>
                    </div>
                    """, unsafe_allow_html=True)

# Career Coach Page (AI Chat)
def career_coach():
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("### 🤖 Career Coach")
        st.info("Get personalized career advice from our AI assistant")
    
    with col2:
        if lottie_ai:
            st_lottie(lottie_ai, height=150, key="ai-lottie")
    
    # Initialize chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {"role": "ai", "content": "Hello! I'm your career coach. How can I help you with your career questions today?"}
        ]
    
    # Display chat history
    for message in st.session_state.chat_history:
        if message["role"] == "ai":
            st.markdown(f'<div class="chat-bubble">{message["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-bubble user-bubble">{message["content"]}</div>', unsafe_allow_html=True)
    
    # Pre-defined questions
    st.markdown("**Quick questions:**")
    col1, col2 = st.columns(2)
    quick_questions = [
        "How do I transition to a new career?",
        "What skills are most in-demand?",
        "How can I improve my resume?",
        "What certifications should I pursue?"
    ]
    
    for i, question in enumerate(quick_questions):
        with col1 if i % 2 == 0 else col2:
            if st.button(question, key=f"quick_{i}", use_container_width=True):
                # Add user message to chat history
                st.session_state.chat_history.append({"role": "user", "content": question})
                
                # Generate AI response (simulated)
                responses = [
                    "Transitioning to a new career requires identifying transferable skills, gaining new qualifications through courses or certifications, networking with professionals in the target industry, and potentially starting with entry-level positions or internships to gain experience.",
                    "Currently, the most in-demand skills include programming languages like Python and JavaScript, cloud computing expertise (AWS, Azure, GCP), data analysis and visualization, AI and machine learning, cybersecurity, and soft skills like communication and problem-solving.",
                    "To improve your resume, focus on quantifying achievements with metrics, tailoring it to each job application, using action verbs, highlighting relevant skills, keeping it concise (1-2 pages), and ensuring it's free of errors. Consider using a clean, professional format.",
                    "The certifications you should pursue depend on your career goals. For IT roles, consider AWS/Azure certifications, CompTIA, or Cisco. For project management, PMP or CAPM. For data fields, look into Google Data Analytics or Microsoft Power BI. Always research what's valued in your specific target industry."
                ]
                response = responses[i]
                
                # Add AI response to chat history
                st.session_state.chat_history.append({"role": "ai", "content": response})
                
                # Refresh to display the new message
                st.rerun()
    
    # User input
    user_input = st.chat_input("Type your career question here...")
    
    if user_input:
        # Add user message
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        # Generate AI response (simulated)
        ai_response = generate_ai_response(user_input)
        
        # Add AI message to chat history
        st.session_state.chat_history.append({"role": "ai", "content": ai_response})
        
        # Refresh to display the new message
        st.rerun()
    
    # Clear conversation
    if st.button("Clear Conversation"):
        st.session_state.chat_history = [
            {"role": "ai", "content": "Hello! I'm your career coach. How can I help you with your career questions today?"}
        ]
        st.rerun()

def generate_ai_response(user_input):
    """Simulate AI response based on user input"""
    # This is a simplified version - in a real app, you would use an AI API
    
    input_lower = user_input.lower()
    
    if "transition" in input_lower or "change career" in input_lower:
        return """Transitioning to a new career involves several key steps:
1. Self-assessment: Identify your transferable skills and interests
2. Research: Learn about target industries and roles
3. Skill development: Acquire necessary skills through courses, certifications, or projects
4. Networking: Connect with professionals in your target field
5. Gain experience: Consider internships, freelancing, or volunteer work
6. Update your materials: Tailor your resume and LinkedIn profile
7. Start applying: Look for entry points into your new field

Would you like me to elaborate on any of these steps?"""
    
    elif "skill" in input_lower or "learn" in input_lower:
        return """Based on current market trends, here are the most valuable skills to develop:

**Technical Skills:**
- Programming (Python, JavaScript, Java)
- Cloud Computing (AWS, Azure, GCP)
- Data Analysis & Visualization
- AI/Machine Learning
- Cybersecurity
- DevOps tools

**Soft Skills:**
- Communication and collaboration
- Problem-solving
- Adaptability
- Leadership
- Time management

The specific skills you should focus on depend on your career goals. Would you like me to suggest skills for a particular field?"""
    
    elif "resume" in input_lower or "cv" in input_lower:
        return """Here are some tips to improve your resume:

1. **Quantify achievements**: Use numbers to show impact (e.g., "Increased sales by 20%")
2. **Tailor for each job**: Highlight relevant skills and experiences
3. **Use action verbs**: Started with words like "Developed", "Managed", "Created"
4. **Keep it concise**: Ideally 1-2 pages maximum
5. **Include keywords**: Many companies use ATS systems to scan for keywords
6. **Clean format**: Use a professional, easy-to-read layout
7. **Proofread**: Eliminate all typos and grammatical errors

Would you like me to review your resume or suggest a template?"""
    
    elif "interview" in input_lower:
        return """Here are some interview preparation tips:

1. **Research the company**: Understand their products, culture, and recent news
2. **Practice common questions**: Prepare STAR (Situation, Task, Action, Result) stories
3. **Prepare questions to ask**: Show your interest in the role and company
4. **Review your resume**: Be ready to discuss everything on it
5. **Dress appropriately**: Match the company's dress code
6. **Arrive early**: Plan to be 10-15 minutes early for virtual or in-person interviews
7. **Follow up**: Send a thank-you email within 24 hours

Would you like to practice some common interview questions?"""
    
    elif "salary" in input_lower or "pay" in input_lower:
        return """Salary negotiation can be tricky. Here are some tips:

1. **Research market rates**: Use sites like Glassdoor, LinkedIn Salary, and Payscale
2. **Know your value**: Consider your experience, skills, and education
3. **Wait for the right time**: Don't discuss salary until you have an offer
4. **Give a range**: Provide a salary range based on your research
5. **Consider the whole package**: Benefits, bonuses, and perks have value too
6. **Practice your negotiation**: Rehearse your talking points
7. **Be prepared to walk away**: Know your minimum acceptable salary

What specific role are you considering? I can help you research typical salary ranges."""
    
    else:
        return """I'm here to help with your career questions! You can ask me about:
- Career transitions and changes
- Skill development recommendations
- Resume and LinkedIn profile tips
- Interview preparation
- Salary negotiation
- Job search strategies
- Professional certifications

What specific career challenge are you facing right now?"""

# Industry Insights Page
def industry_insights():
    st.markdown("### 📈 Industry Insights")
    st.info("Explore trends and opportunities across different industries")
    
    # Industry selection
    selected_industry = st.selectbox("Select an industry", list(INDUSTRY_TRENDS.keys()))
    
    if selected_industry:
        industry_data = INDUSTRY_TRENDS[selected_industry]
        
        st.markdown(f"## {selected_industry} Industry Overview")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Growth Outlook", industry_data["growth"])
        with col2:
            # Count of careers in this industry
            industry_careers = [c for c in CAREERS_DATA if c.get("industry", "Technology") == selected_industry]
            st.metric("Number of Career Paths", len(industry_careers))
        with col3:
            st.metric("In-Demand Skills", len(industry_data["in_demand_skills"]))
        
        # Key trends
        st.markdown("### 🔥 Key Trends")
        for trend in industry_data["trends"]:
            st.markdown(f"- {trend}")
        
        # In-demand skills
        st.markdown("### 💼 In-Demand Skills")
        cols = st.columns(3)
        for i, skill in enumerate(industry_data["in_demand_skills"]):
            with cols[i % 3]:
                st.markdown(f"- {skill}")
        
        # Future outlook
        st.markdown("### 🔮 Future Outlook")
        st.info(industry_data["future_outlook"])
        
        # Careers in this industry
        st.markdown("### 🧭 Career Paths in This Industry")
        industry_careers = [c for c in CAREERS_DATA if c.get("industry", "Technology") == selected_industry]
        
        for career in industry_careers:
            with st.expander(f"{career['title']}"):
                st.markdown(f"**Description:** {career.get('description', 'No description available')}")
                st.markdown(f"**Salary Range:** {career['salary_range']['starting']}")
                st.markdown(f"**Growth Outlook:** {career['growth_outlook']}")
                st.markdown(f"**Demand:** {career['demand']}")
                
                st.markdown("**Key Skills:**")
                skill_cols = st.columns(3)
                for i, skill in enumerate(career['skills']):
                    with skill_cols[i % 3]:
                        st.markdown(f"- {skill}")
                
                if st.button("View Learning Path", key=f"industry_path_{career['title']}"):
                    st.session_state.selected_career = career['title']
                    navigate_to("Learning Paths")

# Mentor Connect Page
def mentor_connect():
    st.markdown("### 👥 Mentor Connect")
    st.info("Connect with experienced professionals in your field of interest")
    
    # Search and filter mentors
    col1, col2 = st.columns(2)
    
    with col1:
        skill_filter = st.selectbox("Filter by skill", ["All"] + list(set([skill for mentor in MENTORS for skill in mentor["skills"]])))
    with col2:
        availability_filter = st.selectbox("Filter by availability", ["All", "Weekdays", "Weekends", "Flexible"])
    
    # Filter mentors
    filtered_mentors = MENTORS
    if skill_filter != "All":
        filtered_mentors = [m for m in filtered_mentors if skill_filter in m["skills"]]
    if availability_filter != "All":
        filtered_mentors = [m for m in filtered_mentors if availability_filter.lower() in m["availability"].lower()]
    
    # Display mentors
    st.markdown(f"### Available Mentors ({len(filtered_mentors)})")
    
    for mentor in filtered_mentors:
        col1, col2 = st.columns([1, 3])
        
        with col1:
            # Placeholder for mentor image
            st.markdown(f"""
            <div style="text-align: center;">
                <div style="font-size: 3rem;">👤</div>
                <h3>{mentor['name']}</h3>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="mentor-card">
                <h4>{mentor['role']} at {mentor['company']}</h4>
                <p>Experience: {mentor['experience']} | Rating: ⭐{mentor['rating']} | Sessions: {mentor['sessions']}</p>
                <p><strong>Skills:</strong> {', '.join(mentor['skills'][:4])}</p>
                <p><strong>Availability:</strong> {mentor['availability']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Request Session", key=f"request_{mentor['name']}"):
                if mentor['name'] not in st.session_state.mentor_connections:
                    st.session_state.mentor_connections.append(mentor['name'])
                    st.success(f"Session requested with {mentor['name']}! They'll contact you soon.")
                    
                    # Check for badge
                    if "Mentorship Seeker" not in st.session_state.earned_badges:
                        st.session_state.earned_badges.append("Mentorship Seeker")
                        st.success("🎉 You earned the Mentorship Seeker badge!")
                else:
                    st.info("You've already connected with this mentor")
        
        st.markdown("---")
    
    # My connections
    if st.session_state.mentor_connections:
        st.markdown("### 🤝 My Mentor Connections")
        for mentor in st.session_state.mentor_connections:
            st.markdown(f"- {mentor}")

# Job Market Page
def job_market():
    st.markdown("### 💼 Job Market")
    st.info("Explore current job opportunities and market trends")
    
    # Job search
    st.markdown("#### 🔍 Search Jobs")
    col1, col2 = st.columns(2)
    
    with col1:
        job_title = st.text_input("Job title", placeholder="e.g., Frontend Developer")
    with col2:
        location = st.text_input("Location", placeholder="e.g., Bangalore")
    
    # Filter jobs
    filtered_jobs = JOB_POSTINGS
    if job_title:
        filtered_jobs = [j for j in filtered_jobs if job_title.lower() in j["title"].lower()]
    if location:
        filtered_jobs = [j for j in filtered_jobs if location.lower() in j["location"].lower()]
    
    # Display jobs
    st.markdown(f"### Available Jobs ({len(filtered_jobs)})")
    
    for job in filtered_jobs:
        st.markdown(f"""
        <div class="role-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h3>{job['title']}</h3>
                <span class="salary-tag">{job['salary']}</span>
            </div>
            <p><strong>{job['company']}</strong> | {job['location']} | {job['experience']} | {job['posted']}</p>
            <div>
                <p style="margin-bottom: 5px;"><strong>Required Skills:</strong></p>
                <div>{"".join([f'<span class="skill-badge">{skill}</span>' for skill in job['skills']])}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Apply Now", key=f"apply_{job['title']}_{job['company']}"):
                st.success(f"Application sent for {job['title']} at {job['company']}!")
                
                # Check for badge
                if "Job Hunter" not in st.session_state.earned_badges:
                    st.session_state.earned_badges.append("Job Hunter")
                    st.success("🎉 You earned the Job Hunter badge!")
        with col2:
            if st.button("Save Job", key=f"save_{job['title']}_{job['company']}"):
                if job['title'] not in st.session_state.saved_jobs:
                    st.session_state.saved_jobs.append(job['title'])
                    st.success(f"Saved {job['title']} to your profile!")
        
        st.markdown("---")
    
    # Saved jobs
    if st.session_state.saved_jobs:
        st.markdown("### 📋 Saved Jobs")
        for job in st.session_state.saved_jobs:
            st.markdown(f"- {job}")

# ROI Analysis Page
def roi_analysis():
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("### 📈 ROI Analysis")
        st.info("Calculate Return on Investment for different career paths")
    
    with col2:
        if lottie_roi:
            st_lottie(lottie_roi, height=150, key="roi-lottie")
    
    # Get selected career from session state or let user choose
    selected_career = st.session_state.get('selected_career', "")
    
    if not selected_career:
        st.markdown("#### Select a career to analyze its ROI")
        career_options = [career['title'] for career in CAREERS_DATA]
        selected_career = st.selectbox("Choose a career", career_options)
    
    if selected_career:
        # Find the career data
        career_data = next((career for career in CAREERS_DATA if career['title'] == selected_career), None)
        
        if career_data:
            st.markdown(f"### ROI Analysis for {selected_career}")
            
            # Display key ROI metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                # Extract numeric value from salary range string
                salary_match = re.search(r'₹(\d+)[^\d]*(\d+)?', career_data['salary_range']['starting'])
                if salary_match:
                    min_salary = int(salary_match.group(1))
                    max_salary = int(salary_match.group(2)) if salary_match.group(2) else min_salary
                    avg_salary = (min_salary + max_salary) / 2
                    st.metric("Avg Starting Salary", f"₹{avg_salary:.1f}L")
            
            with col2:
                # Calculate ROI timeline
                roi_timeline = career_data.get('roi_timeline', '3-5 years')
                st.metric("ROI Timeline", roi_timeline)
            
            with col3:
                # Stress level
                stress_level = career_data.get('stress_level', 'Medium')
                st.metric("Stress Level", stress_level)
            
            with col4:
                # Automation risk
                automation_risk = career_data.get('automation_risk', 'Medium')
                st.metric("Automation Risk", automation_risk)
            
            # Investment cost visualization
            st.markdown("#### Investment vs Return")
            
            # Simulate investment and return over time
            years = list(range(1, 11))
            
            # Calculate costs (education + opportunity cost)
            education_cost = 500000 if career_data.get('investment_cost') == 'High' else (
                300000 if career_data.get('investment_cost') == 'Medium' else 100000
            )
            
            # Calculate earnings over time
            starting_salary = avg_salary * 100000  # Convert LPA to actual amount
            growth_rate = 0.15 if career_data['growth_outlook'] == 'Very High' else (
                0.10 if career_data['growth_outlook'] == 'High' else 0.07
            )
            
            # Simulate earnings
            earnings = []
            cumulative_net = []
            for year in years:
                if year == 1:
                    # First year - mostly investment
                    year_earnings = starting_salary * 0.5  # Assuming half year of employment
                    year_net = year_earnings - education_cost
                else:
                    year_earnings = starting_salary * (1 + growth_rate) ** (year - 1)
                    year_net = year_earnings
                earnings.append(year_earnings)
                cumulative_net.append(year_net + (cumulative_net[-1] if cumulative_net else 0))
            
            # Create DataFrame for visualization
            roi_df = pd.DataFrame({
                'Year': years,
                'Earnings': earnings,
                'Cumulative Net': cumulative_net
            })
            
            # Plot earnings and cumulative net
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=roi_df['Year'], 
                y=roi_df['Earnings'],
                mode='lines+markers',
                name='Annual Earnings',
                line=dict(color='#4A90E2', width=3)
            ))
            
            fig.add_trace(go.Scatter(
                x=roi_df['Year'], 
                y=roi_df['Cumulative Net'],
                mode='lines+markers',
                name='Cumulative Net',
                line=dict(color='#2ECC71', width=3)
            ))
            
            # Add break-even point
            break_even_year = next((i for i, val in enumerate(cumulative_net) if val >= 0), None)
            if break_even_year is not None:
                fig.add_vline(x=break_even_year + 1, line_dash="dash", line_color="red",
                             annotation_text=f"Break-even: Year {break_even_year + 1}")
            
            fig.update_layout(
                title="Earnings Projection Over Time",
                xaxis_title="Years",
                yaxis_title="Amount (₹)",
                hovermode="x unified"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Key insights
            st.markdown("#### Key Insights")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("##### 👍 Advantages")
                advantages = [
                    f"High growth potential ({career_data['growth_outlook']})",
                    f"Strong demand in market ({career_data['demand']})",
                    f"Good starting salary (₹{avg_salary:.1f}L)",
                    f"Future-proof skills against automation"
                ]
                for advantage in advantages:
                    st.markdown(f"- {advantage}")
            
            with col2:
                st.markdown("##### 👎 Considerations")
                considerations = [
                    f"Requires significant upfront investment ({career_data.get('investment_cost', 'Medium')})",
                    f"ROI timeline: {roi_timeline}",
                    f"Stress level: {stress_level}",
                    f"Automation risk: {automation_risk}"
                ]
                for consideration in considerations:
                    st.markdown(f"- {consideration}")
            
            # Compare with other careers
            st.markdown("#### Compare with Other Careers")
            
            compare_careers = [c for c in CAREERS_DATA if c['title'] != selected_career]
            compare_options = [c['title'] for c in compare_careers[:3]]
            compare_selected = st.selectbox("Select another career to compare", compare_options)
            
            if compare_selected:
                compare_data = next((c for c in compare_careers if c['title'] == compare_selected), None)
                
                if compare_data:
                    # Create comparison table
                    comparison_data = {
                        'Metric': ['Starting Salary', 'Growth Outlook', 'Demand', 'Investment Cost', 
                                  'ROI Timeline', 'Stress Level', 'Automation Risk'],
                        selected_career: [
                            career_data['salary_range']['starting'],
                            career_data['growth_outlook'],
                            career_data['demand'],
                            career_data.get('investment_cost', 'Medium'),
                            career_data.get('roi_timeline', '3-5 years'),
                            career_data.get('stress_level', 'Medium'),
                            career_data.get('automation_risk', 'Medium')
                        ],
                        compare_selected: [
                            compare_data['salary_range']['starting'],
                            compare_data['growth_outlook'],
                            compare_data['demand'],
                            compare_data.get('investment_cost', 'Medium'),
                            compare_data.get('roi_timeline', '3-5 years'),
                            compare_data.get('stress_level', 'Medium'),
                            compare_data.get('automation_risk', 'Medium')
                        ]
                    }
                    
                    comparison_df = pd.DataFrame(comparison_data)
                    st.table(comparison_df)
            
            # Check for badge
            if "ROI Analyst" not in st.session_state.earned_badges:
                st.session_state.earned_badges.append("ROI Analyst")
                st.success("🎉 You earned the ROI Analyst badge!")

# Career Comparison Page
def career_comparison():
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("### ⚖️ Career Comparison")
        st.info("Compare different career paths side-by-side")
    
    with col2:
        if lottie_compare:
            st_lottie(lottie_compare, height=150, key="compare-lottie")
    
    # Career selection
    col1, col2 = st.columns(2)
    
    with col1:
        career_options = [career['title'] for career in CAREERS_DATA]
        selected_career_1 = st.selectbox(
            "Select first career", 
            career_options,
            index=career_options.index(st.session_state.selected_career_1) if st.session_state.selected_career_1 in career_options else 0
        )
        st.session_state.selected_career_1 = selected_career_1
    
    with col2:
        selected_career_2 = st.selectbox(
            "Select second career", 
            [c for c in career_options if c != selected_career_1],
            index=0
        )
        st.session_state.selected_career_2 = selected_career_2
    
    if selected_career_1 and selected_career_2:
        # Get career data
        career_1 = next((c for c in CAREERS_DATA if c['title'] == selected_career_1), None)
        career_2 = next((c for c in CAREERS_DATA if c['title'] == selected_career_2), None)
        
        if career_1 and career_2:
            st.markdown(f"## Comparison: {selected_career_1} vs {selected_career_2}")
            
            # Key metrics comparison
            st.markdown("### Key Metrics Comparison")
            
            metrics_data = {
                'Metric': ['Program Type', 'Duration', 'Eligibility', 'Starting Salary', 
                          'Mid-Career Salary', 'Growth Outlook', 'Demand', 'Investment Cost',
                          'ROI Timeline', 'Stress Level', 'Automation Risk'],
                selected_career_1: [
                    career_1.get('type', 'N/A'),
                    career_1.get('duration', 'N/A'),
                    career_1.get('eligibility', 'N/A')[:30] + '...' if career_1.get('eligibility') and len(career_1.get('eligibility')) > 30 else career_1.get('eligibility', 'N/A'),
                    career_1['salary_range']['starting'],
                    career_1['salary_range'].get('mid', 'N/A'),
                    career_1['growth_outlook'],
                    career_1['demand'],
                    career_1.get('investment_cost', 'Medium'),
                    career_1.get('roi_timeline', '3-5 years'),
                    career_1.get('stress_level', 'Medium'),
                    career_1.get('automation_risk', 'Medium')
                ],
                selected_career_2: [
                    career_2.get('type', 'N/A'),
                    career_2.get('duration', 'N/A'),
                    career_2.get('eligibility', 'N/A')[:30] + '...' if career_2.get('eligibility') and len(career_2.get('eligibility')) > 30 else career_2.get('eligibility', 'N/A'),
                    career_2['salary_range']['starting'],
                    career_2['salary_range'].get('mid', 'N/A'),
                    career_2['growth_outlook'],
                    career_2['demand'],
                    career_2.get('investment_cost', 'Medium'),
                    career_2.get('roi_timeline', '3-5 years'),
                    career_2.get('stress_level', 'Medium'),
                    career_2.get('automation_risk', 'Medium')
                ]
            }
            
            metrics_df = pd.DataFrame(metrics_data)
            st.table(metrics_df)
            
            # Skills comparison
            st.markdown("### Skills Comparison")
            
            skills_1 = set(career_1['skills'])
            skills_2 = set(career_2['skills'])
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"##### {selected_career_1} Only")
                unique_skills_1 = skills_1 - skills_2
                for skill in list(unique_skills_1)[:5]:
                    st.markdown(f"- {skill}")
                if not unique_skills_1:
                    st.info("No unique skills")
            
            with col2:
                st.markdown("##### Common Skills")
                common_skills = skills_1 & skills_2
                for skill in list(common_skills)[:5]:
                    st.markdown(f"- {skill}")
                if not common_skills:
                    st.info("No common skills")
            
            with col3:
                st.markdown(f"##### {selected_career_2} Only")
                unique_skills_2 = skills_2 - skills_1
                for skill in list(unique_skills_2)[:5]:
                    st.markdown(f"- {skill}")
                if not unique_skills_2:
                    st.info("No unique skills")
            
            # Future trends comparison
            st.markdown("### Future Trends Comparison")
            
            trends_1 = career_1.get('future_trends', ['Not specified'])
            trends_2 = career_2.get('future_trends', ['Not specified'])
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"##### {selected_career_1}")
                for trend in trends_1[:3]:
                    st.markdown(f"- {trend}")
            
            with col2:
                st.markdown(f"##### {selected_career_2}")
                for trend in trends_2[:3]:
                    st.markdown(f"- {trend}")
            
            # ROI comparison chart
            st.markdown("### ROI Comparison")
            
            # Simulate ROI for both careers
            years = list(range(1, 8))
            
            def calculate_roi(career):
                # Extract numeric value from salary range string
                salary_match = re.search(r'₹(\d+)[^\d]*(\d+)?', career['salary_range']['starting'])
                if salary_match:
                    min_salary = int(salary_match.group(1))
                    max_salary = int(salary_match.group(2)) if salary_match.group(2) else min_salary
                    starting_salary = (min_salary + max_salary) / 2 * 100000
                
                # Calculate education cost
                education_cost = 500000 if career.get('investment_cost') == 'High' else (
                    300000 if career.get('investment_cost') == 'Medium' else 100000
                )
                
                # Calculate growth rate
                growth_rate = 0.15 if career['growth_outlook'] == 'Very High' else (
                    0.10 if career['growth_outlook'] == 'High' else 0.07
                )
                
                # Calculate cumulative net
                cumulative_net = []
                for year in years:
                    if year == 1:
                        year_earnings = starting_salary * 0.5  # Assuming half year of employment
                        year_net = year_earnings - education_cost
                    else:
                        year_earnings = starting_salary * (1 + growth_rate) ** (year - 1)
                        year_net = year_earnings
                    cumulative_net.append(year_net + (cumulative_net[-1] if cumulative_net else 0))
                
                return cumulative_net
            
            roi_1 = calculate_roi(career_1)
            roi_2 = calculate_roi(career_2)
            
            # Create ROI comparison chart
            roi_df = pd.DataFrame({
                'Year': years,
                selected_career_1: roi_1,
                selected_career_2: roi_2
            })
            
            fig = px.line(roi_df, x='Year', y=[selected_career_1, selected_career_2],
                         title='Cumulative Net Income Comparison',
                         labels={'value': 'Cumulative Net (₹)', 'variable': 'Career Path'})
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Recommendations
            st.markdown("### Recommendation")
            
            # Simple recommendation logic
            if roi_1[-1] > roi_2[-1] and career_1['growth_outlook'] >= career_2['growth_outlook']:
                st.success(f"**{selected_career_1}** appears to be the better choice based on financial returns and growth potential")
            elif roi_2[-1] > roi_1[-1] and career_2['growth_outlook'] >= career_1['growth_outlook']:
                st.success(f"**{selected_career_2}** appears to be the better choice based on financial returns and growth potential")
            else:
                st.info("Both careers have their advantages. Consider your personal interests and skills when making a decision.")
            
            # Check for badge
            if "Comparison Pro" not in st.session_state.earned_badges:
                st.session_state.earned_badges.append("Comparison Pro")
                st.success("🎉 You earned the Comparison Pro badge!")

# Side Hustles Page
def side_hustles():
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown("### 💰 Side Hustles & Part-Time Jobs")
        st.info("Earn while learning with these part-time opportunities")
    
    with col2:
        if lottie_money:
            st_lottie(lottie_money, height=150, key="money-lottie")
    
    # Get user skills and career interests
    user_skills = st.session_state.get('skills', [])
    user_career_interest = st.session_state.get('career_interest', "")
    
    # Filter side hustles based on user skills and career interests
    filtered_hustles = SIDE_HUSTLES
    
    if user_skills:
        # Prioritize hustles that match user skills
        filtered_hustles.sort(key=lambda h: len(set(h['skills']) & set(user_skills)), reverse=True)
    
    if user_career_interest:
        # Further filter by career relevance
        filtered_hustles = [h for h in filtered_hustles if 
                           any(career in h['career_relevance'] for career in [user_career_interest]) or 
                           not user_career_interest]
    
    # Display side hustles
    st.markdown(f"### Recommended Side Hustles ({len(filtered_hustles)})")
    
    for hustle in filtered_hustles:
        # Calculate match score based on skills
        skill_match = len(set(hustle['skills']) & set(user_skills)) / len(hustle['skills']) * 100 if user_skills else 0
        
        st.markdown(f"""
        <div class="side-hustle-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h3>{hustle['title']}</h3>
                <div style="background: #4A90E2; color: white; padding: 5px 10px; border-radius: 15px;">
                    {skill_match:.0f}% Match
                </div>
            </div>
            <p>{hustle['description']}</p>
            <div style="display: flex; gap: 10px; margin-bottom: 10px;">
                <span class="salary-tag">Earnings: {hustle['earning_potential']}</span>
                <span class="growth-tag">Time: {hustle['time_commitment']}</span>
            </div>
            <div>
                <p style="margin-bottom: 5px;"><strong>Skills Required:</strong></p>
                <div>{"".join([f'<span class="skill-badge">{skill}</span>' for skill in hustle['skills']])}</div>
            </div>
            <div style="margin-top: 10px;">
                <p style="margin-bottom: 5px;"><strong>Platforms:</strong> {', '.join(hustle['platforms'])}</p>
                <p style="margin-bottom: 5px;"><strong>Relevant Careers:</strong> {', '.join(hustle['career_relevance'])}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Initialize progress tracking for this hustle
        if hustle['title'] not in st.session_state.side_hustle_progress:
            st.session_state.side_hustle_progress[hustle['title']] = 0
        
        # Progress tracking
        progress = st.slider(
            f"Progress on {hustle['title']}", 
            0, 100, 
            st.session_state.side_hustle_progress[hustle['title']],
            key=f"hustle_progress_{hustle['title']}"
        )
        
        st.session_state.side_hustle_progress[hustle['title']] = progress
        st.progress(progress / 100)
        
        # Action buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Get Started", key=f"start_{hustle['title']}"):
                st.success(f"Getting started with {hustle['title']}! Check the platforms listed above for opportunities.")
        with col2:
            if st.button("Save for Later", key=f"save_{hustle['title']}"):
                st.info(f"Saved {hustle['title']} to your profile!")
        
        st.markdown("---")
    
    # Side hustle progress overview
    st.markdown("### Your Side Hustle Progress")
    
    if st.session_state.side_hustle_progress:
        hustle_progress_df = pd.DataFrame({
            'Side Hustle': list(st.session_state.side_hustle_progress.keys()),
            'Progress': list(st.session_state.side_hustle_progress.values())
        })
        fig = px.bar(hustle_progress_df, x='Side Hustle', y='Progress', 
                title='Your Side Hustle Progress',
                color='Progress', color_continuous_scale='Blues')
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
        # Check for badge
        active_hustles = sum(1 for progress in st.session_state.side_hustle_progress.values() if progress > 0)
        if active_hustles >= 2 and "Side Hustler" not in st.session_state.earned_badges:
            st.session_state.earned_badges.append("Side Hustler")
            st.success("🎉 You earned the Side Hustler badge!")
    else:
        st.info("You haven't started any side hustles yet. Explore the options above to get started!")
    
    # Resources section
    st.markdown("### 📚 Side Hustle Resources")
    
    resources = [
        {
            "name": "Upwork",
            "description": "Largest freelancing platform with diverse opportunities",
            "url": "https://www.upwork.com",
            "category": "Freelancing"
        },
        {
            "name": "Fiverr",
            "description": "Platform for micro-jobs and gigs starting at $5",
            "url": "https://www.fiverr.com",
            "category": "Freelancing"
        },
        {
            "name": "Freelancer.com",
            "description": "Global freelancing marketplace with competitive projects",
            "url": "https://www.freelancer.com",
            "category": "Freelancing"
        },
        {
            "name": "Kaggle",
            "description": "Data science competitions and micro-tasks with prizes",
            "url": "https://www.kaggle.com",
            "category": "Data Science"
        },
        {
            "name": "99designs",
            "description": "Design contests and freelance opportunities for creatives",
            "url": "https://99designs.com",
            "category": "Design"
        },
        {
            "name": "Chegg Tutors",
            "description": "Online tutoring platform for subject matter experts",
            "url": "https://www.chegg.com/tutors",
            "category": "Education"
        }
    ]
    
    resource_cols = st.columns(2)
    for i, resource in enumerate(resources):
        with resource_cols[i % 2]:
            st.markdown(f"""
            <div style="padding: 1rem; background: #f9f9f9; border-radius: 10px; margin-bottom: 1rem;">
                <strong>{resource['name']}</strong> ({resource['category']})
                <p style="margin: 0.5rem 0; color: #666;">{resource['description']}</p>
                <a href="{resource['url']}" target="_blank">Visit website</a>
            </div>
            """, unsafe_allow_html=True)

# Profile & Badges Page
def profile_badges():
    st.markdown("### 👤 Profile & Achievements")
    
    # User profile
    st.markdown("#### Personal Information")
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Name", "John Doe")
        email = st.text_input("Email", st.session_state.user_email)
    with col2:
        education = st.selectbox("Education Level", ["High School", "Bachelor's", "Master's", "PhD", "Other"])
        experience = st.selectbox("Years of Experience", ["0-2", "3-5", "6-10", "10+"])
    
    # Skills
    st.markdown("#### Your Skills")
    if st.session_state.skills:
        st.markdown(" ".join([f'<span class="skill-badge">{skill}</span>' for skill in st.session_state.skills]), unsafe_allow_html=True)
    else:
        st.info("Complete the skills assessment to see your skills")
    
    # Badges
    st.markdown("#### 🏆 Earned Badges")
    
    if st.session_state.earned_badges:
        cols = st.columns(3)
        for i, badge_name in enumerate(st.session_state.earned_badges):
            badge = next((b for b in BADGES if b["name"] == badge_name), None)
            if badge:
                with cols[i % 3]:
                    st.markdown(f"""
                    <div style="text-align: center; padding: 1rem; background: #f9f9f9; border-radius: 10px; margin-bottom: 1rem;">
                        <div style="font-size: 2rem;">{badge['icon']}</div>
                        <h4>{badge['name']}</h4>
                        <p style="font-size: 0.8rem; color: #666;">{badge['description']}</p>
                    </div>
                    """, unsafe_allow_html=True)
    else:
        st.info("Complete activities to earn badges!")
    
    # Progress
    st.markdown("#### 📊 Your Progress")
    
    if st.session_state.learning_path_progress:
        for career, progress in st.session_state.learning_path_progress.items():
            total_progress = sum(progress.values()) / 4
            st.markdown(f"**{career}**: {total_progress:.1f}%")
            st.progress(total_progress / 100)
    else:
        st.info("Start a learning path to track your progress!")
    
    # Side hustle progress
    if st.session_state.side_hustle_progress:
        st.markdown("#### 💰 Side Hustle Progress")
        for hustle, progress in st.session_state.side_hustle_progress.items():
            st.markdown(f"**{hustle}**: {progress}%")
            st.progress(progress / 100)

# Main app logic
def main():
    # Check if user is logged in
    if not st.session_state.logged_in:
        # Show authentication pages
        auth_tab1, auth_tab2 = st.tabs(["Login", "Sign Up"])
        
        with auth_tab1:
            show_login_page()
        
        with auth_tab2:
            show_signup_page()
        
        return  # Stop execution here if not logged in
    
    # User is logged in - show the main app
    # Sidebar navigation
    with st.sidebar:
        st.image("https://img.icons8.com/fluency/96/graduation-cap.png", width=80)
        st.title("Career Advisor")
        
        # Display user info
        st.markdown(f"**👤 User:** {st.session_state.user_email}")
        
        # Show badge count
        if st.session_state.earned_badges:
            st.markdown(f"**🏆 Badges:** {len(st.session_state.earned_badges)}")
        
        st.markdown("---")
        
        # Navigation buttons
        if st.button("🏠 Home", use_container_width=True):
            navigate_to("Home")
        if st.button("📊 Skills Assessment", use_container_width=True):
            navigate_to("Skills Assessment")
        if st.button("💼 Career Matches", use_container_width=True):
            navigate_to("Career Matches")
        if st.button("📚 Learning Paths", use_container_width=True):
            navigate_to("Learning Paths")
        if st.button("🤖 Career Coach", use_container_width=True):
            navigate_to("Career Coach")
        if st.button("📈 ROI Analysis", use_container_width=True):
            navigate_to("ROI Analysis")
        if st.button("⚖️ Career Comparison", use_container_width=True):
            navigate_to("Career Comparison")
        if st.button("💰 Side Hustles", use_container_width=True):
            navigate_to("Side Hustles")
        if st.button("📈 Industry Insights", use_container_width=True):
            navigate_to("Industry Insights")
        if st.button("👥 Mentor Connect", use_container_width=True):
            navigate_to("Mentor Connect")
        if st.button("💼 Job Market", use_container_width=True):
            navigate_to("Job Market")
        if st.button("👤 Profile & Badges", use_container_width=True):
            navigate_to("Profile & Badges")
        
        st.markdown("---")
        
        # User profile section
        st.markdown("### Your Profile")
        if st.session_state.get('skills'):
            st.markdown(f"**Skills:** {', '.join(st.session_state.skills[:5])}{'...' if len(st.session_state.skills) > 5 else ''}")
        
        if st.session_state.get('assessment_results'):
            overall_score = sum(st.session_state.assessment_results.values()) / len(st.session_state.assessment_results)
            st.metric("Skills Score", f"{overall_score:.1f}/5.0")
        
        st.markdown("---")
        
        # Logout button
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user_email = None
            st.rerun()
        
        st.markdown("---")
        st.caption("Your career development companion")
    
    # Display the current page based on navigation
    if st.session_state.current_page == "Home":
        home_page()
    elif st.session_state.current_page == "Skills Assessment":
        skills_assessment()
    elif st.session_state.current_page == "Career Matches":
        career_matches()
    elif st.session_state.current_page == "Learning Paths":
        learning_paths()
    elif st.session_state.current_page == "Career Coach":
        career_coach()
    elif st.session_state.current_page == "ROI Analysis":
        roi_analysis()
    elif st.session_state.current_page == "Career Comparison":
        career_comparison()
    elif st.session_state.current_page == "Side Hustles":
        side_hustles()
    elif st.session_state.current_page == "Industry Insights":
        industry_insights()
    elif st.session_state.current_page == "Mentor Connect":
        mentor_connect()
    elif st.session_state.current_page == "Job Market":
        job_market()
    elif st.session_state.current_page == "Profile & Badges":
        profile_badges()

if __name__ == "__main__":
    main()