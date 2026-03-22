# 🧠 **Observer Pattern**

---

## 📋 Table of Contents
- [What is Observer Pattern?](#-what-is-observer-pattern)
  - [Key Characteristics](#-key-characteristics)
  - [The Problem It Solves](#-the-problem-it-solves)
  - [Real-World Analogy](#-real-world-analogy)
  - [Visual Representation](#-visual-representation)
- [When to Use](#-when-to-use)
- [When NOT to Use](#-when-not-to-use)
- [Basic Implementation](#-basic-implementation)
- [Real-World Examples](#-real-world-examples)
  - [Example 1: Stock Market Feed](#example-1-stock-market-feed)
  - [Example 2: Event System](#example-2-event-system)
  - [Example 3: Reactive Data Store](#example-3-reactive-data-store)
- [Common Pitfalls](#-common-pitfalls)
- [Best Practices](#-best-practices)
- [Summary](#-summary)
- [Observer Pattern Checklist](#-observer-pattern-checklist)
- [Key Takeaways](#-key-takeaways)

---

## 🔷 What is Observer Pattern?

**Observer Pattern** is a behavioral design pattern that defines a **one-to-many dependency** between objects. When one object (the **Subject**) changes state, all its dependents (**Observers**) are **automatically notified and updated** — without the subject knowing who or how many observers exist.

It is the backbone of **event-driven programming**, **reactive systems**, and **pub/sub architectures**.

---

### 🔑 Key Characteristics

| Characteristic     | Description                                                     |
|--------------------|-----------------------------------------------------------------|
| **One-to-Many**    | One subject notifies many observers                             |
| **Loose Coupling** | Subject knows only the Observer interface, not concrete classes |
| **Push or Pull**   | Subject can push data to observers, or observers can pull it    |
| **Dynamic**        | Observers can subscribe/unsubscribe at runtime                  |
| **Automatic**      | No polling needed — notifications are event-driven              |

---

### 🔥 The Problem It Solves

Without Observer, components must poll for changes or be tightly coupled:

```python
# ❌ WITHOUT Observer — tight coupling and polling
class OrderSystem:
    def place_order(self, order):
        self._save_to_db(order)

        # Must know about EVERY system that cares about orders
        EmailService().send_confirmation(order)     # coupled!
        InventorySystem().reserve_stock(order)      # coupled!
        AnalyticsDashboard().record_sale(order)     # coupled!
        SMSService().notify_customer(order)         # coupled!
        # Adding a new service = modifying OrderSystem every time!
```

With Observer:

```python
# ✅ WITH Observer — OrderSystem knows nothing about consumers
class OrderSystem:
    def place_order(self, order):
        self._save_to_db(order)
        self.notify_observers("order_placed", order)  # fire and forget
        # Any number of observers can react — OrderSystem never changes!
```

---

### 🌍 Real-World Analogy

Think of a **newspaper subscription**:

```
Publisher (Subject)
    │
    ├──► Subscriber A  (gets every edition)
    ├──► Subscriber B  (gets every edition)
    └──► Subscriber C  (gets every edition)
```

- The **publisher** prints the newspaper once
- Every **subscriber** automatically receives their copy
- Subscribers can **subscribe or cancel** any time
- The publisher never calls each subscriber by name — it just publishes

---

### 🖼️ Visual Representation

```
┌─────────────────────────────────────┐
│           Subject                   │
│  observers: [ObsA, ObsB, ObsC]      │
│                                     │
│  attach(observer)                   │
│  detach(observer)                   │
│  notify() ──────────────────────┐   │
└─────────────────────────────────┼───┘
                                  │ calls update() on each
              ┌───────────────────┼───────────────────┐
              ▼                   ▼                   ▼
     ┌────────────┐      ┌────────────┐      ┌────────────┐
     │ Observer A │      │ Observer B │      │ Observer C │
     │ update()   │      │ update()   │      │ update()   │
     └────────────┘      └────────────┘      └────────────┘
```

---

### 🔀 Participants

| Role                 | Responsibility                                     |
|----------------------|----------------------------------------------------|
| **Subject**          | Maintains observer list; notifies on state change  |
| **Observer**         | Interface with `update()` method                   |
| **ConcreteSubject**  | Holds actual state; triggers notifications         |
| **ConcreteObserver** | Reacts to notifications; queries subject if needed |

---

## ✅ When to Use

| Scenario                                                       | Why It Fits                    |
|----------------------------------------------------------------|--------------------------------|
| Changes in one object require **updating unknown others**      | Decoupled notification         |
| Need **event-driven** architecture                             | Core pattern for events        |
| Objects should be able to **notify without knowing receivers** | Loose coupling                 |
| Need **dynamic subscription** — listeners added at runtime     | attach/detach support          |
| Building **reactive UIs** (state → view sync)                  | Foundation of React, Vue, etc. |

---

## ❌ When NOT to Use

- When the **notification chain is unpredictable** — cascading updates can be hard to debug
- When **order of notification matters** and must be guaranteed — standard observer gives no order guarantee
- When **observers are very slow** and block the subject — use async/threaded notification instead
- When there are only **1-2 hardcoded listeners** — direct calls are simpler

---

## 🏗️ Basic Implementation

### Classic Structure

```python
from abc import ABC, abstractmethod
from typing import Any

# ─────────────────────────────────────────
# Observer Interface
# ─────────────────────────────────────────
class Observer(ABC):
    @abstractmethod
    def update(self, subject: 'Subject', event: str, data: Any) -> None:
        pass


# ─────────────────────────────────────────
# Subject Base Class
# ─────────────────────────────────────────
class Subject:
    def __init__(self):
        self._observers: list[Observer] = []

    def attach(self, observer: Observer) -> None:
        if observer not in self._observers:
            self._observers.append(observer)
            print(f"  ➕ {observer.__class__.__name__} subscribed")

    def detach(self, observer: Observer) -> None:
        if observer in self._observers:
            self._observers.remove(observer)
            print(f"  ➖ {observer.__class__.__name__} unsubscribed")

    def notify(self, event: str, data: Any = None) -> None:
        for observer in list(self._observers):   # copy — safe if observer detaches during notify
            observer.update(self, event, data)


# ─────────────────────────────────────────
# Concrete Subject
# ─────────────────────────────────────────
class WeatherStation(Subject):
    def __init__(self):
        super().__init__()
        self._temperature = 0.0
        self._humidity    = 0.0
        self._pressure    = 1013.0

    @property
    def temperature(self) -> float:
        return self._temperature

    @property
    def humidity(self) -> float:
        return self._humidity

    def set_measurements(self, temp: float, humidity: float, pressure: float) -> None:
        self._temperature = temp
        self._humidity    = humidity
        self._pressure    = pressure
        print(f"\n  🌡️  Weather updated: {temp}°C, {humidity}% humidity, {pressure}hPa")
        self.notify("measurements_updated", {
            "temperature": temp,
            "humidity":    humidity,
            "pressure":    pressure,
        })


# ─────────────────────────────────────────
# Concrete Observers
# ─────────────────────────────────────────
class CurrentConditionsDisplay(Observer):
    def update(self, subject: WeatherStation, event: str, data: Any) -> None:
        if event == "measurements_updated":
            print(f"  📺 Current: {data['temperature']}°C, {data['humidity']}% humidity")


class StatisticsDisplay(Observer):
    def __init__(self):
        self._temps: list[float] = []

    def update(self, subject: WeatherStation, event: str, data: Any) -> None:
        if event == "measurements_updated":
            self._temps.append(data["temperature"])
            avg = sum(self._temps) / len(self._temps)
            print(f"  📊 Stats: Avg={avg:.1f}°C | "
                  f"Min={min(self._temps)}°C | Max={max(self._temps)}°C")


class AlertSystem(Observer):
    def update(self, subject: WeatherStation, event: str, data: Any) -> None:
        if event == "measurements_updated":
            if data["temperature"] > 35:
                print(f"  🚨 HEAT ALERT: {data['temperature']}°C exceeds threshold!")
            if data["humidity"] > 90:
                print(f"  🚨 HUMIDITY ALERT: {data['humidity']}% is dangerously high!")


# ─────────────────────────────────────────
# Client
# ─────────────────────────────────────────
station  = WeatherStation()
display  = CurrentConditionsDisplay()
stats    = StatisticsDisplay()
alerts   = AlertSystem()

station.attach(display)
station.attach(stats)
station.attach(alerts)

station.set_measurements(22.0, 65.0, 1012.0)
station.set_measurements(28.5, 70.0, 1008.0)
station.set_measurements(38.0, 92.0, 1005.0)   # triggers alerts!

print("\n--- Unsubscribing display ---")
station.detach(display)
station.set_measurements(25.0, 60.0, 1010.0)   # display no longer notified
```

---

## 🌍 Real-World Examples

### Example 1: Stock Market Feed

```python
from abc import ABC, abstractmethod
from typing import Any, Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

class PriceDirection(Enum):
    UP   = "▲"
    DOWN = "▼"
    FLAT = "─"

@dataclass
class StockTick:
    symbol:    str
    price:     float
    volume:    int
    timestamp: datetime = field(default_factory=datetime.now)
    direction: PriceDirection = PriceDirection.FLAT

    def __repr__(self):
        return (f"{self.direction.value} {self.symbol}: "
                f"${self.price:.2f} (vol: {self.volume:,})")


# ─────────────────────────────────────────
# Observer Interface
# ─────────────────────────────────────────
class MarketObserver(ABC):
    @abstractmethod
    def on_tick(self, tick: StockTick) -> None:
        pass

    @abstractmethod
    def on_market_event(self, event: str, data: Any) -> None:
        pass


# ─────────────────────────────────────────
# Subject: Stock Market Feed
# ─────────────────────────────────────────
class StockMarketFeed:
    def __init__(self):
        # symbol → list of observers watching that symbol
        self._symbol_observers: dict[str, list[MarketObserver]] = {}
        # observers watching ALL symbols
        self._global_observers: list[MarketObserver] = []
        # last known prices
        self._prices: dict[str, float] = {}

    def subscribe(self, observer: MarketObserver,
                  symbol: str | None = None) -> None:
        if symbol:
            if symbol not in self._symbol_observers:
                self._symbol_observers[symbol] = []
            if observer not in self._symbol_observers[symbol]:
                self._symbol_observers[symbol].append(observer)
                print(f"  ➕ {observer.__class__.__name__} watching {symbol}")
        else:
            if observer not in self._global_observers:
                self._global_observers.append(observer)
                print(f"  ➕ {observer.__class__.__name__} watching ALL symbols")

    def unsubscribe(self, observer: MarketObserver,
                    symbol: str | None = None) -> None:
        if symbol:
            if symbol in self._symbol_observers:
                self._symbol_observers[symbol].discard(observer) \
                    if hasattr(self._symbol_observers[symbol], 'discard') \
                    else None
                try:
                    self._symbol_observers[symbol].remove(observer)
                except ValueError:
                    pass
        else:
            try:
                self._global_observers.remove(observer)
            except ValueError:
                pass

    def publish_tick(self, symbol: str, price: float, volume: int) -> None:
        prev_price = self._prices.get(symbol, price)
        direction  = (PriceDirection.UP   if price > prev_price else
                      PriceDirection.DOWN if price < prev_price else
                      PriceDirection.FLAT)

        tick = StockTick(symbol, price, volume, direction=direction)
        self._prices[symbol] = price

        print(f"\n  📈 Market: {tick}")

        # Notify symbol-specific observers
        for obs in list(self._symbol_observers.get(symbol, [])):
            obs.on_tick(tick)

        # Notify global observers
        for obs in list(self._global_observers):
            obs.on_tick(tick)

    def broadcast_event(self, event: str, data: Any = None) -> None:
        print(f"\n  📢 Market Event: {event}")
        all_obs = set(self._global_observers)
        for observers in self._symbol_observers.values():
            all_obs.update(observers)
        for obs in all_obs:
            obs.on_market_event(event, data)


# ─────────────────────────────────────────
# Concrete Observers
# ─────────────────────────────────────────
class Portfolio(MarketObserver):
    """Tracks a user's holdings and calculates real-time P&L."""

    def __init__(self, name: str):
        self.name     = name
        self._holdings: dict[str, int]   = {}   # symbol → shares
        self._costs:    dict[str, float] = {}   # symbol → avg cost
        self._prices:   dict[str, float] = {}   # symbol → current price

    def buy(self, symbol: str, shares: int, price: float) -> None:
        existing = self._holdings.get(symbol, 0)
        existing_cost = self._costs.get(symbol, price)
        total_shares  = existing + shares
        avg_cost      = (existing * existing_cost + shares * price) / total_shares
        self._holdings[symbol] = total_shares
        self._costs[symbol]    = avg_cost
        self._prices[symbol]   = price
        print(f"  💼 [{self.name}] Bought {shares} {symbol} @ ${price:.2f}")

    def on_tick(self, tick: StockTick) -> None:
        if tick.symbol in self._holdings:
            self._prices[tick.symbol] = tick.price
            self._print_pnl(tick.symbol)

    def on_market_event(self, event: str, data: Any) -> None:
        if event == "market_close":
            print(f"\n  💼 [{self.name}] End of day summary:")
            total_pnl = 0.0
            for symbol, shares in self._holdings.items():
                price    = self._prices.get(symbol, 0)
                cost     = self._costs.get(symbol, 0)
                pnl      = (price - cost) * shares
                total_pnl += pnl
                print(f"     {symbol}: {shares} shares | "
                      f"cost ${cost:.2f} | current ${price:.2f} | "
                      f"P&L ${pnl:+.2f}")
            print(f"     Total P&L: ${total_pnl:+.2f}")

    def _print_pnl(self, symbol: str) -> None:
        shares   = self._holdings[symbol]
        price    = self._prices[symbol]
        cost     = self._costs[symbol]
        pnl      = (price - cost) * shares
        print(f"  💼 [{self.name}] {symbol}: "
              f"{shares} shares | P&L ${pnl:+.2f}")


class PriceAlertObserver(MarketObserver):
    """Fires alerts when price crosses user-defined thresholds."""

    def __init__(self):
        # symbol → list of (threshold_type, price, callback)
        self._alerts: dict[str, list] = {}

    def add_alert(self, symbol: str, above: float | None = None,
                  below: float | None = None) -> None:
        if symbol not in self._alerts:
            self._alerts[symbol] = []
        if above:
            self._alerts[symbol].append(("above", above))
            print(f"  🔔 Alert set: {symbol} > ${above:.2f}")
        if below:
            self._alerts[symbol].append(("below", below))
            print(f"  🔔 Alert set: {symbol} < ${below:.2f}")

    def on_tick(self, tick: StockTick) -> None:
        for alert_type, threshold in self._alerts.get(tick.symbol, []):
            if alert_type == "above" and tick.price > threshold:
                print(f"  🚨 ALERT: {tick.symbol} ${tick.price:.2f} "
                      f"crossed ABOVE ${threshold:.2f}!")
            elif alert_type == "below" and tick.price < threshold:
                print(f"  🚨 ALERT: {tick.symbol} ${tick.price:.2f} "
                      f"crossed BELOW ${threshold:.2f}!")

    def on_market_event(self, event: str, data: Any) -> None:
        pass


class MarketLogger(MarketObserver):
    """Logs all ticks to an audit trail."""

    def __init__(self):
        self._log: list[str] = []

    def on_tick(self, tick: StockTick) -> None:
        entry = f"[{tick.timestamp.strftime('%H:%M:%S')}] {tick}"
        self._log.append(entry)

    def on_market_event(self, event: str, data: Any) -> None:
        entry = f"[{datetime.now().strftime('%H:%M:%S')}] EVENT: {event} | {data}"
        self._log.append(entry)
        print(f"  📋 Logged market event: {event}")

    def dump_log(self) -> None:
        print(f"\n  📋 Audit Log ({len(self._log)} entries):")
        for entry in self._log[-5:]:    # show last 5
            print(f"     {entry}")


# ─────────────────────────────────────────
# Client
# ─────────────────────────────────────────
feed   = StockMarketFeed()

alice  = Portfolio("Alice")
bob    = Portfolio("Bob")
alerts = PriceAlertObserver()
logger = MarketLogger()

# Alice watches AAPL and GOOGL
alice.buy("AAPL",  10, 175.00)
alice.buy("GOOGL",  5, 140.00)

# Bob only watches AAPL
bob.buy("AAPL", 20, 170.00)

# Set price alerts
alerts.add_alert("AAPL",  above=185.00, below=165.00)
alerts.add_alert("GOOGL", above=150.00)

# Subscribe
feed.subscribe(alice,  "AAPL")
feed.subscribe(alice,  "GOOGL")
feed.subscribe(bob,    "AAPL")
feed.subscribe(alerts, "AAPL")
feed.subscribe(alerts, "GOOGL")
feed.subscribe(logger)           # logger watches everything

# Simulate market data
feed.publish_tick("AAPL",  178.50, 1_200_000)
feed.publish_tick("GOOGL", 142.30,   800_000)
feed.publish_tick("AAPL",  186.00,   950_000)   # triggers alert!
feed.publish_tick("GOOGL", 152.10,   600_000)   # triggers alert!
feed.publish_tick("AAPL",  163.00, 2_100_000)   # triggers below alert!

feed.broadcast_event("market_close", {"date": "2025-01-15"})
logger.dump_log()
```

---

### Example 2: Event System

```python
from __future__ import annotations
from typing import Callable, Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
from functools import wraps
import threading

# ─────────────────────────────────────────
# Event Data
# ─────────────────────────────────────────
@dataclass
class Event:
    name:      str
    data:      Any              = None
    source:    Optional[str]    = None
    timestamp: datetime         = field(default_factory=datetime.now)
    cancelled: bool             = False

    def cancel(self) -> None:
        """Allows an observer to cancel the event (stop further propagation)."""
        self.cancelled = True

# Handler type: a callable that accepts an Event
EventHandler = Callable[[Event], None]


# ─────────────────────────────────────────
# Event Bus (Subject + Dispatcher)
# ─────────────────────────────────────────
class EventBus:
    """
    Central event dispatcher.
    Supports: wildcards, one-time handlers, priority, cancellation.
    """

    def __init__(self):
        # event_name → list of (priority, handler)
        self._handlers: Dict[str, List[tuple]] = {}
        self._lock = threading.Lock()

    def on(self, event_name: str, handler: EventHandler,
           priority: int = 0) -> EventHandler:
        """Subscribe handler to event. Higher priority runs first."""
        with self._lock:
            if event_name not in self._handlers:
                self._handlers[event_name] = []
            self._handlers[event_name].append((priority, handler))
            self._handlers[event_name].sort(key=lambda x: x[0], reverse=True)
        print(f"  ➕ '{handler.__name__}' subscribed to '{event_name}' "
              f"(priority={priority})")
        return handler   # return handler for use as decorator

    def once(self, event_name: str, handler: EventHandler) -> None:
        """Subscribe handler that fires only once then unsubscribes."""
        def one_time_wrapper(event: Event) -> None:
            handler(event)
            self.off(event_name, one_time_wrapper)
        one_time_wrapper.__name__ = f"{handler.__name__}[once]"
        self.on(event_name, one_time_wrapper)

    def off(self, event_name: str, handler: EventHandler) -> None:
        """Unsubscribe handler from event."""
        with self._lock:
            if event_name in self._handlers:
                self._handlers[event_name] = [
                    (p, h) for p, h in self._handlers[event_name]
                    if h is not handler
                ]

    def emit(self, event_name: str, data: Any = None,
             source: str = "") -> Event:
        """Fire event — notifies all subscribers in priority order."""
        event = Event(name=event_name, data=data, source=source)
        print(f"\n  📣 Event: '{event_name}' from '{source or 'unknown'}'")

        handlers = []
        with self._lock:
            # Exact match handlers
            handlers += self._handlers.get(event_name, [])
            # Wildcard handlers (subscribed to "*")
            handlers += self._handlers.get("*", [])

        # Sort combined list by priority
        handlers.sort(key=lambda x: x[0], reverse=True)

        for _, handler in handlers:
            if event.cancelled:
                print(f"  🚫 Event '{event_name}' was cancelled")
                break
            handler(event)

        return event

    def subscribe(self, event_name: str, priority: int = 0):
        """Decorator factory for subscribing methods."""
        def decorator(fn: EventHandler) -> EventHandler:
            self.on(event_name, fn, priority=priority)
            return fn
        return decorator


# ─────────────────────────────────────────
# Application Components (Observers)
# ─────────────────────────────────────────
class AuthService:
    def __init__(self, bus: EventBus):
        bus.on("user.login",   self.on_login,  priority=10)  # high priority
        bus.on("user.logout",  self.on_logout)
        bus.on("user.login_failed", self.on_failed, priority=10)

    def on_login(self, event: Event) -> None:
        user = event.data
        if not user.get("active", True):
            print(f"  🔒 Auth: Blocked inactive user '{user['name']}'")
            event.cancel()   # stop further processing
        else:
            print(f"  🔒 Auth: User '{user['name']}' authenticated")

    def on_logout(self, event: Event) -> None:
        print(f"  🔒 Auth: Session ended for '{event.data['name']}'")

    def on_failed(self, event: Event) -> None:
        attempts = event.data.get("attempts", 1)
        print(f"  🔒 Auth: Failed login attempt #{attempts} "
              f"for '{event.data['username']}'")
        if attempts >= 3:
            print(f"  🔒 Auth: Account '{event.data['username']}' LOCKED!")
            event.cancel()


class AuditLogger:
    def __init__(self, bus: EventBus):
        bus.on("*", self.log_all, priority=-10)  # lowest priority, catch-all
        self._log: List[str] = []

    def log_all(self, event: Event) -> None:
        entry = (f"[{event.timestamp.strftime('%H:%M:%S')}] "
                 f"{event.name} | source={event.source} | "
                 f"cancelled={event.cancelled}")
        self._log.append(entry)
        print(f"  📋 Audit: {entry}")


class NotificationService:
    def __init__(self, bus: EventBus):
        bus.on("user.login",         self.on_login)
        bus.on("order.placed",       self.on_order)
        bus.on("payment.completed",  self.on_payment)

    def on_login(self, event: Event) -> None:
        print(f"  📧 Email: Welcome back, {event.data['name']}!")

    def on_order(self, event: Event) -> None:
        order = event.data
        print(f"  📧 Email: Order #{order['id']} confirmed — "
              f"${order['total']:.2f}")

    def on_payment(self, event: Event) -> None:
        print(f"  📱 SMS: Payment of ${event.data['amount']:.2f} received!")


class AnalyticsService:
    def __init__(self, bus: EventBus):
        bus.on("user.login",    self.track)
        bus.on("order.placed",  self.track)
        self._events: List[str] = []

    def track(self, event: Event) -> None:
        self._events.append(event.name)
        print(f"  📊 Analytics: Tracked '{event.name}' "
              f"(total: {len(self._events)})")


# ─────────────────────────────────────────
# Client
# ─────────────────────────────────────────
bus = EventBus()

auth         = AuthService(bus)
logger       = AuditLogger(bus)
notifications = NotificationService(bus)
analytics    = AnalyticsService(bus)

# One-time welcome handler
bus.once("user.login", lambda e: print(
    f"  🎉 First-time greeting for {e.data['name']}!"
))

print("\n=== User Login ===")
bus.emit("user.login", {"name": "Alice", "active": True}, source="web")

print("\n=== Another Login (one-time handler gone) ===")
bus.emit("user.login", {"name": "Bob", "active": True}, source="mobile")

print("\n=== Blocked Inactive User ===")
bus.emit("user.login", {"name": "Charlie", "active": False}, source="web")

print("\n=== Failed Login Attempts ===")
for i in range(1, 4):
    bus.emit("user.login_failed",
             {"username": "hacker", "attempts": i}, source="web")

print("\n=== Order Placed ===")
bus.emit("order.placed", {"id": "ORD-001", "total": 149.99}, source="shop")
bus.emit("payment.completed", {"amount": 149.99}, source="payment")
```

---

### Example 3: Reactive Data Store

```python
from __future__ import annotations
from typing import Any, Callable
from copy import deepcopy
from dataclasses import dataclass

# ─────────────────────────────────────────
# Reactive Property
# ─────────────────────────────────────────
class ReactiveProperty:
    """
    A single reactive value.
    Any callable subscribed to it fires when the value changes.
    """

    def __init__(self, initial: Any = None, name: str = ""):
        self._value     = initial
        self._name      = name
        self._observers: list[Callable] = []

    @property
    def value(self) -> Any:
        return self._value

    @value.setter
    def value(self, new_val: Any) -> None:
        if new_val != self._value:
            old_val    = self._value
            self._value = new_val
            self._notify(old_val, new_val)

    def watch(self, fn: Callable) -> Callable:
        """Subscribe a callable; returns it for use as decorator."""
        self._observers.append(fn)
        return fn

    def unwatch(self, fn: Callable) -> None:
        try:
            self._observers.remove(fn)
        except ValueError:
            pass

    def _notify(self, old: Any, new: Any) -> None:
        for fn in list(self._observers):
            fn(new, old)

    def __repr__(self):
        return f"ReactiveProperty({self._name}={self._value!r})"


# ─────────────────────────────────────────
# Reactive Store (Vuex/Redux-style)
# ─────────────────────────────────────────
class Store:
    """
    Centralized reactive state store.
    Components watch specific keys; notified only when those keys change.
    """

    def __init__(self, initial_state: dict[str, Any]):
        self._state:    dict[str, ReactiveProperty] = {}
        self._watchers: dict[str, list[Callable]]   = {}   # key → watchers
        self._global:   list[Callable]              = []   # watch any change
        self._history:  list[dict]                  = []
        self._computing = False                            # prevents re-entrancy

        for key, value in initial_state.items():
            self._state[key] = ReactiveProperty(value, name=key)
            self._state[key].watch(
                lambda new, old, k=key: self._on_change(k, new, old)
            )

    def get(self, key: str) -> Any:
        if key not in self._state:
            raise KeyError(f"Unknown state key: '{key}'")
        return self._state[key].value

    def set(self, key: str, value: Any) -> None:
        if key not in self._state:
            self._state[key] = ReactiveProperty(value, name=key)
            self._state[key].watch(
                lambda new, old, k=key: self._on_change(k, new, old)
            )
            self._on_change(key, value, None)
        else:
            self._state[key].value = value   # triggers observers via property

    def update(self, **kwargs) -> None:
        """Batch update multiple keys."""
        for key, value in kwargs.items():
            self.set(key, value)

    def watch(self, key: str, fn: Callable) -> Callable:
        """Watch a specific key for changes."""
        if key not in self._watchers:
            self._watchers[key] = []
        self._watchers[key].append(fn)
        print(f"  👁️  Watching '{key}': {fn.__name__}")
        return fn

    def watch_all(self, fn: Callable) -> Callable:
        """Watch any state change."""
        self._global.append(fn)
        return fn

    def unwatch(self, key: str, fn: Callable) -> None:
        if key in self._watchers:
            try:
                self._watchers[key].remove(fn)
            except ValueError:
                pass

    def _on_change(self, key: str, new: Any, old: Any) -> None:
        if self._computing:
            return
        self._computing = True
        try:
            print(f"\n  🔄 State: '{key}' changed: {old!r} → {new!r}")
            self._history.append({"key": key, "old": old, "new": deepcopy(new)})

            # Key-specific watchers
            for fn in list(self._watchers.get(key, [])):
                fn(new, old)

            # Global watchers
            for fn in list(self._global):
                fn(key, new, old)
        finally:
            self._computing = False

    def snapshot(self) -> dict[str, Any]:
        return {k: deepcopy(v.value) for k, v in self._state.items()}

    def history(self, key: str | None = None) -> list[dict]:
        if key:
            return [h for h in self._history if h["key"] == key]
        return self._history


# ─────────────────────────────────────────
# UI Components (Observers via watch)
# ─────────────────────────────────────────
class UserProfileComponent:
    def __init__(self, store: Store):
        self._store = store
        store.watch("user",   self.on_user_changed)
        store.watch("theme",  self.on_theme_changed)

    def on_user_changed(self, new: dict, old: dict | None) -> None:
        print(f"  🖼️  ProfileComponent re-renders: {new['name']}, {new['email']}")

    def on_theme_changed(self, new: str, old: str) -> None:
        print(f"  🖼️  ProfileComponent applies theme: {new}")


class CartComponent:
    def __init__(self, store: Store):
        store.watch("cart", self.on_cart_changed)

    def on_cart_changed(self, new: list, old: list | None) -> None:
        total = sum(item["price"] * item["qty"] for item in new)
        print(f"  🛒 CartComponent: {len(new)} items | Total: ${total:.2f}")


class NotificationBadge:
    def __init__(self, store: Store):
        store.watch("notifications", self.on_notifications)

    def on_notifications(self, new: list, old: list | None) -> None:
        unread = sum(1 for n in new if not n.get("read"))
        print(f"  🔔 Badge: {unread} unread notification(s)")


class DevToolsLogger:
    def __init__(self, store: Store):
        store.watch_all(self.log_change)

    def log_change(self, key: str, new: Any, old: Any) -> None:
        print(f"  🔧 DevTools: [{key}] {old!r} → {new!r}")


# ─────────────────────────────────────────
# Client
# ─────────────────────────────────────────
store = Store({
    "user":          {"name": "Guest", "email": ""},
    "theme":         "light",
    "cart":          [],
    "notifications": [],
    "is_loading":    False,
})

# Mount components — they register their watchers
profile  = UserProfileComponent(store)
cart     = CartComponent(store)
badge    = NotificationBadge(store)
devtools = DevToolsLogger(store)

print("\n=== User logs in ===")
store.set("user", {"name": "Alice", "email": "alice@example.com"})

print("\n=== Change theme ===")
store.set("theme", "dark")

print("\n=== Add items to cart ===")
store.set("cart", [
    {"name": "Python Book", "price": 39.99, "qty": 1},
])
store.set("cart", [
    {"name": "Python Book",  "price": 39.99, "qty": 1},
    {"name": "Keyboard",     "price": 79.00, "qty": 1},
])

print("\n=== Notifications arrive ===")
store.set("notifications", [
    {"id": 1, "text": "Order shipped!",  "read": False},
    {"id": 2, "text": "Flash sale 20%!", "read": False},
])

print("\n=== Mark notification read ===")
notifs = deepcopy(store.get("notifications"))
notifs[0]["read"] = True
store.set("notifications", notifs)

print("\n=== State Snapshot ===")
snap = store.snapshot()
for k, v in snap.items():
    print(f"  {k}: {v}")

print(f"\n=== History for 'cart' ===")
for entry in store.history("cart"):
    print(f"  {entry['old']!r} → {entry['new']!r}")
```

---

## ⚠️ Common Pitfalls

### ❌ Pitfall 1: Memory Leaks — Observers Never Unsubscribed

```python
# ❌ WRONG — observer registered but never removed
class Screen:
    def __init__(self, subject):
        subject.attach(self)   # registered

    # Screen is destroyed but never detached!
    # Subject holds reference → Screen never garbage collected → leak!

# ✅ CORRECT — always provide a cleanup/unsubscribe path
class Screen:
    def __init__(self, subject):
        self._subject = subject
        subject.attach(self)

    def destroy(self) -> None:
        self._subject.detach(self)   # explicit cleanup
```

### ❌ Pitfall 2: Modifying Observer List During Notification

```python
# ❌ WRONG — observer detaches itself during notification loop
def notify(self):
    for obs in self._observers:     # iterating original list
        obs.update(self)            # observer may call detach() here
        # RuntimeError: list changed size during iteration!

# ✅ CORRECT — iterate over a copy of the list
def notify(self, event, data=None):
    for obs in list(self._observers):   # copy first
        obs.update(self, event, data)   # safe even if observer detaches
```

### ❌ Pitfall 3: Cascading / Infinite Update Loops

```python
# ❌ WRONG — A notifies B, B updates state, which notifies A → infinite loop
class A(Observer):
    def update(self, subject, event, data):
        self.value = data + 1
        self._subject_b.set_value(self.value)   # triggers B → triggers A again!

# ✅ CORRECT — use a guard flag to prevent re-entrancy
class Subject:
    def __init__(self):
        self._notifying = False

    def notify(self, event, data):
        if self._notifying:
            return              # break the loop
        self._notifying = True
        try:
            for obs in list(self._observers):
                obs.update(self, event, data)
        finally:
            self._notifying = False
```

### ❌ Pitfall 4: Slow Observers Blocking the Subject

```python
import time
# ❌ WRONG — slow observer blocks all subsequent observers
class SlowObserver(Observer):
    def update(self, subject, event, data):
        time.sleep(5)           # blocks subject for 5 seconds!
        send_email(data)        # all other observers wait

# ✅ CORRECT — dispatch slow work to a thread or queue
import threading

class AsyncObserver(Observer):
    def update(self, subject, event, data):
        threading.Thread(
            target=self._do_work,
            args=(data,),
            daemon=True
        ).start()

    def _do_work(self, data):
        time.sleep(5)           # runs in background
        send_email(data)
```

---

## ✅ Best Practices

### 1. Always Iterate Over a Copy When Notifying

```python
from typing import Any
def notify(self, event: str, data: Any = None) -> None:
    for observer in list(self._observers):   # list() makes a copy
        observer.update(self, event, data)
```

### 2. Use Weak References to Prevent Memory Leaks

```python
import weakref

class Subject:
    def __init__(self):
        self._observers: list[weakref.ref] = []

    def attach(self, observer: Observer) -> None:
        self._observers.append(weakref.ref(observer))

    def notify(self, event, data=None):
        alive = []
        for ref in self._observers:
            obs = ref()              # dereference
            if obs is not None:      # still alive?
                obs.update(self, event, data)
                alive.append(ref)
        self._observers = alive      # prune dead refs
```

### 3. Typed Events with Enum

```python
from enum import Enum, auto

class StockEvent(Enum):
    TICK          = auto()
    MARKET_OPEN   = auto()
    MARKET_CLOSE  = auto()
    CIRCUIT_BREAK = auto()

# Safe, autocomplete-friendly, no typos
subject.notify(StockEvent.TICK, data)
```

### 4. Support Filtered Subscriptions

```python
from typing import Any, Callable
# ✅ Let observers declare which events they care about
class EventBus:
    def on(self, event: str, handler: Callable) -> None:
        self._handlers.setdefault(event, []).append(handler)

    def emit(self, event: str, data: Any = None) -> None:
        for handler in self._handlers.get(event, []):
            handler(data)
        for handler in self._handlers.get("*", []):   # wildcards
            handler(data)
```

---

## 📊 Summary

| Aspect             | Detail                                                  |
|--------------------|---------------------------------------------------------|
| **Type**           | Behavioral                                              |
| **Intent**         | One object change automatically notifies all dependents |
| **Key Methods**    | `attach()`, `detach()`, `notify()`, `update()`          |
| **Python Native**  | Properties with `__set__`, `@property`, signals in PyQt |
| **Real-world Use** | Event systems, reactive UIs, pub/sub, data streams      |
| **Famous Uses**    | Django signals, React state, RxPY, PyQt signals/slots   |

---

## ✅ Observer Pattern Checklist


- Does the Subject iterate over a COPY of observers when notifying?
- Is there a clear detach/unsubscribe path to prevent memory leaks?
- Are events typed (Enum or dataclass) rather than raw strings?
- Are slow observers dispatched asynchronously?
- Is there a re-entrancy guard to prevent infinite notification loops?
- Can observers subscribe to specific events (filtered subscriptions)?
- Are weak references used when observers have shorter lifetimes than subjects?


---

## 💡 Key Takeaways

1. **One-to-many with zero coupling** — subject knows only the Observer interface, never concrete types
2. **Foundation of event-driven programming** — every GUI, reactive UI, and message broker is built on this
3. **Memory leaks are the #1 pitfall** — always provide and call `detach()`; consider weak references
4. **Iterate over a copy** when notifying — observers may detach themselves mid-loop
5. **Django signals, PyQt signals/slots, RxPY** are all production implementations of this pattern
6. **Differs from Mediator** — Observer is one-to-many broadcast; Mediator is many-to-many coordination through a hub
