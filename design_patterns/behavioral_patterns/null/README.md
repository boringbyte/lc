# 🧠 **Null Object Pattern**

---

## 📋 Table of Contents
- [What is Null Object Pattern?](#-what-is-null-object-pattern)
  - [Key Characteristics](#-key-characteristics)
  - [The Problem It Solves](#-the-problem-it-solves)
  - [Real-World Analogy](#-real-world-analogy)
  - [Visual Representation](#-visual-representation)
- [When to Use](#-when-to-use)
- [When NOT to Use](#-when-not-to-use)
- [Basic Implementation](#-basic-implementation)
- [Real-World Examples](#-real-world-examples)
  - [Example 1: Logger System](#example-1-logger-system)
  - [Example 2: Payment & Discount System](#example-2-payment--discount-system)
  - [Example 3: User Permission System](#example-3-user-permission-system)
- [Common Pitfalls](#-common-pitfalls)
- [Best Practices](#-best-practices)
- [Summary](#-summary)
- [Null Object Pattern Checklist](#-null-object-pattern-checklist)
- [Key Takeaways](#-key-takeaways)

---

## 🔷 What is Null Object Pattern?

**Null Object Pattern** is a behavioral design pattern that provides a **default object with do-nothing behavior** as a substitute for `None`. Instead of checking `if obj is not None` everywhere, you always have a valid object that simply does nothing when called.

It eliminates `None` checks by making "absence" an explicit, safe, callable object.

---

### 🔑 Key Characteristics

| Characteristic               | Description                                                |
|------------------------------|------------------------------------------------------------|
| **No `None` checks**         | Client code never needs `if obj is not None`               |
| **Do-nothing behavior**      | Null object implements the interface but does nothing      |
| **Transparent substitution** | Client treats real and null objects identically            |
| **Safe defaults**            | Null objects return safe neutral values (0, "", [], False) |
| **Encapsulates absence**     | "No object" becomes an explicit design decision            |

---

### 🔥 The Problem It Solves

Without Null Object, `None` checks pollute the entire codebase:

```python
# ❌ WITHOUT Null Object — None checks scattered everywhere
class Order:
    def __init__(self, discount=None, logger=None):
        self._discount = discount
        self._logger   = logger

    def checkout(self, amount: float) -> float:
        if self._logger:                        # check 1
            self._logger.log("Starting checkout")

        if self._discount:                      # check 2
            amount = self._discount.apply(amount)

        if self._logger:                        # check 3
            self._logger.log(f"Final: {amount}")

        return amount

# Every method has repetitive None guards — forget one and it crashes!
```

With Null Object:

```python
# ✅ WITH Null Object — zero None checks, clean code
class Order:
    def __init__(self,
                 discount: Discount = NullDiscount(),
                 logger: Logger     = NullLogger()):
        self._discount = discount
        self._logger   = logger

    def checkout(self, amount: float) -> float:
        self._logger.log("Starting checkout")       # always safe
        amount = self._discount.apply(amount)       # always safe
        self._logger.log(f"Final: {amount}")        # always safe
        return amount
```

---

### 🌍 Real-World Analogy

Think of a **volume knob turned to zero**:

```
Real Speaker  → plays sound at set volume
Null Speaker  → knob at 0 — accepts commands, produces nothing

TV.set_volume(50)  → sound plays
TV.set_volume(0)   → silence, but no error, no crash, no "if speaker exists" check
```

The TV doesn't need to check "do I have a speaker?" — the null speaker just silently absorbs all commands.

---

### 🖼️ Visual Representation

```
┌─────────────────────────────────────────┐
│            AbstractObject               │
│         operation() → abstract          │
└──────────────┬──────────────────────────┘
               │ implements
    ┌──────────┴──────────┐
    ▼                     ▼
┌──────────────┐   ┌──────────────────┐
│  RealObject  │   │   NullObject     │
│              │   │                  │
│ operation()  │   │ operation()      │
│ → does work  │   │ → does NOTHING   │
│ → returns    │   │ → returns safe   │
│   real value │   │   neutral value  │
└──────────────┘   └──────────────────┘
        ▲                  ▲
        └──────────────────┘
                │
            Client uses
         both identically —
         no isinstance checks
```

---

## ✅ When to Use

| Scenario                                                 | Why It Fits                       |
|----------------------------------------------------------|-----------------------------------|
| **Optional dependencies** (logger, notifier, cache)      | Inject NullLogger instead of None |
| **Default do-nothing behavior** when no real impl exists | Null object is the safe default   |
| **Repeated `if obj is not None` checks** throughout code | Replace with null object          |
| **Testing** — disable side effects without mock setup    | NullLogger, NullMailer, NullCache |
| **Guest/anonymous users**                                | NullUser with zero permissions    |

---

## ❌ When NOT to Use

- When `None` **carries meaningful semantic information** — "no result found" should stay `None` or `Optional`
- When the absence should **raise an error** — silence can hide bugs
- When the null object needs to **return meaningful values** that differ per call site — hard to generalize
- When a **single None check** would suffice — don't over-engineer

---

## 🏗️ Basic Implementation

### Classic Structure

```python
from abc import ABC, abstractmethod

# ─────────────────────────────────────────
# Abstract Interface
# ─────────────────────────────────────────
class Animal(ABC):
    @abstractmethod
    def make_sound(self) -> str:
        pass

    @abstractmethod
    def move(self) -> str:
        pass

    @abstractmethod
    def is_null(self) -> bool:
        pass


# ─────────────────────────────────────────
# Real Object
# ─────────────────────────────────────────
class Dog(Animal):
    def __init__(self, name: str):
        self.name = name

    def make_sound(self) -> str:
        return f"{self.name} says: Woof!"

    def move(self) -> str:
        return f"{self.name} runs happily."

    def is_null(self) -> bool:
        return False


class Cat(Animal):
    def __init__(self, name: str):
        self.name = name

    def make_sound(self) -> str:
        return f"{self.name} says: Meow!"

    def move(self) -> str:
        return f"{self.name} slinks gracefully."

    def is_null(self) -> bool:
        return False


# ─────────────────────────────────────────
# Null Object
# ─────────────────────────────────────────
class NullAnimal(Animal):
    """
    Represents 'no animal'. Safe to call any method on.
    Returns neutral values, never raises exceptions.
    """

    def make_sound(self) -> str:
        return ""         # neutral: empty string

    def move(self) -> str:
        return ""         # neutral: empty string

    def is_null(self) -> bool:
        return True       # allows explicit null check when truly needed


# ─────────────────────────────────────────
# Factory — returns NullAnimal instead of None
# ─────────────────────────────────────────
class AnimalShelter:
    def __init__(self):
        self._animals = {
            "buddy": Dog("Buddy"),
            "whiskers": Cat("Whiskers"),
        }

    def get_animal(self, name: str) -> Animal:
        return self._animals.get(name.lower(), NullAnimal())
        # Never returns None — always returns a valid Animal


# ─────────────────────────────────────────
# Client — zero None checks
# ─────────────────────────────────────────
shelter = AnimalShelter()

for name in ["buddy", "whiskers", "ghost", "unknown"]:
    animal = shelter.get_animal(name)
    sound  = animal.make_sound()
    move   = animal.move()
    if sound:   # only print if something to say
        print(f"  🐾 {sound}")
    if move:
        print(f"  🐾 {move}")
    if animal.is_null():
        print(f"  ❓ '{name}' not found in shelter")

# Output:
#   🐾 Buddy says: Woof!
#   🐾 Buddy runs happily.
#   🐾 Whiskers says: Meow!
#   🐾 Whiskers slinks gracefully.
#   ❓ 'ghost' not found in shelter
#   ❓ 'unknown' not found in shelter
```

---

## 🌍 Real-World Examples

### Example 1: Logger System

```python
from abc import ABC, abstractmethod
from typing import Any
from datetime import datetime
from enum import Enum

class LogLevel(Enum):
    DEBUG   = 10
    INFO    = 20
    WARNING = 30
    ERROR   = 40

# ─────────────────────────────────────────
# Abstract Logger
# ─────────────────────────────────────────
class Logger(ABC):
    @abstractmethod
    def debug(self, msg: str, **context: Any) -> None:
        pass

    @abstractmethod
    def info(self, msg: str, **context: Any) -> None:
        pass

    @abstractmethod
    def warning(self, msg: str, **context: Any) -> None:
        pass

    @abstractmethod
    def error(self, msg: str, **context: Any) -> None:
        pass

    @abstractmethod
    def is_null(self) -> bool:
        pass


# ─────────────────────────────────────────
# Real Logger
# ─────────────────────────────────────────
class ConsoleLogger(Logger):
    def __init__(self, level: LogLevel = LogLevel.DEBUG, prefix: str = ""):
        self._level  = level
        self._prefix = prefix

    def _log(self, level: LogLevel, msg: str, **ctx) -> None:
        if level.value < self._level.value:
            return
        ts      = datetime.now().strftime("%H:%M:%S")
        prefix  = f"[{self._prefix}] " if self._prefix else ""
        context = " | ".join(f"{k}={v}" for k, v in ctx.items())
        context = f" | {context}" if context else ""
        print(f"  [{ts}] {level.name:<7} {prefix}{msg}{context}")

    def debug(self, msg: str, **ctx) -> None:
        self._log(LogLevel.DEBUG, msg, **ctx)

    def info(self, msg: str, **ctx) -> None:
        self._log(LogLevel.INFO, msg, **ctx)

    def warning(self, msg: str, **ctx) -> None:
        self._log(LogLevel.WARNING, msg, **ctx)

    def error(self, msg: str, **ctx) -> None:
        self._log(LogLevel.ERROR, msg, **ctx)

    def is_null(self) -> bool:
        return False


class FileLogger(Logger):
    def __init__(self, filepath: str, level: LogLevel = LogLevel.INFO):
        self._filepath = filepath
        self._level    = level
        self._entries  = []  # simulate file writes

    def _log(self, level: LogLevel, msg: str, **ctx) -> None:
        if level.value < self._level.value:
            return
        ts    = datetime.now().isoformat()
        entry = {"ts": ts, "level": level.name, "msg": msg, **ctx}
        self._entries.append(entry)
        print(f"  📁 FILE → {self._filepath}: {entry}")

    def debug(self, msg, **ctx):   self._log(LogLevel.DEBUG,   msg, **ctx)
    def info(self, msg, **ctx):    self._log(LogLevel.INFO,    msg, **ctx)
    def warning(self, msg, **ctx): self._log(LogLevel.WARNING, msg, **ctx)
    def error(self, msg, **ctx):   self._log(LogLevel.ERROR,   msg, **ctx)
    def is_null(self) -> bool:     return False


# ─────────────────────────────────────────
# Null Logger — the silent stand-in
# ─────────────────────────────────────────
class NullLogger(Logger):
    """
    Does absolutely nothing. Safe to call any method on.
    Use as default when logging is optional or unwanted (e.g. tests).
    """
    def debug(self, msg: str, **ctx) -> None:   pass
    def info(self, msg: str, **ctx) -> None:    pass
    def warning(self, msg: str, **ctx) -> None: pass
    def error(self, msg: str, **ctx) -> None:   pass
    def is_null(self) -> bool:                  return True


# ─────────────────────────────────────────
# Composite Logger — logs to multiple sinks
# ─────────────────────────────────────────
class CompositeLogger(Logger):
    """Fans out log calls to multiple loggers."""

    def __init__(self, *loggers: Logger):
        self._loggers = [l for l in loggers if not l.is_null()]

    def debug(self, msg, **ctx):
        for l in self._loggers: l.debug(msg, **ctx)

    def info(self, msg, **ctx):
        for l in self._loggers: l.info(msg, **ctx)

    def warning(self, msg, **ctx):
        for l in self._loggers: l.warning(msg, **ctx)

    def error(self, msg, **ctx):
        for l in self._loggers: l.error(msg, **ctx)

    def is_null(self) -> bool:
        return len(self._loggers) == 0


# ─────────────────────────────────────────
# Service using Logger — zero None checks
# ─────────────────────────────────────────
class OrderService:
    def __init__(self, logger: Logger = NullLogger()):
        self._logger = logger   # NullLogger is the safe default

    def place_order(self, order_id: str, amount: float) -> dict:
        self._logger.info("Placing order", order_id=order_id, amount=amount)

        if amount <= 0:
            self._logger.error("Invalid amount", order_id=order_id)
            return {"status": "error", "message": "Invalid amount"}

        self._logger.debug("Validating inventory", order_id=order_id)
        # ... business logic ...
        self._logger.info("Order placed successfully", order_id=order_id)
        return {"status": "success", "order_id": order_id}

    def cancel_order(self, order_id: str) -> None:
        self._logger.warning("Cancelling order", order_id=order_id)
        # ... cancel logic ...
        self._logger.info("Order cancelled", order_id=order_id)


# ─────────────────────────────────────────
# Client
# ─────────────────────────────────────────
print("=== Production: Console + File logging ===\n")
prod_logger = CompositeLogger(
    ConsoleLogger(level=LogLevel.DEBUG, prefix="ORDER"),
    FileLogger("orders.log", level=LogLevel.INFO),
)
prod_service = OrderService(logger=prod_logger)
prod_service.place_order("ORD-001", 149.99)

print("\n=== Testing: Silent (NullLogger default) ===\n")
test_service = OrderService()   # no logger passed — uses NullLogger
result = test_service.place_order("ORD-TEST", 99.99)
print(f"  Result: {result}")    # works perfectly, zero log noise

print("\n=== Invalid order with full logging ===\n")
prod_service.place_order("ORD-002", -50.00)
```

---

### Example 2: Payment & Discount System

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class CartItem:
    name:  str
    price: float
    qty:   int

    @property
    def total(self) -> float:
        return self.price * self.qty


# ─────────────────────────────────────────
# Discount Interface
# ─────────────────────────────────────────
class Discount(ABC):
    @abstractmethod
    def apply(self, amount: float) -> float:
        pass

    @abstractmethod
    def description(self) -> str:
        pass

    @abstractmethod
    def is_null(self) -> bool:
        pass


# ─────────────────────────────────────────
# Real Discounts
# ─────────────────────────────────────────
class PercentageDiscount(Discount):
    def __init__(self, percent: float, label: str = ""):
        self._pct   = percent
        self._label = label or f"{percent:.0f}% off"

    def apply(self, amount: float) -> float:
        saving = amount * (self._pct / 100)
        print(f"  🏷️  {self._label}: -${saving:.2f}")
        return amount - saving

    def description(self) -> str:
        return self._label

    def is_null(self) -> bool:
        return False


class FixedDiscount(Discount):
    def __init__(self, value: float, label: str = ""):
        self._value = value
        self._label = label or f"${value:.2f} off"

    def apply(self, amount: float) -> float:
        saving = min(self._value, amount)   # can't discount more than total
        print(f"  🏷️  {self._label}: -${saving:.2f}")
        return amount - saving

    def description(self) -> str:
        return self._label

    def is_null(self) -> bool:
        return False


class TieredDiscount(Discount):
    """Applies different % based on cart value."""

    def __init__(self):
        self._tiers = [
            (500, 15),    # ≥ $500 → 15% off
            (200, 10),    # ≥ $200 → 10% off
            (100,  5),    # ≥ $100 → 5% off
        ]

    def apply(self, amount: float) -> float:
        for threshold, pct in self._tiers:
            if amount >= threshold:
                saving = amount * (pct / 100)
                print(f"  🏷️  Tiered discount ({pct}% for ≥${threshold}): "
                      f"-${saving:.2f}")
                return amount - saving
        return amount

    def description(self) -> str:
        return "Tiered volume discount"

    def is_null(self) -> bool:
        return False


# ─────────────────────────────────────────
# Null Discount
# ─────────────────────────────────────────
class NullDiscount(Discount):
    """No discount. Returns amount unchanged. Never raises."""

    def apply(self, amount: float) -> float:
        return amount   # pass-through

    def description(self) -> str:
        return "No discount"

    def is_null(self) -> bool:
        return True


# ─────────────────────────────────────────
# Notification Interface
# ─────────────────────────────────────────
class Notifier(ABC):
    @abstractmethod
    def send(self, recipient: str, subject: str, body: str) -> None:
        pass

    @abstractmethod
    def is_null(self) -> bool:
        pass


class EmailNotifier(Notifier):
    def send(self, recipient: str, subject: str, body: str) -> None:
        print(f"  📧 Email → {recipient}: [{subject}] {body[:50]}...")

    def is_null(self) -> bool:
        return False


class NullNotifier(Notifier):
    def send(self, recipient: str, subject: str, body: str) -> None:
        pass   # silent — no notification sent

    def is_null(self) -> bool:
        return True


# ─────────────────────────────────────────
# Checkout — uses all null objects as defaults
# ─────────────────────────────────────────
class Checkout:
    def __init__(self,
                 discount: Discount  = NullDiscount(),
                 notifier: Notifier  = NullNotifier()):
        self._discount = discount
        self._notifier = notifier

    def process(self, items: list[CartItem], customer_email: str) -> float:
        subtotal = sum(item.total for item in items)
        print(f"\n  🛒 Subtotal: ${subtotal:.2f}")
        print(f"  🏷️  Discount: {self._discount.description()}")

        # No None check needed — NullDiscount just passes through
        final = self._discount.apply(subtotal)
        print(f"  💳 Final: ${final:.2f}")

        # No None check needed — NullNotifier silently swallows
        self._notifier.send(
            customer_email,
            "Order Confirmed",
            f"Your order total is ${final:.2f}. Thank you!"
        )
        return final


# ─────────────────────────────────────────
# Client
# ─────────────────────────────────────────
items = [
    CartItem("Python Book",    49.99, 2),
    CartItem("Keyboard",       89.00, 1),
    CartItem("USB Hub",        29.99, 1),
]

print("=== No discount, no notification (all nulls) ===")
Checkout().process(items, "alice@example.com")

print("\n=== 10% off + email notification ===")
Checkout(
    discount=PercentageDiscount(10, "Member discount"),
    notifier=EmailNotifier()
).process(items, "alice@example.com")

print("\n=== Fixed $20 coupon, no notification ===")
Checkout(
    discount=FixedDiscount(20.00, "SAVE20 coupon"),
).process(items, "bob@example.com")

print("\n=== Tiered discount + email ===")
Checkout(
    discount=TieredDiscount(),
    notifier=EmailNotifier()
).process(items, "carol@example.com")
```

---

### Example 3: User Permission System

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum

class Permission(Enum):
    READ    = "read"
    WRITE   = "write"
    DELETE  = "delete"
    ADMIN   = "admin"
    EXPORT  = "export"


# ─────────────────────────────────────────
# User Interface
# ─────────────────────────────────────────
class User(ABC):
    @abstractmethod
    def get_id(self) -> str | None:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def has_permission(self, permission: Permission) -> bool:
        pass

    @abstractmethod
    def get_permissions(self) -> set[Permission]:
        pass

    @abstractmethod
    def is_authenticated(self) -> bool:
        pass

    @abstractmethod
    def is_null(self) -> bool:
        pass


# ─────────────────────────────────────────
# Real Users
# ─────────────────────────────────────────
@dataclass
class AuthenticatedUser(User):
    _id:          str
    _name:        str
    _permissions: set[Permission] = field(default_factory=set)

    def get_id(self) -> str:
        return self._id

    def get_name(self) -> str:
        return self._name

    def has_permission(self, permission: Permission) -> bool:
        return permission in self._permissions or Permission.ADMIN in self._permissions

    def get_permissions(self) -> set[Permission]:
        return self._permissions.copy()

    def is_authenticated(self) -> bool:
        return True

    def is_null(self) -> bool:
        return False

    def grant(self, *permissions: Permission) -> 'AuthenticatedUser':
        self._permissions.update(permissions)
        return self


# ─────────────────────────────────────────
# Null User — the Guest / Anonymous user
# ─────────────────────────────────────────
class GuestUser(User):
    """
    Represents an unauthenticated visitor.
    Has no permissions, no ID, safe to call all methods on.
    """

    def get_id(self) -> None:
        return None

    def get_name(self) -> str:
        return "Guest"

    def has_permission(self, permission: Permission) -> bool:
        return False   # guests have no permissions

    def get_permissions(self) -> set[Permission]:
        return set()   # empty — neutral value

    def is_authenticated(self) -> bool:
        return False

    def is_null(self) -> bool:
        return True


# ─────────────────────────────────────────
# User Repository — returns GuestUser, never None
# ─────────────────────────────────────────
class UserRepository:
    def __init__(self):
        self._users = {
            "alice": AuthenticatedUser("u1", "Alice").grant(
                Permission.READ, Permission.WRITE, Permission.EXPORT
            ),
            "bob": AuthenticatedUser("u2", "Bob").grant(
                Permission.READ
            ),
            "admin": AuthenticatedUser("u3", "Admin").grant(
                Permission.ADMIN    # admin implies all
            ),
        }

    def find(self, username: str) -> User:
        return self._users.get(username.lower(), GuestUser())
        # Never returns None — returns GuestUser for unknown usernames


# ─────────────────────────────────────────
# Resource Controller — zero None/auth checks
# ─────────────────────────────────────────
class DocumentController:
    def __init__(self, repo: UserRepository):
        self._repo = repo

    def _check(self, user: User, perm: Permission, action: str) -> bool:
        if not user.is_authenticated():
            print(f"  🔒 [{user.get_name()}] Not authenticated — {action} denied")
            return False
        if not user.has_permission(perm):
            print(f"  🚫 [{user.get_name()}] Missing {perm.value} permission — "
                  f"{action} denied")
            return False
        return True

    def read(self, username: str, doc_id: str) -> None:
        user = self._repo.find(username)    # always a valid User
        if self._check(user, Permission.READ, "read"):
            print(f"  📄 [{user.get_name()}] Reading document {doc_id}")

    def write(self, username: str, doc_id: str, content: str) -> None:
        user = self._repo.find(username)
        if self._check(user, Permission.WRITE, "write"):
            print(f"  ✏️  [{user.get_name()}] Writing to {doc_id}: '{content[:30]}'")

    def delete(self, username: str, doc_id: str) -> None:
        user = self._repo.find(username)
        if self._check(user, Permission.DELETE, "delete"):
            print(f"  🗑️  [{user.get_name()}] Deleted {doc_id}")

    def export(self, username: str, doc_id: str) -> None:
        user = self._repo.find(username)
        if self._check(user, Permission.EXPORT, "export"):
            print(f"  📤 [{user.get_name()}] Exported {doc_id}")

    def admin_reset(self, username: str) -> None:
        user = self._repo.find(username)
        if self._check(user, Permission.ADMIN, "admin reset"):
            print(f"  🔧 [{user.get_name()}] System reset performed")


# ─────────────────────────────────────────
# Client
# ─────────────────────────────────────────
repo       = UserRepository()
controller = DocumentController(repo)

print("=== Alice (read + write + export) ===")
controller.read("alice",   "DOC-001")
controller.write("alice",  "DOC-001", "Updated content here")
controller.delete("alice", "DOC-001")    # no delete permission
controller.export("alice", "DOC-001")

print("\n=== Bob (read only) ===")
controller.read("bob",   "DOC-002")
controller.write("bob",  "DOC-002", "Trying to edit...")   # denied

print("\n=== Admin ===")
controller.admin_reset("admin")
controller.write("admin", "DOC-003", "Admin edit")   # ADMIN implies all

print("\n=== Unknown user (GuestUser — no None crashes) ===")
controller.read("unknown_user", "DOC-001")    # GuestUser — safely denied
controller.write("hacker",      "DOC-001", "inject!")   # safely denied
```

---

## ⚠️ Common Pitfalls

### ❌ Pitfall 1: Null Object Silently Hiding Real Bugs

```python
# ❌ DANGEROUS — silence masks a genuine error
class NullPaymentGateway(PaymentGateway):
    def charge(self, amount: float) -> Receipt:
        return Receipt(success=True, amount=0)   # fake success!

# The order "succeeds" but no money is charged — silent data corruption!

# ✅ CORRECT — null objects should never fake success for critical ops
class NullPaymentGateway(PaymentGateway):
    def charge(self, amount: float) -> Receipt:
        raise RuntimeError(
            "No payment gateway configured — cannot charge."
        )
# Payment is not optional. Null object is wrong here — use proper validation.
```

### ❌ Pitfall 2: Returning Null Object Where `None` is Semantically Correct

```python
# ❌ WRONG — confuses "not found" with "null object"
class ProductRepo:
    def find(self, id: int) -> Product:
        return self._db.get(id) or NullProduct()
        # Now callers can't distinguish "not found" from "found a real product"!

# ✅ CORRECT — for lookups, Optional[Product] is clearer
from typing import Optional

class ProductRepo:
    def find(self, id: int) -> Optional[Product]:
        return self._db.get(id)    # None means "not found" — that IS the answer

# Use Null Object for optional BEHAVIORS (logger, notifier),
# not for optional DATA (search results, lookups).
```

### ❌ Pitfall 3: Null Object Returning Wrong Neutral Values

```python
# ❌ WRONG — returning None from a null object defeats the purpose
class BadNullLogger(Logger):
    def get_entries(self) -> None:
        return None   # caller still has to check!

# ✅ CORRECT — always return a safe neutral value matching the return type
class GoodNullLogger(Logger):
    def get_entries(self) -> list[str]:
        return []     # empty list — safe to iterate, len(), etc.

    def get_entry_count(self) -> int:
        return 0      # safe for math

    def get_last_entry(self) -> str:
        return ""     # safe for string ops
```

### ❌ Pitfall 4: Creating Null Objects for Every Class

```python
# ❌ OVERKILL — null objects for classes that are never optional
class NullOrderItem(OrderItem): ...      # OrderItem is never optional!
class NullProductCategory(Category): ... # Category always exists!
class NullDatabase(Database): ...        # If DB is absent, we WANT an error!

# ✅ CORRECT — only create null objects for genuinely optional collaborators
# Good candidates: Logger, Notifier, Cache, Discount, Analytics, FeatureFlag
# Bad candidates: Database, Repository, Core domain objects
```

---

## ✅ Best Practices

### 1. Use `NullObject` as the Default Parameter Value

```python
# ✅ Null object as default — callers never need to pass None
class OrderService:
    def __init__(self,
                 logger:   Logger   = NullLogger(),
                 notifier: Notifier = NullNotifier(),
                 cache:    Cache    = NullCache()):
        self._logger   = logger
        self._notifier = notifier
        self._cache    = cache
```

### 2. Add `is_null()` for Rare Explicit Checks

```python
# ✅ Provide is_null() when callers genuinely need to distinguish
class NullLogger(Logger):
    def is_null(self) -> bool: return True

class ConsoleLogger(Logger):
    def is_null(self) -> bool: return False

# Use sparingly — if you're calling is_null() everywhere, reconsider
if logger.is_null():
    print("Warning: logging is disabled in this environment")
```

### 3. Make Null Objects Singletons

```python
# ✅ Null objects hold no state — one instance is enough
class NullLogger(Logger):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

# Or use a module-level constant:
NULL_LOGGER   = NullLogger()
NULL_NOTIFIER = NullNotifier()
NULL_CACHE    = NullCache()
```

### 4. Document Neutral Return Values Clearly

```python
class NullCache(Cache):
    def get(self, key: str) -> None:
        return None    # ← document: "cache miss" neutral value

    def get_many(self, keys: list[str]) -> dict:
        return {}      # ← document: "no cached entries"

    def get_ttl(self, key: str) -> int:
        return 0       # ← document: "no TTL — treat as expired"
```

---

## 📊 Summary

| Aspect          | Detail                                                           |
|-----------------|------------------------------------------------------------------|
| **Type**        | Behavioral                                                       |
| **Intent**      | Replace `None` checks with a do-nothing object                   |
| **Key Benefit** | Eliminates `if obj is not None` guards throughout codebase       |
| **Best For**    | Optional collaborators: loggers, notifiers, caches, discounts    |
| **Avoid For**   | Core domain objects, lookups where absence is meaningful         |
| **Python Tip**  | Use as default parameter value — `logger: Logger = NullLogger()` |

---

## ✅ Null Object Pattern Checklist

- Does the Null Object implement the full interface?
- Does every method return a safe neutral value ([], 0, "", False)?
- Is the Null Object used as the default parameter, not None?
- Is the Null Object stateless (singleton candidate)?
- Is is_null() provided for rare cases that genuinely need to distinguish?
- Are critical operations (payments, DB writes) excluded from Null Object treatment?
- Is Optional[T] used instead where "not found" is semantically meaningful?

---

## 💡 Key Takeaways

1. **Eliminates None checks** — client code becomes cleaner and crash-free
2. **Makes absence explicit** — a GuestUser or NullLogger is a conscious design decision
3. **Perfect for optional collaborators** — logger, notifier, cache, analytics, feature flags
4. **Neutral return values matter** — `[]` not `None`, `0` not `None`, `""` not `None`
5. **Not a silver bullet** — don't use it where `None` or an exception is the correct signal
