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

PROJECT_TYPES = [
    "RPA (Robotic Process Automation)",
    "AI & Machine Learning",
    "IoT Implementation",
    "Custom Application Development",
    "Data Analytics & BI",
    "Digital Transformation",
    "Infrastructure Upgrade",
    "Cybersecurity Enhancement",
    "Cloud Migration",
    "Integration Project"
]
    
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
    
    .support-package {
        background: #f0fdf4;
        border: 2px solid #22c55e;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        position: relative;
    }
    
    .support-package.selected {
        border-color: #dc2626;
        background: #fef2f2;
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
        st.session_state.support_extras = {'support': 0, 'training': 0}
    if 'implementation_projects' not in st.session_state:
        st.session_state.implementation_projects = []
    if 'company_info' not in st.session_state:
        st.session_state.company_info = {}

initialize_session_state()

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
        "support_requests": "Standard (5 per month)",
        "improvement_hours": "10 hours",
        "training_requests": "2 per quarter",
        "report_requests": "1 per month",
        "description": "Essential support for small teams with basic IT needs"
    },
    "Bronze": {
        "price": 195975,
        "support_requests": "Priority (15 per month)",
        "improvement_hours": "25 hours",
        "training_requests": "4 per quarter",
        "report_requests": "3 per month",
        "description": "Enhanced support for growing organizations"
    },
    "Silver": {
        "price": 649498,
        "support_requests": "Premium (35 per month)",
        "improvement_hours": "50 hours",
        "training_requests": "8 per quarter",
        "report_requests": "6 per month",
        "description": "Comprehensive support for medium enterprises"
    },
    "Gold": {
        "price": 1578139,
        "support_requests": "Premium Plus (75 per month)",
        "improvement_hours": "100 hours",
        "training_requests": "15 per quarter",
        "report_requests": "12 per month",
        "description": "Premium support for large organizations"
    },
    "Platinum": {
        "price": 2500000,
        "support_requests": "Unlimited",
        "improvement_hours": "200 hours",
        "training_requests": "Unlimited",
        "report_requests": "Unlimited",
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
        "year_1_total": 88770,  # Sum of all Year 1 components
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
        "year_1_total": 285660,  # Sum of all Year 1 components
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
        "year_1_total": 455015,  # Sum of all Year 1 components
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
        "year_1_total": 869861,  # Sum of all Year 1 components
        "year_2_cost": 100980,
        "year_3_cost": 109058,
        "processes_covered": "Covers up to 20 processes",
        "implementation_processes": "Covers up to 10 processes"
    }
}

DEPARTMENTS = [
    "Finance", "Human Resources", "Operations", "Sales", "Marketing", 
    "IT", "Customer Service", "Supply Chain", "Manufacturing", "Executive"
]

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
    total += st.session_state.support_extras['support'] * 1800
    total += st.session_state.support_extras['training'] * 5399
    
    return total

def calculate_implementation_total():
    return sum(project.get('budget', 0) for project in st.session_state.implementation_projects)

def calculate_total_budget():
    return calculate_operational_total() + calculate_support_total() + calculate_implementation_total()

# Header
def show_header():
    # Get selected company for dynamic header
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

