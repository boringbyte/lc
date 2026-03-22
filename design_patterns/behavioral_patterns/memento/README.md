# 🧠 **Memento Pattern**

---

## 📋 Table of Contents
- [What is Memento Pattern?](#-what-is-memento-pattern)
  - [Key Characteristics](#-key-characteristics)
  - [The Problem It Solves](#-the-problem-it-solves)
  - [Real-World Analogy](#-real-world-analogy)
  - [Visual Representation](#-visual-representation)
- [When to Use](#-when-to-use)
- [When NOT to Use](#-when-not-to-use)
- [Basic Implementation](#-basic-implementation)
- [Real-World Examples](#-real-world-examples)
  - [Example 1: Text Editor with Full Undo History](#example-1-text-editor-with-full-undo-history)
  - [Example 2: Game Save System](#example-2-game-save-system)
  - [Example 3: Transaction Rollback System](#example-3-transaction-rollback-system)
- [Common Pitfalls](#-common-pitfalls)
- [Best Practices](#-best-practices)
- [Summary](#-summary)
- [Memento Pattern Checklist](#-memento-pattern-checklist)
- [Key Takeaways](#-key-takeaways)

---

## 🔷 What is Memento Pattern?

**Memento Pattern** is a behavioral design pattern that lets you **capture and restore an object's internal state** without violating its encapsulation. The object's private state is saved into a "memento" snapshot that can be restored later — the outside world never sees the internals.

---

### 🔑 Key Characteristics

| Characteristic              | Description                                                    |
|-----------------------------|----------------------------------------------------------------|
| **Encapsulation Preserved** | State is saved/restored without exposing internals             |
| **Snapshot-based**          | A memento is an immutable snapshot of state at a point in time |
| **Originator-controlled**   | Only the originator can write/read a memento's contents        |
| **Caretaker-managed**       | History of mementos is managed externally                      |
| **Reversibility**           | Any past state can be fully restored                           |

---

### 🔥 The Problem It Solves

To implement undo, you need to save state. But saving state naively breaks encapsulation:

```python
# ❌ WITHOUT Memento — forced to expose private state for undo
class Editor:
    def __init__(self):
        self._content  = ""
        self._font     = "Arial"
        self._cursor   = 0

# To save state externally, the caretaker must reach into privates:
saved_content = editor._content   # ❌ breaks encapsulation!
saved_font    = editor._font      # ❌ now caretaker knows internals!
saved_cursor  = editor._cursor    # ❌ tightly coupled to Editor fields!

# If Editor renames _content to _text, ALL caretaker code breaks!
```

With Memento:

```python
# ✅ WITH Memento — state saved as an opaque snapshot
memento = editor.save()           # Editor controls what goes in
history.push(memento)             # Caretaker stores it (opaque box)
editor.restore(memento)           # Editor controls how to restore
# Caretaker never touches memento's internals — encapsulation intact
```

---

### 🌍 Real-World Analogy

Think of **save points in a video game**:

```
Game State ──► Save Slot 1  (dungeon entrance)
Game State ──► Save Slot 2  (after boss fight)
Game State ──► Save Slot 3  (collected all items)

Player dies → Load Save Slot 2 → Game restored exactly
```

- The **game** (Originator) creates the save file
- The **save slots** (Mementos) store the frozen state
- The **save manager** (Caretaker) manages which slots exist
- The player (Client) never manually edits the save file binary

---

### 🖼️ Visual Representation

```
┌──────────────────┐      save()      ┌──────────────────┐
│   Originator     │ ───────────────► │     Memento      │
│                  │                  │  (opaque state)  │
│  _state = {...}  │ ◄─────────────── │                  │
│  save()          │    restore()     │  _state: private │
│  restore()       │                  │  get_state()     │
└──────────────────┘                  └────────┬─────────┘
                                               │ stores
                                               ▼
                                      ┌──────────────────┐
                                      │    Caretaker     │
                                      │                  │
                                      │  history: []     │
                                      │  push(memento)   │
                                      │  pop() → memento │
                                      └──────────────────┘
```

---

### 🔀 Participants

| Role           | Responsibility                                                   |
|----------------|------------------------------------------------------------------|
| **Originator** | Creates mementos from its state; restores state from mementos    |
| **Memento**    | Immutable snapshot of originator's internal state                |
| **Caretaker**  | Stores and manages mementos; never reads their contents          |
| **Client**     | Instructs caretaker to save/restore; triggers originator actions |

---

## ✅ When to Use

| Scenario                                              | Why It Fits                                   |
|-------------------------------------------------------|-----------------------------------------------|
| Need **undo/redo** without breaking encapsulation     | Memento is designed for this                  |
| Need **snapshots** of object state at different times | Each save = one memento                       |
| Need **rollback** on failure in a workflow            | Save before risky operation, restore on error |
| Need **checkpoints** in a long-running process        | Save progress at milestones                   |
| Want to **compare** past vs current state             | Diff two mementos                             |

---

## ❌ When NOT to Use

- When the object's state is **very large** — mementos consume significant memory
- When **frequent saves** are needed — snapshot overhead may be too high
- When state can be **recomputed cheaply** — no need to snapshot it
- When the object has **external references** (e.g. open files, DB connections) — snapshots can't capture those

---

## 🏗️ Basic Implementation

### Classic Structure

```python
from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from copy import deepcopy
from datetime import datetime

# ─────────────────────────────────────────
# Memento — immutable snapshot
# ─────────────────────────────────────────
class Memento:
    """
    Opaque container for state.
    Only the Originator should read its contents.
    Caretaker treats it as a black box.
    """

    def __init__(self, state: Any):
        self.__state    = deepcopy(state)       # deep copy — fully isolated
        self.__created  = datetime.now()

    def _get_state(self) -> Any:
        """
        Name-mangled: only accessible as _Memento__state.
        Signals to other classes: "don't touch this."
        """
        return deepcopy(self.__state)           # return copy, not reference

    @property
    def created_at(self) -> datetime:
        return self.__created

    def __repr__(self):
        return f"Memento(saved at {self.__created.strftime('%H:%M:%S')})"


# ─────────────────────────────────────────
# Originator — the object whose state we save
# ─────────────────────────────────────────
class TextEditor:
    def __init__(self):
        self._content  = ""
        self._cursor   = 0
        self._font     = "Arial"
        self._font_size = 12

    def type(self, text: str) -> None:
        self._content = (
            self._content[:self._cursor] +
            text +
            self._content[self._cursor:]
        )
        self._cursor += len(text)

    def set_font(self, font: str, size: int) -> None:
        self._font      = font
        self._font_size = size

    def show(self) -> None:
        print(f"  📄 Content : '{self._content}'")
        print(f"     Cursor  : {self._cursor}")
        print(f"     Font    : {self._font} {self._font_size}pt")

    # ── Memento interface ──────────────────
    def save(self) -> Memento:
        """Captures full internal state into a Memento."""
        return Memento({
            "content":   self._content,
            "cursor":    self._cursor,
            "font":      self._font,
            "font_size": self._font_size,
        })

    def restore(self, memento: Memento) -> None:
        """Restores state from a Memento."""
        state = memento._get_state()            # only originator calls this
        self._content   = state["content"]
        self._cursor    = state["cursor"]
        self._font      = state["font"]
        self._font_size = state["font_size"]


# ─────────────────────────────────────────
# Caretaker — manages history of mementos
# ─────────────────────────────────────────
class History:
    def __init__(self, originator: TextEditor):
        self._originator = originator
        self._mementos:  list[Memento] = []

    def save(self) -> None:
        m = self._originator.save()
        self._mementos.append(m)
        print(f"  💾 Saved  → {m}")

    def undo(self) -> None:
        if len(self._mementos) < 2:
            print("  ⚠️  Nothing to undo")
            return
        self._mementos.pop()                    # discard current
        m = self._mementos[-1]                  # restore previous
        self._originator.restore(m)
        print(f"  ↩️  Restored → {m}")

    def show_history(self) -> None:
        print(f"  📚 History ({len(self._mementos)} snapshots):")
        for i, m in enumerate(self._mementos):
            marker = " ◄ current" if i == len(self._mementos) - 1 else ""
            print(f"     [{i}] {m}{marker}")


# ─────────────────────────────────────────
# Client
# ─────────────────────────────────────────
editor  = TextEditor()
history = History(editor)

history.save()                        # snapshot 0: empty

editor.type("Hello")
history.save()                        # snapshot 1

editor.type(", World")
history.save()                        # snapshot 2

editor.set_font("Consolas", 14)
editor.type("!")
history.save()                        # snapshot 3

print("\n=== Current State ===")
editor.show()

history.show_history()

print("\n=== Undo ===")
history.undo()
editor.show()

print("\n=== Undo again ===")
history.undo()
editor.show()
```

---

## 🌍 Real-World Examples

### Example 1: Text Editor with Full Undo History

```python
from __future__ import annotations
from copy import deepcopy
from dataclasses import dataclass, field
from typing import  Any
from datetime import datetime
from enum import Enum, auto

class ActionType(Enum):
    TYPE    = auto()
    DELETE  = auto()
    FORMAT  = auto()
    INSERT  = auto()

# ─────────────────────────────────────────
# Memento
# ─────────────────────────────────────────
class EditorMemento:
    def __init__(self, state: dict[str, Any], label: str = ""):
        self.__state      = deepcopy(state)
        self.__created_at = datetime.now()
        self.__label      = label

    def _get_state(self) -> dict[str, Any]:
        return deepcopy(self.__state)

    @property
    def label(self) -> str:
        return self.__label or f"Snapshot at {self.__created_at.strftime('%H:%M:%S')}"

    def __repr__(self):
        return f"Memento('{self.__label}')"


# ─────────────────────────────────────────
# Originator: Rich Text Editor
# ─────────────────────────────────────────
@dataclass
class TextFormat:
    bold:      bool = False
    italic:    bool = False
    underline: bool = False
    color:     str  = "black"
    font_size: int  = 12

class RichTextEditor:
    def __init__(self):
        self._content:    str             = ""
        self._cursor:     int             = 0
        self._selection:  tuple | None = None    # (start, end)
        self._format:     TextFormat      = TextFormat()
        self._title:      str             = "Untitled"

    # ── Editing operations ─────────────────
    def type(self, text: str) -> None:
        if self._selection:
            start, end = self._selection
            self._content  = self._content[:start] + self._content[end:]
            self._cursor   = start
            self._selection = None

        self._content = (
            self._content[:self._cursor] + text + self._content[self._cursor:]
        )
        self._cursor += len(text)
        print(f"  ✏️  Typed: '{text}'")

    def delete(self, count: int = 1) -> None:
        if self._cursor > 0:
            deleted = self._content[self._cursor - count:self._cursor]
            self._content = (
                self._content[:self._cursor - count] + self._content[self._cursor:]
            )
            self._cursor -= count
            print(f"  🗑️  Deleted: '{deleted}'")

    def select(self, start: int, end: int) -> None:
        self._selection = (start, end)
        selected = self._content[start:end]
        print(f"  🔵 Selected [{start}:{end}]: '{selected}'")

    def set_format(self, **kwargs) -> None:
        for k, v in kwargs.items():
            if hasattr(self._format, k):
                setattr(self._format, k, v)
        print(f"  🎨 Format: {kwargs}")

    def set_title(self, title: str) -> None:
        self._title = title

    def show(self) -> None:
        fmt = self._format
        style = " ".join(filter(None, [
            "Bold"      if fmt.bold      else "",
            "Italic"    if fmt.italic    else "",
            "Underline" if fmt.underline else "",
        ])) or "Normal"
        print(f"  📄 [{self._title}] '{self._content}'")
        print(f"     Cursor: {self._cursor} | Style: {style} "
              f"| Size: {fmt.font_size}pt | Color: {fmt.color}")

    # ── Memento interface ──────────────────
    def save(self, label: str = "") -> EditorMemento:
        return EditorMemento({
            "content":   self._content,
            "cursor":    self._cursor,
            "selection": self._selection,
            "format":    deepcopy(self._format),
            "title":     self._title,
        }, label=label)

    def restore(self, memento: EditorMemento) -> None:
        state            = memento._get_state()
        self._content    = state["content"]
        self._cursor     = state["cursor"]
        self._selection  = state["selection"]
        self._format     = deepcopy(state["format"])
        self._title      = state["title"]


# ─────────────────────────────────────────
# Caretaker: Full Undo/Redo History
# ─────────────────────────────────────────
class EditorCaretaker:
    def __init__(self, editor: RichTextEditor, max_history: int = 50):
        self._editor      = editor
        self._max_history = max_history
        self._undo_stack: list[EditorMemento] = []
        self._redo_stack: list[EditorMemento] = []

    def checkpoint(self, label: str = "") -> None:
        """Save current state as a checkpoint."""
        m = self._editor.save(label)
        self._undo_stack.append(m)
        self._redo_stack.clear()    # new change invalidates redo

        # Enforce max history size
        if len(self._undo_stack) > self._max_history:
            self._undo_stack.pop(0)

        print(f"  💾 Checkpoint: '{m.label}'")

    def undo(self) -> bool:
        if len(self._undo_stack) < 2:
            print("  ⚠️  Nothing to undo")
            return False

        current = self._undo_stack.pop()
        self._redo_stack.append(current)

        previous = self._undo_stack[-1]
        self._editor.restore(previous)
        print(f"  ↩️  Undo → restored '{previous.label}'")
        return True

    def redo(self) -> bool:
        if not self._redo_stack:
            print("  ⚠️  Nothing to redo")
            return False

        m = self._redo_stack.pop()
        self._undo_stack.append(m)
        self._editor.restore(m)
        print(f"  ↪️  Redo → '{m.label}'")
        return True

    def show_history(self) -> None:
        print(f"\n  📚 Undo stack ({len(self._undo_stack)}):")
        for i, m in enumerate(self._undo_stack):
            tag = " ◄ current" if i == len(self._undo_stack) - 1 else ""
            print(f"     [{i}] {m.label}{tag}")
        print(f"  📚 Redo stack ({len(self._redo_stack)}):")
        for i, m in enumerate(self._redo_stack):
            print(f"     [{i}] {m.label}")


# ─────────────────────────────────────────
# Client
# ─────────────────────────────────────────
editor    = RichTextEditor()
caretaker = EditorCaretaker(editor)

editor.set_title("My Document")
caretaker.checkpoint("Initial empty state")

editor.type("Hello World")
caretaker.checkpoint("After typing 'Hello World'")

editor.select(6, 11)
editor.type("Python")
caretaker.checkpoint("Replaced 'World' with 'Python'")

editor.set_format(bold=True, color="blue", font_size=16)
caretaker.checkpoint("Applied bold blue formatting")

editor.type(" — awesome!")
caretaker.checkpoint("Added suffix")

print("\n=== Current State ===")
editor.show()
caretaker.show_history()

print("\n--- Undo 2 times ---")
caretaker.undo()
editor.show()
caretaker.undo()
editor.show()

print("\n--- Redo ---")
caretaker.redo()
editor.show()
```

---

### Example 2: Game Save System

```python
from __future__ import annotations
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any
from datetime import datetime

# ─────────────────────────────────────────
# Game State Data Classes
# ─────────────────────────────────────────
@dataclass
class PlayerStats:
    level:  int   = 1
    hp:     int   = 100
    max_hp: int   = 100
    xp:     int   = 0
    gold:   int   = 50

@dataclass
class WorldState:
    current_zone:    str        = "Starting Village"
    position:        tuple      = (0, 0)
    discovered_zones: list[str] = field(default_factory=list)
    completed_quests: list[str] = field(default_factory=list)

@dataclass
class Inventory:
    items:    list[str]      = field(default_factory=list)
    equipped: dict[str, str] = field(default_factory=dict)

    def add(self, item: str):
        self.items.append(item)

    def equip(self, slot: str, item: str):
        if item in self.items:
            self.equipped[slot] = item


# ─────────────────────────────────────────
# Memento: Save File
# ─────────────────────────────────────────
class SaveFile:
    def __init__(self, state: dict[str, Any], slot_name: str):
        self.__state      = deepcopy(state)
        self.__slot_name  = slot_name
        self.__saved_at   = datetime.now()
        self.__play_time  = state.get("play_time", 0)

    def _get_state(self) -> dict[str, Any]:
        return deepcopy(self.__state)

    @property
    def slot_name(self) -> str:
        return self.__slot_name

    @property
    def saved_at(self) -> datetime:
        return self.__saved_at

    @property
    def play_time(self) -> int:
        return self.__play_time

    def summary(self) -> str:
        s = self.__state
        return (
            f"  💾 [{self.__slot_name}] "
            f"Zone: {s['world']['current_zone']} | "
            f"Level: {s['stats']['level']} | "
            f"HP: {s['stats']['hp']}/{s['stats']['max_hp']} | "
            f"Gold: {s['stats']['gold']} | "
            f"Saved: {self.__saved_at.strftime('%H:%M:%S')}"
        )


# ─────────────────────────────────────────
# Originator: Game
# ─────────────────────────────────────────
class Game:
    def __init__(self, player_name: str):
        self.player_name = player_name
        self._stats      = PlayerStats()
        self._world      = WorldState()
        self._inventory  = Inventory()
        self._play_time  = 0        # seconds

    # ── Game actions ───────────────────────
    def gain_xp(self, amount: int) -> None:
        self._stats.xp += amount
        print(f"  ⭐ Gained {amount} XP (total: {self._stats.xp})")
        if self._stats.xp >= self._stats.level * 100:
            self._level_up()

    def _level_up(self) -> None:
        self._stats.level  += 1
        self._stats.max_hp += 20
        self._stats.hp      = self._stats.max_hp
        self._stats.xp      = 0
        print(f"  🎉 LEVEL UP! Now level {self._stats.level} | HP: {self._stats.hp}")

    def take_damage(self, amount: int) -> None:
        self._stats.hp = max(0, self._stats.hp - amount)
        print(f"  💔 Took {amount} damage | HP: {self._stats.hp}/{self._stats.max_hp}")
        if self._stats.hp == 0:
            print("  💀 You died!")

    def collect_gold(self, amount: int) -> None:
        self._stats.gold += amount
        print(f"  💰 Collected {amount} gold (total: {self._stats.gold})")

    def pick_up(self, item: str) -> None:
        self._inventory.add(item)
        print(f"  🎒 Picked up: {item}")

    def travel_to(self, zone: str, position: tuple) -> None:
        self._world.current_zone = zone
        self._world.position     = position
        if zone not in self._world.discovered_zones:
            self._world.discovered_zones.append(zone)
            print(f"  🗺️  Discovered new zone: {zone}!")
        else:
            print(f"  🚶 Traveled to: {zone}")

    def complete_quest(self, quest: str) -> None:
        self._world.completed_quests.append(quest)
        print(f"  📜 Quest completed: '{quest}'")

    def show_status(self) -> None:
        print(f"\n  👤 {self.player_name}")
        print(f"     Zone  : {self._world.current_zone} {self._world.position}")
        print(f"     Level : {self._stats.level} | "
              f"HP: {self._stats.hp}/{self._stats.max_hp} | "
              f"XP: {self._stats.xp} | Gold: {self._stats.gold}")
        print(f"     Items : {self._inventory.items}")
        print(f"     Quests: {self._world.completed_quests}")

    # ── Memento interface ──────────────────
    def save(self, slot_name: str) -> SaveFile:
        return SaveFile({
            "player_name": self.player_name,
            "stats":       deepcopy(self._stats).__dict__,
            "world": {
                "current_zone":     self._world.current_zone,
                "position":         self._world.position,
                "discovered_zones": list(self._world.discovered_zones),
                "completed_quests": list(self._world.completed_quests),
            },
            "inventory": {
                "items":    list(self._inventory.items),
                "equipped": dict(self._inventory.equipped),
            },
            "play_time": self._play_time,
        }, slot_name=slot_name)

    def restore(self, save_file: SaveFile) -> None:
        state = save_file._get_state()

        s                    = state["stats"]
        self._stats          = PlayerStats(**s)

        w                    = state["world"]
        self._world          = WorldState(
            current_zone    = w["current_zone"],
            position        = w["position"],
            discovered_zones = w["discovered_zones"],
            completed_quests = w["completed_quests"],
        )

        i                    = state["inventory"]
        self._inventory      = Inventory(
            items    = i["items"],
            equipped = i["equipped"],
        )
        self._play_time      = state.get("play_time", 0)
        print(f"  📂 Loaded save: '{save_file.slot_name}'")


# ─────────────────────────────────────────
# Caretaker: Save Manager
# ─────────────────────────────────────────
class SaveManager:
    MAX_SLOTS = 5

    def __init__(self, game: Game):
        self._game  = game
        self._slots: dict[str, SaveFile] = {}

    def save(self, slot_name: str) -> None:
        if slot_name in self._slots:
            print(f"  ⚠️  Overwriting slot '{slot_name}'")
        self._slots[slot_name] = self._game.save(slot_name)
        print(self._slots[slot_name].summary())

    def load(self, slot_name: str) -> bool:
        if slot_name not in self._slots:
            print(f"  ❌ No save in slot '{slot_name}'")
            return False
        self._game.restore(self._slots[slot_name])
        return True

    def delete(self, slot_name: str) -> None:
        if slot_name in self._slots:
            del self._slots[slot_name]
            print(f"  🗑️  Deleted slot '{slot_name}'")

    def list_saves(self) -> None:
        if not self._slots:
            print("  📂 No save files found")
            return
        print(f"\n  📂 Save Files ({len(self._slots)} slots):")
        for slot_name, save in self._slots.items():
            print(save.summary())


# ─────────────────────────────────────────
# Client
# ─────────────────────────────────────────
game    = Game("Hero")
manager = SaveManager(game)

print("=== Starting Adventure ===")
game.travel_to("Starting Village", (0, 0))
game.pick_up("Wooden Sword")
game.collect_gold(30)

manager.save("slot_1")  # save at village

print("\n=== Exploring the forest ===")
game.travel_to("Dark Forest", (10, 5))
game.gain_xp(60)
game.pick_up("Magic Shield")
game.complete_quest("Find the Forest Path")

manager.save("slot_2")  # save in forest

print("\n=== Boss Fight ===")
game.gain_xp(50)         # level up!
game.take_damage(80)     # nearly dead!
game.collect_gold(200)

manager.save("slot_3")   # save after boss

print("\n=== Tough Enemy — near death ===")
game.take_damage(95)     # dead!
game.show_status()

print("\n=== Loading last safe save ===")
manager.list_saves()
manager.load("slot_2")   # reload forest save
game.show_status()
```

---

### Example 3: Transaction Rollback System

```python
from __future__ import annotations
from copy import deepcopy
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime
from contextlib import contextmanager

# ─────────────────────────────────────────
# Memento: Database Snapshot
# ─────────────────────────────────────────
class DBSnapshot:
    def __init__(self, tables: Dict[str, Any], transaction_id: str):
        self.__tables         = deepcopy(tables)
        self.__transaction_id = transaction_id
        self.__created_at     = datetime.now()

    def _get_tables(self) -> Dict[str, Any]:
        return deepcopy(self.__tables)

    @property
    def transaction_id(self) -> str:
        return self.__transaction_id

    @property
    def created_at(self) -> datetime:
        return self.__created_at

    def __repr__(self):
        return f"Snapshot(txn={self.__transaction_id})"


# ─────────────────────────────────────────
# Originator: In-Memory Database
# ─────────────────────────────────────────
class InMemoryDB:
    def __init__(self):
        self._tables: Dict[str, List[Dict]] = {}

    def create_table(self, name: str) -> None:
        self._tables[name] = []
        print(f"  🗄️  Table '{name}' created")

    def insert(self, table: str, record: Dict) -> None:
        if table not in self._tables:
            raise ValueError(f"Table '{table}' does not exist")
        self._tables[table].append(deepcopy(record))
        print(f"  ➕ INSERT INTO {table}: {record}")

    def update(self, table: str, pk: str, pk_value: Any,
               **fields) -> bool:
        if table not in self._tables:
            return False
        for record in self._tables[table]:
            if record.get(pk) == pk_value:
                record.update(fields)
                print(f"  ✏️  UPDATE {table} SET {fields} WHERE {pk}={pk_value}")
                return True
        return False

    def delete(self, table: str, pk: str, pk_value: Any) -> bool:
        if table not in self._tables:
            return False
        before = len(self._tables[table])
        self._tables[table] = [
            r for r in self._tables[table] if r.get(pk) != pk_value
        ]
        deleted = before - len(self._tables[table])
        if deleted:
            print(f"  🗑️  DELETE FROM {table} WHERE {pk}={pk_value}")
        return bool(deleted)

    def select(self, table: str) -> List[Dict]:
        return deepcopy(self._tables.get(table, []))

    def show(self, table: str) -> None:
        rows = self.select(table)
        print(f"\n  📊 {table} ({len(rows)} rows):")
        for row in rows:
            print(f"     {row}")

    # ── Memento interface ──────────────────
    def snapshot(self, txn_id: str) -> DBSnapshot:
        return DBSnapshot(self._tables, transaction_id=txn_id)

    def restore(self, snap: DBSnapshot) -> None:
        self._tables = snap._get_tables()
        print(f"  ⏪ Rolled back to {snap}")


# ─────────────────────────────────────────
# Caretaker: Transaction Manager
# ─────────────────────────────────────────
class TransactionManager:
    def __init__(self, db: InMemoryDB):
        self._db       = db
        self._counter  = 0
        self._stack:   List[DBSnapshot] = []

    def begin(self) -> str:
        self._counter += 1
        txn_id = f"TXN-{self._counter:04d}"
        snap   = self._db.snapshot(txn_id)
        self._stack.append(snap)
        print(f"\n  🟢 BEGIN {txn_id}")
        return txn_id

    def commit(self, txn_id: str) -> None:
        if self._stack:
            self._stack.pop()
        print(f"  ✅ COMMIT {txn_id}")

    def rollback(self, txn_id: str) -> None:
        if not self._stack:
            print(f"  ⚠️  Nothing to rollback for {txn_id}")
            return
        snap = self._stack.pop()
        self._db.restore(snap)
        print(f"  🔴 ROLLBACK {txn_id}")

    @contextmanager
    def transaction(self):
        """Context manager: auto-commit or rollback."""
        txn_id = self.begin()
        try:
            yield txn_id
            self.commit(txn_id)
        except Exception as e:
            print(f"  ❌ Error: {e}")
            self.rollback(txn_id)


# ─────────────────────────────────────────
# Client
# ─────────────────────────────────────────
db  = InMemoryDB()
txm = TransactionManager(db)

# Setup
db.create_table("accounts")
db.insert("accounts", {"id": 1, "name": "Alice", "balance": 1000})
db.insert("accounts", {"id": 2, "name": "Bob",   "balance": 500})

print("\n=== Successful Transfer ===")
with txm.transaction() as txn:
    db.update("accounts", "id", 1, balance=800)   # Alice -200
    db.update("accounts", "id", 2, balance=700)   # Bob   +200

db.show("accounts")

print("\n=== Failed Transfer (rollback) ===")
with txm.transaction() as txn:
    db.update("accounts", "id", 1, balance=500)   # Alice -300
    raise ValueError("Insufficient funds — transaction aborted!")

db.show("accounts")   # Alice still at 800 — rollback worked!

print("\n=== Nested Transactions ===")
outer = txm.begin()
db.insert("accounts", {"id": 3, "name": "Carol", "balance": 250})

inner = txm.begin()
db.update("accounts", "id", 3, balance=0)    # risky operation
db.show("accounts")
txm.rollback(inner)   # undo just the inner transaction
db.show("accounts")   # Carol at 250 again

txm.commit(outer)     # commit outer (Carol inserted at 250)
db.show("accounts")
```

---

## ⚠️ Common Pitfalls

### ❌ Pitfall 1: Shallow Copy Instead of Deep Copy

```python
# ❌ WRONG — shallow copy shares mutable references
class BadMemento:
    def __init__(self, state):
        self.__state = state          # same reference! mutations affect memento

# Modify original → memento is corrupted silently!
editor.content.append("x")           # also modifies BadMemento!

# ✅ CORRECT — always deep copy mutable state
from copy import deepcopy

class GoodMemento:
    def __init__(self, state):
        self.__state = deepcopy(state)  # fully independent copy
```

### ❌ Pitfall 2: Caretaker Reading Memento Internals

```python
# ❌ WRONG — caretaker reaches into memento contents
class BadCaretaker:
    def show_history(self):
        for m in self._mementos:
            print(m._Memento__state)    # breaks encapsulation!
            print(m.__state)            # AttributeError in Python

# ✅ CORRECT — only expose safe metadata from Memento
class GoodMemento:
    @property
    def label(self) -> str:    return self.__label        # safe to expose
    @property
    def created_at(self):      return self.__created_at   # safe to expose
    # __state is NEVER exposed publicly
```

### ❌ Pitfall 3: Unbounded History — Memory Leak

```python
# ❌ WRONG — history grows forever
class BadCaretaker:
    def save(self):
        self._history.append(self._editor.save())  # never pruned!

# With large documents saved every keystroke → GB of RAM!

# ✅ CORRECT — enforce a max history size
class GoodCaretaker:
    def __init__(self, max_size: int = 50):
        self._max_size = max_size

    def save(self):
        self._history.append(self._editor.save())
        if len(self._history) > self._max_size:
            self._history.pop(0)     # remove oldest
```

### ❌ Pitfall 4: Saving External Resources in Memento

```python
# ❌ WRONG — mementos can't snapshot open file handles or DB connections
class BadMemento:
    def __init__(self, state):
        self.__file_handle = state["open_file"]   # can't snapshot this!
        self.__db_conn     = state["db_conn"]      # will be stale on restore!

# ✅ CORRECT — save only serializable, self-contained state
class GoodMemento:
    def __init__(self, state):
        self.__file_path  = state["file_path"]    # path is serializable
        self.__query_log  = list(state["queries"]) # copy the log, not the connection
```

---

## ✅ Best Practices

### 1. Always Deep Copy Mutable State

```python
from copy import deepcopy

class Memento:
    def __init__(self, state):
        self.__state = deepcopy(state)   # non-negotiable for mutable objects

    def _get_state(self):
        return deepcopy(self.__state)    # also deep copy on read-out
```

### 2. Expose Only Safe Metadata from Mementos

```python
class Memento:
    # ✅ Public — safe for caretaker to display
    @property
    def label(self)      -> str:      return self.__label
    @property
    def created_at(self) -> datetime: return self.__created_at

    # ✅ Protected — only originator should call (name-mangled in Python)
    def _get_state(self) -> Any:
        return deepcopy(self.__state)

    # ❌ Never expose __state directly
```

### 3. Use Context Managers for Auto-Rollback

```python
@contextmanager
def transaction(self):
    txn_id = self.begin()
    try:
        yield txn_id
        self.commit(txn_id)
    except Exception as e:
        self.rollback(txn_id)
        raise   # re-raise so caller knows it failed
```

### 4. Label Mementos for Debugging

```python
# ✅ Always pass a meaningful label to snapshots
caretaker.checkpoint("After user typed 'Hello'")
caretaker.checkpoint("Applied bold formatting")
manager.save("slot_1")   # descriptive slot names
```

### 5. Consider Incremental Snapshots for Large State

```python
class IncrementalMemento:
    """Stores only a diff from the previous state — saves memory."""
    def __init__(self, diff: Dict[str, Any], base: 'Memento'):
        self.__diff = deepcopy(diff)
        self.__base = base   # reference to previous full snapshot

    def _reconstruct(self) -> Dict:
        base_state = self.__base._get_state()
        base_state.update(self.__diff)       # apply diff on top of base
        return base_state
```

---

## 📊 Summary

| Aspect             | Detail                                                                       |
|--------------------|------------------------------------------------------------------------------|
| **Type**           | Behavioral                                                                   |
| **Intent**         | Save and restore object state without exposing internals                     |
| **Key Roles**      | Originator (saves/restores), Memento (snapshot), Caretaker (stores mementos) |
| **Core Rule**      | Only Originator reads Memento contents; Caretaker is blind to internals      |
| **Python Tip**     | Use `__` name-mangling to enforce memento privacy                            |
| **Real-world Use** | Undo/redo, game saves, DB transactions, configuration rollback               |

---

## ✅ Memento Pattern Checklist

- Is state deep-copied into the memento (not shallow-copied)?
- Is memento state private (__state, not _state)?
- Does only the Originator call _get_state()?
- Does the Caretaker treat mementos as opaque objects?
- Is there a maximum history size to prevent memory leaks?
- Are external resources (files, connections) excluded from snapshots?
- Are mementos labeled for debugging and display?
- Is redo stack cleared when a new action is taken?
- 
---

## 💡 Key Takeaways

1. **Encapsulation is preserved** — the outside world never sees the originator's internals
2. **Deep copy is mandatory** — shallow copies silently corrupt your history
3. **Caretaker is blind** — it stores mementos but never reads their contents
4. **Python name-mangling** (`__state`) is your best tool to enforce memento privacy
5. **Memory is the cost** — every snapshot consumes RAM; always cap history size
6. **Differs from Command** — Command stores *operations* to replay; Memento stores *state* to restore
