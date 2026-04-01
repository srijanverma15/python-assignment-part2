# ---------------- PART 2: Restaurant Order System ----------------

import copy

# given data

menu = {
    "Paneer Tikka":   {"category": "Starters",  "price": 180.0, "available": True},
    "Chicken Wings":  {"category": "Starters",  "price": 220.0, "available": False},
    "Veg Soup":       {"category": "Starters",  "price": 120.0, "available": True},
    "Butter Chicken": {"category": "Mains",     "price": 320.0, "available": True},
    "Dal Tadka":      {"category": "Mains",     "price": 180.0, "available": True},
    "Veg Biryani":    {"category": "Mains",     "price": 250.0, "available": True},
    "Garlic Naan":    {"category": "Mains",     "price":  40.0, "available": True},
    "Gulab Jamun":    {"category": "Desserts",  "price":  90.0, "available": True},
    "Rasgulla":       {"category": "Desserts",  "price":  80.0, "available": True},
    "Ice Cream":      {"category": "Desserts",  "price": 110.0, "available": False},
}

inventory = {
    "Paneer Tikka":   {"stock": 10, "reorder_level": 3},
    "Chicken Wings":  {"stock":  8, "reorder_level": 2},
    "Veg Soup":       {"stock": 15, "reorder_level": 5},
    "Butter Chicken": {"stock": 12, "reorder_level": 4},
    "Dal Tadka":      {"stock": 20, "reorder_level": 5},
    "Veg Biryani":    {"stock":  6, "reorder_level": 3},
    "Garlic Naan":    {"stock": 30, "reorder_level": 10},
    "Gulab Jamun":    {"stock":  5, "reorder_level": 2},
    "Rasgulla":       {"stock":  4, "reorder_level": 3},
    "Ice Cream":      {"stock":  7, "reorder_level": 4},
}

sales_log = {
    "2025-01-01": [
        {"order_id": 1,  "items": ["Paneer Tikka", "Garlic Naan"], "total": 220.0},
        {"order_id": 2,  "items": ["Gulab Jamun", "Veg Soup"], "total": 210.0},
        {"order_id": 3,  "items": ["Butter Chicken", "Garlic Naan"], "total": 360.0},
    ],
    "2025-01-02": [
        {"order_id": 4,  "items": ["Dal Tadka", "Garlic Naan"], "total": 220.0},
        {"order_id": 5,  "items": ["Veg Biryani", "Gulab Jamun"], "total": 340.0},
    ],
    "2025-01-03": [
        {"order_id": 6,  "items": ["Paneer Tikka", "Rasgulla"], "total": 260.0},
        {"order_id": 7,  "items": ["Butter Chicken", "Veg Biryani"], "total": 570.0},
        {"order_id": 8,  "items": ["Garlic Naan", "Gulab Jamun"], "total": 130.0},
    ],
    "2025-01-04": [
        {"order_id": 9,  "items": ["Dal Tadka", "Garlic Naan", "Rasgulla"], "total": 300.0},
        {"order_id": 10, "items": ["Paneer Tikka", "Gulab Jamun"], "total": 270.0},
    ],
}

# ---------------- TASK 1 ----------------

print("\n--- MENU ---")

categories = ["Starters", "Mains", "Desserts"]

for category in categories:
    print(f"\n===== {category} =====")

    for item, details in menu.items():
        if details["category"] == category:
            status = "Available" if details["available"] else "Unavailable"
            print(f"{item:<15} ₹{details['price']:.2f}   [{status}]")

# stats
print("\nMenu Stats:")
print("Total items:", len(menu))

available_count = sum(1 for i in menu.values() if i["available"])
print("Available items:", available_count)

most_expensive = max(menu.items(), key=lambda x: x[1]["price"])
print("Most expensive item:", most_expensive[0], "-", most_expensive[1]["price"])

print("Items under ₹150:")
for item, details in menu.items():
    if details["price"] < 150:
        print(item, "-", details["price"])


# ---------------- TASK 2 ----------------

print("\n--- CART OPERATIONS ---")

cart = []

def add_to_cart(item_name, quantity):
    if item_name not in menu:
        print(f"{item_name} not found in menu")
        return

    if not menu[item_name]["available"]:
        print(f"{item_name} is unavailable")
        return

    for item in cart:
        if item["item"] == item_name:
            item["quantity"] += quantity
            return

    cart.append({
        "item": item_name,
        "quantity": quantity,
        "price": menu[item_name]["price"]
    })


def remove_from_cart(item_name):
    for item in cart:
        if item["item"] == item_name:
            cart.remove(item)
            return
    print(f"{item_name} not in cart")


# simulation

add_to_cart("Paneer Tikka", 2)
add_to_cart("Gulab Jamun", 1)
add_to_cart("Paneer Tikka", 1)
add_to_cart("Mystery Burger", 1)
add_to_cart("Chicken Wings", 1)
remove_from_cart("Gulab Jamun")

# order summary

print("\n========== Order Summary ==========")

subtotal = 0

for item in cart:
    total_price = item["quantity"] * item["price"]
    subtotal += total_price
    print(f"{item['item']:<15} x{item['quantity']}   ₹{total_price:.2f}")

gst = subtotal * 0.05
total = subtotal + gst

print("------------------------------------")
print(f"Subtotal: ₹{subtotal:.2f}")
print(f"GST (5%): ₹{gst:.2f}")
print(f"Total Payable: ₹{total:.2f}")
print("====================================")


# ---------------- TASK 3 ----------------

print("\n--- INVENTORY ---")

inventory_backup = copy.deepcopy(inventory)

# change one value
inventory["Paneer Tikka"]["stock"] -= 2

print("\nOriginal Inventory:")
print(inventory)

print("\nBackup Inventory:")
print(inventory_backup)

# restore
inventory = copy.deepcopy(inventory_backup)

# deduct based on cart

for item in cart:
    name = item["item"]
    qty = item["quantity"]

    if inventory[name]["stock"] < qty:
        print(f"Not enough stock for {name}")
        inventory[name]["stock"] = 0
    else:
        inventory[name]["stock"] -= qty

# reorder alerts
for item, data in inventory.items():
    if data["stock"] <= data["reorder_level"]:
        print(f"⚠ Reorder Alert: {item} — Only {data['stock']} left")


# ---------------- TASK 4 ----------------

print("\n--- SALES ANALYSIS ---")

# revenue per day
daily_revenue = {}

for date, orders in sales_log.items():
    total = sum(order["total"] for order in orders)
    daily_revenue[date] = total
    print(date, ":", total)

# best day
best_day = max(daily_revenue, key=daily_revenue.get)
print("Best Day:", best_day)

# most ordered item
item_count = {}

for orders in sales_log.values():
    for order in orders:
        for item in order["items"]:
            item_count[item] = item_count.get(item, 0) + 1

most_ordered = max(item_count, key=item_count.get)
print("Most Ordered Item:", most_ordered)

# add new day
sales_log["2025-01-05"] = [
    {"order_id": 11, "items": ["Butter Chicken", "Gulab Jamun", "Garlic Naan"], "total": 490.0},
    {"order_id": 12, "items": ["Paneer Tikka", "Rasgulla"], "total": 260.0},
]

print("\nUpdated Revenue:")

for date, orders in sales_log.items():
    total = sum(order["total"] for order in orders)
    print(date, ":", total)

# enumerate orders
print("\nAll Orders:")

count = 1
for date, orders in sales_log.items():
    for order in orders:
        items_str = ", ".join(order["items"])
        print(f"{count}. [{date}] Order #{order['order_id']} — ₹{order['total']} — Items: {items_str}")
        count += 1
