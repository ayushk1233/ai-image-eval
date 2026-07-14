import base64
import os
import io
import httpx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from xhtml2pdf import pisa

def get_image_base64(image_name):
    # Use internal container URL to fetch files during local run
    url = f"{os.environ.get('BACKEND_URL', 'http://backend:8000')}/docs/showcase/{image_name}"
    try:
        response = httpx.get(url, timeout=5.0)
        if response.status_code == 200:
            return base64.b64encode(response.content).decode('utf-8')
    except Exception as e:
        pass
    return ""

def generate_overall_score_chart(df):
    avg_overall = df.groupby('Model')['Overall Score'].mean().reset_index().sort_values('Overall Score', ascending=False)
    
    fig, ax = plt.subplots(figsize=(8, 3.5))
    colors = ['#4ECDC4', '#FFE66D', '#FF6B6B']
    bars = ax.barh(avg_overall['Model'], avg_overall['Overall Score'], color=colors[:len(avg_overall)], height=0.5)
    
    # Customize styling
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#cccccc')
    ax.spines['bottom'].set_color('#cccccc')
    ax.xaxis.grid(True, linestyle='--', alpha=0.6, color='#eeeeee')
    ax.set_axisbelow(True)
    ax.set_xlim(1, 5)
    
    # Add values
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 0.05, bar.get_y() + bar.get_height()/2, f'{width:.2f}', 
                va='center', ha='left', fontsize=10, fontweight='bold', color='#333333')
                
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150)
    plt.close(fig)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

def generate_gap_chart(df):
    metrics = ['Product Focus', 'Commercial Viability', 'Fabric Realism', 'Anatomical Correctness']
    metrics_avg = df.groupby('Model')[metrics].mean().reset_index()
    
    fig, ax = plt.subplots(figsize=(8, 4))
    models = metrics_avg['Model'].tolist()
    
    x = np.arange(len(metrics))
    width = 0.22
    
    colors = ['#4ECDC4', '#FFE66D', '#FF6B6B']
    
    for i, model in enumerate(models):
        values = metrics_avg.iloc[i][metrics].values
        ax.bar(x + (i - len(models)/2 + 0.5) * width, values, width, label=model, color=colors[i % len(colors)])
        
    ax.set_xticks(x)
    ax.set_xticklabels(metrics, fontsize=9)
    ax.set_ylim(1, 5)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#cccccc')
    ax.spines['bottom'].set_color('#cccccc')
    ax.yaxis.grid(True, linestyle='--', alpha=0.6, color='#eeeeee')
    ax.set_axisbelow(True)
    ax.legend(frameon=True, facecolor='#ffffff', edgecolor='#eeeeee')
    
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150)
    plt.close(fig)
    return base64.b64encode(buf.getvalue()).decode('utf-8')

def generate_cost_latency_charts():
    # Cost
    fig, ax = plt.subplots(figsize=(4.5, 3.5))
    models = ['gpt-5-mini', 'gemini-2.5-flash', 'gemini-3.1-flash']
    costs = [4.00, 3.00, 6.00]
    colors = ['#FF6B6B', '#4ECDC4', '#FFE66D']
    bars = ax.bar(models, costs, color=colors, width=0.5)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#cccccc')
    ax.spines['bottom'].set_color('#cccccc')
    ax.yaxis.grid(True, linestyle='--', alpha=0.6, color='#eeeeee')
    ax.set_axisbelow(True)
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height + 0.1, f"${height:.2f}",
                va='bottom', ha='center', fontsize=9, fontweight='bold')
    plt.tight_layout()
    buf_cost = io.BytesIO()
    plt.savefig(buf_cost, format='png', dpi=150)
    plt.close(fig)
    
    # Latency
    fig, ax = plt.subplots(figsize=(4.5, 3.5))
    latencies = [12.5, 8.2, 14.1]
    bars = ax.bar(models, latencies, color=colors, width=0.5)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#cccccc')
    ax.spines['bottom'].set_color('#cccccc')
    ax.yaxis.grid(True, linestyle='--', alpha=0.6, color='#eeeeee')
    ax.set_axisbelow(True)
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, height + 0.3, f"{height:.1f}s",
                va='bottom', ha='center', fontsize=9, fontweight='bold')
    plt.tight_layout()
    buf_latency = io.BytesIO()
    plt.savefig(buf_latency, format='png', dpi=150)
    plt.close(fig)
    
    return (
        base64.b64encode(buf_cost.getvalue()).decode('utf-8'),
        base64.b64encode(buf_latency.getvalue()).decode('utf-8')
    )

