import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import re

# Page configuration
st.set_page_config(
    page_title="Group Shared Services Catalog",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for B2B service catalog styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #1f77b4, #2e86ab);
        color: white;
        margin: -1rem -1rem 2rem -1rem;
        border-radius: 0 0 20px 20px;
    }
    
    .service-dept-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border: 2px solid #f0f0f0;
        text-align: center;
        height: 350px;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        cursor: pointer;
        position: relative;
        margin: 1rem 0;
    }
    
    .service-dept-card:hover {
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
    
    .pricing-info {
        background: #e8f4fd;
        padding: 0.5rem;
        border-radius: 8px;
        font-size: 0.8rem;
        color: #1976d2;
        font-weight: bold;
        margin-top: 1rem;
    }
    
    .coming-soon-badge {
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
    
    .service-offering-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        margin: 15px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transition: transform 0.2s ease;
    }
    
    .service-offering-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    .pricing-badge {
        background: #28a745;
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: bold;
        display: inline-block;
        margin: 0.25rem 0;
    }
    
    .tier-standard { background: #28a745; }
    .tier-premium { background: #fd7e14; }
    .tier-enterprise { background: #6f42c1; }
    
    .budget-selection {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 2px solid #28a745;
    }
    
    .roi-highlight {
        background: linear-gradient(90deg, #e8f5e8, #f0f8f0);
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border-left: 4px solid #28a745;
    }
    
    .subsidiary-portal {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin: 20px 0;
    }
    
    .cost-calculator {
        background: #e3f2fd;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .service-tier-tabs {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for budget selections
if 'selected_services' not in st.session_state:
    st.session_state.selected_services = {}
if 'current_subsidiary' not in st.session_state:
    st.session_state.current_subsidiary = None
if 'budget_year' not in st.session_state:
    st.session_state.budget_year = 2025
if 'selected_department' not in st.session_state:
    st.session_state.selected_department = None

# Enhanced service offerings based on actual service data
@st.cache_data
def load_service_offerings():
    """Load comprehensive service offerings for subsidiaries based on real service catalog"""
    
    # IT Service Offerings - Based on actual Oracle Cloud Services (276 services)
    it_offerings = [
        {
            "service_name": "Oracle Fusion HCM Complete Suite",
            "category": "Human Capital Management",
            "description": "Comprehensive Human Capital Management platform including Absence Management, Human Capital Core, Payroll Processing, Performance Management, Goal Management, Learning Management, and Recruiting modules.",
            "business_value": "Streamline HR operations across all subsidiaries, reduce HR processing time by 60%, ensure global compliance, and improve employee experience with self-service capabilities.",
            "service_tiers": {
                "Essential": {"price_per_employee_monthly": 35, "features": "Core HCM, Absence, Basic Payroll, Self-Service Portal", "min_users": 100},
                "Professional": {"price_per_employee_monthly": 55, "features": "Full HCM Suite, Performance Management, Learning, Advanced Reporting", "min_users": 250},
                "Enterprise": {"price_per_employee_monthly": 75, "features": "Complete Platform, AI Insights, Custom Workflows, Integration Support", "min_users": 500}
            },
            "implementation_cost": 75000,
            "ongoing_support": "24/7 support, training, system enhancements, custom reporting",
            "contract_terms": "24-month minimum commitment for best rates",
            "target_subsidiaries": "All subsidiaries requiring comprehensive HR management",
            "roi_timeline": "ROI achieved within 12-18 months through automation and efficiency gains",
            "case_studies": "Regional subsidiary reduced HR operational costs by $400K annually and improved compliance by 95%",
            "service_owner": "Oracle HCM Center of Excellence",
            "available_regions": "Global with local compliance and language support"
        },
        {
            "service_name": "Oracle Fusion ERP Cloud Platform",
            "category": "Enterprise Resource Planning", 
            "description": "Complete ERP solution covering Financial Management, Supply Chain, Procurement, Project Management, and Business Intelligence with self-service capabilities for streamlined operations.",
            "business_value": "Unify business operations, reduce manual processes by 70%, improve financial reporting accuracy, and enable real-time business insights across all locations.",
            "service_tiers": {
                "Core": {"price_per_user_monthly": 150, "features": "Financial Management, Basic Procurement, Standard Reporting", "min_users": 25},
                "Advanced": {"price_per_user_monthly": 250, "features": "Full ERP Suite, Advanced Analytics, Mobile Access, Workflow Automation", "min_users": 50},
                "Premium": {"price_per_user_monthly": 350, "features": "Complete Platform, AI-powered Insights, Custom Integration, Dedicated Support", "min_users": 100}
            },
            "implementation_cost": 150000,
            "ongoing_support": "Comprehensive support including system administration, user training, and continuous optimization",
            "contract_terms": "36-month commitment recommended for complex implementations",
            "target_subsidiaries": "Medium to large subsidiaries requiring integrated business operations",
            "roi_timeline": "ROI achieved within 18-24 months through process automation and improved efficiency",
            "case_studies": "Manufacturing subsidiary achieved $800K savings annually through process automation and improved inventory management",
            "service_owner": "Oracle ERP Center of Excellence",
            "available_regions": "Global with local implementation teams"
        },
        {
            "service_name": "Oracle Fusion Talent Management Suite",
            "category": "Talent & Performance Management",
            "description": "Advanced talent management including Performance Management, Goal Management, Career Development, Succession Management, and Workforce Planning to optimize human capital.",
            "business_value": "Improve employee performance by 40%, increase retention rates by 25%, accelerate leadership development, and align workforce strategy with business goals.",
            "service_tiers": {
                "Standard": {"price_per_employee_monthly": 25, "features": "Performance Reviews, Goal Setting, Basic Analytics", "min_users": 200},
                "Professional": {"price_per_employee_monthly": 40, "features": "Complete Talent Suite, Succession Planning, Advanced Analytics", "min_users": 500},
                "Enterprise": {"price_per_employee_monthly": 60, "features": "Full Platform, AI-powered Insights, Strategic Workforce Planning", "min_users": 1000}
            },
            "implementation_cost": 50000,
            "ongoing_support": "Training programs, best practice guidance, and performance optimization",
            "contract_terms": "12-month minimum with annual reviews",
            "target_subsidiaries": "Organizations focused on talent development and performance management",
            "roi_timeline": "ROI achieved within 8-12 months through improved productivity and retention",
            "case_studies": "Service subsidiary improved performance ratings by 35% and reduced turnover by 20%",
            "service_owner": "Talent Management Center of Excellence",
            "available_regions": "Global"
        },
        {
            "service_name": "Oracle Learning & Development Platform",
            "category": "Learning Management",
            "description": "Comprehensive learning management system with course creation, skills tracking, certification management, and personalized learning paths for workforce development.",
            "business_value": "Accelerate employee skill development, ensure compliance training completion, reduce training costs by 50%, and improve knowledge retention through personalized learning.",
            "service_tiers": {
                "Basic": {"price_per_learner_monthly": 15, "features": "Course Library, Basic Tracking, Mobile Access", "min_users": 100},
                "Advanced": {"price_per_learner_monthly": 25, "features": "Custom Content Creation, Advanced Analytics, Certification Management", "min_users": 250},
                "Premium": {"price_per_learner_monthly": 35, "features": "AI-powered Recommendations, Skills Gap Analysis, Integration Support", "min_users": 500}
            },
            "implementation_cost": 25000,
            "ongoing_support": "Content development support, platform administration, and usage analytics",
            "contract_terms": "12-month commitment with content updates included",
            "target_subsidiaries": "Organizations requiring comprehensive training and development programs",
            "roi_timeline": "ROI achieved within 6-9 months through reduced training costs and improved productivity",
            "case_studies": "Technology subsidiary reduced training costs by 60% while improving skill competency scores by 45%",
            "service_owner": "Learning & Development Team",
            "available_regions": "Global with localized content"
        }
        {
            "service_name": "Enterprise IT Infrastructure Services",
            "category": "Infrastructure & Operations",
            "description": "Comprehensive IT infrastructure management including cloud hosting, security, backup, monitoring, and 24/7 support for your business operations.",
            "business_value": "Reduce IT infrastructure costs by 30%, achieve 99.9% uptime, eliminate need for in-house IT infrastructure team.",
            "service_tiers": {
                "Standard": {"price_per_user_monthly": 35, "features": "Basic Cloud Infrastructure, Email, Office Apps", "min_users": 25},
                "Premium": {"price_per_user_monthly": 55, "features": "Advanced Security, Backup, Monitoring, VPN", "min_users": 50},
                "Enterprise": {"price_per_user_monthly": 85, "features": "Custom Infrastructure, Advanced Analytics, Dedicated Support", "min_users": 200}
            },
            "implementation_cost": 75000,
            "ongoing_support": "24/7 NOC support included",
            "contract_terms": "24-month commitment recommended",
            "target_subsidiaries": "All subsidiaries requiring IT infrastructure",
            "roi_timeline": "ROI achieved within 6-9 months",
            "case_studies": "DEF Subsidiary eliminated $500K annual IT infrastructure costs",
            "service_owner": "Infrastructure Services Team",
            "available_regions": "Americas, EMEA, APAC"
        },
        {
            "service_name": "Digital Transformation Consulting",
            "category": "Strategic Consulting",
            "description": "Expert consulting services to digitize your business processes, implement automation, and optimize operations for competitive advantage.",
            "business_value": "Increase operational efficiency by 50%, reduce manual processes by 70%, accelerate digital adoption.",
            "service_tiers": {
                "Assessment": {"price_fixed": 25000, "features": "Digital Maturity Assessment, Roadmap Development", "duration": "4-6 weeks"},
                "Implementation": {"price_per_month": 50000, "features": "Process Digitization, System Integration, Training", "duration": "6-12 months"},
                "Transformation": {"price_per_month": 100000, "features": "Complete Digital Transformation, Change Management", "duration": "12-24 months"}
            },
            "implementation_cost": 0,
            "ongoing_support": "Quarterly reviews included",
            "contract_terms": "Project-based engagement",
            "target_subsidiaries": "Subsidiaries undergoing digital transformation",
            "roi_timeline": "ROI achieved within 12-18 months",
            "case_studies": "GHI Subsidiary achieved 200% ROI in 18 months",
            "service_owner": "Digital Transformation Office",
            "available_regions": "Global with local consultants"
        }
    ]
    
    # Procurement Service Offerings
    procurement_offerings = [
        {
            "service_name": "Strategic Sourcing & Procurement Services",
            "category": "Procurement Management",
            "description": "End-to-end procurement services including strategic sourcing, vendor management, contract negotiation, and procurement operations.",
            "business_value": "Achieve 15-25% cost savings, reduce procurement cycle time by 60%, ensure compliance and risk mitigation.",
            "service_tiers": {
                "Essential": {"price_percentage": 2.5, "features": "Basic Procurement Support, Vendor Management", "spend_threshold": 1000000},
                "Professional": {"price_percentage": 2.0, "features": "Strategic Sourcing, Contract Management, Analytics", "spend_threshold": 5000000},
                "Enterprise": {"price_percentage": 1.5, "features": "Complete Procurement Outsourcing, Advanced Analytics", "spend_threshold": 20000000}
            },
            "implementation_cost": 30000,
            "ongoing_support": "Dedicated procurement team",
            "contract_terms": "36-month commitment for best rates",
            "target_subsidiaries": "Subsidiaries with significant procurement spend",
            "roi_timeline": "Savings realized within 3-6 months",
            "case_studies": "JKL Subsidiary saved $2M annually on $10M spend",
            "service_owner": "Strategic Procurement Team",
            "available_regions": "Global with local sourcing expertise"
        },
        {
            "service_name": "Supplier Onboarding & Management Platform",
            "category": "Vendor Management",
            "description": "Comprehensive supplier lifecycle management including onboarding, performance monitoring, risk assessment, and compliance tracking.",
            "business_value": "Reduce supplier onboarding time by 80%, improve supplier performance by 40%, ensure 100% compliance.",
            "service_tiers": {
                "Standard": {"price_per_supplier": 50, "features": "Basic Onboarding, Performance Tracking", "max_suppliers": 500},
                "Premium": {"price_per_supplier": 35, "features": "Advanced Analytics, Risk Assessment, Integration", "max_suppliers": 2000},
                "Enterprise": {"price_per_supplier": 25, "features": "Custom Workflows, AI-powered Insights, Unlimited", "max_suppliers": "Unlimited"}
            },
            "implementation_cost": 15000,
            "ongoing_support": "Platform support and training included",
            "contract_terms": "12-month minimum commitment",
            "target_subsidiaries": "Subsidiaries with complex supplier networks",
            "roi_timeline": "ROI achieved within 4-6 months",
            "case_studies": "MNO Subsidiary reduced supplier management costs by 60%",
            "service_owner": "Vendor Management Platform Team",
            "available_regions": "Global platform with local compliance"
        }
    ]
    
    # Facilities Service Offerings
    facilities_offerings = [
        {
            "service_name": "Integrated Facilities Management",
            "category": "Facilities Operations",
            "description": "Complete facilities management including maintenance, security, cleaning, space planning, and asset management for your locations.",
            "business_value": "Reduce facilities costs by 25%, improve workplace satisfaction by 45%, ensure 99.5% service availability.",
            "service_tiers": {
                "Basic": {"price_per_sqft_monthly": 3.5, "features": "Basic Maintenance, Cleaning, Security", "min_sqft": 10000},
                "Comprehensive": {"price_per_sqft_monthly": 5.0, "features": "Full FM Services, Space Planning, Asset Management", "min_sqft": 25000},
                "Premium": {"price_per_sqft_monthly": 7.0, "features": "Concierge Services, Advanced Analytics, Sustainability", "min_sqft": 50000}
            },
            "implementation_cost": 25000,
            "ongoing_support": "24/7 service desk included",
            "contract_terms": "24-month commitment for optimal rates",
            "target_subsidiaries": "Subsidiaries with significant office space",
            "roi_timeline": "Savings realized immediately",
            "case_studies": "PQR Subsidiary reduced facilities costs by $300K annually",
            "service_owner": "Integrated Facilities Management Team",
            "available_regions": "Major metropolitan areas globally"
        },
        {
            "service_name": "Workplace Experience & Space Optimization",
            "category": "Workplace Strategy",
            "description": "Modern workplace design, space optimization, hybrid work solutions, and employee experience enhancement services.",
            "business_value": "Optimize space utilization by 40%, increase employee satisfaction by 50%, enable flexible work models.",
            "service_tiers": {
                "Assessment": {"price_fixed": 15000, "features": "Space Utilization Analysis, Recommendations", "duration": "2-4 weeks"},
                "Design": {"price_per_sqft": 25, "features": "Workplace Design, Technology Integration", "min_sqft": 5000},
                "Implementation": {"price_per_sqft": 75, "features": "Complete Workplace Transformation", "min_sqft": 10000}
            },
            "implementation_cost": 0,
            "ongoing_support": "Quarterly optimization reviews",
            "contract_terms": "Project-based with optional ongoing support",
            "target_subsidiaries": "Subsidiaries modernizing workplace strategies",
            "roi_timeline": "ROI achieved within 12-15 months through space savings",
            "case_studies": "STU Subsidiary reduced real estate footprint by 30%",
            "service_owner": "Workplace Strategy Team",
            "available_regions": "Global with local design partners"
        }
    ]
    
    return {
        'it_offerings': pd.DataFrame(it_offerings),
        'procurement_offerings': pd.DataFrame(procurement_offerings),
        'facilities_offerings': pd.DataFrame(facilities_offerings)
    }

# Service departments configuration for B2B catalog
service_departments = {
    "Information Technology": {
        "description": "Enterprise technology solutions, cloud services, digital transformation, and IT infrastructure management to accelerate your business growth and operational excellence.",
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
        "offerings_count": 15,
        "avg_implementation": "3-6 months",
        "pricing_model": "Per user/Per transaction",
        "global_availability": True,
        "avg_cost_savings": "25-40%"
    },
    "Procurement": {
        "description": "Strategic sourcing, vendor management, procurement operations, and supply chain optimization services to reduce costs and improve operational efficiency.",
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
        "offerings_count": 8,
        "avg_implementation": "2-4 months",
        "pricing_model": "% of spend/Fixed fee",
        "global_availability": True,
        "avg_cost_savings": "15-25%"
    },
    "Facilities": {
        "description": "Comprehensive facilities management, workplace strategy, space optimization, and corporate real estate services to create efficient and engaging work environments.",
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
        "offerings_count": 6,
        "avg_implementation": "1-3 months",
        "pricing_model": "Per sq ft/Per employee",
        "global_availability": True,
        "avg_cost_savings": "20-35%"
    },
    "Finance & Accounting": {
        "description": "Financial planning, accounting operations, treasury management, and business intelligence services to optimize financial performance and ensure compliance.",
        "icon": "💰",
        "color": "#ff7f0e",
        "offerings_count": "Coming Soon",
        "avg_implementation": "TBD",
        "pricing_model": "TBD", 
        "global_availability": False,
        "coming_soon": True
    },
    "Human Resources": {
        "description": "HR operations, talent management, payroll services, learning & development, and workforce analytics to optimize human capital management.",
        "icon": "🧑‍💼",
        "color": "#2ca02c",
        "offerings_count": "Coming Soon",
        "avg_implementation": "TBD",
        "pricing_model": "TBD",
        "global_availability": False,
        "coming_soon": True
    },
    "Legal & Compliance": {
        "description": "Legal advisory, contract management, regulatory compliance, and risk management services to support business operations and mitigate risks.",
        "icon": "⚖️",
        "color": "#8c564b",
        "offerings_count": "Coming Soon", 
        "avg_implementation": "TBD",
        "pricing_model": "TBD",
        "global_availability": False,
        "coming_soon": True
    }
}

# Load service offerings
service_offerings = load_service_offerings()

def show_main_catalog_page():
    """Main B2B service catalog page for subsidiaries"""
    
    # Header with value proposition
    st.markdown("""
    <div class='main-header'>
        <h1>🏢 Group Shared Services Catalog</h1>
        <p>Professional services for subsidiary companies • Budget Planning • Service Selection</p>
        <p><strong>Proven Results:</strong> 25% average cost reduction • 99.5% service availability • Global delivery</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Subsidiary selection and budget year
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        subsidiary_options = [
            "Select Your Subsidiary...",
            "ABC Manufacturing Ltd",
            "DEF Technology Inc", 
            "GHI Retail Corp",
            "JKL Energy Solutions",
            "MNO Financial Services",
            "PQR Healthcare Group"
        ]
        selected_subsidiary = st.selectbox("🏛️ Select Your Subsidiary", subsidiary_options)
        if selected_subsidiary != "Select Your Subsidiary...":
            st.session_state.current_subsidiary = selected_subsidiary
    
    with col2:
        budget_year = st.selectbox("📅 Budget Planning Year", [2024, 2025, 2026])
        st.session_state.budget_year = budget_year
    
    with col3:
        if st.session_state.current_subsidiary:
            st.metric("Your Current Selections", len(st.session_state.selected_services))
    
    with col4:
        if st.session_state.current_subsidiary:
            total_budget = sum([item.get('annual_cost', 0) for item in st.session_state.selected_services.values()])
            st.metric("Estimated Annual Cost", f"${total_budget:,.0f}")
    
    # Key value propositions
    st.markdown("### 🎯 Why Choose Group Shared Services?")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Average Cost Savings", "25%", "vs building in-house")
    with col2:
        st.metric("Service Availability", "99.5%", "SLA guaranteed")
    with col3:
        st.metric("Global Reach", "50+ Countries", "Local expertise")
    with col4:
        st.metric("Implementation Speed", "50% Faster", "vs traditional approaches")
    
    st.markdown("---")
    
    # Service department cards
    st.markdown("### 🛍️ Browse Our Service Offerings")
    col1, col2, col3 = st.columns(3)
    
    departments_list = list(service_departments.items())
    
    for i, (dept_name, dept_info) in enumerate(departments_list):
        col = [col1, col2, col3][i % 3]
        
        with col:
            # Create service department card
            coming_soon_badge = '<div class="coming-soon-badge">Coming Soon</div>' if dept_info.get("coming_soon", False) else ''
            
            # Handle both SVG and emoji icons
            if dept_info['icon'].startswith('<svg'):
                icon_display = dept_info['icon']
            else:
                icon_display = f"<div style='font-size: 4rem;'>{dept_info['icon']}</div>"
            
            # Pricing info for active departments
            pricing_html = ""
            if not dept_info.get("coming_soon", False):
                pricing_html = f"""
                <div class="pricing-info">
                    💰 {dept_info['pricing_model']}<br>
                    ⏱️ {dept_info['avg_implementation']} implementation<br>
                    💹 {dept_info['avg_cost_savings']} average savings
                </div>
                """
            
            card_html = f"""
            <div class="service-dept-card">
                {coming_soon_badge}
                <div class="dept-icon">{icon_display}</div>
                <div class="dept-title">{dept_name}</div>
                <div class="dept-description">{dept_info['description'][:140]}...</div>
                <p><strong>{dept_info['offerings_count']}</strong> available offerings</p>
                {pricing_html}
            </div>
            """
            
            st.markdown(card_html, unsafe_allow_html=True)
            
            # Browse button
            if dept_info.get("coming_soon", False):
                st.button(f"🚧 Coming Q3 2025", key=f"btn_{dept_name}", disabled=True, use_container_width=True)
            else:
                if st.button(f"🛍️ Browse {dept_name}", key=f"btn_{dept_name}", use_container_width=True):
                    st.session_state.selected_department = dept_name
                    st.rerun()

def show_service_offering_details(offering, idx, department):
    """Enhanced service offering card with pricing and selection options"""
    
    # Calculate pricing examples
    tiers = offering['service_tiers']
    tier_names = list(tiers.keys())
    
    with st.expander(f"🛍️ {offering['service_name']}", expanded=False):
        
        # Service overview
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"**📋 Service Description:**")
            st.write(offering['description'])
            
            st.markdown(f"**💼 Business Value & ROI:**")
            st.markdown(f'<div class="roi-highlight">{offering["business_value"]}</div>', unsafe_allow_html=True)
            st.write(f"**ROI Timeline:** {offering['roi_timeline']}")
            
        with col2:
            st.markdown("**📊 Service Details**")
            st.write(f"**Service Owner:** {offering['service_owner']}")
            st.write(f"**Target:** {offering['target_subsidiaries']}")
            st.write(f"**Global Availability:** {'✅ Yes' if offering['available_regions'] == 'Global' else offering['available_regions']}")
            st.write(f"**Contract Terms:** {offering['contract_terms']}")
            
            if offering.get('case_studies'):
                st.markdown("**🎯 Success Story:**")
                st.info(offering['case_studies'])
        
        # Service tiers and pricing
        st.markdown("### 💰 Service Tiers & Pricing")
        
        tier_tabs = st.tabs([f"📦 {tier}" for tier in tier_names])
        
        for i, (tier_name, tier_info) in enumerate(tiers.items()):
            with tier_tabs[i]:
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    st.write(f"**Features:** {tier_info['features']}")
                    
                    # Pricing display based on model
                    if 'price_per_employee_monthly' in tier_info:
                        st.write(f"**💰 Pricing:** ${tier_info['price_per_employee_monthly']}/employee/month")
                        st.write(f"**📊 Minimum:** {tier_info['min_users']} employees")
                        
                        # Cost calculator
                        st.markdown("**💡 Cost Calculator:**")
                        num_employees = st.number_input(f"Number of Employees ({tier_name})", 
                                                      min_value=tier_info['min_users'], 
                                                      value=tier_info['min_users'],
                                                      key=f"calc_{idx}_{tier_name}_emp")
                        monthly_cost = num_employees * tier_info['price_per_employee_monthly']
                        annual_cost = monthly_cost * 12 + offering['implementation_cost']
                        
                        st.metric("Monthly Cost", f"${monthly_cost:,.0f}")
                        st.metric("Annual Cost (incl. setup)", f"${annual_cost:,.0f}")
                        
                    elif 'price_per_user_monthly' in tier_info:
                        st.write(f"**💰 Pricing:** ${tier_info['price_per_user_monthly']}/user/month")
                        st.write(f"**📊 Minimum:** {tier_info['min_users']} users")
                        
                        num_users = st.number_input(f"Number of Users ({tier_name})", 
                                                   min_value=tier_info['min_users'], 
                                                   value=tier_info['min_users'],
                                                   key=f"calc_{idx}_{tier_name}_user")
                        monthly_cost = num_users * tier_info['price_per_user_monthly']
                        annual_cost = monthly_cost * 12 + offering['implementation_cost']
                        
                        st.metric("Monthly Cost", f"${monthly_cost:,.0f}")
                        st.metric("Annual Cost (incl. setup)", f"${annual_cost:,.0f}")
                        
                    elif 'price_percentage' in tier_info:
                        st.write(f"**💰 Pricing:** {tier_info['price_percentage']}% of procurement spend")
                        st.write(f"**📊 Minimum Spend:** ${tier_info['spend_threshold']:,.0f}/year")
                        
                        annual_spend = st.number_input(f"Annual Procurement Spend ({tier_name})", 
                                                      min_value=tier_info['spend_threshold'], 
                                                      value=tier_info['spend_threshold'],
                                                      key=f"calc_{idx}_{tier_name}_spend")
                        service_cost = annual_spend * (tier_info['price_percentage'] / 100)
                        total_cost = service_cost + offering['implementation_cost']
                        
                        st.metric("Annual Service Cost", f"${service_cost:,.0f}")
                        st.metric("Total Cost (incl. setup)", f"${total_cost:,.0f}")
                        
                    elif 'price_per_sqft_monthly' in tier_info:
                        st.write(f"**💰 Pricing:** ${tier_info['price_per_sqft_monthly']}/sq ft/month")
                        st.write(f"**📊 Minimum:** {tier_info['min_sqft']:,.0f} sq ft")
                        
                        sqft = st.number_input(f"Square Footage ({tier_name})", 
                                              min_value=tier_info['min_sqft'], 
                                              value=tier_info['min_sqft'],
                                              key=f"calc_{idx}_{tier_name}_sqft")
                        monthly_cost = sqft * tier_info['price_per_sqft_monthly']
                        annual_cost = monthly_cost * 12 + offering['implementation_cost']
                        
                        st.metric("Monthly Cost", f"${monthly_cost:,.0f}")
                        st.metric("Annual Cost (incl. setup)", f"${annual_cost:,.0f}")
                        
                    elif 'price_fixed' in tier_info:
                        st.write(f"**💰 Pricing:** ${tier_info['price_fixed']:,.0f} fixed")
                        st.write(f"**⏱️ Duration:** {tier_info.get('duration', 'As specified')}")
                        annual_cost = tier_info['price_fixed']
                        st.metric("Project Cost", f"${annual_cost:,.0f}")
                        
                    elif 'price_per_month' in tier_info:
                        st.write(f"**💰 Pricing:** ${tier_info['price_per_month']:,.0f}/month")
                        st.write(f"**⏱️ Duration:** {tier_info.get('duration', 'Ongoing')}")
                        
                        months = st.number_input(f"Project Duration (months) ({tier_name})", 
                                                min_value=1, value=12,
                                                key=f"calc_{idx}_{tier_name}_months")
                        total_cost = tier_info['price_per_month'] * months
                        st.metric("Total Project Cost", f"${total_cost:,.0f}")
                        annual_cost = total_cost
                
                with col2:
                    # Add to budget button
                    if st.button(f"➕ Add {tier_name} to Budget", key=f"add_{idx}_{tier_name}"):
                        service_key = f"{offering['service_name']}_{tier_name}"
                        st.session_state.selected_services[service_key] = {
                            'service': offering['service_name'],
                            'tier': tier_name,
                            'department': department,
                            'annual_cost': annual_cost,
                            'features': tier_info['features'],
                            'selected_date': datetime.now()
                        }
                        st.success(f"✅ Added {tier_name} tier to your budget!")
                
                with col3:
                    # Request consultation
                    if st.button(f"📞 Request Consultation", key=f"consult_{idx}_{tier_name}"):
                        st.info(f"""
                        **Consultation Requested for {tier_name}**
                        
                        Our specialist will contact you within 24 hours to discuss:
                        • Detailed requirements assessment
                        • Custom pricing options
                        • Implementation timeline
                        • Success metrics and ROI projections
                        """)

def show_offerings_catalog(department_name):
    """Show service offerings for a specific department"""
    
    dept_info = service_departments[department_name]
    
    # Back button
    col1, col2 = st.columns([1, 6])
    with col1:
        if st.button("← Back to Catalog", key="back_button"):
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
        st.markdown(f"<h1 style='color: {dept_info['color']};'>{department_name} Services</h1>", unsafe_allow_html=True)

    st.markdown(dept_info["description"])
    
    # Department value metrics
    st.markdown("<div class='metric-row'>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Available Offerings", dept_info["offerings_count"])
    with col2:
        st.metric("Avg Implementation", dept_info["avg_implementation"])
    with col3:
        st.metric("Pricing Model", dept_info["pricing_model"])
    with col4:
        st.metric("Avg Cost Savings", dept_info["avg_cost_savings"])
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("---")
    
    # Show selected services summary
    if st.session_state.selected_services:
        dept_selections = {k: v for k, v in st.session_state.selected_services.items() if v['department'] == department_name}
        if dept_selections:
            st.markdown("### 🛒 Your Current Selections")
            total_cost = sum([item['annual_cost'] for item in dept_selections.values()])
            st.success(f"**{len(dept_selections)} services selected** | **Annual Cost: ${total_cost:,.0f}**")
    
    # Service offerings tabs
    tab1, tab2, tab3 = st.tabs(["🛍️ Browse Services", "📊 Compare Options", "💰 Budget Summary"])
    
    with tab1:
        # Get offerings for this department
        dept_key = department_name.lower().replace(" ", "_")
        if f'{dept_key}_offerings' in service_offerings:
            df = service_offerings[f'{dept_key}_offerings']
            
            # Category-based display
            categories = df['category'].unique()
            
            for category in categories:
                st.markdown(f"### 📂 {category}")
                category_offerings = df[df['category'] == category]
                
                for idx, offering in category_offerings.iterrows():
                    show_service_offering_details(offering, idx, department_name)
    
    with tab2:
        st.subheader("📊 Service Comparison")
        
        if f'{dept_key}_offerings' in service_offerings:
            df = service_offerings[f'{dept_key}_offerings']
            
            # Create comparison table
            comparison_data = []
            for idx, offering in df.iterrows():
                tiers = offering['service_tiers']
                for tier_name, tier_info in tiers.items():
                    comparison_data.append({
                        'Service': offering['service_name'],
                        'Tier': tier_name,
                        'Features': tier_info['features'],
                        'ROI Timeline': offering['roi_timeline'],
                        'Implementation': offering['ongoing_support']
                    })
            
            comparison_df = pd.DataFrame(comparison_data)
            st.dataframe(comparison_df, use_container_width=True)
    
    with tab3:
        show_budget_summary()

def show_budget_summary():
    """Show budget summary and export options"""
    
    st.subheader("💰 Budget Planning Summary")
    
    if not st.session_state.selected_services:
        st.info("No services selected yet. Browse our offerings and add services to your budget.")
        return
    
    # Budget overview
    total_annual_cost = sum([item['annual_cost'] for item in st.session_state.selected_services.values()])
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Selected Services", len(st.session_state.selected_services))
    with col2:
        st.metric("Total Annual Cost", f"${total_annual_cost:,.0f}")
    with col3:
        estimated_savings = total_annual_cost * 0.25  # 25% average savings
        st.metric("Estimated Annual Savings", f"${estimated_savings:,.0f}", "vs building in-house")
    
    # Detailed breakdown
    st.markdown("### 📋 Selected Services Breakdown")
    
    budget_data = []
    for service_key, details in st.session_state.selected_services.items():
        budget_data.append({
            'Department': details['department'],
            'Service': details['service'],
            'Tier': details['tier'],
            'Features': details['features'],
            'Annual Cost': f"${details['annual_cost']:,.0f}",
            'Selected Date': details['selected_date'].strftime('%Y-%m-%d')
        })
    
    budget_df = pd.DataFrame(budget_data)
    st.dataframe(budget_df, use_container_width=True)
    
    # Department breakdown chart
    if len(st.session_state.selected_services) > 0:
        dept_costs = {}
        for details in st.session_state.selected_services.values():
            dept = details['department']
            dept_costs[dept] = dept_costs.get(dept, 0) + details['annual_cost']
        
        dept_df = pd.DataFrame(list(dept_costs.items()), columns=['Department', 'Annual Cost'])
        fig = px.pie(dept_df, values='Annual Cost', names='Department', 
                     title="Budget Allocation by Department")
        st.plotly_chart(fig, use_container_width=True)
    
    # Action buttons
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📧 Request Detailed Proposal", use_container_width=True):
            st.success("""
            ✅ **Proposal Request Submitted!**
            
            Our team will prepare a detailed proposal including:
            • Customized pricing based on your requirements
            • Implementation timeline and milestones  
            • ROI projections and business case
            • Contract terms and SLA details
            
            **Expected delivery:** 3-5 business days
            """)
    
    with col2:
        if st.button("💰 Submit Budget Request", use_container_width=True):
            st.success(f"""
            ✅ **Budget Request Submitted for {st.session_state.budget_year}!**
            
            **Total Annual Investment:** ${total_annual_cost:,.0f}
            **Services Selected:** {len(st.session_state.selected_services)}
            **Request ID:** BGT-{datetime.now().strftime('%Y%m%d%H%M%S')}
            
            Your request has been forwarded to the Group CFO for approval.
            """)
    
    with col3:
        if st.button("📊 Export to Excel", use_container_width=True):
            st.info("Excel export functionality will download a detailed budget worksheet with all selected services, pricing, and business cases.")
    
    with col4:
        if st.button("🗑️ Clear Selections", use_container_width=True):
            st.session_state.selected_services = {}
            st.rerun()

# Main app logic
if st.session_state.selected_department is None:
    show_main_catalog_page()
else:
    show_offerings_catalog(st.session_state.selected_department)

# Enhanced footer for B2B catalog
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666666; padding: 20px; background: #f8f9fa; border-radius: 10px;'>
    <p><strong>Group Shared Services Catalog</strong> • Subsidiary Portal • Version 2.0</p>
    <p>🌍 <strong>Global Reach:</strong> 50+ countries • 📞 <strong>24/7 Support:</strong> support@groupservices.com</p>
    <p>💼 <strong>Account Management:</strong> subsidiary.relations@group.com • 📱 <strong>Mobile Portal:</strong> Available on all devices</p>
    <p>📈 <strong>Proven Results:</strong> $50M+ in subsidiary savings • 500+ successful implementations • 95% client satisfaction</p>
</div>
""", unsafe_allow_html=True)
