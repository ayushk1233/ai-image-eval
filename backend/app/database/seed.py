from sqlalchemy.orm import Session
from backend.app.database.session import SessionLocal
from backend.app.models.prompt import Prompt

# Hardcoded prompts for E-commerce Fashion Product Photography
PROMPTS_DATA = [
    {"prompt_text": "A young Indian woman wearing a red Banarasi silk saree, standing in a brightly lit Diwali setting with diyas, high-fashion product photography, 4k, photorealistic", "category": "E-commerce Fashion", "use_case": "Diwali Saree Marketing"},
    {"prompt_text": "A handsome Indian man in a navy blue embroidered Kurta pajama, posing elegantly against a festive marigold background, e-commerce catalog style, 8k resolution", "category": "E-commerce Fashion", "use_case": "Festive Menswear"},
    {"prompt_text": "Close-up of a modern Indian bride wearing a pastel lehenga with intricate zari work, soft glowing wedding decor in the background, studio lighting, highly detailed", "category": "E-commerce Fashion", "use_case": "Bridal Lehenga Showcase"},
    {"prompt_text": "An Indian woman in a vibrant yellow salwar kameez twirling, festive Holi background with subtle colors in the air, joyous expression, professional fashion shoot", "category": "E-commerce Fashion", "use_case": "Holi Festival Collection"},
    {"prompt_text": "A male model wearing a sleek black Nehru jacket over a white kurta, standing in a modern luxury apartment, sharp focus, fashion magazine editorial style", "category": "E-commerce Fashion", "use_case": "Luxury Menswear"},
    {"prompt_text": "A graceful South Indian woman in a green Kanjeevaram saree with gold jewelry, traditional temple architecture in the background, cinematic lighting, 8k", "category": "E-commerce Fashion", "use_case": "South Indian Traditional"},
    {"prompt_text": "A couple wearing matching pastel ethnic wear, laughing together in a well-lit studio with minimal floral decor, perfect for Valentine's ethnic collection", "category": "E-commerce Fashion", "use_case": "Couples Ethnic Wear"},
    {"prompt_text": "An elderly Indian man looking distinguished in a classic white dhoti and silk kurta, sitting in a heritage haveli courtyard, natural sunlight, highly detailed", "category": "E-commerce Fashion", "use_case": "Heritage Collection"},
    {"prompt_text": "A young Indian girl in a pink chaniya choli ready for Navratri garba, holding dandiya sticks, dynamic pose, colorful background, professional studio photography", "category": "E-commerce Fashion", "use_case": "Navratri Festive Wear"},
    {"prompt_text": "A male model showcasing a maroon velvet sherwani with golden embroidery, royal palace backdrop, luxurious fashion campaign, photorealistic", "category": "E-commerce Fashion", "use_case": "Wedding Sherwani"},
    {"prompt_text": "An Indian woman wearing a contemporary Indo-western fusion gown, deep blue with silver sequins, walking down a grand staircase, high fashion", "category": "E-commerce Fashion", "use_case": "Indo-Western Fusion"},
    {"prompt_text": "A handsome young man in a casual short kurta and jeans, drinking chai at a local street cafe, lifestyle e-commerce photography, soft morning light", "category": "E-commerce Fashion", "use_case": "Casual Ethnic Wear"},
    {"prompt_text": "An Indian woman in a bright orange bandhani saree, standing in a desert landscape in Rajasthan, wind blowing the pallu, vibrant colors, fashion editorial", "category": "E-commerce Fashion", "use_case": "Regional Saree Collection"},
    {"prompt_text": "A young boy and girl in traditional festive wear, holding sparklers, smiling at the camera, warm festive lighting, perfect for children's e-commerce", "category": "E-commerce Fashion", "use_case": "Kids Festive Wear"},
    {"prompt_text": "A male model wearing a crisp white linen kurta pajama, relaxing in a modern minimalist living room, clean bright aesthetic, lifestyle product shot", "category": "E-commerce Fashion", "use_case": "Summer Ethnic Wear"},
    {"prompt_text": "An Indian woman wearing a heavy bridal red dupatta over her head, intricate mehndi on her hands, extreme close-up on the fabric details, macro photography", "category": "E-commerce Fashion", "use_case": "Fabric Detail Shot"},
    {"prompt_text": "A man in a vibrant yellow silk kurta, celebrating Haldi ceremony, yellow marigold flowers falling, candid smiling portrait, high quality", "category": "E-commerce Fashion", "use_case": "Wedding Ceremony Wear"},
    {"prompt_text": "A woman wearing a modern pre-draped saree in emerald green, cocktail party setting with bokeh lights, sophisticated luxury fashion", "category": "E-commerce Fashion", "use_case": "Party Wear Saree"},
    {"prompt_text": "A young man wearing a floral printed jacket over a plain kurta, standing against a vibrant graffiti wall, urban ethnic street style, dynamic lighting", "category": "E-commerce Fashion", "use_case": "Urban Ethnic Fashion"},
    {"prompt_text": "An Indian woman in a simple elegant cotton saree, working at a modern office desk with a laptop, professional lifestyle e-commerce shot", "category": "E-commerce Fashion", "use_case": "Office Wear Saree"}
]

def seed_prompts(db: Session):
    for data in PROMPTS_DATA:
        existing = db.query(Prompt).filter_by(prompt_text=data["prompt_text"]).first()
        if not existing:
            new_prompt = Prompt(
                prompt_text=data["prompt_text"],
                category=data["category"],
                use_case=data["use_case"]
            )
            db.add(new_prompt)
    db.commit()
    print(f"Seeded {len(PROMPTS_DATA)} prompts successfully (idempotent).")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        seed_prompts(db)
    finally:
        db.close()
