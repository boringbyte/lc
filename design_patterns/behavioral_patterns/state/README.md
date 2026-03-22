# 🧠 **State Pattern**

---

## 📋 Table of Contents
- [What is State Pattern?](#-what-is-state-pattern)
  - [Key Characteristics](#-key-characteristics)
  - [The Problem It Solves](#-the-problem-it-solves)
  - [Real-World Analogy](#-real-world-analogy)
  - [Visual Representation](#-visual-representation)
- [When to Use](#-when-to-use)
- [When NOT to Use](#-when-not-to-use)
- [Basic Implementation](#-basic-implementation)
- [Real-World Examples](#-real-world-examples)
  - [Example 1: Vending Machine](#example-1-vending-machine)
  - [Example 2: Order Lifecycle](#example-2-order-lifecycle)
  - [Example 3: TCP Connection](#example-3-tcp-connection)
- [Common Pitfalls](#-common-pitfalls)
- [Best Practices](#-best-practices)
- [Summary](#-summary)
- [State Pattern Checklist](#-state-pattern-checklist)
- [Key Takeaways](#-key-takeaways)

---

## 🔷 What is State Pattern?

**State Pattern** is a behavioral design pattern that lets an object **alter its behavior when its internal state changes**. The object appears to change its class. Instead of giant `if/elif` chains that check state flags, each state becomes its own class with its own behavior.

---

### 🔑 Key Characteristics

| Characteristic              | Description                                        |
|-----------------------------|----------------------------------------------------|
| **State as Object**         | Each state is a fully encapsulated class           |
| **Context Delegation**      | Context delegates behavior to current state object |
| **Clean Transitions**       | States manage their own transitions                |
| **Open/Closed**             | Add new states without modifying existing ones     |
| **Eliminates Conditionals** | No more `if state == "X": ... elif state == "Y":`  |

---

### 🔥 The Problem It Solves

Without State Pattern, state-dependent behavior becomes an unmaintainable mess:

```python
# ❌ WITHOUT State Pattern — conditional explosion
class TrafficLight:
    def __init__(self):
        self._state = "red"

    def next(self):
        if self._state == "red":
            self._state = "green"
            print("Now GREEN — go!")
        elif self._state == "green":
            self._state = "yellow"
            print("Now YELLOW — slow down!")
        elif self._state == "yellow":
            self._state = "red"
            print("Now RED — stop!")
        # Adding a new state (e.g. flashing amber) = modify ALL methods!

    def get_duration(self):
        if self._state == "red":    return 60
        elif self._state == "green": return 45
        elif self._state == "yellow": return 5
        # Every method has the same if/elif chain repeated!
```

With State Pattern:

```python
# ✅ WITH State Pattern — each state owns its behavior
class RedState:
    def next(self, light): light.set_state(GreenState())
    def duration(self):    return 60
    def describe(self):    print("RED — stop!")

# Each state is self-contained — adding FlashingAmberState touches nothing else
```

---

### 🌍 Real-World Analogy

Think of a **vending machine**:

```
[No Money]  ──insert coin──►  [Has Money]  ──select item──►  [Dispensing]
    ▲                              │                               │
    └───────────────────────────────────────────────────── item dispensed
```

- In **No Money** state: pressing buttons does nothing
- In **Has Money** state: can select items or get refund
- In **Dispensing** state: cannot insert coins or select items
- **Same machine, completely different behavior** depending on state

---

### 🖼️ Visual Representation

```
┌─────────────────────────────────────────────────┐
│                   Context                       │
│   _state: State ──► delegates all calls to it   │
│   set_state(new_state)                          │
│   request() ────────────────────────────────┐   │
└─────────────────────────────────────────────┼───┘
                                              │
              ┌───────────────────────────────┤
              │          State (interface)    │
              │          handle(context)      │
              └──────────┬────────────────────┘
                         │ implements
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
  │  StateA     │ │  StateB     │ │  StateC     │
  │  handle()   │ │  handle()   │ │  handle()   │
  │  → go to B  │ │  → go to C  │ │  → go to A  │
  └─────────────┘ └─────────────┘ └─────────────┘
```

---

### 🔀 Participants

| Role              | Responsibility                                                      |
|-------------------|---------------------------------------------------------------------|
| **Context**       | Holds reference to current state; exposes interface to clients      |
| **State**         | Interface/abstract class declaring state-specific behavior          |
| **ConcreteState** | Implements behavior for one specific state; may trigger transitions |

---

## ✅ When to Use

| Scenario                                                        | Why It Fits                         |
|-----------------------------------------------------------------|-------------------------------------|
| Object behavior **depends heavily on its state**                | Each state owns its logic           |
| **Large conditionals** checking state flags in multiple methods | Replace with state classes          |
| **State transitions** have complex rules                        | States manage their own transitions |
| Adding **new states** should not modify existing code           | Open/Closed principle               |
| State-specific behavior needs to be **tested independently**    | Each state is isolated              |

---

## ❌ When NOT to Use

- When there are only **2-3 simple states** with minimal behavior — plain `if/else` is cleaner
- When **states are trivial flags** (enabled/disabled) — a boolean suffices
- When transitions are **extremely rare** — the abstraction overhead isn't worth it

---

## 🏗️ Basic Implementation

### Classic Structure

```python
from __future__ import annotations
from abc import ABC, abstractmethod

# ─────────────────────────────────────────
# State Interface
# ─────────────────────────────────────────
class State(ABC):
    @abstractmethod
    def handle(self, context: 'Context') -> None:
        pass

    @abstractmethod
    def describe(self) -> str:
        pass


# ─────────────────────────────────────────
# Context
# ─────────────────────────────────────────
class Context:
    def __init__(self, initial_state: State):
        self._state = initial_state
        print(f"  🔧 Initial state: {self._state.describe()}")

    def set_state(self, state: State) -> None:
        print(f"  🔀 Transition: {self._state.describe()} → {state.describe()}")
        self._state = state

    def request(self) -> None:
        self._state.handle(self)   # delegate to current state

    @property
    def state(self) -> State:
        return self._state


# ─────────────────────────────────────────
# Concrete States
# ─────────────────────────────────────────
class StateA(State):
    def handle(self, context: Context) -> None:
        print("  ⚙️  StateA: handling request → transitioning to B")
        context.set_state(StateB())

    def describe(self) -> str:
        return "State A"


class StateB(State):
    def handle(self, context: Context) -> None:
        print("  ⚙️  StateB: handling request → transitioning to C")
        context.set_state(StateC())

    def describe(self) -> str:
        return "State B"


class StateC(State):
    def handle(self, context: Context) -> None:
        print("  ⚙️  StateC: handling request → cycling back to A")
        context.set_state(StateA())

    def describe(self) -> str:
        return "State C"


# ─────────────────────────────────────────
# Client
# ─────────────────────────────────────────
ctx = Context(StateA())

for _ in range(6):
    ctx.request()

# Initial state: State A
# ⚙️  StateA → transitioning to B
# 🔀 Transition: State A → State B
# ⚙️  StateB → transitioning to C
# 🔀 Transition: State B → State C
# ⚙️  StateC → cycling back to A
# 🔀 Transition: State C → State A  ... repeats
```

---

## 🌍 Real-World Examples

### Example 1: Vending Machine

```python
from __future__ import annotations
from abc import ABC, abstractmethod

# ─────────────────────────────────────────
# State Interface
# ─────────────────────────────────────────
class VendingState(ABC):

    @abstractmethod
    def insert_coin(self, machine: 'VendingMachine', amount: float) -> None:
        pass

    @abstractmethod
    def select_item(self, machine: 'VendingMachine', item_code: str) -> None:
        pass

    @abstractmethod
    def dispense(self, machine: 'VendingMachine') -> None:
        pass

    @abstractmethod
    def refund(self, machine: 'VendingMachine') -> None:
        pass

    def describe(self) -> str:
        return self.__class__.__name__.replace("State", "")


# ─────────────────────────────────────────
# Concrete States
# ─────────────────────────────────────────
class IdleState(VendingState):
    """No money inserted. Machine waiting."""

    def insert_coin(self, machine: 'VendingMachine', amount: float) -> None:
        machine.add_balance(amount)
        print(f"  💰 Coin inserted: ${amount:.2f} | Balance: ${machine.balance:.2f}")
        machine.set_state(HasMoneyState())

    def select_item(self, machine: 'VendingMachine', item_code: str) -> None:
        print("  ❌ Please insert coins first.")

    def dispense(self, machine: 'VendingMachine') -> None:
        print("  ❌ No item selected and no money inserted.")

    def refund(self, machine: 'VendingMachine') -> None:
        print("  ❌ No money to refund.")


class HasMoneyState(VendingState):
    """Money inserted. Waiting for item selection."""

    def insert_coin(self, machine: 'VendingMachine', amount: float) -> None:
        machine.add_balance(amount)
        print(f"  💰 Added: ${amount:.2f} | Balance: ${machine.balance:.2f}")

    def select_item(self, machine: 'VendingMachine', item_code: str) -> None:
        item = machine.get_item(item_code)
        if not item:
            print(f"  ❌ Item '{item_code}' not found.")
            return
        if machine.balance < item["price"]:
            shortage = item["price"] - machine.balance
            print(f"  ❌ Insufficient funds. Need ${shortage:.2f} more for '{item['name']}'.")
            return
        if item["stock"] == 0:
            print(f"  ❌ '{item['name']}' is out of stock.")
            return

        machine.set_selected(item_code)
        print(f"  ✅ Selected: '{item['name']}' (${item['price']:.2f})")
        machine.set_state(ItemSelectedState())

    def dispense(self, machine: 'VendingMachine') -> None:
        print("  ❌ Please select an item first.")

    def refund(self, machine: 'VendingMachine') -> None:
        amount = machine.balance
        machine.clear_balance()
        print(f"  💵 Refunded: ${amount:.2f}")
        machine.set_state(IdleState())


class ItemSelectedState(VendingState):
    """Item selected. Ready to dispense."""

    def insert_coin(self, machine: 'VendingMachine', amount: float) -> None:
        print("  ⚠️  Item already selected. Dispensing shortly...")

    def select_item(self, machine: 'VendingMachine', item_code: str) -> None:
        print("  ⚠️  Item already selected. Cancel first to choose another.")

    def dispense(self, machine: 'VendingMachine') -> None:
        item_code = machine.selected_item
        item      = machine.get_item(item_code)

        change = machine.balance - item["price"]
        machine.deduct_balance(item["price"])
        machine.reduce_stock(item_code)

        print(f"  🎁 Dispensing: '{item['name']}'")
        if change > 0:
            print(f"  💵 Change returned: ${change:.2f}")

        machine.clear_selection()
        machine.clear_balance()

        if machine.is_empty():
            print("  ⚠️  Machine is now EMPTY.")
            machine.set_state(OutOfStockState())
        else:
            machine.set_state(IdleState())

    def refund(self, machine: 'VendingMachine') -> None:
        amount = machine.balance
        machine.clear_balance()
        machine.clear_selection()
        print(f"  💵 Cancelled. Refunded: ${amount:.2f}")
        machine.set_state(IdleState())


class OutOfStockState(VendingState):
    """All items sold out."""

    def insert_coin(self, machine: 'VendingMachine', amount: float) -> None:
        print("  ❌ Machine is out of stock. Cannot accept payment.")

    def select_item(self, machine: 'VendingMachine', item_code: str) -> None:
        print("  ❌ Machine is out of stock.")

    def dispense(self, machine: 'VendingMachine') -> None:
        print("  ❌ Machine is out of stock.")

    def refund(self, machine: 'VendingMachine') -> None:
        print("  ❌ No money inserted.")


# ─────────────────────────────────────────
# Context: Vending Machine
# ─────────────────────────────────────────
class VendingMachine:
    def __init__(self):
        self._state:    VendingState       = IdleState()
        self._balance:  float              = 0.0
        self._selected: str | None      = None
        self._inventory = {
            "A1": {"name": "Cola",   "price": 1.50, "stock": 2},
            "A2": {"name": "Chips",  "price": 1.00, "stock": 1},
            "B1": {"name": "Water",  "price": 0.75, "stock": 3},
        }

    # ── State delegation ──────────────────
    def insert_coin(self, amount: float) -> None:
        self._state.insert_coin(self, amount)

    def select_item(self, code: str) -> None:
        self._state.select_item(self, code)

    def dispense(self) -> None:
        self._state.dispense(self)

    def refund(self) -> None:
        self._state.refund(self)

    # ── Internal helpers ──────────────────
    def set_state(self, state: VendingState) -> None:
        print(f"  🔀 [{self._state.describe()} → {state.describe()}]")
        self._state = state

    def add_balance(self, amount: float) -> None:
        self._balance += amount

    def deduct_balance(self, amount: float) -> None:
        self._balance -= amount

    def clear_balance(self) -> None:
        self._balance = 0.0

    def set_selected(self, code: str) -> None:
        self._selected = code

    def clear_selection(self) -> None:
        self._selected = None

    def reduce_stock(self, code: str) -> None:
        self._inventory[code]["stock"] -= 1

    def get_item(self, code: str) -> dict | None:
        return self._inventory.get(code)

    def is_empty(self) -> bool:
        return all(i["stock"] == 0 for i in self._inventory.values())

    @property
    def balance(self) -> float:
        return self._balance

    @property
    def selected_item(self) -> str | None:
        return self._selected

    def show_inventory(self) -> None:
        print("\n  📦 Inventory:")
        for code, item in self._inventory.items():
            print(f"     [{code}] {item['name']:8s} ${item['price']:.2f}"
                  f"  stock: {item['stock']}")
        print(f"  💳 Balance: ${self._balance:.2f}"
              f"  |  State: {self._state.describe()}\n")


# ─────────────────────────────────────────
# Client
# ─────────────────────────────────────────
machine = VendingMachine()
machine.show_inventory()

print("=== Normal Purchase ===")
machine.insert_coin(1.00)
machine.insert_coin(0.50)
machine.select_item("A1")    # Cola $1.50
machine.dispense()
machine.show_inventory()

print("=== Insufficient Funds ===")
machine.insert_coin(0.50)
machine.select_item("A1")    # Need $1.50, only have $0.50
machine.refund()

print("=== Buy Last Chips ===")
machine.insert_coin(1.00)
machine.select_item("A2")    # Chips $1.00
machine.dispense()

print("=== Try Inserting into Empty Machine ===")
machine.insert_coin(2.00)    # blocked — out of stock after all items gone
```

---

### Example 2: Order Lifecycle

```python
from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime

# ─────────────────────────────────────────
# State Interface
# ─────────────────────────────────────────
class OrderState(ABC):

    @abstractmethod
    def confirm(self, order: 'Order') -> None:
        pass

    @abstractmethod
    def pay(self, order: 'Order', amount: float) -> None:
        pass

    @abstractmethod
    def ship(self, order: 'Order', tracking: str) -> None:
        pass

    @abstractmethod
    def deliver(self, order: 'Order') -> None:
        pass

    @abstractmethod
    def cancel(self, order: 'Order', reason: str) -> None:
        pass

    @abstractmethod
    def refund(self, order: 'Order') -> None:
        pass

    def name(self) -> str:
        return self.__class__.__name__.replace("State", "").upper()

    def _reject(self, action: str, state: str) -> None:
        print(f"  ❌ Cannot '{action}' — order is in '{state}' state.")


# ─────────────────────────────────────────
# Concrete States
# ─────────────────────────────────────────
class PendingState(OrderState):
    """Order created, awaiting confirmation."""

    def confirm(self, order: 'Order') -> None:
        print(f"  ✅ Order #{order.id} confirmed.")
        order.add_event("Order confirmed")
        order.set_state(ConfirmedState())

    def pay(self, order, amount):
        self._reject("pay", self.name())

    def ship(self, order, tracking):
        self._reject("ship", self.name())

    def deliver(self, order):
        self._reject("deliver", self.name())

    def cancel(self, order: 'Order', reason: str) -> None:
        print(f"  🚫 Order #{order.id} cancelled: {reason}")
        order.add_event(f"Cancelled: {reason}")
        order.set_state(CancelledState())

    def refund(self, order):
        self._reject("refund", self.name())


class ConfirmedState(OrderState):
    """Confirmed, awaiting payment."""

    def confirm(self, order):
        self._reject("confirm again", self.name())

    def pay(self, order: 'Order', amount: float) -> None:
        if amount < order.total:
            shortage = order.total - amount
            print(f"  ❌ Payment of ${amount:.2f} insufficient. "
                  f"Need ${shortage:.2f} more.")
            return
        order.record_payment(amount)
        change = amount - order.total
        if change > 0:
            print(f"  💵 Change: ${change:.2f}")
        print(f"  💳 Payment of ${order.total:.2f} received for order #{order.id}.")
        order.add_event(f"Payment received: ${amount:.2f}")
        order.set_state(PaidState())

    def ship(self, order, tracking):
        self._reject("ship", self.name())

    def deliver(self, order):
        self._reject("deliver", self.name())

    def cancel(self, order: 'Order', reason: str) -> None:
        print(f"  🚫 Order #{order.id} cancelled before payment: {reason}")
        order.add_event(f"Cancelled: {reason}")
        order.set_state(CancelledState())

    def refund(self, order):
        self._reject("refund", self.name())


class PaidState(OrderState):
    """Paid, ready to ship."""

    def confirm(self, order):
        self._reject("confirm", self.name())

    def pay(self, order, amount):
        self._reject("pay again", self.name())

    def ship(self, order: 'Order', tracking: str) -> None:
        order.tracking_number = tracking
        print(f"  📦 Order #{order.id} shipped. Tracking: {tracking}")
        order.add_event(f"Shipped: tracking={tracking}")
        order.set_state(ShippedState())

    def deliver(self, order):
        self._reject("deliver", self.name())

    def cancel(self, order: 'Order', reason: str) -> None:
        print(f"  🚫 Order #{order.id} cancelled after payment — auto-refunding.")
        order.add_event(f"Cancelled with refund: {reason}")
        order.set_state(RefundedState())

    def refund(self, order):
        self._reject("refund directly", self.name())


class ShippedState(OrderState):
    """In transit."""

    def confirm(self, order):    self._reject("confirm", self.name())
    def pay(self, order, amt):   self._reject("pay", self.name())

    def ship(self, order, tracking):
        self._reject("ship again", self.name())

    def deliver(self, order: 'Order') -> None:
        print(f"  🏠 Order #{order.id} delivered successfully!")
        order.add_event("Delivered")
        order.set_state(DeliveredState())

    def cancel(self, order: 'Order', reason: str) -> None:
        print(f"  ⚠️  Order #{order.id} is in transit — initiating return.")
        order.add_event(f"Return initiated: {reason}")
        order.set_state(ReturnedState())

    def refund(self, order):
        self._reject("refund", self.name())


class DeliveredState(OrderState):
    """Successfully delivered."""

    def confirm(self, order):    self._reject("confirm", self.name())
    def pay(self, order, amt):   self._reject("pay", self.name())
    def ship(self, order, trk):  self._reject("ship", self.name())
    def deliver(self, order):    self._reject("deliver again", self.name())

    def cancel(self, order: 'Order', reason: str) -> None:
        print(f"  📮 Order #{order.id} — return requested post-delivery.")
        order.add_event(f"Return requested: {reason}")
        order.set_state(ReturnedState())

    def refund(self, order: 'Order') -> None:
        print(f"  💵 Goodwill refund issued for order #{order.id}.")
        order.add_event("Goodwill refund issued")
        order.set_state(RefundedState())


class CancelledState(OrderState):
    """Order cancelled — terminal state."""

    def confirm(self, order):    self._reject("confirm", self.name())
    def pay(self, order, amt):   self._reject("pay", self.name())
    def ship(self, order, trk):  self._reject("ship", self.name())
    def deliver(self, order):    self._reject("deliver", self.name())
    def cancel(self, order, r):  print("  ℹ️  Already cancelled.")
    def refund(self, order):     self._reject("refund cancelled order", self.name())


class RefundedState(OrderState):
    """Refund issued — terminal state."""

    def confirm(self, order):    self._reject("confirm", self.name())
    def pay(self, order, amt):   self._reject("pay", self.name())
    def ship(self, order, trk):  self._reject("ship", self.name())
    def deliver(self, order):    self._reject("deliver", self.name())
    def cancel(self, order, r):  self._reject("cancel", self.name())
    def refund(self, order):     print("  ℹ️  Already refunded.")


class ReturnedState(OrderState):
    """Item returned by customer."""

    def confirm(self, order):    self._reject("confirm", self.name())
    def pay(self, order, amt):   self._reject("pay", self.name())
    def ship(self, order, trk):  self._reject("ship", self.name())
    def deliver(self, order):    self._reject("deliver", self.name())
    def cancel(self, order, r):  self._reject("cancel", self.name())

    def refund(self, order: 'Order') -> None:
        print(f"  💵 Refund processed for returned order #{order.id}.")
        order.add_event("Refund processed after return")
        order.set_state(RefundedState())


# ─────────────────────────────────────────
# Context: Order
# ─────────────────────────────────────────
@dataclass
class OrderItem:
    name:  str
    price: float
    qty:   int

class Order:
    def __init__(self, order_id: str, items: list[OrderItem]):
        self.id              = order_id
        self.items           = items
        self._state: OrderState = PendingState()
        self._events: list[str] = [f"Order created: {order_id}"]
        self._payment        = 0.0
        self.tracking_number: str | None = None

    @property
    def total(self) -> float:
        return sum(i.price * i.qty for i in self.items)

    def set_state(self, state: OrderState) -> None:
        print(f"  🔀 Status: {self._state.name()} → {state.name()}")
        self._state = state

    def add_event(self, event: str) -> None:
        ts = datetime.now().strftime("%H:%M:%S")
        self._events.append(f"[{ts}] {event}")

    def record_payment(self, amount: float) -> None:
        self._payment = amount

    # ── Public interface (delegates to state) ──
    def confirm(self)                  -> None: self._state.confirm(self)
    def pay(self, amount: float)       -> None: self._state.pay(self, amount)
    def ship(self, tracking: str)      -> None: self._state.ship(self, tracking)
    def deliver(self)                  -> None: self._state.deliver(self)
    def cancel(self, reason: str = "") -> None: self._state.cancel(self, reason)
    def refund(self)                   -> None: self._state.refund(self)

    def show(self) -> None:
        print(f"\n  📋 Order #{self.id}")
        print(f"     State  : {self._state.name()}")
        print(f"     Total  : ${self.total:.2f}")
        print(f"     Items  : {[(i.name, i.qty) for i in self.items]}")
        print(f"     History:")
        for e in self._events:
            print(f"       • {e}")


# ─────────────────────────────────────────
# Client
# ─────────────────────────────────────────
items = [
    OrderItem("Python Book", 39.99, 1),
    OrderItem("Mechanical Keyboard", 79.00, 1),
]

print("=== Happy Path ===")
order = Order("ORD-001", items)
order.confirm()
order.pay(120.00)
order.ship("TRACK-XYZ-9876")
order.deliver()
order.show()

print("\n=== Invalid Operations ===")
order.pay(50.00)     # already delivered
order.ship("NEW")   # already delivered

print("\n=== Cancellation After Payment ===")
order2 = Order("ORD-002", [OrderItem("Mouse", 29.99, 2)])
order2.confirm()
order2.pay(59.98)
order2.cancel("Customer changed mind")
order2.show()

print("\n=== Return & Refund ===")
order3 = Order("ORD-003", [OrderItem("Monitor", 299.99, 1)])
order3.confirm()
order3.pay(300.00)
order3.ship("TRACK-ABC-1234")
order3.deliver()
order3.cancel("Defective product")   # triggers return
order3.refund()
order3.show()
```

---

### Example 3: TCP Connection

```python
from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime

# ─────────────────────────────────────────
# State Interface
# ─────────────────────────────────────────
class TCPState(ABC):

    @abstractmethod
    def open(self, conn: 'TCPConnection') -> None:
        pass

    @abstractmethod
    def send(self, conn: 'TCPConnection', data: str) -> None:
        pass

    @abstractmethod
    def receive(self, conn: 'TCPConnection') -> str | None:
        pass

    @abstractmethod
    def close(self, conn: 'TCPConnection') -> None:
        pass

    def name(self) -> str:
        return self.__class__.__name__.replace("State", "").upper()


# ─────────────────────────────────────────
# Concrete TCP States
# ─────────────────────────────────────────
class ClosedState(TCPState):
    """Connection is closed. Initial / final state."""

    def open(self, conn: 'TCPConnection') -> None:
        print(f"  📡 [{conn.id}] SYN sent → initiating handshake")
        conn.log("SYN sent")
        conn.set_state(SynSentState())

    def send(self, conn, data):
        print(f"  ❌ [{conn.id}] Cannot send — connection is CLOSED.")

    def receive(self, conn) -> None:
        print(f"  ❌ [{conn.id}] Cannot receive — connection is CLOSED.")
        return None

    def close(self, conn):
        print(f"  ℹ️  [{conn.id}] Already closed.")


class SynSentState(TCPState):
    """SYN sent, waiting for SYN-ACK."""

    def open(self, conn):
        print(f"  ⚠️  [{conn.id}] Already connecting...")

    def send(self, conn, data):
        print(f"  ❌ [{conn.id}] Cannot send — handshake not complete.")

    def receive(self, conn) -> str | None:
        # Simulate receiving SYN-ACK
        print(f"  📡 [{conn.id}] SYN-ACK received → sending ACK")
        conn.log("SYN-ACK received, ACK sent")
        conn.set_state(EstablishedState())
        return None

    def close(self, conn: 'TCPConnection') -> None:
        print(f"  📡 [{conn.id}] Aborting handshake → RST sent")
        conn.log("Connection aborted")
        conn.set_state(ClosedState())


class EstablishedState(TCPState):
    """Connection established. Full duplex data transfer."""

    def open(self, conn):
        print(f"  ℹ️  [{conn.id}] Already established.")

    def send(self, conn: 'TCPConnection', data: str) -> None:
        conn.out_buffer.append(data)
        print(f"  📤 [{conn.id}] SENT ({len(data)} bytes): '{data[:40]}'")
        conn.log(f"Sent {len(data)} bytes")

    def receive(self, conn: 'TCPConnection') -> str | None:
        if conn.in_buffer:
            data = conn.in_buffer.pop(0)
            print(f"  📥 [{conn.id}] RECV ({len(data)} bytes): '{data[:40]}'")
            conn.log(f"Received {len(data)} bytes")
            return data
        print(f"  📥 [{conn.id}] No data available.")
        return None

    def close(self, conn: 'TCPConnection') -> None:
        print(f"  📡 [{conn.id}] FIN sent → initiating graceful shutdown")
        conn.log("FIN sent")
        conn.set_state(FinWaitState())


class FinWaitState(TCPState):
    """FIN sent, waiting for FIN-ACK."""

    def open(self, conn):
        print(f"  ❌ [{conn.id}] Cannot open — closing in progress.")

    def send(self, conn: 'TCPConnection', data: str) -> None:
        # Half-close: can still receive but not send new data
        print(f"  ❌ [{conn.id}] Cannot send — FIN already sent.")

    def receive(self, conn: 'TCPConnection') -> str | None:
        if conn.in_buffer:
            data = conn.in_buffer.pop(0)
            print(f"  📥 [{conn.id}] Late data received: '{data[:40]}'")
            return data
        # Simulate receiving FIN-ACK
        print(f"  📡 [{conn.id}] FIN-ACK received → connection fully closed")
        conn.log("FIN-ACK received, connection closed")
        conn.set_state(ClosedState())
        return None

    def close(self, conn):
        print(f"  ℹ️  [{conn.id}] Close already in progress.")


# ─────────────────────────────────────────
# Context: TCP Connection
# ─────────────────────────────────────────
class TCPConnection:
    def __init__(self, connection_id: str, remote: str):
        self.id         = connection_id
        self.remote     = remote
        self._state:    TCPState   = ClosedState()
        self.in_buffer: list[str]  = []
        self.out_buffer: list[str] = []
        self._log:      list[str]  = []

    def set_state(self, state: TCPState) -> None:
        print(f"  🔀 [{self.id}] TCP State: {self._state.name()} → {state.name()}")
        self._state = state

    def log(self, msg: str) -> None:
        ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        self._log.append(f"[{ts}] {msg}")

    def inject(self, data: str) -> None:
        """Simulate receiving data from remote."""
        self.in_buffer.append(data)

    # ── Public TCP interface ──────────────
    def open(self)              -> None:          self._state.open(self)
    def send(self, data: str)   -> None:          self._state.send(self, data)
    def receive(self)           -> str | None: return self._state.receive(self)
    def close(self)             -> None:          self._state.close(self)

    @property
    def state_name(self) -> str:
        return self._state.name()

    def show_log(self) -> None:
        print(f"\n  📋 Connection Log [{self.id}] → {self.remote}")
        for entry in self._log:
            print(f"     {entry}")
        print(f"     Final state: {self._state.name()}")


# ─────────────────────────────────────────
# Client
# ─────────────────────────────────────────
print("=== Normal TCP Lifecycle ===\n")
conn = TCPConnection("CONN-001", "api.example.com:443")

conn.send("data")       # blocked — closed
conn.open()             # SYN sent → SYN_SENT
conn.receive()          # SYN-ACK → ESTABLISHED
conn.send("GET / HTTP/1.1")
conn.send("Host: api.example.com")
conn.inject("HTTP/1.1 200 OK\r\nContent-Length: 42")
conn.receive()
conn.inject("{'status': 'ok', 'data': [1, 2, 3]}")
conn.receive()
conn.close()            # FIN → FIN_WAIT
conn.receive()          # FIN-ACK → CLOSED
conn.show_log()

print("\n=== Aborted Connection ===\n")
conn2 = TCPConnection("CONN-002", "unreachable.host:80")
conn2.open()
conn2.close()   # abort during SYN_SENT
conn2.send("should not work")
conn2.show_log()
```

---

## ⚠️ Common Pitfalls

### ❌ Pitfall 1: State Classes Knowing Too Much About Each Other

```python
# ❌ WRONG — StateA directly imports and instantiates StateB
from state_b import StateB    # tight coupling between states!

class StateA(State):
    def handle(self, context):
        context.set_state(StateB())   # StateA knows StateB exists

# This is sometimes unavoidable, but minimize it:
# ✅ BETTER — use a factory or let Context manage transitions
class StateA(State):
    def handle(self, context):
        context.transition_to_next()  # Context decides what 'next' means
```

### ❌ Pitfall 2: Storing State-Specific Data in the Context

```python
# ❌ WRONG — context accumulates state-specific fields
class Context:
    def __init__(self):
        self.retry_count  = 0      # only meaningful in RetryingState
        self.locked_until = None   # only meaningful in LockedState
        self.last_attempt = None   # only meaningful in AttemptingState
        # Context becomes bloated with fields no current state uses!

# ✅ CORRECT — state-specific data lives in the state object
class RetryingState(State):
    def __init__(self):
        self.retry_count = 0       # belongs here, not in context
```

### ❌ Pitfall 3: Not Handling All Actions in Every State

```python
# ❌ WRONG — missing method raises AttributeError
class IncompleteState(State):
    def handle(self, context):
        ...
    # forgot to implement undo() — crashes at runtime!

# ✅ CORRECT — base State provides default rejections
class State(ABC):
    def handle(self, ctx): raise NotImplementedError
    def undo(self, ctx):
        print(f"  ❌ Cannot 'undo' in {self.__class__.__name__}")
    def reset(self, ctx):
        print(f"  ❌ Cannot 'reset' in {self.__class__.__name__}")
```

### ❌ Pitfall 4: Transitioning State Inside a Guard Clause

```python
# ❌ WRONG — state transition before operation completes
class PaidState(State):
    def ship(self, context):
        context.set_state(ShippedState())   # transition first
        context.record_tracking(...)        # then operation — may fail!
        # If record_tracking() raises, state is wrong!

# ✅ CORRECT — complete operation first, then transition
class PaidState(State):
    def ship(self, context):
        context.record_tracking(...)        # operation first
        context.set_state(ShippedState())   # transition only on success
```

---

## ✅ Best Practices

### 1. Provide Default Behavior in Base State

```python
class OrderState(ABC):
    def name(self) -> str:
        return self.__class__.__name__.replace("State", "").upper()

    def _reject(self, action: str) -> None:
        """Reusable rejection message — avoids boilerplate in every state."""
        print(f"  ❌ Cannot '{action}' — order is '{self.name()}'.")

    # Concrete states only override what they support.
    # Everything else calls _reject() automatically.
    def confirm(self, order): self._reject("confirm")
    def pay(self, order, amt): self._reject("pay")
    def ship(self, order, trk): self._reject("ship")
```

### 2. Log All Transitions

```python
class Context:
    def set_state(self, state: State) -> None:
        print(f"  🔀 {self._state.name()} → {state.name()}")
        self._transitions.append({
            "from":      self._state.name(),
            "to":        state.name(),
            "timestamp": datetime.now(),
        })
        self._state = state
```

### 3. Use Singletons for Stateless States

```python
# ✅ If a state holds NO instance data, share one instance
class IdleState(State):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

# context.set_state(IdleState())  ← always the same object, no allocation
```

### 4. Guard Transitions Explicitly

```python
class ConfirmedState(State):
    def pay(self, order: Order, amount: float) -> None:
        # Guard: validate before transitioning
        if amount < order.total:
            print(f"  ❌ Insufficient payment ${amount:.2f}")
            return          # no transition — state unchanged
        # All guards passed → safe to transition
        order.record_payment(amount)
        order.set_state(PaidState())
```

---

## 📊 Summary

| Aspect             | Detail                                                                |
|--------------------|-----------------------------------------------------------------------|
| **Type**           | Behavioral                                                            |
| **Intent**         | Object changes behavior when internal state changes                   |
| **Eliminates**     | Massive `if/elif` chains checking state flags                         |
| **Key Roles**      | Context (delegates), State (interface), ConcreteState (owns behavior) |
| **Transitions**    | Managed by state objects themselves OR by context                     |
| **Real-world Use** | Order lifecycles, TCP, vending machines, game AI, UI workflows        |

---

## ✅ State Pattern Checklist


- Does each state fully implement (or explicitly reject) every action?
- Does the Context delegate ALL behavior to the current state?
- Is state-specific data stored in the state object, not the context?
- Are transitions guarded — operations complete before state changes?
- Are all state transitions logged for debugging?
- Is there a base State class providing default _reject() behavior?
- Are stateless states reused as singletons to avoid allocations?
- Can new states be added without modifying existing state classes?


---

## 💡 Key Takeaways

1. **Eliminates conditional explosion** — no more repeated `if state == "X"` across every method
2. **Each state owns its rules** — what is allowed, what transitions to, what is rejected
3. **Open/Closed in action** — add a new `ReturnedState` without touching any other state class
4. **Context is a thin shell** — it delegates everything; it never contains state logic itself
5. **Transition order matters** — always complete the operation before calling `set_state()`
6. **Differs from Strategy** — Strategy swaps *algorithms*; State swaps *entire behavior profiles* based on lifecycle position
