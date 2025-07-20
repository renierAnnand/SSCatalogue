import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import re

# Page configuration
st.set_page_config(
    page_title="Shared Services Digital Catalogue",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .service-card {
        background-color: white;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #1f77b4;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .dept-header {
        color: #1f77b4;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .coming-soon {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# Load and prepare data
@st.cache_data
def load_service_data():
    """Load service data from your Excel files"""
    
    # Sample IT Services data based on your file structure
    it_services = [
        {
            "service_name": "Oracle Cloud HCM - Absence Management",
            "application": "Oracle Cloud Services",
            "business_area": "Fusion Human Capital Management",
            "module": "Absence",
            "support_type": "Implementation, Support, Training, Enhancement",
            "description": "Comprehensive absence management solution including leave tracking, approval workflows, and compliance reporting.",
            "target_customers": "HR Department, Employees, Managers",
            "avg_working_days": "5-10 days",
            "category": "Human Resources"
        },
        {
            "service_name": "Oracle Cloud HCM - Payroll",
            "application": "Oracle Cloud Services", 
            "business_area": "Fusion Payroll",
            "module": "Fusion Payroll",
            "support_type": "Implementation, Support, Training, Enhancement",
            "description": "Complete payroll processing solution with automated calculations, tax compliance, and reporting.",
            "target_customers": "Payroll Team, HR Department, Finance",
            "avg_working_days": "7-14 days",
            "category": "Payroll"
        },
        {
            "service_name": "Oracle Learning Management",
            "application": "Oracle Cloud Services",
            "business_area": "Fusion Learning",
            "module": "Fusion Learning",
            "support_type": "Implementation, Support, Training",
            "description": "Learning and development platform for employee training, certification tracking, and skills development.",
            "target_customers": "Learning & Development, All Employees",
            "avg_working_days": "10-15 days",
            "category": "Learning & Development"
        },
        {
            "service_name": "Performance Management System",
            "application": "Oracle Cloud Services",
            "business_area": "Fusion Talent Management",
            "module": "Fusion Performance Management",
            "support_type": "Implementation, Support, Training",
            "description": "Performance review system with goal setting, feedback collection, and performance analytics.",
            "target_customers": "HR, Managers, All Employees",
            "avg_working_days": "5-7 days",
            "category": "Performance Management"
        },
        {
            "service_name": "IT Help Desk Support",
            "application": "Service Desk",
            "business_area": "IT Support",
            "module": "Incident Management",
            "support_type": "24/7 Support",
            "description": "Round-the-clock IT support for hardware, software, and network issues.",
            "target_customers": "All Employees",
            "avg_working_days": "1-2 days",
            "category": "Technical Support"
        }
    ]
    
    # Sample Procurement Services data based on your file structure
    procurement_services = [
        {
            "service_name": "Supplier Registration",
            "department": "Planning",
            "description": "Review, verify, and enter supplier data in the system including documentation validation and compliance checks.",
            "request_by_user": "Yes",
            "status": "Active Service",
            "avg_time_minutes": 30,
            "monthly_requests": 91,
            "system_used": "EBS & Fusion",
            "service_type": "Common"
        },
        {
            "service_name": "Training Services",
            "department": "Our Team",
            "description": "Training employees in all operations related to procurement department including system usage and procedures.",
            "request_by_user": "Yes", 
            "status": "Active Service",
            "avg_time_minutes": 20,
            "monthly_requests": 35,
            "system_used": "EBS & Fusion",
            "service_type": "Common"
        },
        {
            "service_name": "Purchase Request Processing",
            "department": "Purchasing",
            "description": "End-to-end purchase request handling including analysis, approval, order creation, and supplier coordination.",
            "request_by_user": "Yes",
            "status": "Active Service", 
            "avg_time_minutes": 45,
            "monthly_requests": 150,
            "system_used": "EBS & Fusion",
            "service_type": "Core"
        },
        {
            "service_name": "Item Master Creation",
            "department": "Planning",
            "description": "Define new items, enter technical specifications, assign category codes, and maintain item data accuracy.",
            "request_by_user": "Yes",
            "status": "Active Service",
            "avg_time_minutes": 25,
            "monthly_requests": 80,
            "system_used": "EBS & Fusion", 
            "service_type": "Common"
        },
        {
            "service_name": "Vendor Performance Review",
            "department": "Planning",
            "description": "Regular assessment of vendor performance including delivery metrics, quality scores, and compliance evaluation.",
            "request_by_user": "No",
            "status": "Internal Process",
            "avg_time_minutes": 60,
            "monthly_requests": 20,
            "system_used": "EBS & Fusion",
            "service_type": "Internal"
        }
    ]
    
    # Sample Facility Services (placeholder until HR file is received)
    facility_services = [
        {
            "service_name": "Office Space Management",
            "category": "Space Planning",
            "description": "Workspace allocation, desk assignments, and office layout optimization for efficiency and comfort.",
            "sla_hours": 24,
            "priority": "Medium",
            "cost_center": "Facilities"
        },
        {
            "service_name": "Maintenance Services", 
            "category": "Asset Maintenance",
            "description": "Preventive and corrective maintenance for building systems, furniture, and equipment.",
            "sla_hours": 4,
            "priority": "High",
            "cost_center": "Facilities"
        },
        {
            "service_name": "Safety & Security",
            "category": "Safety",
            "description": "Building security, access control, emergency procedures, and safety compliance monitoring.",
            "sla_hours": 1,
            "priority": "Critical",
            "cost_center": "Security"
        },
        {
            "service_name": "Cleaning Services",
            "category": "Janitorial",
            "description": "Daily cleaning, sanitization, waste management, and maintaining hygienic work environment.",
            "sla_hours": 12,
            "priority": "Medium", 
            "cost_center": "Facilities"
        }
    ]
    
    return {
        'it_services': pd.DataFrame(it_services),
        'procurement_services': pd.DataFrame(procurement_services),
        'facility_services': pd.DataFrame(facility_services)
    }

# Define departments with enhanced information
departments = {
    "Information Technology": {
        "description": "Delivering enterprise applications, digital solutions, cloud services, and technical support to enable business operations and digital transformation.",
        "icon": "💻",
        "color": "#1f77b4",
        "services_count": 276,
        "avg_resolution_time": "3-7 days",
        "contact": "it-support@company.com"
    },
    "Procurement": {
        "description": "Ensuring efficient sourcing, vendor management, purchase processing, and supplier relationship management to support business continuity.",
        "icon": "📦", 
        "color": "#ff7f0e",
        "services_count": 51,
        "avg_resolution_time": "2-5 days",
        "contact": "procurement@company.com"
    },
    "Facilities": {
        "description": "Delivering facility management, safety services, asset maintenance, and workspace solutions for optimal work environment.",
        "icon": "🏢",
        "color": "#2ca02c", 
        "services_count": 45,
        "avg_resolution_time": "1-3 days",
        "contact": "facilities@company.com"
    },
    "Human Resources": {
        "description": "Supporting employee lifecycle, payroll, benefits administration, learning & development, and organizational excellence.",
        "icon": "🧑‍💼",
        "color": "#d62728",
        "services_count": "TBD",
        "avg_resolution_time": "TBD", 
        "contact": "hr@company.com",
        "soon": True
    },
    "Finance": {
        "description": "Financial planning, budgeting, accounting, reporting, and business intelligence to support strategic decision-making.",
        "icon": "💰",
        "color": "#9467bd",
        "services_count": "TBD",
        "avg_resolution_time": "TBD",
        "contact": "finance@company.com", 
        "soon": True
    },
    "Legal": {
        "description": "Legal advisory, contract management, compliance, and risk management services.",
        "icon": "⚖️",
        "color": "#8c564b",
        "services_count": "TBD", 
        "avg_resolution_time": "TBD",
        "contact": "legal@company.com",
        "soon": True
    }
}

# Load service data
service_data = load_service_data()

# Sidebar navigation
st.sidebar.title("🏢 Shared Services Portal")
st.sidebar.markdown("---")

# Department selection
page = st.sidebar.selectbox(
    "Select Department",
    list(departments.keys()),
    help="Choose a department to view available services"
)

# Search functionality
st.sidebar.markdown("### 🔍 Search Services")
search_term = st.sidebar.text_input("Search for services...", placeholder="Enter keywords")

# Quick stats in sidebar
st.sidebar.markdown("### 📊 Quick Stats")
total_services = sum([int(dept["services_count"]) for dept in departments.values() if isinstance(dept["services_count"], int)])
st.sidebar.metric("Total Services", total_services)
st.sidebar.metric("Active Departments", len([d for d in departments.values() if not d.get("soon", False)]))

# Main page content
dept_info = departments[page]

# Department header
col1, col2 = st.columns([1, 4])
with col1:
    st.markdown(f"<div style='font-size: 4rem; color: {dept_info['color']};'>{dept_info['icon']}</div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<h1 style='color: {dept_info['color']};'>{page} Department</h1>", unsafe_allow_html=True)

st.markdown(dept_info["description"])

# Department metrics
if not dept_info.get("soon", False):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Available Services", dept_info["services_count"])
    with col2:
        st.metric("Avg Resolution Time", dept_info["avg_resolution_time"])
    with col3:
        st.metric("Status", "🟢 Active")
    with col4:
        st.metric("Contact", dept_info["contact"])

st.markdown("---")

# Coming soon departments
if dept_info.get("soon", False):
    st.markdown("""
    <div class='coming-soon'>
        <h2>🚧 Coming Soon</h2>
        <p>This service catalogue is currently being developed and will be available soon.</p>
        <p>For immediate assistance, please contact: <strong>{}</strong></p>
    </div>
    """.format(dept_info["contact"]), unsafe_allow_html=True)
    
else:
    # Tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Service Catalogue", "📈 Analytics", "📝 Request Service", "ℹ️ Department Info"])
    
    with tab1:
        st.subheader("Available Services")
        
        # Service filtering and display
        if page == "Information Technology":
            df = service_data['it_services']
            
            # Filter controls
            col1, col2 = st.columns(2)
            with col1:
                categories = ['All'] + list(df['category'].unique())
                selected_category = st.selectbox("Filter by Category", categories)
            with col2:
                support_types = ['All'] + list(df['support_type'].unique())
                selected_support = st.selectbox("Filter by Support Type", support_types)
            
            # Apply filters
            filtered_df = df.copy()
            if selected_category != 'All':
                filtered_df = filtered_df[filtered_df['category'] == selected_category]
            if selected_support != 'All':
                filtered_df = filtered_df[filtered_df['support_type'].str.contains(selected_support, case=False, na=False)]
            if search_term:
                filtered_df = filtered_df[filtered_df['service_name'].str.contains(search_term, case=False, na=False)]
            
            # Display services
            for idx, service in filtered_df.iterrows():
                with st.expander(f"🔧 {service['service_name']}", expanded=False):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Application:** {service['application']}")
                        st.write(f"**Business Area:** {service['business_area']}")
                        st.write(f"**Module:** {service['module']}")
                    with col2:
                        st.write(f"**Support Type:** {service['support_type']}")
                        st.write(f"**Avg Time:** {service['avg_working_days']}")
                        st.write(f"**Target Customers:** {service['target_customers']}")
                    st.write(f"**Description:** {service['description']}")
                    st.button(f"Request {service['service_name']}", key=f"req_it_{idx}")
        
        elif page == "Procurement":
            df = service_data['procurement_services']
            
            # Filter controls
            col1, col2 = st.columns(2)
            with col1:
                departments_list = ['All'] + list(df['department'].unique())
                selected_dept = st.selectbox("Filter by Department", departments_list)
            with col2:
                service_types = ['All'] + list(df['service_type'].unique())
                selected_type = st.selectbox("Filter by Service Type", service_types)
            
            # Apply filters
            filtered_df = df.copy()
            if selected_dept != 'All':
                filtered_df = filtered_df[filtered_df['department'] == selected_dept]
            if selected_type != 'All':
                filtered_df = filtered_df[filtered_df['service_type'] == selected_type]
            if search_term:
                filtered_df = filtered_df[filtered_df['service_name'].str.contains(search_term, case=False, na=False)]
            
            # Display services
            for idx, service in filtered_df.iterrows():
                with st.expander(f"📦 {service['service_name']}", expanded=False):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Department:** {service['department']}")
                        st.write(f"**Status:** {service['status']}")
                        st.write(f"**Avg Processing Time:** {service['avg_time_minutes']} minutes")
                    with col2:
                        st.write(f"**Monthly Requests:** {service['monthly_requests']}")
                        st.write(f"**System Used:** {service['system_used']}")
                        st.write(f"**Service Type:** {service['service_type']}")
                    st.write(f"**Description:** {service['description']}")
                    if service['request_by_user'] == 'Yes':
                        st.button(f"Request {service['service_name']}", key=f"req_proc_{idx}")
        
        elif page == "Facilities":
            df = service_data['facility_services']
            
            # Apply search filter
            filtered_df = df.copy()
            if search_term:
                filtered_df = filtered_df[filtered_df['service_name'].str.contains(search_term, case=False, na=False)]
            
            # Display services
            for idx, service in filtered_df.iterrows():
                priority_color = {"Critical": "🔴", "High": "🟠", "Medium": "🟡", "Low": "🟢"}
                with st.expander(f"🏢 {service['service_name']} {priority_color.get(service['priority'], '⚪')}", expanded=False):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Category:** {service['category']}")
                        st.write(f"**Priority:** {service['priority']}")
                    with col2:
                        st.write(f"**SLA:** {service['sla_hours']} hours")
                        st.write(f"**Cost Center:** {service['cost_center']}")
                    st.write(f"**Description:** {service['description']}")
                    st.button(f"Request {service['service_name']}", key=f"req_fac_{idx}")
    
    with tab2:
        st.subheader("📈 Service Analytics")
        
        if page == "Procurement":
            df = service_data['procurement_services']
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Service requests by department
                dept_requests = df.groupby('department')['monthly_requests'].sum().reset_index()
                fig1 = px.bar(dept_requests, x='department', y='monthly_requests', 
                             title="Monthly Service Requests by Department",
                             color='monthly_requests',
                             color_continuous_scale='Blues')
                st.plotly_chart(fig1, use_container_width=True)
            
            with col2:
                # Average processing time
                avg_time = df.groupby('service_type')['avg_time_minutes'].mean().reset_index()
                fig2 = px.pie(avg_time, values='avg_time_minutes', names='service_type',
                             title="Average Processing Time by Service Type")
                st.plotly_chart(fig2, use_container_width=True)
            
            # Service volume trends (simulated data)
            st.subheader("📊 Service Volume Trends")
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
            volume_data = {
                'Month': months,
                'Supplier Registration': [91, 88, 95, 102, 89, 94],
                'Purchase Requests': [150, 145, 160, 170, 155, 165],
                'Training': [35, 30, 40, 25, 45, 38]
            }
            volume_df = pd.DataFrame(volume_data)
            
            fig3 = px.line(volume_df, x='Month', y=['Supplier Registration', 'Purchase Requests', 'Training'],
                          title="Service Request Volume Trends")
            st.plotly_chart(fig3, use_container_width=True)
        
        elif page == "Information Technology":
            st.info("Analytics dashboard for IT services - showing service distribution and performance metrics")
            # Add IT-specific analytics here
            
        elif page == "Facilities":
            st.info("Analytics dashboard for Facility services - showing maintenance metrics and space utilization")
            # Add Facility-specific analytics here
    
    with tab3:
        st.subheader("📝 Service Request Form")
        
        with st.form("service_request_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                requester_name = st.text_input("Your Name*")
                requester_email = st.text_input("Email Address*")
                employee_id = st.text_input("Employee ID")
                department = st.selectbox("Your Department", 
                    ["Select...", "Engineering", "Finance", "HR", "Marketing", "Operations", "Other"])
            
            with col2:
                urgency = st.selectbox("Urgency Level", ["Low", "Medium", "High", "Critical"])
                preferred_date = st.date_input("Preferred Completion Date")
                cost_center = st.text_input("Cost Center (if applicable)")
                phone = st.text_input("Phone Number")
            
            service_requested = st.selectbox("Service Requested", 
                ["Select a service..."] + [s['service_name'] for s in service_data[f'{page.lower().replace(" ", "_")}_services'].to_dict('records') if page.lower().replace(" ", "_") in service_data])
            
            description = st.text_area("Detailed Description*", 
                placeholder="Please provide detailed information about your request...")
            
            attachments = st.file_uploader("Attach Supporting Documents", 
                accept_multiple_files=True, type=['pdf', 'doc', 'docx', 'xls', 'xlsx', 'png', 'jpg'])
            
            submitted = st.form_submit_button("Submit Request", type="primary")
            
            if submitted:
                if requester_name and requester_email and description and service_requested != "Select a service...":
                    st.success(f"""
                    ✅ **Service Request Submitted Successfully!**
                    
                    **Request ID:** SR-{datetime.now().strftime('%Y%m%d%H%M%S')}
                    **Service:** {service_requested}
                    **Estimated Response Time:** {dept_info['avg_resolution_time']}
                    
                    You will receive a confirmation email shortly at {requester_email}
                    """)
                else:
                    st.error("Please fill in all required fields marked with *")
    
    with tab4:
        st.subheader("ℹ️ Department Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📞 Contact Information")
            st.write(f"**Email:** {dept_info['contact']}")
            st.write("**Phone:** +966-11-XXX-XXXX")
            st.write("**Location:** Building A, Floor 3")
            
            st.markdown("### ⏰ Service Hours")
            st.write("**Monday - Thursday:** 8:00 AM - 5:00 PM")
            st.write("**Sunday:** 8:00 AM - 4:00 PM")
            st.write("**Emergency Support:** 24/7 for critical issues")
        
        with col2:
            st.markdown("### 📋 Service Level Agreements")
            st.write(f"**Standard Response Time:** {dept_info['avg_resolution_time']}")
            st.write("**Critical Issues:** 1-2 hours")
            st.write("**High Priority:** 4-8 hours")
            st.write("**Medium Priority:** 1-2 business days")
            st.write("**Low Priority:** 3-5 business days")
            
            st.markdown("### 📊 Performance Metrics")
            st.write("**Service Availability:** 99.5%")
            st.write("**Customer Satisfaction:** 4.2/5.0")
            st.write("**First Call Resolution:** 75%")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666666; padding: 20px;'>
    <p>Shared Services Digital Catalogue • Version 1.0 • Last Updated: July 2025</p>
    <p>For technical support with this portal, contact: <strong>it-support@company.com</strong></p>
</div>
""", unsafe_allow_html=True)