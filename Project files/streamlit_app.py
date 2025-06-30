import streamlit as st
import datetime
from langchain_ibm import WatsonxLLM
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# ✅ IBM Watsonx configuration - Replace with your actual credentials
WATSONX_URL = "https://us-south.ml.cloud.ibm.com"  # Replace with your actual URL
WATSONX_APIKEY = "v2pjUHPAm5HfLBGpVN5T1-DHjM3tbAVIzyQmEUhMS_0v"  # Replace with your actual API key
WATSONX_PROJECT_ID = "443a8ed4-48fd-4630-ab81-e5a5480dd375"  # Replace with your actual project ID


# Initialize IBM WatsonxLLM
@st.cache_resource
def initialize_llm():
    try:
        llm = WatsonxLLM(
            model_id="ibm/granite-13b-instruct-v2",
            url=WATSONX_URL,
            apikey=WATSONX_APIKEY,
            project_id=WATSONX_PROJECT_ID,
            params={
                "decoding_method": "greedy",
                "max_new_tokens": 500,
                "temperature": 0.7
            }
        )
        return llm
    except Exception as e:
        st.error(f"Failed to initialize IBM WatsonxLLM: {e}")
        return None


# Create LangChain prompt template
prompt_template = PromptTemplate(
    input_variables=["user_question"],
    template="""You are a smart city sustainability assistant. You help with questions about:
- Sustainable city planning and operations
- Energy efficiency and renewable energy
- Water management and conservation
- Waste management and recycling
- Air quality and pollution control
- Smart transportation systems
- Green building practices
- Environmental monitoring

User Question: {user_question}

Please provide a clear, helpful, and actionable response focused on sustainability and smart city solutions:"""
)

