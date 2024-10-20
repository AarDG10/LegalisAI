import streamlit as st
from transformers import AutoTokenizer, AutoModel
import torch
import json
import os

# Load the InLegalBERT model and tokenizer
@st.cache_resource
def load_model():
    model_name = "law-ai/InLegalBERT"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)
    return model, tokenizer

model, tokenizer = load_model()

# Load the legal sections from JSON
def load_legal_sections(file_path='../../Trainer/train_sections.json'):
    with open(file_path, 'r') as f:
        return json.load(f)

legal_sections = load_legal_sections()

# Streamlit UI
st.title("Legalis AI (Based on Jaccard Similarity)")

# User input for case description
case_description = st.text_area("Enter your legal case description:")

# Helper function to compute Jaccard similarity
def jaccard_similarity(tokens1, tokens2):
    set1, set2 = set(tokens1), set(tokens2)
    return len(set1.intersection(set2)) / len(set1.union(set2))

# Semantic search function using Jaccard similarity
def find_relevant_sections(case_description, legal_sections, model, tokenizer):
    case_inputs = tokenizer.tokenize(case_description)
    
    results = []
    for section in legal_sections:
        section_tokens = tokenizer.tokenize(section['text'])
        # Calculate Jaccard similarity
        similarity = jaccard_similarity(case_inputs, section_tokens)
        results.append((section['title'], section['text'], similarity))

    return sorted(results, key=lambda x: -x[2])[:5]  # Return top 5 matches (higher similarity)

def load_existing_data(file_path='../../Trainer/accuracy.json'):
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:  # Check if file exists and is not empty
        with open(file_path, 'r') as json_file:
            try:
                return json.load(json_file)
            except json.JSONDecodeError:
                st.error("Error decoding JSON, returning an empty list.")
                return []  # Return an empty list if JSON is invalid
    return []  # Return an empty list if the file doesn't exist or is empty

sect = load_existing_data() #picking up the sections to add in json file for comparison

# Run the search if button is pressed
if st.button("Find Relevant Legal Sections"):
    if case_description:
        relevant_sections = find_relevant_sections(case_description, legal_sections, model, tokenizer)
        for title, text, similarity in relevant_sections:
            sect.append(title)
            st.write(f"**Section**: {title}")
            st.write(f"**Text**: {text[:350]}...")  # Show the first 350 characters
            st.write(f"**Jaccard Similarity**: {similarity:.4f}")
    else:
        st.write("Please enter a case description.")


#Script to dump list into json for checking accuracy metric
with open('../../Trainer/accuracy.json', 'w') as json_file:
    json.dump(sect, json_file, indent=4)