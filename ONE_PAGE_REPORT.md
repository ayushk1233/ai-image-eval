# One-Page Report: E-commerce Product Photography Evaluation for the Indian Market

## 1. The Evaluation
We evaluated three leading text-to-image models (**GPT-5 Image Mini**, **Gemini 2.5 Flash Image**, and **Gemini 3.1 Flash Image Preview**) specifically for **E-commerce Product Photography** targeting the **Indian demographic**. The goal was to determine which model produces images that balance cultural authenticity (accurate ethnic wear, styling, and fabrics) with commercial viability (usable catalog-style framing).

## 2. The Core Setup
- **Infrastructure:** We built a fully Dockerized end-to-end platform using FastAPI and SQLite for the backend, and Streamlit for the frontend.
- **Pipeline:** We curated a benchmark of highly specific Indian ethnic wear prompts (e.g., "Navratri chaniya choli", "Kanjeevaram saree"). Images were generated programmatically via the vendor APIs.
- **Methodology:** We utilized a blind, randomized human evaluation protocol. Participants rated the images on a 1-5 Likert scale across key metrics: Prompt Adherence, Visual Quality, Indian Relevance, Commercial Viability, Product Focus, and Fabric Realism.

## 3. The Main Findings
Our data collection revealed two distinct, conflicting model personalities:
- **GPT-5 Image Mini excels at "Product Focus" & Framing.** It acts like a commercial catalog photographer, placing the apparel center stage. However, it severely lacks photorealism and struggles with intricate Indian fabric textures, often falling into the "uncanny AI valley."
- **Gemini (2.5 & 3.1) excels at "Visual Quality" & "Fabric Realism."** It captures stunning cultural nuances, lighting, and skin textures. However, it acts more like a cinematic artist than a product photographer. It aggressively over-generates complex, distracting backgrounds, causing the actual commercial product to be lost in the scene.

## 4. The Most Important Takeaway
There is no single "best" model out of the box for Indian e-commerce. AI labs must recognize that **commercial utility requires a fundamentally different aesthetic than artistic generation**. 

For immediate commercial use, **GPT-5 Image Mini** provides the necessary catalog framing but requires touch-ups for realism. **Gemini** generates beautiful cultural art, but requires aggressive negative prompting to force plain studio backgrounds in order to be commercially viable for product catalogs.
