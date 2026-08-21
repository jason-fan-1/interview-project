"""Sample candidate data for the unit tests in main.py."""

OUT_OF_STOCK_ITEMS = [
    {
        "item_id": "available",
        "title": "Snack item",
        "category": "Snacks",
        "brand": "Brand A",
        "base_price": 10.0,
        "margin_rate": 0.2,
        "pctr": 0.5,
        "in_stock": True,
    },
    {
        "item_id": "unavailable",
        "title": "Unavailable snack",
        "category": "Snacks",
        "brand": "Brand B",
        "base_price": 10.0,
        "margin_rate": 0.2,
        "pctr": 0.9,
        "in_stock": False,
    },
]

BRAND_DIVERSITY_ITEMS = [
    {"item_id": "a1", "brand": "Brand A", "pctr": 0.9},
    {"item_id": "a2", "brand": "Brand A", "pctr": 0.8},
    {"item_id": "a3", "brand": "Brand A", "pctr": 0.7},
    {"item_id": "b1", "brand": "Brand B", "pctr": 0.6},
    {"item_id": "a4", "brand": "Brand A", "pctr": 0.5},
]

EMPTY_CANDIDATE_ITEMS = []
EMPTY_QUERY = ""
