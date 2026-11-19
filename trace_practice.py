USERS = {1: "Ravi", 2: "Priya"} 
 
def get_owner_name(ticket): 
    return USERS[ticket["owner_id"]] 
 
def print_ticket(ticket): 
    print(ticket["title"], "-", get_owner_name(ticket)) 
 
tickets = [ 
    {"title": "Laptop not charging", "owner_id": 1}, 
    {"title": "Cannot log in to VPN", "owner_id": 2},
] 
for t in tickets: 
    print_ticket(t) 