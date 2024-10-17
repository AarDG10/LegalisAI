import json
import re

def extract_key_info(summary):
    # Step 1: Extract key points and verdict from the summary
    # Regular expression to find verdicts and key phrases
    verdict_pattern = r'(?i)(verdict|held|court|decided|the court|concluded|finds|rules|order)'
    key_points = []
    
    # Splitting summary into sentences for processing
    sentences = re.split(r'(?<=[.!?]) +', summary)
    
    for sentence in sentences:
        if re.search(verdict_pattern, sentence):
            key_points.append(sentence.strip())
    
    # Join key points to form a cleaned summary
    cleaned_summary = ' '.join(key_points).strip()
    
    # Limit the summary to 350 characters
    if len(cleaned_summary) > 350:
        cleaned_summary = cleaned_summary[:350] + '...'  # Append ellipsis if truncated

    return cleaned_summary

def clean_and_summarize(record):
    # Extract title, date, and summary from the JSON record
    title = record.get('title', '')
    date = record.get('date', '')
    summary = record.get('summary', '')

    # Step 1: Clean and Extract Key Information
    cleaned_summary = extract_key_info(summary)

    # Step 2: Generate a Cleaned Summary
    summary_output = {
        'title': title,
        'date': date,
        'summary': cleaned_summary  # Only key points and verdict
    }

    return summary_output

input_file_path = '../spiders/data1.json'  # Path to your input JSON file
output_file_path = './cleaned_data.json'  # Path for the output JSON file

def summarize_json_file(input_file_path, output_file_path):
    # Load JSON data from a file
    with open(input_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    summaries = []
    for record in data:
        cleaned_summary = clean_and_summarize(record)
        summaries.append(cleaned_summary)

    # Write the summaries to a new JSON file
    with open(output_file_path, 'w', encoding='utf-8') as f:
        json.dump(summaries, f, ensure_ascii=False, indent=4)

# Example usage

summarize_json_file(input_file_path, output_file_path)

print(f'Summarized data written to {output_file_path}')
