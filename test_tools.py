from src.tools.tools import (
    search_product,
    check_inventory,
    get_order_status
)

print(search_product("nonexistentproduct"))
print(check_inventory("P999"))
print(get_order_status("O9999"))
