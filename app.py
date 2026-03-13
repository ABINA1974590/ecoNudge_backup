from flask import Flask, render_template, request, redirect, url_for, flash
import json
import uuid
import requests
from ai_suggestions import generate_suggestions, GuestSuggestionResult

app = Flask(__name__)
app.secret_key = 'econudge_secret'

# Synthetic guest data 
synthetic_guests = []

# TCS GenAI Lab API Key
TCS_GENAI_API_KEY = 'sk-hMZ7kyoK4WN8E7jL-X8XgA'
TCS_GENAI_ENDPOINT = 'https://genailab.tcs.in/model_predict'

# AI Models Used:
# 1. v0-sustainable-hospitality-platform (ai_suggestions.py) ✓ ACTIVE
# 2. TCS GenAI Lab API ('sustainability' model) ✓ ACTIVE NOW

def enhanced_nudge(profile):
    # Map form to v0 profile
    v0_profile = {
        'name': profile['name'],
        'stay_duration': 3,
        'eco_conscious': profile['sust_pref'] == 'high',
        'towel_reuse_willing': True,
        'has_medical_condition': profile['health_conditions'] != 'none',
        'requires_frequent_linen_change': profile['health_conditions'] == 'mobility',
        'has_children': profile['children'] == 'yes',
    }
    
    # v0-AI Model Call
    result, nudge_text, impact = generate_suggestions(v0_profile)
    
    # TCS GenAI Lab API - ENHANCED NUDGE
    try:
        response = requests.post(TCS_GENAI_ENDPOINT, 
            json={'model': 'sustainability', 'input': profile}, 
            headers={'Authorization': f'Bearer {TCS_GENAI_API_KEY}'},
            timeout=5
        )
        if response.ok:
            tcs_enhance = response.json().get('nudge', 'Enhanced by TCS GenAI')
            nudge_text += f"\n\n✨ TCS GenAI: {tcs_enhance}"
    except:
        # Fallback - don't break app
        nudge_text += "\n\n✨ TCS GenAI ready (network/API issue)"
    
    return nudge_text, impact

@app.route('/')
def guest_form():
    return render_template('guest_form.html')

@app.route('/nudge', methods=['POST'])
def nudge():
    profile = {
        'name': request.form['name'],
        'age_group': request.form['age_group'],
        'health_conditions': request.form['health_conditions'],
        'children': request.form['children'],
        'caregiver': request.form['caregiver'],
        'sust_pref': request.form['sust_pref']
    }
    nudge_text, impact = enhanced_nudge(profile)
    guest_id = str(uuid.uuid4())[:8]
    synthetic_guests.append({
        'id': guest_id,
        'name': profile['name'],
        **profile,
        'nudge': nudge_text,
        'impact': impact,
        'opted_out': False
    })
    return render_template('guest_nudge.html', profile=profile, nudge=nudge_text, impact=impact, guest_id=guest_id)

@app.route('/rooms')
def rooms():
    return render_template('rooms.html')

@app.route('/explore')
def explore():
    return render_template('explore.html')

@app.route('/optout/<guest_id>')
def optout(guest_id):
    for guest in synthetic_guests:
        if guest['id'] == guest_id:
            guest['opted_out'] = True
            flash('Opt-out successful.')
            break
    return redirect(url_for('guest_form'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
