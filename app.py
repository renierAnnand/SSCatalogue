import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import re

# Page configuration
st.set_page_config(
    page_title="Shared Services Digital Catalogue",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for enhanced styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        color: white;
        margin: -1rem -1rem 2rem -1rem;
        border-radius: 0 0 20px 20px;
    }
    
    .dept-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border: 2px solid #f0f0f0;
        text-align: center;
        height: 320px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        cursor: pointer;
        position: relative;
        margin: 1rem 0;
    }
    
    .dept-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
        border-color: #1f77b4;
    }
    
    .dept-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 80px;
    }
    
    .dept-icon svg {
        width: 60px;
        height: 60px;
    }
    
    .dept-title {
        font-size: 1.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    
    .dept-description {
        color: #666;
        font-size: 0.9rem;
        line-height: 1.4;
        margin-bottom: 1rem;
    }
    
    .dept-metrics {
        font-size: 0.8rem;
        color: #888;
        margin-top: 1rem;
    }
    
    .soon-badge {
        position: absolute;
        top: 15px;
        right: 15px;
        background: #ff4444;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 15px;
        font-size: 0.75rem;
        font-weight: bold;
        transform: rotate(15deg);
    }
    
    .service-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        margin: 15px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transition: transform 0.2s ease;
    }
    
    .service-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    .sla-badge {
        background: #28a745;
        color: white;
        padding: 0.25rem 0.5rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: bold;
    }
    
    .priority-critical { background: #dc3545; }
    .priority-high { background: #fd7e14; }
    .priority-medium { background: #ffc107; color: #000; }
    .priority-low { background: #28a745; }
    
    .metric-row {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .coming-soon {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin: 20px 0;
    }
    
    .search-container {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .category-header {
        background: linear-gradient(90deg, #e3f2fd, #f3e5f5);
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0 0.5rem 0;
        border-left: 4px solid #1976d2;
    }
    
    .request-button {
        background: #1f77b4;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        cursor: pointer;
        transition: background 0.3s ease;
    }
    
    .request-button:hover {
        background: #1565c0;
    }
    
    .feedback-section {
        background: #e8f5e8;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'selected_department' not in st.session_state:
    st.session_state.selected_department = None
if 'service_requests' not in st.session_state:
    st.session_state.service_requests = []
if 'feedback_data' not in st.session_state:
    st.session_state.feedback_data = []

# Enhanced service data with governance and actionable information
@st.cache_data
def load_enhanced_service_data():
    """Load comprehensive service data with all required fields"""
    
    # Enhanced IT Services with complete information
    it_services = [
        {
            "service_name": "Oracle HCM Absence Management Setup",
            "category": "Human Capital Management",
            "description": "Configure and manage employee leave tracking, approval workflows, and absence reporting in Oracle HCM. Get automated leave calculations and compliance reporting.",
            "business_value": "Reduces manual leave processing by 80% and ensures compliance with labor regulations.",
            "how_to_request": "Submit a ticket through IT Service Portal with required absence types and approval hierarchy details.",
            "target_users": "HR Team, People Managers, All Employees",
            "service_owner": "Oracle HCM Team",
            "sla_hours": 72,
            "sla_description": "3 business days for standard configuration",
            "cost_model": "Fixed scope rate",
            "prerequisites": "Valid Oracle HCM license, approved business requirements",
            "available_hours": "Monday-Friday 8:00-17:00",
            "priority": "Medium",
            "request_volume_monthly": 8,
            "satisfaction_score": 4.2
        },
        {
            "service_name": "Oracle Payroll Implementation",
            "category": "Payroll & Benefits",
            "description": "Implement complete payroll processing solution with automated salary calculations, tax compliance, and integrated reporting for your organization.",
            "business_value": "Ensures 100% accurate payroll processing and reduces payroll cycle time by 50%.",
            "how_to_request": "Contact Payroll Implementation Team via email with company structure and payroll requirements document.",
            "target_users": "Payroll Team, Finance Department, HR Leadership",
            "service_owner": "Payroll Systems Team",
            "sla_hours": 336,
            "sla_description": "14 business days for standard implementation",
            "cost_model": "Project-based pricing",
            "prerequisites": "Organizational chart, salary structures, tax registration documents",
            "available_hours": "Monday-Friday 8:00-17:00",
            "priority": "High",
            "request_volume_monthly": 3,
            "satisfaction_score": 4.5
        },
        {
            "service_name": "Learning Management System Access",
            "category": "Learning & Development",
            "description": "Get access to Oracle Learning platform for employee training, certification tracking, and skills development programs with personalized learning paths.",
            "business_value": "Improves employee skills development efficiency by 60% and tracks compliance training automatically.",
            "how_to_request": "Request through Manager approval in Employee Self-Service portal or submit form to L&D team.",
            "target_users": "All Employees, Learning & Development Team, Managers",
            "service_owner": "Learning & Development",
            "sla_hours": 24,
            "sla_description": "24 hours for access provisioning",
            "cost_model": "Included in employee benefits",
            "prerequisites": "Manager approval, completed orientation program",
            "available_hours": "24/7 self-service, support Monday-Friday 8:00-17:00",
            "priority": "Medium",
            "request_volume_monthly": 45,
            "satisfaction_score": 4.1
        },
        {
            "service_name": "IT Help Desk - Hardware Support",
            "category": "Technical Support",
            "description": "Get immediate support for computer hardware issues, equipment replacement, and peripheral setup. Includes diagnosis, repair, and replacement services.",
            "business_value": "Minimizes business disruption with 95% first-call resolution rate for hardware issues.",
            "how_to_request": "Call IT Help Desk at ext. 2000, submit online ticket, or use chat support in company portal.",
            "target_users": "All Employees",
            "service_owner": "IT Support Team",
            "sla_hours": 4,
            "sla_description": "4 hours for critical hardware issues, 24 hours for standard requests",
            "cost_model": "Included in IT support package",
            "prerequisites": "Valid employee ID, asset tag information",
            "available_hours": "24/7 for critical issues, regular support Monday-Friday 7:00-19:00",
            "priority": "High",
            "request_volume_monthly": 120,
            "satisfaction_score": 4.3
        },
        {
            "service_name": "Network Access & VPN Setup",
            "category": "Network & Security",
            "description": "Configure secure network access and VPN connectivity for remote work. Includes security protocols setup and multi-factor authentication.",
            "business_value": "Enables secure remote work capabilities while maintaining 99.9% network security standards.",
            "how_to_request": "Submit security access form through IT portal with manager approval and business justification.",
            "target_users": "Remote Employees, Contractors, Traveling Staff",
            "service_owner": "Network Security Team",
            "sla_hours": 8,
            "sla_description": "8 hours for standard VPN setup, 2 hours for emergency access",
            "cost_model": "Included in security package",
            "prerequisites": "Security clearance, completed security training, approved device",
            "available_hours": "Monday-Friday 8:00-17:00, emergency support 24/7",
            "priority": "Medium",
            "request_volume_monthly": 35,
            "satisfaction_score": 4.0
        }
    ]
    
    # Enhanced Procurement Services
    procurement_services = [
        {
            "service_name": "Supplier Registration & Onboarding",
            "category": "Vendor Management",
            "description": "Complete supplier registration process including documentation verification, compliance checking, and system setup for new vendors.",
            "business_value": "Ensures 100% compliant supplier base and reduces onboarding time by 40%.",
            "how_to_request": "Submit supplier details through Procurement Portal or email procurement team with vendor information package.",
            "target_users": "Procurement Team, Department Heads, Project Managers",
            "service_owner": "Vendor Management Team",
            "sla_hours": 72,
            "sla_description": "3 business days for standard registration",
            "cost_model": "No charge to internal requesters",
            "prerequisites": "Vendor tax documents, bank details, insurance certificates, business license",
            "available_hours": "Monday-Friday 8:00-17:00",
            "priority": "Medium",
            "request_volume_monthly": 25,
            "satisfaction_score": 4.2
        },
        {
            "service_name": "Purchase Request Processing",
            "category": "Purchasing",
            "description": "End-to-end purchase request handling from requisition to purchase order, including approval workflows and supplier coordination.",
            "business_value": "Reduces procurement cycle time by 50% and ensures 100% compliance with purchasing policies.",
            "how_to_request": "Submit purchase requisition through ERP system with detailed specifications and budget approval.",
            "target_users": "All Departments, Project Managers, Budget Holders",
            "service_owner": "Purchasing Team",
            "sla_hours": 48,
            "sla_description": "2 business days for standard requests under $10K",
            "cost_model": "Included in departmental overhead",
            "prerequisites": "Approved budget, detailed specifications, three quotes for purchases over $5K",
            "available_hours": "Monday-Friday 8:00-17:00",
            "priority": "High",
            "request_volume_monthly": 85,
            "satisfaction_score": 4.1
        },
        {
            "service_name": "Procurement Training & Support",
            "category": "Training & Development",
            "description": "Comprehensive training on procurement policies, system usage, and best practices for department procurement coordinators.",
            "business_value": "Improves procurement compliance by 85% and reduces processing errors by 70%.",
            "how_to_request": "Register for training sessions through Learning Portal or request customized training via procurement team.",
            "target_users": "Department Coordinators, New Employees, Project Managers",
            "service_owner": "Procurement Training Team",
            "sla_hours": 168,
            "sla_description": "7 days to schedule training session",
            "cost_model": "Included in training budget",
            "prerequisites": "Basic computer skills, employee access to ERP system",
            "available_hours": "Monday-Friday 9:00-16:00",
            "priority": "Medium",
            "request_volume_monthly": 15,
            "satisfaction_score": 4.4
        },
        {
            "service_name": "Strategic Sourcing Support",
            "category": "Strategic Planning",
            "description": "Professional sourcing support for complex procurements including market analysis, RFP development, and vendor evaluation.",
            "business_value": "Achieves average 15% cost savings and ensures optimal vendor selection for strategic purchases.",
            "how_to_request": "Submit strategic sourcing request through procurement with project details and business case.",
            "target_users": "Senior Management, Department Heads, Project Leaders",
            "service_owner": "Strategic Sourcing Team",
            "sla_hours": 120,
            "sla_description": "5 business days for project initiation",
            "cost_model": "Shared savings model",
            "prerequisites": "Approved project budget over $50K, defined requirements, stakeholder alignment",
            "available_hours": "Monday-Friday 8:00-17:00",
            "priority": "High",
            "request_volume_monthly": 8,
            "satisfaction_score": 4.6
        }
    ]
    
    # Enhanced Facility Services
    facility_services = [
        {
            "service_name": "Workspace Setup & Allocation",
            "category": "Space Management",
            "description": "Professional workspace setup including desk assignment, equipment installation, and ergonomic assessment for new employees or relocations.",
            "business_value": "Ensures 100% ready workspaces for new hires and improves employee satisfaction by 30%.",
            "how_to_request": "Submit workspace request through HR onboarding system or Facilities portal with move-in date and requirements.",
            "target_users": "HR Team, New Employees, Department Managers",
            "service_owner": "Space Planning Team",
            "sla_hours": 48,
            "sla_description": "2 business days for standard setup",
            "cost_model": "Included in facilities overhead",
            "prerequisites": "Approved headcount, security clearance, equipment specifications",
            "available_hours": "Monday-Friday 8:00-17:00",
            "priority": "High",
            "request_volume_monthly": 20,
            "satisfaction_score": 4.3
        },
        {
            "service_name": "Preventive Maintenance Services",
            "category": "Asset Maintenance",
            "description": "Scheduled maintenance for building systems, furniture, and equipment to prevent breakdowns and extend asset life.",
            "business_value": "Reduces emergency repairs by 60% and extends equipment life by 25%.",
            "how_to_request": "Maintenance requests are automatically scheduled. Report issues through Facilities portal for additional service.",
            "target_users": "All Building Occupants",
            "service_owner": "Maintenance Team",
            "sla_hours": 168,
            "sla_description": "Scheduled based on maintenance calendar",
            "cost_model": "Included in facilities budget",
            "prerequisites": "None for scheduled maintenance",
            "available_hours": "Monday-Friday 7:00-18:00",
            "priority": "Medium",
            "request_volume_monthly": 50,
            "satisfaction_score": 4.0
        },
        {
            "service_name": "Security & Access Control",
            "category": "Safety & Security",
            "description": "Comprehensive building security including access card management, visitor registration, and 24/7 monitoring services.",
            "business_value": "Maintains 100% security compliance and reduces security incidents by 90%.",
            "how_to_request": "Submit access requests through Security portal with manager approval. Report security issues immediately by calling 3911.",
            "target_users": "All Employees, Visitors, Contractors",
            "service_owner": "Security Team",
            "sla_hours": 2,
            "sla_description": "2 hours for access provisioning, immediate for security incidents",
            "cost_model": "Included in security budget",
            "prerequisites": "Security clearance, photo ID, manager approval",
            "available_hours": "24/7 monitoring, access requests Monday-Friday 8:00-17:00",
            "priority": "Critical",
            "request_volume_monthly": 40,
            "satisfaction_score": 4.5
        },
        {
            "service_name": "Environmental Services",
            "category": "Cleaning & Maintenance",
            "description": "Professional cleaning, sanitization, and waste management services to maintain healthy and productive work environment.",
            "business_value": "Maintains 98% cleanliness standards and reduces sick leave by 20%.",
            "how_to_request": "Standard cleaning is automatically scheduled. Request additional services through Facilities portal.",
            "target_users": "All Building Occupants",
            "service_owner": "Environmental Services Team",
            "sla_hours": 24,
            "sla_description": "24 hours for additional cleaning requests",
            "cost_model": "Included in facilities budget",
            "prerequisites": "None for standard services",
            "available_hours": "Cleaning: Monday-Friday 6:00-8:00 & 17:00-20:00",
            "priority": "Medium",
            "request_volume_monthly": 30,
            "satisfaction_score": 4.1
        }
    ]
    
    return {
        'it_services': pd.DataFrame(it_services),
        'procurement_services': pd.DataFrame(procurement_services),
        'facility_services': pd.DataFrame(facility_services)
    }

# Enhanced departments configuration
departments = {
    "Information Technology": {
        "description": "Delivering technical support, enterprise applications support, digital and AI solutions, network services, administration services with IT operations to enable innovation, operational excellence, and enterprise security solutions across the organization.",
        "icon": """<svg width="60" height="60" viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
  <rect x="15" y="20" width="50" height="35" rx="3" fill="#2E5BBA" stroke="#1E4A99" stroke-width="2"/>
  <rect x="18" y="23" width="44" height="26" fill="#87CEEB"/>
  <rect x="22" y="27" width="15" height="2" fill="#1E4A99"/>
  <rect x="22" y="31" width="20" height="2" fill="#1E4A99"/>
  <rect x="22" y="35" width="12" height="2" fill="#1E4A99"/>
  <rect x="22" y="39" width="18" height="2" fill="#1E4A99"/>
  <rect x="22" y="43" width="10" height="2" fill="#1E4A99"/>
  <rect x="37" y="55" width="6" height="8" fill="#666"/>
  <ellipse cx="40" cy="67" rx="12" ry="3" fill="#666"/>
  <path d="M50 35 L62 35 L62 45 L52 50 L50 45 Z" fill="#4A90E2" opacity="0.7"/>
  <rect x="55" y="25" width="8" height="15" rx="2" fill="#34C759"/>
  <rect x="57" y="27" width="4" height="8" fill="#FFF"/>
  <ellipse cx="25" cy="15" rx="6" ry="3" fill="#E6F3FF"/>
  <ellipse cx="20" cy="15" rx="4" ry="2.5" fill="#E6F3FF"/>
  <ellipse cx="30" cy="15" rx="4" ry="2.5" fill="#E6F3FF"/>
</svg>""",
        "color": "#1f77b4",
        "services_count": 276,
        "avg_resolution_time": "24-72 hours",
        "contact": "it-support@company.com",
        "satisfaction_score": 4.2,
        "availability": "99.5%"
    },
    "Finance": {
        "description": "Finance Department plays a critical role in supporting an organization's financial health, decision-making, and compliance. It provides a wide range of services that ensure efficient management of money, resources, and reporting.",
        "icon": "💰",
        "color": "#ff7f0e",
        "services_count": "TBD",
        "avg_resolution_time": "TBD", 
        "contact": "finance@company.com",
        "soon": True
    },
    "HR": {
        "description": "Report all your HR issues, inquiries, or complaints, from payroll and attendance to system access and more, and track their resolution with full transparency, instant updates, and streamlined communication through one platform.",
        "icon": "🧑‍💼",
        "color": "#2ca02c",
        "services_count": "TBD",
        "avg_resolution_time": "TBD",
        "contact": "hr@company.com",
        "soon": True
    },
    "Procurement": {
        "description": "The Procurement Department focuses on ensuring the availability of materials and services by coordinating with suppliers, updating their information, creating items, and maintaining efficiency, quality, and competitive pricing across all processes.",
        "icon": """<svg width="60" height="60" viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
  <rect x="20" y="30" width="40" height="30" fill="#CD853F" stroke="#8B4513" stroke-width="2"/>
  <path d="M20 30 L30 20 L50 20 L60 30" fill="#DEB887" stroke="#8B4513" stroke-width="1"/>
  <path d="M60 30 L60 60 L70 50 L70 20 L60 30" fill="#A0522D"/>
  <rect x="25" y="35" width="20" height="12" fill="#FFF" stroke="#333" stroke-width="1"/>
  <line x1="27" y1="38" x2="27" y2="42" stroke="#000" stroke-width="0.5"/>
  <line x1="29" y1="38" x2="29" y2="42" stroke="#000" stroke-width="1"/>
  <line x1="31" y1="38" x2="31" y2="42" stroke="#000" stroke-width="0.5"/>
  <line x1="33" y1="38" x2="33" y2="42" stroke="#000" stroke-width="1"/>
  <line x1="35" y1="38" x2="35" y2="42" stroke="#000" stroke-width="0.5"/>
  <line x1="37" y1="38" x2="37" y2="42" stroke="#000" stroke-width="1"/>
  <line x1="39" y1="38" x2="39" y2="42" stroke="#000" stroke-width="0.5"/>
  <line x1="41" y1="38" x2="41" y2="42" stroke="#000" stroke-width="1"/>
  <line x1="43" y1="38" x2="43" y2="42" stroke="#000" stroke-width="0.5"/>
  <rect x="10" y="55" width="25" height="12" fill="#FF6B35" rx="2"/>
  <rect x="10" y="50" width="8" height="5" fill="#FF6B35"/>
  <circle cx="15" cy="70" r="3" fill="#333"/>
  <circle cx="28" cy="70" r="3" fill="#333"/>
  <rect x="50" y="10" width="20" height="15" fill="#4A90E2"/>
  <rect x="52" y="12" width="3" height="6" fill="#87CEEB"/>
  <rect x="57" y="12" width="3" height="6" fill="#87CEEB"/>
  <rect x="62" y="12" width="3" height="6" fill="#87CEEB"/>
  <rect x="67" y="12" width="3" height="6" fill="#87CEEB"/>
  <path d="M48 10 L60 5 L72 10" fill="#2E5BBA"/>
</svg>""", 
        "color": "#d62728",
        "services_count": 51,
        "avg_resolution_time": "24-72 hours",
        "contact": "procurement@company.com",
        "satisfaction_score": 4.3,
        "availability": "99.2%"
    },
    "Facility": {
        "description": "The Facilities and Safety Department delivers multiple services in maintenance, safety and security, facility operations, asset inventory. Organizing the workspace to ensure a safe, efficient, and well-organized work environment.",
        "icon": """<svg width="60" height="60" viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
  <rect x="25" y="25" width="30" height="40" fill="#4A90E2" stroke="#2E5BBA" stroke-width="2"/>
  <path d="M20 25 L40 15 L60 25" fill="#2E5BBA"/>
  <rect x="30" y="30" width="6" height="6" fill="#87CEEB"/>
  <rect x="44" y="30" width="6" height="6" fill="#87CEEB"/>
  <rect x="30" y="40" width="6" height="6" fill="#87CEEB"/>
  <rect x="44" y="40" width="6" height="6" fill="#87CEEB"/>
  <rect x="30" y="50" width="6" height="6" fill="#87CEEB"/>
  <rect x="44" y="50" width="6" height="6" fill="#87CEEB"/>
  <rect x="37" y="55" width="6" height="10" fill="#8B4513" rx="1"/>
  <circle cx="41" cy="59" r="0.5" fill="#FFD700"/>
  <rect x="10" y="35" width="15" height="30" fill="#6BB6FF"/>
  <rect x="12" y="40" width="4" height="4" fill="#87CEEB"/>
  <rect x="18" y="40" width="4" height="4" fill="#87CEEB"/>
  <rect x="12" y="50" width="4" height="4" fill="#87CEEB"/>
  <rect x="18" y="50" width="4" height="4" fill="#87CEEB"/>
  <rect x="55" y="35" width="15" height="30" fill="#6BB6FF"/>
  <rect x="57" y="40" width="4" height="4" fill="#87CEEB"/>
  <rect x="63" y="40" width="4" height="4" fill="#87CEEB"/>
  <rect x="57" y="50" width="4" height="4" fill="#87CEEB"/>
  <rect x="63" y="50" width="4" height="4" fill="#87CEEB"/>
  <rect x="52" y="28" width="4" height="3" fill="#333" rx="1"/>
  <circle cx="54" cy="29.5" r="1" fill="#FF0000"/>
  <path d="M15 20 L18 17 L20 19 L17 22 Z" fill="#FFD700"/>
  <circle cx="16" cy="21" r="1" fill="#FFA500"/>
  <line x1="65" y1="20" x2="68" y2="17" stroke="#FF6B35" stroke-width="2"/>
  <rect x="63" y="21" width="4" height="1" fill="#8B4513"/>
  <rect x="0" y="65" width="80" height="15" fill="#90EE90" opacity="0.3"/>
  <rect x="5" y="62" width="8" height="3" fill="#666"/>
  <rect x="67" y="62" width="8" height="3" fill="#666"/>
</svg>""",
        "color": "#9467bd",
        "services_count": 45,
        "avg_resolution_time": "2-48 hours",
        "contact": "facilities@company.com",
        "satisfaction_score": 4.1,
        "availability": "99.8%"
    },
    "Legal": {
        "description": "Legal advisory, contract management, compliance, and risk management services to support business operations and ensure regulatory compliance.",
        "icon": "⚖️",
        "color": "#8c564b",
        "services_count": "TBD", 
        "avg_resolution_time": "TBD",
        "contact": "legal@company.com",
        "soon": True
    }
}

# Load enhanced service data
service_data = load_enhanced_service_data()

def show_main_page():
    """Enhanced main landing page with KPIs and improved design"""
    
    # Main header with KPIs
    st.markdown("""
    <div class='main-header'>
        <h1>🏢 Shared Services Digital Catalogue</h1>
        <p>Your gateway to efficient, professional shared services</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick metrics
    col1, col2, col3, col4 = st.columns(4)
    total_services = sum([int(dept["services_count"]) for dept in departments.values() if isinstance(dept["services_count"], int)])
    active_depts = len([d for d in departments.values() if not d.get("soon", False)])
    
    with col1:
        st.metric("Total Services", total_services, "🚀")
    with col2:
        st.metric("Active Departments", f"{active_depts}/6", "📈")
    with col3:
        st.metric("Avg Satisfaction", "4.2/5.0", "⭐")
    with col4:
        st.metric("Service Availability", "99.5%", "✅")
    
    st.markdown("---")
    
    # Department cards grid
    col1, col2, col3 = st.columns(3)
    
    departments_list = list(departments.items())
    
    for i, (dept_name, dept_info) in enumerate(departments_list):
        col = [col1, col2, col3][i % 3]
        
        with col:
            # Create enhanced clickable card
            soon_badge = '<div class="soon-badge">Soon</div>' if dept_info.get("soon", False) else ''
            
            # Handle both SVG and emoji icons
            if dept_info['icon'].startswith('<svg'):
                icon_display = dept_info['icon']
            else:
                icon_display = f"<div style='font-size: 4rem;'>{dept_info['icon']}</div>"
            
            # Add metrics for active departments
            metrics_html = ""
            if not dept_info.get("soon", False):
                satisfaction = dept_info.get("satisfaction_score", "N/A")
                availability = dept_info.get("availability", "N/A")
                metrics_html = f"""
                <div class="dept-metrics">
                    📊 {dept_info['services_count']} services<br>
                    ⭐ {satisfaction}/5.0 satisfaction<br>
                    ✅ {availability} availability
                </div>
                """
            
            card_html = f"""
            <div class="dept-card">
                {soon_badge}
                <div class="dept-icon">{icon_display}</div>
                <div class="dept-title">{dept_name}</div>
                <div class="dept-description">{dept_info['description'][:120]}...</div>
                {metrics_html}
            </div>
            """
            
            st.markdown(card_html, unsafe_allow_html=True)
            
            # Button to select department
            if st.button(f"Enter {dept_name}", key=f"btn_{dept_name}", use_container_width=True):
                st.session_state.selected_department = dept_name
                st.rerun()

def show_enhanced_service_catalogue(department_name, df):
    """Enhanced service catalogue with better categorization and search"""
    
    st.subheader("🔍 Service Catalogue")
    
    # Enhanced search and filter section
    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        search_term = st.text_input("🔍 Search services...", placeholder="Enter keywords", key="service_search")
    
    with col2:
        categories = ['All Categories'] + list(df['category'].unique())
        selected_category = st.selectbox("📂 Filter by Category", categories)
    
    with col3:
        priorities = ['All Priorities'] + list(df['priority'].unique())
        selected_priority = st.selectbox("⚡ Filter by Priority", priorities)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Apply filters
    filtered_df = df.copy()
    
    if search_term:
        mask = (
            filtered_df['service_name'].str.contains(search_term, case=False, na=False) |
            filtered_df['description'].str.contains(search_term, case=False, na=False) |
            filtered_df['target_users'].str.contains(search_term, case=False, na=False)
        )
        filtered_df = filtered_df[mask]
    
    if selected_category != 'All Categories':
        filtered_df = filtered_df[filtered_df['category'] == selected_category]
    
    if selected_priority != 'All Priorities':
        filtered_df = filtered_df[filtered_df['priority'] == selected_priority]
    
    # Group services by category
    if not filtered_df.empty:
        categories = filtered_df['category'].unique()
        
        for category in categories:
            category_services = filtered_df[filtered_df['category'] == category]
            
            # Category header
            st.markdown(f"""
            <div class="category-header">
                <h3>📂 {category} ({len(category_services)} services)</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Services in this category
            for idx, service in category_services.iterrows():
                show_enhanced_service_card(service, idx)
    else:
        st.warning("No services found matching your search criteria.")

def show_enhanced_service_card(service, idx):
    """Enhanced service card with all governance information"""
    
    # Priority badge
    priority_class = f"priority-{service['priority'].lower()}"
    sla_badge = f'<span class="sla-badge {priority_class}">{service["sla_description"]}</span>'
    
    with st.expander(f"🔧 {service['service_name']} {sla_badge}", expanded=False):
        
        # Main service information
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"**📋 Description:**")
            st.write(service['description'])
            
            st.markdown(f"**💼 Business Value:**")
            st.write(service['business_value'])
            
            st.markdown(f"**📝 How to Request:**")
            st.info(service['how_to_request'])
        
        with col2:
            st.markdown("**📊 Service Details**")
            st.write(f"**Owner:** {service['service_owner']}")
            st.write(f"**Target Users:** {service['target_users']}")
            st.write(f"**Priority:** {service['priority']}")
            st.write(f"**Available:** {service['available_hours']}")
            
            # Metrics
            st.markdown("**📈 Performance**")
            col_met1, col_met2 = st.columns(2)
            with col_met1:
                st.metric("Monthly Requests", service['request_volume_monthly'])
            with col_met2:
                st.metric("Satisfaction", f"{service['satisfaction_score']}/5.0")
        
        # Prerequisites and additional info
        if service['prerequisites'] and service['prerequisites'] != "None":
            st.markdown(f"**⚠️ Prerequisites:** {service['prerequisites']}")
        
        if service['cost_model']:
            st.markdown(f"**💰 Cost Model:** {service['cost_model']}")
        
        # Action buttons
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            if st.button(f"🎫 Request {service['service_name']}", key=f"req_{idx}", use_container_width=True):
                st.session_state.selected_service = service['service_name']
                st.success(f"✅ Service request initiated for: {service['service_name']}")
        
        with col2:
            if st.button("📞 Contact Owner", key=f"contact_{idx}"):
                st.info(f"Contact: {service['service_owner']}")
        
        with col3:
            if st.button("⭐ Rate Service", key=f"rate_{idx}"):
                st.session_state.rating_service = service['service_name']

def show_enhanced_analytics(department_name, df):
    """Enhanced analytics with governance KPIs"""
    
    st.subheader("📈 Service Analytics & KPIs")
    
    # Key Performance Indicators
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_satisfaction = df['satisfaction_score'].mean()
        st.metric("Avg Satisfaction Score", f"{avg_satisfaction:.1f}/5.0", 
                 delta=f"+{(avg_satisfaction-4.0)*100:.0f}% vs target")
    
    with col2:
        total_monthly_volume = df['request_volume_monthly'].sum()
        st.metric("Monthly Service Volume", total_monthly_volume, 
                 delta="+12% vs last month")
    
    with col3:
        high_priority_services = len(df[df['priority'].isin(['High', 'Critical'])])
        st.metric("High Priority Services", high_priority_services,
                 delta=f"{(high_priority_services/len(df)*100):.0f}% of total")
    
    with col4:
        avg_sla = df['sla_hours'].mean()
        st.metric("Avg SLA (hours)", f"{avg_sla:.0f}h",
                 delta="Within target")
    
    # Visualizations
    tab1, tab2, tab3 = st.tabs(["📊 Service Volume", "⭐ Satisfaction Trends", "⏱️ SLA Performance"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            # Service requests by category
            category_volume = df.groupby('category')['request_volume_monthly'].sum().reset_index()
            fig1 = px.bar(category_volume, x='category', y='request_volume_monthly',
                         title="Monthly Requests by Category",
                         color='request_volume_monthly',
                         color_continuous_scale='Blues')
            fig1.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # Service priority distribution
            priority_dist = df['priority'].value_counts().reset_index()
            fig2 = px.pie(priority_dist, values='count', names='priority',
                         title="Service Distribution by Priority",
                         color_discrete_map={
                             'Critical': '#dc3545',
                             'High': '#fd7e14', 
                             'Medium': '#ffc107',
                             'Low': '#28a745'
                         })
            st.plotly_chart(fig2, use_container_width=True)
    
    with tab2:
        # Satisfaction by service
        satisfaction_data = df[['service_name', 'satisfaction_score', 'category']].copy()
        satisfaction_data['service_short'] = satisfaction_data['service_name'].str[:20] + '...'
        
        fig3 = px.bar(satisfaction_data, x='service_short', y='satisfaction_score',
                     color='category', title="Service Satisfaction Scores",
                     hover_data=['service_name'])
        fig3.add_hline(y=4.0, line_dash="dash", line_color="red", 
                      annotation_text="Target: 4.0")
        fig3.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig3, use_container_width=True)
    
    with tab3:
        # SLA vs Volume analysis
        fig4 = px.scatter(df, x='sla_hours', y='request_volume_monthly',
                         size='satisfaction_score', color='priority',
                         hover_data=['service_name'],
                         title="SLA vs Request Volume Analysis")
        fig4.update_layout(xaxis_title="SLA (hours)", yaxis_title="Monthly Requests")
        st.plotly_chart(fig4, use_container_width=True)

def show_enhanced_request_form(department_name):
    """Enhanced service request form with workflow"""
    
    st.subheader("📝 Service Request Submission")
    
    # Service selection
    dept_key = department_name.lower().replace(" ", "_")
    if f'{dept_key}_services' in service_data:
        available_services = service_data[f'{dept_key}_services']['service_name'].tolist()
    else:
        available_services = []
    
    with st.form("enhanced_service_request_form"):
        # Service selection
        service_requested = st.selectbox("🔧 Select Service*", 
            ["Select a service..."] + available_services)
        
        if service_requested != "Select a service...":
            # Get service details
            service_info = service_data[f'{dept_key}_services'][
                service_data[f'{dept_key}_services']['service_name'] == service_requested
            ].iloc[0]
            
            # Show service info
            st.info(f"**SLA:** {service_info['sla_description']} | **Owner:** {service_info['service_owner']}")
            
            if service_info['prerequisites'] != "None":
                st.warning(f"**Prerequisites:** {service_info['prerequisites']}")
        
        # Requestor information
        st.markdown("### 👤 Requestor Information")
        col1, col2 = st.columns(2)
        
        with col1:
            requester_name = st.text_input("Your Name*")
            requester_email = st.text_input("Email Address*")
            employee_id = st.text_input("Employee ID*")
            department = st.selectbox("Your Department*", 
                ["Select...", "Engineering", "Finance", "HR", "Marketing", "Operations", "Other"])
        
        with col2:
            manager_name = st.text_input("Direct Manager")
            cost_center = st.text_input("Cost Center")
            phone = st.text_input("Phone Number")
            location = st.text_input("Office Location")
        
        # Request details
        st.markdown("### 📋 Request Details")
        col1, col2 = st.columns(2)
        
        with col1:
            urgency = st.selectbox("Urgency Level*", ["Low", "Medium", "High", "Critical"])
            preferred_date = st.date_input("Preferred Completion Date")
        
        with col2:
            business_justification = st.selectbox("Business Justification*", 
                ["Operational Requirement", "New Employee", "System Upgrade", 
                 "Compliance", "Cost Optimization", "Other"])
            
            if business_justification == "Other":
                other_justification = st.text_input("Please specify:")
        
        description = st.text_area("Detailed Description*", 
            placeholder="Please provide comprehensive details about your request, including specific requirements, timelines, and any relevant context...")
        
        # File attachments
        attachments = st.file_uploader("📎 Attach Supporting Documents", 
            accept_multiple_files=True, 
            type=['pdf', 'doc', 'docx', 'xls', 'xlsx', 'png', 'jpg', 'zip'],
            help="Upload any relevant documents, specifications, or approvals")
        
        # Approval workflow
        if urgency in ["High", "Critical"]:
            st.warning("⚠️ High/Critical priority requests require manager approval.")
            manager_approval = st.checkbox("I have manager approval for this urgent request")
        else:
            manager_approval = True
        
        # Submit button
        submitted = st.form_submit_button("🚀 Submit Request", 
                                        type="primary", 
                                        use_container_width=True)
        
        if submitted:
            # Validation
            required_fields = [requester_name, requester_email, employee_id, 
                             department != "Select...", description, 
                             service_requested != "Select a service..."]
            
            if all(required_fields) and manager_approval:
                # Generate request ID
                request_id = f"SR-{datetime.now().strftime('%Y%m%d%H%M%S')}"
                
                # Store request
                request_data = {
                    'request_id': request_id,
                    'service': service_requested,
                    'requester': requester_name,
                    'email': requester_email,
                    'department': department,
                    'urgency': urgency,
                    'status': 'Submitted',
                    'submit_date': datetime.now(),
                    'description': description
                }
                st.session_state.service_requests.append(request_data)
                
                # Success message with workflow info
                if urgency == "Critical":
                    next_step = "Request escalated to management - expect contact within 2 hours"
                elif urgency == "High":
                    next_step = "Request prioritized - initial response within 4 hours"
                else:
                    next_step = f"Request queued - response within {service_info.get('sla_description', '2 business days')}"
                
                st.success(f"""
                ✅ **Service Request Submitted Successfully!**
                
                **Request ID:** {request_id}
                **Service:** {service_requested}
                **Next Step:** {next_step}
                **Service Owner:** {service_info.get('service_owner', 'N/A')}
                
                📧 Confirmation email sent to {requester_email}
                📱 SMS notification sent (if enabled)
                """)
                
                # Show tracking info
                st.info(f"🔍 Track your request status at: portal.company.com/requests/{request_id}")
                
            else:
                missing_fields = []
                if not requester_name: missing_fields.append("Name")
                if not requester_email: missing_fields.append("Email")
                if not employee_id: missing_fields.append("Employee ID")
                if department == "Select...": missing_fields.append("Department")
                if not description: missing_fields.append("Description")
                if service_requested == "Select a service...": missing_fields.append("Service")
                if not manager_approval: missing_fields.append("Manager Approval")
                
                st.error(f"❌ Please complete the following required fields: {', '.join(missing_fields)}")

def show_department_page(department_name):
    """Enhanced department page with comprehensive information"""
    
    dept_info = departments[department_name]
    
    # Back button
    col1, col2 = st.columns([1, 6])
    with col1:
        if st.button("← Back to Main", key="back_button"):
            st.session_state.selected_department = None
            st.rerun()
    
    # Department header
    col1, col2 = st.columns([1, 4])
    with col1:
        if dept_info['icon'].startswith('<svg'):
            st.markdown(f"<div>{dept_info['icon']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='font-size: 4rem; color: {dept_info['color']};'>{dept_info['icon']}</div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<h1 style='color: {dept_info['color']};'>{department_name} Department</h1>", unsafe_allow_html=True)

    st.markdown(dept_info["description"])

    # Enhanced department metrics
    if not dept_info.get("soon", False):
        st.markdown("<div class='metric-row'>", unsafe_allow_html=True)
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Available Services", dept_info["services_count"])
        with col2:
            st.metric("Avg Response Time", dept_info["avg_resolution_time"])
        with col3:
            st.metric("Satisfaction Score", f"{dept_info.get('satisfaction_score', 'N/A')}/5.0")
        with col4:
            st.metric("Service Availability", dept_info.get('availability', 'N/A'))
        with col5:
            st.metric("Status", "🟢 Active")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")

    # Coming soon departments
    if dept_info.get("soon", False):
        st.markdown(f"""
        <div class='coming-soon'>
            <h2>🚧 Coming Soon</h2>
            <p>This service catalogue is currently being developed and will be available soon.</p>
            <p>Expected launch: <strong>Q3 2025</strong></p>
            <p>For immediate assistance, please contact: <strong>{dept_info["contact"]}</strong></p>
        </div>
        """, unsafe_allow_html=True)
        
    else:
        # Enhanced tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["📋 Service Catalogue", "📈 Analytics & KPIs", "📝 Request Service", "ℹ️ Department Info", "💬 Feedback"])
        
        with tab1:
            dept_key = department_name.lower().replace(" ", "_")
            if f'{dept_key}_services' in service_data:
                df = service_data[f'{dept_key}_services']
                show_enhanced_service_catalogue(department_name, df)
        
        with tab2:
            dept_key = department_name.lower().replace(" ", "_")
            if f'{dept_key}_services' in service_data:
                df = service_data[f'{dept_key}_services']
                show_enhanced_analytics(department_name, df)
        
        with tab3:
            show_enhanced_request_form(department_name)
        
        with tab4:
            show_department_info(dept_info)
        
        with tab5:
            show_feedback_section(department_name)

def show_department_info(dept_info):
    """Enhanced department information with governance details"""
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📞 Contact Information")
        st.write(f"**Email:** {dept_info['contact']}")
        st.write("**Phone:** +966-11-XXX-XXXX")
        st.write("**Location:** Building A, Floor 3")
        st.write("**Manager:** John Smith")
        
        st.markdown("### ⏰ Service Hours")
        st.write("**Monday - Thursday:** 8:00 AM - 5:00 PM")
        st.write("**Sunday:** 8:00 AM - 4:00 PM")
        st.write("**Emergency Support:** 24/7 for critical issues")
        st.write("**Response Time:** Within 2 hours during business hours")
        
        st.markdown("### 📋 Governance & Quality")
        st.write("**ISO Certification:** ISO 20000 (IT Service Management)")
        st.write("**Quality Reviews:** Monthly")
        st.write("**Service Catalog Updates:** Quarterly")
        st.write("**SLA Compliance:** 98.5% average")
    
    with col2:
        st.markdown("### 📊 Service Level Agreements")
        st.write(f"**Standard Response:** {dept_info['avg_resolution_time']}")
        st.write("**Critical Issues:** 1-2 hours")
        st.write("**High Priority:** 4-8 hours") 
        st.write("**Medium Priority:** 1-2 business days")
        st.write("**Low Priority:** 3-5 business days")
        
        st.markdown("### 📈 Performance Metrics")
        st.write(f"**Service Availability:** {dept_info.get('availability', '99.5%')}")
        st.write(f"**Customer Satisfaction:** {dept_info.get('satisfaction_score', 4.2)}/5.0")
        st.write("**First Call Resolution:** 75%")
        st.write("**Service Adoption Rate:** 85%")
        
        st.markdown("### 🏆 Continuous Improvement")
        st.write("**Monthly Service Reviews:** First Monday of each month")
        st.write("**Annual Service Survey:** December")
        st.write("**Process Improvement:** Quarterly initiatives")
        st.write("**Knowledge Base Updates:** Weekly")

def show_feedback_section(department_name):
    """Feedback collection for continuous improvement"""
    
    st.subheader("💬 Your Feedback Matters")
    
    # Recent feedback summary
    if st.session_state.feedback_data:
        recent_feedback = [f for f in st.session_state.feedback_data if f['department'] == department_name]
        if recent_feedback:
            avg_rating = sum(f['rating'] for f in recent_feedback) / len(recent_feedback)
            st.metric("Department Feedback Score", f"{avg_rating:.1f}/5.0", 
                     delta=f"{len(recent_feedback)} responses")
    
    # Feedback form
    with st.form("feedback_form"):
        st.markdown("### Rate Your Experience")
        
        col1, col2 = st.columns(2)
        with col1:
            overall_rating = st.select_slider(
                "Overall Department Rating",
                options=[1, 2, 3, 4, 5],
                value=4,
                format_func=lambda x: "⭐" * x
            )
            
            service_used = st.selectbox(
                "Which service did you use recently?",
                ["General Inquiry"] + list(service_data.get(f'{department_name.lower().replace(" ", "_")}_services', pd.DataFrame()).get('service_name', []))
            )
        
        with col2:
            response_time_rating = st.select_slider(
                "Response Time Rating",
                options=[1, 2, 3, 4, 5],
                value=4,
                format_func=lambda x: "⭐" * x
            )
            
            ease_of_request = st.select_slider(
                "Ease of Requesting Service",
                options=[1, 2, 3, 4, 5],
                value=4,
                format_func=lambda x: "⭐" * x
            )
        
        feedback_comments = st.text_area(
            "Comments & Suggestions",
            placeholder="Tell us about your experience and how we can improve..."
        )
        
        improvement_suggestions = st.text_area(
            "Specific Improvement Ideas",
            placeholder="What specific changes would make our services better?"
        )
        
        submitted_feedback = st.form_submit_button("Submit Feedback", type="primary")
        
        if submitted_feedback:
            feedback_entry = {
                'department': department_name,
                'service': service_used,
                'rating': overall_rating,
                'response_time': response_time_rating,
                'ease_of_request': ease_of_request,
                'comments': feedback_comments,
                'suggestions': improvement_suggestions,
                'timestamp': datetime.now(),
                'feedback_id': f"FB-{datetime.now().strftime('%Y%m%d%H%M%S')}"
            }
            
            st.session_state.feedback_data.append(feedback_entry)
            
            st.success("""
            ✅ **Thank you for your feedback!**
            
            Your input helps us continuously improve our services.
            **Feedback ID:** {feedback_id}
            **Next:** Our team reviews all feedback monthly and implements improvements quarterly.
            """.format(feedback_id=feedback_entry['feedback_id']))

# Main app logic
if st.session_state.selected_department is None:
    show_main_page()
else:
    show_department_page(st.session_state.selected_department)

# Enhanced footer with governance information
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666666; padding: 20px;'>
    <p><strong>Shared Services Digital Catalogue</strong> • Version 2.0 • Last Updated: July 2025</p>
    <p>📊 <strong>Service Governance:</strong> Monthly reviews • Quarterly updates • Annual satisfaction survey</p>
    <p>🔧 <strong>Technical Support:</strong> it-support@company.com • 📱 <strong>Mobile App:</strong> Available on App Store & Google Play</p>
    <p>📋 <strong>Quality Standards:</strong> ISO 20000 Certified • SLA Compliance: 98.5% • Customer Satisfaction: 4.2/5.0</p>
</div>
""", unsafe_allow_html=True)
