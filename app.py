import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import uuid

# Page configuration
st.set_page_config(
    page_title="Alkhorayef Group - 2025 Shared Service Catalogue",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Company list for Alkhorayef Group
ALKHORAYEF_COMPANIES = [
    "APC", "AIC", "AGC", "APS", "PS", "AWPT", "AMIC", "ACC", "SPC", "Tom Egypt"
]

# Enhanced PROJECT_TYPES organized by categories
PROJECT_CATEGORIES = {
    "🤖 Digital Transformation & Automation": [
        "RPA (Robotic Process Automation)",
        "Process Automation & Optimization",
        "Digital Workflow Management",
        "Business Process Re-engineering",
        "Document Management System",
        "Electronic Signature Solutions"
    ],
    
    "🧠 AI & Advanced Analytics": [
        "AI & Machine Learning Platform",
        "Predictive Analytics Implementation",
        "Computer Vision Solutions",
        "Natural Language Processing",
        "Chatbot & Virtual Assistant",
        "AI-Powered Quality Control"
    ],
    
    "📊 Data & Business Intelligence": [
        "Data Analytics & BI Platform",
        "Data Warehouse Implementation",
        "Real-time Dashboard Development",
        "Data Lake Architecture",
        "Master Data Management",
        "Data Migration & Integration",
        "Self-Service Analytics Tools"
    ],
    
    "💼 Enterprise Applications": [
        "ERP System Implementation",
        "CRM System Deployment",
        "HCM/HR System Implementation",
        "Supply Chain Management System",
        "Asset Management System",
        "Project Management Platform",
        "Financial Management System",
        "Procurement & Vendor Management"
    ],
    
    "🏭 Industry-Specific Solutions": [
        "Manufacturing Execution System (MES)",
        "Industrial IoT (IIoT) Implementation",
        "Equipment Monitoring & Maintenance",
        "Quality Management System",
        "Inventory Management System",
        "Transportation Management System",
        "Warehouse Management System",
        "Field Service Management"
    ],
    
    "☁️ Infrastructure & Cloud": [
        "Cloud Migration & Modernization",
        "Hybrid Cloud Implementation",
        "Infrastructure Upgrade",
        "Network Infrastructure Enhancement",
        "Server Virtualization",
        "Backup & Disaster Recovery",
        "Performance Monitoring System"
    ],
    
    "🔒 Security & Compliance": [
        "Cybersecurity Enhancement",
        "Identity & Access Management",
        "Security Information & Event Management (SIEM)",
        "Data Loss Prevention (DLP)",
        "Compliance Management System",
        "Risk Management Platform",
        "Audit & Governance Tools"
    ],
    
    "🔗 Integration & Connectivity": [
        "System Integration Project",
        "API Development & Management",
        "EDI Implementation",
        "B2B Portal Development",
        "Mobile Application Development",
        "Web Portal Implementation",
        "Third-party System Integration"
    ],
    
    "💬 Communication & Collaboration": [
        "Unified Communications Platform",
        "Video Conferencing Solutions",
        "Team Collaboration Tools",
        "Knowledge Management System",
        "Training & Learning Management System"
    ],
    
    "👥 Customer Experience": [
        "Customer Portal Development",
        "E-commerce Platform",
        "Customer Service Management",
        "Marketing Automation Platform",
        "Social Media Management Tools"
    ],
    
    "💰 Financial & Regulatory": [
        "Financial Reporting & Analytics",
        "Regulatory Compliance System",
        "Tax Management System",
        "Treasury Management System",
        "Budget Planning & Forecasting"
    ],
    
    "🌱 Sustainability & ESG": [
        "Environmental Management System",
        "Sustainability Reporting Platform",
        "Energy Management System",
        "Carbon Footprint Tracking",
        "ESG Compliance & Reporting"
    ],
    
    "⚙️ Custom & Specialized": [
        "Custom Application Development",
        "Legacy System Modernization",
        "Database Optimization & Migration",
        "Business Intelligence Custom Reports",
        "Specialized Industry Solution",
        "Research & Development Platform"
    ]
}

# Flatten the categories for backward compatibility
PROJECT_TYPES = []
for category, services in PROJECT_CATEGORIES.items():
    PROJECT_TYPES.extend(services)

DEPARTMENTS = [
    "Finance", "Human Resources", "Operations", "Sales", "Marketing", 
    "IT", "Customer Service", "Supply Chain", "Manufacturing", "Executive"
]

# Predefined service data
ORACLE_SERVICES = {
    "Oracle ERP Cloud": {
        "description": "Complete enterprise resource planning solution with financials, procurement, and project management",
        "price_per_user": 180,
        "setup_cost": 25000
    },
    "Oracle HCM Cloud": {
        "description": "Human capital management including payroll, talent management, and workforce planning",
        "price_per_user": 75,
        "setup_cost": 15000
    },
    "Oracle Supply Chain Management": {
        "description": "End-to-end supply chain planning, inventory management, and logistics optimization",
        "price_per_user": 120,
        "setup_cost": 20000
    },
    "Oracle Fusion Analytics": {
        "description": "Pre-built analytics and reporting for Oracle applications with real-time insights",
        "price_per_user": 45,
        "setup_cost": 8000
    }
}

MICROSOFT_SERVICES = {
    "Microsoft 365 E3": {
        "description": "Premium productivity suite with advanced security, compliance, and analytics capabilities",
        "price_per_user": 82,
        "setup_cost": 5000
    },
    "Microsoft Teams Phone": {
        "description": "Cloud-based phone system integrated with Teams for calling and conferencing",
        "price_per_user": 28,
        "setup_cost": 3000
    },
    "Power BI Premium": {
        "description": "Advanced business intelligence with AI-powered insights and enterprise-grade capabilities",
        "price_per_user": 75,
        "setup_cost": 4000
    },
    "Project for the Web": {
        "description": "Cloud-based project management with resource scheduling and portfolio management",
        "price_per_user": 120,
        "setup_cost": 6000
    },
    "Microsoft Dynamics 365": {
        "description": "Customer relationship management and enterprise applications suite",
        "price_per_user": 210,
        "setup_cost": 30000
    }
}

SUPPORT_PACKAGES = {
    "Basic": {
        "price": 52000,
        "support_requests_standard": 0,
        "support_requests_priority": 0,
        "support_requests_premium": 0,
        "total_support_requests": 0,
        "improvement_hours": 0,
        "training_requests": 0,
        "report_requests": 0,
        "systems_operation": "✓ Included",
        "description": "Essential support for small teams with basic IT needs"
    },
    "Bronze": {
        "price": 195975,
        "support_requests_standard": 60,
        "support_requests_priority": 25,
        "support_requests_premium": 15,
        "total_support_requests": 100,
        "improvement_hours": 0,
        "training_requests": 0,
        "report_requests": 0,
        "systems_operation": "✓ Included",
        "description": "Enhanced support for growing organizations"
    },
    "Silver": {
        "price": 649498,
        "support_requests_standard": 540,
        "support_requests_priority": 100,
        "support_requests_premium": 60,
        "total_support_requests": 400,
        "improvement_hours": 0,
        "training_requests": 0,
        "report_requests": 5,
        "systems_operation": "✓ Included",
        "description": "Comprehensive support for medium enterprises"
    },
    "Gold": {
        "price": 1578139,
        "support_requests_standard": 600,
        "support_requests_priority": 250,
        "support_requests_premium": 150,
        "total_support_requests": 1000,
        "improvement_hours": 240,
        "training_requests": 5,
        "report_requests": 5,
        "systems_operation": "✓ Included",
        "description": "Premium support for large organizations"
    },
    "Platinum": {
        "price": 2500000,
        "support_requests_standard": 935,
        "support_requests_priority": 400,
        "support_requests_premium": 240,
        "total_support_requests": 1575,
        "improvement_hours": 380,
        "training_requests": 10,
        "report_requests": 15,
        "systems_operation": "✓ Included",
        "description": "Enterprise-grade support with dedicated resources"
    }
}

# RPA Package data from the provided table
RPA_PACKAGES = {
    "Bronze (1 Credit)": {
        "discovery_analysis": 33110,
        "build_implementation": 3080,
        "project_management": 9350,
        "infrastructure_license": 43230,
        "year_1_total": 88770,
        "year_2_cost": 10098,
        "year_3_cost": 10906,
        "processes_covered": "Covers up to 2 processes",
        "implementation_processes": "Covers 1 process"
    },
    "Silver (3 Credits)": {
        "discovery_analysis": 94964,
        "build_implementation": 8778,
        "project_management": 57310,
        "infrastructure_license": 124608,
        "year_1_total": 285660,
        "year_2_cost": 30294,
        "year_3_cost": 32718,
        "processes_covered": "Covers up to 5 processes",
        "implementation_processes": "Covers up to 3 processes"
    },
    "Gold (5 Credits)": {
        "discovery_analysis": 148995,
        "build_implementation": 13860,
        "project_management": 92950,
        "infrastructure_license": 199210,
        "year_1_total": 455015,
        "year_2_cost": 50490,
        "year_3_cost": 54529,
        "processes_covered": "Covers up to 10 processes",
        "implementation_processes": "Covers up to 5 processes"
    },
    "Platinum (10 Credits)": {
        "discovery_analysis": 281435,
        "build_implementation": 26180,
        "project_management": 180766,
        "infrastructure_license": 381480,
        "year_1_total": 869861,
        "year_2_cost": 100980,
        "year_3_cost": 109058,
        "processes_covered": "Covers up to 20 processes",
        "implementation_processes": "Covers up to 10 processes"
    }
}

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e40af, #3b82f6);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    .category-section {
        background: #f8fafc;
        border: 2px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 5px solid #3b82f6;
    }
    
    .service-card {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }
    
    .service-card:hover {
        border-color: #3b82f6;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
    }
    
    .cost-display {
        background: #f0f9ff;
        border: 2px solid #0ea5e9;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
        margin: 0.5rem 0;
        font-weight: bold;
    }
    
    .total-budget {
        background: linear-gradient(45deg, #dc2626, #ef4444);
        color: white;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        font-size: 1.2em;
        font-weight: bold;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(220, 38, 38, 0.3);
    }
    
    .support-package-card {
        background: white;
        border: 2px solid #e5e7eb;
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        text-align: center;
        position: relative;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    
    .support-package-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.15);
    }
    
    .support-package-card.basic {
        border-color: #6b7280;
        background: linear-gradient(135deg, #f9fafb 0%, #f3f4f6 100%);
    }
    
    .support-package-card.bronze {
        border-color: #92400e;
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
    }
    
    .support-package-card.silver {
        border-color: #374151;
        background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
    }
    
    .support-package-card.gold {
        border-color: #d97706;
        background: linear-gradient(135deg, #fef3c7 0%, #fcd34d 100%);
    }
    
    .support-package-card.platinum {
        border-color: #1e293b;
        background: linear-gradient(135deg, #e2e8f0 0%, #cbd5e1 100%);
    }
    
    .support-package-card.selected {
        border-color: #dc2626;
        background: linear-gradient(135deg, #fef2f2 0%, #fecaca 100%);
        box-shadow: 0 15px 35px rgba(220, 38, 38, 0.25);
    }
    
    .package-header {
        border-bottom: 1px solid rgba(0,0,0,0.1);
        padding-bottom: 1rem;
        margin-bottom: 1.5rem;
    }
    
    .package-name {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 0.5rem;
    }
    
    .package-price {
        font-size: 2rem;
        font-weight: 800;
        color: #dc2626;
        margin-bottom: 0.5rem;
    }
    
    .package-tagline {
        font-style: italic;
        color: #6b7280;
        font-size: 0.9rem;
        line-height: 1.4;
    }
    
    .package-features {
        text-align: left;
        flex-grow: 1;
        margin: 1rem 0;
    }
    
    .feature-item {
        display: flex;
        align-items: center;
        margin: 0.75rem 0;
        padding: 0.5rem;
        background: rgba(255,255,255,0.7);
        border-radius: 8px;
        font-size: 0.9rem;
    }
    
    .feature-icon {
        margin-right: 0.75rem;
        font-size: 1.1rem;
    }
    
    .feature-label {
        font-weight: 600;
        color: #374151;
    }
    
    .feature-value {
        color: #6b7280;
        margin-left: 0.5rem;
    }
    
    .select-button {
        background: linear-gradient(45deg, #3b82f6, #1d4ed8);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        cursor: pointer;
        transition: all 0.3s ease;
        margin-top: 1rem;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }
    
    .select-button:hover {
        background: linear-gradient(45deg, #1d4ed8, #1e40af);
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4);
    }
    
    .select-button.basic {
        background: linear-gradient(45deg, #6b7280, #4b5563);
    }
    
    .select-button.bronze {
        background: linear-gradient(45deg, #92400e, #78350f);
    }
    
    .select-button.silver {
        background: linear-gradient(45deg, #374151, #1f2937);
    }
    
    .select-button.gold {
        background: linear-gradient(45deg, #d97706, #b45309);
    }
    
    .select-button.platinum {
        background: linear-gradient(45deg, #1e293b, #0f172a);
    }
    
    .project-card {
        background: #fffbeb;
        border: 2px solid #f59e0b;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .custom-service {
        background: #f3e8ff;
        border: 2px solid #8b5cf6;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .sidebar-budget {
        position: sticky;
        top: 1rem;
    }
    
    .metric-card {
        background: white;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
        border: 1px solid #e5e7eb;
        margin: 0.5rem 0;
    }
    
    .category-selector {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .support-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .unlimited-badge {
        background: linear-gradient(45deg, #ef4444, #dc2626);
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-left: 0.5rem;
    }
    
    .popular-badge {
        position: absolute;
        top: -10px;
        right: 15px;
        background: linear-gradient(45deg, #f59e0b, #d97706);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
def initialize_session_state():
    if 'operational_services' not in st.session_state:
        st.session_state.operational_services = {}
    if 'custom_operational' not in st.session_state:
        st.session_state.custom_operational = []
    if 'support_package' not in st.session_state:
        st.session_state.support_package = None
    if 'support_extras' not in st.session_state:
        st.session_state.support_extras = {'support': 0, 'training': 0, 'reports': 0}
    if 'implementation_projects' not in st.session_state:
        st.session_state.implementation_projects = []
    if 'company_info' not in st.session_state:
        st.session_state.company_info = {}

initialize_session_state()

# Utility functions
def calculate_operational_total():
    total = 0
    
    # Predefined services
    for service_key, data in st.session_state.operational_services.items():
        if data.get('selected', False) and data.get('users', 0) > 0:
            users = data.get('users', 0)
            actual_service_name = data.get('actual_service_name', '')
            is_new_implementation = data.get('new_implementation', False)
            
            # Direct lookup using the actual service name stored in session state
            if actual_service_name in ORACLE_SERVICES:
                service_info = ORACLE_SERVICES[actual_service_name]
                monthly_cost = service_info['price_per_user'] * users
                setup_cost = service_info['setup_cost'] if is_new_implementation else 0
                total += (monthly_cost * 12) + setup_cost
            elif actual_service_name in MICROSOFT_SERVICES:
                service_info = MICROSOFT_SERVICES[actual_service_name]
                monthly_cost = service_info['price_per_user'] * users
                setup_cost = service_info['setup_cost'] if is_new_implementation else 0
                total += (monthly_cost * 12) + setup_cost
    
    # Custom services
    for custom_service in st.session_state.custom_operational:
        users = custom_service.get('users', 0)
        monthly_cost = custom_service.get('price_per_user', 0) * users
        setup_cost = custom_service.get('setup_cost', 0) if custom_service.get('new_implementation', False) else 0
        total += (monthly_cost * 12) + setup_cost
    
    return total

def calculate_support_total():
    total = 0
    
    if st.session_state.support_package:
        total += SUPPORT_PACKAGES[st.session_state.support_package]['price']
    
    # Add extras
    total += st.session_state.support_extras.get('support', 0) * 1800
    total += st.session_state.support_extras.get('training', 0) * 5399
    total += st.session_state.support_extras.get('reports', 0) * 5399
    
    return total

def calculate_implementation_total():
    return sum(project.get('budget', 0) for project in st.session_state.implementation_projects)

def calculate_total_budget():
    return calculate_operational_total() + calculate_support_total() + calculate_implementation_total()

# Header
def show_header():
    selected_company_info = st.session_state.company_info.get('company_code', '')
    
    header_subtitle = f"Shared Service Catalogue and Budgeting System"
    if selected_company_info:
        header_subtitle = f"{selected_company_info} - Shared Service Catalogue and Budgeting System"
    
    st.markdown(f"""
    <div class='main-header'>
        <h1>💼 Alkhorayef Group</h1>
        <h2>2025 Shared Service Catalogue</h2>
        <p>{header_subtitle}</p>
        <p><strong>Budget Year:</strong> 2025 | <strong>Version:</strong> 2.0</p>
    </div>
    """, unsafe_allow_html=True)

# Sidebar for company info and budget summary
def show_sidebar():
    with st.sidebar:
        st.markdown("### 🏢 Company Information")
        
        st.markdown("**🏭 Alkhorayef Group**")
        
        # Company selection with abbreviations only
        selected_company = st.selectbox(
            "Select Your Company", 
            options=ALKHORAYEF_COMPANIES,
            index=0,
            key="company_selection",
            help="Choose which Alkhorayef Group company you represent"
        )
        
        # Display selected company info with abbreviation only
        st.markdown(f"""
        <div style='background: #f0f9ff; border: 1px solid #0ea5e9; border-radius: 8px; padding: 1rem; margin: 0.5rem 0;'>
            <strong>Selected:</strong> {selected_company}
        </div>
        """, unsafe_allow_html=True)
        
        department = st.text_input("Department", key="department", placeholder="e.g., IT, Finance, Operations")
        contact_person = st.text_input("Contact Person", key="contact_person", placeholder="Your full name")
        email = st.text_input("Email", key="email", placeholder="your.email@alkhorayef.com")
        
        st.session_state.company_info = {
            'company': selected_company,
            'company_code': selected_company,
            'department': department,
            'contact_person': contact_person,
            'email': email,
            'date': datetime.now().strftime("%Y-%m-%d")
        }
        
        st.markdown("---")
        
        # Budget summary
        st.markdown("### 💰 Service Selection Summary")
        
        operational_total = calculate_operational_total()
        support_total = calculate_support_total()
        implementation_total = calculate_implementation_total()
        total_budget = operational_total + support_total + implementation_total
        
        st.markdown(f"""
        <div class='metric-card'>
            <h4>Operational Services</h4>
            <h3>SAR {operational_total:,.0f}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class='metric-card'>
            <h4>Support Packages</h4>
            <h3>SAR {support_total:,.0f}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class='metric-card'>
            <h4>Custom Implementations</h4>
            <h3>SAR {implementation_total:,.0f}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class='total-budget'>
            💰 Total 2025 Shared Services Budget<br>
            <span style='font-size: 1.5em'>SAR {total_budget:,.0f}</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Progress indicators
        operational_count = len([k for k, v in st.session_state.operational_services.items() if v.get('selected', False) and v.get('users', 0) > 0]) + len(st.session_state.custom_operational)
        support_selected = 1 if st.session_state.support_package else 0
        implementation_count = len(st.session_state.implementation_projects)
        
        st.markdown("### 📊 Service Selection Progress")
        st.metric("Operational Services", operational_count)
        st.metric("Support Package", "Selected" if support_selected else "Not Selected")
        st.metric("Implementation Projects", implementation_count)
        
        # Show support package details if selected
        if st.session_state.support_package:
            st.markdown("### 📋 Selected Support Package")
            selected_package = SUPPORT_PACKAGES[st.session_state.support_package]
            st.markdown(f"**{st.session_state.support_package}**")
            st.markdown(f"- Total Support Requests: {selected_package.get('total_support_requests', 'N/A')}")
            st.markdown(f"- Improvement Hours: {selected_package.get('improvement_hours', 'N/A')}")
            st.markdown(f"- Training Requests: {selected_package.get('training_requests', 'N/A')}")
            st.markdown(f"- Report Requests: {selected_package.get('report_requests', 'N/A')}")
            
            # Show additional services if any
            extra_support = st.session_state.support_extras.get('support', 0)
            extra_training = st.session_state.support_extras.get('training', 0) 
            extra_reports = st.session_state.support_extras.get('reports', 0)
            
            if extra_support > 0 or extra_training > 0 or extra_reports > 0:
                st.markdown("**Additional Services:**")
                if extra_support > 0:
                    st.markdown(f"- Extra Support: {extra_support}")
                if extra_training > 0:
                    st.markdown(f"- Extra Training: {extra_training}")
                if extra_reports > 0:
                    st.markdown(f"- Extra Reports: {extra_reports}")

# Operational Services Section
def show_operational_services():
    st.markdown("""
    <div class='category-section'>
        <h2>🔧 Operational Services</h2>
        <p>Select recurring licenses and software subscriptions for daily operations.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Oracle Services
    st.markdown("### 🟠 Oracle Cloud Services")
    
    col1, col2 = st.columns(2)
    oracle_services = list(ORACLE_SERVICES.items())
    
    for i, (service_name, details) in enumerate(oracle_services):
        col = col1 if i % 2 == 0 else col2
        service_key = f"oracle_{service_name.lower().replace(' ', '_').replace('&', 'and')}"
        
        with col:
            st.markdown(f"""
            <div class='service-card'>
                <h4>{service_name}</h4>
                <p style='color: #6b7280; font-size: 0.9em;'>{details['description']}</p>
                <div style='background: #f3f4f6; padding: 0.5rem; border-radius: 5px; margin: 0.5rem 0;'>
                    💰 SAR {details['price_per_user']}/user/month<br>
                    🆕 Setup (new implementation): SAR {details['setup_cost']:,}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Initialize service data if not exists
            if service_key not in st.session_state.operational_services:
                st.session_state.operational_services[service_key] = {
                    'selected': False, 
                    'users': 0, 
                    'actual_service_name': service_name,
                    'new_implementation': False
                }
            
            # Get current values from session state
            current_selected = st.session_state.operational_services[service_key].get('selected', False)
            current_users = st.session_state.operational_services[service_key].get('users', 0)
            current_new_impl = st.session_state.operational_services[service_key].get('new_implementation', False)
            
            selected = st.checkbox(f"Include {service_name}", 
                                 key=f"{service_key}_selected",
                                 value=current_selected)
            
            if selected:
                # New Implementation checkbox
                new_implementation = st.checkbox(
                    "🆕 New Implementation", 
                    key=f"{service_key}_new_impl",
                    value=current_new_impl,
                    help="Check this if it's a new implementation requiring setup. Uncheck if adding users to existing system."
                )
                
                users = st.number_input(f"Number of users for {service_name}", 
                                      min_value=0, 
                                      value=current_users,
                                      key=f"{service_key}_users",
                                      step=1)
                
                # Update session state immediately
                st.session_state.operational_services[service_key] = {
                    'selected': True,
                    'users': users,
                    'actual_service_name': service_name,
                    'new_implementation': new_implementation
                }
                
                if users > 0:
                    monthly_cost = details['price_per_user'] * users
                    setup_cost = details['setup_cost'] if new_implementation else 0
                    annual_cost = monthly_cost * 12 + setup_cost
                    
                    setup_text = f" + SAR {setup_cost:,} setup" if new_implementation else " (no setup cost)"
                    
                    st.markdown(f"""
                    <div class='cost-display'>
                        📊 Monthly: SAR {monthly_cost:,.0f}{setup_text}<br>
                        <strong>Annual Total: SAR {annual_cost:,.0f}</strong>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.session_state.operational_services[service_key] = {
                    'selected': False,
                    'users': 0,
                    'actual_service_name': service_name,
                    'new_implementation': False
                }
    
    st.markdown("---")
    
    # Microsoft Services
    st.markdown("### 🟦 Microsoft Cloud Services")
    
    col1, col2 = st.columns(2)
    microsoft_services = list(MICROSOFT_SERVICES.items())
    
    for i, (service_name, details) in enumerate(microsoft_services):
        col = col1 if i % 2 == 0 else col2
        service_key = f"microsoft_{service_name.lower().replace(' ', '_').replace('&', 'and')}"
        
        with col:
            st.markdown(f"""
            <div class='service-card'>
                <h4>{service_name}</h4>
                <p style='color: #6b7280; font-size: 0.9em;'>{details['description']}</p>
                <div style='background: #f3f4f6; padding: 0.5rem; border-radius: 5px; margin: 0.5rem 0;'>
                    💰 SAR {details['price_per_user']}/user/month<br>
                    🆕 Setup (new implementation): SAR {details['setup_cost']:,}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Initialize service data if not exists
            if service_key not in st.session_state.operational_services:
                st.session_state.operational_services[service_key] = {
                    'selected': False, 
                    'users': 0, 
                    'actual_service_name': service_name,
                    'new_implementation': False
                }
            
            # Get current values from session state
            current_selected = st.session_state.operational_services[service_key].get('selected', False)
            current_users = st.session_state.operational_services[service_key].get('users', 0)
            current_new_impl = st.session_state.operational_services[service_key].get('new_implementation', False)
            
            selected = st.checkbox(f"Include {service_name}", 
                                 key=f"{service_key}_selected",
                                 value=current_selected)
            
            if selected:
                # New Implementation checkbox
                new_implementation = st.checkbox(
                    "🆕 New Implementation", 
                    key=f"{service_key}_new_impl",
                    value=current_new_impl,
                    help="Check this if it's a new implementation requiring setup. Uncheck if adding users to existing system."
                )
                
                users = st.number_input(f"Number of users for {service_name}", 
                                      min_value=0, 
                                      value=current_users,
                                      key=f"{service_key}_users",
                                      step=1)
                
                # Update session state immediately
                st.session_state.operational_services[service_key] = {
                    'selected': True,
                    'users': users,
                    'actual_service_name': service_name,
                    'new_implementation': new_implementation
                }
                
                if users > 0:
                    monthly_cost = details['price_per_user'] * users
                    setup_cost = details['setup_cost'] if new_implementation else 0
                    annual_cost = monthly_cost * 12 + setup_cost
                    
                    setup_text = f" + SAR {setup_cost:,} setup" if new_implementation else " (no setup cost)"
                    
                    st.markdown(f"""
                    <div class='cost-display'>
                        📊 Monthly: SAR {monthly_cost:,.0f}{setup_text}<br>
                        <strong>Annual Total: SAR {annual_cost:,.0f}</strong>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.session_state.operational_services[service_key] = {
                    'selected': False,
                    'users': 0,
                    'actual_service_name': service_name,
                    'new_implementation': False
                }
    
    st.markdown("---")
    
    # Custom Services
    st.markdown("### ➕ Add Custom Services")
    
    with st.expander("Add Custom Operational Service", expanded=False):
        st.markdown("""
        <div class='custom-service'>
            <h4>Define Your Custom Service</h4>
            <p>Add any additional operational software or service not listed above.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            custom_name = st.text_input("Service Name", placeholder="e.g., Custom CRM Solution", key="custom_service_name_input")
            custom_price = st.number_input("Price per User/Month (SAR)", min_value=0, value=50, key="custom_service_price_input")
        
        with col2:
            custom_setup = st.number_input("Setup Cost (SAR)", min_value=0, value=5000, key="custom_service_setup_input")
            custom_users = st.number_input("Number of Users", min_value=0, value=0, key="custom_service_users_input")
        
        custom_description = st.text_area("Service Description", 
                                        placeholder="Describe what this service provides...", 
                                        key="custom_service_description_input")
        
        custom_new_implementation = st.checkbox(
            "🆕 New Implementation (includes setup cost)", 
            value=True,
            help="Check if this is a new implementation requiring setup cost",
            key="custom_service_new_impl_input"
        )
        
        if st.button("Add Custom Service", key="add_custom_operational_service_btn"):
            if custom_name and custom_description and custom_users > 0:
                custom_service = {
                    'name': custom_name,
                    'description': custom_description,
                    'price_per_user': custom_price,
                    'setup_cost': custom_setup,
                    'users': custom_users,
                    'new_implementation': custom_new_implementation
                }
                
                st.session_state.custom_operational.append(custom_service)
                st.success(f"✅ Added custom service: {custom_name}")
                st.rerun()
            else:
                st.error("Please fill in all required fields and specify at least 1 user.")
    
    # Display custom services
    if st.session_state.custom_operational:
        st.markdown("### 📋 Your Custom Services")
        
        for i, service in enumerate(st.session_state.custom_operational):
            monthly_cost = service['price_per_user'] * service['users']
            setup_cost = service['setup_cost'] if service.get('new_implementation', False) else 0
            annual_cost = monthly_cost * 12 + setup_cost
            
            implementation_status = "New Implementation" if service.get('new_implementation', False) else "Adding to Existing"
            setup_display = f"Setup: SAR {setup_cost:,}" if service.get('new_implementation', False) else "No Setup Cost"
            
            st.markdown(f"""
            <div class='service-card' style='border-left: 4px solid #8b5cf6;'>
                <h4>{service['name']} (Custom)</h4>
                <p style='color: #6b7280;'>{service['description']}</p>
                <p><strong>Users:</strong> {service['users']} | <strong>Status:</strong> {implementation_status}</p>
                <p><strong>Monthly:</strong> SAR {monthly_cost:,.0f} | <strong>{setup_display}</strong> | <strong>Annual:</strong> SAR {annual_cost:,.0f}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Remove {service['name']}", key=f"remove_custom_service_{i}"):
                st.session_state.custom_operational.pop(i)
                st.rerun()

# Support Packages Section with Comprehensive Comparison Table
def show_support_packages():
    st.markdown("""
    <div class='category-section'>
        <h2>🛠️ Support Packages</h2>
        <p>Choose the support level that best fits your organization's needs. Compare all features and pricing in the comprehensive table below.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📞 Support Packages Comparison")
    
    # Create comprehensive comparison table
    packages_list = list(SUPPORT_PACKAGES.items())
    
    # Define package colors
    package_colors = {
        "Basic": "#6b7280",
        "Bronze": "#92400e", 
        "Silver": "#374151",
        "Gold": "#d97706",
        "Platinum": "#1e293b"
    }
    
    # Create the comparison table HTML
    table_html = """
    <table style='width: 100%; border-collapse: collapse; margin: 2rem 0; font-size: 14px;'>
        <thead>
            <tr style='background: #f8fafc;'>
                <th style='padding: 1rem; text-align: left; border: 1px solid #e5e7eb; font-weight: 600;'>Features</th>
    """
    
    # Add package headers with colors
    for package_name, _ in packages_list:
        color = package_colors.get(package_name, "#6b7280")
        table_html += f"""
                <th style='padding: 1rem; text-align: center; border: 1px solid #e5e7eb; background: {color}; color: white; font-weight: 600;'>
                    {package_name.upper()}
                </th>
        """
    
    table_html += """
            </tr>
        </thead>
        <tbody>
    """
    
    # Add rows for each feature
    features = [
        ("Systems Operation", "systems_operation"),
        ("Support Requests (Standard)", "support_requests_standard"),
        ("Support Requests (Priority)", "support_requests_priority"), 
        ("Support Requests (Premium)", "support_requests_premium"),
        ("Total Support Requests", "total_support_requests"),
        ("System Improvement Hours", "improvement_hours"),
        ("Training Requests", "training_requests"),
        ("New Reports Requests", "report_requests"),
        ("Total Package Cost (SAR)", "price"),
    ]
    
    for i, (feature_name, feature_key) in enumerate(features):
        bg_color = "#f9fafb" if i % 2 == 0 else "#ffffff"
        table_html += f"""
            <tr style='background: {bg_color};'>
                <td style='padding: 0.75rem; border: 1px solid #e5e7eb; font-weight: 500;'>{feature_name}</td>
        """
        
        for package_name, details in packages_list:
            value = details.get(feature_key, "N/A")
            
            # Format the value based on feature type
            if feature_key == "price":
                formatted_value = f"SAR {value:,.0f}"
                style = "font-weight: 700; color: #dc2626;"
            elif feature_key == "systems_operation":
                formatted_value = value
                style = "color: #16a34a; font-weight: 600;"
            elif isinstance(value, int):
                if value == 0:
                    formatted_value = "0"
                    style = "color: #6b7280;"
                else:
                    formatted_value = str(value)
                    style = "font-weight: 600; color: #1f2937;"
            else:
                formatted_value = str(value)
                style = ""
            
            # Highlight selected package
            is_selected = st.session_state.support_package == package_name
            cell_bg = "#fef2f2" if is_selected else "inherit"
            border_style = "border: 2px solid #dc2626;" if is_selected else "border: 1px solid #e5e7eb;"
            
            table_html += f"""
                <td style='padding: 0.75rem; {border_style} text-align: center; {style} background: {cell_bg};'>
                    {formatted_value}
                </td>
            """
        
        table_html += "</tr>"
    
    table_html += """
        </tbody>
    </table>
    """
    
    st.markdown(table_html, unsafe_allow_html=True)
    
    # Package selection buttons
    st.markdown("### 🎯 Select Your Support Package")
    cols = st.columns(len(packages_list))
    
    for i, (package_name, details) in enumerate(packages_list):
        with cols[i]:
            is_selected = st.session_state.support_package == package_name
            
            # Package summary card
            color = package_colors.get(package_name, "#6b7280")
            bg_color = "#fef2f2" if is_selected else "#f8fafc"
            border_color = "#dc2626" if is_selected else color
            
            st.markdown(f"""
            <div style='
                background: {bg_color}; 
                border: 2px solid {border_color}; 
                border-radius: 12px; 
                padding: 1rem; 
                text-align: center;
                margin-bottom: 1rem;
            '>
                <h4 style='color: {color}; margin: 0 0 0.5rem 0;'>{package_name}</h4>
                <h3 style='color: #dc2626; margin: 0 0 0.5rem 0;'>SAR {details["price"]:,.0f}</h3>
                <p style='font-size: 0.9em; color: #6b7280; margin: 0;'>{details["description"]}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Selection button
            button_text = "✅ Selected" if is_selected else f"Select {package_name}"
            button_type = "secondary" if is_selected else "primary"
            
            if st.button(button_text, 
                        key=f"select_package_{package_name.lower()}_btn", 
                        disabled=is_selected,
                        type=button_type,
                        use_container_width=True):
                st.session_state.support_package = package_name
                st.success(f"✅ Selected {package_name} Support Package")
                st.rerun()
    
    # Additional services section
    if st.session_state.support_package:
        selected_package = SUPPORT_PACKAGES[st.session_state.support_package]
        
        st.markdown("### ➕ Additional Support Services")
        st.markdown("Enhance your selected package with additional services as needed.")
        
        # Show additional service costs table
        st.markdown("""
        <table style='width: 100%; border-collapse: collapse; margin: 1rem 0;'>
            <thead>
                <tr style='background: #f8fafc;'>
                    <th style='padding: 0.75rem; text-align: left; border: 1px solid #e5e7eb;'>Additional Service</th>
                    <th style='padding: 0.75rem; text-align: center; border: 1px solid #e5e7eb;'>Cost (SAR)</th>
                    <th style='padding: 0.75rem; text-align: center; border: 1px solid #e5e7eb;'>Available for All Packages</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td style='padding: 0.75rem; border: 1px solid #e5e7eb;'>Additional Support Request</td>
                    <td style='padding: 0.75rem; border: 1px solid #e5e7eb; text-align: center; font-weight: 600;'>1,800</td>
                    <td style='padding: 0.75rem; border: 1px solid #e5e7eb; text-align: center; color: #16a34a;'>✓ Yes</td>
                </tr>
                <tr style='background: #f9fafb;'>
                    <td style='padding: 0.75rem; border: 1px solid #e5e7eb;'>Additional Training Request</td>
                    <td style='padding: 0.75rem; border: 1px solid #e5e7eb; text-align: center; font-weight: 600;'>5,399</td>
                    <td style='padding: 0.75rem; border: 1px solid #e5e7eb; text-align: center; color: #16a34a;'>✓ Yes</td>
                </tr>
                <tr>
                    <td style='padding: 0.75rem; border: 1px solid #e5e7eb;'>Additional New Reports Request</td>
                    <td style='padding: 0.75rem; border: 1px solid #e5e7eb; text-align: center; font-weight: 600;'>5,399</td>
                    <td style='padding: 0.75rem; border: 1px solid #e5e7eb; text-align: center; color: #16a34a;'>✓ Yes</td>
                </tr>
            </tbody>
        </table>
        """, unsafe_allow_html=True)
        
        # Additional services input
        col1, col2, col3 = st.columns(3)
        
        with col1:
            extra_support = st.number_input(
                "🛠️ Extra Support Requests", 
                min_value=0, 
                value=st.session_state.support_extras.get('support', 0),
                key="extra_support_requests_input"
            )
            st.session_state.support_extras['support'] = extra_support
        
        with col2:
            extra_training = st.number_input(
                "🎓 Extra Training Requests", 
                min_value=0, 
                value=st.session_state.support_extras.get('training', 0),
                key="extra_training_requests_input"
            )
            st.session_state.support_extras['training'] = extra_training
        
        with col3:
            extra_reports = st.number_input(
                "📊 Extra Report Requests", 
                min_value=0, 
                value=st.session_state.support_extras.get('reports', 0),
                key="extra_reports_requests_input"
            )
            if 'reports' not in st.session_state.support_extras:
                st.session_state.support_extras['reports'] = 0
            st.session_state.support_extras['reports'] = extra_reports
        
        # Calculate total cost
        base_cost = selected_package['price']
        extra_support_cost = extra_support * 1800
        extra_training_cost = extra_training * 5399
        extra_reports_cost = extra_reports * 5399
        total_extra_cost = extra_support_cost + extra_training_cost + extra_reports_cost
        total_cost = base_cost + total_extra_cost
        
        if total_extra_cost > 0:
            st.markdown(f"""
            <div style='background: #fef3c7; border: 2px solid #f59e0b; border-radius: 12px; padding: 1.5rem; margin: 1rem 0;'>
                <h4 style='margin: 0 0 1rem 0; color: #92400e;'>💰 Cost Summary</h4>
                <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;'>
                    <div>
                        <strong>Base Package ({st.session_state.support_package}):</strong><br>
                        SAR {base_cost:,.0f}
                    </div>
                    <div>
                        <strong>Additional Services:</strong><br>
                        SAR {total_extra_cost:,.0f}
                    </div>
                </div>
                <hr style='margin: 1rem 0; border: 1px solid #f59e0b;'>
                <div style='text-align: center;'>
                    <h3 style='margin: 0; color: #dc2626;'>Total Support Cost: SAR {total_cost:,.0f}</h3>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Breakdown
            if extra_support > 0:
                st.markdown(f"- **Extra Support:** {extra_support} × SAR 1,800 = SAR {extra_support_cost:,.0f}")
            if extra_training > 0:
                st.markdown(f"- **Extra Training:** {extra_training} × SAR 5,399 = SAR {extra_training_cost:,.0f}")
            if extra_reports > 0:
                st.markdown(f"- **Extra Reports:** {extra_reports} × SAR 5,399 = SAR {extra_reports_cost:,.0f}")
        else:
            st.markdown(f"""
            <div style='background: #dcfce7; border: 2px solid #16a34a; border-radius: 12px; padding: 1.5rem; margin: 1rem 0; text-align: center;'>
                <h3 style='margin: 0; color: #16a34a;'>✅ Selected: {st.session_state.support_package} - SAR {base_cost:,.0f}</h3>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("👆 Please select a support package from the table above to continue.")

# Implementation Projects Section with Enhanced Categories
def show_implementation_projects():
    st.markdown("""
    <div class='category-section'>
        <h2>🚀 Custom Implementation Projects</h2>
        <p>Define your strategic technology initiatives and custom development projects.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Add new project form
    st.markdown("### ➕ Add New Implementation Project")
    
    with st.expander("Define New Project", expanded=True):
        st.markdown("""
        <div class='project-card'>
            <h4>Project Details</h4>
            <p>Provide comprehensive information about your implementation project.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            project_name = st.text_input("Project Name", placeholder="e.g., AI-Powered Analytics Platform", key="project_name_input")
            
            # Enhanced project type selection with categories
            st.markdown("#### Select Project Category & Type")
            st.markdown("""
            <div class='category-selector'>
                <p style='margin-bottom: 0.5rem; font-weight: 500;'>Choose from our comprehensive service categories:</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Category selection
            selected_category = st.selectbox(
                "Project Category", 
                options=list(PROJECT_CATEGORIES.keys()),
                key="project_category_input",
                help="Select the main category for your project"
            )
            
            # Service type based on selected category
            project_type = st.selectbox(
                "Specific Service Type", 
                options=PROJECT_CATEGORIES[selected_category],
                key="project_type_input",
                help=f"Select the specific service within {selected_category}"
            )
            
            timeline = st.selectbox("Timeline", ["Q1 2025", "Q2 2025", "Q3 2025", "Q4 2025", "Multi-quarter", "2+ years"], key="project_timeline_input")
            priority = st.select_slider("Priority Level", ["Low", "Medium", "High", "Critical"], value="Medium", key="project_priority_input")
        
        with col2:
            budget = st.number_input("Budget Estimate (SAR)", min_value=0, value=100000, step=10000, key="project_budget_input")
            departments = st.multiselect("Departments Involved", DEPARTMENTS, key="project_departments_input")
            
            # Show category description
            category_descriptions = {
                "🤖 Digital Transformation & Automation": "Streamline operations through intelligent automation and process optimization",
                "🧠 AI & Advanced Analytics": "Leverage artificial intelligence and machine learning for data-driven insights",
                "📊 Data & Business Intelligence": "Transform raw data into actionable business intelligence and reporting",
                "💼 Enterprise Applications": "Implement core business applications for operational excellence",
                "🏭 Industry-Specific Solutions": "Specialized solutions for manufacturing and industrial operations",
                "☁️ Infrastructure & Cloud": "Modernize IT infrastructure with cloud-native technologies",
                "🔒 Security & Compliance": "Enhance cybersecurity posture and regulatory compliance",
                "🔗 Integration & Connectivity": "Connect systems and enable seamless data flow",
                "💬 Communication & Collaboration": "Improve team collaboration and communication capabilities",
                "👥 Customer Experience": "Enhance customer interactions and engagement platforms",
                "💰 Financial & Regulatory": "Strengthen financial management and regulatory compliance",
                "🌱 Sustainability & ESG": "Support environmental and sustainability initiatives",
                "⚙️ Custom & Specialized": "Tailored solutions for unique business requirements"
            }
            
            if selected_category in category_descriptions:
                st.info(f"**{selected_category}**: {category_descriptions[selected_category]}")
            
        project_description = st.text_area("Project Description", 
                                         placeholder="Describe the project scope, objectives, and expected outcomes...", 
                                         key="project_description_input")
        
        success_criteria = st.text_area("Success Criteria", 
                                      placeholder="Define how success will be measured...", 
                                      key="project_success_criteria_input")
        
        # Special handling for RPA projects
        if project_type == "RPA (Robotic Process Automation)":
            st.markdown("#### 🤖 RPA Package Selection")
            st.info("For RPA projects, you can select from our predefined packages or specify a custom budget.")
            
            use_rpa_package = st.checkbox("Use Predefined RPA Package", key="use_rpa_package_input")
            
            if use_rpa_package:
                rpa_package = st.selectbox("Select RPA Package", list(RPA_PACKAGES.keys()), key="rpa_package_selection")
                
                if rpa_package:
                    package_details = RPA_PACKAGES[rpa_package]
                    st.markdown(f"""
                    **Selected Package:** {rpa_package}  
                    **Year 1 Budget:** SAR {package_details['year_1_total']:,.0f}  
                    **{package_details['processes_covered']}**  
                    **Implementation:** {package_details['implementation_processes']}
                    """)
                    
                    # Update budget with RPA package cost
                    budget = package_details['year_1_total']
                    st.session_state['project_budget_input'] = budget
        
        if st.button("Add Project", type="primary", key="add_implementation_project_btn"):
            if project_name and project_description and budget > 0:
                new_project = {
                    'name': project_name,
                    'category': selected_category,
                    'type': project_type,
                    'description': project_description,
                    'timeline': timeline,
                    'priority': priority,
                    'budget': budget,
                    'departments': departments,
                    'success_criteria': success_criteria,
                    'created_date': datetime.now().strftime("%Y-%m-%d")
                }
                
                # Add RPA package details if applicable
                if project_type == "RPA (Robotic Process Automation)" and 'use_rpa_package_input' in st.session_state and st.session_state['use_rpa_package_input']:
                    if 'rpa_package_selection' in st.session_state:
                        rpa_package = st.session_state['rpa_package_selection']
                        new_project['rpa_package'] = True
                        new_project['rpa_details'] = RPA_PACKAGES[rpa_package]
                        new_project['rpa_package_name'] = rpa_package
                
                st.session_state.implementation_projects.append(new_project)
                st.success(f"✅ Added project: {project_name}")
                st.rerun()
            else:
                st.error("Please fill in project name, description, and budget.")
    
    # Display existing projects
    if st.session_state.implementation_projects:
        st.markdown("### 📋 Your Implementation Projects")
        
        total_implementation_budget = 0
        
        # Group projects by category for better organization
        projects_by_category = {}
        for project in st.session_state.implementation_projects:
            category = project.get('category', '⚙️ Custom & Specialized')
            if category not in projects_by_category:
                projects_by_category[category] = []
            projects_by_category[category].append(project)
        
        for category, projects in projects_by_category.items():
            st.markdown(f"#### {category}")
            
            for i, project in enumerate(projects):
                # Find the original index in the full projects list
                original_index = st.session_state.implementation_projects.index(project)
                total_implementation_budget += project['budget']
                
                # Color coding by priority
                priority_colors = {
                    'Low': '#10b981',
                    'Medium': '#f59e0b', 
                    'High': '#ef4444',
                    'Critical': '#dc2626'
                }
                
                priority_color = priority_colors.get(project['priority'], '#6b7280')
                
                # Special display for RPA packages
                if project.get('rpa_package', False):
                    rpa_details = project.get('rpa_details', {})
                    three_year_total = rpa_details.get('year_1_total', 0) + rpa_details.get('year_2_cost', 0) + rpa_details.get('year_3_cost', 0)
                    
                    st.markdown(f"""
                    <div class='project-card' style='border-left: 4px solid {priority_color};'>
                        <div style='display: flex; justify-content: space-between; align-items: start;'>
                            <div style='flex: 1;'>
                                <h4>{project['name']} 🤖</h4>
                                <p style='color: #6b7280; margin: 0.5rem 0;'><strong>RPA Package:</strong> {project.get('rpa_package_name', 'Custom')}</p>
                                <p style='color: #6b7280; margin: 0.5rem 0;'><strong>Timeline:</strong> {project['timeline']}</p>
                                <p style='color: {priority_color}; margin: 0.5rem 0;'><strong>Priority:</strong> {project['priority']}</p>
                                <p style='margin: 0.5rem 0;'>{project['description']}</p>
                                <p style='margin: 0.5rem 0;'><strong>Process Coverage:</strong> {rpa_details.get('processes_covered', 'N/A')}</p>
                                {f"<p style='margin: 0.5rem 0;'><strong>Departments:</strong> {', '.join(project['departments'])}</p>" if project['departments'] else ""}
                            </div>
                            <div style='text-align: right; margin-left: 1rem;'>
                                <h3 style='color: #1f2937; margin: 0;'>SAR {project['budget']:,.0f}</h3>
                                <p style='color: #6b7280; font-size: 0.9em; margin: 0;'>Year 1</p>
                                <p style='color: #6b7280; font-size: 0.9em; margin: 0;'>3-Year: SAR {three_year_total:,.0f}</p>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class='project-card' style='border-left: 4px solid {priority_color};'>
                        <div style='display: flex; justify-content: space-between; align-items: start;'>
                            <div style='flex: 1;'>
                                <h4>{project['name']}</h4>
                                <p style='color: #6b7280; margin: 0.5rem 0;'><strong>Type:</strong> {project['type']}</p>
                                <p style='color: #6b7280; margin: 0.5rem 0;'><strong>Timeline:</strong> {project['timeline']}</p>
                                <p style='color: {priority_color}; margin: 0.5rem 0;'><strong>Priority:</strong> {project['priority']}</p>
                                <p style='margin: 0.5rem 0;'>{project['description']}</p>
                                {f"<p style='margin: 0.5rem 0;'><strong>Departments:</strong> {', '.join(project['departments'])}</p>" if project['departments'] else ""}
                            </div>
                            <div style='text-align: right; margin-left: 1rem;'>
                                <h3 style='color: #1f2937; margin: 0;'>SAR {project['budget']:,.0f}</h3>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                col1, col2 = st.columns([3, 1])
                with col2:
                    if st.button(f"Remove", key=f"remove_implementation_project_{original_index}"):
                        st.session_state.implementation_projects.pop(original_index)
                        st.rerun()
        
        st.markdown(f"""
        <div class='cost-display' style='background: #fef3c7; border-color: #f59e0b;'>
            💰 Total Implementation Budget: <strong>SAR {total_implementation_budget:,.0f}</strong>
        </div>
        """, unsafe_allow_html=True)

# Summary Section (keeping the existing implementation)
def show_summary():
    st.markdown("""
    <div class='category-section'>
        <h2>📊 Service Catalogue Summary & Budget Analysis</h2>
        <p>Comprehensive overview of your 2025 shared services selection and investment strategy.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Calculate totals
    operational_total = calculate_operational_total()
    support_total = calculate_support_total()
    implementation_total = calculate_implementation_total()
    total_budget = operational_total + support_total + implementation_total
    
    if total_budget == 0:
        st.info("👋 No services selected yet. Please visit the other sections to build your shared services selection.")
        return
    
    # Budget overview metrics
    st.markdown("### 💰 Service Selection Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Operational Services", f"SAR {operational_total:,.0f}", 
                 f"{operational_total/total_budget*100:.1f}%" if total_budget > 0 else "0%")
    
    with col2:
        st.metric("Support Packages", f"SAR {support_total:,.0f}", 
                 f"{support_total/total_budget*100:.1f}%" if total_budget > 0 else "0%")
    
    with col3:
        st.metric("Implementation", f"SAR {implementation_total:,.0f}", 
                 f"{implementation_total/total_budget*100:.1f}%" if total_budget > 0 else "0%")
    
    with col4:
        st.markdown(f"""
        <div class='total-budget'>
            💰 Total 2025 Shared Services Budget<br>
            <span style='font-size: 1.8em'>SAR {total_budget:,.0f}</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Charts
    col1, col2 = st.columns(2)
    
    # Pie chart for budget distribution
    with col1:
        if total_budget > 0:
            fig_pie = px.pie(
                values=[operational_total, support_total, implementation_total],
                names=['Operational Services', 'Support Packages', 'Implementation Projects'],
                title="2025 Shared Services Budget Distribution",
                color_discrete_map={
                    'Operational Services': '#3b82f6',
                    'Support Packages': '#10b981',
                    'Implementation Projects': '#f59e0b'
                }
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pie, use_container_width=True, key="budget_pie_chart")
    
    # Monthly cash flow projection
    with col2:
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        
        monthly_operational = [0] * 12
        monthly_support = [0] * 12
        monthly_implementation = [0] * 12
        
        # Support and Operational costs are billed at year-end (December)
        monthly_operational[11] = operational_total
        monthly_support[11] = support_total
        
        # Implementation projects billed based on timeline/completion
        if st.session_state.implementation_projects:
            q1_projects = []
            q2_projects = []
            q3_projects = []
            q4_projects = []
            multi_quarter_projects = []
            
            for project in st.session_state.implementation_projects:
                timeline = project.get('timeline', 'Q4 2025')
                budget = project.get('budget', 0)
                
                if project.get('rpa_package', False):
                    multi_quarter_projects.append(budget)
                elif 'Q1' in timeline:
                    q1_projects.append(budget)
                elif 'Q2' in timeline:
                    q2_projects.append(budget)
                elif 'Q3' in timeline:
                    q3_projects.append(budget)
                elif 'Q4' in timeline:
                    q4_projects.append(budget)
                else:
                    multi_quarter_projects.append(budget)
            
            if q1_projects:
                monthly_implementation[2] = sum(q1_projects)
            if q2_projects:
                monthly_implementation[5] = sum(q2_projects)
            if q3_projects:
                monthly_implementation[8] = sum(q3_projects)
            if q4_projects:
                monthly_implementation[11] = sum(q4_projects)
            if multi_quarter_projects:
                monthly_amount = sum(multi_quarter_projects) / 12
                monthly_implementation = [x + monthly_amount for x in monthly_implementation]
        
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(name='Operational (Year-end)', x=months, y=monthly_operational, marker_color='#3b82f6'))
        fig_bar.add_trace(go.Bar(name='Support (Year-end)', x=months, y=monthly_support, marker_color='#10b981'))
        fig_bar.add_trace(go.Bar(name='Implementation (On Completion)', x=months, y=monthly_implementation, marker_color='#f59e0b'))
        
        fig_bar.update_layout(
            title='Monthly Shared Services Cash Flow Projection (SAR)<br><sub>Support & Operations billed year-end | Projects billed on completion</sub>',
            barmode='stack',
            xaxis_title='Month',
            yaxis_title='Cost (SAR)',
            showlegend=True
        )
        st.plotly_chart(fig_bar, use_container_width=True, key="cash_flow_chart")
    
    # Export and submission options
    st.markdown("### 📤 Export & Submit Selection")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📊 Export to Excel", use_container_width=True, key="export_excel_btn"):
            st.success("📊 Excel export functionality would generate a comprehensive budget report including all selected services, costs, and projections.")
    
    with col2:
        if st.button("💾 Save Draft", use_container_width=True, key="save_draft_btn"):
            st.success("💾 Draft saved! Your selections have been preserved and you can continue editing later.")
    
    with col3:
        if st.button("📧 Share Summary", use_container_width=True, key="share_summary_btn"):
            st.success("📧 Budget summary prepared for sharing with stakeholders and finance team.")
    
    with col4:
        if st.button("🚀 Submit Final Budget", type="primary", use_container_width=True, key="submit_final_budget_btn"):
            company_code = st.session_state.company_info.get('company_code', 'ALK')
            reference_id = f"{company_code}-2025-{datetime.now().strftime('%Y%m%d%H%M%S')}-{str(uuid.uuid4())[:8].upper()}"
            
            st.balloons()
            st.success(f"""
            ✅ **2025 Shared Service Selection Successfully Submitted!**
            
            **Reference ID:** {reference_id}
            
            **Submission Summary:**
            - Company: {st.session_state.company_info.get('company', 'N/A')}
            - Department: {st.session_state.company_info.get('department', 'N/A')}
            - Contact: {st.session_state.company_info.get('contact_person', 'N/A')}
            - Email: {st.session_state.company_info.get('email', 'N/A')}
            - Total Budget: SAR {total_budget:,.0f}
            - Operational Services: SAR {operational_total:,.0f}
            - Support Package: SAR {support_total:,.0f}
            - Implementation Projects: SAR {implementation_total:,.0f}
            
            **Next Steps:**
            1. Shared Services team review (3-5 business days)
            2. Finance approval process
            3. Q4 2024: Service implementation planning begins
            4. Q1 2025: Service delivery starts
            
            A detailed service catalogue report has been sent to your email and the shared services team.
            """)

# Main application
def main():
    show_header()
    show_sidebar()
    
    # Navigation
    tab1, tab2, tab3, tab4 = st.tabs(["🔧 Operational Services", "🛠️ Support Packages", "🚀 Implementation Projects", "📊 Summary"])
    
    with tab1:
        show_operational_services()
    
    with tab2:
        show_support_packages()
    
    with tab3:
        show_implementation_projects()
    
    with tab4:
        show_summary()

if __name__ == "__main__":
    main()
