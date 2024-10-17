import streamlit as st
from transformers import AutoTokenizer, AutoModel
import torch
import json

# Load the InLegalBERT model and tokenizer
@st.cache_resource
def load_model():
    model_name = "law-ai/InLegalBERT"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)
    return model, tokenizer

model, tokenizer = load_model()

# Load the legal sections from JSON
def load_legal_sections(file_path='../Trainer/train_sections.json'):
    with open(file_path, 'r') as f:
        return json.load(f)

legal_sections = load_legal_sections()

# Streamlit UI
st.title("Legalis AI")

# User input for case description
case_description = st.text_area("Enter your legal case description:")

# Semantic search function using BERT embeddings
def find_relevant_sections(case_description, legal_sections, model, tokenizer):
    case_inputs = tokenizer(case_description, return_tensors='pt', truncation=True, padding=True)
    with torch.no_grad():
        case_embedding = model(**case_inputs).last_hidden_state.mean(dim=1)

    results = []
    for section in legal_sections:
        section_inputs = tokenizer(section['text'], return_tensors='pt', truncation=True, padding=True)
        with torch.no_grad():
            section_embedding = model(**section_inputs).last_hidden_state.mean(dim=1)
        similarity = torch.cosine_similarity(case_embedding, section_embedding).item()
        results.append((section['title'], section['text'], similarity))

    return sorted(results, key=lambda x: -x[2])[:5]  # Return top 5 matches

# Run the search if button is pressed
if st.button("Find Relevant Legal Sections"):
    if case_description:
        relevant_sections = find_relevant_sections(case_description, legal_sections, model, tokenizer)
        for title, text, score in relevant_sections:
            st.write(f"**Section**: {title}")
            st.write(f"**Text**: {text[:350]}...")  # Show the first 350 characters
            st.write(f"**Similarity Score**: {score:.4f}")
    else:
        st.write("Please enter a case description.")