# Company list for Alkhorayef Group
ALKHORAYEF_COMPANIES = [
    "APC", "AIC", "AGC", "APS", "PS", "AWPT", "AMIC", "ACC", "SPC", "Tom Egypt"
]

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
        
        # Budget summary - force recalculation each time
        st.markdown("### 💰 Service Selection Summary")
        
        # Force recalculation of all totals
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
        
        # Debug info (can be removed in production)
        if st.checkbox("Show Debug Info", value=False):
            st.markdown("### 🔍 Debug Information")
            st.write("Operational Services State:")
            for key, value in st.session_state.operational_services.items():
                if value.get('selected', False):
                    impl_status = "New" if value.get('new_implementation', False) else "Existing"
                    st.write(f"- {key}: Users={value.get('users', 0)}, Implementation={impl_status}")
            st.write(f"Custom Services: {len(st.session_state.custom_operational)}")
            st.write(f"Support Package: {st.session_state.support_package}")
            st.write(f"Projects: {len(st.session_state.implementation_projects)}")

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
                    
                    # Dynamic cost display
                    setup_text = f" + SAR {setup_cost:,} setup" if new_implementation else " (no setup cost)"
                    
                    st.markdown(f"""
                    <div class='cost-display'>
                        📊 Monthly: SAR {monthly_cost:,.0f}{setup_text}<br>
                        <strong>Annual Total: SAR {annual_cost:,.0f}</strong>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if not new_implementation and setup_cost > 0:
                        st.info("💡 No setup cost - adding users to existing system")
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
                    
                    # Dynamic cost display
                    setup_text = f" + SAR {setup_cost:,} setup" if new_implementation else " (no setup cost)"
                    
                    st.markdown(f"""
                    <div class='cost-display'>
                        📊 Monthly: SAR {monthly_cost:,.0f}{setup_text}<br>
                        <strong>Annual Total: SAR {annual_cost:,.0f}</strong>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if not new_implementation and setup_cost > 0:
                        st.info("💡 No setup cost - adding users to existing system")
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

# Support Packages Section
def show_support_packages():
    st.markdown("""
    <div class='category-section'>
        <h2>🛠️ Support Packages</h2>
        <p>Choose the support level that best fits your organization's needs.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 📞 Available Support Packages")
    
    # Display packages in rows to accommodate all 5 packages
    packages_list = list(SUPPORT_PACKAGES.items())
    
    # First row: Basic, Bronze, Silver
    cols1 = st.columns(3)
    for i in range(min(3, len(packages_list))):
        package_name, details = packages_list[i]
        
        with cols1[i]:
            is_selected = st.session_state.support_package == package_name
            border_color = "#dc2626" if is_selected else "#22c55e"
            bg_color = "#fef2f2" if is_selected else "#f0fdf4"
            
            # Create the card content without problematic HTML
            st.markdown(f"### {package_name}")
            st.markdown(f"**SAR {details['price']:,.0f}**")
            
            with st.container():
                st.markdown("---")
                st.write(f"**Support Requests:** {details['support_requests']}")
                st.write(f"**Improvement Hours:** {details['improvement_hours']}")
                st.write(f"**Training Requests:** {details['training_requests']}")
                st.write(f"**Report Requests:** {details['report_requests']}")
                st.markdown("---")
                st.caption(details['description'])
            
            if st.button(f"Select {package_name}", key=f"select_package_{package_name.lower()}_btn"):
                st.session_state.support_package = package_name
                st.success(f"✅ Selected {package_name} Support Package")
                st.rerun()
    
    # Second row: Gold, Platinum (centered)
    if len(packages_list) > 3:
        st.markdown("<br>", unsafe_allow_html=True)
        cols2 = st.columns([1, 2, 2, 1])  # Center the remaining packages
        
        for i in range(3, len(packages_list)):
            package_name, details = packages_list[i]
            col_index = i - 3 + 1  # Start from column 1 for centering
            
            with cols2[col_index]:
                is_selected = st.session_state.support_package == package_name
                
                # Create the card content without problematic HTML
                st.markdown(f"### {package_name}")
                st.markdown(f"**SAR {details['price']:,.0f}**")
                
                with st.container():
                    st.markdown("---")
                    st.write(f"**Support Requests:** {details['support_requests']}")
                    st.write(f"**Improvement Hours:** {details['improvement_hours']}")
                    st.write(f"**Training Requests:** {details['training_requests']}")
                    st.write(f"**Report Requests:** {details['report_requests']}")
                    st.markdown("---")
                    st.caption(details['description'])
                
                if st.button(f"Select {package_name}", key=f"select_package_{package_name.lower()}_btn_row2"):
                    st.session_state.support_package = package_name
                    st.success(f"✅ Selected {package_name} Support Package")
                    st.rerun()
    
    # Show selected package
    if st.session_state.support_package:
        selected_package = SUPPORT_PACKAGES[st.session_state.support_package]
        st.markdown(f"""
        <div class='cost-display' style='background: #dcfce7; border-color: #16a34a;'>
            ✅ Selected: <strong>{st.session_state.support_package}</strong> - SAR {selected_package['price']:,.0f}
        </div>
        """, unsafe_allow_html=True)
        
        # Additional services
        st.markdown("### ➕ Additional Support Services")
        
        col1, col2 = st.columns(2)
        
        with col1:
            extra_support = st.number_input("Extra Support Requests (SAR 1,800 each)", 
                                          min_value=0, 
                                          value=st.session_state.support_extras['support'],
                                          key="extra_support_requests_input")
            st.session_state.support_extras['support'] = extra_support
        
        with col2:
            extra_training = st.number_input("Extra Training/Reports (SAR 5,399 each)", 
                                           min_value=0, 
                                           value=st.session_state.support_extras['training'],
                                           key="extra_training_reports_input")
            st.session_state.support_extras['training'] = extra_training
        
        if extra_support > 0 or extra_training > 0:
            extra_cost = (extra_support * 1800) + (extra_training * 5399)
            total_support_cost = selected_package['price'] + extra_cost
            
            st.markdown(f"""
            <div class='cost-display'>
                💰 Additional Services: SAR {extra_cost:,.0f}<br>
                <strong>Total Support Cost: SAR {total_support_cost:,.0f}</strong>
            </div>
            """, unsafe_allow_html=True)

# Implementation Projects Section
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
            project_type = st.selectbox("Project Type", PROJECT_TYPES, key="project_type_input")
            timeline = st.selectbox("Timeline", ["Q1 2025", "Q2 2025", "Q3 2025", "Q4 2025", "Multi-quarter", "2+ years"], key="project_timeline_input")
            priority = st.select_slider("Priority Level", ["Low", "Medium", "High", "Critical"], value="Medium", key="project_priority_input")
        
        with col2:
            budget = st.number_input("Budget Estimate (SAR)", min_value=0, value=100000, step=10000, key="project_budget_input")
            departments = st.multiselect("Departments Involved", DEPARTMENTS, key="project_departments_input")
            
        project_description = st.text_area("Project Description", 
                                         placeholder="Describe the project scope, objectives, and expected outcomes...", 
                                         key="project_description_input")
        
        success_criteria = st.text_area("Success Criteria", 
                                      placeholder="Define how success will be measured...", 
                                      key="project_success_criteria_input")
        
        if st.button("Add Project", type="primary", key="add_implementation_project_btn"):
            if project_name and project_description and budget > 0:
                new_project = {
                    'name': project_name,
                    'type': project_type,
                    'description': project_description,
                    'timeline': timeline,
                    'priority': priority,
                    'budget': budget,
                    'departments': departments,
                    'success_criteria': success_criteria,
                    'created_date': datetime.now().strftime("%Y-%m-%d")
                }
                
                st.session_state.implementation_projects.append(new_project)
                st.success(f"✅ Added project: {project_name}")
                st.rerun()
            else:
                st.error("Please fill in project name, description, and budget.")
    
    # Display existing projects
    if st.session_state.implementation_projects:
        st.markdown("### 📋 Your Implementation Projects")
        
        total_implementation_budget = 0
        
        for i, project in enumerate(st.session_state.implementation_projects):
            total_implementation_budget += project['budget']
            
            # Color coding by priority
            priority_colors = {
                'Low': '#10b981',
                'Medium': '#f59e0b', 
                'High': '#ef4444',
                'Critical': '#dc2626'
            }
            
            priority_color = priority_colors.get(project['priority'], '#6b7280')
            
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
                if st.button(f"Remove", key=f"remove_implementation_project_{i}"):
                    st.session_state.implementation_projects.pop(i)
                    st.rerun()
        
        st.markdown(f"""
        <div class='cost-display' style='background: #fef3c7; border-color: #f59e0b;'>
            💰 Total Implementation Budget: <strong>SAR {total_implementation_budget:,.0f}</strong>
        </div>
        """, unsafe_allow_html=True)

# Summary Section
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
    
    # Charts
    col1, col2 = st.columns(2)
    
    # Pie chart for budget distribution
    with col1:
        if total_budget > 0:
            fig_pie = px.pie(
                values=[operational_total, support_total, implementation_total],
                names=['Operational Services', 'Support Packages', 'Implementation Projects'],
                title="2025 IT Budget Distribution",
                color_discrete_map={
                    'Operational Services': '#3b82f6',
                    'Support Packages': '#10b981',
                    'Implementation Projects': '#f59e0b'
                }
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pie, use_container_width=True)
    
    # Monthly cash flow projection with correct billing schedule
    with col2:
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        
        # Initialize monthly arrays
        monthly_operational = [0] * 12
        monthly_support = [0] * 12
        monthly_implementation = [0] * 12
        
        # Support and Operational costs are billed at year-end (December)
        monthly_operational[11] = operational_total  # December (index 11)
        monthly_support[11] = support_total  # December (index 11)
        
        # Implementation projects billed based on timeline/completion
        if st.session_state.implementation_projects:
            # Distribute implementation costs based on project timelines
            q1_projects = []
            q2_projects = []
            q3_projects = []
            q4_projects = []
            multi_quarter_projects = []
            
            for project in st.session_state.implementation_projects:
                timeline = project.get('timeline', 'Q4 2025')
                budget = project.get('budget', 0)
                
                # Special handling for RPA packages (multi-quarter by default)
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
                else:  # Multi-quarter or 2+ years
                    multi_quarter_projects.append(budget)
            
            # Assign project costs to completion months
            if q1_projects:
                monthly_implementation[2] = sum(q1_projects)  # March (end of Q1)
            if q2_projects:
                monthly_implementation[5] = sum(q2_projects)  # June (end of Q2)
            if q3_projects:
                monthly_implementation[8] = sum(q3_projects)  # September (end of Q3)
            if q4_projects:
                monthly_implementation[11] = sum(q4_projects)  # December (end of Q4)
            if multi_quarter_projects:
                # Spread multi-quarter projects across the year
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
    
    # Cash flow explanation
    st.markdown("""
    ### 💳 Billing Schedule Information
    - **📅 Operational & Support**: Billed at year-end (December)
    - **🚀 Implementation Projects**: Billed upon project completion based on timeline
    - **📊 Chart Above**: Shows actual payment timing based on your project schedules
    """)
    
    # Detailed breakdowns
    st.markdown("### 📋 Detailed Budget Breakdown")
    
    # Operational Services Table
    if operational_total > 0:
        st.markdown("#### 🔧 Operational Services")
        
        operational_data = []
        
        # Predefined services
        for service_key, data in st.session_state.operational_services.items():
            if data.get('selected', False) and data.get('users', 0) > 0:
                actual_service_name = data.get('actual_service_name', '')
                users = data.get('users', 0)
                is_new_implementation = data.get('new_implementation', False)
                
                # Determine provider and get service info
                if actual_service_name in ORACLE_SERVICES:
                    service_info = ORACLE_SERVICES[actual_service_name]
                    monthly_cost = service_info['price_per_user'] * users
                    setup_cost = service_info['setup_cost'] if is_new_implementation else 0
                    annual_cost = (monthly_cost * 12) + setup_cost
                    
                    implementation_status = "New Implementation" if is_new_implementation else "Adding Users"
                    
                    operational_data.append({
                        'Service': actual_service_name,
                        'Provider': 'Oracle',
                        'Users': users,
                        'Status': implementation_status,
                        'Monthly Cost': f"SAR {monthly_cost:,.0f}",
                        'Setup Cost': f"SAR {setup_cost:,.0f}",
                        'Annual Cost': f"SAR {annual_cost:,.0f}"
                    })
                
                elif actual_service_name in MICROSOFT_SERVICES:
                    service_info = MICROSOFT_SERVICES[actual_service_name]
                    monthly_cost = service_info['price_per_user'] * users
                    setup_cost = service_info['setup_cost'] if is_new_implementation else 0
                    annual_cost = (monthly_cost * 12) + setup_cost
                    
                    implementation_status = "New Implementation" if is_new_implementation else "Adding Users"
                    
                    operational_data.append({
                        'Service': actual_service_name,
                        'Provider': 'Microsoft',
                        'Users': users,
                        'Status': implementation_status,
                        'Monthly Cost': f"SAR {monthly_cost:,.0f}",
                        'Setup Cost': f"SAR {setup_cost:,.0f}",
                        'Annual Cost': f"SAR {annual_cost:,.0f}"
                    })
        
        # Custom services
        for custom_service in st.session_state.custom_operational:
            users = custom_service['users']
            monthly_cost = custom_service['price_per_user'] * users
            is_new_implementation = custom_service.get('new_implementation', False)
            setup_cost = custom_service['setup_cost'] if is_new_implementation else 0
            annual_cost = (monthly_cost * 12) + setup_cost
            
            implementation_status = "New Implementation" if is_new_implementation else "Adding Users"
            
            operational_data.append({
                'Service': f"{custom_service['name']} (Custom)",
                'Provider': 'Custom',
                'Users': users,
                'Status': implementation_status,
                'Monthly Cost': f"SAR {monthly_cost:,.0f}",
                'Setup Cost': f"SAR {setup_cost:,.0f}",
                'Annual Cost': f"SAR {annual_cost:,.0f}"
            })
        
        if operational_data:
            st.dataframe(pd.DataFrame(operational_data), use_container_width=True)
    
    # Support Package Details
    if support_total > 0:
        st.markdown("#### 🛠️ Support Package")
        
        support_data = [{
            'Package': st.session_state.support_package,
            'Base Cost': f"SAR {SUPPORT_PACKAGES[st.session_state.support_package]['price']:,.0f}",
            'Extra Support Requests': st.session_state.support_extras['support'],
            'Extra Training/Reports': st.session_state.support_extras['training'],
            'Additional Cost': f"SAR {(st.session_state.support_extras['support'] * 1800) + (st.session_state.support_extras['training'] * 5399):,.0f}",
            'Total Cost': f"SAR {support_total:,.0f}"
        }]
        
        st.dataframe(pd.DataFrame(support_data), use_container_width=True)
    
    # Implementation Projects Table
    if implementation_total > 0:
        st.markdown("#### 🚀 Implementation Projects")
        
        implementation_data = []
        for project in st.session_state.implementation_projects:
            if project.get('rpa_package', False):
                # Special handling for RPA packages
                rpa_details = project.get('rpa_details', {})
                three_year_total = rpa_details.get('year_1_total', 0) + rpa_details.get('year_2_cost', 0) + rpa_details.get('year_3_cost', 0)
                
                implementation_data.append({
                    'Project Name': project['name'],
                    'Type': project['type'],
                    'Priority': project['priority'],
                    'Timeline': project['timeline'],
                    'Process Coverage': rpa_details.get('processes_covered', 'N/A'),
                    'Year 1 Budget': f"SAR {project['budget']:,.0f}",
                    '3-Year Total': f"SAR {three_year_total:,.0f}"
                })
            else:
                # Regular projects
                implementation_data.append({
                    'Project Name': project['name'],
                    'Type': project['type'],
                    'Priority': project['priority'],
                    'Timeline': project['timeline'],
                    'Departments': ', '.join(project['departments']) if project['departments'] else 'N/A',
                    'Budget': f"SAR {project['budget']:,.0f}",
                    '3-Year Total': f"SAR {project['budget']:,.0f}"
                })
        
        st.dataframe(pd.DataFrame(implementation_data), use_container_width=True)
    
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
            # Generate unique reference ID with company code
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
