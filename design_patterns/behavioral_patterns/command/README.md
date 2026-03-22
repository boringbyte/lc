# 🧠 **Command Pattern**

---

## 📋 Table of Contents
- [What is Command Pattern?](#-what-is-command-pattern)
  - [Key Characteristics](#-key-characteristics)
  - [The Problem It Solves](#-the-problem-it-solves)
  - [Real-World Analogy](#-real-world-analogy)
  - [Visual Representation](#-visual-representation)
- [When to Use](#-when-to-use)
- [When NOT to Use](#-when-not-to-use)
- [Basic Implementation](#-basic-implementation)
- [Real-World Examples](#-real-world-examples)
  - [Example 1: Text Editor with Undo/Redo](#example-1-text-editor-with-undoredo)
  - [Example 2: Smart Home Automation](#example-2-smart-home-automation)
  - [Example 3: Task Queue System](#example-3-task-queue-system)
- [Common Pitfalls](#-common-pitfalls)
- [Best Practices](#-best-practices)
- [Summary](#-summary)
- [Command Pattern Checklist](#-command-pattern-checklist)
- [Key Takeaways](#-key-takeaways)

---

## 🔷 What is Command Pattern?

**Command Pattern** is a behavioral design pattern that turns a **request into a stand-alone object** containing all information about that request. This lets you **parameterize methods, queue operations, log them, and support undoable operations**.

---

### 🔑 Key Characteristics

| Characteristic    | Description                                      |
|-------------------|--------------------------------------------------|
| **Encapsulation** | A request becomes a self-contained object        |
| **Decoupling**    | Invoker doesn't know how the command is executed |
| **Reversibility** | Commands can implement `undo()`                  |
| **Queueable**     | Commands can be stored, delayed, or replayed     |
| **Composable**    | Multiple commands can be grouped (Macro Command) |

---

### 🔥 The Problem It Solves

Without Command Pattern, the invoker is tightly coupled to the receiver's logic:

```python
# ❌ WITHOUT Command Pattern — tightly coupled
class Button:
    def click(self):
        # Button KNOWS how to save a document?? Wrong!
        document.save()   # coupled directly to document
        # What if we want undo? What if we want to queue it?
        # What if the same button does different things in different contexts?
```

With Command Pattern:

```python
# ✅ WITH Command Pattern — fully decoupled
class Button:
    def __init__(self, command):
        self.command = command   # Button just holds a command object

    def click(self):
        self.command.execute()   # Doesn't know or care what it does
```

---

### 🌍 Real-World Analogy

Think of a **restaurant order**:

```
You (Client) → Waiter (Invoker) → Order Slip (Command) → Chef (Receiver)
```

- The **waiter** doesn't cook; they carry the **order slip**
- The **order slip** contains all info needed to prepare the dish
- The **chef** executes the actual work
- The order can be **queued**, **canceled**, or **modified** before execution
- The kitchen can **replay** orders or **undo** mistakes

---

### 🖼️ Visual Representation

```
┌─────────┐     creates    ┌─────────────┐    stores     ┌──────────┐
│ Client  │ ─────────────► │   Command   │ ◄──────────── │ Invoker  │
└─────────┘                │  execute()  │               │  invoke()│
                           │  undo()     │               └──────────┘
                           └──────┬──────┘
                                  │ calls
                                  ▼
                           ┌─────────────┐
                           │  Receiver   │
                           │  action()   │
                           └─────────────┘
```

---

### 🔀 Participants

| Role                | Responsibility                                                |
|---------------------|---------------------------------------------------------------|
| **Client**          | Creates the command, sets its receiver                        |
| **Invoker**         | Asks the command to execute; knows nothing about what it does |
| **Command**         | Interface with `execute()` and optionally `undo()`            |
| **ConcreteCommand** | Implements the command; binds receiver + action               |
| **Receiver**        | The object that actually does the work                        |

---

## ✅ When to Use

| Scenario                                         | Why It Fits                                    |
|--------------------------------------------------|------------------------------------------------|
| Need **undo/redo** functionality                 | Commands store state for reversal              |
| Need to **queue or schedule** operations         | Commands are objects — store them anywhere     |
| Need **transactional behavior** (all or nothing) | Group commands, rollback on failure            |
| **Parameterize UI elements** with actions        | Buttons, menus, shortcuts share same interface |
| **Logging / auditing** operations                | Each command object is a log entry             |

---

## ❌ When NOT to Use

- When operations are **simple and one-off** — adds unnecessary structure
- When **undo is never needed** and actions are fire-and-forget
- When the **number of commands explodes** with tiny variations — consider strategies instead

---

## 🏗️ Basic Implementation

### Classic Structure

```python
from abc import ABC, abstractmethod

# ─────────────────────────────────────────
# Command Interface
# ─────────────────────────────────────────
class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass

    @abstractmethod
    def undo(self) -> None:
        pass


# ─────────────────────────────────────────
# Receiver — the object that does actual work
# ─────────────────────────────────────────
class Light:
    def __init__(self, location: str):
        self.location = location
        self.is_on = False

    def turn_on(self):
        self.is_on = True
        print(f"  💡 {self.location} light is ON")

    def turn_off(self):
        self.is_on = False
        print(f"  🌑 {self.location} light is OFF")


# ─────────────────────────────────────────
# Concrete Commands
# ─────────────────────────────────────────
class TurnOnCommand(Command):
    def __init__(self, light: Light):
        self._light = light

    def execute(self) -> None:
        self._light.turn_on()

    def undo(self) -> None:
        self._light.turn_off()   # reverse of execute


class TurnOffCommand(Command):
    def __init__(self, light: Light):
        self._light = light

    def execute(self) -> None:
        self._light.turn_off()

    def undo(self) -> None:
        self._light.turn_on()    # reverse of execute


# ─────────────────────────────────────────
# Invoker — triggers commands, manages history
# ─────────────────────────────────────────
class RemoteControl:
    def __init__(self):
        self._history: list[Command] = []

    def press(self, command: Command) -> None:
        command.execute()
        self._history.append(command)

    def press_undo(self) -> None:
        if self._history:
            command = self._history.pop()
            command.undo()
        else:
            print("  Nothing to undo.")


# ─────────────────────────────────────────
# Client Code
# ─────────────────────────────────────────
bedroom_light = Light("Bedroom")
remote = RemoteControl()

on_cmd  = TurnOnCommand(bedroom_light)
off_cmd = TurnOffCommand(bedroom_light)

remote.press(on_cmd)   # 💡 Bedroom light is ON
remote.press(off_cmd)  # 🌑 Bedroom light is OFF
remote.press_undo()    # 💡 Bedroom light is ON   (undone)
remote.press_undo()    # 🌑 Bedroom light is OFF  (undone)
remote.press_undo()    # Nothing to undo.
```

---

## 🌍 Real-World Examples

### Example 1: Text Editor with Undo/Redo

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

# ─────────────────────────────────────────
# Receiver
# ─────────────────────────────────────────
class Document:
    def __init__(self):
        self.content: str = ""

    def insert(self, position: int, text: str) -> None:
        self.content = (
            self.content[:position] + text + self.content[position:]
        )

    def delete(self, position: int, length: int) -> None:
        self.content = (
            self.content[:position] + self.content[position + length:]
        )

    def show(self) -> None:
        print(f"  📄 Document: '{self.content}'")


# ─────────────────────────────────────────
# Command Interface
# ─────────────────────────────────────────
class EditorCommand(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass

    @abstractmethod
    def undo(self) -> None:
        pass


# ─────────────────────────────────────────
# Concrete Commands
# ─────────────────────────────────────────
class InsertCommand(EditorCommand):
    def __init__(self, doc: Document, position: int, text: str):
        self._doc      = doc
        self._position = position
        self._text     = text

    def execute(self) -> None:
        self._doc.insert(self._position, self._text)
        print(f"  ✏️  Inserted '{self._text}' at position {self._position}")

    def undo(self) -> None:
        self._doc.delete(self._position, len(self._text))
        print(f"  ↩️  Undid insert of '{self._text}'")


class DeleteCommand(EditorCommand):
    def __init__(self, doc: Document, position: int, length: int):
        self._doc       = doc
        self._position  = position
        self._length    = length
        self._deleted   = ""   # saved for undo

    def execute(self) -> None:
        # Save deleted text BEFORE deleting (needed for undo)
        self._deleted = self._doc.content[self._position:self._position + self._length]
        self._doc.delete(self._position, self._length)
        print(f"  🗑️  Deleted '{self._deleted}' at position {self._position}")

    def undo(self) -> None:
        self._doc.insert(self._position, self._deleted)
        print(f"  ↩️  Restored '{self._deleted}'")


class ReplaceCommand(EditorCommand):
    """Macro command: Delete + Insert combined."""
    def __init__(self, doc: Document, position: int, length: int, new_text: str):
        self._delete = DeleteCommand(doc, position, length)
        self._insert = InsertCommand(doc, position, new_text)

    def execute(self) -> None:
        self._delete.execute()
        self._insert.execute()

    def undo(self) -> None:
        # Undo in REVERSE order
        self._insert.undo()
        self._delete.undo()


# ─────────────────────────────────────────
# Invoker — History Manager
# ─────────────────────────────────────────
class EditorHistory:
    def __init__(self):
        self._undo_stack: list[EditorCommand] = []
        self._redo_stack: list[EditorCommand] = []

    def execute(self, command: EditorCommand) -> None:
        command.execute()
        self._undo_stack.append(command)
        self._redo_stack.clear()   # new action clears redo history

    def undo(self) -> None:
        if not self._undo_stack:
            print("  Nothing to undo.")
            return
        command = self._undo_stack.pop()
        command.undo()
        self._redo_stack.append(command)

    def redo(self) -> None:
        if not self._redo_stack:
            print("  Nothing to redo.")
            return
        command = self._redo_stack.pop()
        command.execute()
        self._undo_stack.append(command)


# ─────────────────────────────────────────
# Client
# ─────────────────────────────────────────
doc     = Document()
history = EditorHistory()

print("=== Text Editor Demo ===\n")

history.execute(InsertCommand(doc, 0, "Hello"))
doc.show()  # 'Hello'

history.execute(InsertCommand(doc, 5, " World"))
doc.show()  # 'Hello World'

history.execute(DeleteCommand(doc, 0, 5))
doc.show()  # ' World'

history.execute(ReplaceCommand(doc, 0, 6, "Hi there!"))
doc.show()  # 'Hi there!'

print("\n--- Undo 2 times ---")
history.undo()
doc.show()  # ' World'
history.undo()
doc.show()  # 'Hello World'

print("\n--- Redo ---")
history.redo()
doc.show()  # ' World'
```

---

### Example 2: Smart Home Automation

```python
from abc import ABC, abstractmethod

# ─────────────────────────────────────────
# Receivers
# ─────────────────────────────────────────
class Light:
    def __init__(self, name: str):
        self.name       = name
        self.brightness = 0

    def set_brightness(self, level: int):
        self.brightness = max(0, min(100, level))
        print(f"  💡 {self.name}: brightness → {self.brightness}%")


class Thermostat:
    def __init__(self):
        self.temperature = 20

    def set_temperature(self, temp: float):
        self.temperature = temp
        print(f"  🌡️  Thermostat → {temp}°C")


class MusicPlayer:
    def __init__(self):
        self.playing = False
        self.volume  = 50

    def play(self, track: str):
        self.playing = True
        print(f"  🎵 Playing: {track}")

    def stop(self):
        self.playing = False
        print(f"  ⏹️  Music stopped")

    def set_volume(self, level: int):
        self.volume = level
        print(f"  🔊 Volume → {level}")


# ─────────────────────────────────────────
# Command Interface
# ─────────────────────────────────────────
class SmartHomeCommand(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass

    @abstractmethod
    def undo(self) -> None:
        pass

    @property
    def description(self) -> str:
        return self.__class__.__name__


# ─────────────────────────────────────────
# Concrete Commands
# ─────────────────────────────────────────
class SetBrightnessCommand(SmartHomeCommand):
    def __init__(self, light: Light, level: int):
        self._light    = light
        self._level    = level
        self._previous = light.brightness  # store for undo

    def execute(self):
        self._previous = self._light.brightness
        self._light.set_brightness(self._level)

    def undo(self):
        self._light.set_brightness(self._previous)

    @property
    def description(self):
        return f"Set {self._light.name} to {self._level}%"


class SetTemperatureCommand(SmartHomeCommand):
    def __init__(self, thermostat: Thermostat, temp: float):
        self._thermostat = thermostat
        self._temp       = temp
        self._previous   = thermostat.temperature

    def execute(self):
        self._previous = self._thermostat.temperature
        self._thermostat.set_temperature(self._temp)

    def undo(self):
        self._thermostat.set_temperature(self._previous)

    @property
    def description(self):
        return f"Set thermostat to {self._temp}°C"


class PlayMusicCommand(SmartHomeCommand):
    def __init__(self, player: MusicPlayer, track: str, volume: int):
        self._player   = player
        self._track    = track
        self._volume   = volume
        self._was_playing = False

    def execute(self):
        self._was_playing = self._player.playing
        self._player.set_volume(self._volume)
        self._player.play(self._track)

    def undo(self):
        if not self._was_playing:
            self._player.stop()

    @property
    def description(self):
        return f"Play '{self._track}' at volume {self._volume}"


# ─────────────────────────────────────────
# Macro Command — groups commands as one
# ─────────────────────────────────────────
class MacroCommand(SmartHomeCommand):
    """Composite: execute/undo multiple commands as one atomic unit."""

    def __init__(self, name: str, commands: list[SmartHomeCommand]):
        self._name     = name
        self._commands = commands

    def execute(self):
        print(f"\n  🏠 Running scene: '{self._name}'")
        for cmd in self._commands:
            cmd.execute()

    def undo(self):
        print(f"\n  🏠 Reversing scene: '{self._name}'")
        for cmd in reversed(self._commands):  # reverse order on undo
            cmd.undo()

    @property
    def description(self):
        return f"Scene: {self._name}"


# ─────────────────────────────────────────
# Invoker — Smart Home Hub
# ─────────────────────────────────────────
class SmartHomeHub:
    def __init__(self):
        self._history: list[SmartHomeCommand] = []
        self._scheduled: list[SmartHomeCommand] = []

    def run(self, command: SmartHomeCommand) -> None:
        command.execute()
        self._history.append(command)
        print(f"  📝 Logged: {command.description}")

    def undo_last(self) -> None:
        if self._history:
            cmd = self._history.pop()
            print(f"\n↩️  Undoing: {cmd.description}")
            cmd.undo()

    def schedule(self, command: SmartHomeCommand) -> None:
        """Queue a command to run later."""
        self._scheduled.append(command)
        print(f"  ⏰ Scheduled: {command.description}")

    def run_scheduled(self) -> None:
        """Execute all scheduled commands."""
        print("\n🔔 Running scheduled tasks...")
        while self._scheduled:
            self.run(self._scheduled.pop(0))


# ─────────────────────────────────────────
# Client
# ─────────────────────────────────────────
hub         = SmartHomeHub()
living_light = Light("Living Room")
bedroom_light = Light("Bedroom")
thermostat  = Thermostat()
player      = MusicPlayer()

# Define "Movie Night" scene as a macro command
movie_night = MacroCommand("Movie Night", [
    SetBrightnessCommand(living_light,  20),
    SetBrightnessCommand(bedroom_light,  0),
    SetTemperatureCommand(thermostat,   22),
    PlayMusicCommand(player, "Inception OST", 40),
])

hub.run(movie_night)

print("\n--- Undoing Movie Night ---")
hub.undo_last()

# Schedule a "Good Morning" scene
print("\n--- Scheduling Morning Scene ---")
hub.schedule(SetBrightnessCommand(living_light, 100))
hub.schedule(SetTemperatureCommand(thermostat, 21))
hub.run_scheduled()
```

---

### Example 3: Task Queue System

```python
from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
import time

class TaskStatus(Enum):
    PENDING   = "pending"
    RUNNING   = "running"
    DONE      = "done"
    FAILED    = "failed"

# ─────────────────────────────────────────
# Command Interface
# ─────────────────────────────────────────
class Task(ABC):
    def __init__(self, name: str):
        self.name       = name
        self.status     = TaskStatus.PENDING
        self.created_at = datetime.now()
        self.retries    = 0
        self.max_retries = 3

    @abstractmethod
    def execute(self) -> bool:
        """Returns True on success, False on failure."""
        pass

    def undo(self) -> None:
        """Optional rollback logic."""
        pass

    def __repr__(self):
        return f"Task({self.name}, {self.status.value})"


# ─────────────────────────────────────────
# Concrete Tasks
# ─────────────────────────────────────────
class EmailTask(Task):
    def __init__(self, recipient: str, subject: str):
        super().__init__(f"Email→{recipient}")
        self.recipient = recipient
        self.subject   = subject

    def execute(self) -> bool:
        print(f"  📧 Sending email to {self.recipient}: '{self.subject}'")
        # Simulate work
        return True


class DatabaseBackupTask(Task):
    def __init__(self, db_name: str):
        super().__init__(f"Backup:{db_name}")
        self.db_name   = db_name
        self._backup_path: str | None = None

    def execute(self) -> bool:
        self._backup_path = f"/backups/{self.db_name}_{datetime.now().strftime('%Y%m%d')}.sql"
        print(f"  🗄️  Backing up '{self.db_name}' → {self._backup_path}")
        return True

    def undo(self) -> None:
        if self._backup_path:
            print(f"  🗑️  Deleting backup: {self._backup_path}")


class ReportGenerationTask(Task):
    def __init__(self, report_type: str):
        super().__init__(f"Report:{report_type}")
        self.report_type = report_type

    def execute(self) -> bool:
        print(f"  📊 Generating {self.report_type} report...")
        return True


# ─────────────────────────────────────────
# Invoker — Task Queue
# ─────────────────────────────────────────
class TaskQueue:
    def __init__(self):
        self._queue:     list[Task] = []
        self._completed: list[Task] = []
        self._failed:    list[Task] = []

    def enqueue(self, task: Task) -> None:
        self._queue.append(task)
        print(f"  ➕ Queued: {task.name}")

    def process_all(self) -> None:
        print(f"\n🚀 Processing {len(self._queue)} tasks...\n")
        while self._queue:
            task = self._queue.pop(0)
            self._run(task)

    def _run(self, task: Task) -> None:
        task.status = TaskStatus.RUNNING
        try:
            success = task.execute()
            if success:
                task.status = TaskStatus.DONE
                self._completed.append(task)
                print(f"  ✅ Done: {task.name}\n")
            else:
                self._handle_failure(task)
        except Exception as e:
            print(f"  ❌ Error in {task.name}: {e}")
            self._handle_failure(task)

    def _handle_failure(self, task: Task) -> None:
        task.retries += 1
        if task.retries < task.max_retries:
            print(f"  🔁 Retry {task.retries}/{task.max_retries}: {task.name}")
            self._queue.insert(0, task)   # re-queue at front
        else:
            task.status = TaskStatus.FAILED
            self._failed.append(task)
            print(f"  💀 Permanently failed: {task.name}")

    def summary(self) -> None:
        print(f"\n📋 Queue Summary:")
        print(f"  ✅ Completed : {len(self._completed)}")
        print(f"  ❌ Failed    : {len(self._failed)}")
        for t in self._failed:
            print(f"     • {t.name}")


# ─────────────────────────────────────────
# Client
# ─────────────────────────────────────────
queue = TaskQueue()

queue.enqueue(EmailTask("alice@example.com", "Monthly Report"))
queue.enqueue(DatabaseBackupTask("production_db"))
queue.enqueue(ReportGenerationTask("Q4 Sales"))
queue.enqueue(EmailTask("bob@example.com", "Backup Confirmation"))

queue.process_all()
queue.summary()
```

---

## ⚠️ Common Pitfalls

### ❌ Pitfall 1: Forgetting to Save State for Undo

```python
# ❌ WRONG — can't undo because previous state wasn't saved
class BadSetValueCommand(Command):
    def execute(self):
        self._obj.value = self._new_value  # old value is lost!

    def undo(self):
        pass  # 🤷 no idea what the old value was

# ✅ CORRECT — snapshot state before changing it
class GoodSetValueCommand(Command):
    def execute(self):
        self._prev_value = self._obj.value  # save FIRST
        self._obj.value  = self._new_value

    def undo(self):
        self._obj.value  = self._prev_value  # restore
```

### ❌ Pitfall 2: Command Doing Too Much (God Command)

```python
# ❌ WRONG — violates Single Responsibility
class GodCommand(Command):
    def execute(self):
        self._validate_user()
        self._send_email()
        self._update_db()
        self._log_audit()
        self._notify_slack()  # 5 things in one command!

# ✅ CORRECT — Macro Command delegates to focused commands
class OnboardUserCommand(MacroCommand):
    def __init__(self, user):
        super().__init__([
            ValidateUserCommand(user),
            SendWelcomeEmailCommand(user),
            CreateDatabaseRecordCommand(user),
            LogAuditCommand(user),
            NotifySlackCommand(user),
        ])
```

### ❌ Pitfall 3: Not Clearing Redo Stack on New Command

```python
# ❌ WRONG — redo stack becomes stale after new actions
class BadHistory:
    def execute(self, cmd):
        cmd.execute()
        self._undo_stack.append(cmd)
        # Missing: self._redo_stack.clear() ← leads to inconsistent state!

# ✅ CORRECT
class GoodHistory:
    def execute(self, cmd):
        cmd.execute()
        self._undo_stack.append(cmd)
        self._redo_stack.clear()  # always clear redo on new action
```

### ❌ Pitfall 4: Mutable Arguments in Command

```python
# ❌ WRONG — list mutated externally after command creation
class BadCommand(Command):
    def __init__(self, items: list):
        self._items = items  # stores reference, not a copy!

    def execute(self):
        process(self._items)  # items may have changed by now!

# ✅ CORRECT — snapshot at construction time
class GoodCommand(Command):
    def __init__(self, items: list):
        self._items = list(items)  # copy to isolate from external changes
```

---

## ✅ Best Practices

### 1. Snapshot State at `execute()`, Not at Construction

```python
class MoveCommand(Command):
    def execute(self):
        self._prev_pos = self._obj.position  # snapshot just before acting
        self._obj.move(self._new_pos)
```

### 2. Macro Commands for Atomic Operations

```python
class TransferFundsCommand(MacroCommand):
    def __init__(self, src, dst, amount):
        super().__init__([
            DebitCommand(src, amount),
            CreditCommand(dst, amount),
            LogTransactionCommand(src, dst, amount),
        ])
    # All three succeed or all three undo — atomically
```

### 3. Use a Command Factory for Complex Setup

```python
class CommandFactory:
    def __init__(self, document: Document):
        self._doc = document

    def insert(self, pos: int, text: str) -> InsertCommand:
        return InsertCommand(self._doc, pos, text)

    def delete(self, pos: int, length: int) -> DeleteCommand:
        return DeleteCommand(self._doc, pos, length)
```

### 4. Add `description` Property for Logging/UI

```python
class Command(ABC):
    @property
    def description(self) -> str:
        return self.__class__.__name__  # sensible default

class InsertCommand(Command):
    @property
    def description(self) -> str:
        return f"Insert '{self._text}' at pos {self._position}"
```

---

## 📊 Summary

| Aspect               | Detail                                                 |
|----------------------|--------------------------------------------------------|
| **Type**             | Behavioral                                             |
| **Intent**           | Encapsulate a request as an object                     |
| **Key Benefit**      | Undo/Redo, queuing, logging, macro operations          |
| **Participants**     | Client, Invoker, Command, ConcreteCommand, Receiver    |
| **Python Use Cases** | Task queues (Celery tasks), GUI actions, DB migrations |

---

## ✅ Command Pattern Checklist

- Does each command encapsulate ONE operation?
- Is state snapshot taken in execute() before modifying?
- Does undo() perfectly reverse execute()?
- Does the invoker know NOTHING about what the command does?
- Is the redo stack cleared when a new command is executed?
- Are complex operations broken into Macro Commands?
- Do commands have a description property for logging?


---

## 💡 Key Takeaways

1. **A request becomes an object** — storable, transmittable, reversible
2. **Invoker is fully decoupled** from what the command actually does
3. **Undo/Redo is built-in** by snapshotting state before execution
4. **Macro Command** (composite) enables atomic multi-step operations
5. **Real-world Python** — Celery tasks, Django migrations, and GUI frameworks all use this pattern
