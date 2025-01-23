from injuries_keywords_dictionary import injury_phrases
body_part_list = {
    "front_right_thigh": 1,
    "back_right_thigh": 1,
    "front_left_thigh": 1,
    "back_left_thigh": 1,
    "front_pelvis": 1,
    "back_pelvis": 1,
    "front_lower_right_hand": 1,
    "back_lower_right_hand": 1,
    "front_lower_left_hand": 1,
    "back_lower_left_hand": 1,
    "front_higher_right_hand": 1,
    "back_higher_right_hand": 1,
    "front_higher_left_hand": 1,
    "back_higher_left_hand": 1,
    "front_head": 1,
    "back_head": 1,
    "front_neck": 1,
    "back_neck": 1,
    "front_chest": 1,
    "back_chest": 1,
    "front_abdomen": 1,
    "back_abdomen": 1,
    "front_lower_right_leg": 1,
    "back_lower_right_leg": 1,
    "front_lower_left_leg": 1,
    "back_lower_left_leg": 1,
}
def extract_injury_priority(descriptions):
    body_parts = descriptions.split(';;')
    max_priority = 0

    for part in body_parts:
        part = part.strip()
        if not part:
            continue

        body_part_desc = part.split(';Description:')
        if len(body_part_desc) < 2:
            continue

        body_part = body_part_desc[0].replace('»', '').strip().lower().replace(' ', '_')
        description = body_part_desc[1].split(';Comment:')[0].strip()

        print(f"Processing body part: {body_part}, description: {description}")

        for body_part_key, injuries in injury_phrases.items():
            if body_part_key in body_part:
                print(f"Matching body part key: {body_part_key}")
                for injury in injuries:
                    if injury["phrase"] in description:
                        print(f"Matching injury phrase: {injury['phrase']}, threat level: {injury['threat_level']}")
                        max_priority = max(max_priority, injury["threat_level"])

    return max_priority

def count_body_parts(descriptions):
    body_parts = descriptions.split(';;')
    return len([part for part in body_parts if part.strip()])
def calculate_priority(age, diseases, allergies, on_medication, blood_type, descriptions, priority_enter):
    priority = 0
    priority_enter = int(priority_enter)
    print(f"priority_enter: {priority_enter}")
    if priority_enter == 3:
        if descriptions.strip():  
            print("priority_enter is 3")
            priority = extract_injury_priority(descriptions)
        else:
            print("priority_enter is 3 but no description provided")
            priority = 0  
    elif priority_enter == 2:
        print("priority_enter is 2")
        body_parts_count = count_body_parts(descriptions)
        print(f"body_parts_count: {body_parts_count}")
        if body_parts_count > 13:
            priority = 2
        elif body_parts_count > 0:
            priority = 1
        else:
            priority = 0
    else:
        print("priority_enter is not 2 or 3")
    age = int(age)

    high_risk_diseases = ["Heart disease", "Diabetes", "Epilepsy", "Cancer"]
    if any(disease in high_risk_diseases for disease in diseases):
        priority = max(priority, 2)

    high_risk_allergies = ["Peanut allergy", "Insect sting allergy"]
    if any(allergy in high_risk_allergies for allergy in allergies):
        priority = max(priority, 1)

    if age >= 70:
        priority = max(priority, 1)
    elif age >= 85:
        priority = max(priority, 2)

    # if on_medication:
    #     priority = min(priority + 1, 2)

    if diseases != 'None' or on_medication:
        priority += 1
    if age >= 65 or blood_type == 'AB-':
        priority += 1
    if 'Heart disease' in diseases or 'Cancer' in diseases:
        priority += 1

    priority = min(priority, 2)

    return priority
