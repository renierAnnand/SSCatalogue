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
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'questionnaire_data' not in st.session_state:
    st.session_state.questionnaire_data = {}
if 'current_section' not in st.session_state:
    st.session_state.current_section = 'Operations'
if 'company_info' not in st.session_state:
    st.session_state.company_info = {}

# Oracle Fusion Licensing Data
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

# Implementation Services
implementation_services = [
    {"name": "Automation / RPA", "description": "Using Robotic Process Automation to automate repetitive tasks.", "question": "Are there any planned or ongoing RPA initiatives for 2025? If yes, please describe.", "category": "implementation"},
    {"name": "IoT", "description": "IoT systems for real-time monitoring and data collection.", "question": "Are there any planned or ongoing IoT initiatives for 2025? If yes, please describe.", "category": "implementation"},
    {"name": "eCommerce", "description": "New features or upgrades to online eCommerce platform.", "question": "Are there any new eCommerce initiatives or feature enhancements planned for 2025?", "category": "implementation"},
    {"name": "Data Analytics & BI", "description": "Expanding data-driven decision-making capabilities.", "question": "Are there any data analytics or business intelligence projects planned for 2025?", "category": "implementation"},
    {"name": "Customer Experience & Digital Channels", "description": "Improving customer-facing platforms such as websites, mobile apps, or customer portals.", "question": "Are there any planned initiatives for improving customer experience or digital channels in 2025?", "category": "implementation"},
    {"name": "Custom System & App Development", "description": "Developing custom software or mobile apps for internal or external use.", "question": "Are there any planned custom systems or app developments for 2025?", "category": "implementation"},
    {"name": "SharePoint Development", "description": "Developing or enhancing SharePoint systems for document management and collaboration.", "question": "Are there any SharePoint development needs for 2025? If yes, please describe.", "category": "implementation"},
    {"name": "AI Use Cases", "description": "Include details about AI-powered automation, machine learning models, and tools like Azure AI, etc.", "question": "Are there any AI projects planned for 2025? If yes, please describe.", "category": "implementation"},
    {"name": "Predictive Analytics", "description": "Specify departments or projects that will leverage AI models for forecasting and predictive analysis.", "question": "Do you plan to use AI for predictive analytics in 2025? If yes, please describe.", "category": "implementation"},
    {"name": "Large Language Models (LLM)", "description": "Specify if any departments plan to use LLMs for content creation, customer service, or internal knowledge management.", "question": "Are there any planned initiatives for using LLMs (e.g., GPT models) for content generation or support in 2025?", "category": "implementation"},
    {"name": "Oracle ERP Related", "description": "Custom ERP Development and Implementations", "question": "Any Custom development needed?", "category": "implementation"},
    {"name": "Web Development Related", "description": "Custom web development & Integration", "question": "Any Custom web development needed?", "category": "implementation"},
    {"name": "Microsoft CRM Related", "description": "Any CRM custom Development & Integration requirements", "question": "Any Custom CRM development and Integration Needed?", "category": "implementation"},
    {"name": "Network & Infrastructure - Existing Branch", "description": "Expand Infrastructure Services of Existing Branch or Building (Network, WiFi, Security Services, New Points in same Branch)", "question": "Specify departments, locations and Number of Users", "category": "implementation"},
    {"name": "Network & Infrastructure - New Branch", "description": "Implement New Branch or Building Infrastructure (Network, WiFi, Internet, Security Services...)", "question": "Specify departments, locations and Number of Users", "category": "implementation"},
    {"name": "Enterprise Telephony", "description": "Enable New or Existing Users for Enterprise Telephony Features", "question": "Specify Number of Users", "category": "implementation"}
]

# Support Services
support_services = [
    {"name": "General IT Support Package", "description": "General IT Support Package - Jira ticket (This incorporates all IT & Digital Support needs)", "question": "What is your support ticket volume for 2025?", "category": "support"}
]

