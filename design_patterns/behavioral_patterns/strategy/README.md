# 🧠 **Strategy Pattern**

---

## 📋 Table of Contents
- [What is Strategy Pattern?](#-what-is-strategy-pattern)
  - [Key Characteristics](#-key-characteristics)
  - [The Problem It Solves](#-the-problem-it-solves)
  - [Real-World Analogy](#-real-world-analogy)
  - [Visual Representation](#-visual-representation)
- [When to Use](#-when-to-use)
- [When NOT to Use](#-when-not-to-use)
- [Basic Implementation](#-basic-implementation)
- [Real-World Examples](#-real-world-examples)
  - [Example 1: Payment Processing](#example-1-payment-processing)
  - [Example 2: Sorting & Filtering Engine](#example-2-sorting--filtering-engine)
  - [Example 3: Data Export Pipeline](#example-3-data-export-pipeline)
- [Common Pitfalls](#-common-pitfalls)
- [Best Practices](#-best-practices)
- [Summary](#-summary)
- [Strategy Pattern Checklist](#-strategy-pattern-checklist)
- [Key Takeaways](#-key-takeaways)

---

## 🔷 What is Strategy Pattern?

**Strategy Pattern** is a behavioral design pattern that defines a **family of algorithms**, encapsulates each one in its own class, and makes them **interchangeable at runtime**. The client selects which algorithm to use without knowing its implementation details.

---

### 🔑 Key Characteristics

| Characteristic              | Description                                       |
|-----------------------------|---------------------------------------------------|
| **Encapsulated Algorithms** | Each algorithm lives in its own class             |
| **Interchangeable**         | Strategies can be swapped at runtime              |
| **Open/Closed**             | Add new strategies without touching existing code |
| **Context-Agnostic**        | Context uses strategy via interface only          |
| **Eliminates Conditionals** | Replaces `if/elif` algorithm-selection chains     |

---

### 🔥 The Problem It Solves

Without Strategy, algorithm selection pollutes the context with conditionals:

```python
# ❌ WITHOUT Strategy — algorithm logic buried in the context
class DataExporter:
    def export(self, data, format_type: str):
        if format_type == "csv":
            # 30 lines of CSV logic here
            ...
        elif format_type == "json":
            # 30 lines of JSON logic here
            ...
        elif format_type == "xml":
            # 30 lines of XML logic here
            ...
        elif format_type == "excel":
            # 30 lines of Excel logic here
            ...
        # Adding "parquet" = modify this method again!
        # Testing CSV alone = impossible without the whole class!
```

With Strategy:

```python
# ✅ WITH Strategy — context is clean, algorithms are isolated
class DataExporter:
    def __init__(self, strategy: ExportStrategy):
        self._strategy = strategy

    def export(self, data):
        return self._strategy.export(data)   # delegates entirely

# Swap algorithm at runtime, add new ones freely, test each in isolation
```

---

### 🌍 Real-World Analogy

Think of **GPS navigation**:

```
Destination set → Choose strategy:
  🚗 Fastest Route    (highway-first algorithm)
  🌿 Eco Route        (fuel-efficient algorithm)
  🚶 Walking Route    (pedestrian-path algorithm)
  🚲 Cycling Route    (bike-lane algorithm)
```

- The **GPS app** (Context) is the same regardless of route type
- Each **route type** (Strategy) is a different algorithm
- You can **switch strategy** mid-journey without rebuilding the app
- The app never needs to know the internals of each routing algorithm

---

### 🖼️ Visual Representation

```
┌─────────────────────────────────────┐
│             Context                 │
│  _strategy: Strategy                │
│                                     │
│  set_strategy(strategy)             │
│  execute() ──────────────────────┐  │
└──────────────────────────────────┼──┘
                                   │ delegates
              ┌────────────────────┤
              │   Strategy (ABC)   │
              │   execute(data)    │
              └────────┬───────────┘
                       │ implements
       ┌───────────────┼───────────────┐
       ▼               ▼               ▼
┌───────────┐   ┌───────────┐   ┌───────────┐
│Strategy A │   │Strategy B │   │Strategy C │
│execute()  │   │execute()  │   │execute()  │
└───────────┘   └───────────┘   └───────────┘
  (Algorithm 1)  (Algorithm 2)   (Algorithm 3)
```

---

### 🔀 Participants

| Role                 | Responsibility                                                |
|----------------------|---------------------------------------------------------------|
| **Strategy**         | Common interface all concrete strategies implement            |
| **ConcreteStrategy** | A specific algorithm implementation                           |
| **Context**          | Holds a strategy reference; delegates execution to it         |
| **Client**           | Chooses and injects the appropriate strategy into the context |

---

## ✅ When to Use

| Scenario                                         | Why It Fits                          |
|--------------------------------------------------|--------------------------------------|
| Multiple **variants of an algorithm** exist      | Each variant = one strategy class    |
| Algorithm needs to be **swapped at runtime**     | `context.set_strategy(new_strategy)` |
| Large **conditional blocks** selecting behavior  | Replace with strategy injection      |
| Algorithms should be **testable in isolation**   | Each strategy has no dependencies    |
| Behavior varies by **user preference or config** | Inject the right strategy at startup |

---

## ❌ When NOT to Use

- When you only have **2 algorithms that never change** — a simple boolean flag is cleaner
- When algorithms are **trivially small** (one line) — overhead of a class isn't justified
- When **all clients always use the same algorithm** — no need for abstraction
- When algorithms need **deep access to context internals** — tight coupling defeats the purpose

---

## 🏗️ Basic Implementation

### Classic Structure

```python
from abc import ABC, abstractmethod

# ─────────────────────────────────────────
# Strategy Interface
# ─────────────────────────────────────────
class SortStrategy(ABC):
    @abstractmethod
    def sort(self, data: list[int]) -> list[int]:
        pass

    @property
    def name(self) -> str:
        return self.__class__.__name__


# ─────────────────────────────────────────
# Concrete Strategies
# ─────────────────────────────────────────
class BubbleSortStrategy(SortStrategy):
    def sort(self, data: list[int]) -> list[int]:
        arr = list(data)
        n   = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        print(f"  🫧 BubbleSort applied")
        return arr


class QuickSortStrategy(SortStrategy):
    def sort(self, data: list[int]) -> list[int]:
        arr = list(data)
        self._quick_sort(arr, 0, len(arr) - 1)
        print(f"  ⚡ QuickSort applied")
        return arr

    def _quick_sort(self, arr, low, high):
        if low < high:
            pi = self._partition(arr, low, high)
            self._quick_sort(arr, low, pi - 1)
            self._quick_sort(arr, pi + 1, high)

    def _partition(self, arr, low, high):
        pivot = arr[high]
        i     = low - 1
        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1


class PythonBuiltinSortStrategy(SortStrategy):
    def sort(self, data: list[int]) -> list[int]:
        print(f"  🐍 Python built-in sort (Timsort) applied")
        return sorted(data)


# ─────────────────────────────────────────
# Context
# ─────────────────────────────────────────
class Sorter:
    def __init__(self, strategy: SortStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: SortStrategy) -> None:
        print(f"  🔀 Strategy changed to: {strategy.name}")
        self._strategy = strategy

    def sort(self, data: list[int]) -> list[int]:
        print(f"  📊 Input : {data}")
        result = self._strategy.sort(data)
        print(f"  📊 Output: {result}")
        return result


# ─────────────────────────────────────────
# Client
# ─────────────────────────────────────────
data   = [64, 34, 25, 12, 22, 11, 90]
sorter = Sorter(BubbleSortStrategy())

sorter.sort(data)

sorter.set_strategy(QuickSortStrategy())
sorter.sort(data)

sorter.set_strategy(PythonBuiltinSortStrategy())
sorter.sort(data)
```

---

## 🌍 Real-World Examples

### Example 1: Payment Processing

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

class PaymentStatus(Enum):
    SUCCESS  = "success"
    FAILED   = "failed"
    PENDING  = "pending"
    REFUNDED = "refunded"

@dataclass
class PaymentResult:
    status:         PaymentStatus
    transaction_id: str
    amount:         float
    currency:       str         = "USD"
    message:        str         = ""
    timestamp:      datetime    = field(default_factory=datetime.now)
    metadata:       dict        = field(default_factory=dict)

    def __repr__(self):
        return (f"PaymentResult({self.status.value} | "
                f"txn={self.transaction_id} | ${self.amount:.2f})")


@dataclass
class PaymentRequest:
    amount:   float
    currency: str
    customer: str
    metadata: dict = field(default_factory=dict)


# ─────────────────────────────────────────
# Strategy Interface
# ─────────────────────────────────────────
class PaymentStrategy(ABC):

    @abstractmethod
    def pay(self, request: PaymentRequest) -> PaymentResult:
        pass

    @abstractmethod
    def refund(self, transaction_id: str, amount: float) -> PaymentResult:
        pass

    @abstractmethod
    def validate(self, request: PaymentRequest) -> tuple[bool, str]:
        """Returns (is_valid, error_message)."""
        pass

    @property
    def name(self) -> str:
        return self.__class__.__name__.replace("Strategy", "")


# ─────────────────────────────────────────
# Concrete Strategies
# ─────────────────────────────────────────
class CreditCardStrategy(PaymentStrategy):
    def __init__(self, card_number: str, expiry: str, cvv: str):
        self._card   = card_number[-4:]    # store only last 4 digits
        self._expiry = expiry
        self._cvv    = cvv                 # in real life, never store this!

    def validate(self, request: PaymentRequest) -> tuple[bool, str]:
        if request.amount <= 0:
            return False, "Amount must be positive"
        if request.amount > 10_000:
            return False, "Single transaction limit exceeded ($10,000)"
        return True, ""

    def pay(self, request: PaymentRequest) -> PaymentResult:
        valid, err = self.validate(request)
        if not valid:
            return PaymentResult(
                PaymentStatus.FAILED, "", request.amount, message=err
            )
        txn_id = f"CC-{datetime.now().strftime('%Y%m%d%H%M%S')}-{self._card}"
        print(f"  💳 Credit Card ****{self._card}: "
              f"charging ${request.amount:.2f}")
        return PaymentResult(
            status         = PaymentStatus.SUCCESS,
            transaction_id = txn_id,
            amount         = request.amount,
            currency       = request.currency,
            message        = f"Card ****{self._card} charged",
            metadata       = {"card_last4": self._card},
        )

    def refund(self, transaction_id: str, amount: float) -> PaymentResult:
        print(f"  💳 Credit Card: refunding ${amount:.2f} for {transaction_id}")
        return PaymentResult(
            status         = PaymentStatus.REFUNDED,
            transaction_id = f"REF-{transaction_id}",
            amount         = amount,
            message        = "Refund processed — 3-5 business days",
        )


class PayPalStrategy(PaymentStrategy):
    def __init__(self, email: str):
        self._email = email
        self._token: str | None = None

    def _authenticate(self) -> bool:
        # Simulate OAuth token fetch
        self._token = f"pp_token_{self._email[:5]}_xyz"
        print(f"  🔑 PayPal: authenticated as {self._email}")
        return True

    def validate(self, request: PaymentRequest) -> tuple[bool, str]:
        if request.amount > 50_000:
            return False, "PayPal limit exceeded ($50,000)"
        if request.currency not in ["USD", "EUR", "GBP"]:
            return False, f"Currency {request.currency} not supported by PayPal"
        return True, ""

    def pay(self, request: PaymentRequest) -> PaymentResult:
        valid, err = self.validate(request)
        if not valid:
            return PaymentResult(PaymentStatus.FAILED, "", request.amount, message=err)

        self._authenticate()
        txn_id = f"PP-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        print(f"  🅿️  PayPal ({self._email}): sending ${request.amount:.2f}")
        return PaymentResult(
            status         = PaymentStatus.SUCCESS,
            transaction_id = txn_id,
            amount         = request.amount,
            currency       = request.currency,
            message        = f"PayPal payment from {self._email}",
            metadata       = {"paypal_email": self._email, "token": self._token},
        )

    def refund(self, transaction_id: str, amount: float) -> PaymentResult:
        print(f"  🅿️  PayPal: refunding ${amount:.2f} for {transaction_id}")
        return PaymentResult(
            PaymentStatus.REFUNDED,
            f"PP-REF-{transaction_id}",
            amount,
            message="PayPal refund — instant",
        )


class CryptoStrategy(PaymentStrategy):
    def __init__(self, wallet_address: str, coin: str = "BTC"):
        self._wallet = wallet_address
        self._coin   = coin
        # Simulated exchange rates
        self._rates  = {"BTC": 45000.0, "ETH": 2500.0, "USDC": 1.0}

    def validate(self, request: PaymentRequest) -> tuple[bool, str]:
        if self._coin not in self._rates:
            return False, f"Unsupported coin: {self._coin}"
        if len(self._wallet) < 26:
            return False, "Invalid wallet address"
        return True, ""

    def pay(self, request: PaymentRequest) -> PaymentResult:
        valid, err = self.validate(request)
        if not valid:
            return PaymentResult(PaymentStatus.FAILED, "", request.amount, message=err)

        rate          = self._rates[self._coin]
        crypto_amount = request.amount / rate
        txn_id        = f"CRYPTO-{self._coin}-{datetime.now().strftime('%Y%m%d%H%M%S')}"

        print(f"  ₿  Crypto ({self._coin}): "
              f"{crypto_amount:.8f} {self._coin} "
              f"(${request.amount:.2f}) → {self._wallet[:8]}...")
        return PaymentResult(
            status         = PaymentStatus.PENDING,    # crypto needs confirmations
            transaction_id = txn_id,
            amount         = request.amount,
            message        = f"{crypto_amount:.8f} {self._coin} — awaiting confirmation",
            metadata       = {
                "coin":          self._coin,
                "crypto_amount": crypto_amount,
                "wallet":        self._wallet,
            },
        )

    def refund(self, transaction_id: str, amount: float) -> PaymentResult:
        print(f"  ₿  Crypto: refunds require manual processing for {transaction_id}")
        return PaymentResult(
            PaymentStatus.PENDING, f"CRYPTO-REF-{transaction_id}", amount,
            message="Crypto refund pending manual review",
        )


class BuyNowPayLaterStrategy(PaymentStrategy):
    def __init__(self, customer_id: str, installments: int = 4):
        self._customer_id  = customer_id
        self._installments = installments

    def validate(self, request: PaymentRequest) -> tuple[bool, str]:
        if request.amount < 50:
            return False, "BNPL minimum order is $50"
        if request.amount > 2000:
            return False, "BNPL maximum order is $2,000"
        return True, ""

    def pay(self, request: PaymentRequest) -> PaymentResult:
        valid, err = self.validate(request)
        if not valid:
            return PaymentResult(PaymentStatus.FAILED, "", request.amount, message=err)

        per_installment = request.amount / self._installments
        txn_id = f"BNPL-{self._customer_id}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        print(f"  🛍️  BNPL ({self._installments}x): "
              f"${per_installment:.2f}/installment for ${request.amount:.2f}")
        return PaymentResult(
            status         = PaymentStatus.SUCCESS,
            transaction_id = txn_id,
            amount         = request.amount,
            message        = f"{self._installments} installments of ${per_installment:.2f}",
            metadata       = {
                "installments":     self._installments,
                "per_installment":  per_installment,
            },
        )

    def refund(self, transaction_id: str, amount: float) -> PaymentResult:
        print(f"  🛍️  BNPL: cancelling remaining installments for {transaction_id}")
        return PaymentResult(
            PaymentStatus.REFUNDED, f"BNPL-REF-{transaction_id}", amount,
            message="BNPL plan cancelled, remaining installments voided",
        )


# ─────────────────────────────────────────
# Context: Checkout
# ─────────────────────────────────────────
class Checkout:
    def __init__(self, strategy: PaymentStrategy):
        self._strategy = strategy
        self._receipts: list[PaymentResult] = []

    def set_strategy(self, strategy: PaymentStrategy) -> None:
        print(f"  🔀 Payment method: {strategy.name}")
        self._strategy = strategy

    def process(self, amount: float, customer: str,
                currency: str = "USD", **meta) -> PaymentResult:
        req    = PaymentRequest(amount, currency, customer, metadata=meta)
        result = self._strategy.pay(req)
        self._receipts.append(result)
        print(f"  {'✅' if result.status == PaymentStatus.SUCCESS else '⏳' if result.status == PaymentStatus.PENDING else '❌'} "
              f"{result}")
        return result

    def refund_last(self) -> PaymentResult | None:
        if not self._receipts:
            print("  ❌ No transactions to refund.")
            return None
        last   = self._receipts[-1]
        result = self._strategy.refund(last.transaction_id, last.amount)
        print(f"  💵 Refund: {result}")
        return result


# ─────────────────────────────────────────
# Client
# ─────────────────────────────────────────
checkout = Checkout(CreditCardStrategy("4111111111111234", "12/26", "123"))

print("=== Credit Card Payment ===")
checkout.process(149.99, "Alice", order_id="ORD-001")

print("\n=== Switch to PayPal ===")
checkout.set_strategy(PayPalStrategy("alice@example.com"))
checkout.process(89.50, "Alice")

print("\n=== Switch to Crypto ===")
checkout.set_strategy(CryptoStrategy("1A2b3C4d5E6f7G8h9I0j", coin="ETH"))
checkout.process(500.00, "Alice")

print("\n=== Buy Now Pay Later ===")
checkout.set_strategy(BuyNowPayLaterStrategy("CUST-007", installments=4))
checkout.process(399.99, "Alice")

print("\n=== Refund Last ===")
checkout.refund_last()

print("\n=== Validation Failure ===")
checkout.set_strategy(BuyNowPayLaterStrategy("CUST-007"))
checkout.process(25.00, "Alice")   # below BNPL minimum
```

---

### Example 2: Sorting & Filtering Engine

```python
from abc import ABC, abstractmethod
from typing import List, TypeVar, Generic, Callable, Any
from dataclasses import dataclass
from functools import cmp_to_key
import time

T = TypeVar("T")

@dataclass
class Product:
    id:       int
    name:     str
    price:    float
    rating:   float
    category: str
    stock:    int

    def __repr__(self):
        return f"{self.name} (${self.price:.2f} | ⭐{self.rating} | {self.category})"


# ─────────────────────────────────────────
# Sort Strategy
# ─────────────────────────────────────────
class SortStrategy(ABC, Generic[T]):
    @abstractmethod
    def sort(self, items: List[T]) -> List[T]:
        pass

    @property
    def name(self) -> str:
        return self.__class__.__name__.replace("Sort", "").replace("Strategy", "")


class PriceAscendingSort(SortStrategy):
    def sort(self, items: List[Product]) -> List[Product]:
        return sorted(items, key=lambda p: p.price)


class PriceDescendingSort(SortStrategy):
    def sort(self, items: List[Product]) -> List[Product]:
        return sorted(items, key=lambda p: p.price, reverse=True)


class RatingSort(SortStrategy):
    def sort(self, items: List[Product]) -> List[Product]:
        return sorted(items, key=lambda p: p.rating, reverse=True)


class RelevanceSort(SortStrategy):
    """Composite score: weighted rating + inverse price + stock availability."""

    def _score(self, p: Product) -> float:
        price_score  = max(0, 100 - p.price) / 100
        rating_score = p.rating / 5.0
        stock_score  = min(p.stock, 10) / 10.0
        return (rating_score * 0.5) + (price_score * 0.3) + (stock_score * 0.2)

    def sort(self, items: List[Product]) -> List[Product]:
        return sorted(items, key=self._score, reverse=True)


# ─────────────────────────────────────────
# Filter Strategy
# ─────────────────────────────────────────
class FilterStrategy(ABC, Generic[T]):
    @abstractmethod
    def filter(self, items: List[T]) -> List[T]:
        pass

    def __and__(self, other: 'FilterStrategy') -> 'CompositeFilterStrategy':
        return CompositeFilterStrategy([self, other])

    @property
    def name(self) -> str:
        return self.__class__.__name__.replace("Filter", "").replace("Strategy", "")


class CompositeFilterStrategy(FilterStrategy):
    """Combines multiple filters with AND logic."""

    def __init__(self, filters: List[FilterStrategy]):
        self._filters = filters

    def filter(self, items: List[Product]) -> List[Product]:
        result = items
        for f in self._filters:
            result = f.filter(result)
        return result

    def __and__(self, other: FilterStrategy) -> 'CompositeFilterStrategy':
        return CompositeFilterStrategy(self._filters + [other])


class PriceRangeFilter(FilterStrategy):
    def __init__(self, min_price: float, max_price: float):
        self._min = min_price
        self._max = max_price

    def filter(self, items: List[Product]) -> List[Product]:
        return [p for p in items if self._min <= p.price <= self._max]


class CategoryFilter(FilterStrategy):
    def __init__(self, *categories: str):
        self._categories = set(c.lower() for c in categories)

    def filter(self, items: List[Product]) -> List[Product]:
        return [p for p in items if p.category.lower() in self._categories]


class MinRatingFilter(FilterStrategy):
    def __init__(self, min_rating: float):
        self._min = min_rating

    def filter(self, items: List[Product]) -> List[Product]:
        return [p for p in items if p.rating >= self._min]


class InStockFilter(FilterStrategy):
    def filter(self, items: List[Product]) -> List[Product]:
        return [p for p in items if p.stock > 0]


# ─────────────────────────────────────────
# Context: Product Search Engine
# ─────────────────────────────────────────
class ProductSearchEngine:
    def __init__(self, products: List[Product]):
        self._products       = products
        self._sort_strategy: SortStrategy   = RelevanceSort()
        self._filter_strategy: FilterStrategy = InStockFilter()

    def set_sort(self, strategy: SortStrategy) -> 'ProductSearchEngine':
        self._sort_strategy = strategy
        return self   # fluent interface

    def set_filter(self, strategy: FilterStrategy) -> 'ProductSearchEngine':
        self._filter_strategy = strategy
        return self

    def search(self, query: str = "") -> List[Product]:
        # 1. Optional text search
        results = self._products
        if query:
            q       = query.lower()
            results = [p for p in results
                       if q in p.name.lower() or q in p.category.lower()]

        # 2. Apply filter strategy
        results = self._filter_strategy.filter(results)

        # 3. Apply sort strategy
        results = self._sort_strategy.sort(results)

        print(f"\n  🔍 Query: '{query or '*'}' | "
              f"Filter: {self._filter_strategy.name} | "
              f"Sort: {self._sort_strategy.name} | "
              f"Results: {len(results)}")
        for i, p in enumerate(results, 1):
            print(f"     {i}. {p}")

        return results


# ─────────────────────────────────────────
# Client
# ─────────────────────────────────────────
products = [
    Product(1, "Python Cookbook",     49.99, 4.8, "Books",       15),
    Product(2, "Mechanical Keyboard", 89.00, 4.6, "Electronics",  8),
    Product(3, "USB-C Hub",           29.99, 4.2, "Electronics",  0),   # out of stock
    Product(4, "Design Patterns",     39.99, 4.9, "Books",        5),
    Product(5, "Webcam HD",           69.00, 4.1, "Electronics",  3),
    Product(6, "Standing Desk",      299.00, 4.7, "Furniture",    2),
    Product(7, "Ergonomic Chair",    249.00, 4.5, "Furniture",    0),   # out of stock
    Product(8, "Clean Code",          34.99, 4.7, "Books",       20),
]

engine = ProductSearchEngine(products)

print("=== Default (Relevance, In-Stock only) ===")
engine.search()

print("\n=== Books sorted by Rating ===")
engine.set_filter(CategoryFilter("books")) \
      .set_sort(RatingSort()) \
      .search()

print("\n=== Electronics under $80, in-stock, price ascending ===")
combined_filter = PriceRangeFilter(0, 80) & CategoryFilter("electronics") & InStockFilter()
engine.set_filter(combined_filter) \
      .set_sort(PriceAscendingSort()) \
      .search()

print("\n=== All products rated 4.5+, price high to low ===")
engine.set_filter(MinRatingFilter(4.5)) \
      .set_sort(PriceDescendingSort()) \
      .search()
```

---

### Example 3: Data Export Pipeline

```python
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json

@dataclass
class ExportResult:
    format:    str
    content:   str
    size_bytes: int
    rows:      int
    timestamp: datetime = field(default_factory=datetime.now)

    def preview(self, lines: int = 5) -> None:
        content_lines = self.content.split("\n")
        shown = "\n".join(content_lines[:lines])
        print(f"\n  📄 {self.format} Preview ({self.rows} rows, "
              f"{self.size_bytes} bytes):\n{shown}")
        if len(content_lines) > lines:
            print(f"  ... ({len(content_lines) - lines} more lines)")


# ─────────────────────────────────────────
# Compression Strategy
# ─────────────────────────────────────────
class CompressionStrategy(ABC):
    @abstractmethod
    def compress(self, data: str) -> str:
        pass

    @property
    def name(self) -> str:
        return self.__class__.__name__.replace("Compression", "")


class NoCompression(CompressionStrategy):
    def compress(self, data: str) -> str:
        return data


class RunLengthEncoding(CompressionStrategy):
    """Simple RLE — demo only, not real gzip."""
    def compress(self, data: str) -> str:
        if not data:
            return data
        result, count, char = [], 1, data[0]
        for c in data[1:]:
            if c == char:
                count += 1
            else:
                result.append(f"{count}{char}" if count > 1 else char)
                char, count = c, 1
        result.append(f"{count}{char}" if count > 1 else char)
        compressed = "".join(result)
        print(f"  🗜️  RLE: {len(data)} → {len(compressed)} bytes "
              f"({100 * (1 - len(compressed)/len(data)):.1f}% reduction)")
        return compressed


# ─────────────────────────────────────────
# Export Format Strategy
# ─────────────────────────────────────────
class ExportStrategy(ABC):
    def __init__(self, compression: CompressionStrategy = None):
        self._compression = compression or NoCompression()

    @abstractmethod
    def export(self, data: List[Dict[str, Any]],
               columns: Optional[List[str]] = None) -> ExportResult:
        pass

    @property
    def format_name(self) -> str:
        return self.__class__.__name__.replace("ExportStrategy", "")

    def _apply_compression(self, content: str) -> str:
        return self._compression.compress(content)


class CSVExportStrategy(ExportStrategy):
    def __init__(self, delimiter: str = ",", compression=None):
        super().__init__(compression)
        self._delimiter = delimiter

    def export(self, data: List[Dict], columns: Optional[List[str]] = None) -> ExportResult:
        if not data:
            return ExportResult("CSV", "", 0, 0)

        cols    = columns or list(data[0].keys())
        lines   = [self._delimiter.join(str(c) for c in cols)]

        for row in data:
            values = []
            for col in cols:
                val = str(row.get(col, ""))
                # Escape delimiter inside values
                if self._delimiter in val:
                    val = f'"{val}"'
                values.append(val)
            lines.append(self._delimiter.join(values))

        content = self._apply_compression("\n".join(lines))
        print(f"  📊 CSV: exported {len(data)} rows, "
              f"{len(cols)} columns")
        return ExportResult("CSV", content, len(content.encode()), len(data))


class JSONExportStrategy(ExportStrategy):
    def __init__(self, indent: int = 2, compression=None):
        super().__init__(compression)
        self._indent = indent

    def export(self, data: List[Dict], columns: Optional[List[str]] = None) -> ExportResult:
        filtered = data
        if columns:
            filtered = [{k: row[k] for k in columns if k in row} for row in data]

        content = self._apply_compression(
            json.dumps(filtered, indent=self._indent, default=str)
        )
        print(f"  📋 JSON: exported {len(data)} records")
        return ExportResult("JSON", content, len(content.encode()), len(data))


class MarkdownExportStrategy(ExportStrategy):
    def export(self, data: List[Dict], columns: Optional[List[str]] = None) -> ExportResult:
        if not data:
            return ExportResult("Markdown", "", 0, 0)

        cols  = columns or list(data[0].keys())
        lines = []

        # Header row
        lines.append("| " + " | ".join(str(c) for c in cols) + " |")
        # Separator row
        lines.append("| " + " | ".join("---" for _ in cols) + " |")
        # Data rows
        for row in data:
            cells = [str(row.get(col, "")) for col in cols]
            lines.append("| " + " | ".join(cells) + " |")

        content = self._apply_compression("\n".join(lines))
        print(f"  📝 Markdown: exported {len(data)} rows as table")
        return ExportResult("Markdown", content, len(content.encode()), len(data))


class SQLExportStrategy(ExportStrategy):
    def __init__(self, table_name: str = "export", compression=None):
        super().__init__(compression)
        self._table = table_name

    def _quote(self, val: Any) -> str:
        if val is None:
            return "NULL"
        if isinstance(val, (int, float)):
            return str(val)
        return f"'{str(val).replace(chr(39), chr(39)*2)}'"

    def export(self, data: List[Dict], columns: Optional[List[str]] = None) -> ExportResult:
        if not data:
            return ExportResult("SQL", "", 0, 0)

        cols  = columns or list(data[0].keys())
        lines = []

        # CREATE TABLE
        col_defs = ", ".join(f"{c} TEXT" for c in cols)
        lines.append(f"CREATE TABLE IF NOT EXISTS {self._table} ({col_defs});")
        lines.append("")

        # INSERT statements
        for row in data:
            values    = ", ".join(self._quote(row.get(c)) for c in cols)
            col_names = ", ".join(cols)
            lines.append(
                f"INSERT INTO {self._table} ({col_names}) VALUES ({values});"
            )

        content = self._apply_compression("\n".join(lines))
        print(f"  🗄️  SQL: exported {len(data)} INSERT statements "
              f"for table '{self._table}'")
        return ExportResult("SQL", content, len(content.encode()), len(data))


# ─────────────────────────────────────────
# Context: Report Exporter
# ─────────────────────────────────────────
class ReportExporter:
    def __init__(self, strategy: ExportStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: ExportStrategy) -> None:
        print(f"  🔀 Export strategy: {strategy.format_name}")
        self._strategy = strategy

    def export(self, data: List[Dict],
               columns: Optional[List[str]] = None,
               preview: bool = True) -> ExportResult:
        result = self._strategy.export(data, columns)
        if preview:
            result.preview()
        return result


# ─────────────────────────────────────────
# Client
# ─────────────────────────────────────────
sales_data = [
    {"id": 1, "product": "Python Book",   "qty": 5,  "revenue": 249.95, "region": "US"},
    {"id": 2, "product": "Keyboard",      "qty": 2,  "revenue": 178.00, "region": "EU"},
    {"id": 3, "product": "Webcam",        "qty": 8,  "revenue": 552.00, "region": "US"},
    {"id": 4, "product": "Standing Desk", "qty": 1,  "revenue": 299.00, "region": "CA"},
    {"id": 5, "product": "Clean Code",    "qty": 12, "revenue": 419.88, "region": "US"},
]

exporter = ReportExporter(CSVExportStrategy())

print("=== CSV Export ===")
exporter.export(sales_data, columns=["product", "qty", "revenue"])

print("\n=== JSON Export ===")
exporter.set_strategy(JSONExportStrategy(indent=2))
exporter.export(sales_data)

print("\n=== Markdown Export ===")
exporter.set_strategy(MarkdownExportStrategy())
exporter.export(sales_data, columns=["product", "qty", "revenue", "region"])

print("\n=== SQL Export ===")
exporter.set_strategy(SQLExportStrategy(table_name="sales_report"))
exporter.export(sales_data, columns=["id", "product", "qty", "revenue"])

print("\n=== CSV with Compression ===")
exporter.set_strategy(CSVExportStrategy(compression=RunLengthEncoding()))
exporter.export(sales_data, preview=False)
```

---

## ⚠️ Common Pitfalls

### ❌ Pitfall 1: Leaking Context Knowledge Into Strategies

```python
# ❌ WRONG — strategy knows too much about the context's internals
class BadSortStrategy(SortStrategy):
    def sort(self, context: Sorter) -> list:
        data = context._raw_data          # reaches into context!
        context._is_sorted = True         # modifies context state!
        return sorted(data)

# ✅ CORRECT — strategy only operates on the data it receives
class GoodSortStrategy(SortStrategy):
    def sort(self, data: list[int]) -> list[int]:
        return sorted(data)               # self-contained
```

### ❌ Pitfall 2: Strategy Proliferation for Trivial Variants

```python
# ❌ OVERKILL — creating a class for a one-liner variation
class AscendingSort(SortStrategy):
    def sort(self, data): return sorted(data)

class DescendingSort(SortStrategy):
    def sort(self, data): return sorted(data, reverse=True)

# ✅ BETTER — use a configurable strategy or a lambda
class ConfigurableSortStrategy(SortStrategy):
    def __init__(self, key=None, reverse: bool = False):
        self._key     = key
        self._reverse = reverse

    def sort(self, data):
        return sorted(data, key=self._key, reverse=self._reverse)

# Or simply pass callables for trivial cases:
sorter = Sorter(strategy=lambda data: sorted(data, reverse=True))
```

### ❌ Pitfall 3: Forgetting Strategies Are Stateless by Default

```python
# ❌ WRONG — mutable state in a shared strategy causes bugs
class BadCachingSort(SortStrategy):
    def __init__(self):
        self._cache = {}    # shared across all contexts using this strategy!

    def sort(self, data):
        key = tuple(data)
        if key not in self._cache:
            self._cache[key] = sorted(data)
        return self._cache[key]

# Two contexts share one instance → one's data leaks into the other's cache!

# ✅ CORRECT — keep strategies stateless, OR create one instance per context
```

### ❌ Pitfall 4: Using Strategy Where State Pattern Fits Better

```python
# ❌ MISUSE — using Strategy when behavior changes based on lifecycle
class OrderProcessor:
    def process(self, order, strategy):
        strategy.process(order)
        # But which strategy is valid depends on order.status!
        # This is a STATE problem, not a strategy problem.

# ✅ CORRECT — if the algorithm choice depends on internal lifecycle state,
# use the State Pattern instead of Strategy.
```

---

## ✅ Best Practices

### 1. Accept Callables as Lightweight Strategies

```python
from typing import Callable

# ✅ For simple cases, accept plain callables — no need for a class
class Sorter:
    def __init__(self, sort_fn: Callable = sorted):
        self._sort_fn = sort_fn

    def sort(self, data):
        return self._sort_fn(data)

# Usage — zero boilerplate
sorter = Sorter(sort_fn=lambda d: sorted(d, key=lambda x: -x))
```

### 2. Make Strategies Composable

```python
# ✅ Composable filters via & operator
in_stock = InStockFilter()
books    = CategoryFilter("books")
cheap    = PriceRangeFilter(0, 50)

combined = in_stock & books & cheap   # CompositeFilterStrategy
results  = engine.set_filter(combined).search()
```

### 3. Provide a Default Strategy

```python
class DataExporter:
    def __init__(self, strategy: ExportStrategy = None):
        self._strategy = strategy or CSVExportStrategy()   # sensible default
```

### 4. Name Strategies Clearly

```python
# ✅ Name reflects WHAT the strategy does, not HOW
class HighestRatedFirstSort(SortStrategy): ...    # clear
class RelevanceSort(SortStrategy):         ...    # clear
class MergeSort(SortStrategy):             ...    # implementation detail — less clear

# ✅ For payment strategies, name reflects the provider/method:
class PayPalStrategy(PaymentStrategy):  ...
class CryptoStrategy(PaymentStrategy):  ...
```

---

## 📊 Summary

| Aspect             | Detail                                                                  |
|--------------------|-------------------------------------------------------------------------|
| **Type**           | Behavioral                                                              |
| **Intent**         | Define a family of algorithms and make them interchangeable             |
| **Eliminates**     | Conditional chains selecting algorithm variants                         |
| **Key Roles**      | Strategy (interface), ConcreteStrategy (algorithm), Context (delegates) |
| **Python Bonus**   | Strategies can be plain callables — no class needed for simple cases    |
| **Real-world Use** | Payment methods, sorting, compression, export formats, routing          |

---

## ✅ Strategy Pattern Checklist

- Does each strategy implement only ONE algorithm with NO side effects on context?
- Can strategies be swapped at runtime via set_strategy()?
- Is the context fully decoupled — it knows only the Strategy interface?
- Are trivial strategies implemented as callables rather than classes?
- Is there a sensible default strategy?
- Are strategies composable for combined behavior (e.g. filter1 & filter2)?
- Can each strategy be unit-tested completely independently?
- Are strategy names descriptive of WHAT they do, not HOW?

---

## 💡 Key Takeaways

1. **Encapsulates algorithms** — each lives in its own class, testable and swappable independently
2. **Eliminates conditionals** — no more `if format == "csv": ... elif format == "json":`
3. **Callables are valid strategies** in Python — for simple cases, skip the class entirely
4. **Composability is a superpower** — chain strategies together for complex behavior
5. **Open/Closed in action** — add `ParquetExportStrategy` without touching `DataExporter`
6. **Key difference from State** — Strategy swaps *algorithms chosen by the client*; State swaps *behavior driven by internal lifecycle*
