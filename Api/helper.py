def assign_role(user_id):
    if user_id//10000000 == 62 and user_id >= 620000000 and user_id < 630000000:
        return 3
    elif user_id//10000 == 100 and user_id >= 1000000 and user_id <= 1009999:
        return 2 
    elif user_id//100000 == 999 and user_id >= 99900000 and user_id <= 99999999:
        return 1
    else:
        raise ValueError