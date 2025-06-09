import streamlit as st
import pandas as pd
import datetime

def calculate_total_cost(vm_type, vm_instances, instance_type, storage_amount, frontend_framework, 
                         duration_months, gen_ai_backend, open_ai_service, parsing_data, embeddings, backend_resources):
    # Base costs per VM type per month
    vm_costs = {
        " VM with docker support - 16v CPUâ€™s, 64 GB RAM (minimum)": 1,
        "Custom": 1.5  # Base cost for custom, to be adjusted
    }
    
    # Instance type cost
    instance_cost = 100 if instance_type == "Shared" else 600
    
    # Frontend framework cost (set to zero as per requirements)
    frontend_cost = 0
    
    # Gen AI backend cost
    gen_ai_cost = 0 if gen_ai_backend == "Opensource" else 25
    
    # Parsing data cost
    parsing_cost = 0 if parsing_data == "Llama Cloud" else 0  # Custom parsing cost not specified
    
    # Embeddings cost
    embedding_cost = 0 if embeddings == "OpenAI embeddings models" else 5
    
    # Backend resources cost
    backend_cost = 20 if backend_resources == "Python (FastAPI) + Typescript (NestJS)" else 0
    
    # Storage cost per GB
    storage_cost = 0.1 * storage_amount
    
    # Calculate VM cost
    vm_cost = vm_instances* instance_cost
    
    # Calculate base cost
    base_cost = vm_cost + storage_cost + frontend_cost + gen_ai_cost + parsing_cost + embedding_cost + backend_cost
    
    # Total monthly cost
    total_monthly_cost = base_cost
    
    # Total project cost
    total_project_cost = total_monthly_cost * duration_months
    
    return {
        "VM Cost": vm_cost,
        "Storage Cost": storage_cost,
        "Frontend Cost": frontend_cost,
        "Gen AI Cost": gen_ai_cost,
        "Parsing Cost": parsing_cost,
        "Embedding Cost": embedding_cost,
        "Backend Cost": backend_cost,
        "Monthly Cost": total_monthly_cost,
        "Total Project Cost": total_project_cost
    }

