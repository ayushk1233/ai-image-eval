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

def trigger_generation(prompt_id: int, model_name: str):
    url = f"{get_base_url()}/api/generations/"
    payload = {
        "prompt_id": prompt_id,
        "model_name": model_name
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()

def get_unrated_images(participant_id: int):
    url = f"{get_base_url()}/api/generations/unrated"
    params = {"participant_id": participant_id}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def submit_rating(participant_id: int, image_generation_id: int, prompt_adherence: int, visual_quality: int, indian_relevance: int, overall: int, comments: str = None):
    url = f"{get_base_url()}/api/ratings/"
    payload = {
        "participant_id": participant_id,
        "image_generation_id": image_generation_id,
        "prompt_adherence": prompt_adherence,
        "visual_quality": visual_quality,
        "indian_relevance": indian_relevance,
        "overall": overall,
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
