from pydantic import BaseModel
from typing import List, Optional

class LeaderboardItem(BaseModel):
    model_name: str
    win_rate: float
    avg_overall: float
    avg_prompt_adherence: float
    avg_visual_quality: float
    avg_indian_relevance: float
    avg_commercial_viability: float
    avg_product_focus: float
    avg_anatomical_correctness: float
    avg_lighting_consistency: float
    avg_fabric_realism: float
    avg_demographic_authenticity: float

class Statistics(BaseModel):
    total_images: int
    total_participants: int
    avg_overall: float
    current_leading_model: Optional[str]

class PromptResultModelStat(BaseModel):
    model_name: str
    avg_overall: float
    win_rate: float

class PromptResult(BaseModel):
    prompt_id: int
    prompt_text: str
    category: str
    use_case: str
    models: List[PromptResultModelStat]
