import streamlit as st
import requests
import time

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="Power AI BI",
    page_icon="📊",
    layout="wide"
)

# =====================================================
# PREMIUM CSS
# =====================================================
st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: 'Segoe UI', sans-serif;
}

/* ================================================= */
/* MAIN APP */
/* ================================================= */

.stApp {
    background-color: #0f172a;
    color: white;
}

/* ================================================= */
/* TITLES */
/* ================================================= */

h1, h2, h3 {
    color: #f8fafc;
}

/* ================================================= */
/* SIDEBAR */
/* ================================================= */

section[data-testid="stSidebar"] {
    background-color: #111827;
    border-right: 1px solid #1e293b;
}

/* ================================================= */
/* KPI CARDS */
/* ================================================= */

[data-testid="metric-container"] {

    background: linear-gradient(
        145deg,
        #1e293b,
        #0f172a
    );

    border: 1px solid #334155;

    padding: 18px;

    border-radius: 18px;

    box-shadow:
        0 4px 12px rgba(0,0,0,0.25);

    transition: 0.3s ease-in-out;

    min-height: 110px;
}

[data-testid="metric-container"]:hover {

    transform: translateY(-3px);

    border: 1px solid #38bdf8;
}

/* KPI LABEL */
[data-testid="metric-container"] label {

    color: #cbd5e1 !important;

    font-size: 13px !important;

    font-weight: 600 !important;

    text-transform: uppercase;

    letter-spacing: 0.5px;
}

/* KPI VALUE */
[data-testid="metric-container"] [data-testid="stMetricValue"] {

    color: white;

    font-size: 28px !important;

    font-weight: bold;
}

/* ================================================= */
/* RESULT CARDS */
/* ================================================= */

.card {

    background: #1e293b;

    border: 1px solid #334155;

    padding: 16px;

    border-radius: 14px;

    margin-top: 10px;
    margin-bottom: 10px;

    box-shadow:
        0px 3px 8px rgba(0,0,0,0.25);

    line-height: 1.6;
}

/* ================================================= */
/* CHAT */
/* ================================================= */

.user-bubble {

    background: #2563eb;

    padding: 12px 16px;

    border-radius: 18px;

    color: white;
}

.bot-bubble {

    background: #1e293b;

    padding: 12px 16px;

    border-radius: 18px;

    color: white;
}

/* ================================================= */
/* EXPANDER */
/* ================================================= */

.streamlit-expanderHeader {

    background-color: #1e293b !important;

    border-radius: 10px !important;
}

/* ================================================= */
/* CHART IMAGE */
/* ================================================= */

img {

    border-radius: 16px;

    border: 1px solid #334155;

    margin-top: 10px;

    margin-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# HEADER
# =====================================================
st.title("🤖 Power AI BI")

st.caption(
    "AI Powered Business Intelligence & Analytics Platform"
)

# =====================================================
# SESSION
# =====================================================
if "messages" not in st.session_state:
    st.session_state.messages = []

# =====================================================
# SIDEBAR
# =====================================================
with st.sidebar:

    st.header("⚙️ Controls")

    db_choice = st.selectbox(
        "Database",
        ["mysql", "postgresql"]
    )

    enable_ai = st.toggle(
        "Enable Deep AI Insights (Slower)",
        value=False
    )

    uploaded_file = st.file_uploader(
        "Upload Data",
        type=["csv", "xlsx", "pdf", "docx", "txt", "pptx", "ppt"]
    )

    # =================================================
    # AUTO FILE DETACH
    # =================================================
    if uploaded_file is None:

        try:
            requests.post(
                "http://127.0.0.1:5000/file/detach"
            )
        except:
            pass

    # =================================================
    # CLEAR CHAT
    # =================================================
    if st.button("🧹 Clear Chat"):

        st.session_state.messages = []

        st.rerun()

# =====================================================
# CHAT HISTORY
# =====================================================
for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):

        st.markdown(msg["content"])

# =====================================================
# CHAT INPUT
# =====================================================
prompt = st.chat_input(
    "Ask something like 'Top 5 products by sales'..."
)

