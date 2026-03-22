# 🧠 **Interpreter Pattern**

---

## 📋 Table of Contents
- [What is Interpreter Pattern?](#-what-is-interpreter-pattern)
  - [Key Characteristics](#-key-characteristics)
  - [The Problem It Solves](#-the-problem-it-solves)
  - [Real-World Analogy](#-real-world-analogy)
  - [Visual Representation](#-visual-representation)
- [When to Use](#-when-to-use)
- [When NOT to Use](#-when-not-to-use)
- [Basic Implementation](#-basic-implementation)
- [Real-World Examples](#-real-world-examples)
  - [Example 1: Boolean Query Engine](#example-1-boolean-query-engine)
  - [Example 2: Math Expression Parser](#example-2-math-expression-parser)
  - [Example 3: Mini Rule Engine](#example-3-mini-rule-engine)
- [Common Pitfalls](#-common-pitfalls)
- [Best Practices](#-best-practices)
- [Summary & Checklist](#-summary)
- [Interpreter Pattern Checklist](#-interpreter-pattern-checklist)
- [Key Takeaways](#-key-takeaways)
- [Complete Behavioral Patterns Final Reference](#-complete-behavioral-patterns-final-reference)
- [Final Quick Selection Guide](#-final-quick-selection-guide)

---

## 🔷 What is Interpreter Pattern?

**Interpreter Pattern** is a behavioral design pattern that defines a **grammar for a language** and provides an **interpreter to process sentences in that language**. Each grammar rule becomes a class, and sentences are represented as trees of these rule objects that can be evaluated by calling `interpret()`.

In short: **turn a language into a tree of objects, then walk the tree to evaluate it.**

---

### 🔑 Key Characteristics

| Characteristic           | Description                                                                |
|--------------------------|----------------------------------------------------------------------------|
| **Grammar as Classes**   | Each rule or token in the grammar maps to one class                        |
| **Composite Structure**  | Expressions form a tree — terminals are leaves, non-terminals are branches |
| **Recursive Evaluation** | `interpret()` calls `interpret()` on children — naturally recursive        |
| **Extensible Grammar**   | Add new grammar rules by adding new expression classes                     |
| **Context-Driven**       | A `Context` object carries state/variables used during interpretation      |

---

### 🔥 The Problem It Solves

Without Interpreter, parsing and evaluating custom languages requires tangled, monolithic code:

```python
# ❌ WITHOUT Interpreter — one giant function full of string parsing
def evaluate_rule(rule: str, data: dict) -> bool:
    # Manually parse "age > 18 AND country == 'US' OR vip == True"
    rule = rule.strip()
    if " AND " in rule:
        parts = rule.split(" AND ", 1)
        return evaluate_rule(parts[0], data) and evaluate_rule(parts[1], data)
    elif " OR " in rule:
        parts = rule.split(" OR ", 1)
        return evaluate_rule(parts[0], data) or evaluate_rule(parts[1], data)
    elif " > " in rule:
        field, val = rule.split(" > ")
        return data[field.strip()] > float(val.strip())
    # ... 50 more conditions, no extensibility, untestable, fragile!
```

With Interpreter:

```python
# ✅ WITH Interpreter — each rule is a clean, testable class
rule = AndExpression(
    GreaterThanExpression("age", 18),
    EqualExpression("country", "US")
)
result = rule.interpret({"age": 25, "country": "US"})   # True
# Add new operators = add new classes. Existing code never changes.
```

---

### 🌍 Real-World Analogy

Think of **reading music notation**:

```
Sheet Music (sentence in the language)
    │
    ├── Measure 1
    │     ├── Quarter Note C  ← terminal expression
    │     ├── Half Note E     ← terminal expression
    │     └── Rest            ← terminal expression
    └── Measure 2
          ├── Chord (C+E+G)   ← non-terminal: interprets 3 notes together
          └── Quarter Note F

Musician (Interpreter) walks the tree and produces sound.
Conductor (Context) holds tempo, key signature, dynamics.
```

Each symbol in sheet music maps to a grammar rule. The musician interprets the tree top-down, with context (tempo, key) influencing each note.

---

### 🖼️ Visual Representation

```
           Sentence: "A AND (B OR C)"
                        │
                    AndExpression
                   ┌─────┴──────┐
              TermA           OrExpression
           (terminal)        ┌──────┴──────┐
                           TermB         TermC
                         (terminal)    (terminal)

interpret(context):
  AndExpression.interpret()
    → left.interpret()  → TermA evaluates itself
    → right.interpret() → OrExpression.interpret()
                            → left.interpret()  → TermB
                            → right.interpret() → TermC
```

---

### 🔀 Participants

| Role                      | Responsibility                                               |
|---------------------------|--------------------------------------------------------------|
| **AbstractExpression**    | Declares `interpret(context)` interface                      |
| **TerminalExpression**    | Leaf node — interprets a single symbol directly              |
| **NonTerminalExpression** | Branch node — holds child expressions, delegates to them     |
| **Context**               | Carries global state, variables, input during interpretation |
| **Client**                | Builds the expression tree and calls `interpret(context)`    |

---

## ✅ When to Use

| Scenario                                             | Why It Fits                           |
|------------------------------------------------------|---------------------------------------|
| Simple **domain-specific language (DSL)** needed     | Grammar maps cleanly to classes       |
| **Recurring grammar** that needs evaluation          | Config rules, query filters, formulas |
| Grammar is **small and stable**                      | Few rules — manageable class count    |
| **Business rules** expressed as text need evaluation | Rule engines, permission expressions  |
| **Search query** syntax (AND/OR/NOT)                 | Each operator = one expression class  |

---

## ❌ When NOT to Use

- When the grammar is **complex or large** — use a proper parser generator (ANTLR, PLY, Lark)
- When **performance is critical** — tree walking is slow for large inputs
- When grammar **changes frequently** — every change may require new/modified classes
- When the language is a **standard one** (SQL, JSON, regex) — use existing parsers

---

## 🏗️ Basic Implementation

### Classic Structure

```python
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any

# ─────────────────────────────────────────
# Context — carries variables/state
# ─────────────────────────────────────────
class Context:
    def __init__(self, variables: dict[str, Any] = None):
        self._variables: dict[str, Any] = variables or {}

    def get(self, name: str) -> Any:
        if name not in self._variables:
            raise NameError(f"Undefined variable: '{name}'")
        return self._variables[name]

    def set(self, name: str, value: Any) -> None:
        self._variables[name] = value


# ─────────────────────────────────────────
# Abstract Expression
# ─────────────────────────────────────────
class BooleanExpression(ABC):
    @abstractmethod
    def interpret(self, context: Context) -> bool:
        pass

    # Operator overloads for expressive tree construction
    def __and__(self, other: 'BooleanExpression') -> 'AndExpression':
        return AndExpression(self, other)

    def __or__(self, other: 'BooleanExpression') -> 'OrExpression':
        return OrExpression(self, other)

    def __invert__(self) -> 'NotExpression':
        return NotExpression(self)


# ─────────────────────────────────────────
# Terminal Expressions — leaves of the tree
# ─────────────────────────────────────────
class VariableExpression(BooleanExpression):
    """Looks up a boolean variable in the context."""

    def __init__(self, name: str):
        self._name = name

    def interpret(self, context: Context) -> bool:
        return bool(context.get(self._name))

    def __repr__(self):
        return self._name


class ConstantExpression(BooleanExpression):
    """A literal True or False."""

    def __init__(self, value: bool):
        self._value = value

    def interpret(self, context: Context) -> bool:
        return self._value

    def __repr__(self):
        return str(self._value)


# ─────────────────────────────────────────
# Non-Terminal Expressions — branches
# ─────────────────────────────────────────
class AndExpression(BooleanExpression):
    def __init__(self, left: BooleanExpression, right: BooleanExpression):
        self._left  = left
        self._right = right

    def interpret(self, context: Context) -> bool:
        return self._left.interpret(context) and self._right.interpret(context)

    def __repr__(self):
        return f"({self._left} AND {self._right})"


class OrExpression(BooleanExpression):
    def __init__(self, left: BooleanExpression, right: BooleanExpression):
        self._left  = left
        self._right = right

    def interpret(self, context: Context) -> bool:
        return self._left.interpret(context) or self._right.interpret(context)

    def __repr__(self):
        return f"({self._left} OR {self._right})"


class NotExpression(BooleanExpression):
    def __init__(self, operand: BooleanExpression):
        self._operand = operand

    def interpret(self, context: Context) -> bool:
        return not self._operand.interpret(context)

    def __repr__(self):
        return f"(NOT {self._operand})"


# ─────────────────────────────────────────
# Client — builds tree and interprets
# ─────────────────────────────────────────
a = VariableExpression("a")
b = VariableExpression("b")
c = VariableExpression("c")

# Build: a AND (b OR NOT c)
expr = a & (b | ~c)
print(f"Expression: {expr}")

test_cases = [
    {"a": True,  "b": True,  "c": True},
    {"a": True,  "b": False, "c": True},
    {"a": True,  "b": False, "c": False},
    {"a": False, "b": True,  "c": False},
]

for values in test_cases:
    ctx    = Context(values)
    result = expr.interpret(ctx)
    print(f"  {values} → {result}")

# Expression: (a AND (b OR (NOT c)))
#   {'a': True,  'b': True,  'c': True}  → True
#   {'a': True,  'b': False, 'c': True}  → False
#   {'a': True,  'b': False, 'c': False} → True
#   {'a': False, 'b': True,  'c': False} → False
```

---

## 🌍 Real-World Examples

### Example 1: Boolean Query Engine

```python
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any
from dataclasses import dataclass

# ─────────────────────────────────────────
# Document & Context
# ─────────────────────────────────────────
@dataclass
class Document:
    id:       int
    title:    str
    tags:     set[str]
    author:   str
    year:     int
    views:    int
    premium:  bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "id":      self.id,
            "title":   self.title,
            "tags":    self.tags,
            "author":  self.author,
            "year":    self.year,
            "views":   self.views,
            "premium": self.premium,
        }

    def __repr__(self):
        return f"Doc({self.id}: '{self.title}')"


class QueryContext:
    def __init__(self, document: Document):
        self._doc = document

    def get_field(self, field: str) -> Any:
        data = self._doc.to_dict()
        if field not in data:
            raise KeyError(f"Unknown field: '{field}'")
        return data[field]


# ─────────────────────────────────────────
# Abstract Query Expression
# ─────────────────────────────────────────
class QueryExpression(ABC):
    @abstractmethod
    def interpret(self, context: QueryContext) -> bool:
        pass

    @abstractmethod
    def describe(self) -> str:
        pass

    # Fluent operators
    def __and__(self, other: 'QueryExpression') -> 'AndQuery':
        return AndQuery(self, other)

    def __or__(self, other: 'QueryExpression') -> 'OrQuery':
        return OrQuery(self, other)

    def __invert__(self) -> 'NotQuery':
        return NotQuery(self)

    def __repr__(self):
        return self.describe()


# ─────────────────────────────────────────
# Terminal Expressions
# ─────────────────────────────────────────
class HasTagQuery(QueryExpression):
    def __init__(self, tag: str):
        self._tag = tag.lower()

    def interpret(self, ctx: QueryContext) -> bool:
        tags = ctx.get_field("tags")
        return self._tag in {t.lower() for t in tags}

    def describe(self) -> str:
        return f"tag:{self._tag}"


class AuthorQuery(QueryExpression):
    def __init__(self, author: str):
        self._author = author.lower()

    def interpret(self, ctx: QueryContext) -> bool:
        return ctx.get_field("author").lower() == self._author

    def describe(self) -> str:
        return f"author:{self._author}"


class FieldCompareQuery(QueryExpression):
    """Generic field comparison: field OP value."""

    OPS = {
        "==": lambda a, b: a == b,
        "!=": lambda a, b: a != b,
        ">":  lambda a, b: a >  b,
        ">=": lambda a, b: a >= b,
        "<":  lambda a, b: a <  b,
        "<=": lambda a, b: a <= b,
    }

    def __init__(self, field: str, op: str, value: Any):
        if op not in self.OPS:
            raise ValueError(f"Unknown operator '{op}'. Use: {list(self.OPS)}")
        self._field = field
        self._op    = op
        self._value = value

    def interpret(self, ctx: QueryContext) -> bool:
        field_val = ctx.get_field(self._field)
        return self.OPS[self._op](field_val, self._value)

    def describe(self) -> str:
        return f"{self._field}{self._op}{self._value!r}"


class TitleContainsQuery(QueryExpression):
    def __init__(self, keyword: str):
        self._keyword = keyword.lower()

    def interpret(self, ctx: QueryContext) -> bool:
        return self._keyword in ctx.get_field("title").lower()

    def describe(self) -> str:
        return f"title~'{self._keyword}'"


class IsPremiumQuery(QueryExpression):
    def interpret(self, ctx: QueryContext) -> bool:
        return ctx.get_field("premium")

    def describe(self) -> str:
        return "premium:true"


# ─────────────────────────────────────────
# Non-Terminal Expressions
# ─────────────────────────────────────────
class AndQuery(QueryExpression):
    def __init__(self, left: QueryExpression, right: QueryExpression):
        self._left  = left
        self._right = right

    def interpret(self, ctx: QueryContext) -> bool:
        # Short-circuit evaluation
        return self._left.interpret(ctx) and self._right.interpret(ctx)

    def describe(self) -> str:
        return f"({self._left.describe()} AND {self._right.describe()})"


class OrQuery(QueryExpression):
    def __init__(self, left: QueryExpression, right: QueryExpression):
        self._left  = left
        self._right = right

    def interpret(self, ctx: QueryContext) -> bool:
        return self._left.interpret(ctx) or self._right.interpret(ctx)

    def describe(self) -> str:
        return f"({self._left.describe()} OR {self._right.describe()})"


class NotQuery(QueryExpression):
    def __init__(self, operand: QueryExpression):
        self._operand = operand

    def interpret(self, ctx: QueryContext) -> bool:
        return not self._operand.interpret(ctx)

    def describe(self) -> str:
        return f"NOT({self._operand.describe()})"


# ─────────────────────────────────────────
# Query Parser — turns a string into an expression tree
# ─────────────────────────────────────────
class QueryParser:
    """
    Simple recursive descent parser.
    Supports: tag:X, author:X, field>value, title~keyword, NOT, AND, OR
    """

    def parse(self, query_str: str) -> QueryExpression:
        tokens = query_str.strip().split()
        expr, _ = self._parse_or(tokens, 0)
        return expr

    def _parse_or(self, tokens: list[str],
                  pos: int) -> tuple[QueryExpression, int]:
        left, pos = self._parse_and(tokens, pos)
        while pos < len(tokens) and tokens[pos].upper() == "OR":
            right, pos = self._parse_and(tokens, pos + 1)
            left = OrQuery(left, right)
        return left, pos

    def _parse_and(self, tokens: list[str],
                   pos: int) -> tuple[QueryExpression, int]:
        left, pos = self._parse_unary(tokens, pos)
        while pos < len(tokens) and tokens[pos].upper() == "AND":
            right, pos = self._parse_unary(tokens, pos + 1)
            left = AndQuery(left, right)
        return left, pos

    def _parse_unary(self, tokens: list[str],
                     pos: int) -> tuple[QueryExpression, int]:
        if tokens[pos].upper() == "NOT":
            operand, pos = self._parse_unary(tokens, pos + 1)
            return NotQuery(operand), pos
        return self._parse_primary(tokens, pos)

    def _parse_primary(self, tokens: list[str],
                       pos: int) -> tuple[QueryExpression, int]:
        token = tokens[pos]

        if token.startswith("tag:"):
            return HasTagQuery(token[4:]), pos + 1

        if token.startswith("author:"):
            return AuthorQuery(token[7:]), pos + 1

        if token.startswith("title~"):
            return TitleContainsQuery(token[6:]), pos + 1

        if token == "premium:true":
            return IsPremiumQuery(), pos + 1

        # field>value, field>=value, etc.
        for op in [">=", "<=", "!=", ">", "<", "=="]:
            if op in token:
                field, val_str = token.split(op, 1)
                val = int(val_str) if val_str.isdigit() else val_str
                return FieldCompareQuery(field, op, val), pos + 1

        raise SyntaxError(f"Cannot parse token: '{token}'")


# ─────────────────────────────────────────
# Search Engine
# ─────────────────────────────────────────
class DocumentSearchEngine:
    def __init__(self, documents: list[Document]):
        self._docs   = documents
        self._parser = QueryParser()

    def search(self, query: QueryExpression) -> list[Document]:
        results = [
            doc for doc in self._docs
            if query.interpret(QueryContext(doc))
        ]
        print(f"\n  🔍 Query : {query.describe()}")
        print(f"  📄 Found : {len(results)} document(s)")
        for doc in results:
            print(f"     • {doc} | tags={doc.tags} | "
                  f"views={doc.views} | premium={doc.premium}")
        return results

    def search_string(self, query_str: str) -> list[Document]:
        query = self._parser.parse(query_str)
        return self.search(query)


# ─────────────────────────────────────────
# Client
# ─────────────────────────────────────────
docs = [
    Document(1, "Python Design Patterns",
             {"python", "design", "programming"}, "alice", 2023, 4200, premium=False),
    Document(2, "Advanced Python",
             {"python", "advanced"}, "bob",   2022, 1800, premium=True),
    Document(3, "Clean Code in Python",
             {"python", "clean-code"}, "alice", 2024, 3100, premium=False),
    Document(4, "JavaScript Patterns",
             {"javascript", "design"}, "carol", 2023,  950, premium=False),
    Document(5, "Rust for Python Devs",
             {"rust", "python"}, "bob",   2024, 2600, premium=True),
    Document(6, "Data Structures",
             {"algorithms", "cs"}, "alice", 2021,  720, premium=False),
]

engine = DocumentSearchEngine(docs)

# ── Build queries programmatically ──
print("=== Python tag AND views > 2000 ===")
engine.search(
    HasTagQuery("python") & FieldCompareQuery("views", ">", 2000)
)

print("\n=== Author alice OR premium ===")
engine.search(
    AuthorQuery("alice") | IsPremiumQuery()
)

print("\n=== Python tag AND NOT premium AND year >= 2023 ===")
engine.search(
    HasTagQuery("python")
    & ~IsPremiumQuery()
    & FieldCompareQuery("year", ">=", 2023)
)

print("\n=== design tag OR title contains 'python' ===")
engine.search(
    HasTagQuery("design") | TitleContainsQuery("python")
)

# ── Parse queries from strings ──
print("\n=== String query: tag:python AND views>2000 ===")
engine.search_string("tag:python AND views>2000")

print("\n=== String query: author:alice OR NOT premium:true ===")
engine.search_string("author:alice OR NOT premium:true")
```

---

### Example 2: Math Expression Parser

```python
from __future__ import annotations
from abc import ABC, abstractmethod
import math

# ─────────────────────────────────────────
# Context — holds variable bindings
# ─────────────────────────────────────────
class MathContext:
    def __init__(self, variables: dict[str, float] = None):
        self._vars:    dict[str, float] = variables or {}
        self._history: list[str]        = []

    def get(self, name: str) -> float:
        if name not in self._vars:
            raise NameError(f"Undefined variable: '{name}'")
        return self._vars[name]

    def set(self, name: str, value: float) -> None:
        self._vars[name] = value

    def log(self, entry: str) -> None:
        self._history.append(entry)


# ─────────────────────────────────────────
# Abstract Expression
# ─────────────────────────────────────────
class MathExpression(ABC):
    @abstractmethod
    def interpret(self, context: MathContext) -> float:
        pass

    @abstractmethod
    def to_string(self) -> str:
        pass

    # Operator overloads for clean tree building
    def __add__(self, other):  return AddExpression(self, _wrap(other))
    def __sub__(self, other):  return SubtractExpression(self, _wrap(other))
    def __mul__(self, other):  return MultiplyExpression(self, _wrap(other))
    def __truediv__(self, other): return DivideExpression(self, _wrap(other))
    def __pow__(self, other):  return PowerExpression(self, _wrap(other))
    def __neg__(self):         return NegateExpression(self)
    def __repr__(self):        return self.to_string()


def _wrap(val) -> MathExpression:
    """Auto-wrap raw numbers into NumberExpression."""
    return val if isinstance(val, MathExpression) else NumberExpression(val)


# ─────────────────────────────────────────
# Terminal Expressions
# ─────────────────────────────────────────
class NumberExpression(MathExpression):
    def __init__(self, value: float):
        self._value = float(value)

    def interpret(self, context: MathContext) -> float:
        return self._value

    def to_string(self) -> str:
        return str(int(self._value) if self._value == int(self._value)
                   else self._value)


class VariableExpression(MathExpression):
    def __init__(self, name: str):
        self._name = name

    def interpret(self, context: MathContext) -> float:
        return context.get(self._name)

    def to_string(self) -> str:
        return self._name


class ConstantExpression(MathExpression):
    """Mathematical constants: π, e, φ"""
    CONSTANTS = {
        "pi":  math.pi,
        "e":   math.e,
        "phi": (1 + math.sqrt(5)) / 2,
        "tau": math.tau,
    }

    def __init__(self, name: str):
        if name not in self.CONSTANTS:
            raise ValueError(f"Unknown constant: '{name}'")
        self._name  = name
        self._value = self.CONSTANTS[name]

    def interpret(self, context: MathContext) -> float:
        return self._value

    def to_string(self) -> str:
        return self._name


# ─────────────────────────────────────────
# Binary Non-Terminal Expressions
# ─────────────────────────────────────────
class BinaryExpression(MathExpression):
    def __init__(self, left: MathExpression, right: MathExpression,
                 symbol: str):
        self._left   = left
        self._right  = right
        self._symbol = symbol

    def to_string(self) -> str:
        return f"({self._left.to_string()} {self._symbol} {self._right.to_string()})"


class AddExpression(BinaryExpression):
    def __init__(self, left, right):
        super().__init__(left, right, "+")

    def interpret(self, ctx: MathContext) -> float:
        result = self._left.interpret(ctx) + self._right.interpret(ctx)
        ctx.log(f"{self.to_string()} = {result:.6g}")
        return result


class SubtractExpression(BinaryExpression):
    def __init__(self, left, right):
        super().__init__(left, right, "-")

    def interpret(self, ctx: MathContext) -> float:
        return self._left.interpret(ctx) - self._right.interpret(ctx)


class MultiplyExpression(BinaryExpression):
    def __init__(self, left, right):
        super().__init__(left, right, "*")

    def interpret(self, ctx: MathContext) -> float:
        return self._left.interpret(ctx) * self._right.interpret(ctx)


class DivideExpression(BinaryExpression):
    def __init__(self, left, right):
        super().__init__(left, right, "/")

    def interpret(self, ctx: MathContext) -> float:
        divisor = self._right.interpret(ctx)
        if divisor == 0:
            raise ZeroDivisionError(f"Division by zero in: {self.to_string()}")
        return self._left.interpret(ctx) / divisor


class PowerExpression(BinaryExpression):
    def __init__(self, left, right):
        super().__init__(left, right, "**")

    def interpret(self, ctx: MathContext) -> float:
        return self._left.interpret(ctx) ** self._right.interpret(ctx)


class ModuloExpression(BinaryExpression):
    def __init__(self, left, right):
        super().__init__(left, right, "%")

    def interpret(self, ctx: MathContext) -> float:
        return self._left.interpret(ctx) % self._right.interpret(ctx)


# ─────────────────────────────────────────
# Unary Non-Terminal Expressions
# ─────────────────────────────────────────
class NegateExpression(MathExpression):
    def __init__(self, operand: MathExpression):
        self._operand = operand

    def interpret(self, ctx: MathContext) -> float:
        return -self._operand.interpret(ctx)

    def to_string(self) -> str:
        return f"(-{self._operand.to_string()})"


class FunctionExpression(MathExpression):
    """Applies a named math function to one argument."""

    FUNCTIONS = {
        "sqrt":  math.sqrt,
        "abs":   abs,
        "sin":   math.sin,
        "cos":   math.cos,
        "tan":   math.tan,
        "log":   math.log,
        "log10": math.log10,
        "exp":   math.exp,
        "ceil":  math.ceil,
        "floor": math.floor,
        "round": round,
    }

    def __init__(self, name: str, argument: MathExpression):
        if name not in self.FUNCTIONS:
            raise ValueError(f"Unknown function: '{name}'")
        self._name = name
        self._arg  = argument

    def interpret(self, ctx: MathContext) -> float:
        val = self._arg.interpret(ctx)
        return self.FUNCTIONS[self._name](val)

    def to_string(self) -> str:
        return f"{self._name}({self._arg.to_string()})"


class AssignExpression(MathExpression):
    """Assignment: variable = expression. Returns the assigned value."""

    def __init__(self, name: str, expr: MathExpression):
        self._name = name
        self._expr = expr

    def interpret(self, ctx: MathContext) -> float:
        value = self._expr.interpret(ctx)
        ctx.set(self._name, value)
        print(f"  📌 {self._name} = {value:.6g}")
        return value

    def to_string(self) -> str:
        return f"{self._name} = {self._expr.to_string()}"


# ─────────────────────────────────────────
# Expression Parser — string → tree
# ─────────────────────────────────────────
class MathParser:
    """
    Recursive descent parser for math expressions.
    Grammar:
      expr    = assign
      assign  = NAME '=' add  |  add
      add     = mul (('+' | '-') mul)*
      mul     = unary (('*' | '/') unary)*
      unary   = '-' unary  |  power
      power   = primary ('**' primary)*
      primary = NUMBER | NAME | FUNC '(' expr ')' | '(' expr ')'
    """

    def __init__(self, text: str):
        import re
        token_spec = [
            ("NUMBER",  r'\d+\.?\d*'),
            ("NAME",    r'[a-zA-Z_]\w*'),
            ("OP",      r'\*\*|[+\-*/()=%]'),
            ("SKIP",    r'\s+'),
        ]
        pattern = "|".join(f"(?P<{n}>{p})" for n, p in token_spec)
        self._tokens = [
            (m.lastgroup, m.group())
            for m in re.finditer(pattern, text)
            if m.lastgroup != "SKIP"
        ]
        self._pos = 0

    def _peek(self) -> tuple | None:
        return self._tokens[self._pos] if self._pos < len(self._tokens) else None

    def _consume(self, expected_val: str = None) -> tuple:
        tok = self._tokens[self._pos]
        if expected_val and tok[1] != expected_val:
            raise SyntaxError(f"Expected '{expected_val}', got '{tok[1]}'")
        self._pos += 1
        return tok

    def parse(self) -> MathExpression:
        expr = self._parse_assign()
        if self._pos < len(self._tokens):
            raise SyntaxError(f"Unexpected token: {self._peek()}")
        return expr

    def _parse_assign(self) -> MathExpression:
        # Check for assignment: NAME = expr
        if (self._pos + 1 < len(self._tokens) and
                self._tokens[self._pos][0]   == "NAME" and
                self._tokens[self._pos + 1][1] == "="):
            name = self._consume()[1]
            self._consume("=")
            expr = self._parse_add()
            return AssignExpression(name, expr)
        return self._parse_add()

    def _parse_add(self) -> MathExpression:
        left = self._parse_mul()
        while (tok := self._peek()) and tok[1] in ("+", "-"):
            op = self._consume()[1]
            right = self._parse_mul()
            left  = (AddExpression(left, right) if op == "+"
                     else SubtractExpression(left, right))
        return left

    def _parse_mul(self) -> MathExpression:
        left = self._parse_unary()
        while (tok := self._peek()) and tok[1] in ("*", "/", "%"):
            op    = self._consume()[1]
            right = self._parse_unary()
            if op == "*": left = MultiplyExpression(left, right)
            elif op == "/": left = DivideExpression(left, right)
            else:           left = ModuloExpression(left, right)
        return left

    def _parse_unary(self) -> MathExpression:
        if (tok := self._peek()) and tok[1] == "-":
            self._consume("-")
            return NegateExpression(self._parse_unary())
        return self._parse_power()

    def _parse_power(self) -> MathExpression:
        base = self._parse_primary()
        if (tok := self._peek()) and tok[1] == "**":
            self._consume("**")
            exp = self._parse_unary()
            return PowerExpression(base, exp)
        return base

    def _parse_primary(self) -> MathExpression:
        tok = self._peek()
        if not tok:
            raise SyntaxError("Unexpected end of expression")

        kind, val = tok

        if kind == "NUMBER":
            self._consume()
            return NumberExpression(float(val))

        if kind == "NAME":
            self._consume()
            # Function call?
            if self._peek() and self._peek()[1] == "(":
                self._consume("(")
                arg = self._parse_add()
                self._consume(")")
                return FunctionExpression(val, arg)
            # Known constant?
            if val in ConstantExpression.CONSTANTS:
                return ConstantExpression(val)
            # Variable
            return VariableExpression(val)

        if val == "(":
            self._consume("(")
            expr = self._parse_add()
            self._consume(")")
            return expr

        raise SyntaxError(f"Unexpected token: {tok}")


def calc(expr_str: str, **variables) -> float:
    """Convenience: parse and evaluate a math expression string."""
    ctx  = MathContext(variables)
    tree = MathParser(expr_str).parse()
    result = tree.interpret(ctx)
    print(f"  📐 {expr_str!r:35s} = {result:.6g}")
    return result


# ─────────────────────────────────────────
# Client
# ─────────────────────────────────────────
print("=== Basic Arithmetic ===")
calc("2 + 3 * 4")
calc("(2 + 3) * 4")
calc("10 / 4")
calc("2 ** 10")
calc("17 % 5")

print("\n=== Variables ===")
ctx = MathContext({"x": 3.0, "y": 4.0})
tree = MathParser("sqrt(x**2 + y**2)").parse()
print(f"  📐 sqrt(x²+y²) with x=3, y=4 = {tree.interpret(ctx):.6g}")

calc("x * 2 + y", x=5.0, y=10.0)

print("\n=== Constants ===")
calc("2 * pi * 5")           # circumference of circle r=5
calc("e ** 2")
calc("(1 + sqrt(5)) / 2")   # golden ratio approximation

print("\n=== Functions ===")
calc("sin(pi / 6)")          # 0.5
calc("log(e)")               # 1.0
calc("sqrt(144)")
calc("floor(3.9)")

print("\n=== Assignment ===")
ctx2 = MathContext()
MathParser("r = 7").parse().interpret(ctx2)
MathParser("area = pi * r ** 2").parse().interpret(ctx2)
MathParser("perimeter = 2 * pi * r").parse().interpret(ctx2)

print("\n=== Build tree programmatically ===")
x   = VariableExpression("x")
pi  = ConstantExpression("pi")
# Area of circle: π * x²
area_expr = MultiplyExpression(pi, PowerExpression(x, NumberExpression(2)))
print(f"  Expression: {area_expr.to_string()}")
ctx3 = MathContext({"x": 5.0})
print(f"  Area (r=5): {area_expr.interpret(ctx3):.4f}")
```

---

### Example 3: Mini Rule Engine

```python
from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Callable
from datetime import datetime
from enum import Enum

# ─────────────────────────────────────────
# Context — the entity being evaluated
# ─────────────────────────────────────────
@dataclass
class RuleContext:
    entity:    dict[str, Any]
    triggered: list[str] = field(default_factory=list)
    actions:   list[str] = field(default_factory=list)

    def get(self, field: str) -> Any:
        parts = field.split(".")
        val   = self.entity
        for part in parts:
            if isinstance(val, dict):
                val = val.get(part)
            else:
                val = getattr(val, part, None)
            if val is None:
                return None
        return val


# ─────────────────────────────────────────
# Abstract Rule Expression
# ─────────────────────────────────────────
class RuleExpression(ABC):
    @abstractmethod
    def evaluate(self, context: RuleContext) -> bool:
        pass

    @abstractmethod
    def describe(self) -> str:
        pass

    def __and__(self, other):  return AllOf(self, other)
    def __or__(self, other):   return AnyOf(self, other)
    def __invert__(self):      return NoneOf(self)
    def __repr__(self):        return self.describe()


# ─────────────────────────────────────────
# Condition Expressions (Terminals)
# ─────────────────────────────────────────
class FieldCondition(RuleExpression):
    """field OP value — the most common condition type."""

    OPERATORS: dict[str, Callable] = {
        "eq":  lambda a, b: a == b,
        "ne":  lambda a, b: a != b,
        "gt":  lambda a, b: a is not None and a >  b,
        "gte": lambda a, b: a is not None and a >= b,
        "lt":  lambda a, b: a is not None and a <  b,
        "lte": lambda a, b: a is not None and a <= b,
        "in":  lambda a, b: a in b,
        "nin": lambda a, b: a not in b,
        "contains": lambda a, b: b in str(a) if a else False,
        "startswith": lambda a, b: str(a).startswith(b) if a else False,
    }

    def __init__(self, field: str, op: str, value: Any):
        if op not in self.OPERATORS:
            raise ValueError(
                f"Unknown operator '{op}'. Valid: {list(self.OPERATORS)}"
            )
        self._field = field
        self._op    = op
        self._value = value

    def evaluate(self, ctx: RuleContext) -> bool:
        actual = ctx.get(self._field)
        return self.OPERATORS[self._op](actual, self._value)

    def describe(self) -> str:
        return f"{self._field} {self._op} {self._value!r}"


class ExistsCondition(RuleExpression):
    """Checks that a field is not None."""

    def __init__(self, field: str):
        self._field = field

    def evaluate(self, ctx: RuleContext) -> bool:
        return ctx.get(self._field) is not None

    def describe(self) -> str:
        return f"{self._field} exists"


class CustomCondition(RuleExpression):
    """Arbitrary callable condition."""

    def __init__(self, label: str, fn: Callable[[RuleContext], bool]):
        self._label = label
        self._fn    = fn

    def evaluate(self, ctx: RuleContext) -> bool:
        return self._fn(ctx)

    def describe(self) -> str:
        return f"custom:{self._label}"


# ─────────────────────────────────────────
# Composite Expressions (Non-Terminals)
# ─────────────────────────────────────────
class AllOf(RuleExpression):
    """All conditions must be true (AND with n operands)."""

    def __init__(self, *conditions: RuleExpression):
        self._conditions = conditions

    def evaluate(self, ctx: RuleContext) -> bool:
        return all(c.evaluate(ctx) for c in self._conditions)

    def describe(self) -> str:
        parts = " AND ".join(c.describe() for c in self._conditions)
        return f"ALL({parts})"


class AnyOf(RuleExpression):
    """At least one condition must be true (OR with n operands)."""

    def __init__(self, *conditions: RuleExpression):
        self._conditions = conditions

    def evaluate(self, ctx: RuleContext) -> bool:
        return any(c.evaluate(ctx) for c in self._conditions)

    def describe(self) -> str:
        parts = " OR ".join(c.describe() for c in self._conditions)
        return f"ANY({parts})"


class NoneOf(RuleExpression):
    """Negation of a condition."""

    def __init__(self, condition: RuleExpression):
        self._condition = condition

    def evaluate(self, ctx: RuleContext) -> bool:
        return not self._condition.evaluate(ctx)

    def describe(self) -> str:
        return f"NOT({self._condition.describe()})"


class AtLeast(RuleExpression):
    """At least N of the given conditions must be true."""

    def __init__(self, n: int, *conditions: RuleExpression):
        self._n          = n
        self._conditions = conditions

    def evaluate(self, ctx: RuleContext) -> bool:
        passed = sum(1 for c in self._conditions if c.evaluate(ctx))
        return passed >= self._n

    def describe(self) -> str:
        parts = ", ".join(c.describe() for c in self._conditions)
        return f"AT_LEAST({self._n} of [{parts}])"


# ─────────────────────────────────────────
# Rule — wraps a condition with metadata and actions
# ─────────────────────────────────────────
@dataclass
class Rule:
    name:        str
    condition:   RuleExpression
    actions:     list[str]                  = field(default_factory=list)
    priority:    int                        = 0
    enabled:     bool                       = True
    description: str                        = ""

    def evaluate(self, ctx: RuleContext) -> bool:
        if not self.enabled:
            return False
        result = self.condition.evaluate(ctx)
        if result:
            ctx.triggered.append(self.name)
            ctx.actions.extend(self.actions)
            print(f"  ✅ Rule TRIGGERED: '{self.name}'")
            for action in self.actions:
                print(f"     → Action: {action}")
        return result


# ─────────────────────────────────────────
# Rule Engine
# ─────────────────────────────────────────
class RuleEngine:
    def __init__(self):
        self._rules: list[Rule] = []

    def add_rule(self, rule: Rule) -> 'RuleEngine':
        self._rules.append(rule)
        # Keep sorted by priority (highest first)
        self._rules.sort(key=lambda r: r.priority, reverse=True)
        return self

    def evaluate(self, entity: dict[str, Any],
                 stop_on_first: bool = False) -> RuleContext:
        ctx = RuleContext(entity=entity)
        print(f"\n  ⚙️  Evaluating {len(self._rules)} rules for: "
              f"{entity.get('name', entity.get('id', '?'))}")
        print(f"  {'─'*45}")

        triggered = 0
        for rule in self._rules:
            fired = rule.evaluate(ctx)
            if fired:
                triggered += 1
            if fired and stop_on_first:
                print(f"  (Stopped after first match)")
                break

        print(f"  {'─'*45}")
        print(f"  {triggered}/{len(self._rules)} rules triggered")
        return ctx


# ─────────────────────────────────────────
# Client — Fraud Detection + Loan Approval
# ─────────────────────────────────────────
print("=" * 55)
print("  FRAUD DETECTION ENGINE")
print("=" * 55)

fraud_engine = RuleEngine()

fraud_engine\
    .add_rule(Rule(
        name      = "High Amount",
        condition = FieldCondition("amount", "gt", 10_000),
        actions   = ["flag_for_review", "notify_risk_team"],
        priority  = 10,
    ))\
    .add_rule(Rule(
        name      = "New Account Large Transfer",
        condition = AllOf(
            FieldCondition("account_age_days", "lt", 30),
            FieldCondition("amount", "gt", 2_000),
        ),
        actions   = ["block_transaction", "request_verification"],
        priority  = 20,
    ))\
    .add_rule(Rule(
        name      = "Foreign + High Risk Country",
        condition = AllOf(
            FieldCondition("is_foreign", "eq", True),
            FieldCondition("country_risk", "in", ["HIGH", "VERY_HIGH"]),
        ),
        actions   = ["require_2fa", "flag_for_review"],
        priority  = 15,
    ))\
    .add_rule(Rule(
        name      = "Velocity Check",
        condition = FieldCondition("txn_last_hour", "gt", 5),
        actions   = ["rate_limit_user", "notify_user"],
        priority  = 12,
    ))\
    .add_rule(Rule(
        name      = "Suspicious Pattern",
        condition = AtLeast(2,
            FieldCondition("amount",          "gt", 5_000),
            FieldCondition("is_foreign",      "eq", True),
            FieldCondition("new_device",      "eq", True),
            FieldCondition("txn_last_hour",   "gt", 3),
        ),
        actions   = ["block_transaction", "alert_fraud_team"],
        priority  = 25,
    ))

transactions = [
    {"name": "Safe payment",   "amount": 150,    "account_age_days": 365,
     "is_foreign": False, "country_risk": "LOW",  "txn_last_hour": 1,
     "new_device": False},

    {"name": "New + Large",    "amount": 3_500,  "account_age_days": 10,
     "is_foreign": False, "country_risk": "LOW",  "txn_last_hour": 2,
     "new_device": False},

    {"name": "Suspicious",     "amount": 8_000,  "account_age_days": 200,
     "is_foreign": True,  "country_risk": "HIGH", "txn_last_hour": 5,
     "new_device": True},
]

for txn in transactions:
    fraud_engine.evaluate(txn)

print("\n" + "=" * 55)
print("  LOAN APPROVAL ENGINE")
print("=" * 55)

loan_engine = RuleEngine()

loan_engine\
    .add_rule(Rule(
        name      = "Excellent Credit — Auto Approve",
        condition = AllOf(
            FieldCondition("credit_score",    "gte", 750),
            FieldCondition("debt_to_income",  "lte", 0.30),
            FieldCondition("employment_years","gte", 2),
        ),
        actions   = ["auto_approve", "offer_prime_rate"],
        priority  = 30,
    ))\
    .add_rule(Rule(
        name      = "Good Credit — Approve",
        condition = AllOf(
            FieldCondition("credit_score",   "gte", 680),
            FieldCondition("debt_to_income", "lte", 0.40),
        ),
        actions   = ["approve", "offer_standard_rate"],
        priority  = 20,
    ))\
    .add_rule(Rule(
        name      = "Poor Credit — Reject",
        condition = AnyOf(
            FieldCondition("credit_score",   "lt", 580),
            FieldCondition("debt_to_income", "gt", 0.55),
        ),
        actions   = ["reject", "send_denial_letter"],
        priority  = 25,
    ))\
    .add_rule(Rule(
        name      = "Manual Review",
        condition = AllOf(
            FieldCondition("credit_score",   "gte", 580),
            FieldCondition("credit_score",   "lt",  680),
        ),
        actions   = ["queue_for_manual_review", "request_documents"],
        priority  = 15,
    ))

applicants = [
    {"name": "Alice",   "credit_score": 790, "debt_to_income": 0.22,
     "employment_years": 5},
    {"name": "Bob",     "credit_score": 710, "debt_to_income": 0.35,
     "employment_years": 3},
    {"name": "Carol",   "credit_score": 620, "debt_to_income": 0.42,
     "employment_years": 1},
    {"name": "Dave",    "credit_score": 520, "debt_to_income": 0.60,
     "employment_years": 0},
]

for applicant in applicants:
    ctx = loan_engine.evaluate(applicant)
    if ctx.actions:
        final = ctx.actions[-1]
        print(f"  📋 Final actions: {ctx.actions}")
```

---

## ⚠️ Common Pitfalls

### ❌ Pitfall 1: Using Interpreter for Complex Grammars

```python
# ❌ WRONG — building a full SQL parser with Interpreter Pattern
class SelectExpression(SQLExpression): ...
class WhereExpression(SQLExpression): ...
class JoinExpression(SQLExpression): ...
class SubqueryExpression(SQLExpression): ...
class WindowFunctionExpression(SQLExpression): ...
# 50+ classes later — use a real parser library instead!

# ✅ CORRECT — Interpreter is for SMALL, SIMPLE, STABLE grammars
# For complex languages: use PLY, Lark, ANTLR, or pyparsing
from lark import Lark
parser = Lark(grammar_string, parser="earley")
```

### ❌ Pitfall 2: Putting Parsing Logic Inside Expressions

```python
# ❌ WRONG — expression classes parse their own input
class AddExpression:
    def __init__(self, text: str):
        parts = text.split("+")    # parsing inside the expression!
        self._left  = parse(parts[0])
        self._right = parse(parts[1])

# ✅ CORRECT — separate Parser from Expressions completely
# Parser builds the tree; Expressions only interpret
class AddExpression:
    def __init__(self, left: MathExpression, right: MathExpression):
        self._left  = left    # receives already-parsed sub-trees
        self._right = right
```

### ❌ Pitfall 3: Mutable Context Shared Across Independent Evaluations

```python
# ❌ WRONG — same context reused across multiple evaluate() calls
ctx  = Context({"x": 5})
expr.interpret(ctx)    # may modify ctx
expr.interpret(ctx)    # second call sees modified state — surprise!

# ✅ CORRECT — create a fresh context per evaluation
def evaluate(expression, variables):
    ctx = Context(dict(variables))   # fresh copy each time
    return expression.interpret(ctx)
```

### ❌ Pitfall 4: Deep Recursion for Large Expressions

```python
# ❌ PROBLEM — deeply nested expressions hit Python's recursion limit
# e.g. a + b + c + d + ... (1000 terms) → 1000 levels of recursion → RecursionError

# ✅ MITIGATION — use an explicit stack for iterative evaluation
# Or increase limit (last resort):
import sys
sys.setrecursionlimit(5000)

# ✅ BETTER — flatten left-associative chains during parsing
# (a + b) + c  →  AddMany([a, b, c]) instead of Add(Add(a, b), c)
class AddManyExpression(MathExpression):
    def __init__(self, operands: list[MathExpression]):
        self._operands = operands

    def interpret(self, ctx) -> float:
        return sum(op.interpret(ctx) for op in self._operands)  # iterative
```

---

## ✅ Best Practices

### 1. Separate Parser from Interpreter

```python
# ✅ Clean separation of concerns:
# Parser: string → tree
# Interpreter: tree → result

class MathParser:
    def parse(self, text: str) -> MathExpression: ...  # builds tree only

class MathExpression(ABC):
    def interpret(self, ctx: MathContext) -> float: ... # evaluates only

# Usage:
tree   = MathParser().parse("2 * pi * r")
result = tree.interpret(MathContext({"r": 5.0}))
```

### 2. Use `__and__`, `__or__`, `__invert__` for Expressive Tree Building

```python
# ✅ Python operator overloads make expression trees readable
a = FieldCondition("age",     "gte", 18)
b = FieldCondition("country", "eq",  "US")
c = FieldCondition("premium", "eq",  True)

rule = a & (b | c)   # much cleaner than AndExpression(a, OrExpression(b, c))
```

### 3. Cache Frequently-Used Sub-Expressions

```python
# ✅ Share immutable sub-trees across multiple rules
IS_ADULT    = FieldCondition("age", "gte", 18)
IS_VERIFIED = FieldCondition("verified", "eq", True)

rule1 = IS_ADULT & IS_VERIFIED & FieldCondition("tier", "eq", "gold")
rule2 = IS_ADULT & FieldCondition("country", "eq", "US")
# IS_ADULT is shared safely — expressions are stateless
```

### 4. Add `describe()` for Logging and Debugging

```python
# ✅ Every expression should be able to describe itself
class AllOf(RuleExpression):
    def describe(self) -> str:
        return "ALL(" + " AND ".join(c.describe() for c in self._conditions) + ")"

# Use describe() in logs:
print(f"Rule triggered: {rule.condition.describe()}")
# → "ALL(age gte 18 AND country eq 'US')"
```

---

## 📊 Summary

| Aspect             | Detail                                                                                |
|--------------------|---------------------------------------------------------------------------------------|
| **Type**           | Behavioral                                                                            |
| **Intent**         | Define a grammar and evaluate sentences in that grammar as a tree                     |
| **Key Mechanism**  | Each grammar rule = one class; `interpret(context)` walks the tree recursively        |
| **Best For**       | Small, stable DSLs — query filters, rule engines, expression evaluators               |
| **Worst For**      | Complex grammars — use PLY, Lark, or ANTLR instead                                    |
| **Real-world Use** | Search queries, rule engines, config evaluators, formula parsers, boolean expressions |

---

## ✅ Interpreter Pattern Checklist

- Is the grammar small and stable enough to justify this pattern?
- Is parsing separated from interpreting (Parser class vs Expression classes)?
- Does every expression implement interpret(context) and describe()?
- Are terminal expressions truly leaf nodes (no child expressions)?
- Does Context carry all needed external state cleanly?
- Are expressions stateless (safe to reuse across contexts)?
- Is recursion depth acceptable for expected input sizes?
- For complex grammars, is a parser library used instead?

---

## 💡 Key Takeaways

1. **Grammar as a class hierarchy** — each rule becomes a class; sentences become trees of those classes
2. **Double recursion** — `interpret()` calls itself on children, naturally walking the tree
3. **Separate parsing from evaluation** — the Parser builds the tree; Expression classes evaluate it
4. **Expressions should be stateless** — context carries state, expressions are pure functions on it
5. **Operator overloads** (`__and__`, `__or__`, `__invert__`) make tree construction expressive in Python
6. **Scale limit** — for grammars beyond ~10 rules, switch to a dedicated parser library

---

## 🎉 Complete Behavioral Patterns Final Reference

All **12 behavioral patterns** are now covered:

| #  | Pattern                     | Intent                                         | Key Mechanism                                |
|----|-----------------------------|------------------------------------------------|----------------------------------------------|
| 1  | **Chain of Responsibility** | Pass request along handler chain               | Each handler processes or forwards           |
| 2  | **Command**                 | Encapsulate request as object                  | `execute()` / `undo()` on command objects    |
| 3  | **Iterator**                | Traverse collection without exposing internals | `__iter__` / `__next__` protocol             |
| 4  | **Mediator**                | Replace O(n²) links with O(n) hub              | All components talk through one mediator     |
| 5  | **Memento**                 | Snapshot and restore state                     | Originator creates opaque snapshots          |
| 6  | **Observer**                | Notify many on one object's change             | `attach` / `detach` / `notify`               |
| 7  | **State**                   | Change behavior when state changes             | Delegate to current state object             |
| 8  | **Strategy**                | Make algorithms interchangeable                | Inject and swap strategy objects             |
| 9  | **Template Method**         | Lock skeleton, defer steps                     | `final` template + abstract hooks            |
| 10 | **Visitor**                 | Add operations without modifying hierarchy     | Double dispatch via `accept(visitor)`        |
| 11 | **Null Object**             | Replace `None` checks with do-nothing object   | Implement interface with safe no-ops         |
| 12 | **Interpreter**             | Evaluate sentences in a custom grammar         | Grammar rule = class; tree walk = evaluation |

---

### 🔍 Final Quick Selection Guide

```
Traversing or filtering a collection?
  → Iterator

Undo/Redo needed?
  → Command (stores operations) or Memento (stores state)

Event-driven or reactive system?
  → Observer (broadcast) or Mediator (coordinated hub)

Behavior changes with lifecycle?
  → State

Swap algorithms at runtime?
  → Strategy

Reuse algorithm skeleton with variable steps?
  → Template Method

Add operations to a stable class hierarchy?
  → Visitor

Decouple sender from receiver in a pipeline?
  → Chain of Responsibility

Eliminate None checks for optional collaborators?
  → Null Object

Evaluate a custom DSL, query, or formula?
  → Interpreter
```