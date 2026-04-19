# 🧠 **Template Method Pattern**

---

## 📋 Table of Contents
- [What is Template Method Pattern?](#-what-is-template-method-pattern)
  - [Key Characteristics](#-key-characteristics)
  - [The Problem It Solves](#-the-problem-it-solves)
  - [Real-World Analogy](#-real-world-analogy)
  - [Visual Representation](#-visual-representation)
- [When to Use](#-when-to-use)
- [When NOT to Use](#-when-not-to-use)
- [Basic Implementation](#-basic-implementation)
- [Real-World Examples](#-real-world-examples)
  - [Example 1: Data Processing Pipeline](#example-1-data-processing-pipeline)
  - [Example 2: Game AI Turn System](#example-2-game-ai-turn-system)
  - [Example 3: Report Generator](#example-3-report-generator)
- [Common Pitfalls](#-common-pitfalls)
- [Best Practices](#-best-practices)
- [Summary](#-summary)
- [Template Method Pattern Checklist](#-template-method-pattern-checklist)
- [Key Takeaways](#-key-takeaways)

---

## 🔷 What is Template Method Pattern?

**Template Method Pattern** is a behavioral design pattern that defines the **skeleton of an algorithm in a base class**, deferring some steps to subclasses. Subclasses can override specific steps without changing the algorithm's overall structure.

The base class says: **"Here is the recipe — you can customize certain steps, but the order never changes."**

---

### 🔑 Key Characteristics

| Characteristic          | Description                                                         |
|-------------------------|---------------------------------------------------------------------|
| **Fixed Skeleton**      | The algorithm's structure is locked in the base class               |
| **Deferred Steps**      | Subclasses override only the parts that vary                        |
| **Hollywood Principle** | "Don't call us, we'll call you" — base class calls subclass methods |
| **Code Reuse**          | Common logic lives once in the base class                           |
| **Hooks**               | Optional override points with default (often empty) implementations |

---

### 🔥 The Problem It Solves

Without Template Method, the same algorithmic skeleton gets duplicated across subclasses:

```python
# ❌ WITHOUT Template Method — duplicated skeleton everywhere
class CSVReport:
    def generate(self):
        self._connect_to_db()       # identical in every report
        self._validate_params()     # identical in every report
        data = self._fetch_data()   # identical in every report
        # format differs
        output = self._to_csv(data)
        self._send_email(output)    # identical in every report
        self._log_completion()      # identical in every report

class PDFReport:
    def generate(self):
        self._connect_to_db()       # copy-paste!
        self._validate_params()     # copy-paste!
        data = self._fetch_data()   # copy-paste!
        # only this line differs:
        output = self._to_pdf(data)
        self._send_email(output)    # copy-paste!
        self._log_completion()      # copy-paste!
# Any change to the skeleton must be made in EVERY subclass!
```

With Template Method:

```python
# ✅ WITH Template Method — skeleton lives once, only variations differ
class ReportGenerator:
    def generate(self):              # ← template method: never overridden
        self._connect_to_db()
        self._validate_params()
        data = self._fetch_data()
        output = self._format(data)  # ← abstract: subclasses override this
        self._send_email(output)
        self._log_completion()

class CSVReport(ReportGenerator):
    def _format(self, data): ...     # only this changes

class PDFReport(ReportGenerator):
    def _format(self, data): ...     # only this changes
```

---

### 🌍 Real-World Analogy

Think of a **franchise restaurant** like McDonald's:

```
Corporate (Base Class): defines the process
  1. Take order      ← fixed step
  2. Prepare patty   ← fixed step
  3. Add toppings    ← *** customizable per franchise ***
  4. Wrap/Package    ← fixed step
  5. Serve customer  ← fixed step

Tokyo McDonald's:   adds teriyaki sauce  (override step 3)
India McDonald's:   adds aloo tikki      (override step 3)
US McDonald's:      adds standard toppings (default step 3)
```

The **process never changes** — only specific steps vary by location.

---

### 🖼️ Visual Representation

```
┌──────────────────────────────────────────────┐
│          AbstractClass (Base)                │
│                                              │
│  template_method()  ← FINAL — never override │
│    ├── step_one()   ← concrete (shared)      │
│    ├── step_two()   ← abstract (must override│
│    ├── step_three() ← hook (optional)        │
│    └── step_four()  ← concrete (shared)      │
└──────────────────────┬───────────────────────┘
                       │ inherits
          ┌────────────┴────────────┐
          ▼                         ▼
┌──────────────────┐     ┌──────────────────┐
│  ConcreteClassA  │     │  ConcreteClassB  │
│                  │     │                  │
│  step_two()  ✓   │     │  step_two()  ✓   │
│  step_three() ✓  │     │  (uses hook      │
│  (overrides hook)│     │   default)       │
└──────────────────┘     └──────────────────┘
```

---

### 🔀 Participants

| Role                  | Responsibility                                                      |
|-----------------------|---------------------------------------------------------------------|
| **AbstractClass**     | Defines `template_method()` and all step signatures                 |
| **template_method()** | The fixed skeleton — calls steps in order; should not be overridden |
| **Abstract steps**    | Must be overridden by subclasses — the variable parts               |
| **Concrete steps**    | Implemented in base class — shared by all subclasses                |
| **Hooks**             | Optional override points with default (often empty) implementations |
| **ConcreteClass**     | Overrides abstract steps (and optionally hooks)                     |

---

## ✅ When to Use

| Scenario                                                             | Why It Fits                             |
|----------------------------------------------------------------------|-----------------------------------------|
| Multiple classes share the **same algorithm skeleton**               | Define it once in base class            |
| Only **specific steps** vary between subclasses                      | Override only those steps               |
| Want to **enforce invariant steps** that must always run             | Lock them in template method            |
| Need **optional extension points** (hooks)                           | Subclasses override only what they need |
| **Framework design** — library defines structure, users fill in gaps | Classic Template Method use case        |

---

## ❌ When NOT to Use

- When the algorithm varies **too much** between subclasses — Strategy is more flexible
- When you need to **swap algorithms at runtime** — use Strategy instead (inheritance is static)
- When subclasses need to **reorder the steps** — Template Method locks step order
- When the hierarchy gets **too deep** — deep inheritance chains become unmaintainable

---

## 🏗️ Basic Implementation

### Classic Structure

```python
from abc import ABC, abstractmethod

# ─────────────────────────────────────────
# Abstract Class
# ─────────────────────────────────────────
class DataMiner(ABC):

    def mine(self) -> None:
        """
        Template Method — defines the skeleton.
        Marked as final convention (use __init_subclass__ to enforce if needed).
        """
        raw  = self._extract()
        data = self._parse(raw)
        self._analyze(data)
        self._hook_before_report()          # optional hook
        self._send_report(data)

    # ── Abstract steps — subclasses MUST override ──
    @abstractmethod
    def _extract(self) -> str:
        """Pull raw data from the source."""
        pass

    @abstractmethod
    def _parse(self, raw: str) -> list:
        """Parse raw data into structured form."""
        pass

    # ── Concrete step — shared by all subclasses ──
    def _analyze(self, data: list) -> None:
        print(f"  📊 Analyzing {len(data)} records...")

    def _send_report(self, data: list) -> None:
        print(f"  📧 Sending report with {len(data)} records.")

    # ── Hook — optional, empty default ──
    def _hook_before_report(self) -> None:
        """Override this to add pre-report logic. Default: do nothing."""
        pass


# ─────────────────────────────────────────
# Concrete Classes
# ─────────────────────────────────────────
class CSVDataMiner(DataMiner):
  
    def __init__(self, filepath: str):
        self._filepath = filepath

    def _extract(self) -> str:
        print(f"  📂 Reading CSV: {self._filepath}")
        # Simulated CSV content
        return "name,age,city\nAlice,30,NY\nBob,25,LA\nCarol,35,SF"

    def _parse(self, raw: str) -> list:
        lines  = raw.strip().split("\n")
        header = lines[0].split(",")
        rows   = [dict(zip(header, line.split(","))) for line in lines[1:]]
        print(f"  🔍 Parsed {len(rows)} CSV rows")
        return rows

    def _hook_before_report(self) -> None:
        print("  💾 Caching CSV results to disk...")   # CSV-specific hook


class APIDataMiner(DataMiner):
  
    def __init__(self, endpoint: str):
        self._endpoint = endpoint

    def _extract(self) -> str:
        print(f"  🌐 Fetching API: {self._endpoint}")
        # Simulated JSON response
        return '[{"id":1,"user":"Alice"},{"id":2,"user":"Bob"}]'

    def _parse(self, raw: str) -> list:
        import json
        data = json.loads(raw)
        print(f"  🔍 Parsed {len(data)} API records")
        return data
    # No hook override — uses empty default


# ─────────────────────────────────────────
# Client
# ─────────────────────────────────────────
print("=== CSV Mining ===")
CSVDataMiner("sales_2025.csv").mine()

print("\n=== API Mining ===")
APIDataMiner("https://api.example.com/users").mine()
```

---

## 🌍 Real-World Examples

### Example 1: Data Processing Pipeline

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any
from datetime import datetime

@dataclass
class PipelineResult:
    source:      str
    records_in:  int
    records_out: int
    errors:      list[str]     = field(default_factory=list)
    warnings:    list[str]     = field(default_factory=list)
    metadata:    dict[str, Any] = field(default_factory=dict)
    started_at:  datetime      = field(default_factory=datetime.now)
    finished_at: datetime | None = None

    @property
    def duration_ms(self) -> float:
        if self.finished_at:
            return (self.finished_at - self.started_at).total_seconds() * 1000
        return 0.0

    @property
    def success_rate(self) -> float:
        if self.records_in == 0:
            return 0.0
        return self.records_out / self.records_in * 100

    def summary(self) -> None:
        status = "✅" if not self.errors else "⚠️"
        print(f"\n  {status} Pipeline Summary [{self.source}]")
        print(f"     In       : {self.records_in}")
        print(f"     Out      : {self.records_out}")
        print(f"     Success  : {self.success_rate:.1f}%")
        print(f"     Duration : {self.duration_ms:.1f}ms")
        if self.errors:
            print(f"     Errors   : {len(self.errors)}")
            for e in self.errors[:3]:
                print(f"       ✗ {e}")
        if self.warnings:
            print(f"     Warnings : {len(self.warnings)}")


# ─────────────────────────────────────────
# Abstract Pipeline
# ─────────────────────────────────────────
class DataPipeline(ABC):
    """
    Template Method defines the ETL pipeline skeleton:
    Extract → Validate → Transform → Load → Notify
    """

    def __init__(self, name: str):
        self._name   = name
        self._result: PipelineResult | None = None

    def run(self) -> PipelineResult:
        """Template Method — the fixed ETL skeleton."""
        print(f"\n{'='*50}")
        print(f"  🚀 Pipeline: {self._name}")
        print(f"{'='*50}")

        self._result = PipelineResult(source=self._name, records_in=0, records_out=0)

        try:
            # Step 1: Extract
            print("\n  [1/5] Extracting...")
            raw_data = self._extract()
            self._result.records_in = len(raw_data)
            print(f"        Extracted {len(raw_data)} raw records")

            # Step 2: Validate — hook, default accepts all
            print("\n  [2/5] Validating...")
            valid_data = self._validate(raw_data)
            rejected   = len(raw_data) - len(valid_data)
            if rejected:
                self._result.warnings.append(
                    f"{rejected} records failed validation"
                )
                print(f"        ⚠️  {rejected} records rejected")
            print(f"        {len(valid_data)} records passed validation")

            # Step 3: Transform — abstract, must override
            print("\n  [3/5] Transforming...")
            transformed = self._transform(valid_data)
            print(f"        {len(transformed)} records transformed")

            # Step 4: Enrich — hook, default passes through
            print("\n  [4/5] Enriching...")
            enriched = self._enrich(transformed)
            print(f"        {len(enriched)} records after enrichment")

            # Step 5: Load — abstract, must override
            print("\n  [5/5] Loading...")
            loaded = self._load(enriched)
            self._result.records_out = loaded

            # Post-run hook
            self._on_success(self._result)

        except Exception as e:
            error_msg = f"{type(e).__name__}: {e}"
            self._result.errors.append(error_msg)
            print(f"\n  ❌ Pipeline failed: {error_msg}")
            self._on_failure(self._result, e)

        finally:
            self._result.finished_at = datetime.now()
            self._on_complete(self._result)

        return self._result

    # ── Abstract steps — MUST override ────────────────
    @abstractmethod
    def _extract(self) -> list[dict]:
        """Pull raw data from the source."""
        pass

    @abstractmethod
    def _transform(self, data: list[dict]) -> list[dict]:
        """Transform records into target shape."""
        pass

    @abstractmethod
    def _load(self, data: list[dict]) -> int:
        """Write records to destination. Returns count loaded."""
        pass

    # ── Hook steps — OPTIONAL override ────────────────
    def _validate(self, data: list[dict]) -> list[dict]:
        """Default: accept all records. Override to add validation rules."""
        return data

    def _enrich(self, data: list[dict]) -> list[dict]:
        """Default: pass-through. Override to add derived fields."""
        return data

    def _on_success(self, result: PipelineResult) -> None:
        """Called after successful load."""
        pass

    def _on_failure(self, result: PipelineResult, error: Exception) -> None:
        """Called when pipeline raises an exception."""
        pass

    def _on_complete(self, result: PipelineResult) -> None:
        """Always called — success or failure. Default: print summary."""
        result.summary()


# ─────────────────────────────────────────
# Concrete Pipeline: User ETL
# ─────────────────────────────────────────
class UserSyncPipeline(DataPipeline):
    """
    Syncs users from a legacy CSV export to the new user database.
    Overrides: extract, transform, load.
    Adds: validation, enrichment hooks.
    """

    def __init__(self, csv_path: str, target_db: str):
        super().__init__("UserSync")
        self._csv_path = csv_path
        self._target   = target_db
        self._loaded_users: list[dict] = []

    def _extract(self) -> list[dict]:
        # Simulate reading a CSV file
        return [
            {"raw_name": "alice smith",  "raw_email": "ALICE@EXAMPLE.COM",
             "raw_age": "30",  "raw_country": "US", "active": "1"},
            {"raw_name": "bob jones",    "raw_email": "bob@example.com",
             "raw_age": "25",  "raw_country": "GB", "active": "1"},
            {"raw_name": "carol white",  "raw_email": "carol@",
             "raw_age": "35",  "raw_country": "CA", "active": "0"},  # invalid email
            {"raw_name": "",             "raw_email": "noname@example.com",
             "raw_age": "28",  "raw_country": "AU", "active": "1"},  # missing name
            {"raw_name": "dave brown",   "raw_email": "dave@example.com",
             "raw_age": "abc", "raw_country": "US", "active": "1"},  # bad age
        ]

    def _validate(self, data: list[dict]) -> list[dict]:
        valid = []
        for rec in data:
            # Name required
            if not rec.get("raw_name", "").strip():
                self._result.errors.append(f"Missing name: {rec}")
                continue
            # Basic email check
            email = rec.get("raw_email", "")
            if "@" not in email or "." not in email.split("@")[-1]:
                self._result.errors.append(f"Invalid email: {email}")
                continue
            valid.append(rec)
        return valid

    def _transform(self, data: list[dict]) -> list[dict]:
        transformed = []
        for rec in data:
            try:
                transformed.append({
                    "name":       rec["raw_name"].title(),
                    "email":      rec["raw_email"].lower().strip(),
                    "age":        int(rec["raw_age"]),
                    "country":    rec["raw_country"].upper(),
                    "is_active":  rec["active"] == "1",
                })
            except (ValueError, KeyError) as e:
                self._result.warnings.append(
                    f"Transform error for {rec.get('raw_name')}: {e}"
                )
        return transformed

    def _enrich(self, data: list[dict]) -> list[dict]:
        """Add derived fields: full_label, created_at."""
        for rec in data:
            rec["full_label"]  = f"{rec['name']} <{rec['email']}>"
            rec["synced_at"]   = datetime.now().isoformat()
            rec["source"]      = "legacy_csv"
        return data

    def _load(self, data: list[dict]) -> int:
        print(f"        Writing to {self._target}...")
        self._loaded_users = data
        for rec in data:
            print(f"        ✓ {rec['full_label']} | "
                  f"country={rec['country']} | active={rec['is_active']}")
        return len(data)

    def _on_success(self, result: PipelineResult) -> None:
        print(f"\n  🎉 Sync complete — {result.records_out} users in {self._target}")

    def _on_failure(self, result: PipelineResult, error: Exception) -> None:
        print(f"  🔔 Alert: UserSync failed — notifying ops team")


# ─────────────────────────────────────────
# Concrete Pipeline: Sales Aggregation
# ─────────────────────────────────────────
class SalesAggregationPipeline(DataPipeline):
    """
    Aggregates daily sales records into regional summaries.
    Only overrides the 3 abstract steps — uses all default hooks.
    """

    def __init__(self):
        super().__init__("SalesAggregation")

    def _extract(self) -> list[dict]:
        # Simulate raw sales transaction records
        return [
            {"txn": "T001", "region": "US", "amount": 149.99, "product": "Book"},
            {"txn": "T002", "region": "EU", "amount": 89.00,  "product": "Keyboard"},
            {"txn": "T003", "region": "US", "amount": 29.99,  "product": "USB Hub"},
            {"txn": "T004", "region": "CA", "amount": 299.00, "product": "Desk"},
            {"txn": "T005", "region": "US", "amount": 69.00,  "product": "Webcam"},
            {"txn": "T006", "region": "EU", "amount": 39.99,  "product": "Book"},
        ]

    def _transform(self, data: list[dict]) -> list[dict]:
        # Aggregate by region
        aggregated: dict[str, dict] = {}
        for rec in data:
            region = rec["region"]
            if region not in aggregated:
                aggregated[region] = {
                    "region":       region,
                    "total_revenue": 0.0,
                    "order_count":  0,
                    "products":     set(),
                }
            aggregated[region]["total_revenue"] += rec["amount"]
            aggregated[region]["order_count"]   += 1
            aggregated[region]["products"].add(rec["product"])

        result = []
        for agg in aggregated.values():
            agg["products"]       = list(agg["products"])
            agg["avg_order_value"] = agg["total_revenue"] / agg["order_count"]
            result.append(agg)

        return result

    def _load(self, data: list[dict]) -> int:
        print("        Writing regional summaries...")
        for agg in data:
            print(f"        📊 {agg['region']}: "
                  f"${agg['total_revenue']:.2f} revenue | "
                  f"{agg['order_count']} orders | "
                  f"avg ${agg['avg_order_value']:.2f}")
        return len(data)


# ─────────────────────────────────────────
# Client
# ─────────────────────────────────────────
UserSyncPipeline("legacy_users.csv", "users_db").run()
SalesAggregationPipeline().run()
```

---

### Example 2: Game AI Turn System

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import random

@dataclass
class GameState:
    turn:       int              = 0
    player_hp:  int              = 100
    enemy_hp:   int              = 100
    player_mp:  int              = 50
    enemy_mp:   int              = 50
    log:        list[str]        = field(default_factory=list)
    status_effects: list[str]    = field(default_factory=list)

    def add_log(self, msg: str) -> None:
        self.log.append(f"  [Turn {self.turn}] {msg}")
        print(f"  [T{self.turn}] {msg}")

    def is_over(self) -> bool:
        return self.player_hp <= 0 or self.enemy_hp <= 0


# ─────────────────────────────────────────
# Abstract AI Turn
# ─────────────────────────────────────────
class EnemyAI(ABC):
    """
    Template Method: defines the enemy's turn skeleton.
    Each AI archetype overrides specific decision steps.
    """

    def __init__(self, name: str):
        self.name = name

    def take_turn(self, state: GameState) -> None:
        """Template Method — the fixed turn sequence."""
        state.add_log(f"--- {self.name}'s turn ---")

        # Step 1: Assess situation
        threat_level = self._assess_threat(state)

        # Step 2: Choose action based on assessment
        action = self._choose_action(state, threat_level)
        state.add_log(f"{self.name} decides to: {action}")

        # Step 3: Execute action
        self._execute_action(action, state)

        # Step 4: React to outcome — hook
        self._post_action_hook(state)

        # Step 5: Apply end-of-turn effects — concrete, shared
        self._apply_end_of_turn(state)

    # ── Abstract — MUST override ───────────────────────
    @abstractmethod
    def _choose_action(self, state: GameState, threat: str) -> str:
        """Decide what action to take this turn."""
        pass

    @abstractmethod
    def _execute_action(self, action: str, state: GameState) -> None:
        """Carry out the chosen action."""
        pass

    # ── Concrete — shared logic ────────────────────────
    def _assess_threat(self, state: GameState) -> str:
        hp_ratio = state.player_hp / 100
        if hp_ratio > 0.7:
            threat = "low"
        elif hp_ratio > 0.4:
            threat = "medium"
        else:
            threat = "high"
        state.add_log(f"{self.name} assesses threat: {threat} "
                      f"(player HP: {state.player_hp})")
        return threat

    def _apply_end_of_turn(self, state: GameState) -> None:
        # Restore 5 MP each turn — applies to all AI types
        state.enemy_mp = min(50, state.enemy_mp + 5)

    # ── Hook — OPTIONAL override ───────────────────────
    def _post_action_hook(self, state: GameState) -> None:
        """Override to add post-action reactions. Default: nothing."""
        pass


# ─────────────────────────────────────────
# Concrete AI: Aggressive Warrior
# ─────────────────────────────────────────
class AggressiveWarriorAI(EnemyAI):
  
    def __init__(self):
        super().__init__("Warrior")
        self._rage_stacks = 0

    def _choose_action(self, state: GameState, threat: str) -> str:
        # Always aggressive — escalates with low HP
        if state.enemy_hp < 30:
            return "berserker_rage"
        if threat == "high":
            return "heavy_strike"
        return "normal_attack"

    def _execute_action(self, action: str, state: GameState) -> None:
        if action == "normal_attack":
            dmg = random.randint(10, 18)
            state.player_hp -= dmg
            state.add_log(f"Warrior strikes for {dmg} damage! "
                          f"(Player HP: {state.player_hp})")

        elif action == "heavy_strike":
            dmg = random.randint(20, 35)
            state.player_hp -= dmg
            state.add_log(f"⚔️  Warrior HEAVY STRIKES for {dmg}! "
                          f"(Player HP: {state.player_hp})")

        elif action == "berserker_rage":
            self._rage_stacks += 1
            dmg = random.randint(15, 25) + self._rage_stacks * 5
            state.player_hp -= dmg
            state.add_log(f"🔥 Warrior BERSERKS (stack {self._rage_stacks}) "
                          f"for {dmg}! (Player HP: {state.player_hp})")

    def _post_action_hook(self, state: GameState) -> None:
        # Warrior taunts when player HP is low
        if state.player_hp < 30:
            state.add_log("Warrior: 'You cannot defeat me!'")


# ─────────────────────────────────────────
# Concrete AI: Cautious Mage
# ─────────────────────────────────────────
class CautiousMageAI(EnemyAI):
  
    def __init__(self):
        super().__init__("Mage")
        self._shields_up = False

    def _choose_action(self, state: GameState, threat: str) -> str:
        # Prioritize survival — cast shield when hurt
        if state.enemy_hp < 50 and not self._shields_up:
            return "magic_shield"
        # Use powerful spell when MP available
        if state.enemy_mp >= 20 and threat != "low":
            return "fireball"
        # Save MP with basic attack
        return "magic_missile"

    def _execute_action(self, action: str, state: GameState) -> None:
        if action == "magic_missile":
            dmg = random.randint(8, 14)
            state.player_hp -= dmg
            state.add_log(f"✨ Mage fires magic missile for {dmg}. "
                          f"(Player HP: {state.player_hp})")

        elif action == "fireball":
            dmg = random.randint(25, 40)
            state.enemy_mp -= 20
            state.player_hp -= dmg
            state.add_log(f"🔥 Mage casts FIREBALL for {dmg}! "
                          f"MP: {state.enemy_mp} | Player HP: {state.player_hp}")

        elif action == "magic_shield":
            self._shields_up = True
            block = 15
            state.enemy_hp = min(100, state.enemy_hp + block)
            state.enemy_mp -= 10
            state.add_log(f"🛡️  Mage raises shield (+{block} HP). "
                          f"Enemy HP: {state.enemy_hp}")

    def _post_action_hook(self, state: GameState) -> None:
        # Mage drops shield when fully healed
        if self._shields_up and state.enemy_hp >= 80:
            self._shields_up = False
            state.add_log("Mage's shield fades.")


# ─────────────────────────────────────────
# Concrete AI: Trickster Rogue
# ─────────────────────────────────────────
class TricksterRogueAI(EnemyAI):
  
    def __init__(self):
        super().__init__("Rogue")
        self._is_stealthed = False
        self._poison_turns = 0

    def _choose_action(self, state: GameState, threat: str) -> str:
        if not self._is_stealthed and random.random() < 0.3:
            return "vanish"
        if self._is_stealthed:
            return "backstab"
        if self._poison_turns == 0:
            return "poison_dagger"
        return "quick_strike"

    def _execute_action(self, action: str, state: GameState) -> None:
        if action == "vanish":
            self._is_stealthed = True
            state.add_log("🌑 Rogue vanishes into the shadows!")

        elif action == "backstab":
            dmg = random.randint(30, 50)   # massive bonus from stealth
            self._is_stealthed = False
            state.player_hp -= dmg
            state.add_log(f"🗡️  Rogue BACKSTABS from stealth for {dmg}! "
                          f"(Player HP: {state.player_hp})")

        elif action == "poison_dagger":
            dmg = random.randint(5, 10)
            self._poison_turns = 3
            state.player_hp -= dmg
            state.status_effects.append("poisoned")
            state.add_log(f"☠️  Rogue poisons! {dmg} dmg + 3 turns of poison. "
                          f"(Player HP: {state.player_hp})")

        elif action == "quick_strike":
            dmg = random.randint(8, 15)
            state.player_hp -= dmg
            state.add_log(f"⚡ Rogue quick-strikes for {dmg}. "
                          f"(Player HP: {state.player_hp})")

    def _post_action_hook(self, state: GameState) -> None:
        # Apply poison damage at end of turn
        if self._poison_turns > 0 and "poisoned" in state.status_effects:
            poison_dmg = 8
            state.player_hp -= poison_dmg
            self._poison_turns -= 1
            state.add_log(f"💚 Poison ticks {poison_dmg} dmg. "
                          f"Turns left: {self._poison_turns}. "
                          f"(Player HP: {state.player_hp})")
            if self._poison_turns == 0:
                state.status_effects.remove("poisoned")
                state.add_log("Poison has worn off.")


# ─────────────────────────────────────────
# Client: Battle Simulation
# ─────────────────────────────────────────
def simulate_battle(ai: EnemyAI, turns: int = 5) -> GameState:
    state = GameState()
    print(f"\n{'='*55}")
    print(f"  ⚔️  Battle vs {ai.name}")
    print(f"{'='*55}")

    for t in range(1, turns + 1):
        state.turn = t
        if state.is_over():
            break
        ai.take_turn(state)

    print(f"\n  Battle Result — Player HP: {state.player_hp} | "
          f"Enemy HP: {state.enemy_hp}")
    return state


random.seed(42)
simulate_battle(AggressiveWarriorAI(), turns=4)
simulate_battle(CautiousMageAI(),      turns=4)
simulate_battle(TricksterRogueAI(),    turns=4)
```

---

### Example 3: Report Generator

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any
from datetime import datetime

@dataclass
class ReportData:
    title:     str
    sections:  list[dict[str, Any]] = field(default_factory=list)
    generated: datetime             = field(default_factory=datetime.now)
    metadata:  dict[str, Any]       = field(default_factory=dict)

    def add_section(self, heading: str, content: Any) -> None:
        self.sections.append({"heading": heading, "content": content})


# ─────────────────────────────────────────
# Abstract Report Generator
# ─────────────────────────────────────────
class ReportGenerator(ABC):
    """
    Template Method: generate() defines the full report lifecycle.
    Subclasses control formatting; base controls structure.
    """

    def __init__(self, title: str):
        self._title  = title
        self._report = ReportData(title=title)

    def generate(self) -> str:
        """Template Method."""

        # Step 1: Collect data
        self._collect_data(self._report)

        # Step 2: Build document
        parts = []
        parts.append(self._render_header(self._report))
        parts.append(self._render_toc(self._report))       # hook

        for section in self._report.sections:
            parts.append(
                self._render_section(section["heading"], section["content"])
            )

        parts.append(self._render_footer(self._report))    # hook

        output = self._join(parts)

        # Step 3: Post-process — hook
        output = self._post_process(output)

        return output

    # ── Abstract — MUST override ──────────────────────
    @abstractmethod
    def _collect_data(self, report: ReportData) -> None:
        """Populate report.sections with content."""
        pass

    @abstractmethod
    def _render_header(self, report: ReportData) -> str:
        pass

    @abstractmethod
    def _render_section(self, heading: str, content: Any) -> str:
        pass

    # ── Concrete shared ───────────────────────────────
    def _join(self, parts: list[str]) -> str:
        return "\n".join(p for p in parts if p)

    # ── Hooks — optional override ─────────────────────
    def _render_toc(self, report: ReportData) -> str:
        return ""   # default: no table of contents

    def _render_footer(self, report: ReportData) -> str:
        return ""   # default: no footer

    def _post_process(self, output: str) -> str:
        return output   # default: pass-through


# ─────────────────────────────────────────
# Concrete: Markdown Report
# ─────────────────────────────────────────
class MarkdownReportGenerator(ReportGenerator):

    def _collect_data(self, report: ReportData) -> None:
        report.add_section("Executive Summary",
            "Q4 revenue exceeded targets by 12%. All regions grew YoY.")
        report.add_section("Regional Breakdown", {
            "US": {"revenue": 450_000, "growth": "15%"},
            "EU": {"revenue": 210_000, "growth": "8%"},
            "CA": {"revenue":  89_000, "growth": "11%"},
        })
        report.add_section("Top Products", [
            {"name": "Python Book",    "units": 1250, "revenue": 62_450},
            {"name": "Mechanical KB",  "units":  890, "revenue": 79_210},
            {"name": "Standing Desk",  "units":  320, "revenue": 95_680},
        ])
        report.add_section("Action Items", [
            "Expand EU warehouse capacity",
            "Launch loyalty programme Q1",
            "Hire 3 engineers for platform team",
        ])

    def _render_header(self, report: ReportData) -> str:
        ts = report.generated.strftime("%B %d, %Y")
        return f"# {report.title}\n\n*Generated: {ts}*\n"

    def _render_toc(self, report: ReportData) -> str:
        lines = ["## Table of Contents\n"]
        for i, sec in enumerate(report.sections, 1):
            slug = sec["heading"].lower().replace(" ", "-")
            lines.append(f"{i}. [{sec['heading']}](#{slug})")
        return "\n".join(lines) + "\n"

    def _render_section(self, heading: str, content: Any) -> str:
        lines = [f"## {heading}\n"]
        if isinstance(content, str):
            lines.append(content)
        elif isinstance(content, dict):
            for k, v in content.items():
                if isinstance(v, dict):
                    kv = " | ".join(f"{dk}: {dv}" for dk, dv in v.items())
                    lines.append(f"- **{k}**: {kv}")
                else:
                    lines.append(f"- **{k}**: {v}")
        elif isinstance(content, list):
            for item in content:
                if isinstance(item, dict):
                    row = " | ".join(f"{k}: {v}" for k, v in item.items())
                    lines.append(f"- {row}")
                else:
                    lines.append(f"- {item}")
        return "\n".join(lines) + "\n"

    def _render_footer(self, report: ReportData) -> str:
        return f"\n---\n*Confidential — {report.generated.year}*"


# ─────────────────────────────────────────
# Concrete: HTML Report
# ─────────────────────────────────────────
class HTMLReportGenerator(ReportGenerator):

    def _collect_data(self, report: ReportData) -> None:
        # Same data as Markdown — shared through base class
        report.add_section("Summary",
            "Strong performance across all metrics this quarter.")
        report.add_section("KPIs", {
            "Revenue":      "$749,000",
            "New Customers": "1,340",
            "Churn Rate":   "2.1%",
            "NPS Score":    "72",
        })
        report.add_section("Recommendations", [
            "Invest in performance marketing",
            "Reduce time-to-close in sales pipeline",
        ])

    def _render_header(self, report: ReportData) -> str:
        ts = report.generated.strftime("%B %d, %Y")
        return (
            f"<!DOCTYPE html><html><head>"
            f"<title>{report.title}</title>"
            f"<style>body{{font-family:sans-serif;max-width:800px;margin:auto}}"
            f"h1{{color:#2c3e50}}h2{{color:#34495e;border-bottom:1px solid #eee}}"
            f"table{{border-collapse:collapse;width:100%}}"
            f"td,th{{border:1px solid #ddd;padding:8px}}</style></head><body>"
            f"<h1>{report.title}</h1><p><em>{ts}</em></p>"
        )

    def _render_section(self, heading: str, content: Any) -> str:
        html = [f"<h2>{heading}</h2>"]
        if isinstance(content, str):
            html.append(f"<p>{content}</p>")
        elif isinstance(content, dict):
            html.append("<table><tr><th>Key</th><th>Value</th></tr>")
            for k, v in content.items():
                html.append(f"<tr><td><strong>{k}</strong></td><td>{v}</td></tr>")
            html.append("</table>")
        elif isinstance(content, list):
            html.append("<ul>")
            for item in content:
                if isinstance(item, dict):
                    row = ", ".join(f"<strong>{k}</strong>: {v}"
                                    for k, v in item.items())
                    html.append(f"<li>{row}</li>")
                else:
                    html.append(f"<li>{item}</li>")
            html.append("</ul>")
        return "\n".join(html)

    def _render_footer(self, report: ReportData) -> str:
        return (f"<hr><footer><small>Confidential — "
                f"{report.generated.year}</small></footer></body></html>")

    def _post_process(self, output: str) -> str:
        # Minify: strip newlines for compact HTML
        return output.replace("\n", "")


# ─────────────────────────────────────────
# Client
# ─────────────────────────────────────────
print("=== Markdown Report ===\n")
md_output = MarkdownReportGenerator("Q4 2025 Sales Report").generate()
print(md_output)

print("\n=== HTML Report (first 300 chars) ===\n")
html_output = HTMLReportGenerator("Q4 2025 KPI Dashboard").generate()
print(html_output[:300] + "...")
print(f"\n(Total HTML size: {len(html_output)} chars)")
```

---

## ⚠️ Common Pitfalls

### ❌ Pitfall 1: Overriding the Template Method Itself

```python
from abc import ABC

# ❌ WRONG — subclass overrides the skeleton, destroying the invariant
class BadReport(ReportGenerator):
    def generate(self) -> str:   # overrides template method!
        # skips validation, footer, logging — breaks the contract
        return self._render_header(self._report)

# ✅ CORRECT — mark template method final (Python convention: document + trust)
class ReportGenerator(ABC):
    def generate(self) -> str:
        """
        Template Method. Do NOT override in subclasses.
        Override _collect_data, _render_section, etc. instead.
        """
        ...

    # In Python, enforce with __init_subclass__ if truly needed:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if "generate" in cls.__dict__:
            raise TypeError(
                f"{cls.__name__} must not override 'generate()' — "
                f"it is the template method."
            )
```

### ❌ Pitfall 2: Too Many Abstract Steps — Forces Unnecessary Overrides

```python
from abc import ABC

# ❌ WRONG — 8 abstract methods forces every subclass to implement all 8
from abc import abstractmethod

class OverlyAbstractPipeline(ABC):
    @abstractmethod
    def _connect(self): pass
    @abstractmethod
    def _authenticate(self): pass
    @abstractmethod
    def _fetch(self): pass
    @abstractmethod
    def _deserialize(self): pass
    @abstractmethod
    def _validate(self): pass
    @abstractmethod
    def _map(self): pass
    @abstractmethod
    def _filter(self): pass
    @abstractmethod
    def _store(self): pass
    # Simple subclasses are forced to implement all 8, even if 6 are identical!

# ✅ CORRECT — make frequently-shared steps concrete; keep only true variants abstract
class BetterPipeline(ABC):
    @abstractmethod
    def _fetch(self): pass       # varies: CSV vs API vs DB

    @abstractmethod
    def _store(self, data): pass # varies: DB vs file vs API

    def _validate(self, data):   # shared — override only if needed
        return [r for r in data if r]

    def _connect(self):          # shared
        print("Connecting...")
```

### ❌ Pitfall 3: Hooks With Side Effects by Default

```python
from abc import ABC

# ❌ WRONG — default hook does something destructive
class BadPipeline(ABC):
    def _on_complete(self, result):
        self._delete_temp_files()   # side effect in default hook!
        # Subclasses that don't call super() silently leak temp files

# ✅ CORRECT — default hooks are always empty (no-ops)
class GoodPipeline(ABC):
    def _on_complete(self, result):
        pass   # empty by default — subclasses opt in to behavior
```

### ❌ Pitfall 4: Deep Inheritance Chains

```python
from abc import ABC

# ❌ WRONG — template method behavior smeared across 4 levels
class BasePipeline(ABC):          ...   # defines skeleton
class AuthenticatedPipeline(BasePipeline): ...   # adds auth step
class PaginatedPipeline(AuthenticatedPipeline):  ...   # adds paging
class CachedPaginatedPipeline(PaginatedPipeline): ...  # adds caching
# Understanding behavior requires reading 4 classes simultaneously!

# ✅ CORRECT — flatten with hooks and composition
class BasePipeline(ABC):
    def _authenticate(self): pass       # hook: opt-in
    def _paginate(self, data): return data    # hook: opt-in
    def _get_from_cache(self, key): return None  # hook: opt-in
```

---

## ✅ Best Practices

### 1. Document Which Methods Are Hooks vs Abstract

```python
from abc import ABC, abstractmethod

class DataPipeline(ABC):
    # ── TEMPLATE METHOD (do not override) ─────────────
    def run(self) -> PipelineResult: ...

    # ── ABSTRACT (must override) ──────────────────────
    @abstractmethod
    def _extract(self) -> list[dict]: ...

    @abstractmethod
    def _load(self, data: list[dict]) -> int: ...

    # ── HOOKS (optional override, default = no-op) ────
    def _validate(self, data: list[dict]) -> list[dict]:
        return data   # default: accept all

    def _on_complete(self, result: PipelineResult) -> None:
        pass          # default: do nothing
```

### 2. Use `final` Semantics via `__init_subclass__`

```python
from abc import ABC

class ReportGenerator(ABC):
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if "generate" in cls.__dict__:
            raise TypeError(
                f"'{cls.__name__}' must not override 'generate()'"
            )
```

### 3. Prefer Template Method Over Copy-Paste Inheritance

```python
from abc import ABC

# When you notice two subclasses have identical method bodies
# except for one inner call — that's the signal to extract a Template Method.

# Before:
class EmailNotifier:
    def notify(self):
        self._connect_smtp()
        msg = self._format_email(self._data)   # ← differs
        self._send(msg)
        self._log()

class SlackNotifier:
    def notify(self):
        self._connect_smtp()                   # identical!
        msg = self._format_slack(self._data)   # ← differs
        self._send(msg)                        # identical!
        self._log()                            # identical!

# After Template Method:
class Notifier(ABC):
    def notify(self):
        self._connect()
        msg = self._format(self._data)   # abstract — the only difference
        self._send(msg)
        self._log()
```

---

## 📊 Summary

| Aspect                  | Detail                                                                        |
|-------------------------|-------------------------------------------------------------------------------|
| **Type**                | Behavioral                                                                    |
| **Intent**              | Define algorithm skeleton in base; let subclasses fill specific steps         |
| **Key Methods**         | `template_method()` (locked), `abstract steps` (required), `hooks` (optional) |
| **Hollywood Principle** | Base class calls subclass — not the other way around                          |
| **Python Tip**          | Protect template method with `__init_subclass__` guard                        |
| **Real-world Use**      | ETL pipelines, game AI, report generators, test frameworks, web frameworks    |

---

## ✅ Template Method Pattern Checklist

- Is the template method clearly documented as "do not override"?
- Is each abstract step truly variable across subclasses?
- Do all hooks default to no-ops (empty implementations)?
- Is the inheritance hierarchy shallow (1-2 levels)?
- Are concrete (shared) steps truly identical across all subclasses?
- Can each subclass override ONLY the steps it needs to change?
- Is the step order in the template method immutable by design?
- Is the pattern justified — is Strategy a better fit given runtime swapping is needed?

---

## 💡 Key Takeaways

1. **Skeleton is locked, steps are open** — the algorithm's order never changes; only specific steps vary
2. **Hollywood Principle** — the base class is in control; it calls subclass methods, not the reverse
3. **Three kinds of methods** — template (locked), abstract (required override), hooks (optional override)
4. **Hooks are no-ops by default** — subclasses opt in to extra behavior, never forced to override
5. **Prefer over copy-paste** — when two classes share a skeleton with one differing step, extract a Template Method
6. **Key difference from Strategy** — Template Method uses *inheritance* and locks *step order*; Strategy uses *composition* and swaps *entire algorithms* at runtime
