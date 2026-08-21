from collections import deque
from typing import List, Dict, Any, Deque, Tuple
import math

try:
    from .config import W_MARGIN, W_PCTR, W_RELEVANCE
except ImportError:
    from config import W_MARGIN, W_PCTR, W_RELEVANCE

class DashMartItem:
    def __init__(self, item_id: str, title: str, category: str, brand: str, 
                 base_price: float, margin_rate: float, pctr: float, in_stock: bool):
        self.item_id = item_id
        self.title = title
        self.category = category
        self.brand = brand
        self.base_price = base_price
        self.margin_rate = margin_rate
        self.pctr = pctr
        self.in_stock = in_stock
        self.composite_score = 0.0

class DashMartReRanker:
    def __init__(self, w_pctr: float = W_PCTR, w_margin: float = W_MARGIN,
                 w_rel: float = W_RELEVANCE):
        self.w_pctr = w_pctr
        self.w_margin = w_margin
        self.w_rel = w_rel

    def compute_relevance(self, query: str, title: str) -> float:
        """Simple keyword matching relevance logic."""
        if not isinstance(query, str) or not isinstance(title, str):
            return 0.0
        if not query or not title:
            return 0.0
        query_words = set(query.lower().split())
        title_words = set(title.lower().split())
        overlap = query_words.intersection(title_words)
        return len(overlap) / max(len(query_words), 1)

    def _is_eligible_item(self, item: DashMartItem) -> bool:
        """Return whether an item meets the stock and price guardrails."""
        try:
            base_price = getattr(item, "base_price", None)
            is_in_stock = getattr(item, "in_stock", None)
            return (
                is_in_stock is True
                and not isinstance(base_price, bool)
                and math.isfinite(float(base_price))
                and float(base_price) > 0
            )
        except (TypeError, ValueError):
            return False

    def _safe_numeric_value(self, value: Any) -> float:
        """Return a finite numeric value, defaulting invalid values to zero."""
        try:
            numeric_value = float(value)
            return numeric_value if math.isfinite(numeric_value) else 0.0
        except (TypeError, ValueError):
            return 0.0

    def compute_composite_score(self, query: str, item: DashMartItem) -> float:
        """Compute the weighted pCTR, margin, and relevance score for an item."""
        pctr = self._safe_numeric_value(getattr(item, "pctr", None))
        margin_rate = self._safe_numeric_value(getattr(item, "margin_rate", None))
        base_price = self._safe_numeric_value(getattr(item, "base_price", None))
        relevance = self.compute_relevance(query, getattr(item, "title", None))
        return (
            self.w_pctr * pctr
            + self.w_margin * (base_price * margin_rate)
            + self.w_rel * relevance
        )

    def _brand_key(self, item: DashMartItem) -> Tuple[str, Any]:
        """Return a normalized brand key without grouping missing brands together."""
        brand = getattr(item, "brand", None)
        if isinstance(brand, str) and brand.strip():
            return ("brand", brand.strip().casefold())
        return ("item", id(item))

    def rank_items(self, query: str, items: List[DashMartItem], top_k: int = 5) -> List[DashMartItem]:
        """Filter, score, and diversify items while preserving score priority."""
        # 1. Apply hard availability and price guardrails.
        valid_items = [item for item in (items or []) if self._is_eligible_item(item)]

        # 2. Assign a composite score to every remaining candidate.
        for item in valid_items:
            item.composite_score = self.compute_composite_score(query, item)

        # 3. Prioritize higher-scoring candidates before applying diversity rules.
        pending_items: Deque[DashMartItem] = deque(
            sorted(valid_items, key=lambda item: item.composite_score, reverse=True)
        )
        ranked_items: List[DashMartItem] = []
        last_selected_brands: Deque[Tuple[str, Any]] = deque(maxlen=2)
        deferred_items = 0

        # 4. Select up to top_k items, deferring a third consecutive brand.
        while pending_items and len(ranked_items) < top_k:
            item = pending_items.popleft()
            item_brand = self._brand_key(item)

            if len(last_selected_brands) == 2 and all(
                brand == item_brand for brand in last_selected_brands
            ):
                # Keep the candidate for a later position instead of discarding it.
                pending_items.append(item)
                deferred_items += 1

                # Stop when every remaining item would violate the constraint.
                if deferred_items >= len(pending_items):
                    break
                continue

            ranked_items.append(item)
            last_selected_brands.append(item_brand)
            deferred_items = 0

        return ranked_items

# --- UNIT TESTS ---
def _build_test_items(samples: List[Dict[str, Any]]) -> List[DashMartItem]:
    """Create DashMartItem objects from unit-test sample dictionaries."""
    return [
        DashMartItem(
            item_id=sample["item_id"],
            title=sample.get("title", "Snack item"),
            category=sample.get("category", "Snacks"),
            brand=sample["brand"],
            base_price=sample.get("base_price", 10.0),
            margin_rate=sample.get("margin_rate", 0.2),
            pctr=sample["pctr"],
            in_stock=sample.get("in_stock", True),
        )
        for sample in samples
    ]


def test_out_of_stock_filtering() -> None:
    """Verify that out-of-stock candidates are excluded from the output."""
    try:
        from .test_main import OUT_OF_STOCK_ITEMS
    except ImportError:
        from test_main import OUT_OF_STOCK_ITEMS

    ranked_items = DashMartReRanker().rank_items(
        "snack", _build_test_items(OUT_OF_STOCK_ITEMS)
    )

    assert [item.item_id for item in ranked_items] == ["available"]


def test_brand_diversity_guardrail() -> None:
    """Verify that no three consecutive ranked items share a brand."""
    try:
        from .test_main import BRAND_DIVERSITY_ITEMS
    except ImportError:
        from test_main import BRAND_DIVERSITY_ITEMS

    ranked_items = DashMartReRanker(w_pctr=1.0, w_margin=0.0, w_rel=0.0).rank_items(
        "", _build_test_items(BRAND_DIVERSITY_ITEMS), top_k=5
    )
    ranked_brands = [item.brand for item in ranked_items]

    assert [item.item_id for item in ranked_items] == ["a1", "a2", "b1", "a4", "a3"]
    assert all(
        not (
            ranked_brands[index]
            == ranked_brands[index + 1]
            == ranked_brands[index + 2]
        )
        for index in range(len(ranked_brands) - 2)
    )


def test_empty_candidates_and_queries() -> None:
    """Verify that empty candidate lists and queries are handled safely."""
    try:
        from .test_main import EMPTY_CANDIDATE_ITEMS, EMPTY_QUERY
    except ImportError:
        from test_main import EMPTY_CANDIDATE_ITEMS, EMPTY_QUERY

    ranker = DashMartReRanker()
    assert ranker.rank_items("snack", _build_test_items(EMPTY_CANDIDATE_ITEMS)) == []

    item = DashMartItem("item", "Snack item", "Snacks", "Brand A", 10.0, 0.2, 0.4, True)
    ranked_items = ranker.rank_items(EMPTY_QUERY, [item])
    expected_score = 0.5 * 0.4 + 0.3 * (10.0 * 0.2)

    assert len(ranked_items) == 1
    assert math.isclose(ranked_items[0].composite_score, expected_score)
