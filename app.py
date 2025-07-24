import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json

# Page configuration
st.set_page_config(
    page_title="AIC 2025 IT Budget Questionnaire",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional questionnaire styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #1e3a8a, #3b82f6);
        color: white;
        margin: -1rem -1rem 2rem -1rem;
        border-radius: 0 0 20px 20px;
    }
    
    .category-header {
        background: linear-gradient(90deg, #f8fafc, #e2e8f0);
        padding: 1rem 2rem;
        border-radius: 10px;
        border-left: 5px solid #3b82f6;
        margin: 1rem 0;
    }
    
    .service-item {
        background: white;
        padding: 1rem;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        margin: 0.5rem 0;
        transition: all 0.3s ease;
    }
    
    .service-item:hover {
        border-color: #3b82f6;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.1);
    }
    
    .budget-summary {
        background: #f0f9ff;
        border: 2px solid #0ea5e9;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .implementation-card {
        background: #fef3c7;
        border: 1px solid #f59e0b;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    .support-card {
        background: #dcfce7;
        border: 1px solid #16a34a;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    .operations-card {
        background: #e0f2fe;
        border: 1px solid #0891b2;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    .pricing-box {
        background: #f1f5f9;
        border: 2px solid #64748b;
        border-radius: 8px;
        padding: 0.75rem;
        margin: 0.5rem 0;
        text-align: center;
    }
    
    .total-cost {
        background: #fef2f2;
        border: 2px solid #dc2626;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        text-align: center;
        font-weight: bold;
        font-size: 1.2em;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'questionnaire_data' not in st.session_state:
    st.session_state.questionnaire_data = {}
if 'current_section' not in st.session_state:
    st.session_state.current_section = 'Operations'
if 'company_info' not in st.session_state:
    st.session_state.company_info = {}

# Pricing data (in SAR)
oracle_pricing = {
    "Oracle Demand Management": {"price_per_user": 45, "setup_cost": 5000},
    "ERP - Financial & PPM": {"price_per_user": 180, "setup_cost": 15000},
    "HCM - Learning Management": {"price_per_user": 25, "setup_cost": 8000},
    "ERP - Order Management": {"price_per_user": 120, "setup_cost": 12000},
    "ERP - Procurement": {"price_per_user": 95, "setup_cost": 10000},
    "ERP - Purchase Requisition": {"price_per_user": 35, "setup_cost": 3000},
    "ERP - Product Management": {"price_per_user": 85, "setup_cost": 7000},
    "ERP - Inventory, Maintenance, and Costing": {"price_per_user": 110, "setup_cost": 12000},
    "ERP Supply Planning": {"price_per_user": 75, "setup_cost": 8000},
    "HCM - Talent Management": {"price_per_user": 65, "setup_cost": 10000},
    "HCM - Core HR": {"price_per_user": 55, "setup_cost": 8000},
    "HCM - Payroll": {"price_per_user": 40, "setup_cost": 6000},
    "ERP - Self Service": {"price_per_user": 25, "setup_cost": 2000},
    "ERP - Planning & Budgeting": {"price_per_user": 90, "setup_cost": 9000}
}

microsoft_pricing = {
    "Exchange Online (Plan 1)": {"price_per_user": 18, "setup_cost": 1000},
    "Enterprise Mobility + Security E3": {"price_per_user": 32, "setup_cost": 2000},
    "Office 365 E3 Original": {"price_per_user": 82, "setup_cost": 3000},
    "Office 365 E3 Unified": {"price_per_user": 90, "setup_cost": 3000},
    "Microsoft Teams Phone Standard": {"price_per_user": 28, "setup_cost": 1500},
    "Project Plan 3": {"price_per_user": 120, "setup_cost": 2000},
    "Project Plan 5": {"price_per_user": 210, "setup_cost": 3000},
    "Visio Plan 2": {"price_per_user": 56, "setup_cost": 1000},
    "M365 Copilot Sub Add-on": {"price_per_user": 112, "setup_cost": 2500},
    "Power BI Pro Per User": {"price_per_user": 38, "setup_cost": 1500},
    "Power BI Premium Per User": {"price_per_user": 75, "setup_cost": 2500},
    "Microsoft 365 F1": {"price_per_user": 15, "setup_cost": 800}
}

support_pricing = {
    "Bronze Package": {"monthly_cost": 8000, "ticket_limit": 50, "response_time": "8 hours"},
    "Silver Package": {"monthly_cost": 15000, "ticket_limit": 100, "response_time": "4 hours"},
    "Gold Package": {"monthly_cost": 25000, "ticket_limit": 200, "response_time": "2 hours"},
    "Platinum Package": {"monthly_cost": 40000, "ticket_limit": 500, "response_time": "1 hour"}
}

# Oracle Fusion Licensing Data with categories
oracle_services = [
    {"name": "Oracle Demand Management", "description": "Provides comprehensive capabilities to predict demand using advanced algorithms, enabling better forecasting and inventory management.", "category": "operations"},
    {"name": "ERP - Financial & PPM", "description": "Supports financial management including accounting, project portfolio management, and real-time financial reporting.", "category": "operations"},
    {"name": "HCM - Learning Management", "description": "Facilitates the creation, delivery, and management of learning programs for employees, tracking progress and compliance.", "category": "operations"},
    {"name": "ERP - Order Management", "description": "Manages order processing from creation to fulfillment with integrated workflows.", "category": "operations"},
    {"name": "ERP - Procurement", "description": "Manages the full procurement process, from supplier engagement to purchase orders and supplier performance tracking.", "category": "operations"},
    {"name": "ERP - Purchase Requisition", "description": "Allows employees to create and submit purchase requests for approval, with seamless integration into procurement processes.", "category": "operations"},
    {"name": "ERP - Product Management", "description": "Comprehensive product lifecycle management with inventory and catalog features.", "category": "operations"},
    {"name": "ERP - Inventory, Maintenance, and Costing", "description": "Integrates the management of inventory, maintenance, and cost tracking for efficient operational workflows.", "category": "operations"},
    {"name": "ERP Supply Planning", "description": "Optimizes supply chain planning with advanced algorithms to align inventory and supply with demand forecasts.", "category": "operations"},
    {"name": "HCM - Talent Management", "description": "Manages the entire talent lifecycle including recruitment, development, performance evaluation, and succession planning.", "category": "operations"},
    {"name": "HCM - Core HR", "description": "Centralized management of employee data, organizational structures, and HR processes, ensuring compliance and streamlined operations.", "category": "operations"},
    {"name": "HCM - Payroll", "description": "Processes payroll efficiently and accurately, integrating with HR functions like time tracking, benefits, and taxation.", "category": "operations"},
    {"name": "ERP - Self Service", "description": "Enables employees and managers to independently manage tasks like expense reporting, purchase requisitions, and time entry through a user-friendly interface.", "category": "operations"},
    {"name": "ERP - Planning & Budgeting", "description": "Enables organizations to plan and manage their budgets with advanced forecasting and scenario analysis tools.", "category": "operations"}
]

# Microsoft Software & Subscriptions
microsoft_services = [
    {"name": "Exchange Online (Plan 1)", "description": "Provides business-class email with 50 GB mailbox and Outlook support for web, desktop, and mobile devices.", "category": "operations"},
    {"name": "Enterprise Mobility + Security E3", "description": "Comprehensive security suite offering identity and access management, device protection, and security analytics.", "category": "operations"},
    {"name": "Office 365 E3 Original", "description": "Core productivity suite with cloud apps like Word, Excel, PowerPoint, and Teams, along with cloud services.", "category": "operations"},
    {"name": "Office 365 E3 Unified", "description": "Unified version of Office 365 E3 offering collaboration tools and additional enterprise services.", "category": "operations"},
    {"name": "Microsoft Teams Phone Standard", "description": "Provides calling capabilities within Microsoft Teams, including PSTN calling and audio conferencing features.", "category": "operations"},
    {"name": "Project Plan 3", "description": "Project management tool with essential features for planning, resource management, and collaboration.", "category": "operations"},
    {"name": "Project Plan 5", "description": "Advanced project management tool with portfolio management, resource optimization, and scheduling features.", "category": "operations"},
    {"name": "Visio Plan 2", "description": "Advanced diagramming tool for creating professional diagrams, flowcharts, and organizational charts.", "category": "operations"},
    {"name": "M365 Copilot Sub Add-on", "description": "Add-on feature for Microsoft 365 offering AI-based tools to assist with tasks and workflows within the suite.", "category": "operations"},
    {"name": "Power BI Pro Per User", "description": "Per-user subscription for Power BI Pro, offering self-service business intelligence tools and report sharing.", "category": "operations"},
    {"name": "Power BI Premium Per User", "description": "Per-user subscription for Power BI Premium, offering advanced data analytics features and larger dataset capacity.", "category": "operations"},
    {"name": "Microsoft 365 F1", "description": "Entry-level Microsoft 365 plan offering core productivity tools for frontline workers.", "category": "operations"}
]

# RPA Packages with exact pricing from Excel
rpa_packages = [
    {"name": "Bronze (1 Credit)", "discovery": 33110, "pm": 3080, "infrastructure": 9350, "year1": 43230, "year2": 10098, "year3": 10906, "processes": "Covers up to 2 processes", "implementation": "Covers 1 process"},
    {"name": "Silver (3 Credits)", "discovery": 94364, "pm": 8778, "infrastructure": 57310, "year1": 124608, "year2": 30294, "year3": 32718, "processes": "Covers up to 5 processes", "implementation": "Covers up to 3 processes"},
    {"name": "Gold (5 Credits)", "discovery": 148995, "pm": 13860, "infrastructure": 92950, "year1": 199210, "year2": 50490, "year3": 54529, "processes": "Covers up to 10 processes", "implementation": "Covers up to 5 processes"},
    {"name": "Platinum (10 Credits)", "discovery": 281435, "pm": 26180, "infrastructure": 180766, "year1": 381480, "year2": 100980, "year3": 109058, "processes": "Covers up to 20 processes", "implementation": "Covers up to 10 processes"}
]

def calculate_total_budget():
    """Calculate total budget from all selected items"""
    total = 0
    
    for key, item in st.session_state.questionnaire_data.items():
        if item.get('category') == 'operations':
            if item.get('type') == 'oracle':
                service_name = item.get('service')
                pricing = oracle_pricing.get(service_name, {})
                total_users = item.get('total_users', 0)
                if total_users > 0:
                    annual_cost = (pricing.get('price_per_user', 0) * total_users * 12) + pricing.get('setup_cost', 0)
                    total += annual_cost
            elif item.get('type') == 'microsoft':
                service_name = item.get('service')
                pricing = microsoft_pricing.get(service_name, {})
                total_users = item.get('total_users', 0)
                if total_users > 0:
                    annual_cost = (pricing.get('price_per_user', 0) * total_users * 12) + pricing.get('setup_cost', 0)
                    total += annual_cost
        
        elif item.get('category') == 'support':
            if item.get('type') == 'support_package':
                level = item.get('level', '')
                pricing = support_pricing.get(level, {})
                annual_cost = pricing.get('monthly_cost', 0) * 12
                total += annual_cost
        
        elif item.get('category') == 'implementation':
            if item.get('type') == 'rpa_package':
                package_details = item.get('package_details', {})
                total += package_details.get('year1', 0)
            else:
                total += item.get('budget_estimate', 0)
    
    return total

def show_header():
    """Display the main header"""
    st.markdown("""
    <div class='main-header'>
        <h1>📋 AIC 2025 IT Budget Questionnaire</h1>
        <p>Annual Technology Budget Planning & Requirements Assessment</p>
        <p><strong>Budget Year:</strong> 2025 | <strong>Version:</strong> 1.0</p>
    </div>
    """, unsafe_allow_html=True)

def show_company_info():
    """Display company information form"""
    st.sidebar.markdown("### 🏢 Company Information")
    
    company = st.sidebar.text_input("Company", value="AIC & Power Systems", key="company")
    business_unit = st.sidebar.text_input("Business Unit", value="AIC & Power Systems", key="business_unit")
    date = st.sidebar.date_input("Date", value=datetime.now(), key="date")
    representative = st.sidebar.text_input("Company Representative", key="representative")
    
    st.session_state.company_info = {
        "company": company,
        "business_unit": business_unit,
        "date": date,
        "representative": representative
    }
    
    # Budget summary in sidebar
    total_budget = calculate_total_budget()
    st.sidebar.markdown("### 💰 Budget Summary")
    
    if st.session_state.questionnaire_data:
        total_users = sum([int(item.get('total_users', 0)) for item in st.session_state.questionnaire_data.values() if item.get('total_users')])
        total_items = len([item for item in st.session_state.questionnaire_data.values() if item.get('selected') or item.get('budget_estimate', 0) > 0])
        
        st.sidebar.metric("Selected Items", total_items)
        st.sidebar.metric("Total Users", total_users)
        st.sidebar.markdown(f"""
        <div class='total-cost'>
            💰 Total Annual Budget<br>
            <span style='font-size: 1.5em; color: #dc2626;'>SAR {total_budget:,.0f}</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.sidebar.metric("Selected Items", 0)
        st.sidebar.metric("Total Users", 0)
        st.sidebar.metric("Total Budget", "SAR 0")

def show_operations_section():
    """Display Operations section - recurring licenses and software"""
    st.markdown("""
    <div class='category-header'>
        <h2>🔧 Operations - Recurring Licenses & Software</h2>
        <p>Day-to-day operational software licenses and subscriptions required for business operations.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Oracle Fusion Licensing
    st.markdown("### 🔶 Oracle Fusion Licensing")
    col1, col2 = st.columns([1, 1])
    
    for i, service in enumerate(oracle_services):
        col = col1 if i % 2 == 0 else col2
        with col:
            with st.container():
                pricing = oracle_pricing.get(service['name'], {})
                price_per_user = pricing.get('price_per_user', 0)
                setup_cost = pricing.get('setup_cost', 0)
                
                st.markdown(f"""
                <div class='operations-card'>
                    <h4>{service['name']}</h4>
                    <p style='font-size: 0.9em; color: #64748b;'>{service['description']}</p>
                    <div class='pricing-box'>
                        💰 SAR {price_per_user}/user/month + SAR {setup_cost:,} setup
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                key = f"oracle_{service['name'].replace(' ', '_').replace('-', '_').lower()}"
                
                selected = st.checkbox(f"Include {service['name']}", key=f"{key}_selected")
                
                if selected:
                    col_a, col_b = st.columns(2)
                    with col_a:
                        ps_users = st.number_input(f"Power System Users", min_value=0, value=0, key=f"{key}_ps")
                    with col_b:
                        shared_users = st.number_input(f"Shared Users (ACC & PS)", min_value=0, value=0, key=f"{key}_shared")
                    
                    total_users = ps_users + shared_users
                    if total_users > 0:
                        annual_cost = (price_per_user * total_users * 12) + setup_cost
                        st.markdown(f"""
                        <div class='pricing-box' style='background: #dcfce7; border-color: #16a34a;'>
                            📊 Total Annual Cost: <strong>SAR {annual_cost:,.0f}</strong><br>
                            Monthly: SAR {price_per_user * total_users:,.0f} | Setup: SAR {setup_cost:,}
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.session_state.questionnaire_data[key] = {
                        'service': service['name'],
                        'category': 'operations',
                        'type': 'oracle',
                        'selected': selected,
                        'ps_users': ps_users,
                        'shared_users': shared_users,
                        'total_users': total_users,
                        'price_per_user': price_per_user,
                        'setup_cost': setup_cost,
                        'annual_cost': (price_per_user * total_users * 12) + setup_cost if total_users > 0 else 0
                    }
                else:
                    if key in st.session_state.questionnaire_data:
                        del st.session_state.questionnaire_data[key]
    
    st.markdown("---")
    
    # Microsoft Software & Subscriptions
    st.markdown("### 🏢 Microsoft Software & Subscriptions")
    
    col1, col2 = st.columns([1, 1])
    
    for i, service in enumerate(microsoft_services):
        col = col1 if i % 2 == 0 else col2
        with col:
            with st.container():
                pricing = microsoft_pricing.get(service['name'], {})
                price_per_user = pricing.get('price_per_user', 0)
                setup_cost = pricing.get('setup_cost', 0)
                
                st.markdown(f"""
                <div class='operations-card'>
                    <h4>{service['name']}</h4>
                    <p style='font-size: 0.9em; color: #64748b;'>{service['description']}</p>
                    <div class='pricing-box'>
                        💰 SAR {price_per_user}/user/month + SAR {setup_cost:,} setup
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                key = f"microsoft_{service['name'].replace(' ', '_').replace('-', '_').replace('(', '').replace(')', '').replace('+', 'plus').lower()}"
                
                selected = st.checkbox(f"Include {service['name']}", key=f"{key}_selected")
                
                if selected:
                    col_a, col_b, col_c = st.columns(3)
                    with col_a:
                        aic_users = st.number_input(f"AIC without PS", min_value=0, value=0, key=f"{key}_aic")
                    with col_b:
                        ps_users = st.number_input(f"Power System", min_value=0, value=0, key=f"{key}_ps")
                    with col_c:
                        acc_users = st.number_input(f"ACC Power System", min_value=0, value=0, key=f"{key}_acc")
                    
                    total_users = aic_users + ps_users + acc_users
                    if total_users > 0:
                        annual_cost = (price_per_user * total_users * 12) + setup_cost
                        st.markdown(f"""
                        <div class='pricing-box' style='background: #dcfce7; border-color: #16a34a;'>
                            📊 Total Annual Cost: <strong>SAR {annual_cost:,.0f}</strong><br>
                            Monthly: SAR {price_per_user * total_users:,.0f} | Setup: SAR {setup_cost:,}
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.session_state.questionnaire_data[key] = {
                        'service': service['name'],
                        'category': 'operations',
                        'type': 'microsoft',
                        'selected': selected,
                        'aic_users': aic_users,
                        'ps_users': ps_users,
                        'acc_users': acc_users,
                        'total_users': total_users,
                        'price_per_user': price_per_user,
                        'setup_cost': setup_cost,
                        'annual_cost': (price_per_user * total_users * 12) + setup_cost if total_users > 0 else 0
                    }
                else:
                    if key in st.session_state.questionnaire_data:
                        del st.session_state.questionnaire_data[key]

def show_support_section():
    """Display Support section"""
    st.markdown("""
    <div class='category-header'>
        <h2>🛠️ Support - Maintenance & Support Services</h2>
        <p>Ongoing support packages and maintenance services for your IT infrastructure and applications.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Support Package Selection
    st.markdown("### 📞 IT Support Packages")
    
    support_selected = st.checkbox("Include IT Support Package", key="support_selected")
    
    if support_selected:
        st.markdown("#### Choose Your Support Level")
        
        # Display all support packages with pricing
        for package_name, details in support_pricing.items():
            with st.expander(f"📦 {package_name} - SAR {details['monthly_cost']:,}/month", expanded=False):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Monthly Cost", f"SAR {details['monthly_cost']:,}")
                    st.metric("Annual Cost", f"SAR {details['monthly_cost'] * 12:,}")
                
                with col2:
                    st.metric("Monthly Ticket Limit", details['ticket_limit'])
                    st.metric("Response Time", details['response_time'])
                
                with col3:
                    st.write("**Includes:**")
                    st.write("- Help Desk Support")
                    st.write("- System Administration")
                    st.write("- Application Support")
                    st.write("- Infrastructure Monitoring")
                    if package_name in ["Gold Package", "Platinum Package"]:
                        st.write("- 24x7 Support")
                        st.write("- Dedicated Account Manager")
                
                if st.button(f"Select {package_name}", key=f"select_{package_name.replace(' ', '_').lower()}"):
                    estimated_tickets = st.number_input(
                        "Estimated Monthly Support Tickets",
                        min_value=0,
                        value=min(details['ticket_limit']//2, 25),
                        max_value=details['ticket_limit'],
                        help=f"Maximum {details['ticket_limit']} tickets per month for this package",
                        key="support_tickets"
                    )
                    
                    st.session_state.questionnaire_data['support_package'] = {
                        'service': f'IT Support Package - {package_name}',
                        'category': 'support',
                        'type': 'support_package',
                        'selected': support_selected,
                        'level': package_name,
                        'monthly_cost': details['monthly_cost'],
                        'annual_cost': details['monthly_cost'] * 12,
                        'monthly_tickets': estimated_tickets,
                        'ticket_limit': details['ticket_limit'],
                        'response_time': details['response_time']
                    }
                    st.success(f"✅ Selected {package_name}")
                    st.markdown(f"""
                    <div class='total-cost'>
                        💰 Annual Support Cost: SAR {details['monthly_cost'] * 12:,}
                    </div>
                    """, unsafe_allow_html=True)
    else:
        if 'support_package' in st.session_state.questionnaire_data:
            del st.session_state.questionnaire_data['support_package']
    
    st.markdown("---")
    
    # Support Package Comparison
    st.markdown("### 📊 Support Package Comparison")
    
    comparison_data = []
    for package_name, details in support_pricing.items():
        comparison_data.append({
            'Package': package_name,
            'Monthly Cost (SAR)': f"{details['monthly_cost']:,}",
            'Annual Cost (SAR)': f"{details['monthly_cost'] * 12:,}",
            'Ticket Limit': details['ticket_limit'],
            'Response Time': details['response_time'],
            'Coverage': "Business Hours" if package_name in ["Bronze Package", "Silver Package"] else "24x7"
        })
    
    comparison_df = pd.DataFrame(comparison_data)
    st.dataframe(comparison_df, use_container_width=True)

def show_implementation_section():
    """Display Implementation section"""
    st.markdown("""
    <div class='category-header'>
        <h2>🚀 Implementation - New Projects & Initiatives</h2>
        <p>New technology implementations, custom development projects, and strategic digital initiatives.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # RPA Packages - Featured prominently with exact pricing
    st.markdown("### 🤖 RPA (Robotic Process Automation) Packages")
    
    rpa_selected = st.checkbox("Include RPA Package for 2025", key="rpa_selected")
    
    if rpa_selected:
        st.markdown("#### Current RPA Utilization")
        col1, col2 = st.columns(2)
        with col1:
            current_package = st.selectbox("2024 Package", ["None", "Bronze", "Silver", "Gold", "Platinum"], key="current_rpa")
        with col2:
            current_utilization = st.slider("Current Package Utilization (%)", 0, 100, 0, key="current_rpa_util")
        
        current_processes = st.text_input("Current RPA Processes", value="None", key="current_rpa_processes")
        
        st.markdown("#### 2025 RPA Package Selection")
        
        # Display RPA packages with exact pricing from Excel
        for package in rpa_packages:
            with st.expander(f"📦 {package['name']} - SAR {package['year1']:,} (Year 1)", expanded=False):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("**Discovery & Analysis**")
                    st.metric("Cost", f"SAR {package['discovery']:,}")
                    st.markdown("**Project Management**")
                    st.metric("Cost", f"SAR {package['pm']:,}")
                
                with col2:
                    st.markdown("**Infrastructure & License (Annual)**")
                    st.metric("Cost", f"SAR {package['infrastructure']:,}")
                    st.write(f"**Process Coverage:** {package['processes']}")
                    st.write(f"**Implementation:** {package['implementation']}")
                
                with col3:
                    st.markdown("**Multi-Year Investment**")
                    st.metric("Year 1 Total", f"SAR {package['year1']:,}")
                    st.metric("Year 2 Total", f"SAR {package['year2']:,}")
                    st.metric("Year 3 Total", f"SAR {package['year3']:,}")
                
                # 3-year total
                three_year_total = package['year1'] + package['year2'] + package['year3']
                st.markdown(f"""
                <div class='total-cost'>
                    💰 3-Year Total Investment: SAR {three_year_total:,}
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"Select {package['name']}", key=f"select_{package['name'].replace(' ', '_').replace('(', '').replace(')', '').lower()}"):
                    st.session_state.questionnaire_data['rpa_package'] = {
                        'service': f"RPA Package - {package['name']}",
                        'category': 'implementation',
                        'type': 'rpa_package',
                        'package_details': package,
                        'current_package': current_package,
                        'current_utilization': current_utilization,
                        'current_processes': current_processes,
                        'annual_cost': package['year1'],
                        'three_year_total': three_year_total
                    }
                    st.success(f"✅ Selected {package['name']} RPA Package")
                    st.balloons()
    else:
        if 'rpa_package' in st.session_state.questionnaire_data:
            del st.session_state.questionnaire_data['rpa_package']
    
    st.markdown("---")
    
    # Digital Initiatives with budget estimates
    st.markdown("### 💡 Digital Initiatives")
    
    digital_initiatives = [
        {"name": "Automation / RPA", "description": "Using Robotic Process Automation to automate repetitive tasks.", "question": "Are there any planned or ongoing RPA initiatives for 2025? If yes, please describe.", "typical_budget": "50000-200000"},
        {"name": "IoT", "description": "IoT systems for real-time monitoring and data collection.", "question": "Are there any planned or ongoing IoT initiatives for 2025? If yes, please describe.", "typical_budget": "75000-300000"},
        {"name": "eCommerce", "description": "New features or upgrades to online eCommerce platform.", "question": "Are there any new eCommerce initiatives or feature enhancements planned for 2025?", "typical_budget": "100000-500000"},
        {"name": "Data Analytics & BI", "description": "Expanding data-driven decision-making capabilities.", "question": "Are there any data analytics or business intelligence projects planned for 2025?", "typical_budget": "80000-250000"},
        {"name": "Customer Experience & Digital Channels", "description": "Improving customer-facing platforms such as websites, mobile apps, or customer portals.", "question": "Are there any planned initiatives for improving customer experience or digital channels in 2025?", "typical_budget": "120000-400000"},
        {"name": "Custom System & App Development", "description": "Developing custom software or mobile apps for internal or external use.", "question": "Are there any planned custom systems or app developments for 2025?", "typical_budget": "100000-600000"},
        {"name": "SharePoint Development", "description": "Developing or enhancing SharePoint systems for document management and collaboration.", "question": "Are there any SharePoint development needs for 2025? If yes, please describe.", "typical_budget": "30000-150000"}
    ]
    
    for service in digital_initiatives:
        with st.expander(f"📊 {service['name']}", expanded=False):
            st.markdown(f"**Description:** {service['description']}")
            st.info(f"💰 **Typical Budget Range:** SAR {service['typical_budget']}")
            
            key = f"digital_{service['name'].replace(' ', '_').replace('/', '_').replace('&', 'and').lower()}"
            
            planned = st.radio(
                service['question'],
                ["No", "Yes", "Under Consideration"],
                key=f"{key}_planned"
            )
            
            if planned in ["Yes", "Under Consideration"]:
                description = st.text_area(
                    "Please provide details:",
                    key=f"{key}_description",
                    help="Describe the scope, timeline, and requirements"
                )
                
                col1, col2 = st.columns(2)
                with col1:
                    priority = st.select_slider(
                        "Priority Level",
                        options=["Low", "Medium", "High", "Critical"],
                        value="Medium",
                        key=f"{key}_priority"
                    )
                
                with col2:
                    timeline = st.selectbox(
                        "Expected Timeline",
                        ["Q1 2025", "Q2 2025", "Q3 2025", "Q4 2025", "Multi-quarter"],
                        key=f"{key}_timeline"
                    )
                
                budget_estimate = st.number_input(
                    "Budget Estimate (SAR)",
                    min_value=0,
                    value=0,
                    key=f"{key}_budget",
                    help=f"Typical range: SAR {service['typical_budget']}"
                )
                
                if budget_estimate > 0:
                    st.markdown(f"""
                    <div class='pricing-box' style='background: #fef3c7; border-color: #f59e0b;'>
                        💰 Estimated Project Cost: <strong>SAR {budget_estimate:,.0f}</strong>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.session_state.questionnaire_data[key] = {
                    'service': service['name'],
                    'category': 'implementation',
                    'type': 'digital_initiative',
                    'planned': planned,
                    'description': description,
                    'priority': priority,
                    'timeline': timeline,
                    'budget_estimate': budget_estimate
                }
            else:
                if key in st.session_state.questionnaire_data:
                    del st.session_state.questionnaire_data[key]
    
    st.markdown("---")
    
    # AI, ML & LLM Initiatives
    st.markdown("### 🤖 AI, ML & LLM Initiatives")
    
    ai_initiatives = [
        {"name": "AI Use Cases", "description": "Include details about AI-powered automation, machine learning models, and tools like Azure AI, etc.", "question": "Are there any AI projects planned for 2025? If yes, please describe.", "typical_budget": "75000-400000"},
        {"name": "Predictive Analytics", "description": "Specify departments or projects that will leverage AI models for forecasting and predictive analysis.", "question": "Do you plan to use AI for predictive analytics in 2025? If yes, please describe.", "typical_budget": "60000-250000"},
        {"name": "Large Language Models (LLM)", "description": "Specify if any departments plan to use LLMs for content creation, customer service, or internal knowledge management.", "question": "Are there any planned initiatives for using LLMs (e.g., GPT models) for content generation or support in 2025?", "typical_budget": "40000-200000"}
    ]
    
    for service in ai_initiatives:
        with st.expander(f"🧠 {service['name']}", expanded=False):
            st.markdown(f"**Description:** {service['description']}")
            st.info(f"💰 **Typical Budget Range:** SAR {service['typical_budget']}")
            
            key = f"ai_{service['name'].replace(' ', '_').replace('(', '').replace(')', '').replace(',', '').lower()}"
            
            planned = st.radio(
                service['question'],
                ["No", "Yes", "Under Consideration"],
                key=f"{key}_planned"
            )
            
            if planned in ["Yes", "Under Consideration"]:
                description = st.text_area(
                    "Please provide details:",
                    key=f"{key}_description"
                )
                
                departments = st.multiselect(
                    "Departments/Areas Involved",
                    ["Finance", "HR", "Operations", "Sales", "Marketing", "IT", "Customer Service", "Supply Chain"],
                    key=f"{key}_departments"
                )
                
                budget_estimate = st.number_input(
                    "Budget Estimate (SAR)",
                    min_value=0,
                    value=0,
                    key=f"{key}_budget",
                    help=f"Typical range: SAR {service['typical_budget']}"
                )
                
                if budget_estimate > 0:
                    st.markdown(f"""
                    <div class='pricing-box' style='background: #fef3c7; border-color: #f59e0b;'>
                        💰 Estimated AI Project Cost: <strong>SAR {budget_estimate:,.0f}</strong>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.session_state.questionnaire_data[key] = {
                    'service': service['name'],
                    'category': 'implementation',
                    'type': 'ai_initiative',
                    'planned': planned,
                    'description': description,
                    'departments': departments,
                    'budget_estimate': budget_estimate
                }
            else:
                if key in st.session_state.questionnaire_data:
                    del st.session_state.questionnaire_data[key]
    
    # General AI Budget
    st.markdown("#### 💰 General AI Exploration Budget")
    general_ai_budget = st.number_input(
        "If you do not have specific AI use cases, you can budget some funds to start exploring AI opportunities:",
        min_value=0,
        value=0,
        key="general_ai_budget",
        help="General AI exploration budget (SAR) - Typical range: SAR 25,000-100,000"
    )
    
    if general_ai_budget > 0:
        st.markdown(f"""
        <div class='pricing-box' style='background: #e0f2fe; border-color: #0891b2;'>
            💰 General AI Exploration Budget: <strong>SAR {general_ai_budget:,.0f}</strong>
        </div>
        """, unsafe_allow_html=True)
        
        st.session_state.questionnaire_data['general_ai_budget'] = {
            'service': 'General AI Budget',
            'category': 'implementation',
            'type': 'ai_budget',
            'budget_estimate': general_ai_budget
        }
    else:
        if 'general_ai_budget' in st.session_state.questionnaire_data:
            del st.session_state.questionnaire_data['general_ai_budget']
    
    st.markdown("---")
    
    # Infrastructure & Network Requirements
    st.markdown("### 🌐 Network & Infrastructure Requirements")
    
    infrastructure_needs = [
        {
            "name": "Existing Branch Infrastructure Expansion",
            "description": "Expand Infrastructure Services of Existing Branch or Building (Network, WiFi, Security Services, New Points in same Branch)",
            "question": "Do you require any Existing Branch Infrastructure upgrades for 2025?",
            "typical_budget": "20000-100000"
        },
        {
            "name": "New Branch Infrastructure Implementation", 
            "description": "Implement New Branch or Building Infrastructure (Network, WiFi, Internet, Security Services...)",
            "question": "Do you require any New Branch Infrastructure for 2025?",
            "typical_budget": "50000-300000"
        },
        {
            "name": "Enterprise Telephony Expansion",
            "description": "Enable New or Existing Users for Enterprise Telephony Features",
            "question": "Do you require to Enable New or Existing Users for Enterprise Telephony for 2025?",
            "typical_budget": "15000-75000"
        }
    ]
    
    for infra in infrastructure_needs:
        with st.expander(f"🏗️ {infra['name']}", expanded=False):
            st.markdown(f"**Description:** {infra['description']}")
            st.info(f"💰 **Typical Budget Range:** SAR {infra['typical_budget']}")
            
            key = f"infra_{infra['name'].replace(' ', '_').lower()}"
            
            required = st.radio(
                infra['question'],
                ["No", "Yes"],
                key=f"{key}_required"
            )
            
            if required == "Yes":
                locations = st.text_area(
                    "Specify departments, locations and number of users:",
                    key=f"{key}_details",
                    help="Provide detailed requirements including locations, departments, and user counts"
                )
                
                estimated_users = st.number_input(
                    "Estimated Number of Users",
                    min_value=0,
                    value=0,
                    key=f"{key}_users"
                )
                
                budget_estimate = st.number_input(
                    "Budget Estimate (SAR)",
                    min_value=0,
                    value=0,
                    key=f"{key}_budget",
                    help=f"Typical range: SAR {infra['typical_budget']}"
                )
                
                if budget_estimate > 0:
                    st.markdown(f"""
                    <div class='pricing-box' style='background: #fef3c7; border-color: #f59e0b;'>
                        💰 Infrastructure Investment: <strong>SAR {budget_estimate:,.0f}</strong><br>
                        Users: {estimated_users} | Cost per user: SAR {budget_estimate/max(estimated_users,1):,.0f}
                    </div>
                    """, unsafe_allow_html=True)
                
                st.session_state.questionnaire_data[key] = {
                    'service': infra['name'],
                    'category': 'implementation',
                    'type': 'infrastructure',
                    'required': required,
                    'details': locations,
                    'estimated_users': estimated_users,
                    'budget_estimate': budget_estimate
                }
            else:
                if key in st.session_state.questionnaire_data:
                    del st.session_state.questionnaire_data[key]

def show_summary():
    """Display questionnaire summary with comprehensive budget breakdown"""
    st.markdown("""
    <div class='category-header'>
        <h2>📊 Questionnaire Summary & Budget Analysis</h2>
        <p>Review your 2025 IT Budget requirements and comprehensive cost analysis.</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.questionnaire_data:
        st.info("No items selected yet. Please fill out the questionnaire sections to see your summary.")
        return
    
    # Calculate comprehensive budget breakdown
    operations_total = 0
    support_total = 0
    implementation_total = 0
    
    operations_items = []
    support_items = []
    implementation_items = []
    
    for key, item in st.session_state.questionnaire_data.items():
        if item.get('category') == 'operations':
            operations_items.append(item)
            operations_total += item.get('annual_cost', 0)
        elif item.get('category') == 'support':
            support_items.append(item)
            support_total += item.get('annual_cost', 0)
        elif item.get('category') == 'implementation':
            implementation_items.append(item)
            implementation_total += item.get('budget_estimate', 0)
            if item.get('type') == 'rpa_package':
                implementation_total += item.get('package_details', {}).get('year1', 0) - item.get('budget_estimate', 0)
    
    total_budget = operations_total + support_total + implementation_total
    
    # Budget overview
    st.markdown("### 💰 Budget Overview")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Operations (Annual)", f"SAR {operations_total:,.0f}", f"{operations_total/max(total_budget,1)*100:.1f}%")
    with col2:
        st.metric("Support (Annual)", f"SAR {support_total:,.0f}", f"{support_total/max(total_budget,1)*100:.1f}%")
    with col3:
        st.metric("Implementation", f"SAR {implementation_total:,.0f}", f"{implementation_total/max(total_budget,1)*100:.1f}%")
    with col4:
        st.markdown(f"""
        <div class='total-cost'>
            💰 Total 2025 Budget<br>
            <span style='font-size: 1.8em; color: #dc2626;'>SAR {total_budget:,.0f}</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Budget distribution chart
    if total_budget > 0:
        fig = px.pie(
            values=[operations_total, support_total, implementation_total],
            names=['Operations', 'Support', 'Implementation'],
            title="2025 IT Budget Distribution",
            color_discrete_map={
                'Operations': '#0891b2',
                'Support': '#16a34a', 
                'Implementation': '#f59e0b'
            }
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Detailed breakdown by category
    if operations_items:
        st.markdown("### 🔧 Operations Budget Breakdown")
        operations_df = []
        for item in operations_items:
            operations_df.append({
                'Service': item['service'],
                'Type': item.get('type', '').title(),
                'Users': item.get('total_users', 0),
                'Monthly Cost': f"SAR {item.get('annual_cost', 0)/12:,.0f}",
                'Annual Cost': f"SAR {item.get('annual_cost', 0):,.0f}",
                'Setup Cost': f"SAR {item.get('setup_cost', 0):,.0f}"
            })
        
        if operations_df:
            st.dataframe(pd.DataFrame(operations_df), use_container_width=True)
    
    if support_items:
        st.markdown("### 🛠️ Support Budget Breakdown")
        for item in support_items:
            st.markdown(f"""
            <div class='support-card'>
                <h4>{item['service']}</h4>
                <p><strong>Monthly Cost:</strong> SAR {item.get('monthly_cost', 0):,}</p>
                <p><strong>Annual Cost:</strong> SAR {item.get('annual_cost', 0):,}</p>
                <p><strong>Response Time:</strong> {item.get('response_time', 'N/A')}</p>
                <p><strong>Monthly Ticket Limit:</strong> {item.get('ticket_limit', 'N/A')}</p>
            </div>
            """, unsafe_allow_html=True)
    
    if implementation_items:
        st.markdown("### 🚀 Implementation Projects Budget")
        implementation_df = []
        for item in implementation_items:
            budget = item.get('budget_estimate', 0)
            if item.get('type') == 'rpa_package':
                budget = item.get('package_details', {}).get('year1', 0)
            
            implementation_df.append({
                'Project': item['service'],
                'Type': item.get('type', '').replace('_', ' ').title(),
                'Priority': item.get('priority', 'N/A'),
                'Timeline': item.get('timeline', 'N/A'),
                'Budget Estimate': f"SAR {budget:,.0f}"
            })
        
        if implementation_df:
            st.dataframe(pd.DataFrame(implementation_df), use_container_width=True)
    
    # Monthly cash flow projection
    st.markdown("### 📈 Monthly Cash Flow Projection")
    
    monthly_operations = operations_total / 12
    monthly_support = support_total / 12
    # Assume implementation costs are spread over the year
    monthly_implementation = implementation_total / 12
    
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    monthly_data = {
        'Month': months,
        'Operations': [monthly_operations] * 12,
        'Support': [monthly_support] * 12,
        'Implementation': [monthly_implementation] * 12,
        'Total': [monthly_operations + monthly_support + monthly_implementation] * 12
    }
    
    fig = px.bar(
        monthly_data, 
        x='Month', 
        y=['Operations', 'Support', 'Implementation'],
        title="Monthly IT Budget Projection (SAR)",
        barmode='stack'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Export and submission options
    st.markdown("### 📤 Export & Submission Options")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📊 Export to Excel", use_container_width=True):
            st.success("Excel export would include:\n• Detailed budget breakdown\n• Service specifications\n• Cost analysis\n• Monthly projections")
    
    with col2:
        if st.button("📧 Email Summary", use_container_width=True):
            st.success("Email sent with comprehensive budget summary to IT team and finance department.")
    
    with col3:
        if st.button("💾 Save Draft", use_container_width=True):
            st.success("Draft saved successfully! You can continue editing later.")
    
    with col4:
        if st.button("🚀 Submit Final", type="primary", use_container_width=True):
            st.balloons()
            st.success(f"""
            ✅ **Budget Questionnaire Submitted Successfully!**
            
            **Submission Summary:**
            - Company: {st.session_state.company_info.get('company', 'N/A')}
            - Representative: {st.session_state.company_info.get('representative', 'N/A')}
            - Total Budget: SAR {total_budget:,.0f}
            - Operations Items: {len(operations_items)}
            - Support Items: {len(support_items)}
            - Implementation Items: {len(implementation_items)}
            - Reference ID: AIC-2025-{datetime.now().strftime('%Y%m%d%H%M%S')}
            
            **Next Steps:**
            1. IT team will review within 5 business days
            2. Finance approval process initiated
            3. Implementation planning begins Q4 2024
            """)

# Main app
def main():
    show_header()
    show_company_info()
    
    # Navigation
    sections = ["Operations", "Support", "Implementation", "Summary"]
    selected_section = st.radio(
        "📋 Select Questionnaire Section:",
        sections,
        horizontal=True,
        key="section_nav"
    )
    
    st.session_state.current_section = selected_section
    
    # Display selected section
    if selected_section == "Operations":
        show_operations_section()
    elif selected_section == "Support":
        show_support_section()
    elif selected_section == "Implementation":
        show_implementation_section()
    elif selected_section == "Summary":
        show_summary()

if __name__ == "__main__":
    main()
