import streamlit as st

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq


# ============================================================
# PAGE SETTINGS
# ============================================================

st.set_page_config(
    page_title="ScamGuardian",
    page_icon="🛡️",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
<style>

/* ============================================================
   FULL SCREEN BACKGROUND
   ============================================================ */

html,
body,
[data-testid="stAppViewContainer"],
[data-testid="stApp"] {

    min-height: 100vh !important;
}


.stApp {

    background:
        radial-gradient(
            circle at top,
            #3b176b 0%,
            #171126 45%,
            #08070d 100%
        );

    color: white;

    min-height: 100vh !important;
}


/* Remove white Streamlit header */

[data-testid="stHeader"] {

    background: transparent !important;
}


/* Main application area */

[data-testid="stAppViewContainer"] {

    background: transparent !important;

    min-height: 100vh !important;
}


/* ============================================================
   MAIN CONTAINER
   ============================================================ */

.block-container {

    max-width: 1400px !important;

    width: 100% !important;

    min-height: 100vh !important;

    padding-top: 25px !important;

    padding-left: 5% !important;

    padding-right: 5% !important;

    padding-bottom: 40px !important;
}


/* ============================================================
   TITLE
   ============================================================ */

.title-text {

    text-align: center;

    font-size: 42px;

    font-weight: 800;

    color: #ffffff;

    margin-top: 0px;

    margin-bottom: 4px;

    letter-spacing: 0.5px;
}


/* ============================================================
   SUBTITLE
   ============================================================ */

.subtitle-text {

    text-align: center;

    font-size: 16px;

    color: #cfc7df;

    margin-top: 0px;

    margin-bottom: 10px;
}


/* ============================================================
   TEXT AREA
   ============================================================ */

.stTextArea {

    margin-top: 0px !important;

    padding-top: 0px !important;
}


/* Text area label */

.stTextArea label,
.stTextArea label p {

    color: #ffffff !important;

    font-size: 16px !important;

    font-weight: 600 !important;
}


/* Text box */

.stTextArea textarea,
[data-baseweb="textarea"] textarea {

    background-color: #ffffff !important;

    color: #000000 !important;

    -webkit-text-fill-color: #000000 !important;

    caret-color: #000000 !important;

    border-radius: 12px !important;

    border: 1px solid #d6c7ee !important;

    font-size: 16px !important;

    line-height: 1.5 !important;

    padding: 14px !important;
}


/* Placeholder */

.stTextArea textarea::placeholder,
[data-baseweb="textarea"] textarea::placeholder {

    color: #777777 !important;

    -webkit-text-fill-color: #777777 !important;

    opacity: 1 !important;
}


/* Text box focus */

.stTextArea textarea:focus,
[data-baseweb="textarea"] textarea:focus {

    color: #000000 !important;

    -webkit-text-fill-color: #000000 !important;

    border: 2px solid #9b5de5 !important;

    box-shadow:
        0 0 0 3px
        rgba(155, 93, 229, 0.20) !important;
}


/* ============================================================
   BUTTON
   ============================================================ */

.stButton {

    margin-top: 5px !important;
}


.stButton > button {

    width: 100%;

    border-radius: 12px;

    border: none;

    padding: 12px 20px;

    font-size: 16px;

    font-weight: 700;

    color: white;

    background:
        linear-gradient(
            90deg,
            #7b2cbf,
            #9d4edd
        );

    transition: 0.3s;
}


.stButton > button:hover {

    background:
        linear-gradient(
            90deg,
            #9d4edd,
            #c77dff
        );

    color: white;

    transform: translateY(-1px);
}


/* ============================================================
   RESULT CARD
   ============================================================ */

.result-card {

    background:
        rgba(255, 255, 255, 0.07);

    border:
        1px solid rgba(255, 255, 255, 0.12);

    border-radius: 15px;

    padding: 22px;

    margin-top: 20px;
}


/* ============================================================
   HIGH RISK
   ============================================================ */

.risk-high {

    display: inline-block;

    background: #dc2626;

    color: white;

    padding: 7px 15px;

    border-radius: 20px;

    font-weight: 700;

    margin-bottom: 15px;
}


/* ============================================================
   MEDIUM RISK
   ============================================================ */

.risk-medium {

    display: inline-block;

    background: #d97706;

    color: white;

    padding: 7px 15px;

    border-radius: 20px;

    font-weight: 700;

    margin-bottom: 15px;
}


/* ============================================================
   LOW RISK
   ============================================================ */

.risk-low {

    display: inline-block;

    background: #16a34a;

    color: white;

    padding: 7px 15px;

    border-radius: 20px;

    font-weight: 700;

    margin-bottom: 15px;
}


/* ============================================================
   RESULT HEADING
   ============================================================ */

.result-heading {

    color: #d8b4fe;

    font-weight: 700;

    font-size: 18px;

    margin-top: 10px;

    margin-bottom: 12px;
}


/* ============================================================
   RESULT TEXT
   ============================================================ */

.result-text {

    color: #f5f3f7;

    font-size: 15px;

    line-height: 1.7;
}


/* ============================================================
   SOURCES
   ============================================================ */

.sources-title {

    color: #e9d5ff;

    font-size: 17px;

    font-weight: 700;

    margin-top: 25px;

    margin-bottom: 5px;
}


/* ============================================================
   SPINNER
   ============================================================ */

.stSpinner > div {

    color: #c084fc !important;
}

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="title-text">🛡️ ScamGuardian</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle-text">'
    'AI-powered scam message detection using RAG'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# LOAD RAG PIPELINE
# ============================================================

@st.cache_resource
def load_pipeline():

    # Load knowledge-base files

    loader = DirectoryLoader(
        "policy_data",
        glob="*.txt",
        loader_cls=TextLoader
    )

    documents = loader.load()


    # Split documents

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_documents(documents)


    # Create embeddings

    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )


    # Create vector database

    vectordb = Chroma.from_documents(
        chunks,
        embeddings
    )


    # Groq LLM

    llm = ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=0,
        groq_api_key=st.secrets["GROQ_API_KEY"]
    )


    return vectordb, llm


