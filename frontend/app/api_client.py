import os
import requests
import streamlit as st

BACKEND_URL = os.environ.get("BACKEND_URL", "http://backend:8000")

def get_base_url():
    # If running locally without docker, you might want to use http://localhost:8000
    # but inside docker compose, "backend" resolves to the backend container.
    return BACKEND_URL

def register_participant(name: str, email: str, age: int, consent: bool):
    url = f"{get_base_url()}/api/participants/"
    payload = {
        "name": name,
        "email": email,
        "age": age,
        "consent": consent
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()

def get_prompts():
    url = f"{get_base_url()}/api/prompts/"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def login_participant(email_or_phone: str):
    url = f"{get_base_url()}/api/participants/login"
    response = requests.get(url, params={"email": email_or_phone})
    response.raise_for_status()
    return response.json()

def trigger_generation(model_name: str, prompt_id: int = None, custom_prompt: str = None, api_key: str = None, participant_id: int = None):
    url = f"{get_base_url()}/api/generations/"
    payload = {
        "model_name": model_name
    }
    if prompt_id is not None:
        payload["prompt_id"] = prompt_id
    if custom_prompt is not None:
        payload["custom_prompt"] = custom_prompt
    if api_key is not None:
        payload["api_key"] = api_key
    if participant_id is not None:
        payload["participant_id"] = participant_id
        
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()

def get_unrated_images(participant_id: int):
    url = f"{get_base_url()}/api/generations/unrated"
    params = {"participant_id": participant_id}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def get_participant_generations(participant_id: int):
    url = f"{get_base_url()}/api/generations/participant/{participant_id}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def submit_rating(
    participant_id: int, image_generation_id: int, 
    prompt_adherence: int, visual_quality: int, 
    indian_relevance: int, overall: int, 
    commercial_viability: int = 3, product_focus: int = 3, 
    anatomical_correctness: int = 3, lighting_consistency: int = 3, 
    fabric_realism: int = 3, demographic_authenticity: int = 3, 
    comments: str = None
):
    url = f"{get_base_url()}/api/ratings/"
    payload = {
        "participant_id": participant_id,
        "image_generation_id": image_generation_id,
        "prompt_adherence": prompt_adherence,
        "visual_quality": visual_quality,
        "indian_relevance": indian_relevance,
        "overall": overall,
        "commercial_viability": commercial_viability,
        "product_focus": product_focus,
        "anatomical_correctness": anatomical_correctness,
        "lighting_consistency": lighting_consistency,
        "fabric_realism": fabric_realism,
        "demographic_authenticity": demographic_authenticity,
        "comments": comments
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()

def get_statistics():
    url = f"{get_base_url()}/api/analytics/statistics"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def get_leaderboard():
    url = f"{get_base_url()}/api/analytics/leaderboard"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def get_results():
    url = f"{get_base_url()}/api/analytics/results"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def get_export_url():
    return f"{get_base_url()}/api/analytics/export"

def get_export_csv():
    url = f"{get_base_url()}/api/analytics/export"
    response = requests.get(url)
    response.raise_for_status()
    return response.content