# Streamlit page config
st.set_page_config(
    page_title="🌆 Smart City Assistant",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dark Theme Styling
st.markdown("""
    <style>
    /* Main background and text colors */
    .stApp {
        background: linear-gradient(135deg, #0f1419 0%, #1a1f2e 100%);
        color: #ffffff;
    }

    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #1e2329 0%, #2b3139 100%);
    }

    /* Main content area */
    .main .block-container {
        background: rgba(30, 35, 41, 0.8);
        border-radius: 15px;
        padding: 2rem;
        margin-top: 1rem;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Headers styling */
    h1, h2, h3, h4, h5, h6 {
        color: #00d4ff !important;
        text-shadow: 0 0 10px rgba(0, 212, 255, 0.3);
    }

    /* Metrics styling */
    .metric-container {
        background: linear-gradient(135deg, #2d3748 0%, #4a5568 100%);
        border-radius: 10px;
        padding: 1rem;
        border: 1px solid rgba(0, 212, 255, 0.2);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }

    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6);
    }

    /* Input styling */
    .stTextInput > div > div > input {
        background: rgba(45, 55, 72, 0.8);
        color: white;
        border: 1px solid rgba(0, 212, 255, 0.3);
        border-radius: 10px;
    }

    /* Sidebar radio buttons */
    .stRadio > div {
        background: rgba(45, 55, 72, 0.5);
        border-radius: 10px;
        padding: 1rem;
    }

    /* Success/Error messages */
    .stSuccess {
        background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);
        border-radius: 10px;
        border: none;
    }

    .stError {
        background: linear-gradient(135deg, #f56565 0%, #e53e3e 100%);
        border-radius: 10px;
        border: none;
    }

    .stWarning {
        background: linear-gradient(135deg, #ed8936 0%, #dd6b20 100%);
        border-radius: 10px;
        border: none;
    }

    .stInfo {
        background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%);
        border-radius: 10px;
        border: none;
    }

    /* Chart styling */
    .stPlotlyChart {
        background: rgba(45, 55, 72, 0.8);
        border-radius: 15px;
        padding: 1rem;
        border: 1px solid rgba(0, 212, 255, 0.2);
    }

    /* Markdown text */
    .stMarkdown {
        color: #e2e8f0;
    }

    /* Spinner */
    .stSpinner {
        color: #00d4ff;
    }

    /* Footer */
    .footer {
        background: linear-gradient(135deg, #1a202c 0%, #2d3748 100%);
        padding: 1rem;
        border-radius: 10px;
        border-top: 2px solid #00d4ff;
        margin-top: 2rem;
    }

    /* Glowing effects */
    .glow {
        animation: glow 2s ease-in-out infinite alternate;
    }

    @keyframes glow {
        from { text-shadow: 0 0 5px #00d4ff, 0 0 10px #00d4ff, 0 0 15px #00d4ff; }
        to { text-shadow: 0 0 10px #00d4ff, 0 0 20px #00d4ff, 0 0 30px #00d4ff; }
    }

    /* Date input styling */
    .stDateInput > div > div > input {
        background: rgba(45, 55, 72, 0.8);
        color: white;
        border: 1px solid rgba(0, 212, 255, 0.3);
        border-radius: 10px;
    }

    /* Selectbox styling */
    .stSelectbox > div > div > div {
        background: rgba(45, 55, 72, 0.8);
        color: white;
        border: 1px solid rgba(0, 212, 255, 0.3);
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize LLM
llm = initialize_llm()

# Sidebar
st.sidebar.title("🔧 Menu")
menu = st.sidebar.radio("Go to", ["🏠 Home", "💬 Ask Assistant", "📊 City Dashboard", "📑 Reports", "🧠 About"])

# 🏠 Home Page
if menu == "🏠 Home":
    st.markdown('<h1 class="glow">🌇 Welcome to the Sustainable Smart City Assistant</h1>', unsafe_allow_html=True)
    st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(0, 212, 255, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%); 
                    padding: 2rem; border-radius: 15px; border: 1px solid rgba(0, 212, 255, 0.2);">
        This assistant helps make your city smarter and greener using IBM Watson AI! 🌱

        #### 🔍 What You Can Do:
        - 💬 Chat with an AI assistant about sustainability
        - 📊 See live city data like pollution or energy use
        - 📑 Generate smart reports for planning
        - ⚡ Get tips for saving water, electricity, and more!
        </div>
    """, unsafe_allow_html=True)
    st.image("https://cdn.pixabay.com/photo/2018/04/12/20/01/smart-city-3314705_960_720.jpg", width=700)

# 💬 AI Assistant
elif menu == "💬 Ask Assistant":
    st.header("🧠 Chat with Smart Assistant (Powered by IBM Watson)")
    st.markdown("Ask anything about sustainability, smart living, or city operations.")

    user_input = st.text_input("🗣 Type your question here:")

    if st.button("🚀 Ask Now"):
        if user_input.strip() == "":
            st.warning("❗ Please enter a question.")
        elif llm is None:
            st.error("❌ IBM WatsonxLLM is not properly configured. Please check your credentials.")
        else:
            with st.spinner("🤖 Thinking with IBM Watson AI..."):
                try:
                    # Create LangChain chain
                    chain = LLMChain(llm=llm, prompt=prompt_template)

                    # Generate response
                    response = chain.run(user_question=user_input)

                    st.success("🤖 Assistant says:")
                    st.write(response)

                except Exception as e:
                    st.error(f"⚠ Something went wrong: {e}")
                    st.info("Please make sure your IBM Watson credentials are correctly configured.")

# 📊 Dashboard
elif menu == "📊 City Dashboard":
    st.markdown('<h2 class="glow">📊 Live City Data</h2>', unsafe_allow_html=True)
    st.markdown("Visualize important metrics to monitor sustainability progress.")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
            <div class="metric-container">
                <h3>🌡 Air Quality Index</h3>
                <h1 style="color: #48bb78;">85</h1>
                <p style="color: #68d391;">↓ 5 from yesterday</p>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
            <div class="metric-container">
                <h3>⚡ Electricity Usage (MW)</h3>
                <h1 style="color: #f6ad55;">320</h1>
                <p style="color: #fc8181;">↑ 12 from last week</p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <div class="metric-container">
                <h3>💧 Water Usage (ML)</h3>
                <h1 style="color: #4299e1;">1200</h1>
                <p style="color: #68d391;">↓ 50 from last month</p>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
            <div class="metric-container">
                <h3>🗑 Waste Collected (Tons)</h3>
                <h1 style="color: #ed8936;">200</h1>
                <p style="color: #fc8181;">↑ 10 from last week</p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("#### 📈 Weekly Trend")
    st.line_chart([100, 120, 140, 130, 150, 160])

    # Add AI-powered insights
    if st.button("🤖 Get AI Insights on Dashboard Data"):
        if llm is None:
            st.error("❌ IBM WatsonxLLM is not properly configured.")
        else:
            with st.spinner("🤖 Analyzing city data with AI..."):
                try:
                    insight_prompt = PromptTemplate(
                        input_variables=["data"],
                        template="""As a smart city sustainability expert, analyze this city data and provide insights:

Air Quality Index: 85 (improved by 5 from yesterday)
Electricity Usage: 320 MW (increased by 12 MW from last week)
Water Usage: 1200 ML (decreased by 50 ML from last month)
Waste Collected: 200 Tons (increased by 10 tons from last week)

Provide 3-4 key insights and recommendations for city planners:"""
                    )

                    insight_chain = LLMChain(llm=llm, prompt=insight_prompt)
                    insights = insight_chain.run(data="city_metrics")

                    st.success("🔍 AI Insights:")
                    st.write(insights)

                except Exception as e:
                    st.error(f"⚠ Failed to generate insights: {e}")

# 📑 Reports Page
elif menu == "📑 Reports":
    st.header("📑 Generate Sustainability Report")
    st.markdown("📅 Select the date range for which you want the report.")

    start = st.date_input("Start Date", datetime.date(2025, 6, 1))
    end = st.date_input("End Date", datetime.date(2025, 6, 19))

    if start > end:
        st.error("❌ Start date must be before end date.")
    elif st.button("📄 Generate Report"):
        st.info("🔍 Analyzing data...")
        st.success("✅ Report generated successfully!")
        st.markdown("""
            #### 📝 Report Summary:
            - ✅ Pollution levels are within safe limits
            - ⚡ Power usage has increased by 5%
            - 💧 Water consumption has dropped by 4%
            - 🗑 Waste generation slightly increased
        """)

        # Add AI-generated report enhancement
        if st.button("🤖 Enhance Report with AI Analysis"):
            if llm is None:
                st.error("❌ IBM WatsonxLLM is not properly configured.")
            else:
                with st.spinner("🤖 Generating detailed AI analysis..."):
                    try:
                        report_prompt = PromptTemplate(
                            input_variables=["period"],
                            template="""Generate a detailed sustainability report analysis for a smart city covering the period from {period}. 

Based on these metrics:
- Pollution levels: within safe limits
- Power usage: increased by 5%
- Water consumption: decreased by 4%
- Waste generation: slightly increased

Provide:
1. Executive summary
2. Key findings and trends
3. Recommendations for improvement
4. Future action items

Make it professional and actionable for city planners:"""
                        )

                        report_chain = LLMChain(llm=llm, prompt=report_prompt)
                        period = f"{start} to {end}"
                        detailed_report = report_chain.run(period=period)

                        st.success("📊 Enhanced AI Report:")
                        st.write(detailed_report)

                    except Exception as e:
                        st.error(f"⚠ Failed to generate enhanced report: {e}")

# 🧠 About Page
elif menu == "🧠 About":
    st.title("ℹ About This Project")
    st.markdown("""
        This project is part of the *SmartInternz Internship Program*.

        ### 🎯 Objective:
        Build an AI-powered assistant that helps city planners and citizens:
        - Understand sustainability data
        - Improve smart city decisions
        - Ask questions and get intelligent responses

        ### 🛠 Tech Stack:
        - 🤖 **IBM WatsonxLLM** (Granite-13B-Instruct-V2)
        - 🔗 **LangChain** (For prompt management)
        - 🌐 **Streamlit** (Frontend)
        - 🔁 REST API (Backend integration ready)
        - 📦 Pinecone (Semantic Search - can be integrated)
        - 🧠 ML Models (Forecasting, Anomaly Detection)

        ### 🔧 Configuration Required:
        Make sure to update these variables in the code:
        - `WATSONX_URL`: Your IBM Watson URL
        - `WATSONX_APIKEY`: Your IBM Watson API key  
        - `WATSONX_PROJECT_ID`: Your Watson project ID

        ---
        👨‍💻 Created by passionate interns using IBM Watson AI.
    """)

# Footer
st.markdown("---")
st.markdown(
    "🚀 *Sustainable Smart City Assistant* • 2025 • Powered by IBM Watson • Built with ❤ by SmartInternz Interns")