# ============================================================
# START PIPELINE
# ============================================================

try:

    vectordb, llm = load_pipeline()

except Exception as e:

    st.error(
        "Unable to load ScamGuardian. "
        "Please check your policy_data folder and API key."
    )

    st.stop()


# ============================================================
# USER MESSAGE
# ============================================================

user_input = st.text_area(

    "Enter a suspicious message:",

    placeholder=(
        "Example: Congratulations! You have won ₹25,00,000. "
        "Click this link and pay ₹500 processing fee..."
    ),

    height=180
)


# ============================================================
# CHECK MESSAGE
# ============================================================

if st.button("🔍 Check Message"):

    if not user_input.strip():

        st.warning(
            "Please enter a message to check."
        )

    else:

        with st.spinner("Analyzing message..."):

            # Retrieve relevant knowledge

            retriever = vectordb.as_retriever(
                search_kwargs={"k": 3}
            )

            docs = retriever.invoke(user_input)


            # Create context

            context = "\n\n".join(
                doc.page_content
                for doc in docs
            )


            # =================================================
            # AI PROMPT
            # =================================================

            prompt = f"""
You are ScamGuardian, an AI scam detection assistant.

Use the knowledge base below to analyze the user's message.

KNOWLEDGE BASE:
{context}

USER MESSAGE:
"{user_input}"

Determine whether this message is a scam.

Give the answer in exactly this format:

SCAM TYPE: [type of scam]

RISK LEVEL: [Low / Medium / High]

WHY IS IT A SCAM:
[Explain in 2-3 simple sentences why the message is suspicious.
If it appears safe, explain why.]

WHAT TO DO:
- [Action 1]
- [Action 2]
- [Action 3]

WHAT NOT TO DO:
- [Thing the user should not do]
- [Thing the user should not do]
- [Thing the user should not do]

Keep the answer simple and easy to understand.

Do not use HTML.

Do not put the answer inside a code block.

Do not add extra sections.
"""


            # Get response

            response = llm.invoke(prompt)

            answer = response.content


        # ====================================================
        # DETERMINE RISK
        # ====================================================

        risk = "Medium"

        for line in answer.splitlines():

            if line.strip().upper().startswith("RISK LEVEL"):

                if "HIGH" in line.upper():

                    risk = "High"

                elif "LOW" in line.upper():

                    risk = "Low"

                else:

                    risk = "Medium"


        # ====================================================
        # RISK BADGE
        # ====================================================

        if risk == "High":

            badge = (
                '<div class="risk-high">'
                '🔴 HIGH RISK'
                '</div>'
            )

        elif risk == "Low":

            badge = (
                '<div class="risk-low">'
                '🟢 LOW RISK'
                '</div>'
            )

        else:

            badge = (
                '<div class="risk-medium">'
                '🟠 MEDIUM RISK'
                '</div>'
            )


        # ====================================================
        # DISPLAY RESULT
        # ====================================================

        st.markdown(
            f'<div class="result-card">'
            f'{badge}'
            f'<div class="result-heading">'
            f'ScamGuardian Analysis'
            f'</div>'
            f'<div class="result-text">'
            f'{answer.replace(chr(10), "<br>")}'
            f'</div>'
            f'</div>',
            unsafe_allow_html=True
        )


        # ====================================================
        # KNOWLEDGE BASE SOURCES
        # ====================================================

        st.markdown(
            '<div class="sources-title">'
            '📚 Knowledge Base Sources'
            '</div>',
            unsafe_allow_html=True
        )


        with st.expander("View knowledge sources"):

            for i, doc in enumerate(
                docs,
                start=1
            ):

                st.markdown(
                    f"**Source {i}**"
                )

                st.write(
                    doc.page_content
                )

                st.divider()