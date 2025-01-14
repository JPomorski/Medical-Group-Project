import injuries_keywords_dictionary as ikd

def calculate_priority(description, age=None, time_since_event=None):

    count_critical = 0  
    count_moderate = 0  

    for phrase, level in ikd.critical_phrases.items():
        if word in description.lower():
            if level == 1:
                count_critical += 1
            elif level == 0:
                count_moderate += 1


    if count_critical >= 2:  
        return 2, count_critical, count_moderate
    if count_critical == 1 and count_moderate >= 3:  
        return 2, count_critical, count_moderate
    if "bezdech" in description.lower() or "brak pulsu" in description.lower():
        return 2, count_critical, count_moderate
    if "os³abienie jednej strony cia³a" in description.lower() or \
       "problem z mówieniem" in description.lower() or \
       "opadanie k¹cika ust" in description.lower():  
        return 2, count_critical, count_moderate
    if age and (age < 12 or age > 65) and count_critical >= 1:  
        return 2, count_critical, count_moderate
    if count_moderate > 4:  
        return 1, count_critical, count_moderate


    if time_since_event and time_since_event > 120:  
        return min(0, max(1, count_critical)), count_critical, count_moderate


    total_weight = count_critical + (0.5 * count_moderate) 
    if total_weight >= 2:
        priority = 2
    elif total_weight >= 1:
        priority = 1
    else:
        priority = 0

    return priority, count_critical, count_moderate