def main():
    st.set_page_config(
        page_title="Project Cost Estimator",
        page_icon="💰",
        layout="wide",
        #initial_sidebar_state="expanded",
    )
    

    st.markdown("""
    <style>
    .main {
        padding: 2rem;
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
    }
    .cost-card {
        padding: 1.5rem;
        border-radius: 0.5rem;
        background-color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    h1.title {
        color: #1f77b4;
        text-align: center; /* Center-align the title */  
    }
    h2, h3 {
        color: #1f77b4;
    }
    .disclaimer {
        font-size: 0.8rem;
        color: #6c757d;
        font-style: italic;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<h1 class='title'>Project Cost Estimation Tool</h1>", unsafe_allow_html=True)
    st.markdown("Use this form to estimate the cost of your cloud-based project")

    with st.form("cost_form"):
        st.header("Project Parameters")

        st.subheader("Infrastructure")
        vm_type = st.selectbox(
            "Virtual Machine Type",
            ["VM with docker support - 16v CPUâ€™s, 64 GB RAM (minimum)", "Custom"]
        )

        instance_type = st.radio("Instance Type", ["Shared", "Dedicated"])
        vm_instances = st.number_input("Number of VM Instances", min_value=1, value=2)
        server_url = st.text_input("Server URL (optional)", "example.com")
        storage_amount = st.slider("Storage (GB)", min_value=10, max_value=1000, value=100, step=10)

        st.subheader("Frontend")
        frontend_framework = st.selectbox(
            "Frontend Framework",
            ["None", "HTML/CSS/JS", "React", "Angular", "Vue.js", "Custom Framework"]
        )

        st.subheader("Project Duration")
        duration_months = st.slider("Duration (months)", min_value=1, max_value=36, value=12)

        st.subheader("Gen AI Frameworks")
        gen_ai_backend = st.radio(
            "Select Backend Type",
            ["Opensource", "Framework Used"]
        )

        if gen_ai_backend == "Framework Used":
            st.subheader("Gen AI Framework Details")
            open_ai_service = st.selectbox(
                "Open AI Service",
                ["gpt-4o", "gpt-4o-mini", "o3-mini", "o1"]
            )
            parsing_data = st.selectbox(
                "Parsing Data",
                ["Llama Cloud", "MinerU", "MS MarktDown", "Custom"]
            )
            if parsing_data == "Custom":
                custom_parsing_url = st.text_input("Enter Custom Parsing Data URL")
            embeddings = st.selectbox(
                "Embeddings",
                ["OpenAI embeddings models", "Custom embeddings"]
            )
            if embeddings == "Custom embeddings":
                custom_embedding_url = st.text_input(
                    "Enter Custom Embedding Costing URL",
                    placeholder="e.g., https://example.com/custom_embeddings")
        else:
            # Default values for "Opensource"
            open_ai_service = "Opensource"
            parsing_data = "Opensource"
            embeddings = "Opensource"

        st.subheader("Backend (RestAPI)")
        backend_resources = st.selectbox(
            "Select Backend Resources",
            ["Python (FastAPI) + Typescript (NestJS)", "Custom"]
        )

        submitted = st.form_submit_button("Calculate Cost Estimate")

    if submitted:
        # Cost Calculation
        result = calculate_total_cost(
            vm_type, vm_instances, instance_type, storage_amount, frontend_framework,
            duration_months, gen_ai_backend, open_ai_service, parsing_data, embeddings, backend_resources
        )

        st.header("Project Configuration Summary")
        
        # Create a table for project configuration summary
        gen_ai_details = f"{gen_ai_backend}, Open AI: {open_ai_service}, Parsing: {parsing_data}, Embedding: {embeddings}"
        config_data = {
            "Parameter": ["VM Type", "Instance Type", "VM Instances", "Storage (GB)", "Server URL", "Frontend Framework", "Duration (months)", "Gen AI Framework"],
            "Value": [vm_type, instance_type, vm_instances, storage_amount, server_url, frontend_framework, duration_months, gen_ai_details]
        }
        config_df = pd.DataFrame(config_data)
        
        # Convert all values in the "Value" column to strings to avoid ArrowTypeError
        config_df["Value"] = config_df["Value"].apply(lambda x: str(x))
        
        st.table(config_df)

        # Cost Breakdown
        col1, col2 = st.columns([2, 1])
        with col1:
            st.header("Cost Breakdown")
            st.metric("Monthly Cost", f"${result['Monthly Cost']:.2f}")
            st.metric("Total Project Cost", f"${result['Total Project Cost']:.2f}")
        with col2:
            st.subheader("Monthly Breakdown")
            for key in ['VM Cost', 'Storage Cost', 'Frontend Cost', 'Gen AI Cost', 'Parsing Cost', 'Embedding Cost', 'Backend Cost']:
                st.write(f"**{key.replace('_', ' ')}:** ${result[key]:.2f}")

        # Visualization
        st.header("Cost Visualization")
        cost_df = pd.DataFrame({
            'Category': ['VM Infrastructure', 'Storage', 'Frontend Cost', 'Gen AI Cost', 'Parsing Cost', 'Embedding Cost', 'Backend Cost'],
            'Cost': [
                result['VM Cost'],
                result['Storage Cost'],
                result['Frontend Cost'],
                result['Gen AI Cost'],
                result['Parsing Cost'],
                result['Embedding Cost'],
                result['Backend Cost']
            ]
        })
        st.bar_chart(cost_df.set_index('Category'))

        # Export CSV
        st.download_button(
            label="Export Estimate as CSV",
            data=cost_df.to_csv().encode('utf-8'),
            file_name=f'project_cost_estimate_{datetime.datetime.now().strftime("%Y%m%d")}.csv',
            mime='text/csv',
        )

        # Disclaimer
        st.markdown("<p class='disclaimer'>This estimate is based on typical industry pricing and may vary depending on specific provider rates and additional services required.</p>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()