# RPA Packages
rpa_packages = [
    {"name": "Bronze (1 Credit)", "discovery": 33110, "pm": 3080, "infrastructure": 9350, "year1": 43230, "year2": 10098, "year3": 10906, "processes": "Covers up to 2 processes", "implementation": "Covers 1 process"},
    {"name": "Silver (3 Credits)", "discovery": 94364, "pm": 8778, "infrastructure": 57310, "year1": 124608, "year2": 30294, "year3": 32718, "processes": "Covers up to 5 processes", "implementation": "Covers up to 3 processes"},
    {"name": "Gold (5 Credits)", "discovery": 148995, "pm": 13860, "infrastructure": 92950, "year1": 199210, "year2": 50490, "year3": 54529, "processes": "Covers up to 10 processes", "implementation": "Covers up to 5 processes"},
    {"name": "Platinum (10 Credits)", "discovery": 281435, "pm": 26180, "infrastructure": 180766, "year1": 381480, "year2": 100980, "year3": 109058, "processes": "Covers up to 20 processes", "implementation": "Covers up to 10 processes"}
]

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
    if st.session_state.questionnaire_data:
        st.sidebar.markdown("### 💰 Budget Summary")
        total_users = sum([int(item.get('users', 0)) for item in st.session_state.questionnaire_data.values() if item.get('users')])
        total_items = len([item for item in st.session_state.questionnaire_data.values() if item.get('selected')])
        st.sidebar.metric("Selected Items", total_items)
        st.sidebar.metric("Total Users", total_users)

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
                st.markdown(f"""
                <div class='operations-card'>
                    <h4>{service['name']}</h4>
                    <p style='font-size: 0.9em; color: #64748b;'>{service['description']}</p>
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
                    
                    st.session_state.questionnaire_data[key] = {
                        'service': service['name'],
                        'category': 'operations',
                        'type': 'oracle',
                        'selected': selected,
                        'ps_users': ps_users,
                        'shared_users': shared_users,
                        'total_users': ps_users + shared_users
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
                st.markdown(f"""
                <div class='operations-card'>
                    <h4>{service['name']}</h4>
                    <p style='font-size: 0.9em; color: #64748b;'>{service['description']}</p>
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
                    
                    st.session_state.questionnaire_data[key] = {
                        'service': service['name'],
                        'category': 'operations',
                        'type': 'microsoft',
                        'selected': selected,
                        'aic_users': aic_users,
                        'ps_users': ps_users,
                        'acc_users': acc_users,
                        'total_users': aic_users + ps_users + acc_users
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
    
    # General Support Package
    st.markdown("### 📞 IT Support Packages")
    
    with st.container():
        st.markdown(f"""
        <div class='support-card'>
            <h4>General IT Support Package</h4>
            <p style='font-size: 0.9em; color: #64748b;'>General IT Support Package - Jira ticket (This incorporates all IT & Digital Support needs)</p>
        </div>
        """, unsafe_allow_html=True)
        
        support_selected = st.checkbox("Include IT Support Package", key="support_selected")
        
        if support_selected:
            support_level = st.selectbox(
                "Select Support Package Level",
                ["Bronze Package", "Silver Package", "Gold Package", "Platinum Package"],
                key="support_level"
            )
            
            estimated_tickets = st.number_input(
                "Estimated Monthly Support Tickets",
                min_value=0,
                value=10,
                help="Estimate your monthly support ticket volume",
                key="support_tickets"
            )
            
            st.session_state.questionnaire_data['support_package'] = {
                'service': 'IT Support Package',
                'category': 'support',
                'selected': support_selected,
                'level': support_level,
                'monthly_tickets': estimated_tickets,
                'annual_tickets': estimated_tickets * 12
            }
        else:
            if 'support_package' in st.session_state.questionnaire_data:
                del st.session_state.questionnaire_data['support_package']
    
    st.markdown("---")
    
    # Support Package Details
    st.markdown("### 📋 Support Package Information")
    st.info("""
    **Support packages typically include:**
    - Help Desk Support (Business Hours / 24x7)
    - System Administration
    - Application Support
    - Infrastructure Monitoring
    - Incident Management
    - Problem Resolution
    - Change Management
    - Performance Optimization
    """)

def show_implementation_section():
    """Display Implementation section"""
    st.markdown("""
    <div class='category-header'>
        <h2>🚀 Implementation - New Projects & Initiatives</h2>
        <p>New technology implementations, custom development projects, and strategic digital initiatives.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Digital Initiatives
    st.markdown("### 💡 Digital Initiatives")
    
    digital_initiatives = [item for item in implementation_services if item['name'] in [
        'Automation / RPA', 'IoT', 'eCommerce', 'Data Analytics & BI', 
        'Customer Experience & Digital Channels', 'Custom System & App Development', 'SharePoint Development'
    ]]
    
    for service in digital_initiatives:
        with st.expander(f"📊 {service['name']}", expanded=False):
            st.markdown(f"**Description:** {service['description']}")
            
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
                
                priority = st.select_slider(
                    "Priority Level",
                    options=["Low", "Medium", "High", "Critical"],
                    value="Medium",
                    key=f"{key}_priority"
                )
                
                budget_estimate = st.number_input(
                    "Budget Estimate (SAR)",
                    min_value=0,
                    value=0,
                    key=f"{key}_budget",
                    help="Rough budget estimate if available"
                )
                
                st.session_state.questionnaire_data[key] = {
                    'service': service['name'],
                    'category': 'implementation',
                    'type': 'digital_initiative',
                    'planned': planned,
                    'description': description,
                    'priority': priority,
                    'budget_estimate': budget_estimate
                }
            else:
                if key in st.session_state.questionnaire_data:
                    del st.session_state.questionnaire_data[key]
    
    st.markdown("---")
    
    # AI, ML & LLM Initiatives
    st.markdown("### 🤖 AI, ML & LLM Initiatives")
    
    ai_initiatives = [item for item in implementation_services if item['name'] in [
        'AI Use Cases', 'Predictive Analytics', 'Large Language Models (LLM)'
    ]]
    
    for service in ai_initiatives:
        with st.expander(f"🧠 {service['name']}", expanded=False):
            st.markdown(f"**Description:** {service['description']}")
            
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
                    key=f"{key}_budget"
                )
                
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
    st.markdown("#### 💰 General AI Budget")
    general_ai_budget = st.number_input(
        "If you do not have specific AI use cases, you can budget some funds to start exploring AI opportunities:",
        min_value=0,
        value=0,
        key="general_ai_budget",
        help="General AI exploration budget (SAR)"
    )
    
    if general_ai_budget > 0:
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
    
    # RPA Packages
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
        
        # Display RPA packages in a nice format
        for package in rpa_packages:
            with st.expander(f"📦 {package['name']} - SAR {package['year1']:,} (Year 1)", expanded=False):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("Discovery & Analysis", f"SAR {package['discovery']:,}")
                    st.metric("Project Management", f"SAR {package['pm']:,}")
                    st.write(f"**Coverage:** {package['processes']}")
                
                with col2:
                    st.metric("Infrastructure & License (Annual)", f"SAR {package['infrastructure']:,}")
                    st.metric("Implementation Coverage", package['implementation'])
                    
                st.markdown("**Multi-Year Costs:**")
                col_y1, col_y2, col_y3 = st.columns(3)
                with col_y1:
                    st.metric("Year 1", f"SAR {package['year1']:,}")
                with col_y2:
                    st.metric("Year 2", f"SAR {package['year2']:,}")
                with col_y3:
                    st.metric("Year 3", f"SAR {package['year3']:,}")
                
                if st.button(f"Select {package['name']}", key=f"select_{package['name'].replace(' ', '_').lower()}"):
                    st.session_state.questionnaire_data['rpa_package'] = {
                        'service': f"RPA Package - {package['name']}",
                        'category': 'implementation',
                        'type': 'rpa_package',
                        'package_details': package,
                        'current_package': current_package,
                        'current_utilization': current_utilization,
                        'current_processes': current_processes
                    }
                    st.success(f"✅ Selected {package['name']} RPA Package")
    else:
        if 'rpa_package' in st.session_state.questionnaire_data:
            del st.session_state.questionnaire_data['rpa_package']
    
    st.markdown("---")
    
    # Infrastructure & Network Requirements
    st.markdown("### 🌐 Network & Infrastructure Requirements")
    
    infrastructure_needs = [
        {
            "name": "Existing Branch Infrastructure Expansion",
            "description": "Expand Infrastructure Services of Existing Branch or Building (Network, WiFi, Security Services, New Points in same Branch)",
            "question": "Do you require any Existing Branch Infrastructure upgrades for 2025?"
        },
        {
            "name": "New Branch Infrastructure Implementation", 
            "description": "Implement New Branch or Building Infrastructure (Network, WiFi, Internet, Security Services...)",
            "question": "Do you require any New Branch Infrastructure for 2025?"
        },
        {
            "name": "Enterprise Telephony Expansion",
            "description": "Enable New or Existing Users for Enterprise Telephony Features",
            "question": "Do you require to Enable New or Existing Users for Enterprise Telephony for 2025?"
        }
    ]
    
    for infra in infrastructure_needs:
        with st.expander(f"🏗️ {infra['name']}", expanded=False):
            st.markdown(f"**Description:** {infra['description']}")
            
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
                    key=f"{key}_budget"
                )
                
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
    
    st.markdown("---")
    
    # Custom Development Projects
    st.markdown("### 👨‍💻 Custom Development Projects")
    
    dev_projects = [
        {"name": "Oracle ERP Related", "description": "Custom ERP Development and Implementations", "question": "Any Custom development needed?"},
        {"name": "Web Development Related", "description": "Custom web development & Integration", "question": "Any Custom web development needed?"},
        {"name": "Microsoft CRM Related", "description": "Any CRM custom Development & Integration requirements", "question": "Any Custom CRM development and Integration Needed?"}
    ]
    
    for project in dev_projects:
        with st.expander(f"💻 {project['name']}", expanded=False):
            st.markdown(f"**Description:** {project['description']}")
            
            key = f"dev_{project['name'].replace(' ', '_').lower()}"
            
            needed = st.radio(
                project['question'],
                ["No", "Yes"],
                key=f"{key}_needed"
            )
            
            if needed == "Yes":
                description = st.text_area(
                    "Please describe the development requirements:",
                    key=f"{key}_description"
                )
                
                timeline = st.selectbox(
                    "Expected Timeline",
                    ["Q1 2025", "Q2 2025", "Q3 2025", "Q4 2025", "Multi-quarter"],
                    key=f"{key}_timeline"
                )
                
                priority = st.select_slider(
                    "Priority Level",
                    options=["Low", "Medium", "High", "Critical"],
                    value="Medium",
                    key=f"{key}_priority"
                )
                
                budget_estimate = st.number_input(
                    "Budget Estimate (SAR)",
                    min_value=0,
                    value=0,
                    key=f"{key}_budget"
                )
                
                st.session_state.questionnaire_data[key] = {
                    'service': project['name'],
                    'category': 'implementation',
                    'type': 'custom_development',
                    'needed': needed,
                    'description': description,
                    'timeline': timeline,
                    'priority': priority,
                    'budget_estimate': budget_estimate
                }
            else:
                if key in st.session_state.questionnaire_data:
                    del st.session_state.questionnaire_data[key]
    
    # Other Projects
    st.markdown("#### 🔧 Other Projects")
    other_projects = st.text_area(
        "List any other planned projects and initiatives not covered above:",
        key="other_projects",
        help="Describe any additional IT projects or initiatives planned for 2025"
    )
    
    if other_projects:
        st.session_state.questionnaire_data['other_projects'] = {
            'service': 'Other Projects',
            'category': 'implementation',
            'type': 'other',
            'description': other_projects
        }
    else:
        if 'other_projects' in st.session_state.questionnaire_data:
            del st.session_state.questionnaire_data['other_projects']

def show_summary():
    """Display questionnaire summary"""
    st.markdown("""
    <div class='category-header'>
        <h2>📊 Questionnaire Summary</h2>
        <p>Review your 2025 IT Budget requirements and responses.</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.questionnaire_data:
        st.info("No items selected yet. Please fill out the questionnaire sections to see your summary.")
        return
    
    # Summary by category
    operations_items = [item for item in st.session_state.questionnaire_data.values() if item.get('category') == 'operations']
    support_items = [item for item in st.session_state.questionnaire_data.values() if item.get('category') == 'support']
    implementation_items = [item for item in st.session_state.questionnaire_data.values() if item.get('category') == 'implementation']
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Operations Items", len(operations_items))
    with col2:
        st.metric("Support Items", len(support_items))
    with col3:
        st.metric("Implementation Items", len(implementation_items))
    
    # Detailed breakdown
    if operations_items:
        st.markdown("### 🔧 Operations Summary")
        for item in operations_items:
            with st.expander(f"📋 {item['service']}", expanded=False):
                st.json(item)
    
    if support_items:
        st.markdown("### 🛠️ Support Summary")
        for item in support_items:
            with st.expander(f"📋 {item['service']}", expanded=False):
                st.json(item)
    
    if implementation_items:
        st.markdown("### 🚀 Implementation Summary")
        for item in implementation_items:
            with st.expander(f"📋 {item['service']}", expanded=False):
                st.json(item)
    
    # Export options
    st.markdown("### 📤 Export Options")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Export to Excel", use_container_width=True):
            st.success("Excel export functionality would generate a comprehensive report with all questionnaire responses.")
    
    with col2:
        if st.button("📧 Email Summary", use_container_width=True):
            st.success("Email functionality would send the summary to the specified recipients.")
    
    with col3:
        if st.button("💾 Save Draft", use_container_width=True):
            st.success("Draft saved! You can continue editing later.")
    
    if st.button("🚀 Submit Questionnaire", type="primary", use_container_width=True):
        st.balloons()
        st.success(f"""
        ✅ **Questionnaire Submitted Successfully!**
        
        **Submission Details:**
        - Company: {st.session_state.company_info.get('company', 'N/A')}
        - Submitted by: {st.session_state.company_info.get('representative', 'N/A')}
        - Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        - Total Items: {len(st.session_state.questionnaire_data)}
        - Reference ID: AIC-2025-{datetime.now().strftime('%Y%m%d%H%M%S')}
        
        Your IT budget questionnaire has been submitted for review by the IT team.
        """)

# Main app
def main():
    show_header()
    show_company_info()
    
    # Navigation
    sections = ["Operations", "Support", "Implementation", "Summary"]
    selected_section = st.radio(
        "Select Section:",
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