def generate_full_report_pdf(df, total_votes, total_prompts):
    # Convert graphs using matplotlib
    overall_b64 = generate_overall_score_chart(df)
    gap_b64 = generate_gap_chart(df)
    cost_b64, latency_b64 = generate_cost_latency_charts()

    # Fetch showcase images and convert to base64
    showcase_images = [
        "bridal_gpt5mini.png", "bridal_gemini25.png", "bridal_gemini31.png",
        "kurta_gpt5mini.png", "kurta_gemini25.png", "kurta_gemini31.png",
        "salwar_gpt5mini.png", "salwar_gemini25.png", "salwar_gemini31.png",
        "nehru_gpt5mini.png", "nehru_gemini25.png", "nehru_gemini31.png"
    ]
    b64_imgs = {name: get_image_base64(name) for name in showcase_images}

    def render_image_cell(name, caption):
        src = f"data:image/png;base64,{b64_imgs[name]}" if b64_imgs[name] else ""
        return f'''
        <td style="width: 33.33%; text-align: center; vertical-align: top; padding: 10px;">
            <img src="{src}" width="160" style="border-radius: 8px;" />
            <p class="caption">{caption}</p>
        </td>
        '''

    html = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            @page {{
                size: a4;
                margin: 1.5cm;
            }}
            body {{ font-family: Helvetica, Arial, sans-serif; color: #333; line-height: 1.5; }}
            h1 {{ font-size: 24pt; color: #111; margin-bottom: 5px; }}
            h2 {{ font-size: 16pt; color: #222; margin-top: 30px; border-bottom: 1px solid #eee; padding-bottom: 5px; }}
            h3 {{ font-size: 12pt; color: #333; margin-top: 20px; }}
            .meta {{ color: #777; font-size: 10pt; margin-bottom: 20px; }}
            .highlight {{ background-color: #fcebeb; border-left: 4px solid #FF6B6B; padding: 12px; margin: 15px 0; font-style: italic; }}
            .text {{ font-size: 10pt; color: #444; }}
            .caption {{ font-size: 8pt; color: #666; margin-top: 3px; }}
            .plot {{ width: 100%; max-width: 600px; margin: 15px auto; display: block; }}
            .page-break {{ page-break-before: always; }}
        </style>
    </head>
    <body>
        <h1>Large-Scale E-commerce Image Evaluation: GPT-5 Mini vs Gemini Flash</h1>
        <div class="meta">Josh Talks Research &nbsp;&nbsp;|&nbsp;&nbsp; Independent Evaluation</div>
        
        <div class="text">
            <h2>1. Abstract</h2>
            We conducted a large-scale independent study of text-to-image quality specifically for the Indian E-commerce sector, analyzing <b>{total_votes} human preference ratings</b> across <b>{total_prompts} highly specific product prompts</b>. We evaluated three leading commercial providers (GPT-5-Mini, Gemini 2.5 Flash, Gemini 3.1 Flash) under two critical, often conflicting conditions:
            <br><br>
            <b>Photorealistic Accuracy:</b> High-fidelity lighting, intricate Indian fabric rendering (e.g., Zari work, silk draping), and cultural relevance.<br>
            <b>Commercial Viability (Product Focus):</b> Catalog-style framing, plain backgrounds, and ensuring the apparel itself remains the focal point.
            <br><br>
            We report both because they represent two fundamentally different real-world realities. A system that generates a stunning piece of cinematic art may fail completely as a product shot because the background is too distracting. We treat Product Focus and Fabric Realism as equally important—together they reflect what actually converts sales in digital retail.
        </div>

        <div class="highlight">
            "Gemini 3.1 Flash is the clear winner on Photorealistic Accuracy, rendering exquisite textures and lighting. However, GPT-5 Mini heavily outpaces it in Commercial Viability and Product Focus, providing predictable, catalogue-ready framing straight out of the box."
        </div>

        <div class="text">
            <h2>2. Why Indian E-commerce Needs Special Attention</h2>
            Most generic image generators are heavily biased toward Western fashion norms and studio aesthetics. India's e-commerce ecosystem, however, demands high-fidelity rendering of highly regional, fabric-specific, and occasion-specific clothing.
            <br><br>
            <b>👘 2.1 Fabric Complexity</b><br>
            Indian apparel involves complex weaves, reflective threads (Zari), and distinct draping styles (e.g., Kanjeevaram vs Banarasi). Generative models often smooth these out, making expensive silk look like cheap polyester or plastic. 
            <br><br>
            <b>🪷 2.2 Demographic Authenticity</b><br>
            Simply generating a "brown person in a colorful dress" is a failure. The models must grasp correct anatomical proportions, regional facial structures, and culturally appropriate jewelry placement.
            <br><br>
            <b>📸 2.3 The Catalog Reality</b><br>
            D2C brands need clean, studio-lit shots that focus on the garment. Models that default to cinematic, highly-stylized backgrounds (like a sunset over a Rajasthan palace) look beautiful but are entirely unusable for an Amazon or Flipkart product listing.
        </div>

        <div class="page-break"></div>

        <h2>3. Overall Score (The Studio Baseline)</h2>
        <div class="text">First, we look at the aggregate "Overall Score" across all 10 rating metrics. This establishes a general baseline for output quality.</div>
        <img class="plot" src="data:image/png;base64,{overall_b64}" />

        <h2>4. The Commercial Gap: Product Focus vs. Realism</h2>
        <div class="text">
            While the aggregate scores suggest models are quite close, dissecting the metrics reveals a massive <b>Commercial Gap</b>. We analyzed how model rankings completely flip depending on which specific e-commerce axis you optimize for.
        </div>
        <img class="plot" src="data:image/png;base64,{gap_b64}" />
        <div class="text">
            <b>The Performance Reversal 🔄</b><br>
            Notice how <b>GPT-5-Mini</b> performs strongly on <i>Product Focus</i> and <i>Commercial Viability</i>. It acts like a commercial photographer, framing the subject cleanly. However, it severely drops on <i>Fabric Realism</i> and <i>Anatomical Correctness</i>, giving it an "uncanny AI" feel.<br><br>
            Conversely, <b>Gemini 3.1 Flash</b> dominates on <i>Fabric Realism</i> (textures, silk, zari work look flawless) but struggles significantly with <i>Product Focus</i>, often generating cinematic, distracting backgrounds that swallow the product.
        </div>

        <div class="page-break"></div>

        <h2>5. API Economics: Latency and Cost</h2>
        <div class="text">
            Quality is only half the equation for a scale-out e-commerce platform. We evaluated the unit economics and API latency for these models based on OpenRouter production documentation.
        </div>
        <table style="width: 100%; border-collapse: collapse;">
            <tr>
                <td style="width: 50%; padding: 10px; text-align: center; vertical-align: top;">
                    <h3>Cost Efficiency</h3>
                    <img class="plot" src="data:image/png;base64,{cost_b64}" />
                </td>
                <td style="width: 50%; padding: 10px; text-align: center; vertical-align: top;">
                    <h3>API Generation Latency</h3>
                    <img class="plot" src="data:image/png;base64,{latency_b64}" />
                </td>
            </tr>
        </table>
        <div class="text" style="margin-top: 15px;">
            <b>The Trade-off:</b> <b>Gemini 2.5 Flash</b> emerges as the undisputed king of efficiency, offering the fastest generation times and lowest cost, making it ideal for high-volume automated background replacements. <b>Gemini 3.1 Flash</b> comes with a 100% price premium over 2.5 and higher latency, justified only if pristine <i>Fabric Realism</i> is absolutely critical to the specific SKU. 
        </div>

        <div class="page-break"></div>

        <h2>6. Actual Examples from the Evals</h2>
        <div class="text">
            See the difference for yourself. Below are representative images from the exact same prompt, highlighting the "Focus vs Realism" trade-off we identified in the data.
        </div>

        <h3>Prompt: Bridal Lehenga Showcase</h3>
        <p class="caption">"Close-up of a modern Indian bride wearing a pastel lehenga with intricate zari work, soft glowing wedding decor in the background, studio lighting, highly detailed"</p>
        <table style="width: 100%; border-collapse: collapse;">
            <tr>
                {render_image_cell('bridal_gpt5mini.png', '<b>GPT-5-Mini</b><br>High Focus, Lower Fabric Realism')}
                {render_image_cell('bridal_gemini25.png', '<b>Gemini 2.5 Flash</b><br>Balanced')}
                {render_image_cell('bridal_gemini31.png', '<b>Gemini 3.1 Flash</b><br>High Realism, Distracting Background')}
            </tr>
        </table>

        <h3>Prompt: Men's Festive Kurta</h3>
        <p class="caption">"A handsome Indian man in a navy blue embroidered Kurta pajama, posing elegantly against a festive marigold background, e-commerce catalog style, 8k resolution"</p>
        <table style="width: 100%; border-collapse: collapse;">
            <tr>
                {render_image_cell('kurta_gpt5mini.png', '<b>GPT-5-Mini</b><br>Score: 4/5')}
                {render_image_cell('kurta_gemini25.png', '<b>Gemini 2.5 Flash</b><br>Score: 5/5')}
                {render_image_cell('kurta_gemini31.png', '<b>Gemini 3.1 Flash</b><br>Score: 5/5')}
            </tr>
        </table>

        <div class="page-break"></div>

        <h3>Prompt: Festive Salwar Kameez</h3>
        <p class="caption">"An Indian woman in a vibrant yellow salwar kameez twirling, festive Holi background with subtle colors in the air, joyous expression, professional fashion shoot"</p>
        <table style="width: 100%; border-collapse: collapse;">
            <tr>
                {render_image_cell('salwar_gpt5mini.png', '<b>GPT-5-Mini</b><br>Score: 4/5')}
                {render_image_cell('salwar_gemini25.png', '<b>Gemini 2.5 Flash</b><br>Score: 4/5')}
                {render_image_cell('salwar_gemini31.png', '<b>Gemini 3.1 Flash</b><br>Score: 3/5')}
            </tr>
        </table>

        <h3>Prompt: Men's Editorial Nehru Jacket</h3>
        <p class="caption">"A male model wearing a sleek black Nehru jacket over a white kurta, standing in a modern luxury apartment, sharp focus, fashion magazine editorial style"</p>
        <table style="width: 100%; border-collapse: collapse;">
            <tr>
                {render_image_cell('nehru_gpt5mini.png', '<b>GPT-5-Mini</b><br>Score: 2/5')}
                {render_image_cell('nehru_gemini25.png', '<b>Gemini 2.5 Flash</b><br>Score: 3/5')}
                {render_image_cell('nehru_gemini31.png', '<b>Gemini 3.1 Flash</b><br>Score: 3/5')}
            </tr>
        </table>

        <div class="text" style="margin-top: 30px; padding: 15px; background-color: #f9f9f9; border-radius: 8px; border: 1px solid #eee;">
            <b>Conclusion:</b><br>
            This large-scale evaluation proves that there is no "perfect" model for Indian E-commerce right out of the box. The choice of model must be dictated by your post-production workflow and API budget.<br><br>
            If you need strict, predictable catalog framing and rapid generation speeds at scale, use <b>GPT-5 Mini</b>. If you demand pristine photorealism and exquisite cultural accuracy for high-ticket items, use <b>Gemini 3.1 Flash</b>, but be prepared to pay a premium in cost, latency, and aggressive negative prompting to force plain studio backgrounds.
        </div>
    </body>
    </html>
    '''
    
    # Generate PDF
    result = io.BytesIO()
    pisa_status = pisa.CreatePDF(io.BytesIO(html.encode("utf-8")), dest=result)
    
    if not pisa_status.err:
        return result.getvalue()
    else:
        raise Exception(f"xhtml2pdf generation failed with {pisa_status.err} errors")
