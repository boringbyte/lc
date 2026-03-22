# 🧠 **Mediator Pattern**

---

## 📋 Table of Contents
- [What is Mediator Pattern?](#-what-is-mediator-pattern)
  - [Key Characteristics](#-key-characteristics)
  - [The Problem It Solves](#-the-problem-it-solves)
  - [Real-World Analogy](#-real-world-analogy)
  - [Visual Representation](#-visual-representation)
- [When to Use](#-when-to-use)
- [When NOT to Use](#-when-not-to-use)
- [Basic Implementation](#-basic-implementation)
- [Real-World Examples](#-real-world-examples)
  - [Example 1: Chat Room](#example-1-chat-room)
  - [Example 2: Air Traffic Control](#example-2-air-traffic-control)
  - [Example 3: UI Form Mediator](#example-3-ui-form-mediator)
- [Common Pitfalls](#-common-pitfalls)
- [Best Practices](#-best-practices)
- [Summary](#-summary)
- [Mediator Pattern Checklist](#-mediator-pattern-checklist)
- [Key Takeaways](#-key-takeaways)

---

## 🔷 What is Mediator Pattern?

**Mediator Pattern** is a behavioral design pattern that **reduces chaotic dependencies between objects** by forcing them to communicate only through a central mediator object. Instead of components talking directly to each other, they all talk **to** and **through** the mediator.

---

### 🔑 Key Characteristics

| Characteristic            | Description                                                     |
|---------------------------|-----------------------------------------------------------------|
| **Centralized Control**   | All communication flows through one object                      |
| **Loose Coupling**        | Components don't reference each other directly                  |
| **Single Responsibility** | Each component focuses on its own logic only                    |
| **Reusability**           | Components become reusable since they have no peer dependencies |
| **Maintainability**       | Adding/removing components doesn't affect others                |

---

### 🔥 The Problem It Solves

Without Mediator, components reference each other directly creating a tangled web:

```python
# ❌ WITHOUT Mediator — every component knows about every other component
class Button:
    def __init__(self, textbox, checkbox, listbox):
        self.textbox  = textbox    # coupled to TextBox
        self.checkbox = checkbox   # coupled to CheckBox
        self.listbox  = listbox    # coupled to ListBox

    def click(self):
        if self.checkbox.is_checked():
            self.textbox.enable()
            self.listbox.populate(self.textbox.get_value())
        # Button knows WAY too much about other components!
        # Change CheckBox → must update Button
        # Add a new component → must update ALL existing components

# With 5 components, you could have up to 5×4 = 20 direct connections!
```

With Mediator:

```python
# ✅ WITH Mediator — components only know the mediator
class Button:
    def __init__(self, mediator):
        self.mediator = mediator   # only dependency!

    def click(self):
        self.mediator.notify(self, "click")   # just fires an event
        # Button knows nothing about what happens next
```

---

### 🌍 Real-World Analogy

Think of an **Air Traffic Controller**:

```
Plane A  ──►  Tower (Mediator)  ◄──  Plane B
Plane C  ──►      │             ◄──  Plane D
                  │
         Coordinates all planes
```

- Planes **never** talk directly to each other
- Every communication goes through the **control tower**
- The tower has the full picture and coordinates everyone
- Adding a new plane just means registering with the tower — other planes are unaffected

---

### 🖼️ Visual Representation

**Without Mediator** — spaghetti connections:
```
A ──── B
│ ╲  ╱ │
│  ╲╱  │
│  ╱╲  │
│ ╱  ╲ │
C ──── D
# Every component talks to every other: O(n²) connections
```

**With Mediator** — star topology:
```
    A
    │
B ──M── D
    │
    C
# Every component talks only to M: O(n) connections
```

---

### 🔀 Participants

| Role                  | Responsibility                                          |
|-----------------------|---------------------------------------------------------|
| **Mediator**          | Interface defining `notify(sender, event)`              |
| **ConcreteMediator**  | Implements coordination logic between components        |
| **Component**         | Base class; holds a mediator reference                  |
| **ConcreteComponent** | Specific UI element or actor; fires events via mediator |

---

## ✅ When to Use

| Scenario                                                | Why It Fits                   |
|---------------------------------------------------------|-------------------------------|
| Components are **tightly coupled** to many others       | Replace O(n²) links with O(n) |
| **Reusing a component** is hard due to its dependencies | Decouple via mediator         |
| **Adding new behavior** requires modifying many classes | Add it in the mediator only   |
| You need a **single place** to observe all interactions | Mediator is the hub           |
| UI forms where **one element change affects others**    | Classic mediator use case     |

---

## ❌ When NOT to Use

- When you only have **2-3 components** — a mediator adds unnecessary indirection
- When the **mediator itself becomes a "God Object"** that knows too much — split it
- When components are **already loosely coupled** and interact rarely

---

## 🏗️ Basic Implementation

### Classic Structure

```python
from __future__ import annotations
from abc import ABC, abstractmethod

# ─────────────────────────────────────────
# Mediator Interface
# ─────────────────────────────────────────
class Mediator(ABC):
    @abstractmethod
    def notify(self, sender: 'Component', event: str) -> None:
        """Called by components to signal an event."""
        pass


# ─────────────────────────────────────────
# Base Component
# ─────────────────────────────────────────
class Component:
    def __init__(self, mediator: Mediator | None = None):
        self._mediator = mediator

    def set_mediator(self, mediator: Mediator) -> None:
        self._mediator = mediator

    def notify(self, event: str) -> None:
        if self._mediator:
            self._mediator.notify(self, event)


# ─────────────────────────────────────────
# Concrete Components
# ─────────────────────────────────────────
class Button(Component):
    def click(self) -> None:
        print("  🖱️  Button clicked")
        self.notify("click")


class TextBox(Component):
    def __init__(self):
        super().__init__()
        self.text    = ""
        self.enabled = True

    def set_text(self, text: str) -> None:
        self.text = text
        print(f"  ✏️  TextBox text set to: '{text}'")
        self.notify("text_changed")

    def enable(self) -> None:
        self.enabled = True
        print("  ✅ TextBox enabled")

    def disable(self) -> None:
        self.enabled = False
        print("  🚫 TextBox disabled")


class CheckBox(Component):
    def __init__(self):
        super().__init__()
        self.checked = False

    def toggle(self) -> None:
        self.checked = not self.checked
        state = "checked" if self.checked else "unchecked"
        print(f"  ☑️  CheckBox {state}")
        self.notify("toggled")


# ─────────────────────────────────────────
# Concrete Mediator
# ─────────────────────────────────────────
class FormMediator(Mediator):
    def __init__(self, button: Button, textbox: TextBox, checkbox: CheckBox):
        self._button   = button
        self._textbox  = textbox
        self._checkbox = checkbox

        # Register mediator with all components
        for c in [button, textbox, checkbox]:
            c.set_mediator(self)

    def notify(self, sender: Component, event: str) -> None:
        if sender is self._checkbox and event == "toggled":
            if self._checkbox.checked:
                self._textbox.enable()
            else:
                self._textbox.disable()

        elif sender is self._button and event == "click":
            print(f"  📤 Submitting form with: '{self._textbox.text}'")


# ─────────────────────────────────────────
# Client Code
# ─────────────────────────────────────────
button   = Button()
textbox  = TextBox()
checkbox = CheckBox()

mediator = FormMediator(button, textbox, checkbox)

checkbox.toggle()          # enables textbox
textbox.set_text("Hello")  # user types
button.click()             # submit

checkbox.toggle()          # disables textbox
button.click()             # submit with disabled textbox

# Output:
#   ☑️  CheckBox checked
#   ✅ TextBox enabled
#   ✏️  TextBox text set to: 'Hello'
#   🖱️  Button clicked
#   📤 Submitting form with: 'Hello'
#   ☑️  CheckBox unchecked
#   🚫 TextBox disabled
#   🖱️  Button clicked
#   📤 Submitting form with: 'Hello'
```

---

## 🌍 Real-World Examples

### Example 1: Chat Room

```python
from abc import ABC, abstractmethod
from datetime import datetime

# ─────────────────────────────────────────
# Mediator Interface
# ─────────────────────────────────────────
class ChatMediator(ABC):
    @abstractmethod
    def send_message(self, message: str, sender: 'User', room: str) -> None:
        pass

    @abstractmethod
    def join_room(self, user: 'User', room: str) -> None:
        pass

    @abstractmethod
    def leave_room(self, user: 'User', room: str) -> None:
        pass

    @abstractmethod
    def send_private(self, message: str, sender: 'User', recipient_name: str) -> None:
        pass


# ─────────────────────────────────────────
# Component: User
# ─────────────────────────────────────────
class User:
    def __init__(self, name: str, mediator: ChatMediator):
        self.name     = name
        self._mediator = mediator
        self._inbox:  list[str] = []

    def join(self, room: str) -> None:
        self._mediator.join_room(self, room)

    def leave(self, room: str) -> None:
        self._mediator.leave_room(self, room)

    def send(self, message: str, room: str) -> None:
        self._mediator.send_message(message, self, room)

    def whisper(self, message: str, to: str) -> None:
        self._mediator.send_private(message, self, to)

    def receive(self, message: str) -> None:
        self._inbox.append(message)
        print(f"  📨 [{self.name}] {message}")

    def __repr__(self):
        return f"User({self.name})"


# ─────────────────────────────────────────
# Concrete Mediator: Chat Server
# ─────────────────────────────────────────
class ChatServer(ChatMediator):
    def __init__(self):
        # room_name → list of users in that room
        self._rooms: dict[str, list[User]] = {}
        # username → user object
        self._users: dict[str, User] = {}
        self._log:   list[str]       = []

    def register(self, user: User) -> None:
        self._users[user.name] = user
        print(f"  🔌 {user.name} connected to server")

    def join_room(self, user: User, room: str) -> None:
        if room not in self._rooms:
            self._rooms[room] = []
            print(f"  🏠 Room '{room}' created")

        if user not in self._rooms[room]:
            self._rooms[room].append(user)
            self._broadcast_system(f"{user.name} joined '{room}'", room, exclude=user)
            print(f"  ✅ {user.name} joined '{room}'")

    def leave_room(self, user: User, room: str) -> None:
        if room in self._rooms and user in self._rooms[room]:
            self._rooms[room].remove(user)
            self._broadcast_system(f"{user.name} left '{room}'", room)
            print(f"  👋 {user.name} left '{room}'")

    def send_message(self, message: str, sender: User, room: str) -> None:
        if room not in self._rooms or sender not in self._rooms[room]:
            sender.receive(f"❌ You are not in room '{room}'")
            return

        timestamp = datetime.now().strftime("%H:%M")
        formatted = f"[{room}][{timestamp}] {sender.name}: {message}"
        self._log.append(formatted)

        # Deliver to everyone in the room except sender
        for user in self._rooms[room]:
            if user is not sender:
                user.receive(formatted)

        print(f"  📡 Broadcast in '{room}': {sender.name}: {message}")

    def send_private(self, message: str, sender: User, recipient_name: str) -> None:
        recipient = self._users.get(recipient_name)
        if not recipient:
            sender.receive(f"❌ User '{recipient_name}' not found")
            return

        timestamp = datetime.now().strftime("%H:%M")
        formatted = f"[DM][{timestamp}] {sender.name} → {recipient_name}: {message}"
        recipient.receive(formatted)
        print(f"  🔒 Private: {sender.name} → {recipient_name}: {message}")

    def _broadcast_system(self, message: str, room: str,
                          exclude: User | None = None) -> None:
        for user in self._rooms.get(room, []):
            if user is not exclude:
                user.receive(f"[System] {message}")

    def room_members(self, room: str) -> list[str]:
        return [u.name for u in self._rooms.get(room, [])]


# ─────────────────────────────────────────
# Client
# ─────────────────────────────────────────
server = ChatServer()

alice = User("Alice", server)
bob   = User("Bob",   server)
carol = User("Carol", server)

server.register(alice)
server.register(bob)
server.register(carol)

print("\n--- Joining rooms ---")
alice.join("general")
bob.join("general")
carol.join("general")
carol.join("python")

print("\n--- Chatting ---")
alice.send("Hey everyone!", "general")
bob.send("Hi Alice!", "general")
carol.send("Hello from Python room too!", "python")

print("\n--- Private message ---")
alice.whisper("Hey Bob, can we chat privately?", "Bob")

print("\n--- Leave ---")
bob.leave("general")
alice.send("Bob left...", "general")

print(f"\nRoom 'general' members: {server.room_members('general')}")
```

---

### Example 2: Air Traffic Control

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum

class FlightStatus(Enum):
    APPROACHING = "approaching"
    HOLDING     = "holding"
    LANDING     = "landing"
    LANDED      = "landed"
    DEPARTING   = "departing"
    AIRBORNE    = "airborne"

@dataclass
class Position:
    altitude_ft: int
    distance_nm: float   # nautical miles from runway

# ─────────────────────────────────────────
# Mediator Interface
# ─────────────────────────────────────────
class ATCMediator(ABC):
    @abstractmethod
    def request_landing(self, aircraft: 'Aircraft') -> bool:
        pass

    @abstractmethod
    def request_takeoff(self, aircraft: 'Aircraft') -> bool:
        pass

    @abstractmethod
    def report_emergency(self, aircraft: 'Aircraft', reason: str) -> None:
        pass

    @abstractmethod
    def update_position(self, aircraft: 'Aircraft', pos: Position) -> None:
        pass


# ─────────────────────────────────────────
# Component: Aircraft
# ─────────────────────────────────────────
class Aircraft:
    def __init__(self, callsign: str, atc: ATCMediator):
        self.callsign  = callsign
        self._atc      = atc
        self.status    = FlightStatus.APPROACHING
        self.position  = Position(altitude_ft=10000, distance_nm=50.0)

    def request_landing(self) -> None:
        print(f"\n  ✈️  {self.callsign}: Requesting landing clearance")
        cleared = self._atc.request_landing(self)
        if cleared:
            self.status = FlightStatus.LANDING
            print(f"  ✈️  {self.callsign}: Landing cleared — beginning descent")
        else:
            self.status = FlightStatus.HOLDING
            print(f"  ✈️  {self.callsign}: Holding pattern — awaiting clearance")

    def request_takeoff(self) -> None:
        print(f"\n  ✈️  {self.callsign}: Requesting takeoff clearance")
        cleared = self._atc.request_takeoff(self)
        if cleared:
            self.status = FlightStatus.AIRBORNE
            print(f"  ✈️  {self.callsign}: Takeoff cleared — wheels up!")
        else:
            print(f"  ✈️  {self.callsign}: Hold position on runway")

    def declare_emergency(self, reason: str) -> None:
        print(f"\n  🚨 {self.callsign}: MAYDAY MAYDAY — {reason}")
        self._atc.report_emergency(self, reason)

    def update_position(self, altitude: int, distance: float) -> None:
        self.position = Position(altitude, distance)
        self._atc.update_position(self, self.position)

    def receive_instruction(self, instruction: str) -> None:
        print(f"  📻 {self.callsign} received: '{instruction}'")

    def __repr__(self):
        return f"Aircraft({self.callsign}, {self.status.value})"


# ─────────────────────────────────────────
# Concrete Mediator: Control Tower
# ─────────────────────────────────────────
class ControlTower(ATCMediator):
    def __init__(self, airport: str):
        self.airport          = airport
        self._runway_clear    = True
        self._aircraft:       dict[str, Aircraft] = {}
        self._holding_queue:  list[Aircraft]      = []
        self._emergency_mode  = False

    def register(self, aircraft: Aircraft) -> None:
        self._aircraft[aircraft.callsign] = aircraft
        print(f"  🗼 Tower: {aircraft.callsign} registered with {self.airport} ATC")

    def request_landing(self, aircraft: Aircraft) -> bool:
        if self._emergency_mode:
            aircraft.receive_instruction("Go around — emergency in progress")
            return False

        if self._runway_clear:
            self._runway_clear = False
            self._broadcast(f"Runway occupied by {aircraft.callsign}", exclude=aircraft)
            return True
        else:
            self._holding_queue.append(aircraft)
            aircraft.receive_instruction(
                f"Join holding pattern — #{len(self._holding_queue)} in queue"
            )
            return False

    def request_takeoff(self, aircraft: Aircraft) -> bool:
        if self._emergency_mode or not self._runway_clear:
            aircraft.receive_instruction("Hold position — runway not available")
            return False

        self._runway_clear = False
        self._broadcast(f"Runway occupied by {aircraft.callsign}", exclude=aircraft)
        return True

    def report_emergency(self, aircraft: Aircraft, reason: str) -> None:
        self._emergency_mode = True
        self._runway_clear   = False

        # Notify ALL other aircraft
        self._broadcast(
            f"EMERGENCY: {aircraft.callsign} — {reason}. Clear airspace.",
            exclude=aircraft
        )
        print(f"  🗼 Tower: Declaring airport emergency. Diverting all traffic.")

        # Priority landing for emergency aircraft
        aircraft.receive_instruction(
            "Emergency services alerted. Cleared for immediate landing on all runways."
        )

    def update_position(self, aircraft: Aircraft, pos: Position) -> None:
        # Check for separation violations with other aircraft
        for callsign, other in self._aircraft.items():
            if other is aircraft:
                continue
            if (abs(other.position.altitude_ft - pos.altitude_ft) < 1000 and
                    abs(other.position.distance_nm - pos.distance_nm) < 3):
                print(f"  ⚠️  Tower: Separation warning! {aircraft.callsign} ↔ {callsign}")
                aircraft.receive_instruction(f"Climb to avoid {callsign}")
                other.receive_instruction(f"Descend to avoid {aircraft.callsign}")

    def runway_cleared(self) -> None:
        """Called when a landing/takeoff is complete."""
        print(f"\n  🗼 Tower: Runway clear")
        if self._holding_queue:
            next_aircraft = self._holding_queue.pop(0)
            print(f"  🗼 Tower: Clearing {next_aircraft.callsign} from hold")
            next_aircraft.receive_instruction("Cleared to land — runway available")
            next_aircraft.status = FlightStatus.LANDING
        else:
            self._runway_clear = True

    def _broadcast(self, message: str, exclude: Aircraft | None = None) -> None:
        for aircraft in self._aircraft.values():
            if aircraft is not exclude:
                aircraft.receive_instruction(f"[All traffic] {message}")


# ─────────────────────────────────────────
# Client
# ─────────────────────────────────────────
tower = ControlTower("KJFK")

ba112  = Aircraft("BA112",  tower)
ua441  = Aircraft("UA441",  tower)
dl889  = Aircraft("DL889",  tower)

for a in [ba112, ua441, dl889]:
    tower.register(a)

print("\n--- Landing requests ---")
ba112.request_landing()   # gets clearance
ua441.request_landing()   # goes to holding
dl889.request_landing()   # goes to holding

print("\n--- BA112 completes landing ---")
tower.runway_cleared()    # UA441 gets clearance automatically

print("\n--- Emergency declared ---")
dl889.declare_emergency("Engine failure — fuel critical")
```

---

### Example 3: UI Form Mediator

```python
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Callable
from enum import Enum

# ─────────────────────────────────────────
# Events
# ─────────────────────────────────────────
class Event(Enum):
    CHANGED   = "changed"
    CLICKED   = "clicked"
    VALIDATED = "validated"
    SUBMITTED = "submitted"

# ─────────────────────────────────────────
# Base Component
# ─────────────────────────────────────────
class FormMediator:
  pass

class UIComponent:
    def __init__(self, name: str):
        self.name      = name
        self._mediator: FormMediator | None = None
        self.visible   = True
        self.enabled   = True

    def set_mediator(self, mediator: 'FormMediator') -> None:
        self._mediator = mediator

    def emit(self, event: Event, data: Any = None) -> None:
        if self._mediator:
            self._mediator.on_event(self, event, data)

    def show(self) -> None:
        self.visible = True
        print(f"  👁️  {self.name}: visible")

    def hide(self) -> None:
        self.visible = False
        print(f"  🙈 {self.name}: hidden")

    def enable(self) -> None:
        self.enabled = True
        print(f"  ✅ {self.name}: enabled")

    def disable(self) -> None:
        self.enabled = False
        print(f"  🚫 {self.name}: disabled")


class InputField(UIComponent):
    def __init__(self, name: str, placeholder: str = ""):
        super().__init__(name)
        self.value       = ""
        self.placeholder = placeholder
        self.error       = ""

    def set_value(self, value: str) -> None:
        self.value = value
        print(f"  ✏️  {self.name}: '{value}'")
        self.emit(Event.CHANGED, value)

    def show_error(self, msg: str) -> None:
        self.error = msg
        print(f"  ❌ {self.name} error: {msg}")

    def clear_error(self) -> None:
        self.error = ""


class DropDown(UIComponent):
    def __init__(self, name: str, options: list[str]):
        super().__init__(name)
        self.options  = options
        self.selected = ""

    def select(self, option: str) -> None:
        if option in self.options:
            self.selected = option
            print(f"  🔽 {self.name}: selected '{option}'")
            self.emit(Event.CHANGED, option)

    def set_options(self, options: list[str]) -> None:
        self.options  = options
        self.selected = ""
        print(f"  🔽 {self.name}: options updated → {options}")


class CheckBox(UIComponent):
    def __init__(self, name: str, label: str):
        super().__init__(name)
        self.label   = label
        self.checked = False

    def toggle(self, value: bool | None = None) -> None:
        self.checked = value if value is not None else not self.checked
        state = "✓" if self.checked else "✗"
        print(f"  [{state}] {self.name}: {self.label}")
        self.emit(Event.CHANGED, self.checked)


class SubmitButton(UIComponent):
    def click(self) -> None:
        if self.enabled:
            print(f"\n  🖱️  {self.name} clicked")
            self.emit(Event.CLICKED)
        else:
            print(f"  🚫 {self.name} is disabled")


# ─────────────────────────────────────────
# Concrete Mediator: Registration Form
# ─────────────────────────────────────────
class RegistrationFormMediator:
    """
    Coordinates a user registration form:
    - Country selection updates city dropdown
    - 'Is Business' checkbox reveals tax ID field
    - Password confirmation validates in real time
    - Submit button only enabled when form is valid
    """

    def __init__(self):
        # Create all components
        self.username    = InputField("Username",    "Enter username")
        self.email       = InputField("Email",       "Enter email")
        self.password    = InputField("Password",    "Enter password")
        self.confirm_pwd = InputField("ConfirmPwd",  "Repeat password")
        self.country     = DropDown("Country",  ["USA", "UK", "Canada"])
        self.city        = DropDown("City",     [])
        self.is_business = CheckBox("IsBusiness", "Register as business")
        self.tax_id      = InputField("TaxID",    "Enter tax ID")
        self.submit      = SubmitButton("Submit")

        # City options per country
        self._cities = {
            "USA":    ["New York", "Los Angeles", "Chicago"],
            "UK":     ["London", "Manchester", "Edinburgh"],
            "Canada": ["Toronto", "Vancouver", "Montreal"],
        }

        # Register mediator with all components
        for component in [
            self.username, self.email, self.password, self.confirm_pwd,
            self.country, self.city, self.is_business, self.tax_id, self.submit
        ]:
            component.set_mediator(self)

        # Initial state
        self.tax_id.hide()
        self.submit.disable()

    def on_event(self, sender: UIComponent, event: Event, data: Any = None) -> None:
        if sender is self.country and event == Event.CHANGED:
            self._handle_country_change(data)

        elif sender is self.is_business and event == Event.CHANGED:
            self._handle_business_toggle(data)

        elif sender is self.confirm_pwd and event == Event.CHANGED:
            self._validate_passwords()

        elif sender is self.submit and event == Event.CLICKED:
            self._handle_submit()

        # Revalidate form on any change
        self._update_submit_button()

    def _handle_country_change(self, country: str) -> None:
        cities = self._cities.get(country, [])
        self.city.set_options(cities)
        if cities:
            self.city.select(cities[0])

    def _handle_business_toggle(self, checked: bool) -> None:
        if checked:
            self.tax_id.show()
        else:
            self.tax_id.hide()
            self.tax_id.value = ""

    def _validate_passwords(self) -> None:
        if (self.confirm_pwd.value and
                self.password.value != self.confirm_pwd.value):
            self.confirm_pwd.show_error("Passwords do not match")
        else:
            self.confirm_pwd.clear_error()

    def _update_submit_button(self) -> None:
        # Form is valid when:
        # - Username, email, password, confirm_pwd are filled
        # - Passwords match
        # - If business: tax_id filled
        # - Country and city selected
        required_filled = all([
            self.username.value,
            self.email.value,
            self.password.value,
            self.confirm_pwd.value,
            self.country.selected,
            self.city.selected,
        ])
        passwords_match = self.password.value == self.confirm_pwd.value
        business_ok = (
            not self.is_business.checked or
            bool(self.tax_id.value)
        )

        if required_filled and passwords_match and business_ok:
            self.submit.enable()
        else:
            self.submit.disable()

    def _handle_submit(self) -> None:
        data: Dict[str, Any] = {
            "username":    self.username.value,
            "email":       self.email.value,
            "country":     self.country.selected,
            "city":        self.city.selected,
            "is_business": self.is_business.checked,
        }
        if self.is_business.checked:
            data["tax_id"] = self.tax_id.value

        print(f"\n  📤 Form submitted!")
        for k, v in data.items():
            print(f"     {k}: {v}")


# ─────────────────────────────────────────
# Client
# ─────────────────────────────────────────
print("=== Registration Form Demo ===\n")
form = RegistrationFormMediator()

print("\n--- User fills in details ---")
form.username.set_value("john_doe")
form.email.set_value("john@example.com")
form.country.select("USA")
form.city.select("New York")
form.password.set_value("secret123")
form.confirm_pwd.set_value("secret456")   # mismatch!

print("\n--- Fix password ---")
form.confirm_pwd.set_value("secret123")  # now matches → submit enables

print("\n--- Toggle business registration ---")
form.is_business.toggle(True)            # shows tax ID field → disables submit
form.tax_id.set_value("TAX-99887")       # fills it → re-enables submit

print("\n--- Submit ---")
form.submit.click()
```

---

## ⚠️ Common Pitfalls

### ❌ Pitfall 1: Mediator Becomes a God Object

```python
# ❌ WRONG — mediator knows and controls everything
class GodMediator:
    def notify(self, sender, event):
        if event == "a": ...
        elif event == "b": ...
        elif event == "c": ...
        # 500 more elif branches — this is a maintenance nightmare!

# ✅ CORRECT — split into focused mediators by domain
class CheckoutMediator:    ...   # handles checkout flow
class SearchMediator:      ...   # handles search interactions
class NavigationMediator:  ...   # handles page routing
```

### ❌ Pitfall 2: Components Bypassing the Mediator

```python
# ❌ WRONG — component talks directly to another component
class Button(Component):
    def __init__(self, textbox):
        self.textbox = textbox   # direct reference — bypass!

    def click(self):
        self.textbox.enable()   # should go through mediator!

# ✅ CORRECT — all communication through mediator only
class Button(Component):
    def click(self):
        self.emit(Event.CLICKED)  # mediator decides what happens
```

### ❌ Pitfall 3: Mediator Holding Business Logic

```python
# ❌ WRONG — mediator doing complex business logic
class Mediator:
    def notify(self, sender, event):
        if event == "purchase":
            tax    = calculate_complex_tax(...)
            stock  = check_inventory(...)
            points = award_loyalty_points(...)
            # This belongs in a service, not a mediator!

# ✅ CORRECT — mediator only coordinates; delegates to services
class Mediator:
    def __init__(self, order_service, inventory_service):
        self._orders    = order_service
        self._inventory = inventory_service

    def notify(self, sender, event):
        if event == "purchase":
            self._orders.process(...)       # delegate
            self._inventory.reserve(...)    # delegate
```

### ❌ Pitfall 4: Forgetting to Register Mediator with Components

```python
# ❌ WRONG — mediator created but components don't know about it
button  = Button()
textbox = TextBox()
mediator = FormMediator(button, textbox)   # components never told!

button.click()   # self._mediator is None — silently does nothing

# ✅ CORRECT — always register mediator during construction
class FormMediator:
    def __init__(self, button, textbox):
        self._button  = button
        self._textbox = textbox
        button.set_mediator(self)    # ← register!
        textbox.set_mediator(self)   # ← register!
```

---

## ✅ Best Practices

### 1. Use Event Enums Instead of Raw Strings

```python
# ✅ Enum prevents typos and enables IDE autocomplete
class Event(Enum):
    CLICKED  = "clicked"
    CHANGED  = "changed"
    SUBMITTED = "submitted"

self.emit(Event.CLICKED)   # safe
# vs
self.emit("clickd")        # ❌ typo silently ignored
```

### 2. Pass Data with Events

```python
# ✅ Carry relevant data with the event
def emit(self, event: Event, data: Any = None) -> None:
    if self._mediator:
        self._mediator.on_event(self, event, data)

# Mediator receives what changed without querying the component
def on_event(self, sender, event, data):
    if event == Event.CHANGED:
        self._update_dependent_fields(data)   # data is the new value
```

### 3. Keep Components Unaware of Each Other

```python
# ✅ Components should only know: their mediator + their own state
class GoodComponent(UIComponent):
    def change(self, value):
        self.value = value
        self.emit(Event.CHANGED, value)   # that's it — mediator handles the rest

# ❌ Components should never hold references to sibling components
class BadComponent(UIComponent):
    def __init__(self, sibling):
        self.sibling = sibling   # coupled! bypass mediator!
```

### 4. Split Large Mediators by Feature

```python
# ✅ One mediator per coherent feature group
class BillingFormMediator:  ...   # payment fields coordination
class AddressFormMediator:  ...   # address auto-fill logic
class CheckoutOrchestrator: ...   # combines both mediators
```

---

## 📊 Summary

| Aspect               | Detail                                                            |
|----------------------|-------------------------------------------------------------------|
| **Type**             | Behavioral                                                        |
| **Intent**           | Replace O(n²) component connections with O(n) via a hub           |
| **Key Benefit**      | Loose coupling, single coordination point, easy to extend         |
| **Participants**     | Mediator, ConcreteMediator, Component, ConcreteComponents         |
| **Real-world Use**   | Chat servers, UI forms, ATC systems, event buses, MVC controllers |
| **Python Use Cases** | Django signals, GUI frameworks (tkinter, PyQt), message brokers   |

---

## ✅ Mediator Pattern Checklist

- Do components communicate only through the mediator?
- Does no component hold a direct reference to a sibling?
- Is the mediator registered with ALL components it coordinates?
- Are events typed (Enum) rather than raw strings?
- Is the mediator free of complex business logic (delegates to services)?
- Is the mediator split by domain if it grows too large?
- Can a new component be added without modifying existing ones?

---

## 💡 Key Takeaways

1. **Replaces O(n²) connections with O(n)** — n components need only n mediator links, not n×(n-1) peer links
2. **Components become reusable** — they depend only on the mediator interface, not on each other
3. **Single place to understand interactions** — all coordination logic lives in one class
4. **Django signals** and **event buses** are real-world implementations of this pattern
5. **MVC Controllers** are essentially mediators between the View and the Model
