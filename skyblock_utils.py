# Imports
import requests
import json
from pprint import pprint

# # # Functions

# Returns GET request response from url
def get_info(call):
    r = requests.get(call)
    return r.json()

# Returns auction info from player uuid
def get_auctions_from_player(uuid):
    return get_info(f"https://api.hypixel.net/skyblock/auction?key={API_KEY}&player={uuid}")

# Returns Bazaar data
def get_bazaar_data():
    return get_info("https://api.hypixel.net/skyblock/bazaar")

# Returns recently finished auctions data
def get_recently_ended_auctions():
    return get_info("https://api.hypixel.net/skyblock/auctions_ended")

# Returns a list of all active auctions
def get_auction_data():
    all_auctions = []

    first_page = get_info("https://api.hypixel.net/skyblock/auctions?page=0")

    auction_data = first_page.get("auctions", [])

    for page in range(1, first_page.get("totalPages", 0) + 1):
        current_page = get_info(f"https://api.hypixel.net/skyblock/auctions?page={page}")
        all_auctions += current_page.get("auctions", [])

    return all_auctions

# Returns total coin count in buy orders on the bazaar
def get_bazaar_buy_order_value(bazaar_data):
    sum_coins = 0
    price_increase_threshold = 2
    buy_order_values = []

    # For every product
    for item_name, item_data in bazaar_data.get("products", {}).items():

        item_sum_coins = 0

        # For every buy order
        for idx, buy_order in enumerate(item_data.get("buy_summary", [])):

            # If its the best price
            if(idx == 0):
                item_expected_value = buy_order.get("pricePerUnit", 0)
                item_sum_coins += buy_order.get("amount", 0) * buy_order.get("pricePerUnit", 0)
            # If its not the best price, check for reasonable price
            else:
                if(buy_order.get("pricePerUnit", 0) < (item_expected_value * price_increase_threshold)):
                    item_sum_coins += buy_order.get("amount", 0) * buy_order.get("pricePerUnit", 0)

        buy_order_values.append((item_name, item_sum_coins))
        sum_coins += item_sum_coins

    sort_bazaar_buy_orders_by_value(buy_order_values)
    return sum_coins

# Sorts and displays a list of buy order items by total value
def sort_bazaar_buy_orders_by_value(buy_order_values):

    # Sort items by values
    buy_order_values.sort(key = lambda x: -x[1])

    # Display items and values
    for (item_name, item_sum_coins) in buy_order_values:
        print(f"{item_name.ljust(30, ' ')} | {round(item_sum_coins):,}")

    return

# Returns total coin count in recently ended auctions
def get_ended_auctions_value(ended_auctions_data):
    sum_coins = 0

    # For every auction object
    for auction_obj in ended_auctions_data.get("auctions", {}):

        # Add the sale price to the sum
        sum_coins += auction_obj.get("price", 0)

    return sum_coins

# Returns auction items after passing them through the filter
def filter_auction_items(auction_data, item_filters):
    filtered_items = []

    # For every auction object
    for auction in auction_data:

        # For every individual filter
        for item_filter in item_filters:

            # For every filter argument
            for filter_property, filter_value in item_filter.items():

                # String filters (item_name)
                if(type(filter_value) == type("")):
                    if(filter_value not in auction.get(filter_property, "")):
                        break

                # Boolean filters (bin)
                elif(type(filter_value) == type(True)):
                    if(filter_value != auction.get(filter_property, False)):
                        break

                # If all subfilters have passed
                filtered_items.append(auction)

    # filtered_items = sorted(filtered_items, key=lambda x: x['price'])

    return filtered_items

# Displays top x items from y list of auction objects
def display_top_auction_items(filtered_items, amount):
    for i in range(min(amount, len(filtered_items))):
        print(f"\n#{i+1} {filtered_items[i]['item_name']}\n - {filtered_items[i]['starting_bid']:,}\n- /viewauction {filtered_items[i]['uuid']}")

# Variables
API_FILE = open("API_KEY.json", "r")
API_KEY = json.loads(API_FILE.read())["API_KEY"]
example_player_uuid = "6a61acfe47c04f038ca6be4ae358e259"
item_filters = (
    {"item_name": "Drill", "bin": True},
    )

# Code
print(f"Bazaar Buy Order Eco: {get_bazaar_buy_order_value(get_bazaar_data()):,}")

print(f"Finished Auctions (60s) Eco: {get_ended_auctions_value(get_recently_ended_auctions()):,}")

auction_data = get_auction_data()

print(f"Amount of auction items: {len(auction_data):,}")

filtered_items = filter_auction_items(auction_data, item_filters)

print(f"Filtered auction items: {len(filtered_items):,}")

display_top_auction_items(filtered_items, 3)
