import streamlit as st
import requests


API_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="DocMind",
    page_icon="🧠",
    layout="centered"
)

# Conversation memory
if "messages" not in st.session_state:
    st.session_state["messages"] = []


# -----------------------------
# Header
# -----------------------------

st.title("🧠 DocMind")

st.markdown(
    "### Intelligent Document Q&A using Retrieval-Augmented Generation"
)

st.caption(
    "Upload a document, then ask questions about its contents."
)

st.divider()


# -----------------------------
# Document Upload
# -----------------------------

st.header("📄 Document")

uploaded_file = st.file_uploader(
    "Upload a PDF document",
    type=["pdf"]
)


if uploaded_file is not None:

    st.info(
        f"Selected document: **{uploaded_file.name}**"
    )

    if st.button(
        "⚙️ Process Document",
        use_container_width=True
    ):

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                "application/pdf"
            )
        }

        with st.spinner(
            "Extracting, chunking, embedding and indexing document..."
        ):

            try:

                response = requests.post(
                    f"{API_URL}/upload",
                    files=files
                )

                if response.status_code == 200:

                    result = response.json()

                    st.session_state["document_processed"] = True
                    st.session_state["document_name"] = uploaded_file.name
                    st.session_state["document_id"] = result["document_id"]

                    # Start a fresh conversation for the newly selected document
                    st.session_state["messages"] = []

                    st.success(
                        f"✅ Document processed successfully — "
                        f"{result['pages']} page(s), "
                        f"{result['chunks']} chunks."
                    )

                else:

                    st.error(
                        f"Processing failed: {response.text}"
                    )

            except requests.exceptions.ConnectionError:

                st.error(
                    "Could not connect to the FastAPI server. "
                    "Make sure Uvicorn is running on port 8000."
                )


# -----------------------------
# Question Answering
# -----------------------------

st.divider()

# -----------------------------
# Conversation History
# -----------------------------

if st.session_state["messages"]:

    st.subheader("💬 Conversation")

    for message in st.session_state["messages"]:

        if message["role"] == "user":

            st.markdown(
                f"**You:** {message['content']}"
            )

        else:

            st.markdown(
                f"**DocMind:** {message['content']}"
            )

st.header("💬 Ask a Question")

if not st.session_state.get(
    "document_processed",
    False
):

    st.warning(
        "Please upload and process a document first."
    )

else:

    st.success(
        f"📚 Ready to answer questions about "
        f"**{st.session_state['document_name']}**"
    )

    question = st.text_input(
        "What would you like to know?"
    )

    if st.button(
        "🔍 Ask Question",
        use_container_width=True
    ):

        if not question.strip():

            st.warning(
                "Please enter a question."
            )

        else:

            with st.spinner(
                "Searching the document and generating an answer..."
            ):

                try:

                    response = requests.post(
                        f"{API_URL}/ask",
                        json={
                            "question": question ,
                             "document_id": st.session_state["document_id"],
                            "history": st.session_state["messages"] 
                        }
                    )

                    if response.status_code == 200:

                        result = response.json()

                        st.subheader("Answer")

                        answer = result["answer"]

                        # Save conversation
                        st.session_state["messages"].append({
                             "role": "user",
                             "content": question
                        })

                        st.session_state["messages"].append({
                         "role": "assistant",
                         "content": answer
                        })

                        st.subheader("Answer")

                        st.write(answer)


                        if result.get("sources"):

                            st.subheader("📚 Sources")

                            for source in result["sources"]:

                                st.markdown(
                                    f"📄 **{source['source']}** — "
                                             f"Page {source['page']}"
                                )
                    else:

                        st.error(
                            f"Request failed: {response.text}"
                        )

                except requests.exceptions.ConnectionError:

                    st.error(
                        "Could not connect to the FastAPI server."
                    )