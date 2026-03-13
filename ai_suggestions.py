from typing import Dict, List, Any
from dataclasses import dataclass

@dataclass
class Impact:
    water_saved: float = 0
    waste_saved: float = 0
    co2_saved: float = 0

@dataclass
class SustainabilitySuggestion:
    id: str
    category: str
    title: str
    description: str
    friendly_nudge: str
    impact: Impact
    is_recommended: bool
    priority: str

@dataclass
class GuestSuggestionResult:
    guest_name: str
    suggestions: List[SustainabilitySuggestion]
    total_impact: Impact
    personalized_message: str

def generate_suggestions(profile: Dict[str, Any]) -> GuestSuggestionResult:
    suggestions: List[SustainabilitySuggestion] = []

    # Towel Reuse Logic (ported from v0 lib/ai-suggestions.ts)
    if profile.get('towel_reuse_willing', False) and not profile.get('requires_frequent_linen_change', False) and not profile.get('has_medical_condition', False):
        suggestions.append(
            SustainabilitySuggestion(
                id="towel-reuse",
                category="towels",
                title="Towel Reuse Program",
                description="Reuse your towels during your stay to save water and reduce washing.",
                friendly_nudge=f"Hi {profile['name']}! Help us save the planet one towel at a time. Hang your towel to reuse it, or leave it on the floor for a fresh one.",
                impact=Impact(water_saved=40 * profile.get('stay_duration', 3), co2_saved=200 * profile.get('stay_duration', 3)),
                is_recommended=True,
                priority="high" if profile.get('eco_conscious', False) else "medium"
            )
        )
    # Add more logic from v0... (towels, linens, amenities, energy, water, etc.)
    # For brevity, implementing core towel + energy for now

    # Energy saving (always)
    suggestions.append(
        SustainabilitySuggestion(
            id="energy-saving",
            category="energy",
            title="Smart Energy Management",
            description="Motion-sensor lights and smart thermostat help reduce energy usage.",
            friendly_nudge=f"{profile['name']}, your room features smart energy systems. Lights turn off when you leave.",
            impact=Impact(co2_saved=500 * profile.get('stay_duration', 3)),
            is_recommended=True,
            priority="medium"
        )
    )

    # Calculate total impact
    total_impact = Impact(
        water_saved=sum(s.impact.water_saved for s in suggestions),
        waste_saved=sum(s.impact.waste_saved for s in suggestions),
        co2_saved=sum(s.impact.co2_saved for s in suggestions)
    )

    # Personalized message
    personalized_message = f"Welcome {profile['name']}! We've personalized eco-suggestions for your stay."
    if profile.get('eco_conscious', False):
        personalized_message += f" Your choices could save {total_impact.water_saved:.0f}L water!"

    # Top nudge (first suggestion for quick preview)
    top_nudge = suggestions[0] if suggestions else None

    return GuestSuggestionResult(
        guest_name=profile['name'],
        suggestions=suggestions,
        total_impact=total_impact,
        personalized_message=personalized_message
    ), top_nudge.friendly_nudge if top_nudge else "General conservation tip", top_nudge.impact.co2_saved if top_nudge else 1.0

