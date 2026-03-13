from flask import Flask, render_template, request, redirect, url_for, flash
import json
import uuid

app = Flask(__name__)
app.secret_key = 'smartnudge_secret'

# Synthetic guest data for dashboard
synthetic_guests = [
    {
        'id': str(uuid.uuid4())[:8],
        'name': 'John Doe',
        'age_group': 'adult',
        'health_conditions': 'none',
        'children': 'no',
        'caregiver': 'no',
        'sust_pref': 'medium',
        'nudge': 'Turn off lights when leaving room to save energy.',
        'impact': 2.5,  # kg CO2 saved
        'opted_out': False
    },
    {
        'id': str(uuid.uuid4())[:8],
        'name': 'Jane Smith',
        'age_group': 'senior',
        'health_conditions': 'mobility',
        'children': 'no',
        'caregiver': 'yes',
        'sust_pref': 'high',
        'nudge': 'Reuse towels to reduce water usage.',
        'impact': 1.8,
        'opted_out': False
    },
    # Add 8 more similar entries...
    {
        'id': str(uuid.uuid4())[:8],
        'name': 'Family Trip',
        'age_group': 'adult',
        'health_conditions': 'none',
        'children': 'yes',
        'caregiver': 'no',
        'sust_pref': 'low',
        'nudge': 'Segregate waste for recycling with kids.',
        'impact': 3.0,
        'opted_out': True
    },
    {
        'id': str(uuid.uuid4())[:8],
        'name': 'Mike Johnson',
        'age_group': 'young',
        'health_conditions': 'allergy',
        'children': 'no',
        'caregiver': 'no',
        'sust_pref': 'high',
        'nudge': 'Opt for digital key to save paper.',
        'impact': 0.5,
        'opted_out': False
    },
    # Continuing to 10...
] * 2  # Duplicate to make 10

# Rule-based AI decision engine
def generate_nudge(profile):
    age = profile['age_group']
    health = profile['health_conditions']
    children = profile['children'] == 'yes'
    caregiver = profile['caregiver'] == 'yes'
    pref = profile['sust_pref']

    nudges = {
        'young': 'Use bike share instead of taxi for short trips.',
        'adult': 'Turn off AC when out; set to 24C.',
        'senior': 'Reuse bath towels - hang to dry.'
    }.get(age, 'Conserve water with shorter showers.')

    if children:
        nudges += ' Teach kids to turn off taps.'
    if caregiver:
        nudges += ' Help others save energy too.'
    if health == 'mobility':
        nudges += ' Request room near elevators.'
    elif health == 'allergy':
        nudges += ' Choose unscented amenities.'
    
    if pref == 'high':
        impact = 3.0
    elif pref == 'medium':
        impact = 2.0
    else:
        impact = 1.0

    return nudges, impact

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
    nudge_text, impact = generate_nudge(profile)
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

@app.route('/optout/<guest_id>')
def optout(guest_id):
    for guest in synthetic_guests:
        if guest['id'] == guest_id:
            guest['opted_out'] = True
            guest['nudge'] = 'Thank you for opting out. We respect your choice.'
            guest['impact'] = 0
            flash('Opt-out successful.')
            break
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    # Stats
    total_guests = len(synthetic_guests)
    nudged = len([g for g in synthetic_guests if not g['opted_out']])
    total_impact = sum(g['impact'] for g in synthetic_guests)
    guest_types = {}
    for g in synthetic_guests:
        key = f"{g['age_group']}-{ 'kids' if g['children']=='yes' else 'no'}-{g['sust_pref']}"
        guest_types[key] = guest_types.get(key, 0) + 1
    
    return render_template('dashboard.html', guests=synthetic_guests, stats={
        'total_guests': total_guests,
        'nudged': nudged,
        'total_impact': round(total_impact, 1),
        'guest_types': guest_types
    })

if __name__ == '__main__':
    app.run(debug=True)
