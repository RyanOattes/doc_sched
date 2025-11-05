from database import get_users, get_periods, get_doc_mappings
import itertools

#SELECTED_YEAR = 2025
#SELECTED_MONTH = 11

def generate_schedule(selected_year, selected_month):
    users = get_users()
    user_role_lookup = {}
    user_docs_lookup = {}
    user_expected_slots = {}
    ############################
    # Create some Lookups
    ############################

    total_ft_fraction = 0.0
    for u in users:
        user_role_lookup[u["id"]] = u["type"]
        user_docs_lookup[u["id"]] = []
        #user_expected_slots[u["id"]] = 0.0
        if u["type"] != "doc":
            total_ft_fraction = total_ft_fraction + float(u["ft_fraction"])

    for u in users:
        if u["type"] != "doc":
            user_expected_slots[u["id"]] = float(u["ft_fraction"]) / total_ft_fraction

    for m in get_doc_mappings():
        user_docs_lookup[m["case_mgr_id"]].append(m["doc_id"])

    print("User Doc Lookups:")
    for u in user_docs_lookup:
        print(u, user_docs_lookup[u])
    print("")

    ############################
    # Expand Days to Half Days
    ############################

    doc_slots = []
    for u in users:
        if user_role_lookup[u["id"]] == "doc":
            for p in get_periods(u["id"], selected_year, selected_month):
                if p["slot"] == "All Day":
                    temp_period_am = p.copy()
                    temp_period_am["slot"] = "Morning"
                    doc_slots.append(temp_period_am)
                    temp_period_pm = p.copy()
                    temp_period_pm["slot"] = "Afternoon"
                    doc_slots.append(temp_period_pm)
                else:
                    doc_slots.append(p)

    print("Doc Slots:")
    for s in doc_slots:
        print(s)
                
    print("")

    print("Expected Doc Slots per User")
    for u in user_expected_slots:
        user_expected_slots[u] = user_expected_slots[u] * len(doc_slots)
        print(u, user_expected_slots[u])
    print("")

    ############################
    # Score Options
    ############################

    #options = [c for c in itertools.combinations_with_replacement(users, len(doc_slots))]
    options = itertools.product(users, repeat=len(doc_slots))
    option_scores = []

    viable_options = []
    for opt in options:
        score = {"deal_breaker": False, "alloc_score": 0, "even_score": 0}

        # Check to make sure the person filling the slot isn't a doc
        for slot_filler in opt:
            if slot_filler["type"] == "doc":
                score["deal_breaker"] = True    

        # Check to make sure the slot_filler should be working with that doc
        for i, slot_filler in enumerate(opt):
            if doc_slots[i]["user_name"] not in user_docs_lookup[slot_filler["id"]]:
                score["deal_breaker"] = True

        if score["deal_breaker"]:
            continue

        # Calculate deviation from fair share of doc days
        user_actual_slots = {}
        for slot_filler in opt:
            if slot_filler["id"] not in user_actual_slots:
                user_actual_slots[slot_filler["id"]] = 0.0
            user_actual_slots[slot_filler["id"]] += 1

        total_error = 0
        for u in user_expected_slots:
            actual_slots = 0
            if u in user_actual_slots:
                actual_slots = user_actual_slots[u]
            user_error = abs(actual_slots - user_expected_slots[u])
            user_error = user_error * user_error
            total_error += user_error
        score["alloc_score"] = total_error

        # Check for even distribution of slots
        even_score = 0
        for i, slot_filler in enumerate(opt[1:]):
            if opt[i]["id"] == opt[i-1]["id"]:
                even_score += 1
        score["even_score"] = even_score

        score["alloc_score"] += score["even_score"]

        #print("")
        viable_options.append(opt)
        option_scores.append(score)

    #viable_options = []
    #for i, os in enumerate(option_scores):
    #    if os["deal_breaker"] == False:
    #        viable_options.append(options[i])

    print(len(viable_options))

    min_score = -1
    min_index = -1
    for i, o in enumerate(viable_options):
        #print(option_scores[i]["score"])
        if option_scores[i]["deal_breaker"] is False:
            if min_score == -1 or min_score > option_scores[i]["alloc_score"]:
                min_score = option_scores[i]["alloc_score"]
                min_index = i

    print("")
    print(min_score)
    #print(viable_options[i])
    print(option_scores[min_index])
    for s in viable_options[min_index]:
        print(s)

    #print("")
    #for os in option_scores:
        #if os["deal_breaker"] is False:
        #if os["alloc_score"] < 5:
    #    if os["even_score"] < 2:
    #        print(os["deal_breaker"], os["alloc_score"], os["even_score"])
    return viable_options[min_index], doc_slots