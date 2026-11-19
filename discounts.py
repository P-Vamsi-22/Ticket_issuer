def calculate_discount(amount): 
    if isinstance(amount, bool) or not isinstance(amount, (int, float)): 
        raise ValueError("Amount must be a number") 
    if amount < 0: 
        raise ValueError("Amount can't be negative") 
    if amount > 1000: 
        return round(amount * 0.9, 2) 
    return amount   
