"""
Structura AI - Architectural Visualizer & Concept Engine
Generates architectural visual rendering prompts and fetches photorealistic
renders via Pollinations AI Flux API.
"""

import urllib.parse


def generate_architectural_render_url(
    structure_type: str,
    built_up_sqft: float,
    architectural_style: str = "Modern Sustainable Biophilic",
    facade_material: str = "Curtain Glass, Exposed Concrete, and Teak Louvers",
    seed: int = 42
) -> str:
    """
    Constructs an architectural rendering prompt and returns the direct
    Pollinations AI Flux image rendering URL.
    """
    prompt = (
        f"hyperrealistic 3D architectural elevation render of a {structure_type}, "
        f"scale {int(built_up_sqft):,} square feet, style {architectural_style}, "
        f"facade with {facade_material}, realistic ambient daylight, golden hour sun reflection, "
        f"lush landscaping, architectural photogrammetry, 8k resolution, octane render, architectural digest feature"
    )

    encoded_prompt = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=768&seed={seed}&model=flux&nologo=true"
    return url
