# 🧠 **Chain of Responsibility**


## 📋 Table of Contents
- [What is Chain of Responsibility?](#-what-is-chain-of-responsibility)
  - [Key Characteristics](#-key-characteristics)
  - [The Problem It Solves](#-the-problem-it-solves)
  - [Real - World Analogy](#-real-world-analogy)
  - [Visual Representation](#-visual-representation)
  - [Request Flow](#-request-flow)
- [When to Use](#-when-to-use)
- [When NOT to Use](#-when-not-to-use)
- [Basic Implementation](#-basic-implementation)
  - [Classic Structure](#classic-structure)
- [Real-World Examples](#-real-world-examples)
  - [Example 1: Support Ticket System](#example-1-support-ticket-system)
  - [Example 2: HTTP Middleware Pipeline](#example-2-http-middleware-pipeline)
  - [Example 3: Purchase Approval System](#example-3-purchase-approval-system)
- [Common Pitfalls](#-common-pitfalls)
- [Best Practices](#-best-practices)
- [Summary](#-summary)
- [Chain of Responsibility Checklist](#-chain-of-responsibility-checklist)
- [Key Takeaways](#-key-takeaways)

---

## 🔷 What is Chain of Responsibility?

**Chain of Responsibility** is a behavioral design pattern that lets you pass requests along a chain of handlers. Each handler decides either to process the request or pass it to the next handler in the chain.

### 🔑 Key Characteristics

| Characteristic            | Description                                                |
|---------------------------|------------------------------------------------------------|
| **Decoupling**            | Sender doesn't know which handler will process the request |
| **Dynamic Chain**         | Chain can be modified at runtime                           |
| **Single Responsibility** | Each handler does one thing                                |
| **Optional Handling**     | Request may go unhandled (or always handled)               |

---

### 🔥 The Problem It Solves

Imagine you have a request that needs to go through multiple validation/processing steps. Without this pattern:

```python
# ❌ WITHOUT Chain of Responsibility — tightly coupled mess

def handle_request(request):
    if request.level == "LOW":
        junior_dev_handle(request)
    elif request.level == "MEDIUM":
        senior_dev_handle(request)
    elif request.level == "HIGH":
        manager_handle(request)
    elif request.level == "CRITICAL":
        cto_handle(request)
    # Adding new levels = modifying this function forever!
```

This violates **Open/Closed Principle** — every new handler requires modifying existing code.

---

### 🌍 Real-World Analogy
Think of **customer support escalation**:

```
You call support → Bot → Junior Agent → Senior Agent → Manager → Director
```

* Each level tries to solve your problem
* If they can't → escalate to next level
* You (the sender) don't care who fixes it, just that it gets fixed

---

### 🖼️ Visual Representation
```
[Sender]
   |
   | request
   v
[Handler 1: Can handle? → Process ✓] --no/pass--> [Handler 2: Can handle? → Process ✓] --no/pass--> [Handler 3: Can handle? → Process ✓] --no/pass--> [Unhandled]
            | yes                                      | yes                                      | yes
            v                                          v                                          v
        [Handled!]                                 [Handled!]                                 [Handled!]

Note:
Each handler either processes the request (yes) or passes it to the next handler (no).
```

### 🔀 Request Flow

```
Request → H1 (can't handle) → H2 (can't handle) → H3 (handles it ✅)
```

Each handler has two choices: handle it, or pass it forward.

---

## ✅ When to Use

| Scenario                              | Why It Fits                            |
|---------------------------------------|----------------------------------------|
| Multiple objects may handle a request | Don't hardcode which one               |
| Handler set changes at runtime        | Chain is dynamic                       |
| Avoid coupling sender to receiver     | Sender just fires, chain does the rest |
| Ordered processing with fallback      | Middleware, logging, auth              |

---

## ❌ When NOT to Use

* When every request must be handled (add a catch-all handler instead)
* When the chain is very long and performance matters
* When the order of handling must be guaranteed and can't change

---

## 🏗️ Basic Implementation

### Classic Structure

```python
from __future__ import annotations
from abc import ABC, abstractmethod

# ─────────────────────────────────────────
# Abstract Handler
# ─────────────────────────────────────────
class Handler(ABC):
    """
    Base handler declares the interface for all handlers.
    Contains a reference to the next handler in chain.
    """

    def __init__(self):
        self._next_handler: Handler | None = None

    def set_next(self, handler: Handler) -> Handler:
        """
        Returns the handler so we can chain .set_next() calls:
        h1.set_next(h2).set_next(h3)
        """
        self._next_handler = handler
        return handler  # ← key: enables fluent chaining

    @abstractmethod
    def handle(self, request: int) -> str | None:
        """Each concrete handler implements its own logic."""
        pass

    def pass_to_next(self, request: int) -> str | None:
        """Helper to forward to next handler if it exists."""
        if self._next_handler:
            return self._next_handler.handle(request)
        return None  # End of chain — no one handled it


# ─────────────────────────────────────────
# Concrete Handlers
# ─────────────────────────────────────────
class SmallHandler(Handler):
    def handle(self, request: int) -> str | None:
        if request <= 10:
            return f"SmallHandler handled request: {request}"
        return self.pass_to_next(request)  # can't handle, pass forward


class MediumHandler(Handler):
    def handle(self, request: int) -> str | None:
        if request <= 50:
            return f"MediumHandler handled request: {request}"
        return self.pass_to_next(request)


class LargeHandler(Handler):
    def handle(self, request: int) -> str | None:
        if request <= 100:
            return f"LargeHandler handled request: {request}"
        return self.pass_to_next(request)


# ─────────────────────────────────────────
# Client Code
# ─────────────────────────────────────────
small = SmallHandler()
medium = MediumHandler()
large = LargeHandler()

# Build the chain: small → medium → large
small.set_next(medium).set_next(large)

# Test
for req in [5, 30, 75, 150]:
    result = small.handle(req)
    print(result or f"No handler for request: {req}")

# Output:
# SmallHandler handled request: 5
# MediumHandler handled request: 30
# LargeHandler handled request: 75
# No handler for request: 150
```

---

## 🌍 Real-World Examples

### Example 1: Support Ticket System

```python
from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum


class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class Ticket:
    id: int
    description: str
    priority: Priority


# ─────────────────────────────────────────
# Abstract Support Agent
# ─────────────────────────────────────────
class SupportAgent(ABC):
    def __init__(self, name: str):
        self.name = name
        self._next: SupportAgent | None = None

    def set_next(self, agent: 'SupportAgent') -> 'SupportAgent':
        self._next = agent
        return agent

    @abstractmethod
    def handle(self, ticket: Ticket) -> str:
        pass

    def escalate(self, ticket: Ticket) -> str:
        if self._next:
            print(f"  [{self.name}] Escalating ticket #{ticket.id}...")
            return self._next.handle(ticket)
        return f"  ❌ Ticket #{ticket.id} unresolved — no one can handle it!"


# ─────────────────────────────────────────
# Concrete Agents
# ─────────────────────────────────────────
class Bot(SupportAgent):
    def handle(self, ticket: Ticket) -> str:
        if ticket.priority == Priority.LOW:
            return f"  🤖 Bot auto-resolved ticket #{ticket.id}: '{ticket.description}'"
        return self.escalate(ticket)


class JuniorAgent(SupportAgent):
    def handle(self, ticket: Ticket) -> str:
        if ticket.priority == Priority.MEDIUM:
            return f"  👨‍💼 Junior handled ticket #{ticket.id}: '{ticket.description}'"
        return self.escalate(ticket)


class SeniorAgent(SupportAgent):
    def handle(self, ticket: Ticket) -> str:
        if ticket.priority == Priority.HIGH:
            return f"  👩‍💼 Senior handled ticket #{ticket.id}: '{ticket.description}'"
        return self.escalate(ticket)


class Manager(SupportAgent):
    def handle(self, ticket: Ticket) -> str:
        # Manager handles everything that reaches them
        return f"  🏢 Manager handled CRITICAL ticket #{ticket.id}: '{ticket.description}'"


# ─────────────────────────────────────────
# Build Chain & Run
# ─────────────────────────────────────────
bot = Bot("Bot")
junior = JuniorAgent("Junior")
senior = SeniorAgent("Senior")
manager = Manager("Manager")

bot.set_next(junior).set_next(senior).set_next(manager)

tickets = [
    Ticket(1, "Password reset request", Priority.LOW),
    Ticket(2, "Feature not working", Priority.MEDIUM),
    Ticket(3, "Data loss reported", Priority.HIGH),
    Ticket(4, "Production server is down", Priority.CRITICAL),
]

for ticket in tickets:
    print(f"\nTicket #{ticket.id} [{ticket.priority.name}]: {ticket.description}")
    result = bot.handle(ticket)
    print(result)

# Output:
# Ticket #1 [LOW]: Password reset request
#   🤖 Bot auto-resolved ticket #1: 'Password reset request'
#
# Ticket #2 [MEDIUM]: Feature not working
#   [Bot] Escalating ticket #2...
#   👨‍💼 Junior handled ticket #2: 'Feature not working'
#
# Ticket #3 [HIGH]: Data loss reported
#   [Bot] Escalating ticket #3...
#   [Junior] Escalating ticket #3...
#   👩‍💼 Senior handled ticket #3: 'Data loss reported'
#
# Ticket #4 [CRITICAL]: Production server is down
#   [Bot] Escalating ticket #4...
#   [Junior] Escalating ticket #4...
#   [Senior] Escalating ticket #4...
#   🏢 Manager handled CRITICAL ticket #4: 'Production server is down'
```

---

### Example 2: HTTP Middleware Pipeline

```python
from dataclasses import dataclass, field
from typing import Callable


@dataclass
class HttpRequest:
    path: str
    headers: dict[str, str] = field(default_factory=dict)
    user: str | None = None


@dataclass
class HttpResponse:
    status: int
    body: str


# ─────────────────────────────────────────
# Middleware Base
# ─────────────────────────────────────────
class Middleware:
    def __init__(self):
        self._next: Middleware | None = None

    def set_next(self, middleware: 'Middleware') -> 'Middleware':
        self._next = middleware
        return middleware

    def handle(self, request: HttpRequest) -> HttpResponse:
        raise NotImplementedError

    def pass_through(self, request: HttpRequest) -> HttpResponse:
        if self._next:
            return self._next.handle(request)
        # Default response at end of chain
        return HttpResponse(200, f"OK: {request.path}")


# ─────────────────────────────────────────
# Concrete Middlewares
# ─────────────────────────────────────────
class LoggingMiddleware(Middleware):
    """Logs every request — always passes to next."""

    def handle(self, request: HttpRequest) -> HttpResponse:
        print(f"  📋 LOG: {request.path} | Headers: {request.headers}")
        response = self.pass_through(request)  # ← always passes through
        print(f"  📋 LOG: Response {response.status}")
        return response


class AuthMiddleware(Middleware):
    """Blocks unauthorized requests."""

    def handle(self, request: HttpRequest) -> HttpResponse:
        token = request.headers.get("Authorization")
        if not token:
            print("  🔒 AUTH: No token — blocked!")
            return HttpResponse(401, "Unauthorized")  # ← short-circuits chain

        # Simulate token validation
        request.user = "john_doe"
        print(f"  🔒 AUTH: Validated — user: {request.user}")
        return self.pass_through(request)


class RateLimitMiddleware(Middleware):
    """Limits requests per user."""

    def __init__(self, limit: int = 3):
        super().__init__()
        self._counts: dict[str, int] = {}
        self._limit = limit

    def handle(self, request: HttpRequest) -> HttpResponse:
        user = request.user or "anonymous"
        self._counts[user] = self._counts.get(user, 0) + 1

        if self._counts[user] > self._limit:
            print(f"  ⚡ RATE LIMIT: {user} exceeded {self._limit} requests")
            return HttpResponse(429, "Too Many Requests")

        print(f"  ⚡ RATE LIMIT: {user} — {self._counts[user]}/{self._limit}")
        return self.pass_through(request)


# ─────────────────────────────────────────
# Build Pipeline & Test
# ─────────────────────────────────────────
logging_mw = LoggingMiddleware()
auth_mw = AuthMiddleware()
rate_limit_mw = RateLimitMiddleware(limit=2)

# Pipeline: Logging → Auth → Rate Limiting → Handler
logging_mw.set_next(auth_mw).set_next(rate_limit_mw)

requests = [
    HttpRequest("/api/data", {"Authorization": "Bearer token123"}),
    HttpRequest("/api/data", {"Authorization": "Bearer token123"}),
    HttpRequest("/api/data", {"Authorization": "Bearer token123"}),  # Hits limit
    HttpRequest("/api/secret"),  # No auth
]

for i, req in enumerate(requests, 1):
    print(f"\n--- Request {i}: {req.path} ---")
    response = logging_mw.handle(req)
    print(f"  → Final: {response.status} {response.body}")
```

---

### Example 3: Purchase Approval System

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class PurchaseRequest:
    item: str
    amount: float
    requester: str


class Approver(ABC):
    def __init__(self, name: str, limit: float):
        self.name = name
        self.limit = limit
        self._next: 'Approver | None' = None

    def set_next(self, approver: 'Approver') -> 'Approver':
        self._next = approver
        return approver

    @abstractmethod
    def approve(self, request: PurchaseRequest) -> str:
        pass


class TeamLead(Approver):
    def approve(self, request: PurchaseRequest) -> str:
        if request.amount <= self.limit:
            return f"✅ {self.name} approved ${request.amount:.2f} for '{request.item}'"
        if self._next:
            return self._next.approve(request)
        return f"❌ No approver found for ${request.amount:.2f}"


class Manager(Approver):
    def approve(self, request: PurchaseRequest) -> str:
        if request.amount <= self.limit:
            return f"✅ {self.name} approved ${request.amount:.2f} for '{request.item}'"
        if self._next:
            return self._next.approve(request)
        return f"❌ No approver found for ${request.amount:.2f}"


class Director(Approver):
    def approve(self, request: PurchaseRequest) -> str:
        if request.amount <= self.limit:
            return f"✅ {self.name} approved ${request.amount:.2f} for '{request.item}'"
        return f"🚫 ${request.amount:.2f} exceeds all approval limits!"


# Build chain: TeamLead($500) → Manager($5000) → Director($50000)
lead = TeamLead("Team Lead", 500)
manager = Manager("Manager", 5_000)
director = Director("Director", 50_000)

lead.set_next(manager).set_next(director)

purchases = [
    PurchaseRequest("Office Supplies", 150.00, "Alice"),
    PurchaseRequest("New Laptop", 1_200.00, "Bob"),
    PurchaseRequest("Server Hardware", 25_000.00, "Charlie"),
    PurchaseRequest("Data Center", 99_999.00, "Dave"),
]

for p in purchases:
    result = lead.approve(p)
    print(result)

# ✅ Team Lead approved $150.00 for 'Office Supplies'
# ✅ Manager approved $1200.00 for 'New Laptop'
# ✅ Director approved $25000.00 for 'Server Hardware'
# 🚫 $99999.00 exceeds all approval limits!
```

---

## ⚠️ Common Pitfalls

### ❌ Pitfall 1: Not Calling `pass_to_next`

```python
# ❌ WRONG — silently swallows the request
class BadHandler(Handler):
    def handle(self, request):
        if request > 10:
            pass  # Forgot to forward! Request dies here silently.


# ✅ CORRECT
class GoodHandler(Handler):
    def handle(self, request):
        if request > 10:
            return self.pass_to_next(request)  # Always explicitly forward
```

### ❌ Pitfall 2: Circular Chain

```python
# ❌ Infinite loop!
h1.set_next(h2)
h2.set_next(h1)  # h1 → h2 → h1 → h2 → ... 💥

# ✅ Always make chain linear and terminating
h1.set_next(h2).set_next(h3)  # One direction only
```

### ❌ Pitfall 3: Giant Single Handler

```python
# ❌ One handler doing everything — defeats the pattern
class GodHandler(Handler):
    def handle(self, request):
        if request.type == "A":
            ...
        elif request.type == "B":
            ...
        elif request.type == "C":
            ...  # 50 more conditions


# ✅ One responsibility per handler
class TypeAHandler(Handler): ...


class TypeBHandler(Handler): ...
```

### ❌ Pitfall 4: Mutable State in Handlers

```python
# ❌ Shared mutable state causes bugs in concurrent scenarios
class BadHandler(Handler):
    request_count = 0  # class-level shared state 💀

    def handle(self, request):
        BadHandler.request_count += 1  # race condition in threads!


# ✅ Keep handlers stateless (or use instance-level, thread-safe state)
```

---

## ✅ Best Practices

### 1. Use Fluent Interface for Chain Building

```python
# ✅ set_next() returns the handler — enables clean chaining
h1.set_next(h2).set_next(h3).set_next(h4)

# vs the verbose alternative
h1.set_next(h2)
h2.set_next(h3)
h3.set_next(h4)
```

### 2. Always Have a Default/Catch-All Handler

```python
class CatchAllHandler(Handler):
    """Ensures no request falls through silently."""

    def handle(self, request):
        print(f"⚠️  Unhandled request: {request}. Logging for review.")
        return "default_response"


# Always attach at the end of chain
h1.set_next(h2).set_next(h3).set_next(CatchAllHandler())
```

### 3. Consider Thread Safety

```python
import threading


class ThreadSafeHandler(Handler):
    def __init__(self):
        super().__init__()
        self._lock = threading.Lock()
        self._count = 0

    def handle(self, request):
        with self._lock:
            self._count += 1
        # process...
```

### 4. Log the Chain Path (for debugging)

```python
class Handler(ABC):
    def handle(self, request, path: list = None):
        path = path or []
        path.append(self.__class__.__name__)
        # ... useful for tracing which handlers were visited
```

---

## 📊 Summary

| Aspect              | Detail                                                              |
|---------------------|---------------------------------------------------------------------|
| **Type**            | Behavioral                                                          |
| **Intent**          | Pass requests along a chain until one handles it                    |
| **Participants**    | Handler (abstract), ConcreteHandlers, Client                        |
| **Key Method**      | `set_next()` + `handle()`                                           |
| **Real-world Use**  | Middleware, event systems, support escalation, validation pipelines |
| **Python built-in** | Logging module uses this! (`logger.parent` chain)                   |

---

## ✅ Chain of Responsibility Checklist

* Does each handler do ONE thing only?
* Does every handler either handle OR explicitly pass_to_next?
* Is the chain linear (no cycles)?
* Is there a catch-all at the end?
* Are handlers stateless (or safely stateful)?
* Does set_next() return the handler (fluent interface)?
* Can the chain be reconfigured without changing handler code?

---

## 💡 Key Takeaways

* Decouples sender from receivers — sender doesn't know who handles it
* Open/Closed Principle — add new handlers without modifying existing ones
* Dynamic chains — reconfigure at runtime
* Python's logging module is a classic real-world implementation of this exact pattern
* Middleware in web frameworks (Django, Flask) follows this pattern
