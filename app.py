from flask import Flask, render_template, redirect, jsonify
import json
import random

app = Flask(__name__)

def get_data():
    with open('main.json', 'r') as f:
        data = json.load(f)
    return data

def save_data(data):
    with open('main.json', 'w') as f:
        json.dump(data, f, indent=4)

@app.route("/")
def index():
    data = get_data()
    character = data['character']
    return render_template("character.html", character=character, data=data)

@app.route("/travel", methods=['POST'])
def travel():
    data = get_data()
    character = data['character']
    new_location = random.choice(data['locations'])
    character['location'] = new_location    
    new_encounter = random.choice(data['npc_encounters'])
    npc_stats = data['npc_stats'][new_encounter]
    character['encounter'] = {
        'name': new_encounter,
        'HP': npc_stats['HP'],
        'Attack': npc_stats['Attack']
    }
    character['combat_log'].append(f"Encountered a {new_encounter} in {new_location}.")
    save_data(data)
    return redirect('/')

@app.route("/attack", methods=['POST'])
def attack():
    data = get_data()
    character = data['character']
    if 'encounter' in character and character['encounter']:
        npc_name = character['encounter']['name']
        npc_hp = character['encounter']['HP']
        damage = character['stats']['Strength']  # Use strength as the damage.
        npc_hp -= damage
        
        if npc_hp <= 0:
            character['encounter'] = None
            message = f"You defeated the {npc_name}!"
            
            # Give XP for defeating an enemy:
            character['experience'] += 10  # Let's say 10 XP for defeating an enemy.
            character['combat_log'].append(f"Gained 10 XP for defeating {npc_name}.")
            
            # Check for level up:
            if character['experience'] >= 100:  # Let's say 100 XP to level up.
                character['experience'] = 0  # Reset XP.
                character['level'] += 1  # Increase level by 1.
                character['combat_log'].append(f"Leveled up to {character['level']}!")
        else:
            character['encounter']['HP'] = npc_hp
            message = f"You dealt {damage} damage to the {npc_name}. It has {npc_hp} HP left."

        character['combat_log'].append(message)
    else:
        message = "There's no enemy to attack!"
        character['combat_log'].append(message)

    save_data(data)
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