# =====================================================
# QUERY
# =====================================================
if prompt:

    # =================================================
    # USER MESSAGE
    # =================================================
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    # =================================================
    # ASSISTANT RESPONSE
    # =================================================
    with st.chat_message("assistant"):

        placeholder = st.empty()

        full_text = ""

        try:

            with st.spinner("Analyzing data..."):

                # =====================================
                # API CALL
                # =====================================
                if uploaded_file:

                    files = {
                        "file": (
                            uploaded_file.name,
                            uploaded_file.getvalue()
                        )
                    }

                    res = requests.post(
                        "http://127.0.0.1:5000/query",
                        data={
                            "question": prompt,
                            "database": db_choice,
                            "enable_ai": str(enable_ai)
                        },
                        files=files
                    )

                else:

                    res = requests.post(
                        "http://127.0.0.1:5000/query",
                        json={
                            "question": prompt,
                            "database": db_choice,
                            "enable_ai": enable_ai
                        }
                    )

                response = res.json()
            
            # =================================================
            # CHAT BOT RESPONSE
            # =================================================
            if response.get("type") == "chat":
                full_text = response.get("message", "")

            # =================================================
            # KPI SUMMARY
            # =================================================
            if "summary" in response:

                st.markdown("## 📊 Dashboard Summary")

                summary_items = list(
                    response["summary"].items()
                )

                # =============================================
                # LIMIT KPI COUNT
                # =============================================
                summary_items = summary_items[:6]

                cols = st.columns(3)

                for idx, (k, v) in enumerate(summary_items):

                    with cols[idx % 3]:

                        st.metric(
                            label=k.replace("_", " ").title(),
                            value=v
                        )

            # =================================================
            # SQL
            # =================================================
            if "sql" in response:

                with st.expander(
                    "🔍 Generated SQL Query"
                ):

                    st.code(
                        response["sql"],
                        language="sql"
                    )

            # =================================================
            # CHART
            # =================================================
            if response.get("chart_path"):

                st.markdown(
                    "## 📈 Analytics Visualization"
                )

                st.image(
                    response["chart_path"],
                    use_container_width=True
                )

            # =================================================
            # FORECAST
            # =================================================
            if response.get("type") == "forecast":

                st.markdown(
                    "## 🔮 Forecast Analysis"
                )

                # =============================================
                # HISTORICAL
                # =============================================
                if response.get("historical"):

                    st.markdown(
                        "### 📊 Historical Data"
                    )

                    for item in response["historical"]:

                        st.markdown(
                            f"<div class='card'>{item}</div>",
                            unsafe_allow_html=True
                        )

                        full_text += item + "\n"

                # =============================================
                # FORECAST
                # =============================================
                if response.get("forecast"):

                    st.markdown(
                        "### 🚀 Forecast Data"
                    )

                    for item in response["forecast"]:

                        st.markdown(
                            f"<div class='card'>{item}</div>",
                            unsafe_allow_html=True
                        )

                        full_text += item + "\n"

            # =================================================
            # RESULTS
            # =================================================
            if "data" in response:

                st.markdown("## 📄 Results")

                for row in response["data"]:

                    st.markdown(
                        f"<div class='card'>{row}</div>",
                        unsafe_allow_html=True
                    )

                    full_text += row + "\n"

            # =================================================
            # INSIGHTS
            # =================================================
            if "insight" in response:

                st.markdown("## 🧠 AI Insights")

                insights = response["insight"]

                if isinstance(insights, list):

                    for item in insights:

                        st.success(item)

                        full_text += item + "\n"

                else:

                    st.success(insights)

                    full_text += insights + "\n"

            # =================================================
            # DASHBOARD INSIGHTS
            # =================================================
            if (
                "dashboard" in response
                and "insights" in response["dashboard"]
            ):

                st.markdown(
                    "## 🚀 Business Insights"
                )

                for item in response["dashboard"]["insights"]:

                    st.info(item)

                    full_text += item + "\n"

            # =================================================
            # RECOMMENDATIONS
            # =================================================
            if (
                "dashboard" in response
                and "recommendations" in response["dashboard"]
            ):

                st.markdown(
                    "## 🎯 Recommendations"
                )

                for item in response["dashboard"]["recommendations"]:

                    st.warning(item)

                    full_text += item + "\n"

            # =================================================
            # TYPING EFFECT
            # =================================================
            typed = ""

            for char in full_text:

                typed += char

                placeholder.markdown(typed)

                time.sleep(0.0005)

            # =================================================
            # STORE MESSAGE
            # =================================================
            st.session_state.messages.append({
                "role": "assistant",
                "content": (
                    full_text
                    if full_text
                    else "Done ✅"
                )
            })

        except Exception as e:

            st.error(str(e))