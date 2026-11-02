import sys

if __name__ == "__main__":
    print("=== Inventory System Analysis ===")
    inventory = {}
    for arg in sys.argv[1:]:
        parts = arg.split(':')
        if len(parts) != 2:
            print(f"Error - invalid parameter '{arg}'")
            continue
        item_name = parts[0]
        qty_str = parts[1]
        if item_name in inventory:
            print(f"Redundant item '{item_name}' - discarding")
            continue
        try:
            qty = int(qty_str)
            inventory[item_name] = qty
        except ValueError as e:
            print(f"Quantity error for '{item_name}': {e}")

    if len(inventory) > 0:
        print(f"Got inventory: {inventory}")
        item_list = list(inventory.keys())
        print(f"Item list: {item_list}")
        total_qty = sum(inventory.values())
        print(f"Total quantity of the {len(item_list)} items: {total_qty}")
        most_item = ""
        least_item = ""
        for item in item_list:
            qty = inventory[item]
            pct = (qty / total_qty) * 100
            print(f"Item {item} represents {round(pct, 1)}%")
            if most_item == "" or qty > inventory[most_item]:
                most_item = item
            if least_item == "" or qty < inventory[least_item]:
                least_item = item
        print(f"Item most abundant: {most_item} with "
              f"quantity {inventory[most_item]}")
        print(f"Item least abundant: {least_item} with "
              f"quantity {inventory[least_item]}")
        inventory.update({'magic_item': 1})
        print(f"Updated inventory: {inventory}")
    else:
        print("At the beginning of the game, "
              "your inventory is usually empty ;)")
