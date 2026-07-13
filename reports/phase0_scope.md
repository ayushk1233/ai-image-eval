# Phase 0: Scope Lock & Decision Freeze

## 1. Category & Use Case
**Category**: E-commerce Fashion Product Photography
**Use Case**: Regional-language festival marketing creative (e.g., Diwali, Holi) featuring traditional Indian wear (sarees, kurtas) in lifestyle settings.

**Why it matters for India**: E-commerce is booming in India, especially in regional and Tier-2/Tier-3 markets. Providing culturally relevant AI models to generate high-quality product images for local festivals can dramatically reduce costs for SMBs and independent sellers, democratizing professional-grade e-commerce media. An AI lab would care about this because understanding nuanced cultural attire and festive settings is a key differentiator in the Indian market, requiring specific visual fidelity that generic western-trained models often fail at.

## 2. Rating Protocol
- **Methodology**: True Arena-style blind comparison
- **Sample Size**: 8-prompt sample per participant
- **Ordering**: Randomized-order per participant (model identity hidden)
- **Criteria (Likert 1-5)**:
  1. Prompt Adherence
  2. Visual Quality
  3. Indian Relevance
  4. Overall

## 3. Prompts Method
We will generate 20-30 prompts with templates focusing on traditional Indian wear across different demographics, regional settings, and festival themes. (e.g., "A young Indian woman wearing a red Banarasi silk saree, standing in a brightly lit Diwali setting with diyas, high-fashion product photography, 4k, photorealistic").

## 4. API Access Checks
- [x] OpenAI `gpt-image-1` (Pending final user validation of API Key)
- [x] Google Gen AI `gemini-2.5-flash-image` (Pending final user validation of API Key)
- [x] Google Gen AI `gemini-3.1-flash-image-preview` (Pending final user validation of API Key)
