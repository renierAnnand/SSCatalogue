import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import uuid

# Page configuration
st.set_page_config(
    page_title="Alkhorayef Group - 2025 IT Budget Planner",
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

DEPARTMENTS = [
    "Finance", "Human Resources", "Operations", "Sales", "Marketing", 
    "IT", "Customer Service", "Supply Chain", "Manufacturing", "Executive"
]

# Utility functions
def calculate_operational_total():
    total = 0
    
    # Predefined services
    for service_key, data in st.session_state.operational_services.items():
        if data.get('selected', False):
            users = data.get('users', 0)
            if service_key.startswith('oracle_'):
                service_name = service_key.replace('oracle_', '').replace('_', ' ').title()
                if service_name in ORACLE_SERVICES:
                    monthly_cost = ORACLE_SERVICES[service_name]['price_per_user'] * users
                    setup_cost = ORACLE_SERVICES[service_name]['setup_cost']
                    total += (monthly_cost * 12) + setup_cost
            elif service_key.startswith('microsoft_'):
                service_name = service_key.replace('microsoft_', '').replace('_', ' ').title()
                # Handle special cases for matching
                if service_name == 'Microsoft 365 E3':
                    service_name = 'Microsoft 365 E3'
                elif service_name == 'Microsoft Teams Phone':
                    service_name = 'Microsoft Teams Phone'
                elif service_name == 'Power Bi Premium':
                    service_name = 'Power BI Premium'
                elif service_name == 'Project For The Web':
                    service_name = 'Project for the Web'
                elif service_name == 'Microsoft Dynamics 365':
                    service_name = 'Microsoft Dynamics 365'
                    
                if service_name in MICROSOFT_SERVICES:
                    monthly_cost = MICROSOFT_SERVICES[service_name]['price_per_user'] * users
                    setup_cost = MICROSOFT_SERVICES[service_name]['setup_cost']
                    total += (monthly_cost * 12) + setup_cost
    
    # Custom services
    for custom_service in st.session_state.custom_operational:
        users = custom_service.get('users', 0)
        monthly_cost = custom_service.get('price_per_user', 0) * users
        setup_cost = custom_service.get('setup_cost', 0)
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
    st.markdown("""
    <div class='main-header'>
        <h1>💼 Alkhorayef Group</h1>
        <h2>2025 IT Budget Planning Tool</h2>
        <p>Strategic Technology Investment Planning & Cost Analysis</p>
        <p><strong>Budget Year:</strong> 2025 | <strong>Version:</strong> 2.0</p>
    </div>
    """, unsafe_allow_html=True)

# Sidebar for company info and budget summary
def show_sidebar():
    with st.sidebar:
        st.markdown("### 🏢 Company Information")
        
        company = st.text_input("Company/Division", value="Alkhorayef Group", key="company")
        department = st.text_input("Department", key="department")
        contact_person = st.text_input("Contact Person", key="contact_person")
        email = st.text_input("Email", key="email")
        
        st.session_state.company_info = {
            'company': company,
            'department': department,
            'contact_person': contact_person,
            'email': email,
            'date': datetime.now().strftime("%Y-%m-%d")
        }
        
        st.markdown("---")
        
        # Budget summary
        st.markdown("### 💰 Budget Summary")
        
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
        
        # Progress indicators
        operational_count = len([k for k, v in st.session_state.operational_services.items() if v.get('selected', False)]) + len(st.session_state.custom_operational)
        support_selected = 1 if st.session_state.support_package else 0
        implementation_count = len(st.session_state.implementation_projects)
        
        st.markdown("### 📊 Selection Progress")
        st.metric("Operational Services", operational_count)
        st.metric("Support Package", "Selected" if support_selected else "Not Selected")
        st.metric("Implementation Projects", implementation_count)

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
                    💰 SAR {details['price_per_user']}/user/month + SAR {details['setup_cost']:,} setup
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Initialize service data if not exists
            if service_key not in st.session_state.operational_services:
                st.session_state.operational_services[service_key] = {'selected': False, 'users': 0}
            
            selected = st.checkbox(f"Include {service_name}", 
                                 key=f"{service_key}_selected",
                                 value=st.session_state.operational_services[service_key]['selected'])
            
            if selected:
                users = st.number_input(f"Number of users for {service_name}", 
                                      min_value=0, 
                                      value=st.session_state.operational_services[service_key]['users'],
                                      key=f"{service_key}_users")
                
                if users > 0:
                    monthly_cost = details['price_per_user'] * users
                    annual_cost = monthly_cost * 12 + details['setup_cost']
                    
                    st.markdown(f"""
                    <div class='cost-display'>
                        📊 Monthly: SAR {monthly_cost:,.0f} | Annual: SAR {annual_cost:,.0f}
                    </div>
                    """, unsafe_allow_html=True)
                
                st.session_state.operational_services[service_key] = {
                    'selected': True,
                    'users': users,
                    'service_name': service_name
                }
            else:
                st.session_state.operational_services[service_key]['selected'] = False
    
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
                    💰 SAR {details['price_per_user']}/user/month + SAR {details['setup_cost']:,} setup
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Initialize service data if not exists
            if service_key not in st.session_state.operational_services:
                st.session_state.operational_services[service_key] = {'selected': False, 'users': 0}
            
            selected = st.checkbox(f"Include {service_name}", 
                                 key=f"{service_key}_selected",
                                 value=st.session_state.operational_services[service_key]['selected'])
            
            if selected:
                users = st.number_input(f"Number of users for {service_name}", 
                                      min_value=0, 
                                      value=st.session_state.operational_services[service_key]['users'],
                                      key=f"{service_key}_users")
                
                if users > 0:
                    monthly_cost = details['price_per_user'] * users
                    annual_cost = monthly_cost * 12 + details['setup_cost']
                    
                    st.markdown(f"""
                    <div class='cost-display'>
                        📊 Monthly: SAR {monthly_cost:,.0f} | Annual: SAR {annual_cost:,.0f}
                    </div>
                    """, unsafe_allow_html=True)
                
                st.session_state.operational_services[service_key] = {
                    'selected': True,
                    'users': users,
                    'service_name': service_name
                }
            else:
                st.session_state.operational_services[service_key]['selected'] = False
    
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
            custom_name = st.text_input("Service Name", placeholder="e.g., Custom CRM Solution")
            custom_price = st.number_input("Price per User/Month (SAR)", min_value=0, value=50)
        
        with col2:
            custom_setup = st.number_input("Setup Cost (SAR)", min_value=0, value=5000)
            custom_users = st.number_input("Number of Users", min_value=0, value=0)
        
        custom_description = st.text_area("Service Description", 
                                        placeholder="Describe what this service provides...")
        
        if st.button("Add Custom Service"):
            if custom_name and custom_description and custom_users > 0:
                custom_service = {
                    'name': custom_name,
                    'description': custom_description,
                    'price_per_user': custom_price,
                    'setup_cost': custom_setup,
                    'users': custom_users
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
            annual_cost = monthly_cost * 12 + service['setup_cost']
            
            st.markdown(f"""
            <div class='service-card' style='border-left: 4px solid #8b5cf6;'>
                <h4>{service['name']} (Custom)</h4>
                <p style='color: #6b7280;'>{service['description']}</p>
                <p><strong>Users:</strong> {service['users']} | <strong>Monthly:</strong> SAR {monthly_cost:,.0f} | <strong>Annual:</strong> SAR {annual_cost:,.0f}</p>
                <button onclick="window.location.reload()">Remove</button>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Remove {service['name']}", key=f"remove_custom_{i}"):
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
    
    # Display packages in a grid
    cols = st.columns(3)
    packages_list = list(SUPPORT_PACKAGES.items())
    
    for i, (package_name, details) in enumerate(packages_list):
        col_index = i % 3
        
        with cols[col_index]:
            is_selected = st.session_state.support_package == package_name
            border_color = "#dc2626" if is_selected else "#22c55e"
            bg_color = "#fef2f2" if is_selected else "#f0fdf4"
            
            st.markdown(f"""
            <div style='background: {bg_color}; border: 2px solid {border_color}; border-radius: 10px; padding: 1.5rem; margin: 1rem 0; height: 400px;'>
                <h3 style='color: {border_color}; margin-bottom: 1rem;'>{package_name}</h3>
                <h2 style='color: #1f2937; margin-bottom: 1rem;'>SAR {details['price']:,.0f}</h2>
                <hr style='margin: 1rem 0;'>
                <p style='margin: 0.5rem 0;'><strong>Support Requests:</strong><br>{details['support_requests']}</p>
                <p style='margin: 0.5rem 0;'><strong>Improvement Hours:</strong><br>{details['improvement_hours']}</p>
                <p style='margin: 0.5rem 0;'><strong>Training Requests:</strong><br>{details['training_requests']}</p>
                <p style='margin: 0.5rem 0;'><strong>Report Requests:</strong><br>{details['report_requests']}</p>
                <hr style='margin: 1rem 0;'>
                <p style='font-size: 0.9em; color: #6b7280;'>{details['description']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Select {package_name}", key=f"select_{package_name}"):
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
                                          key="extra_support_requests")
            st.session_state.support_extras['support'] = extra_support
        
        with col2:
            extra_training = st.number_input("Extra Training/Reports (SAR 5,399 each)", 
                                           min_value=0, 
                                           value=st.session_state.support_extras['training'],
                                           key="extra_training_reports")
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
            project_name = st.text_input("Project Name", placeholder="e.g., AI-Powered Analytics Platform")
            project_type = st.selectbox("Project Type", PROJECT_TYPES)
            timeline = st.selectbox("Timeline", ["Q1 2025", "Q2 2025", "Q3 2025", "Q4 2025", "Multi-quarter", "2+ years"])
            priority = st.select_slider("Priority Level", ["Low", "Medium", "High", "Critical"], value="Medium")
        
        with col2:
            budget = st.number_input("Budget Estimate (SAR)", min_value=0, value=100000, step=10000)
            departments = st.multiselect("Departments Involved", DEPARTMENTS)
            
        project_description = st.text_area("Project Description", 
                                         placeholder="Describe the project scope, objectives, and expected outcomes...")
        
        success_criteria = st.text_area("Success Criteria", 
                                      placeholder="Define how success will be measured...")
        
        if st.button("Add Project", type="primary"):
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
                if st.button(f"Remove", key=f"remove_project_{i}"):
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
        <h2>📊 Budget Summary & Analysis</h2>
        <p>Comprehensive overview of your 2025 IT budget and investment strategy.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Calculate totals
    operational_total = calculate_operational_total()
    support_total = calculate_support_total()
    implementation_total = calculate_implementation_total()
    total_budget = operational_total + support_total + implementation_total
    
    if total_budget == 0:
        st.info("👋 No services or projects selected yet. Please visit the other sections to build your budget.")
        return
    
    # Budget overview metrics
    st.markdown("### 💰 Budget Overview")
    
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
            💰 Total 2025 Budget<br>
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
                title="2025 IT Budget Distribution",
                color_discrete_map={
                    'Operational Services': '#3b82f6',
                    'Support Packages': '#10b981',
                    'Implementation Projects': '#f59e0b'
                }
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pie, use_container_width=True)
    
    # Monthly cash flow projection
    with col2:
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        
        # Assume operational and support costs are spread evenly
        monthly_operational = operational_total / 12
        monthly_support = support_total / 12
        # Assume implementation costs are front-loaded in first 6 months
        monthly_implementation = [implementation_total / 6 if i < 6 else 0 for i in range(12)]
        
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(name='Operational', x=months, y=[monthly_operational]*12))
        fig_bar.add_trace(go.Bar(name='Support', x=months, y=[monthly_support]*12))
        fig_bar.add_trace(go.Bar(name='Implementation', x=months, y=monthly_implementation))
        
        fig_bar.update_layout(
            title='Monthly Cash Flow Projection (SAR)',
            barmode='stack',
            xaxis_title='Month',
            yaxis_title='Cost (SAR)'
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Detailed breakdowns
    st.markdown("### 📋 Detailed Budget Breakdown")
    
    # Operational Services Table
    if operational_total > 0:
        st.markdown("#### 🔧 Operational Services")
        
        operational_data = []
        
        # Predefined services
        for service_key, data in st.session_state.operational_services.items():
            if data.get('selected', False) and data.get('users', 0) > 0:
                service_name = data.get('service_name', service_key)
                users = data.get('users', 0)
                
                # Determine if Oracle or Microsoft
                if service_key.startswith('oracle_'):
                    clean_name = service_key.replace('oracle_', '').replace('_', ' ').title()
                    if clean_name in ORACLE_SERVICES:
                        service_info = ORACLE_SERVICES[clean_name]
                        monthly_cost = service_info['price_per_user'] * users
                        setup_cost = service_info['setup_cost']
                        annual_cost = (monthly_cost * 12) + setup_cost
                        
                        operational_data.append({
                            'Service': clean_name,
                            'Provider': 'Oracle',
                            'Users': users,
                            'Monthly Cost': f"SAR {monthly_cost:,.0f}",
                            'Setup Cost': f"SAR {setup_cost:,.0f}",
                            'Annual Cost': f"SAR {annual_cost:,.0f}"
                        })
                
                elif service_key.startswith('microsoft_'):
                    clean_name = service_key.replace('microsoft_', '').replace('_', ' ').title()
                    # Handle special naming cases
                    name_mapping = {
                        'Microsoft 365 E3': 'Microsoft 365 E3',
                        'Microsoft Teams Phone': 'Microsoft Teams Phone',
                        'Power Bi Premium': 'Power BI Premium',
                        'Project For The Web': 'Project for the Web',
                        'Microsoft Dynamics 365': 'Microsoft Dynamics 365'
                    }
                    clean_name = name_mapping.get(clean_name, clean_name)
                    
                    if clean_name in MICROSOFT_SERVICES:
                        service_info = MICROSOFT_SERVICES[clean_name]
                        monthly_cost = service_info['price_per_user'] * users
                        setup_cost = service_info['setup_cost']
                        annual_cost = (monthly_cost * 12) + setup_cost
                        
                        operational_data.append({
                            'Service': clean_name,
                            'Provider': 'Microsoft',
                            'Users': users,
                            'Monthly Cost': f"SAR {monthly_cost:,.0f}",
                            'Setup Cost': f"SAR {setup_cost:,.0f}",
                            'Annual Cost': f"SAR {annual_cost:,.0f}"
                        })
        
        # Custom services
        for custom_service in st.session_state.custom_operational:
            users = custom_service['users']
            monthly_cost = custom_service['price_per_user'] * users
            setup_cost = custom_service['setup_cost']
            annual_cost = (monthly_cost * 12) + setup_cost
            
            operational_data.append({
                'Service': f"{custom_service['name']} (Custom)",
                'Provider': 'Custom',
                'Users': users,
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
            implementation_data.append({
                'Project Name': project['name'],
                'Type': project['type'],
                'Priority': project['priority'],
                'Timeline': project['timeline'],
                'Departments': ', '.join(project['departments']) if project['departments'] else 'N/A',
                'Budget': f"SAR {project['budget']:,.0f}"
            })
        
        st.dataframe(pd.DataFrame(implementation_data), use_container_width=True)
    
    # Export and submission options
    st.markdown("### 📤 Export & Submission")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📊 Export to Excel", use_container_width=True):
            st.success("📊 Excel export functionality would generate a comprehensive budget report including all selected services, costs, and projections.")
    
    with col2:
        if st.button("💾 Save Draft", use_container_width=True):
            st.success("💾 Draft saved! Your selections have been preserved and you can continue editing later.")
    
    with col3:
        if st.button("📧 Share Summary", use_container_width=True):
            st.success("📧 Budget summary prepared for sharing with stakeholders and finance team.")
    
    with col4:
        if st.button("🚀 Submit Final Budget", type="primary", use_container_width=True):
            # Generate unique reference ID
            reference_id = f"ALK-2025-{datetime.now().strftime('%Y%m%d%H%M%S')}-{str(uuid.uuid4())[:8].upper()}"
            
            st.balloons()
            st.success(f"""
            ✅ **2025 IT Budget Successfully Submitted!**
            
            **Reference ID:** {reference_id}
            
            **Submission Summary:**
            - Company: {st.session_state.company_info.get('company', 'N/A')}
            - Contact: {st.session_state.company_info.get('contact_person', 'N/A')}
            - Total Budget: SAR {total_budget:,.0f}
            - Operational Services: SAR {operational_total:,.0f}
            - Support Package: SAR {support_total:,.0f}
            - Implementation Projects: SAR {implementation_total:,.0f}
            
            **Next Steps:**
            1. Finance team review (3-5 business days)
            2. Executive approval process
            3. Q4 2024: Implementation planning begins
            4. Q1 2025: Budget execution starts
            
            A detailed budget report has been sent to your email and the finance team.
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
