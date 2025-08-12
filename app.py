import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import uuid
import hashlib
import json

# Page configuration
st.set_page_config(
    page_title="Alkhorayef Group - 2025 Multi-Department Shared Services Catalogue",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Authentication Configuration
ADMIN_CREDENTIALS = {
    "it_admin": {
        "password": "itadmin2025",
        "department": "IT",
        "name": "IT Department Head"
    },
    "procurement_admin": {
        "password": "procadmin2025", 
        "department": "Procurement",
        "name": "Procurement Department Head"
    },
    "facility_admin": {
        "password": "faciladmin2025",
        "department": "Facility_Safety", 
        "name": "Facility & Safety Department Head"
    },
    "super_admin": {
        "password": "superadmin2025",
        "department": "ALL",
        "name": "Super Administrator"
    }
}

# Company list for Alkhorayef Group
ALKHORAYEF_COMPANIES = [
    "APC", "AIC", "AGC", "APS", "PS", "AWPT", "AMIC", "ACC", "SPC", "Tom Egypt"
]

# Enhanced PROJECT_TYPES organized by categories for IT
DEFAULT_IT_PROJECT_CATEGORIES = {
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

# Procurement Service Categories based on the Excel file
DEFAULT_PROCUREMENT_SERVICE_CATEGORIES = {
    "🛒 Purchase Order Management": [
        "Purchase Request Processing",
        "Purchase Order Creation & Management",
        "Urgent & Emergency Purchases",
        "Purchase History & Analytics",
        "Purchase Request Review & Approval"
    ],
    
    "🤝 Supplier & Vendor Management": [
        "Supplier Registration & Onboarding",
        "Vendor Document Review & Verification",
        "Supplier Data Management & Updates",
        "Vendor Compliance Management",
        "Supplier Performance Evaluation",
        "Vendor Master Data Maintenance"
    ],
    
    "📋 Master Data Management": [
        "Item Creation & Classification",
        "Part Number Management",
        "Product Data Entry & Updates",
        "Master Data Cleansing & Validation",
        "Item Number Verification & Guidance",
        "Technical Specifications Management"
    ],
    
    "📄 Contract Management": [
        "Service Contract Negotiation",
        "Material Contract Management",
        "Contract Documentation & Filing",
        "Contract Renewal Management",
        "Terms & Conditions Management",
        "Contract Compliance Monitoring"
    ],
    
    "🚚 Logistics & Delivery": [
        "Internal Logistics Coordination",
        "External Shipping Management",
        "Pick-up & Delivery Services",
        "Inter-branch Transportation",
        "Warehouse-to-Company Shipping",
        "Supplier-to-Warehouse Logistics"
    ],
    
    "💰 Payment & Financial Processing": [
        "Payment Request Processing",
        "Invoice Verification & Processing",
        "Petty Cash Management",
        "Payment Coordination with Finance",
        "Currency & Exchange Management",
        "Refund & Return Processing"
    ],
    
    "📊 Sourcing & RFQ Management": [
        "Request for Quotation (RFQ)",
        "Request for Proposal (RFP)",
        "Supplier Quote Collection & Analysis",
        "Market Research & Price Negotiation",
        "Competitive Bidding Management",
        "Source-to-Contract Process"
    ],
    
    "🎓 Training & Development": [
        "Procurement Process Training",
        "Employee Skill Development",
        "System Training & Support",
        "Best Practices Training",
        "Compliance Training",
        "New Employee Orientation"
    ],
    
    "🔍 Audit & Compliance": [
        "Procurement Audit & Review",
        "Document Verification & Validation",
        "Compliance Monitoring",
        "Process Review & Improvement",
        "Risk Assessment & Mitigation",
        "Quality Assurance"
    ],
    
    "📞 Support & Communication": [
        "Ticket Resolution & Support",
        "Stakeholder Communication",
        "Customer Support Procurement",
        "Inter-department Coordination",
        "Supplier Communication Management",
        "Issue Resolution & Follow-up"
    ]
}

# Facility & Safety Service Categories
DEFAULT_FACILITY_SAFETY_SERVICE_CATEGORIES = {
    "🏢 Facility Management & Operations": [
        "Building Maintenance & Repairs",
        "HVAC System Management",
        "Electrical System Maintenance",
        "Plumbing & Water System Management",
        "Facility Cleaning & Janitorial Services",
        "Grounds & Landscape Maintenance",
        "Space Planning & Optimization",
        "Move Management & Office Setup"
    ],
    
    "🔒 Security & Access Control": [
        "Physical Security Management",
        "Access Control Systems",
        "CCTV Surveillance Management",
        "Security Guard Services",
        "Visitor Management Systems",
        "Key & Badge Management",
        "Perimeter Security",
        "Emergency Response Coordination"
    ],
    
    "⚠️ Safety & Compliance": [
        "Workplace Safety Management",
        "Safety Training & Certification",
        "Incident Investigation & Reporting",
        "Safety Equipment Management",
        "Compliance Audit & Monitoring",
        "Risk Assessment & Mitigation",
        "Safety Policy Development",
        "Regulatory Compliance Management"
    ],
    
    "🚨 Emergency Management": [
        "Emergency Response Planning",
        "Fire Safety & Evacuation Procedures",
        "Emergency Communication Systems",
        "Business Continuity Planning",
        "Crisis Management",
        "Emergency Equipment Management",
        "Disaster Recovery Coordination",
        "Emergency Training & Drills"
    ],
    
    "🌡️ Environmental & Health": [
        "Environmental Monitoring",
        "Air Quality Management",
        "Waste Management & Recycling",
        "Hazardous Material Handling",
        "Occupational Health Services",
        "Ergonomic Assessments",
        "Environmental Compliance",
        "Sustainability Initiatives"
    ],
    
    "🔧 Asset & Equipment Management": [
        "Equipment Maintenance Scheduling",
        "Asset Tracking & Inventory",
        "Preventive Maintenance Programs",
        "Equipment Calibration",
        "Tool & Equipment Procurement",
        "Facility Equipment Lifecycle Management",
        "Maintenance Documentation",
        "Equipment Performance Monitoring"
    ],
    
    "🚗 Transportation & Fleet": [
        "Vehicle Fleet Management",
        "Driver Safety Training",
        "Vehicle Maintenance & Inspection",
        "Fuel Management",
        "Fleet Insurance & Compliance",
        "Vehicle Scheduling & Allocation",
        "Transportation Policy Management",
        "Fleet Performance Analytics"
    ],
    
    "📋 Documentation & Reporting": [
        "Safety Documentation Management",
        "Incident Report Processing",
        "Compliance Report Generation",
        "Safety Metrics & KPI Tracking",
        "Audit Trail Management",
        "Regulatory Filing & Submissions",
        "Safety Committee Meeting Management",
        "Training Record Management"
    ],
    
    "👷 Contractor & Vendor Management": [
        "Contractor Safety Qualification",
        "Vendor Safety Compliance",
        "Contractor Training & Orientation",
        "Work Permit Management",
        "Contractor Performance Monitoring",
        "Safety Service Provider Management",
        "Contractor Insurance Verification",
        "Subcontractor Safety Oversight"
    ],
    
    "📊 Safety Analytics & Reporting": [
        "Safety Performance Analytics",
        "Incident Trend Analysis",
        "Risk Assessment Reporting",
        "Safety Dashboard Development",
        "Compliance Status Monitoring",
        "Safety Cost Analysis",
        "Benchmarking & Best Practices",
        "Predictive Safety Analytics"
    ]
}

COMPANY_DEPARTMENTS = [
    "Finance", "Human Resources", "Operations", "Sales", "Marketing", 
    "IT", "Customer Service", "Supply Chain", "Manufacturing", "Executive",
    "Procurement", "Legal", "Quality Assurance", "Safety & Security"
]

# Default service data - these will be loaded into session state
DEFAULT_ORACLE_SERVICES = {
    "Oracle ERP Cloud": {
        "description": "Complete enterprise resource planning solution with financials, procurement, and project management",
        "price_per_user": 180,
        "setup_cost": 25000,
        "department": "IT"
    },
    "Oracle HCM Cloud": {
        "description": "Human capital management including payroll, talent management, and workforce planning",
        "price_per_user": 75,
        "setup_cost": 15000,
        "department": "IT"
    },
    "Oracle Supply Chain Management": {
        "description": "End-to-end supply chain planning, inventory management, and logistics optimization",
        "price_per_user": 120,
        "setup_cost": 20000,
        "department": "IT"
    },
    "Oracle Fusion Analytics": {
        "description": "Pre-built analytics and reporting for Oracle applications with real-time insights",
        "price_per_user": 45,
        "setup_cost": 8000,
        "department": "IT"
    }
}

DEFAULT_MICROSOFT_SERVICES = {
    "Microsoft 365 E3": {
        "description": "Premium productivity suite with advanced security, compliance, and analytics capabilities",
        "price_per_user": 82,
        "setup_cost": 5000,
        "department": "IT"
    },
    "Microsoft Teams Phone": {
        "description": "Cloud-based phone system integrated with Teams for calling and conferencing",
        "price_per_user": 28,
        "setup_cost": 3000,
        "department": "IT"
    },
    "Power BI Premium": {
        "description": "Advanced business intelligence with AI-powered insights and enterprise-grade capabilities",
        "price_per_user": 75,
        "setup_cost": 4000,
        "department": "IT"
    },
    "Project for the Web": {
        "description": "Cloud-based project management with resource scheduling and portfolio management",
        "price_per_user": 120,
        "setup_cost": 6000,
        "department": "IT"
    },
    "Microsoft Dynamics 365": {
        "description": "Customer relationship management and enterprise applications suite",
        "price_per_user": 210,
        "setup_cost": 30000,
        "department": "IT"
    }
}

DEFAULT_OTHER_SERVICES = {
    "Salesforce Enterprise": {
        "description": "Complete CRM platform with sales automation, marketing, and customer service capabilities",
        "price_per_user": 165,
        "setup_cost": 20000,
        "department": "IT"
    },
    "ServiceNow IT Service Management": {
        "description": "Comprehensive IT service management platform with incident, problem, and change management",
        "price_per_user": 95,
        "setup_cost": 15000,
        "department": "IT"
    },
    "Tableau Server": {
        "description": "Enterprise-grade data visualization and business intelligence platform",
        "price_per_user": 70,
        "setup_cost": 12000,
        "department": "IT"
    },
    "DocuSign eSignature": {
        "description": "Digital signature and document workflow automation platform",
        "price_per_user": 25,
        "setup_cost": 3000,
        "department": "IT"
    },
    "Zoom Enterprise Plus": {
        "description": "Advanced video conferencing with webinar and phone system integration",
        "price_per_user": 20,
        "setup_cost": 2500,
        "department": "IT"
    }
}

# Procurement Services with pricing
DEFAULT_PROCUREMENT_SERVICES = {
    "Procurement Management Suite": {
        "description": "Complete purchase-to-pay solution including PO management, supplier onboarding, and analytics",
        "price_per_transaction": 25,
        "setup_cost": 15000,
        "department": "Procurement"
    },
    "Supplier Portal & Management": {
        "description": "Centralized supplier registration, document management, and performance tracking",
        "price_per_supplier": 120,
        "setup_cost": 8000,
        "department": "Procurement"
    },
    "Contract Management System": {
        "description": "End-to-end contract lifecycle management with automated workflows and compliance tracking",
        "price_per_contract": 150,
        "setup_cost": 12000,
        "department": "Procurement"
    },
    "E-Sourcing & RFQ Platform": {
        "description": "Digital sourcing platform for RFQs, RFPs, competitive bidding, and supplier negotiations",
        "price_per_event": 500,
        "setup_cost": 10000,
        "department": "Procurement"
    },
    "Procurement Analytics & Reporting": {
        "description": "Advanced analytics for spend analysis, supplier performance, and procurement KPIs",
        "price_per_user": 85,
        "setup_cost": 6000,
        "department": "Procurement"
    }
}

# Facility & Safety Services with pricing
DEFAULT_FACILITY_SAFETY_SERVICES = {
    "Facility Management Platform": {
        "description": "Comprehensive facility management system for maintenance, space planning, and operations",
        "price_per_sq_meter": 12,
        "setup_cost": 25000,
        "department": "Facility_Safety"
    },
    "Safety Management System": {
        "description": "Integrated safety management platform for incident tracking, training, and compliance",
        "price_per_employee": 45,
        "setup_cost": 18000,
        "department": "Facility_Safety"
    },
    "Security & Access Control": {
        "description": "Complete security management including access control, surveillance, and visitor management",
        "price_per_access_point": 180,
        "setup_cost": 35000,
        "department": "Facility_Safety"
    },
    "Emergency Management System": {
        "description": "Emergency response planning, notification systems, and business continuity management",
        "price_per_location": 2500,
        "setup_cost": 20000,
        "department": "Facility_Safety"
    },
    "Environmental Monitoring": {
        "description": "Environmental compliance tracking, monitoring systems, and sustainability reporting",
        "price_per_monitoring_point": 250,
        "setup_cost": 15000,
        "department": "Facility_Safety"
    },
    "Asset & Equipment Management": {
        "description": "Asset tracking, maintenance scheduling, and equipment lifecycle management",
        "price_per_asset": 35,
        "setup_cost": 12000,
        "department": "Facility_Safety"
    },
    "Fleet Management System": {
        "description": "Vehicle fleet tracking, maintenance, fuel management, and driver safety monitoring",
        "price_per_vehicle": 850,
        "setup_cost": 22000,
        "department": "Facility_Safety"
    },
    "Safety Training & Compliance": {
        "description": "Online safety training platform with certification tracking and compliance management",
        "price_per_employee": 120,
        "setup_cost": 8000,
        "department": "Facility_Safety"
    }
}

# Support packages remain the same but now support multiple departments
DEFAULT_SUPPORT_PACKAGES = {
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
        "description": "Essential support for small teams with basic shared service needs",
        "departments": ["IT", "Procurement", "Facility_Safety"]
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
        "description": "Enhanced support for growing organizations",
        "departments": ["IT", "Procurement", "Facility_Safety"]
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
        "description": "Comprehensive support for medium enterprises",
        "departments": ["IT", "Procurement", "Facility_Safety"]
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
        "description": "Premium support for large organizations",
        "departments": ["IT", "Procurement", "Facility_Safety"]
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
        "description": "Enterprise-grade support with dedicated resources across all departments",
        "departments": ["IT", "Procurement", "Facility_Safety"]
    }
}

# RPA Package data remains the same
DEFAULT_RPA_PACKAGES = {
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
    
    .admin-header {
        background: linear-gradient(90deg, #dc2626, #ef4444);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 12px rgba(220, 38, 38, 0.3);
    }
    
    .department-selector {
        background: #f8fafc;
        border: 2px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        text-align: center;
    }
    
    .department-card {
        background: white;
        border: 2px solid #e5e7eb;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.5rem;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .department-card:hover {
        border-color: #3b82f6;
        box-shadow: 0 4px 16px rgba(59, 130, 246, 0.2);
        transform: translateY(-2px);
    }
    
    .department-card.selected {
        border-color: #dc2626;
        background: linear-gradient(135deg, #fef2f2 0%, #fecaca 100%);
        box-shadow: 0 6px 20px rgba(220, 38, 38, 0.25);
    }
    
    .category-section {
        background: #f8fafc;
        border: 2px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 5px solid #3b82f6;
    }
    
    .admin-section {
        background: #fef2f2;
        border: 2px solid #fecaca;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 5px solid #dc2626;
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
    
    .service-card.procurement {
        border-left: 4px solid #10b981;
    }
    
    .service-card.procurement:hover {
        border-color: #10b981;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.15);
    }
    
    .service-card.facility_safety {
        border-left: 4px solid #f59e0b;
    }
    
    .service-card.facility_safety:hover {
        border-color: #f59e0b;
        box-shadow: 0 4px 12px rgba(245, 158, 11, 0.15);
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
    
    .cost-display.procurement {
        background: #f0fdf4;
        border-color: #10b981;
    }
    
    .cost-display.facility_safety {
        background: #fffbeb;
        border-color: #f59e0b;
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
    
    .custom-service {
        background: #f3e8ff;
        border: 2px solid #8b5cf6;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .project-card {
        background: #fffbeb;
        border: 2px solid #f59e0b;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    .metric-card {
        background: white;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
        border: 1px solid #e5e7eb;
        margin: 0.5rem 0;
    }
    
    .login-card {
        background: white;
        border: 2px solid #e5e7eb;
        border-radius: 12px;
        padding: 2rem;
        margin: 2rem auto;
        max-width: 400px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    .admin-warning {
        background: #fef2f2;
        border: 2px solid #fecaca;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        color: #991b1b;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Authentication Functions
def hash_password(password):
    """Simple password hashing for demo purposes"""
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_admin(username, password):
    """Authenticate admin user"""
    if username in ADMIN_CREDENTIALS:
        stored_password = ADMIN_CREDENTIALS[username]["password"]
        if password == stored_password:  # In production, use proper password hashing
            return True, ADMIN_CREDENTIALS[username]
    return False, None

def show_admin_login():
    """Show admin login interface"""
    st.markdown("""
    <div class='login-card'>
        <h2 style='text-align: center; color: #dc2626; margin-bottom: 1.5rem;'>
            🔐 Department Head Access
        </h2>
        <p style='text-align: center; color: #6b7280; margin-bottom: 1.5rem;'>
            Secure access for authorized Department Heads to manage shared services content and pricing.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("admin_login_form"):
        st.markdown("### Login Credentials")
        username = st.text_input("Username", placeholder="e.g., it_admin")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        submitted = st.form_submit_button("🔓 Access Admin Panel", type="primary", use_container_width=True)
        
        if submitted:
            if username and password:
                is_valid, admin_info = authenticate_admin(username, password)
                if is_valid:
                    st.session_state.admin_authenticated = True
                    st.session_state.admin_user = username
                    st.session_state.admin_info = admin_info
                    st.success(f"✅ Welcome, {admin_info['name']}!")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials. Please check your username and password.")
            else:
                st.error("Please enter both username and password.")
    
    # Demo credentials info
    with st.expander("🔍 Demo Credentials", expanded=False):
        st.markdown("""
        **For demonstration purposes, use these credentials:**
        
        **IT Department:**
        - Username: `it_admin`
        - Password: `itadmin2025`
        
        **Procurement Department:**
        - Username: `procurement_admin`
        - Password: `procadmin2025`
        
        **Facility & Safety Department:**
        - Username: `facility_admin`
        - Password: `faciladmin2025`
        
        **Super Administrator:**
        - Username: `super_admin`
        - Password: `superadmin2025`
        """)

def check_admin_access(required_department=None):
    """Check if user has admin access for the specified department"""
    if not st.session_state.get('admin_authenticated', False):
        return False
    
    admin_info = st.session_state.get('admin_info', {})
    admin_dept = admin_info.get('department', '')
    
    if admin_dept == 'ALL':  # Super admin
        return True
    
    if required_department is None:
        return True
    
    return admin_dept == required_department

# Initialize session state for data management
def initialize_session_state():
    """Initialize session state with default data"""
    if 'selected_department' not in st.session_state:
        st.session_state.selected_department = None
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
    if 'app_mode' not in st.session_state:
        st.session_state.app_mode = 'client'  # 'client' or 'admin'
    if 'admin_authenticated' not in st.session_state:
        st.session_state.admin_authenticated = False
    
    # Initialize admin-managed data from defaults
    if 'admin_oracle_services' not in st.session_state:
        st.session_state.admin_oracle_services = DEFAULT_ORACLE_SERVICES.copy()
    if 'admin_microsoft_services' not in st.session_state:
        st.session_state.admin_microsoft_services = DEFAULT_MICROSOFT_SERVICES.copy()
    if 'admin_other_services' not in st.session_state:
        st.session_state.admin_other_services = DEFAULT_OTHER_SERVICES.copy()
    if 'admin_procurement_services' not in st.session_state:
        st.session_state.admin_procurement_services = DEFAULT_PROCUREMENT_SERVICES.copy()
    if 'admin_facility_safety_services' not in st.session_state:
        st.session_state.admin_facility_safety_services = DEFAULT_FACILITY_SAFETY_SERVICES.copy()
    if 'admin_support_packages' not in st.session_state:
        st.session_state.admin_support_packages = DEFAULT_SUPPORT_PACKAGES.copy()
    if 'admin_rpa_packages' not in st.session_state:
        st.session_state.admin_rpa_packages = DEFAULT_RPA_PACKAGES.copy()
    if 'admin_it_project_categories' not in st.session_state:
        st.session_state.admin_it_project_categories = DEFAULT_IT_PROJECT_CATEGORIES.copy()
    if 'admin_procurement_service_categories' not in st.session_state:
        st.session_state.admin_procurement_service_categories = DEFAULT_PROCUREMENT_SERVICE_CATEGORIES.copy()
    if 'admin_facility_safety_service_categories' not in st.session_state:
        st.session_state.admin_facility_safety_service_categories = DEFAULT_FACILITY_SAFETY_SERVICE_CATEGORIES.copy()

# Get current data (admin-managed if available, otherwise defaults)
def get_current_data():
    """Get current data from admin-managed session state"""
    return {
        'ORACLE_SERVICES': st.session_state.admin_oracle_services,
        'MICROSOFT_SERVICES': st.session_state.admin_microsoft_services,
        'OTHER_SERVICES': st.session_state.admin_other_services,
        'PROCUREMENT_SERVICES': st.session_state.admin_procurement_services,
        'FACILITY_SAFETY_SERVICES': st.session_state.admin_facility_safety_services,
        'SUPPORT_PACKAGES': st.session_state.admin_support_packages,
        'RPA_PACKAGES': st.session_state.admin_rpa_packages,
        'IT_PROJECT_CATEGORIES': st.session_state.admin_it_project_categories,
        'PROCUREMENT_SERVICE_CATEGORIES': st.session_state.admin_procurement_service_categories,
        'FACILITY_SAFETY_SERVICE_CATEGORIES': st.session_state.admin_facility_safety_service_categories
    }

# Department configurations
def get_departments_config():
    """Get departments configuration with current data"""
    current_data = get_current_data()
    
    return {
        "IT": {
            "icon": "💻",
            "title": "Information Technology",
            "project_categories": current_data['IT_PROJECT_CATEGORIES'],
            "color": "#3b82f6",
            "description": "Digital transformation, technology infrastructure, and enterprise applications"
        },
        "Procurement": {
            "icon": "🛒",
            "title": "Procurement & Supply Chain",
            "project_categories": current_data['PROCUREMENT_SERVICE_CATEGORIES'],
            "color": "#10b981",
            "description": "Purchasing, vendor management, contracts, and supply chain optimization"
        },
        "Facility_Safety": {
            "icon": "🏢",
            "title": "Facility & Safety",
            "project_categories": current_data['FACILITY_SAFETY_SERVICE_CATEGORIES'],
            "color": "#f59e0b",
            "description": "Facility management, workplace safety, security, and environmental compliance"
        }
    }

# Admin Management Functions
def show_admin_dashboard():
    """Show admin dashboard with department management options"""
    admin_info = st.session_state.get('admin_info', {})
    admin_dept = admin_info.get('department', '')
    admin_name = admin_info.get('name', 'Administrator')
    
    st.markdown(f"""
    <div class='admin-header'>
        <h1>🔧 Admin Dashboard</h1>
        <h2>Department Head Content Management</h2>
        <p><strong>Welcome:</strong> {admin_name} | <strong>Access Level:</strong> {admin_dept}</p>
        <p>Manage shared services content, pricing, and categories for 2025 budget planning</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Admin navigation
    if admin_dept == 'ALL':
        admin_tabs = st.tabs([
            "🏢 Overview", 
            "💻 IT Services", 
            "🛒 Procurement", 
            "🏢 Facility & Safety", 
            "🛠️ Support Packages",
            "🚀 Implementation Projects"
        ])
        
        with admin_tabs[0]:
            show_admin_overview()
        with admin_tabs[1]:
            show_admin_it_management()
        with admin_tabs[2]:
            show_admin_procurement_management()
        with admin_tabs[3]:
            show_admin_facility_safety_management()
        with admin_tabs[4]:
            show_admin_support_management()
        with admin_tabs[5]:
            show_admin_implementation_management()
            
    elif admin_dept == 'IT':
        admin_tabs = st.tabs([
            "💻 IT Services", 
            "🛠️ Support Packages", 
            "🚀 IT Implementation Projects"
        ])
        with admin_tabs[0]:
            show_admin_it_management()
        with admin_tabs[1]:
            show_admin_support_management()
        with admin_tabs[2]:
            show_admin_it_implementation_management()
            
    elif admin_dept == 'Procurement':
        admin_tabs = st.tabs([
            "🛒 Procurement Services",
            "🚀 Procurement Implementation Projects"
        ])
        with admin_tabs[0]:
            show_admin_procurement_management()
        with admin_tabs[1]:
            show_admin_procurement_implementation_management()
            
    elif admin_dept == 'Facility_Safety':
        admin_tabs = st.tabs([
            "🏢 Facility & Safety Services",
            "🚀 Facility Implementation Projects"
        ])
        with admin_tabs[0]:
            show_admin_facility_safety_management()
        with admin_tabs[1]:
            show_admin_facility_implementation_management()

def show_admin_overview():
    """Show admin overview with system statistics"""
    st.markdown("""
    <div class='admin-section'>
        <h2>📊 System Overview</h2>
        <p>Real-time statistics of the shared services catalogue system.</p>
    </div>
    """, unsafe_allow_html=True)
    
    current_data = get_current_data()
    
    # Statistics cards - Updated to include all 3 categories
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        oracle_count = len(current_data['ORACLE_SERVICES'])
        microsoft_count = len(current_data['MICROSOFT_SERVICES'])
        other_count = len(current_data['OTHER_SERVICES'])
        st.metric("🔧 IT Services", oracle_count + microsoft_count + other_count, f"{oracle_count} Oracle + {microsoft_count} Microsoft + {other_count} Other")
    
    with col2:
        procurement_count = len(current_data['PROCUREMENT_SERVICES'])
        st.metric("🛒 Procurement Services", procurement_count)
    
    with col3:
        facility_count = len(current_data['FACILITY_SAFETY_SERVICES'])
        st.metric("🏢 Facility & Safety Services", facility_count)
    
    with col4:
        support_count = len(current_data['SUPPORT_PACKAGES'])
        st.metric("🛠️ Support Packages", support_count)
    
    # Second row for Implementation Projects statistics
    st.markdown("---")
    st.markdown("#### 🚀 Implementation Projects Management")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        it_categories = len(current_data['IT_PROJECT_CATEGORIES'])
        st.metric("💻 IT Project Categories", it_categories)
    
    with col2:
        proc_categories = len(current_data['PROCUREMENT_SERVICE_CATEGORIES'])
        st.metric("🛒 Procurement Categories", proc_categories)
    
    with col3:
        facility_categories = len(current_data['FACILITY_SAFETY_SERVICE_CATEGORIES'])
        st.metric("🏢 Facility Categories", facility_categories)
    
    with col4:
        rpa_packages = len(current_data['RPA_PACKAGES'])
        st.metric("🤖 RPA Packages", rpa_packages)
    
    # Detailed breakdown
    st.markdown("---")
    st.markdown("#### 📈 Detailed System Statistics")
    
    # Create comprehensive statistics
    stats_data = {
        'Category': [
            '🔧 Operational Services',
            '🛠️ Support Packages', 
            '🚀 Implementation Projects',
            '📊 Total System Items'
        ],
        'IT Department': [
            len(current_data['ORACLE_SERVICES']) + len(current_data['MICROSOFT_SERVICES']) + len(current_data['OTHER_SERVICES']),
            len([p for p in current_data['SUPPORT_PACKAGES'].values() if 'IT' in p.get('departments', [])]),
            len(current_data['IT_PROJECT_CATEGORIES']) + len(current_data['RPA_PACKAGES']),
            len(current_data['ORACLE_SERVICES']) + len(current_data['MICROSOFT_SERVICES']) + len(current_data['OTHER_SERVICES']) + 
            len([p for p in current_data['SUPPORT_PACKAGES'].values() if 'IT' in p.get('departments', [])]) +
            len(current_data['IT_PROJECT_CATEGORIES']) + len(current_data['RPA_PACKAGES'])
        ],
        'Procurement Department': [
            len(current_data['PROCUREMENT_SERVICES']),
            len([p for p in current_data['SUPPORT_PACKAGES'].values() if 'Procurement' in p.get('departments', [])]),
            len(current_data['PROCUREMENT_SERVICE_CATEGORIES']),
            len(current_data['PROCUREMENT_SERVICES']) + 
            len([p for p in current_data['SUPPORT_PACKAGES'].values() if 'Procurement' in p.get('departments', [])]) +
            len(current_data['PROCUREMENT_SERVICE_CATEGORIES'])
        ],
        'Facility & Safety': [
            len(current_data['FACILITY_SAFETY_SERVICES']),
            len([p for p in current_data['SUPPORT_PACKAGES'].values() if 'Facility_Safety' in p.get('departments', [])]),
            len(current_data['FACILITY_SAFETY_SERVICE_CATEGORIES']),
            len(current_data['FACILITY_SAFETY_SERVICES']) + 
            len([p for p in current_data['SUPPORT_PACKAGES'].values() if 'Facility_Safety' in p.get('departments', [])]) +
            len(current_data['FACILITY_SAFETY_SERVICE_CATEGORIES'])
        ]
    }
    
    df_stats = pd.DataFrame(stats_data)
    st.dataframe(df_stats, use_container_width=True)
    
    # Recent activity (simulation)
    st.markdown("### 📈 Recent Admin Activity")
    st.info("🔄 This section would show recent changes made by department heads in a production environment.")
    
    # Implementation Projects Activity Summary
    with st.expander("🚀 Implementation Projects Activity", expanded=False):
        st.markdown("""
        **Recent Changes to Implementation Projects:**
        - ✅ Project categories can now be managed by department heads
        - ✅ RPA packages are fully configurable with pricing
        - ✅ All 3 main categories (Operational, Support, Implementation) are admin-managed
        - ✅ Real-time updates apply immediately to client interface
        """)
    
    # Quick actions
    st.markdown("### ⚡ Quick Actions")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📊 Export All Data", use_container_width=True):
            st.success("📊 System data export functionality would be implemented here.")
    
    with col2:
        if st.button("🔄 Reset to Defaults", use_container_width=True):
            st.warning("⚠️ Reset functionality would restore all services to default settings.")
    
    with col3:
        if st.button("📧 Notify Departments", use_container_width=True):
            st.success("📧 Notification system would alert departments of updates.")
    
    with col4:
        if st.button("🚀 Sync Implementation Projects", use_container_width=True):
            st.success("🚀 Implementation projects synchronized across all departments.")

def show_admin_it_management():
    """Show IT services management interface"""
    if not check_admin_access('IT'):
        st.error("❌ Access denied. This section requires IT Department Head access.")
        return
    
    st.markdown("""
    <div class='admin-section'>
        <h2>💻 IT Services Management</h2>
        <p>Manage Oracle, Microsoft, and other IT services, pricing, and project categories.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Oracle Services Management
    st.markdown("### 🟠 Oracle Services Management")
    
    # Add new Oracle service
    with st.expander("➕ Add New Oracle Service", expanded=False):
        with st.form("add_oracle_service"):
            col1, col2 = st.columns(2)
            
            with col1:
                service_name = st.text_input("Service Name")
                description = st.text_area("Description")
            
            with col2:
                price_per_user = st.number_input("Price per User (SAR/month)", min_value=0, value=100)
                setup_cost = st.number_input("Setup Cost (SAR)", min_value=0, value=5000)
            
            if st.form_submit_button("Add Oracle Service", type="primary"):
                if service_name and description:
                    st.session_state.admin_oracle_services[service_name] = {
                        "description": description,
                        "price_per_user": price_per_user,
                        "setup_cost": setup_cost,
                        "department": "IT"
                    }
                    st.success(f"✅ Added Oracle service: {service_name}")
                    st.rerun()
                else:
                    st.error("Please fill in all required fields.")
    
    # Existing Oracle services
    if st.session_state.admin_oracle_services:
        st.markdown("#### Current Oracle Services")
        
        for service_name, details in st.session_state.admin_oracle_services.items():
            with st.expander(f"🔧 {service_name}", expanded=False):
                col1, col2, col3 = st.columns([2, 2, 1])
                
                with col1:
                    new_desc = st.text_area(
                        "Description", 
                        value=details['description'], 
                        key=f"oracle_desc_{service_name}"
                    )
                    
                with col2:
                    new_price = st.number_input(
                        "Price per User (SAR/month)", 
                        value=details['price_per_user'], 
                        min_value=0,
                        key=f"oracle_price_{service_name}"
                    )
                    new_setup = st.number_input(
                        "Setup Cost (SAR)", 
                        value=details['setup_cost'], 
                        min_value=0,
                        key=f"oracle_setup_{service_name}"
                    )
                
                with col3:
                    if st.button("💾 Update", key=f"update_oracle_{service_name}"):
                        st.session_state.admin_oracle_services[service_name].update({
                            'description': new_desc,
                            'price_per_user': new_price,
                            'setup_cost': new_setup
                        })
                        st.success(f"✅ Updated {service_name}")
                        st.rerun()
                    
                    if st.button("🗑️ Remove", key=f"remove_oracle_{service_name}"):
                        del st.session_state.admin_oracle_services[service_name]
                        st.success(f"🗑️ Removed {service_name}")
                        st.rerun()
    
    st.markdown("---")
    
    # Microsoft Services Management
    st.markdown("### 🟦 Microsoft Services Management")
    
    # Add new Microsoft service
    with st.expander("➕ Add New Microsoft Service", expanded=False):
        with st.form("add_microsoft_service"):
            col1, col2 = st.columns(2)
            
            with col1:
                service_name = st.text_input("Service Name", key="ms_service_name")
                description = st.text_area("Description", key="ms_description")
            
            with col2:
                price_per_user = st.number_input("Price per User (SAR/month)", min_value=0, value=100, key="ms_price")
                setup_cost = st.number_input("Setup Cost (SAR)", min_value=0, value=5000, key="ms_setup")
            
            if st.form_submit_button("Add Microsoft Service", type="primary"):
                if service_name and description:
                    st.session_state.admin_microsoft_services[service_name] = {
                        "description": description,
                        "price_per_user": price_per_user,
                        "setup_cost": setup_cost,
                        "department": "IT"
                    }
                    st.success(f"✅ Added Microsoft service: {service_name}")
                    st.rerun()
                else:
                    st.error("Please fill in all required fields.")
    
    # Existing Microsoft services
    if st.session_state.admin_microsoft_services:
        st.markdown("#### Current Microsoft Services")
        
        for service_name, details in st.session_state.admin_microsoft_services.items():
            with st.expander(f"🔧 {service_name}", expanded=False):
                col1, col2, col3 = st.columns([2, 2, 1])
                
                with col1:
                    new_desc = st.text_area(
                        "Description", 
                        value=details['description'], 
                        key=f"ms_desc_{service_name}"
                    )
                    
                with col2:
                    new_price = st.number_input(
                        "Price per User (SAR/month)", 
                        value=details['price_per_user'], 
                        min_value=0,
                        key=f"ms_price_{service_name}"
                    )
                    new_setup = st.number_input(
                        "Setup Cost (SAR)", 
                        value=details['setup_cost'], 
                        min_value=0,
                        key=f"ms_setup_{service_name}"
                    )
                
                with col3:
                    if st.button("💾 Update", key=f"update_ms_{service_name}"):
                        st.session_state.admin_microsoft_services[service_name].update({
                            'description': new_desc,
                            'price_per_user': new_price,
                            'setup_cost': new_setup
                        })
                        st.success(f"✅ Updated {service_name}")
                        st.rerun()
                    
                    if st.button("🗑️ Remove", key=f"remove_ms_{service_name}"):
                        del st.session_state.admin_microsoft_services[service_name]
                        st.success(f"🗑️ Removed {service_name}")
                        st.rerun()
    
    st.markdown("---")
    
    # Other Services Management
    st.markdown("### 🔧 Other Licenses & Services Management")
    
    # Add new Other service
    with st.expander("➕ Add New Other Service", expanded=False):
        with st.form("add_other_service"):
            col1, col2 = st.columns(2)
            
            with col1:
                service_name = st.text_input("Service Name", key="other_service_name")
                description = st.text_area("Description", key="other_description")
            
            with col2:
                price_per_user = st.number_input("Price per User (SAR/month)", min_value=0, value=100, key="other_price")
                setup_cost = st.number_input("Setup Cost (SAR)", min_value=0, value=5000, key="other_setup")
            
            if st.form_submit_button("Add Other Service", type="primary"):
                if service_name and description:
                    st.session_state.admin_other_services[service_name] = {
                        "description": description,
                        "price_per_user": price_per_user,
                        "setup_cost": setup_cost,
                        "department": "IT"
                    }
                    st.success(f"✅ Added Other service: {service_name}")
                    st.rerun()
                else:
                    st.error("Please fill in all required fields.")
    
    # Existing Other services
    if st.session_state.admin_other_services:
        st.markdown("#### Current Other Services")
        
        for service_name, details in st.session_state.admin_other_services.items():
            with st.expander(f"🔧 {service_name}", expanded=False):
                col1, col2, col3 = st.columns([2, 2, 1])
                
                with col1:
                    new_desc = st.text_area(
                        "Description", 
                        value=details['description'], 
                        key=f"other_desc_{service_name}"
                    )
                    
                with col2:
                    new_price = st.number_input(
                        "Price per User (SAR/month)", 
                        value=details['price_per_user'], 
                        min_value=0,
                        key=f"other_price_{service_name}"
                    )
                    new_setup = st.number_input(
                        "Setup Cost (SAR)", 
                        value=details['setup_cost'], 
                        min_value=0,
                        key=f"other_setup_{service_name}"
                    )
                
                with col3:
                    if st.button("💾 Update", key=f"update_other_{service_name}"):
                        st.session_state.admin_other_services[service_name].update({
                            'description': new_desc,
                            'price_per_user': new_price,
                            'setup_cost': new_setup
                        })
                        st.success(f"✅ Updated {service_name}")
                        st.rerun()
                    
                    if st.button("🗑️ Remove", key=f"remove_other_{service_name}"):
                        del st.session_state.admin_other_services[service_name]
                        st.success(f"🗑️ Removed {service_name}")
                        st.rerun()

def show_admin_procurement_management():
    """Show Procurement services management interface"""
    if not check_admin_access('Procurement'):
        st.error("❌ Access denied. This section requires Procurement Department Head access.")
        return
    
    st.markdown("""
    <div class='admin-section'>
        <h2>🛒 Procurement Services Management</h2>
        <p>Manage procurement services, pricing models, and service categories.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Add new Procurement service
    with st.expander("➕ Add New Procurement Service", expanded=False):
        with st.form("add_procurement_service"):
            col1, col2 = st.columns(2)
            
            with col1:
                service_name = st.text_input("Service Name")
                description = st.text_area("Description")
                pricing_model = st.selectbox(
                    "Pricing Model", 
                    ["price_per_user", "price_per_transaction", "price_per_supplier", "price_per_contract", "price_per_event"]
                )
            
            with col2:
                price_value = st.number_input("Price Value (SAR)", min_value=0, value=100)
                setup_cost = st.number_input("Setup Cost (SAR)", min_value=0, value=5000)
            
            if st.form_submit_button("Add Procurement Service", type="primary"):
                if service_name and description:
                    service_data = {
                        "description": description,
                        pricing_model: price_value,
                        "setup_cost": setup_cost,
                        "department": "Procurement"
                    }
                    st.session_state.admin_procurement_services[service_name] = service_data
                    st.success(f"✅ Added Procurement service: {service_name}")
                    st.rerun()
                else:
                    st.error("Please fill in all required fields.")
    
    # Existing Procurement services
    if st.session_state.admin_procurement_services:
        st.markdown("#### Current Procurement Services")
        
        for service_name, details in st.session_state.admin_procurement_services.items():
            with st.expander(f"🔧 {service_name}", expanded=False):
                col1, col2, col3 = st.columns([2, 2, 1])
                
                with col1:
                    new_desc = st.text_area(
                        "Description", 
                        value=details['description'], 
                        key=f"proc_desc_{service_name}"
                    )
                
                with col2:
                    # Find the pricing model
                    pricing_models = ["price_per_user", "price_per_transaction", "price_per_supplier", "price_per_contract", "price_per_event"]
                    current_pricing_model = None
                    current_price = 0
                    
                    for model in pricing_models:
                        if model in details:
                            current_pricing_model = model
                            current_price = details[model]
                            break
                    
                    new_price = st.number_input(
                        f"Price ({current_pricing_model.replace('_', ' ').title()})", 
                        value=current_price, 
                        min_value=0,
                        key=f"proc_price_{service_name}"
                    )
                    new_setup = st.number_input(
                        "Setup Cost (SAR)", 
                        value=details['setup_cost'], 
                        min_value=0,
                        key=f"proc_setup_{service_name}"
                    )
                
                with col3:
                    if st.button("💾 Update", key=f"update_proc_{service_name}"):
                        st.session_state.admin_procurement_services[service_name]['description'] = new_desc
                        st.session_state.admin_procurement_services[service_name]['setup_cost'] = new_setup
                        if current_pricing_model:
                            st.session_state.admin_procurement_services[service_name][current_pricing_model] = new_price
                        st.success(f"✅ Updated {service_name}")
                        st.rerun()
                    
                    if st.button("🗑️ Remove", key=f"remove_proc_{service_name}"):
                        del st.session_state.admin_procurement_services[service_name]
                        st.success(f"🗑️ Removed {service_name}")
                        st.rerun()

def show_admin_facility_safety_management():
    """Show Facility & Safety services management interface"""
    if not check_admin_access('Facility_Safety'):
        st.error("❌ Access denied. This section requires Facility & Safety Department Head access.")
        return
    
    st.markdown("""
    <div class='admin-section'>
        <h2>🏢 Facility & Safety Services Management</h2>
        <p>Manage facility and safety services, pricing models, and service categories.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Add new Facility & Safety service
    with st.expander("➕ Add New Facility & Safety Service", expanded=False):
        with st.form("add_facility_service"):
            col1, col2 = st.columns(2)
            
            with col1:
                service_name = st.text_input("Service Name")
                description = st.text_area("Description")
                pricing_model = st.selectbox(
                    "Pricing Model", 
                    ["price_per_user", "price_per_employee", "price_per_sq_meter", "price_per_access_point", 
                     "price_per_location", "price_per_monitoring_point", "price_per_asset", "price_per_vehicle"]
                )
            
            with col2:
                price_value = st.number_input("Price Value (SAR)", min_value=0, value=100)
                setup_cost = st.number_input("Setup Cost (SAR)", min_value=0, value=5000)
            
            if st.form_submit_button("Add Facility & Safety Service", type="primary"):
                if service_name and description:
                    service_data = {
                        "description": description,
                        pricing_model: price_value,
                        "setup_cost": setup_cost,
                        "department": "Facility_Safety"
                    }
                    st.session_state.admin_facility_safety_services[service_name] = service_data
                    st.success(f"✅ Added Facility & Safety service: {service_name}")
                    st.rerun()
                else:
                    st.error("Please fill in all required fields.")
    
    # Existing Facility & Safety services
    if st.session_state.admin_facility_safety_services:
        st.markdown("#### Current Facility & Safety Services")
        
        for service_name, details in st.session_state.admin_facility_safety_services.items():
            with st.expander(f"🔧 {service_name}", expanded=False):
                col1, col2, col3 = st.columns([2, 2, 1])
                
                with col1:
                    new_desc = st.text_area(
                        "Description", 
                        value=details['description'], 
                        key=f"fac_desc_{service_name}"
                    )
                
                with col2:
                    # Find the pricing model
                    pricing_models = ["price_per_user", "price_per_employee", "price_per_sq_meter", "price_per_access_point", 
                                    "price_per_location", "price_per_monitoring_point", "price_per_asset", "price_per_vehicle"]
                    current_pricing_model = None
                    current_price = 0
                    
                    for model in pricing_models:
                        if model in details:
                            current_pricing_model = model
                            current_price = details[model]
                            break
                    
                    new_price = st.number_input(
                        f"Price ({current_pricing_model.replace('_', ' ').title()})", 
                        value=current_price, 
                        min_value=0,
                        key=f"fac_price_{service_name}"
                    )
                    new_setup = st.number_input(
                        "Setup Cost (SAR)", 
                        value=details['setup_cost'], 
                        min_value=0,
                        key=f"fac_setup_{service_name}"
                    )
                
                with col3:
                    if st.button("💾 Update", key=f"update_fac_{service_name}"):
                        st.session_state.admin_facility_safety_services[service_name]['description'] = new_desc
                        st.session_state.admin_facility_safety_services[service_name]['setup_cost'] = new_setup
                        if current_pricing_model:
                            st.session_state.admin_facility_safety_services[service_name][current_pricing_model] = new_price
                        st.success(f"✅ Updated {service_name}")
                        st.rerun()
                    
                    if st.button("🗑️ Remove", key=f"remove_fac_{service_name}"):
                        del st.session_state.admin_facility_safety_services[service_name]
                        st.success(f"🗑️ Removed {service_name}")
                        st.rerun()

def show_admin_implementation_management():
    """Show comprehensive implementation projects management for all departments"""
    if not check_admin_access():
        st.error("❌ Access denied. This section requires admin access.")
        return
    
    st.markdown("""
    <div class='admin-section'>
        <h2>🚀 Implementation Projects Management</h2>
        <p>Manage project categories, RPA packages, and implementation settings across all departments.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sub-tabs for different aspects of implementation management
    impl_tabs = st.tabs([
        "💻 IT Categories", 
        "🛒 Procurement Categories", 
        "🏢 Facility Categories",
        "🤖 RPA Packages"
    ])
    
    with impl_tabs[0]:
        show_admin_it_categories_management()
    
    with impl_tabs[1]:
        show_admin_procurement_categories_management()
    
    with impl_tabs[2]:
        show_admin_facility_categories_management()
    
    with impl_tabs[3]:
        show_admin_rpa_management()

def show_admin_it_implementation_management():
    """Show IT implementation projects management"""
    if not check_admin_access('IT'):
        st.error("❌ Access denied. This section requires IT Department Head access.")
        return
    
    st.markdown("""
    <div class='admin-section'>
        <h2>🚀 IT Implementation Projects Management</h2>
        <p>Manage IT project categories and RPA packages.</p>
    </div>
    """, unsafe_allow_html=True)
    
    impl_tabs = st.tabs(["💻 IT Categories", "🤖 RPA Packages"])
    
    with impl_tabs[0]:
        show_admin_it_categories_management()
    
    with impl_tabs[1]:
        show_admin_rpa_management()

def show_admin_procurement_implementation_management():
    """Show Procurement implementation projects management"""
    if not check_admin_access('Procurement'):
        st.error("❌ Access denied. This section requires Procurement Department Head access.")
        return
    
    st.markdown("""
    <div class='admin-section'>
        <h2>🚀 Procurement Implementation Projects Management</h2>
        <p>Manage procurement project categories and implementation settings.</p>
    </div>
    """, unsafe_allow_html=True)
    
    show_admin_procurement_categories_management()

def show_admin_facility_implementation_management():
    """Show Facility & Safety implementation projects management"""
    if not check_admin_access('Facility_Safety'):
        st.error("❌ Access denied. This section requires Facility & Safety Department Head access.")
        return
    
    st.markdown("""
    <div class='admin-section'>
        <h2>🚀 Facility & Safety Implementation Projects Management</h2>
        <p>Manage facility and safety project categories and implementation settings.</p>
    </div>
    """, unsafe_allow_html=True)
    
    show_admin_facility_categories_management()

def show_admin_it_categories_management():
    """Manage IT project categories"""
    st.markdown("### 💻 IT Project Categories Management")
    
    # Add new category
    with st.expander("➕ Add New IT Project Category", expanded=False):
        with st.form("add_it_category"):
            category_name = st.text_input("Category Name (with emoji)", placeholder="e.g., 🆕 New Technology")
            category_services = st.text_area(
                "Services in Category (one per line)", 
                placeholder="Service Name 1\nService Name 2\nService Name 3"
            )
            
            if st.form_submit_button("Add IT Category", type="primary"):
                if category_name and category_services:
                    services_list = [service.strip() for service in category_services.split('\n') if service.strip()]
                    st.session_state.admin_it_project_categories[category_name] = services_list
                    st.success(f"✅ Added IT category: {category_name}")
                    st.rerun()
                else:
                    st.error("Please fill in all required fields.")
    
    # Existing categories management
    if st.session_state.admin_it_project_categories:
        st.markdown("#### Current IT Project Categories")
        
        for category_name, services in st.session_state.admin_it_project_categories.items():
            with st.expander(f"🔧 {category_name}", expanded=False):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    new_services = st.text_area(
                        "Services in Category (one per line)",
                        value='\n'.join(services),
                        key=f"it_cat_services_{category_name}",
                        height=150
                    )
                
                with col2:
                    if st.button("💾 Update", key=f"update_it_cat_{category_name}"):
                        services_list = [service.strip() for service in new_services.split('\n') if service.strip()]
                        st.session_state.admin_it_project_categories[category_name] = services_list
                        st.success(f"✅ Updated {category_name}")
                        st.rerun()
                    
                    if st.button("🗑️ Remove", key=f"remove_it_cat_{category_name}"):
                        del st.session_state.admin_it_project_categories[category_name]
                        st.success(f"🗑️ Removed {category_name}")
                        st.rerun()

def show_admin_procurement_categories_management():
    """Manage Procurement project categories"""
    st.markdown("### 🛒 Procurement Project Categories Management")
    
    # Add new category
    with st.expander("➕ Add New Procurement Project Category", expanded=False):
        with st.form("add_procurement_category"):
            category_name = st.text_input("Category Name (with emoji)", placeholder="e.g., 📦 New Process Category")
            category_services = st.text_area(
                "Services in Category (one per line)", 
                placeholder="Service Name 1\nService Name 2\nService Name 3"
            )
            
            if st.form_submit_button("Add Procurement Category", type="primary"):
                if category_name and category_services:
                    services_list = [service.strip() for service in category_services.split('\n') if service.strip()]
                    st.session_state.admin_procurement_service_categories[category_name] = services_list
                    st.success(f"✅ Added Procurement category: {category_name}")
                    st.rerun()
                else:
                    st.error("Please fill in all required fields.")
    
    # Existing categories management
    if st.session_state.admin_procurement_service_categories:
        st.markdown("#### Current Procurement Project Categories")
        
        for category_name, services in st.session_state.admin_procurement_service_categories.items():
            with st.expander(f"🔧 {category_name}", expanded=False):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    new_services = st.text_area(
                        "Services in Category (one per line)",
                        value='\n'.join(services),
                        key=f"proc_cat_services_{category_name}",
                        height=150
                    )
                
                with col2:
                    if st.button("💾 Update", key=f"update_proc_cat_{category_name}"):
                        services_list = [service.strip() for service in new_services.split('\n') if service.strip()]
                        st.session_state.admin_procurement_service_categories[category_name] = services_list
                        st.success(f"✅ Updated {category_name}")
                        st.rerun()
                    
                    if st.button("🗑️ Remove", key=f"remove_proc_cat_{category_name}"):
                        del st.session_state.admin_procurement_service_categories[category_name]
                        st.success(f"🗑️ Removed {category_name}")
                        st.rerun()

def show_admin_facility_categories_management():
    """Manage Facility & Safety project categories"""
    st.markdown("### 🏢 Facility & Safety Project Categories Management")
    
    # Add new category
    with st.expander("➕ Add New Facility & Safety Project Category", expanded=False):
        with st.form("add_facility_category"):
            category_name = st.text_input("Category Name (with emoji)", placeholder="e.g., 🔒 New Security Category")
            category_services = st.text_area(
                "Services in Category (one per line)", 
                placeholder="Service Name 1\nService Name 2\nService Name 3"
            )
            
            if st.form_submit_button("Add Facility & Safety Category", type="primary"):
                if category_name and category_services:
                    services_list = [service.strip() for service in category_services.split('\n') if service.strip()]
                    st.session_state.admin_facility_safety_service_categories[category_name] = services_list
                    st.success(f"✅ Added Facility & Safety category: {category_name}")
                    st.rerun()
                else:
                    st.error("Please fill in all required fields.")
    
    # Existing categories management
    if st.session_state.admin_facility_safety_service_categories:
        st.markdown("#### Current Facility & Safety Project Categories")
        
        for category_name, services in st.session_state.admin_facility_safety_service_categories.items():
            with st.expander(f"🔧 {category_name}", expanded=False):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    new_services = st.text_area(
                        "Services in Category (one per line)",
                        value='\n'.join(services),
                        key=f"fac_cat_services_{category_name}",
                        height=150
                    )
                
                with col2:
                    if st.button("💾 Update", key=f"update_fac_cat_{category_name}"):
                        services_list = [service.strip() for service in new_services.split('\n') if service.strip()]
                        st.session_state.admin_facility_safety_service_categories[category_name] = services_list
                        st.success(f"✅ Updated {category_name}")
                        st.rerun()
                    
                    if st.button("🗑️ Remove", key=f"remove_fac_cat_{category_name}"):
                        del st.session_state.admin_facility_safety_service_categories[category_name]
                        st.success(f"🗑️ Removed {category_name}")
                        st.rerun()

def show_admin_rpa_management():
    """Manage RPA packages"""
    st.markdown("### 🤖 RPA Packages Management")
    
    # Add new RPA package
    with st.expander("➕ Add New RPA Package", expanded=False):
        with st.form("add_rpa_package"):
            col1, col2 = st.columns(2)
            
            with col1:
                package_name = st.text_input("Package Name", placeholder="e.g., Enterprise (15 Credits)")
                discovery_analysis = st.number_input("Discovery Analysis Cost (SAR)", min_value=0, value=50000)
                build_implementation = st.number_input("Build Implementation Cost (SAR)", min_value=0, value=10000)
                project_management = st.number_input("Project Management Cost (SAR)", min_value=0, value=15000)
                infrastructure_license = st.number_input("Infrastructure License Cost (SAR)", min_value=0, value=60000)
            
            with col2:
                year_2_cost = st.number_input("Year 2 Cost (SAR)", min_value=0, value=15000)
                year_3_cost = st.number_input("Year 3 Cost (SAR)", min_value=0, value=16000)
                processes_covered = st.text_input("Processes Covered", placeholder="e.g., Covers up to 15 processes")
                implementation_processes = st.text_input("Implementation Processes", placeholder="e.g., Covers up to 8 processes")
            
            if st.form_submit_button("Add RPA Package", type="primary"):
                if package_name and processes_covered and implementation_processes:
                    year_1_total = discovery_analysis + build_implementation + project_management + infrastructure_license
                    
                    rpa_package_data = {
                        "discovery_analysis": discovery_analysis,
                        "build_implementation": build_implementation,
                        "project_management": project_management,
                        "infrastructure_license": infrastructure_license,
                        "year_1_total": year_1_total,
                        "year_2_cost": year_2_cost,
                        "year_3_cost": year_3_cost,
                        "processes_covered": processes_covered,
                        "implementation_processes": implementation_processes
                    }
                    
                    st.session_state.admin_rpa_packages[package_name] = rpa_package_data
                    st.success(f"✅ Added RPA package: {package_name}")
                    st.rerun()
                else:
                    st.error("Please fill in all required fields.")
    
    # Existing RPA packages management
    if st.session_state.admin_rpa_packages:
        st.markdown("#### Current RPA Packages")
        
        for package_name, details in st.session_state.admin_rpa_packages.items():
            with st.expander(f"🔧 {package_name}", expanded=False):
                col1, col2, col3 = st.columns([2, 2, 1])
                
                with col1:
                    new_discovery = st.number_input(
                        "Discovery Analysis (SAR)", 
                        value=details['discovery_analysis'], 
                        min_value=0,
                        key=f"rpa_discovery_{package_name}"
                    )
                    new_build = st.number_input(
                        "Build Implementation (SAR)", 
                        value=details['build_implementation'], 
                        min_value=0,
                        key=f"rpa_build_{package_name}"
                    )
                    new_pm = st.number_input(
                        "Project Management (SAR)", 
                        value=details['project_management'], 
                        min_value=0,
                        key=f"rpa_pm_{package_name}"
                    )
                    new_infrastructure = st.number_input(
                        "Infrastructure License (SAR)", 
                        value=details['infrastructure_license'], 
                        min_value=0,
                        key=f"rpa_infrastructure_{package_name}"
                    )
                
                with col2:
                    new_year_2 = st.number_input(
                        "Year 2 Cost (SAR)", 
                        value=details['year_2_cost'], 
                        min_value=0,
                        key=f"rpa_year2_{package_name}"
                    )
                    new_year_3 = st.number_input(
                        "Year 3 Cost (SAR)", 
                        value=details['year_3_cost'], 
                        min_value=0,
                        key=f"rpa_year3_{package_name}"
                    )
                    new_processes_covered = st.text_input(
                        "Processes Covered", 
                        value=details['processes_covered'],
                        key=f"rpa_processes_{package_name}"
                    )
                    new_implementation_processes = st.text_input(
                        "Implementation Processes", 
                        value=details['implementation_processes'],
                        key=f"rpa_impl_{package_name}"
                    )
                
                with col3:
                    if st.button("💾 Update", key=f"update_rpa_{package_name}"):
                        year_1_total = new_discovery + new_build + new_pm + new_infrastructure
                        
                        st.session_state.admin_rpa_packages[package_name].update({
                            'discovery_analysis': new_discovery,
                            'build_implementation': new_build,
                            'project_management': new_pm,
                            'infrastructure_license': new_infrastructure,
                            'year_1_total': year_1_total,
                            'year_2_cost': new_year_2,
                            'year_3_cost': new_year_3,
                            'processes_covered': new_processes_covered,
                            'implementation_processes': new_implementation_processes
                        })
                        st.success(f"✅ Updated {package_name}")
                        st.rerun()
                    
                    if st.button("🗑️ Remove", key=f"remove_rpa_{package_name}"):
                        del st.session_state.admin_rpa_packages[package_name]
                        st.success(f"🗑️ Removed {package_name}")
                        st.rerun()
                    
                    # Show calculated Year 1 total
                    year_1_calc = new_discovery + new_build + new_pm + new_infrastructure
                    st.metric("Year 1 Total", f"SAR {year_1_calc:,.0f}")

def show_admin_support_management():
    """Show support packages management interface"""
    if not check_admin_access():
        st.error("❌ Access denied. This section requires admin access.")
        return
    
    st.markdown("""
    <div class='admin-section'>
        <h2>🛠️ Support Packages Management</h2>
        <p>Manage support packages pricing and features.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Support Packages Management
    if st.session_state.admin_support_packages:
        st.markdown("#### Current Support Packages")
        
        for package_name, details in st.session_state.admin_support_packages.items():
            with st.expander(f"🔧 {package_name} Package", expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    new_price = st.number_input(
                        "Package Price (SAR)", 
                        value=details['price'], 
                        min_value=0,
                        key=f"support_price_{package_name}"
                    )
                    new_description = st.text_area(
                        "Description", 
                        value=details['description'], 
                        key=f"support_desc_{package_name}"
                    )
                    new_standard = st.number_input(
                        "Standard Support Requests", 
                        value=details['support_requests_standard'], 
                        min_value=0,
                        key=f"support_standard_{package_name}"
                    )
                    new_priority = st.number_input(
                        "Priority Support Requests", 
                        value=details['support_requests_priority'], 
                        min_value=0,
                        key=f"support_priority_{package_name}"
                    )
                
                with col2:
                    new_premium = st.number_input(
                        "Premium Support Requests", 
                        value=details['support_requests_premium'], 
                        min_value=0,
                        key=f"support_premium_{package_name}"
                    )
                    new_improvement_hours = st.number_input(
                        "Improvement Hours", 
                        value=details['improvement_hours'], 
                        min_value=0,
                        key=f"support_improvement_{package_name}"
                    )
                    new_training = st.number_input(
                        "Training Requests", 
                        value=details['training_requests'], 
                        min_value=0,
                        key=f"support_training_{package_name}"
                    )
                    new_reports = st.number_input(
                        "Report Requests", 
                        value=details['report_requests'], 
                        min_value=0,
                        key=f"support_reports_{package_name}"
                    )
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("💾 Update Package", key=f"update_support_{package_name}"):
                        st.session_state.admin_support_packages[package_name].update({
                            'price': new_price,
                            'description': new_description,
                            'support_requests_standard': new_standard,
                            'support_requests_priority': new_priority,
                            'support_requests_premium': new_premium,
                            'total_support_requests': new_standard + new_priority + new_premium,
                            'improvement_hours': new_improvement_hours,
                            'training_requests': new_training,
                            'report_requests': new_reports
                        })
                        st.success(f"✅ Updated {package_name} package")
                        st.rerun()
                
                with col2:
                    if st.button("🗑️ Remove Package", key=f"remove_support_{package_name}"):
                        del st.session_state.admin_support_packages[package_name]
                        st.success(f"🗑️ Removed {package_name} package")
                        st.rerun()

# Department selection functions (updated to use current data)
def show_department_selection():
    departments_config = get_departments_config()
    
    st.markdown("""
    <div class='department-selector'>
        <h2>🏢 Select Shared Services Department</h2>
        <p>Choose the department for which you want to configure shared services</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Show current selections if returning from a department
    if len(st.session_state.operational_services) > 0 or len(st.session_state.implementation_projects) > 0:
        st.info("💡 You have existing selections. Switching departments will preserve your data for each department separately.")
    
    cols = st.columns(len(departments_config))
    
    for i, (dept_key, dept_config) in enumerate(departments_config.items()):
        with cols[i]:
            # Check if this department has any selections
            dept_projects = [p for p in st.session_state.implementation_projects if p.get('shared_service_dept') == dept_key]
            dept_services = [k for k, v in st.session_state.operational_services.items() if v.get('selected', False)]
            
            has_selections = len(dept_projects) > 0 or len(dept_services) > 0
            
            card_class = "department-card"
            
            st.markdown(f"""
            <div class='{card_class}' style='position: relative;'>
                <h1 style='margin: 0; color: {dept_config["color"]};'>{dept_config["icon"]}</h1>
                <h3 style='margin: 0.5rem 0; color: #1f2937;'>{dept_config["title"]}</h3>
                <p style='margin: 0; color: #6b7280; font-size: 0.9em;'>{dept_config["description"]}</p>
                {f'<div style="position: absolute; top: 10px; right: 10px; background: #10b981; color: white; padding: 0.25rem 0.5rem; border-radius: 12px; font-size: 0.7rem; font-weight: 600;">✓ Has Selections</div>' if has_selections else ''}
            </div>
            """, unsafe_allow_html=True)
            
            button_text = f"Continue with {dept_config['title']}" if has_selections else f"Select {dept_config['title']}"
            button_type = "secondary" if has_selections else "primary"
            
            if st.button(button_text, 
                        key=f"select_dept_{dept_key}", 
                        use_container_width=True,
                        type=button_type):
                st.session_state.selected_department = dept_key
                st.rerun()

# Utility functions (updated to use current data)
def calculate_operational_total():
    current_data = get_current_data()
    total = 0
    
    # Predefined services (IT)
    for service_key, data in st.session_state.operational_services.items():
        if data.get('selected', False) and data.get('users', 0) > 0:
            users = data.get('users', 0)
            actual_service_name = data.get('actual_service_name', '')
            is_new_implementation = data.get('new_implementation', False)
            
            # Check Oracle services
            if actual_service_name in current_data['ORACLE_SERVICES']:
                service_info = current_data['ORACLE_SERVICES'][actual_service_name]
                monthly_cost = service_info['price_per_user'] * users
                setup_cost = service_info['setup_cost'] if is_new_implementation else 0
                total += (monthly_cost * 12) + setup_cost
            # Check Microsoft services
            elif actual_service_name in current_data['MICROSOFT_SERVICES']:
                service_info = current_data['MICROSOFT_SERVICES'][actual_service_name]
                monthly_cost = service_info['price_per_user'] * users
                setup_cost = service_info['setup_cost'] if is_new_implementation else 0
                total += (monthly_cost * 12) + setup_cost
            # Check Other services
            elif actual_service_name in current_data['OTHER_SERVICES']:
                service_info = current_data['OTHER_SERVICES'][actual_service_name]
                monthly_cost = service_info['price_per_user'] * users
                setup_cost = service_info['setup_cost'] if is_new_implementation else 0
                total += (monthly_cost * 12) + setup_cost
            # Check Procurement services
            elif actual_service_name in current_data['PROCUREMENT_SERVICES']:
                service_info = current_data['PROCUREMENT_SERVICES'][actual_service_name]
                volume = data.get('volume', users)  # Use volume or users depending on service
                
                if 'price_per_user' in service_info:
                    monthly_cost = service_info['price_per_user'] * users
                    annual_cost = monthly_cost * 12
                elif 'price_per_transaction' in service_info:
                    annual_cost = service_info['price_per_transaction'] * volume
                elif 'price_per_supplier' in service_info:
                    annual_cost = service_info['price_per_supplier'] * volume
                elif 'price_per_contract' in service_info:
                    annual_cost = service_info['price_per_contract'] * volume
                elif 'price_per_event' in service_info:
                    annual_cost = service_info['price_per_event'] * volume
                else:
                    annual_cost = 0
                
                setup_cost = service_info['setup_cost'] if is_new_implementation else 0
                total += annual_cost + setup_cost
            # Check Facility & Safety services
            elif actual_service_name in current_data['FACILITY_SAFETY_SERVICES']:
                service_info = current_data['FACILITY_SAFETY_SERVICES'][actual_service_name]
                volume = data.get('volume', users)  # Use volume or users depending on service
                
                if 'price_per_user' in service_info:
                    monthly_cost = service_info['price_per_user'] * users
                    annual_cost = monthly_cost * 12
                elif 'price_per_employee' in service_info:
                    annual_cost = service_info['price_per_employee'] * volume
                elif 'price_per_sq_meter' in service_info:
                    annual_cost = service_info['price_per_sq_meter'] * volume
                elif 'price_per_access_point' in service_info:
                    annual_cost = service_info['price_per_access_point'] * volume
                elif 'price_per_location' in service_info:
                    annual_cost = service_info['price_per_location'] * volume
                elif 'price_per_monitoring_point' in service_info:
                    annual_cost = service_info['price_per_monitoring_point'] * volume
                elif 'price_per_asset' in service_info:
                    annual_cost = service_info['price_per_asset'] * volume
                elif 'price_per_vehicle' in service_info:
                    annual_cost = service_info['price_per_vehicle'] * volume
                else:
                    annual_cost = 0
                
                setup_cost = service_info['setup_cost'] if is_new_implementation else 0
                total += annual_cost + setup_cost
    
    # Custom services
    for custom_service in st.session_state.custom_operational:
        volume = custom_service.get('volume', custom_service.get('users', 0))
        price_per_unit = custom_service.get('price_per_user', custom_service.get('price_per_unit', 0))
        
        if custom_service.get('pricing_model') == 'monthly':
            annual_cost = price_per_unit * volume * 12
        else:
            annual_cost = price_per_unit * volume
            
        setup_cost = custom_service.get('setup_cost', 0) if custom_service.get('new_implementation', False) else 0
        total += annual_cost + setup_cost
    
    return total

def calculate_support_total():
    current_data = get_current_data()
    total = 0
    
    if st.session_state.support_package:
        total += current_data['SUPPORT_PACKAGES'][st.session_state.support_package]['price']
    
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
    selected_dept = st.session_state.selected_department
    app_mode = st.session_state.get('app_mode', 'client')
    
    if app_mode == 'admin':
        admin_info = st.session_state.get('admin_info', {})
        admin_name = admin_info.get('name', 'Administrator')
        
    st.markdown(f"""
    <div class='admin-header'>
        <h1>🔧 Alkhorayef Group</h1>
        <h2>2025 Shared Services Admin Panel</h2>
        <p>Complete Department Head Content Management System</p>
        <p><strong>Administrator:</strong> {admin_name} | <strong>Environment:</strong> Admin Mode</p>
        <div style='background: rgba(255,255,255,0.2); padding: 1rem; border-radius: 8px; margin-top: 1rem;'>
            <strong>🚀 FULL SYSTEM MANAGEMENT:</strong> Operational Services • Support Packages • Implementation Projects
        </div>
    </div>
    """, unsafe_allow_html=True)
    else:
        header_subtitle = "Multi-Department Shared Services Catalogue and Budgeting System"
        if selected_company_info and selected_dept:
            departments_config = get_departments_config()
            dept_name = departments_config[selected_dept]['title']
            header_subtitle = f"{selected_company_info} - {dept_name} - Shared Services Catalogue"
        elif selected_dept:
            departments_config = get_departments_config()
            dept_name = departments_config[selected_dept]['title']
            header_subtitle = f"{dept_name} - Shared Services Catalogue and Budgeting System"
        
        st.markdown(f"""
        <div class='main-header'>
            <h1>💼 Alkhorayef Group</h1>
            <h2>2025 Multi-Department Shared Services Catalogue</h2>
            <p>{header_subtitle}</p>
            <p><strong>Budget Year:</strong> 2025 | <strong>Version:</strong> 2.0 | <strong>Environment:</strong> Client Site</p>
        </div>
        """, unsafe_allow_html=True)

# Sidebar for company info and budget summary (updated for admin mode)
def show_sidebar():
    with st.sidebar:
        # Mode switcher at the top
        st.markdown("### 🔄 Application Mode")
        
        current_mode = st.session_state.get('app_mode', 'client')
        
        # Mode selection
        if current_mode == 'client':
            if st.button("🔧 Switch to Admin Mode", use_container_width=True, type="secondary"):
                st.session_state.app_mode = 'admin'
                st.session_state.admin_authenticated = False  # Require re-authentication
                st.rerun()
        else:
            col1, col2 = st.columns(2)
            with col1:
                if st.button("👥 Client Mode", use_container_width=True):
                    st.session_state.app_mode = 'client'
                    st.rerun()
            with col2:
                if st.button("🚪 Logout", use_container_width=True, type="secondary"):
                    st.session_state.admin_authenticated = False
                    st.session_state.app_mode = 'client'
                    st.rerun()
        
        st.markdown("---")
        
        # Show different content based on mode
        if st.session_state.get('app_mode', 'client') == 'admin':
            # Admin sidebar content
            if st.session_state.get('admin_authenticated', False):
                admin_info = st.session_state.get('admin_info', {})
                st.markdown(f"""
                **🔧 Admin Panel**  
                **User:** {admin_info.get('name', 'Admin')}  
                **Department:** {admin_info.get('department', 'N/A')}  
                **Access Level:** Department Head
                """)
                
                st.markdown("### 📊 System Status")
                current_data = get_current_data()
                
                # Comprehensive statistics for all 3 categories
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**🔧 Operational Services**")
                    total_operational = (len(current_data['ORACLE_SERVICES']) + 
                                       len(current_data['MICROSOFT_SERVICES']) + 
                                       len(current_data['OTHER_SERVICES']) + 
                                       len(current_data['PROCUREMENT_SERVICES']) + 
                                       len(current_data['FACILITY_SAFETY_SERVICES']))
                    st.metric("Total Services", total_operational)
                
                with col2:
                    st.markdown("**🛠️ Support Packages**")
                    st.metric("Packages", len(current_data['SUPPORT_PACKAGES']))
                
                st.markdown("**🚀 Implementation Projects**")
                col1, col2 = st.columns(2)
                
                with col1:
                    total_categories = (len(current_data['IT_PROJECT_CATEGORIES']) + 
                                      len(current_data['PROCUREMENT_SERVICE_CATEGORIES']) + 
                                      len(current_data['FACILITY_SAFETY_SERVICE_CATEGORIES']))
                    st.metric("Project Categories", total_categories)
                
                with col2:
                    st.metric("RPA Packages", len(current_data['RPA_PACKAGES']))
                
                # Admin capabilities highlight
                st.markdown("---")
                st.markdown("""
                <div class='admin-warning'>
                    <strong>🚀 NEW: Full Implementation Management</strong><br>
                    ✅ Manage all 3 categories: Operational, Support & Implementation<br>
                    ✅ Add/Edit project categories for all departments<br>
                    ✅ Configure RPA packages with custom pricing<br>
                    ✅ Real-time updates to client interface
                </div>
                """, unsafe_allow_html=True)
                
            else:
                st.markdown("**🔐 Admin Access Required**")
                st.info("Please log in with your Department Head credentials to access the admin panel.")
                
                # Show demo credentials reminder
                with st.expander("🔑 Demo Access", expanded=False):
                    st.markdown("""
                    **Quick Demo Access:**
                    - IT: `it_admin` / `itadmin2025`
                    - Procurement: `procurement_admin` / `procadmin2025`
                    - Facility: `facility_admin` / `faciladmin2025`
                    - Super Admin: `super_admin` / `superadmin2025`
                    """)
        else:
            # Client sidebar content (existing functionality)
            st.markdown("### 🏢 Company Information")
            
            st.markdown("**🏭 Alkhorayef Group**")
            
            # Company selection
            selected_company = st.selectbox(
                "Select Your Company", 
                options=ALKHORAYEF_COMPANIES,
                index=0,
                key="company_selection",
                help="Choose which Alkhorayef Group company you represent"
            )
            
            # Department selection for the requester (not the shared service department)
            department = st.selectbox(
                "Your Department", 
                options=COMPANY_DEPARTMENTS,
                key="department_selection",
                help="Your department within the company"
            )
            
            contact_person = st.text_input("Contact Person", key="contact_person", placeholder="Your full name")
            email = st.text_input("Email", key="email", placeholder="your.email@alkhorayef.com")
            
            # Display selected company and shared service department
            if st.session_state.selected_department:
                departments_config = get_departments_config()
                dept_config = departments_config[st.session_state.selected_department]
                st.markdown(f"""
                <div style='background: #f0f9ff; border: 1px solid #0ea5e9; border-radius: 8px; padding: 1rem; margin: 0.5rem 0;'>
                    <strong>Company:</strong> {selected_company}<br>
                    <strong>Your Dept:</strong> {department}<br>
                    <strong>Shared Service:</strong> {dept_config['icon']} {dept_config['title']}
                </div>
                """, unsafe_allow_html=True)
                
                # Quick department switcher in sidebar
                if st.button("🔄 Change Department", key="sidebar_change_dept", use_container_width=True):
                    st.session_state.selected_department = None
                    st.rerun()
            
            st.session_state.company_info = {
                'company': selected_company,
                'company_code': selected_company,
                'department': department,
                'contact_person': contact_person,
                'email': email,
                'shared_service_dept': st.session_state.selected_department,
                'date': datetime.now().strftime("%Y-%m-%d")
            }
            
            if st.session_state.selected_department:
                st.markdown("---")
                
                # Budget summary
                departments_config = get_departments_config()
                dept_config = departments_config[st.session_state.selected_department]
                st.markdown(f"### 💰 {dept_config['title']} Budget Summary")
                
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
                    💰 Total 2025 Budget<br>
                    <span style='font-size: 1.5em'>SAR {total_budget:,.0f}</span>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("**🏭 Alkhorayef Group**")
            
            # Company selection
            selected_company = st.selectbox(
                "Select Your Company", 
                options=ALKHORAYEF_COMPANIES,
                index=0,
                key="company_selection",
                help="Choose which Alkhorayef Group company you represent"
            )
            
            # Department selection for the requester (not the shared service department)
            department = st.selectbox(
                "Your Department", 
                options=COMPANY_DEPARTMENTS,
                key="department_selection",
                help="Your department within the company"
            )
            
            contact_person = st.text_input("Contact Person", key="contact_person", placeholder="Your full name")
            email = st.text_input("Email", key="email", placeholder="your.email@alkhorayef.com")
            
            # Display selected company and shared service department
            if st.session_state.selected_department:
                departments_config = get_departments_config()
                dept_config = departments_config[st.session_state.selected_department]
                st.markdown(f"""
                <div style='background: #f0f9ff; border: 1px solid #0ea5e9; border-radius: 8px; padding: 1rem; margin: 0.5rem 0;'>
                    <strong>Company:</strong> {selected_company}<br>
                    <strong>Your Dept:</strong> {department}<br>
                    <strong>Shared Service:</strong> {dept_config['icon']} {dept_config['title']}
                </div>
                """, unsafe_allow_html=True)
                
                # Quick department switcher in sidebar
                if st.button("🔄 Change Department", key="sidebar_change_dept", use_container_width=True):
                    st.session_state.selected_department = None
                    st.rerun()
            
            st.session_state.company_info = {
                'company': selected_company,
                'company_code': selected_company,
                'department': department,
                'contact_person': contact_person,
                'email': email,
                'shared_service_dept': st.session_state.selected_department,
                'date': datetime.now().strftime("%Y-%m-%d")
            }
            
            if st.session_state.selected_department:
                st.markdown("---")
                
                # Budget summary
                departments_config = get_departments_config()
                dept_config = departments_config[st.session_state.selected_department]
                st.markdown(f"### 💰 {dept_config['title']} Budget Summary")
                
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
                    💰 Total 2025 Budget<br>
                    <span style='font-size: 1.5em'>SAR {total_budget:,.0f}</span>
                </div>
                """, unsafe_allow_html=True)

# Operational Services Section - Updated to use current data
def show_operational_services():
    if not st.session_state.selected_department:
        st.warning("Please select a department first from the Department Selection tab.")
        return
    
    departments_config = get_departments_config()
    dept_config = departments_config[st.session_state.selected_department]
    
    st.markdown(f"""
    <div class='category-section'>
        <h2>{dept_config['icon']} {dept_config['title']} - Operational Services</h2>
        <p>Select recurring licenses and software subscriptions for {dept_config['title']} operations.</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.selected_department == "IT":
        show_it_operational_services()
    elif st.session_state.selected_department == "Procurement":
        show_procurement_operational_services()
    elif st.session_state.selected_department == "Facility_Safety":
        show_facility_safety_operational_services()

def show_it_operational_services():
    current_data = get_current_data()
    
    # Oracle Services (using current data)
    st.markdown("### 🟠 Oracle Cloud Services")
    
    col1, col2 = st.columns(2)
    oracle_services = list(current_data['ORACLE_SERVICES'].items())
    
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
    
    # Other Services (using current data)
    st.markdown("### 🔧 Other Licenses & Services")
    
    col1, col2 = st.columns(2)
    other_services = list(current_data['OTHER_SERVICES'].items())
    
    for i, (service_name, details) in enumerate(other_services):
        col = col1 if i % 2 == 0 else col2
        service_key = f"other_{service_name.lower().replace(' ', '_').replace('&', 'and')}"
        
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
    
    # Microsoft Services (using current data)
    st.markdown("### 🟦 Microsoft Cloud Services")
    
    col1, col2 = st.columns(2)
    microsoft_services = list(current_data['MICROSOFT_SERVICES'].items())
    
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

def show_procurement_operational_services():
    current_data = get_current_data()
    
    # Procurement Services
    st.markdown("### 🛒 Procurement Services & Solutions")
    
    col1, col2 = st.columns(2)
    procurement_services = list(current_data['PROCUREMENT_SERVICES'].items())
    
    for i, (service_name, details) in enumerate(procurement_services):
        col = col1 if i % 2 == 0 else col2
        service_key = f"procurement_{service_name.lower().replace(' ', '_').replace('&', 'and')}"
        
        with col:
            # Determine pricing display based on service type
            if 'price_per_user' in details:
                pricing_text = f"SAR {details['price_per_user']}/user/month"
                volume_label = "Number of Users"
            elif 'price_per_transaction' in details:
                pricing_text = f"SAR {details['price_per_transaction']}/transaction/year"
                volume_label = "Annual Transactions"
            elif 'price_per_supplier' in details:
                pricing_text = f"SAR {details['price_per_supplier']}/supplier/year"
                volume_label = "Number of Suppliers"
            elif 'price_per_contract' in details:
                pricing_text = f"SAR {details['price_per_contract']}/contract/year"
                volume_label = "Annual Contracts"
            elif 'price_per_event' in details:
                pricing_text = f"SAR {details['price_per_event']}/event/year"
                volume_label = "Annual Sourcing Events"
            else:
                pricing_text = "Custom Pricing"
                volume_label = "Volume"
            
            st.markdown(f"""
            <div class='service-card procurement'>
                <h4>{service_name}</h4>
                <p style='color: #6b7280; font-size: 0.9em;'>{details['description']}</p>
                <div style='background: #f0fdf4; padding: 0.5rem; border-radius: 5px; margin: 0.5rem 0;'>
                    💰 {pricing_text}<br>
                    🆕 Setup (new implementation): SAR {details['setup_cost']:,}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Initialize service data if not exists
            if service_key not in st.session_state.operational_services:
                st.session_state.operational_services[service_key] = {
                    'selected': False, 
                    'users': 0,
                    'volume': 0,
                    'actual_service_name': service_name,
                    'new_implementation': False
                }
            
            # Get current values from session state
            current_selected = st.session_state.operational_services[service_key].get('selected', False)
            current_volume = st.session_state.operational_services[service_key].get('volume', 0)
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
                    help="Check this if it's a new implementation requiring setup."
                )
                
                # Volume input based on service type
                if 'price_per_user' in details:
                    volume = st.number_input(volume_label, 
                                          min_value=0, 
                                          value=current_users,
                                          key=f"{service_key}_volume",
                                          step=1)
                    users = volume
                else:
                    volume = st.number_input(volume_label, 
                                          min_value=0, 
                                          value=current_volume,
                                          key=f"{service_key}_volume",
                                          step=1)
                    users = 0  # Not user-based
                
                # Update session state immediately
                st.session_state.operational_services[service_key] = {
                    'selected': True,
                    'users': users,
                    'volume': volume,
                    'actual_service_name': service_name,
                    'new_implementation': new_implementation
                }
                
                if volume > 0:
                    # Calculate cost based on pricing model
                    if 'price_per_user' in details:
                        monthly_cost = details['price_per_user'] * volume
                        annual_cost = monthly_cost * 12
                        cost_display = f"Monthly: SAR {monthly_cost:,.0f}"
                    elif 'price_per_transaction' in details:
                        annual_cost = details['price_per_transaction'] * volume
                        cost_display = f"Annual: SAR {annual_cost:,.0f}"
                    elif 'price_per_supplier' in details:
                        annual_cost = details['price_per_supplier'] * volume
                        cost_display = f"Annual: SAR {annual_cost:,.0f}"
                    elif 'price_per_contract' in details:
                        annual_cost = details['price_per_contract'] * volume
                        cost_display = f"Annual: SAR {annual_cost:,.0f}"
                    elif 'price_per_event' in details:
                        annual_cost = details['price_per_event'] * volume
                        cost_display = f"Annual: SAR {annual_cost:,.0f}"
                    else:
                        annual_cost = 0
                        cost_display = "Custom Pricing"
                    
                    setup_cost = details['setup_cost'] if new_implementation else 0
                    total_cost = annual_cost + setup_cost
                    
                    setup_text = f" + SAR {setup_cost:,} setup" if new_implementation else " (no setup cost)"
                    
                    st.markdown(f"""
                    <div class='cost-display procurement'>
                        📊 {cost_display}{setup_text}<br>
                        <strong>Total Annual Cost: SAR {total_cost:,.0f}</strong>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.session_state.operational_services[service_key] = {
                    'selected': False,
                    'users': 0,
                    'volume': 0,
                    'actual_service_name': service_name,
                    'new_implementation': False
                }
    
    # Show common custom services section
    show_custom_operational_services()

def show_facility_safety_operational_services():
    current_data = get_current_data()
    
    # Facility & Safety Services
    st.markdown("### 🏢 Facility & Safety Services & Solutions")
    
    col1, col2 = st.columns(2)
    facility_safety_services = list(current_data['FACILITY_SAFETY_SERVICES'].items())
    
    for i, (service_name, details) in enumerate(facility_safety_services):
        col = col1 if i % 2 == 0 else col2
        service_key = f"facility_safety_{service_name.lower().replace(' ', '_').replace('&', 'and')}"
        
        with col:
            # Determine pricing display based on service type
            if 'price_per_user' in details:
                pricing_text = f"SAR {details['price_per_user']}/user/month"
                volume_label = "Number of Users"
            elif 'price_per_employee' in details:
                pricing_text = f"SAR {details['price_per_employee']}/employee/year"
                volume_label = "Number of Employees"
            elif 'price_per_sq_meter' in details:
                pricing_text = f"SAR {details['price_per_sq_meter']}/sq meter/year"
                volume_label = "Square Meters"
            elif 'price_per_access_point' in details:
                pricing_text = f"SAR {details['price_per_access_point']}/access point/year"
                volume_label = "Number of Access Points"
            elif 'price_per_location' in details:
                pricing_text = f"SAR {details['price_per_location']}/location/year"
                volume_label = "Number of Locations"
            elif 'price_per_monitoring_point' in details:
                pricing_text = f"SAR {details['price_per_monitoring_point']}/monitoring point/year"
                volume_label = "Number of Monitoring Points"
            elif 'price_per_asset' in details:
                pricing_text = f"SAR {details['price_per_asset']}/asset/year"
                volume_label = "Number of Assets"
            elif 'price_per_vehicle' in details:
                pricing_text = f"SAR {details['price_per_vehicle']}/vehicle/year"
                volume_label = "Number of Vehicles"
            else:
                pricing_text = "Custom Pricing"
                volume_label = "Volume"
            
            st.markdown(f"""
            <div class='service-card' style='border-left: 4px solid #f59e0b;'>
                <h4>{service_name}</h4>
                <p style='color: #6b7280; font-size: 0.9em;'>{details['description']}</p>
                <div style='background: #fffbeb; padding: 0.5rem; border-radius: 5px; margin: 0.5rem 0;'>
                    💰 {pricing_text}<br>
                    🆕 Setup (new implementation): SAR {details['setup_cost']:,}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Initialize service data if not exists
            if service_key not in st.session_state.operational_services:
                st.session_state.operational_services[service_key] = {
                    'selected': False, 
                    'users': 0,
                    'volume': 0,
                    'actual_service_name': service_name,
                    'new_implementation': False
                }
            
            # Get current values from session state
            current_selected = st.session_state.operational_services[service_key].get('selected', False)
            current_volume = st.session_state.operational_services[service_key].get('volume', 0)
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
                    help="Check this if it's a new implementation requiring setup."
                )
                
                # Volume input based on service type
                if 'price_per_user' in details:
                    volume = st.number_input(volume_label, 
                                          min_value=0, 
                                          value=current_users,
                                          key=f"{service_key}_volume",
                                          step=1)
                    users = volume
                else:
                    volume = st.number_input(volume_label, 
                                          min_value=0, 
                                          value=current_volume,
                                          key=f"{service_key}_volume",
                                          step=1)
                    users = 0  # Not user-based
                
                # Update session state immediately
                st.session_state.operational_services[service_key] = {
                    'selected': True,
                    'users': users,
                    'volume': volume,
                    'actual_service_name': service_name,
                    'new_implementation': new_implementation
                }
                
                if volume > 0:
                    # Calculate cost based on pricing model
                    if 'price_per_user' in details:
                        monthly_cost = details['price_per_user'] * volume
                        annual_cost = monthly_cost * 12
                        cost_display = f"Monthly: SAR {monthly_cost:,.0f}"
                    elif 'price_per_employee' in details:
                        annual_cost = details['price_per_employee'] * volume
                        cost_display = f"Annual: SAR {annual_cost:,.0f}"
                    elif 'price_per_sq_meter' in details:
                        annual_cost = details['price_per_sq_meter'] * volume
                        cost_display = f"Annual: SAR {annual_cost:,.0f}"
                    elif 'price_per_access_point' in details:
                        annual_cost = details['price_per_access_point'] * volume
                        cost_display = f"Annual: SAR {annual_cost:,.0f}"
                    elif 'price_per_location' in details:
                        annual_cost = details['price_per_location'] * volume
                        cost_display = f"Annual: SAR {annual_cost:,.0f}"
                    elif 'price_per_monitoring_point' in details:
                        annual_cost = details['price_per_monitoring_point'] * volume
                        cost_display = f"Annual: SAR {annual_cost:,.0f}"
                    elif 'price_per_asset' in details:
                        annual_cost = details['price_per_asset'] * volume
                        cost_display = f"Annual: SAR {annual_cost:,.0f}"
                    elif 'price_per_vehicle' in details:
                        annual_cost = details['price_per_vehicle'] * volume
                        cost_display = f"Annual: SAR {annual_cost:,.0f}"
                    else:
                        annual_cost = 0
                        cost_display = "Custom Pricing"
                    
                    setup_cost = details['setup_cost'] if new_implementation else 0
                    total_cost = annual_cost + setup_cost
                    
                    setup_text = f" + SAR {setup_cost:,} setup" if new_implementation else " (no setup cost)"
                    
                    st.markdown(f"""
                    <div class='cost-display' style='background: #fffbeb; border-color: #f59e0b;'>
                        📊 {cost_display}{setup_text}<br>
                        <strong>Total Annual Cost: SAR {total_cost:,.0f}</strong>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.session_state.operational_services[service_key] = {
                    'selected': False,
                    'users': 0,
                    'volume': 0,
                    'actual_service_name': service_name,
                    'new_implementation': False
                }
    
    # Show common custom services section
    show_custom_operational_services()

def show_custom_operational_services():
    st.markdown("---")
    st.markdown("### ➕ Add Custom Services")
    
    with st.expander("Add Custom Operational Service", expanded=False):
        departments_config = get_departments_config()
        dept_config = departments_config[st.session_state.selected_department]
        
        st.markdown(f"""
        <div class='custom-service'>
            <h4>Define Your Custom {dept_config['title']} Service</h4>
            <p>Add any additional operational software or service not listed above.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            custom_name = st.text_input("Service Name", placeholder="e.g., Custom Solution", key="custom_service_name_input")
            
            # Pricing model selection
            pricing_model = st.selectbox(
                "Pricing Model", 
                ["per_user_monthly", "per_transaction_annual", "per_unit_annual", "fixed_annual"],
                format_func=lambda x: {
                    "per_user_monthly": "Per User/Month",
                    "per_transaction_annual": "Per Transaction/Year", 
                    "per_unit_annual": "Per Unit/Year",
                    "fixed_annual": "Fixed Annual"
                }[x],
                key="custom_pricing_model_input"
            )
            
            # Dynamic pricing input based on model
            if pricing_model == "per_user_monthly":
                custom_price = st.number_input("Price per User/Month (SAR)", min_value=0, value=50, key="custom_service_price_input")
                volume_label = "Number of Users"
            elif pricing_model == "per_transaction_annual":
                custom_price = st.number_input("Price per Transaction/Year (SAR)", min_value=0, value=25, key="custom_service_price_input")
                volume_label = "Annual Transactions"
            elif pricing_model == "per_unit_annual":
                custom_price = st.number_input("Price per Unit/Year (SAR)", min_value=0, value=100, key="custom_service_price_input")
                volume_label = "Annual Units"
            else:  # fixed_annual
                custom_price = st.number_input("Fixed Annual Price (SAR)", min_value=0, value=50000, key="custom_service_price_input")
                volume_label = "Quantity (usually 1)"
        
        with col2:
            custom_setup = st.number_input("Setup Cost (SAR)", min_value=0, value=5000, key="custom_service_setup_input")
            custom_volume = st.number_input(volume_label, min_value=0, value=1, key="custom_service_volume_input")
        
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
            if custom_name and custom_description and custom_volume > 0:
                custom_service = {
                    'name': custom_name,
                    'description': custom_description,
                    'price_per_unit': custom_price,
                    'setup_cost': custom_setup,
                    'volume': custom_volume,
                    'pricing_model': pricing_model,
                    'new_implementation': custom_new_implementation,
                    'department': st.session_state.selected_department
                }
                
                st.session_state.custom_operational.append(custom_service)
                st.success(f"✅ Added custom service: {custom_name}")
                st.rerun()
            else:
                st.error("Please fill in all required fields and specify volume.")
    
    # Display custom services
    if st.session_state.custom_operational:
        # Filter custom services by current department
        dept_custom_services = [
            service for service in st.session_state.custom_operational 
            if service.get('department') == st.session_state.selected_department
        ]
        
        if dept_custom_services:
            st.markdown("### 📋 Your Custom Services")
            
            for i, service in enumerate(dept_custom_services):
                # Find original index
                original_index = st.session_state.custom_operational.index(service)
                
                volume = service.get('volume', 0)
                price_per_unit = service.get('price_per_unit', 0)
                pricing_model = service.get('pricing_model', 'per_user_monthly')
                
                if pricing_model == 'per_user_monthly':
                    monthly_cost = price_per_unit * volume
                    annual_cost = monthly_cost * 12
                    cost_display = f"Monthly: SAR {monthly_cost:,.0f}"
                else:
                    annual_cost = price_per_unit * volume
                    cost_display = f"Annual: SAR {annual_cost:,.0f}"
                
                setup_cost = service['setup_cost'] if service.get('new_implementation', False) else 0
                total_cost = annual_cost + setup_cost
                
                implementation_status = "New Implementation" if service.get('new_implementation', False) else "Adding to Existing"
                setup_display = f"Setup: SAR {setup_cost:,}" if service.get('new_implementation', False) else "No Setup Cost"
                
                departments_config = get_departments_config()
                dept_config = departments_config[st.session_state.selected_department]
                
                st.markdown(f"""
                <div class='service-card' style='border-left: 4px solid {dept_config["color"]};'>
                    <h4>{service['name']} (Custom {dept_config['title']})</h4>
                    <p style='color: #6b7280;'>{service['description']}</p>
                    <p><strong>Volume:</strong> {volume} | <strong>Status:</strong> {implementation_status}</p>
                    <p><strong>{cost_display}</strong> | <strong>{setup_display}</strong> | <strong>Total Annual:</strong> SAR {total_cost:,.0f}</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Remove {service['name']}", key=f"remove_custom_service_{original_index}"):
                    st.session_state.custom_operational.pop(original_index)
                    st.rerun()

# Support Packages Section (updated to use current data)
def show_support_packages():
    if not st.session_state.selected_department:
        st.warning("Please select a department first from the Department Selection tab.")
        return
    
    departments_config = get_departments_config()
    dept_config = departments_config[st.session_state.selected_department]
    current_data = get_current_data()
    
    st.markdown(f"""
    <div class='category-section'>
        <h2>{dept_config['icon']} {dept_config['title']} - Support Packages</h2>
        <p>Choose the support level that best fits your {dept_config['title']} needs.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📞 Support Packages Comparison")
    
    # Create comparison using Streamlit's native dataframe
    packages_list = list(current_data['SUPPORT_PACKAGES'].items())
    
    # Filter packages that support the current department
    available_packages = [
        (name, details) for name, details in packages_list 
        if st.session_state.selected_department in details.get('departments', [])
    ]
    
    if not available_packages:
        st.warning(f"No support packages available for {dept_config['title']} department yet.")
        return
    
    # Create comparison data
    comparison_data = {
        'Features': [
            '🔧 Systems Operation',
            '🛠️ Support Requests (Standard)',
            '🔥 Support Requests (Priority)', 
            '⭐ Support Requests (Premium)',
            '📊 Total Support Requests',
            '🔧 System Improvement Hours',
            '🎓 Training Requests',
            '📋 New Reports Requests',
            '💰 Total Package Cost (SAR)',
        ]
    }
    
    # Add data for each available package
    for package_name, details in available_packages:
        comparison_data[package_name] = [
            details['systems_operation'],
            details['support_requests_standard'],
            details['support_requests_priority'],
            details['support_requests_premium'],
            details['total_support_requests'],
            details['improvement_hours'],
            details['training_requests'],
            details['report_requests'],
            f"SAR {details['price']:,.0f}"
        ]
    
    # Create and display the comparison dataframe
    df = pd.DataFrame(comparison_data)
    
    # Style the dataframe to highlight selected package
    def highlight_selected(col):
        if st.session_state.support_package and col.name == st.session_state.support_package:
            return ['background-color: #fef2f2; border: 2px solid #dc2626'] * len(col)
        return [''] * len(col)
    
    styled_df = df.style.apply(highlight_selected, axis=0)
    st.dataframe(styled_df, use_container_width=True)
    
    # Package selection section
    st.markdown("### 🎯 Select Your Support Package")
    
    # Create selection cards using columns
    cols = st.columns(len(available_packages))
    
    package_colors = {
        "Basic": "#6b7280",
        "Bronze": "#92400e", 
        "Silver": "#374151",
        "Gold": "#d97706",
        "Platinum": "#1e293b"
    }
    
    for i, (package_name, details) in enumerate(available_packages):
        with cols[i]:
            is_selected = st.session_state.support_package == package_name
            color = package_colors.get(package_name, "#6b7280")
            
            # Package summary card
            bg_color = "#fef2f2" if is_selected else "#f8fafc"
            border_color = "#dc2626" if is_selected else color
            
            st.markdown(f"""
            <div style='
                background: {bg_color}; 
                border: 3px solid {border_color}; 
                border-radius: 12px; 
                padding: 1rem; 
                text-align: center;
                margin-bottom: 1rem;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            '>
                <h4 style='color: {color}; margin: 0 0 0.5rem 0;'>{package_name}</h4>
                <h3 style='color: #dc2626; margin: 0 0 0.5rem 0; font-size: 1.5rem;'>SAR {details["price"]:,.0f}</h3>
                <p style='font-size: 0.85em; color: #6b7280; margin: 0; line-height: 1.3;'>{details["description"]}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Key highlights
            st.markdown(f"""
            **📊 Total Requests:** {details['total_support_requests']}  
            **🔧 Improvement Hours:** {details['improvement_hours']}  
            **🎓 Training:** {details['training_requests']}  
            **📋 Reports:** {details['report_requests']}
            """)
            
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
    
    # Additional services section (same as before)
    if st.session_state.support_package:
        st.markdown("---")
        st.markdown("### ➕ Additional Support Services")
        st.markdown("Enhance your selected package with additional services as needed.")
        
        # Additional services pricing table
        additional_services_data = {
            'Additional Service': [
                '🛠️ Extra Support Request',
                '🎓 Extra Training Request', 
                '📋 Extra Report Request'
            ],
            'Cost (SAR)': [1800, 5399, 5399],
            'Available': ['✅ All Packages', '✅ All Packages', '✅ All Packages']
        }
        
        st.dataframe(pd.DataFrame(additional_services_data), use_container_width=True)
        
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
                "📋 Extra Report Requests", 
                min_value=0, 
                value=st.session_state.support_extras.get('reports', 0),
                key="extra_reports_requests_input"
            )
            st.session_state.support_extras['reports'] = extra_reports
        
        # Calculate and display total cost
        selected_package = current_data['SUPPORT_PACKAGES'][st.session_state.support_package]
        base_cost = selected_package['price']
        extra_support_cost = extra_support * 1800
        extra_training_cost = extra_training * 5399
        extra_reports_cost = extra_reports * 5399
        total_extra_cost = extra_support_cost + extra_training_cost + extra_reports_cost
        total_cost = base_cost + total_extra_cost
        
        # Cost summary
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Base Package Cost", f"SAR {base_cost:,.0f}")
            if extra_support > 0:
                st.metric("Extra Support", f"SAR {extra_support_cost:,.0f}", f"{extra_support} × SAR 1,800")
        
        with col2:
            st.metric("Additional Services", f"SAR {total_extra_cost:,.0f}")
            if extra_training > 0:
                st.metric("Extra Training", f"SAR {extra_training_cost:,.0f}", f"{extra_training} × SAR 5,399")
            if extra_reports > 0:
                st.metric("Extra Reports", f"SAR {extra_reports_cost:,.0f}", f"{extra_reports} × SAR 5,399")
        
        # Total cost display
        st.markdown(f"""
        <div style='
            background: linear-gradient(135deg, #fef3c7 0%, #fcd34d 100%); 
            border: 3px solid #f59e0b; 
            border-radius: 16px; 
            padding: 2rem; 
            text-align: center;
            margin: 2rem 0;
            box-shadow: 0 8px 25px rgba(245, 158, 11, 0.3);
        '>
            <h2 style='margin: 0; color: #92400e;'>💰 Total Support Cost</h2>
            <h1 style='margin: 0.5rem 0 0 0; color: #dc2626; font-size: 2.5rem;'>SAR {total_cost:,.0f}</h1>
            <p style='margin: 0; color: #92400e; font-weight: 600;'>
                {st.session_state.support_package} Package + Additional Services
            </p>
        </div>
        """, unsafe_allow_html=True)
        
    else:
        st.info("👆 Please select a support package from the comparison table above to continue.")

# Implementation Projects Section with Enhanced Categories (updated to use current data)
def show_implementation_projects():
    if not st.session_state.selected_department:
        st.warning("Please select a department first from the Department Selection tab.")
        return
    
    departments_config = get_departments_config()
    dept_config = departments_config[st.session_state.selected_department]
    current_data = get_current_data()
    
    st.markdown(f"""
    <div class='category-section'>
        <h2>{dept_config['icon']} {dept_config['title']} - Custom Implementation Projects</h2>
        <p>Define your strategic {dept_config['title'].lower()} initiatives and custom development projects.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Add new project form
    st.markdown("### ➕ Add New Implementation Project")
    
    with st.expander("Define New Project", expanded=True):
        st.markdown(f"""
        <div class='project-card'>
            <h4>{dept_config['title']} Project Details</h4>
            <p>Provide comprehensive information about your {dept_config['title'].lower()} implementation project.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            project_name = st.text_input("Project Name", placeholder=f"e.g., {dept_config['title']} Enhancement Platform", key="project_name_input")
            
            # Enhanced project type selection with categories
            st.markdown("#### Select Project Category & Type")
            st.markdown(f"""
            <div class='category-selector'>
                <p style='margin-bottom: 0.5rem; font-weight: 500;'>Choose from {dept_config['title']} service categories:</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Category selection based on department
            project_categories = dept_config['project_categories']
            selected_category = st.selectbox(
                "Project Category", 
                options=list(project_categories.keys()),
                key="project_category_input",
                help="Select the main category for your project"
            )
            
            # Service type based on selected category
            project_type = st.selectbox(
                "Specific Service Type", 
                options=project_categories[selected_category],
                key="project_type_input",
                help=f"Select the specific service within {selected_category}"
            )
            
            timeline = st.selectbox("Timeline", ["Q1 2025", "Q2 2025", "Q3 2025", "Q4 2025", "Multi-quarter", "2+ years"], key="project_timeline_input")
            priority = st.select_slider("Priority Level", ["Low", "Medium", "High", "Critical"], value="Medium", key="project_priority_input")
        
        with col2:
            budget = st.number_input("Budget Estimate (SAR)", min_value=0, value=100000, step=10000, key="project_budget_input")
            departments = st.multiselect("Departments Involved", COMPANY_DEPARTMENTS, key="project_departments_input")
            
            # Show category description based on department
            if st.session_state.selected_department == "IT":
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
            elif st.session_state.selected_department == "Procurement":
                category_descriptions = {
                    "🛒 Purchase Order Management": "Streamline purchase-to-pay processes and order management",
                    "🤝 Supplier & Vendor Management": "Enhance supplier relationships and performance management",
                    "📋 Master Data Management": "Improve data quality and standardization across procurement",
                    "📄 Contract Management": "Optimize contract lifecycle and compliance management",
                    "🚚 Logistics & Delivery": "Enhance logistics coordination and delivery management",
                    "💰 Payment & Financial Processing": "Streamline payment processes and financial coordination",
                    "📊 Sourcing & RFQ Management": "Improve sourcing strategies and competitive bidding",
                    "🎓 Training & Development": "Enhance procurement team capabilities and knowledge",
                    "🔍 Audit & Compliance": "Strengthen audit processes and regulatory compliance",
                    "📞 Support & Communication": "Improve stakeholder communication and support services"
                }
            elif st.session_state.selected_department == "Facility_Safety":
                category_descriptions = {
                    "🏢 Facility Management & Operations": "Optimize building operations, maintenance, and space utilization",
                    "🔒 Security & Access Control": "Enhance physical security and access management systems",
                    "⚠️ Safety & Compliance": "Improve workplace safety and regulatory compliance management",
                    "🚨 Emergency Management": "Strengthen emergency response and business continuity planning",
                    "🌡️ Environmental & Health": "Monitor environmental conditions and occupational health",
                    "🔧 Asset & Equipment Management": "Optimize asset lifecycle and maintenance operations",
                    "🚗 Transportation & Fleet": "Manage vehicle fleet and transportation operations",
                    "📋 Documentation & Reporting": "Streamline safety documentation and compliance reporting",
                    "👷 Contractor & Vendor Management": "Ensure contractor safety compliance and performance",
                    "📊 Safety Analytics & Reporting": "Analyze safety performance and generate insights"
                }
            else:
                category_descriptions = {}
            
            if selected_category in category_descriptions:
                st.info(f"**{selected_category}**: {category_descriptions[selected_category]}")
            
        project_description = st.text_area("Project Description", 
                                         placeholder="Describe the project scope, objectives, and expected outcomes...", 
                                         key="project_description_input")
        
        success_criteria = st.text_area("Success Criteria", 
                                      placeholder="Define how success will be measured...", 
                                      key="project_success_criteria_input")
        
        # Special handling for RPA projects (IT department only)
        if st.session_state.selected_department == "IT" and project_type == "RPA (Robotic Process Automation)":
            st.markdown("#### 🤖 RPA Package Selection")
            st.info("For RPA projects, you can select from our predefined packages or specify a custom budget.")
            
            use_rpa_package = st.checkbox("Use Predefined RPA Package", key="use_rpa_package_input")
            
            if use_rpa_package:
                rpa_package = st.selectbox("Select RPA Package", list(current_data['RPA_PACKAGES'].keys()), key="rpa_package_selection")
                
                if rpa_package:
                    package_details = current_data['RPA_PACKAGES'][rpa_package]
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
                    'created_date': datetime.now().strftime("%Y-%m-%d"),
                    'shared_service_dept': st.session_state.selected_department
                }
                
                # Add RPA package details if applicable
                if (st.session_state.selected_department == "IT" and 
                    project_type == "RPA (Robotic Process Automation)" and 
                    'use_rpa_package_input' in st.session_state and 
                    st.session_state['use_rpa_package_input']):
                    if 'rpa_package_selection' in st.session_state:
                        rpa_package = st.session_state['rpa_package_selection']
                        new_project['rpa_package'] = True
                        new_project['rpa_details'] = current_data['RPA_PACKAGES'][rpa_package]
                        new_project['rpa_package_name'] = rpa_package
                
                st.session_state.implementation_projects.append(new_project)
                st.success(f"✅ Added project: {project_name}")
                st.rerun()
            else:
                st.error("Please fill in project name, description, and budget.")
    
    # Display existing projects for current department
    dept_projects = [
        project for project in st.session_state.implementation_projects 
        if project.get('shared_service_dept') == st.session_state.selected_department
    ]
    
    if dept_projects:
        st.markdown(f"### 📋 Your {dept_config['title']} Implementation Projects")
        
        total_implementation_budget = 0
        
        # Group projects by category for better organization
        projects_by_category = {}
        for project in dept_projects:
            category = project.get('category', '⚙️ Custom & Specialized')
            if category not in projects_by_category:
                projects_by_category[category] = []
            projects_by_category[category].append(project)
        
        for category, projects in projects_by_category.items():
            st.markdown(f"#### {category}")
            
            for project in projects:
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
            💰 Total {dept_config['title']} Implementation Budget: <strong>SAR {total_implementation_budget:,.0f}</strong>
        </div>
        """, unsafe_allow_html=True)

# Summary Section with Multi-Department Support (updated to use current data)
def show_summary():
    if not st.session_state.selected_department:
        st.warning("Please select a department first from the Department Selection tab.")
        return
    
    departments_config = get_departments_config()
    dept_config = departments_config[st.session_state.selected_department]
    
    st.markdown(f"""
    <div class='category-section'>
        <h2>{dept_config['icon']} {dept_config['title']} - Service Catalogue Summary & Budget Analysis</h2>
        <p>Comprehensive overview of your 2025 {dept_config['title'].lower()} shared services selection and investment strategy.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Calculate totals
    operational_total = calculate_operational_total()
    support_total = calculate_support_total()
    implementation_total = calculate_implementation_total()
    total_budget = operational_total + support_total + implementation_total
    
    if total_budget == 0:
        st.info(f"👋 No {dept_config['title'].lower()} services selected yet. Please visit the other sections to build your shared services selection.")
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
            💰 Total 2025 {dept_config['title']} Budget<br>
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
                title=f"2025 {dept_config['title']} Budget Distribution",
                color_discrete_map={
                    'Operational Services': dept_config['color'],
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
                # Only include projects for current department
                if project.get('shared_service_dept') == st.session_state.selected_department:
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
        fig_bar.add_trace(go.Bar(name='Operational (Year-end)', x=months, y=monthly_operational, marker_color=dept_config['color']))
        fig_bar.add_trace(go.Bar(name='Support (Year-end)', x=months, y=monthly_support, marker_color='#10b981'))
        fig_bar.add_trace(go.Bar(name='Implementation (On Completion)', x=months, y=monthly_implementation, marker_color='#f59e0b'))
        
        fig_bar.update_layout(
            title=f'{dept_config["title"]} Monthly Cash Flow Projection (SAR)<br><sub>Support & Operations billed year-end | Projects billed on completion</sub>',
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
            st.success(f"📊 Excel export functionality would generate a comprehensive {dept_config['title'].lower()} budget report including all selected services, costs, and projections.")
    
    with col2:
        if st.button("💾 Save Draft", use_container_width=True, key="save_draft_btn"):
            st.success("💾 Draft saved! Your selections have been preserved and you can continue editing later.")
    
    with col3:
        if st.button("📧 Share Summary", use_container_width=True, key="share_summary_btn"):
            st.success(f"📧 {dept_config['title']} budget summary prepared for sharing with stakeholders and finance team.")
    
    with col4:
        if st.button("🚀 Submit Final Budget", type="primary", use_container_width=True, key="submit_final_budget_btn"):
            company_code = st.session_state.company_info.get('company_code', 'ALK')
            dept_code = st.session_state.selected_department[:3].upper()
            reference_id = f"{company_code}-{dept_code}-2025-{datetime.now().strftime('%Y%m%d%H%M%S')}-{str(uuid.uuid4())[:8].upper()}"
            
            st.balloons()
            st.success(f"""
            ✅ **2025 {dept_config['title']} Shared Service Selection Successfully Submitted!**
            
            **Reference ID:** {reference_id}
            
            **Submission Summary:**
            - Company: {st.session_state.company_info.get('company', 'N/A')}
            - Shared Service Department: {dept_config['title']}
            - Requesting Department: {st.session_state.company_info.get('department', 'N/A')}
            - Contact: {st.session_state.company_info.get('contact_person', 'N/A')}
            - Email: {st.session_state.company_info.get('email', 'N/A')}
            - Total Budget: SAR {total_budget:,.0f}
            - Operational Services: SAR {operational_total:,.0f}
            - Support Package: SAR {support_total:,.0f}
            - Implementation Projects: SAR {implementation_total:,.0f}
            
            **Next Steps:**
            1. {dept_config['title']} shared services team review (3-5 business days)
            2. Finance approval process
            3. Q4 2024: Service implementation planning begins
            4. Q1 2025: Service delivery starts
            
            A detailed {dept_config['title'].lower()} service catalogue report has been sent to your email and the shared services team.
            """)

# Main application
def main():
    # Initialize session state
    initialize_session_state()
    
    # Check application mode
    app_mode = st.session_state.get('app_mode', 'client')
    
    if app_mode == 'admin':
        # Admin mode
        if not st.session_state.get('admin_authenticated', False):
            show_admin_login()
        else:
            show_header()
            show_sidebar()
            show_admin_dashboard()
    else:
        # Client mode (existing functionality)
        show_header()
        show_sidebar()
        
        # Check if department is selected
        if not st.session_state.selected_department:
            show_department_selection()
        else:
            # Back button and department navigation
            departments_config = get_departments_config()
            dept_config = departments_config[st.session_state.selected_department]
            
            col1, col2, col3 = st.columns([1, 3, 1])
            
            with col1:
                if st.button("← Back to Departments", key="back_to_departments", help="Return to department selection"):
                    st.session_state.selected_department = None
                    st.rerun()
            
            with col2:
                st.markdown(f"""
                <div style='text-align: center; padding: 1rem; background: {dept_config['color']}20; border-radius: 8px; margin: 0.5rem 0;'>
                    <h3 style='margin: 0; color: {dept_config['color']};'>
                        {dept_config['icon']} {dept_config['title']} Shared Services
                    </h3>
                    <p style='margin: 0.5rem 0 0 0; color: #6b7280; font-size: 0.9em;'>
                        {dept_config['description']}
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                # Quick department switcher
                if st.button("🔄 Switch Department", key="switch_department", help="Quickly switch to another department"):
                    st.session_state.selected_department = None
                    st.rerun()
            
            # Navigation tabs
            tab1, tab2, tab3, tab4 = st.tabs([
                f"{dept_config['icon']} Operational Services", 
                "🛠️ Support Packages", 
                "🚀 Implementation Projects", 
                "📊 Summary"
            ])
            
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
