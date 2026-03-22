# 🧠 **Visitor Pattern**

---

## 📋 Table of Contents
- [What is Visitor Pattern?](#-what-is-visitor-pattern)
  - [Key Characteristics](#-key-characteristics)
  - [The Problem It Solves](#-the-problem-it-solves)
  - [Real-World Analogy](#-real-world-analogy)
  - [Visual Representation](#-visual-representation)
- [When to Use](#-when-to-use)
- [When NOT to Use](#-when-not-to-use)
- [Basic Implementation](#-basic-implementation)
- [Real-World Examples](#-real-world-examples)
  - [Example 1: AST Expression Evaluator](#example-1-ast-expression-evaluator)
  - [Example 2: Document Exporter](#example-2-document-exporter)
  - [Example 3: E-Commerce Tax & Discount Engine](#example-3-e-commerce-tax--discount-engine)
- [Common Pitfalls](#-common-pitfalls)
- [Best Practices](#-best-practices)
- [Summary](#-summary)
- [Key Takeaways](#-key-takeaways)
- [Complete Behavioral Patterns Reference](#-complete-behavioral-patterns-reference)
- [Quick Selection Guide](#-quick-selection-guide)

---

## 🔷 What is Visitor Pattern?

**Visitor Pattern** is a behavioral design pattern that lets you **add new operations to an existing class hierarchy without modifying those classes**. You define the new operation in a separate "visitor" class, and each element in the hierarchy "accepts" the visitor, letting it operate on itself.

It separates **algorithms from the objects they operate on**.

---

### 🔑 Key Characteristics

| Characteristic             | Description                                                              |
|----------------------------|--------------------------------------------------------------------------|
| **Double Dispatch**        | The right method is selected based on both visitor type AND element type |
| **Open/Closed**            | Add new operations via new visitors — never touch element classes        |
| **Separation of Concerns** | Operations live in visitors, data lives in elements                      |
| **Accumulation**           | Visitors can accumulate state across the entire object structure         |
| **Non-intrusive**          | Elements only need to implement `accept(visitor)`                        |

---

### 🔥 The Problem It Solves

Without Visitor, adding a new operation to a class hierarchy forces you to modify every class:

```python
# ❌ WITHOUT Visitor — each new operation pollutes every element class
class NumberNode:
    def evaluate(self): ...    # operation 1
    def to_string(self): ...   # operation 2
    def optimize(self): ...    # operation 3
    def type_check(self): ...  # operation 4 — added to ALL classes!

class AddNode:
    def evaluate(self): ...
    def to_string(self): ...
    def optimize(self): ...
    def type_check(self): ...  # must add here too!

class MulNode:
    def evaluate(self): ...
    def to_string(self): ...
    def optimize(self): ...
    def type_check(self): ...  # and here! and every new class!

# Adding "generate_code" operation = modify ALL 3+ classes again!
```

With Visitor:

```python
# ✅ WITH Visitor — new operation = new visitor class, zero element changes
class TypeCheckVisitor:
    def visit_number(self, node): ...
    def visit_add(self, node):    ...
    def visit_mul(self, node):    ...

class CodeGenVisitor:          # brand new operation — no element changes!
    def visit_number(self, node): ...
    def visit_add(self, node):    ...
    def visit_mul(self, node):    ...

# Elements only ever need: def accept(self, visitor): visitor.visit_X(self)
```

---

### 🌍 Real-World Analogy

Think of a **tax inspector visiting different business types**:

```
Tax Inspector (Visitor)
    │
    ├── visits Restaurant → applies food service tax rules
    ├── visits Retail Shop → applies retail tax rules
    ├── visits Software Company → applies service tax rules
    └── visits Hospital → applies healthcare exemption rules
```

- The **inspector** (Visitor) carries the tax calculation logic
- Each **business** (Element) knows how to "receive" an inspector: `accept(inspector)`
- The **business type** determines which rules apply — without the inspector knowing each type in advance
- Adding a new inspector type (e.g. `HealthInspector`) never requires modifying the businesses

---

### 🖼️ Visual Representation

```
┌────────────────────────────────────────────────┐
│           Element Hierarchy                    │
│                                                │
│  ElementA              ElementB                │
│  accept(v)             accept(v)               │
│    └─► v.visit_a(self)   └─► v.visit_b(self)   │
└────────────────────┬───────────────────────────┘
                     │ calls visit_X()
          ┌──────────┴──────────┐
          ▼                     ▼
  ┌──────────────┐    ┌──────────────┐
  │  VisitorA    │    │  VisitorB    │
  │ visit_a(el)  │    │ visit_a(el)  │
  │ visit_b(el)  │    │ visit_b(el)  │
  └──────────────┘    └──────────────┘
  (Operation 1)       (Operation 2)

Double dispatch:
  element.accept(visitor)
    → visitor.visit_ElementType(element)
      → visitor runs its logic with full access to element
```

---

### 🔀 Participants

| Role                | Responsibility                                              |
|---------------------|-------------------------------------------------------------|
| **Visitor**         | Interface declaring `visit_X()` for each element type       |
| **ConcreteVisitor** | Implements the operation for each element type              |
| **Element**         | Interface declaring `accept(visitor)`                       |
| **ConcreteElement** | Implements `accept()` by calling `visitor.visit_self(self)` |
| **ObjectStructure** | Holds elements; lets the visitor traverse them              |

---

## ✅ When to Use

| Scenario                                                                 | Why It Fits                  |
|--------------------------------------------------------------------------|------------------------------|
| Need to add **many unrelated operations** to a stable hierarchy          | Each operation = one visitor |
| Class hierarchy is **stable** but operations keep changing               | Add visitors freely          |
| Operations need to **accumulate state** across multiple elements         | Visitor holds state          |
| Want to keep **element classes clean** of unrelated logic                | Operations move to visitors  |
| Need **double dispatch** — behavior based on both caller and callee type | Visitor's core mechanism     |

---

## ❌ When NOT to Use

- When the **element hierarchy changes frequently** — every new element type requires updating ALL visitors
- When there are **only 1-2 operations** that never change — direct methods on elements are simpler
- When elements need to **keep their operations private** — visitor requires exposing internals
- When the hierarchy is **very shallow** (1-2 classes) — overhead isn't justified

---

## 🏗️ Basic Implementation

### Classic Structure

```python
from __future__ import annotations
from abc import ABC, abstractmethod

# ─────────────────────────────────────────
# Visitor Interface
# ─────────────────────────────────────────
class ShapeVisitor(ABC):
    @abstractmethod
    def visit_circle(self, circle: 'Circle') -> None:
        pass

    @abstractmethod
    def visit_rectangle(self, rect: 'Rectangle') -> None:
        pass

    @abstractmethod
    def visit_triangle(self, tri: 'Triangle') -> None:
        pass


# ─────────────────────────────────────────
# Element Interface
# ─────────────────────────────────────────
class Shape(ABC):
    @abstractmethod
    def accept(self, visitor: ShapeVisitor) -> None:
        """Double dispatch: call the visitor's method for THIS type."""
        pass


# ─────────────────────────────────────────
# Concrete Elements
# ─────────────────────────────────────────
class Circle(Shape):
    def __init__(self, radius: float):
        self.radius = radius

    def accept(self, visitor: ShapeVisitor) -> None:
        visitor.visit_circle(self)   # ← dispatches to correct visitor method


class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self.width  = width
        self.height = height

    def accept(self, visitor: ShapeVisitor) -> None:
        visitor.visit_rectangle(self)


class Triangle(Shape):
    def __init__(self, base: float, height: float):
        self.base   = base
        self.height = height

    def accept(self, visitor: ShapeVisitor) -> None:
        visitor.visit_triangle(self)


# ─────────────────────────────────────────
# Concrete Visitors — each is a new operation
# ─────────────────────────────────────────
import math

class AreaCalculator(ShapeVisitor):
    def __init__(self):
        self.total_area = 0.0

    def visit_circle(self, circle: Circle) -> None:
        area = math.pi * circle.radius ** 2
        self.total_area += area
        print(f"  ⭕ Circle area: {area:.2f}")

    def visit_rectangle(self, rect: Rectangle) -> None:
        area = rect.width * rect.height
        self.total_area += area
        print(f"  ▭  Rectangle area: {area:.2f}")

    def visit_triangle(self, tri: Triangle) -> None:
        area = 0.5 * tri.base * tri.height
        self.total_area += area
        print(f"  △  Triangle area: {area:.2f}")


class PerimeterCalculator(ShapeVisitor):
    def __init__(self):
        self.total_perimeter = 0.0

    def visit_circle(self, circle: Circle) -> None:
        p = 2 * math.pi * circle.radius
        self.total_perimeter += p
        print(f"  ⭕ Circle perimeter: {p:.2f}")

    def visit_rectangle(self, rect: Rectangle) -> None:
        p = 2 * (rect.width + rect.height)
        self.total_perimeter += p
        print(f"  ▭  Rectangle perimeter: {p:.2f}")

    def visit_triangle(self, tri: Triangle) -> None:
        # Isoceles triangle approximation
        side = math.sqrt((tri.base / 2) ** 2 + tri.height ** 2)
        p    = tri.base + 2 * side
        self.total_perimeter += p
        print(f"  △  Triangle perimeter: {p:.2f}")


class SVGRenderer(ShapeVisitor):
    """New operation added with ZERO changes to element classes."""

    def __init__(self, x_offset: int = 10):
        self._x = x_offset
        self._svgs: list = []

    def visit_circle(self, circle: Circle) -> None:
        r   = int(circle.radius)
        svg = f'<circle cx="{self._x + r}" cy="{r}" r="{r}" fill="coral"/>'
        self._svgs.append(svg)
        self._x += r * 2 + 10

    def visit_rectangle(self, rect: Rectangle) -> None:
        w   = int(rect.width)
        h   = int(rect.height)
        svg = f'<rect x="{self._x}" y="0" width="{w}" height="{h}" fill="teal"/>'
        self._svgs.append(svg)
        self._x += w + 10

    def visit_triangle(self, tri: Triangle) -> None:
        b   = int(tri.base)
        h   = int(tri.height)
        pts = f"{self._x},{h} {self._x + b//2},0 {self._x + b},{h}"
        svg = f'<polygon points="{pts}" fill="purple"/>'
        self._svgs.append(svg)
        self._x += b + 10

    def render(self) -> str:
        shapes = "\n  ".join(self._svgs)
        return f'<svg xmlns="http://www.w3.org/2000/svg">\n  {shapes}\n</svg>'


# ─────────────────────────────────────────
# Object Structure
# ─────────────────────────────────────────
shapes = [
    Circle(5),
    Rectangle(4, 6),
    Triangle(8, 5),
    Circle(3),
    Rectangle(10, 2),
]

print("=== Area Calculation ===")
area_visitor = AreaCalculator()
for shape in shapes:
    shape.accept(area_visitor)
print(f"  Total area: {area_visitor.total_area:.2f}\n")

print("=== Perimeter Calculation ===")
perim_visitor = PerimeterCalculator()
for shape in shapes:
    shape.accept(perim_visitor)
print(f"  Total perimeter: {perim_visitor.total_perimeter:.2f}\n")

print("=== SVG Rendering ===")
svg_visitor = SVGRenderer()
for shape in shapes:
    shape.accept(svg_visitor)
print(svg_visitor.render())
```

---

## 🌍 Real-World Examples

### Example 1: AST Expression Evaluator

```python
from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

# ─────────────────────────────────────────
# Visitor Interface
# ─────────────────────────────────────────
class ExprVisitor(ABC):
    @abstractmethod
    def visit_number(self, node: 'NumberNode') -> Any:
        pass

    @abstractmethod
    def visit_variable(self, node: 'VariableNode') -> Any:
        pass

    @abstractmethod
    def visit_binary_op(self, node: 'BinaryOpNode') -> Any:
        pass

    @abstractmethod
    def visit_unary_op(self, node: 'UnaryOpNode') -> Any:
        pass

    @abstractmethod
    def visit_function_call(self, node: 'FunctionCallNode') -> Any:
        pass


# ─────────────────────────────────────────
# AST Node Elements
# ─────────────────────────────────────────
class ExprNode(ABC):
    @abstractmethod
    def accept(self, visitor: ExprVisitor) -> Any:
        pass


@dataclass
class NumberNode(ExprNode):
    value: float

    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visit_number(self)


@dataclass
class VariableNode(ExprNode):
    name: str

    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visit_variable(self)


@dataclass
class BinaryOpNode(ExprNode):
    op:    str        # "+", "-", "*", "/", "**", "%"
    left:  ExprNode
    right: ExprNode

    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visit_binary_op(self)


@dataclass
class UnaryOpNode(ExprNode):
    op:      str      # "-", "abs"
    operand: ExprNode

    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visit_unary_op(self)


@dataclass
class FunctionCallNode(ExprNode):
    name: str
    args: list[ExprNode]

    def accept(self, visitor: ExprVisitor) -> Any:
        return visitor.visit_function_call(self)


# ─────────────────────────────────────────
# Visitor 1: Evaluator
# ─────────────────────────────────────────
import math

class EvaluatorVisitor(ExprVisitor):
    """Evaluates the AST to a numeric result."""

    FUNCTIONS = {
        "sqrt": math.sqrt,
        "abs":  abs,
        "sin":  math.sin,
        "cos":  math.cos,
        "log":  math.log,
        "ceil": math.ceil,
        "floor": math.floor,
    }

    def __init__(self, variables: dict[str, float] = None):
        self._vars = variables or {}

    def visit_number(self, node: NumberNode) -> float:
        return node.value

    def visit_variable(self, node: VariableNode) -> float:
        if node.name not in self._vars:
            raise NameError(f"Undefined variable: '{node.name}'")
        return self._vars[node.name]

    def visit_binary_op(self, node: BinaryOpNode) -> float:
        left  = node.left.accept(self)
        right = node.right.accept(self)
        ops = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b if b != 0 else float("inf"),
            "**": lambda a, b: a ** b,
            "%": lambda a, b: a % b,
        }
        if node.op not in ops:
            raise ValueError(f"Unknown operator: '{node.op}'")
        return ops[node.op](left, right)

    def visit_unary_op(self, node: UnaryOpNode) -> float:
        val = node.operand.accept(self)
        if node.op == "-":
            return -val
        if node.op == "abs":
            return abs(val)
        raise ValueError(f"Unknown unary op: '{node.op}'")

    def visit_function_call(self, node: FunctionCallNode) -> float:
        fn = self.FUNCTIONS.get(node.name)
        if not fn:
            raise NameError(f"Unknown function: '{node.name}'")
        args = [arg.accept(self) for arg in node.args]
        return fn(*args)


# ─────────────────────────────────────────
# Visitor 2: Pretty Printer
# ─────────────────────────────────────────
class PrettyPrinterVisitor(ExprVisitor):
    """Converts AST back to a human-readable infix expression."""

    def visit_number(self, node: NumberNode) -> str:
        return str(int(node.value) if node.value == int(node.value)
                   else node.value)

    def visit_variable(self, node: VariableNode) -> str:
        return node.name

    def visit_binary_op(self, node: BinaryOpNode) -> str:
        left  = node.left.accept(self)
        right = node.right.accept(self)
        return f"({left} {node.op} {right})"

    def visit_unary_op(self, node: UnaryOpNode) -> str:
        operand = node.operand.accept(self)
        return f"({node.op}{operand})"

    def visit_function_call(self, node: FunctionCallNode) -> str:
        args = ", ".join(arg.accept(self) for arg in node.args)
        return f"{node.name}({args})"


# ─────────────────────────────────────────
# Visitor 3: Optimizer
# ─────────────────────────────────────────
class ConstantFoldingVisitor(ExprVisitor):
    """
    Optimization pass: evaluates sub-expressions made entirely of
    constants at compile-time.
    e.g. (2 + 3) * x  →  5 * x
    """

    def visit_number(self, node: NumberNode) -> ExprNode:
        return node   # already a constant

    def visit_variable(self, node: VariableNode) -> ExprNode:
        return node   # can't fold variables

    def visit_binary_op(self, node: BinaryOpNode) -> ExprNode:
        left  = node.left.accept(self)
        right = node.right.accept(self)

        # If both children are now constants → fold them
        if isinstance(left, NumberNode) and isinstance(right, NumberNode):
            evaluator = EvaluatorVisitor()
            folded    = BinaryOpNode(node.op, left, right).accept(evaluator)
            print(f"  🔧 Folded: ({left.value} {node.op} {right.value}) → {folded}")
            return NumberNode(folded)

        return BinaryOpNode(node.op, left, right)

    def visit_unary_op(self, node: UnaryOpNode) -> ExprNode:
        operand = node.operand.accept(self)
        if isinstance(operand, NumberNode):
            evaluator = EvaluatorVisitor()
            folded    = UnaryOpNode(node.op, operand).accept(evaluator)
            return NumberNode(folded)
        return UnaryOpNode(node.op, operand)

    def visit_function_call(self, node: FunctionCallNode) -> ExprNode:
        optimized_args = [arg.accept(self) for arg in node.args]
        if all(isinstance(a, NumberNode) for a in optimized_args):
            evaluator = EvaluatorVisitor()
            folded    = FunctionCallNode(node.name, optimized_args).accept(evaluator)
            return NumberNode(folded)
        return FunctionCallNode(node.name, optimized_args)


# ─────────────────────────────────────────
# Visitor 4: Variable Collector
# ─────────────────────────────────────────
class VariableCollectorVisitor(ExprVisitor):
    """Collects all variable names used in the expression."""

    def __init__(self):
        self.variables: set = set()

    def visit_number(self, node: NumberNode) -> None:
        pass

    def visit_variable(self, node: VariableNode) -> None:
        self.variables.add(node.name)

    def visit_binary_op(self, node: BinaryOpNode) -> None:
        node.left.accept(self)
        node.right.accept(self)

    def visit_unary_op(self, node: UnaryOpNode) -> None:
        node.operand.accept(self)

    def visit_function_call(self, node: FunctionCallNode) -> None:
        for arg in node.args:
            arg.accept(self)


# ─────────────────────────────────────────
# Client
# ─────────────────────────────────────────
# Build AST for: sqrt((2 + 3) * x**2 + y)
ast = FunctionCallNode("sqrt", [
    BinaryOpNode("+",
        BinaryOpNode("*",
            BinaryOpNode("+", NumberNode(2), NumberNode(3)),
            BinaryOpNode("**", VariableNode("x"), NumberNode(2))
        ),
        VariableNode("y")
    )
])

printer = PrettyPrinterVisitor()
print(f"Expression : {ast.accept(printer)}")

collector = VariableCollectorVisitor()
ast.accept(collector)
print(f"Variables  : {collector.variables}")

evaluator = EvaluatorVisitor({"x": 3.0, "y": 16.0})
result    = ast.accept(evaluator)
print(f"Evaluated  : {result:.4f}")   # sqrt((2+3)*9 + 16) = sqrt(61) ≈ 7.81

print("\n--- Constant Folding Optimization ---")
optimizer = ConstantFoldingVisitor()
optimized = ast.accept(optimizer)
print(f"Optimized  : {optimized.accept(printer)}")

# Second eval on optimized tree — constants already computed
result2 = optimized.accept(EvaluatorVisitor({"x": 3.0, "y": 16.0}))
print(f"Re-eval    : {result2:.4f}")
```

---

### Example 2: Document Exporter

```python
from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

# ─────────────────────────────────────────
# Document Element Hierarchy
# ─────────────────────────────────────────
class DocElement(ABC):
    @abstractmethod
    def accept(self, visitor: 'DocVisitor') -> str:
        pass


@dataclass
class Heading(DocElement):
    text:  str
    level: int = 1    # 1-6

    def accept(self, visitor: 'DocVisitor') -> str:
        return visitor.visit_heading(self)


@dataclass
class Paragraph(DocElement):
    text: str

    def accept(self, visitor: 'DocVisitor') -> str:
        return visitor.visit_paragraph(self)


@dataclass
class BulletList(DocElement):
    items: list[str]

    def accept(self, visitor: 'DocVisitor') -> str:
        return visitor.visit_bullet_list(self)


@dataclass
class NumberedList(DocElement):
    items: list[str]

    def accept(self, visitor: 'DocVisitor') -> str:
        return visitor.visit_numbered_list(self)


@dataclass
class CodeBlock(DocElement):
    code:     str
    language: str = "python"

    def accept(self, visitor: 'DocVisitor') -> str:
        return visitor.visit_code_block(self)


@dataclass
class Table(DocElement):
    headers: list[str]
    rows:    list[list[str]]

    def accept(self, visitor: 'DocVisitor') -> str:
        return visitor.visit_table(self)


@dataclass
class HorizontalRule(DocElement):
    def accept(self, visitor: 'DocVisitor') -> str:
        return visitor.visit_horizontal_rule(self)


@dataclass
class Document:
    title:    str
    elements: list[DocElement] = field(default_factory=list)

    def add(self, *elements: DocElement) -> 'Document':
        self.elements.extend(elements)
        return self

    def export(self, visitor: 'DocVisitor') -> str:
        parts = [visitor.visit_document_start(self)]
        for el in self.elements:
            parts.append(el.accept(visitor))
        parts.append(visitor.visit_document_end(self))
        return "\n".join(p for p in parts if p is not None)


# ─────────────────────────────────────────
# Visitor Interface
# ─────────────────────────────────────────
class DocVisitor(ABC):
    @abstractmethod
    def visit_document_start(self, doc: Document) -> str:
        pass

    @abstractmethod
    def visit_document_end(self, doc: Document) -> str:
        pass

    @abstractmethod
    def visit_heading(self, el: Heading) -> str:
        pass

    @abstractmethod
    def visit_paragraph(self, el: Paragraph) -> str:
        pass

    @abstractmethod
    def visit_bullet_list(self, el: BulletList) -> str:
        pass

    @abstractmethod
    def visit_numbered_list(self, el: NumberedList) -> str:
        pass

    @abstractmethod
    def visit_code_block(self, el: CodeBlock) -> str:
        pass

    @abstractmethod
    def visit_table(self, el: Table) -> str:
        pass

    @abstractmethod
    def visit_horizontal_rule(self, el: HorizontalRule) -> str:
        pass


# ─────────────────────────────────────────
# Concrete Visitor: Markdown Exporter
# ─────────────────────────────────────────
class MarkdownVisitor(DocVisitor):

    def visit_document_start(self, doc: Document) -> str:
        return f"# {doc.title}\n"

    def visit_document_end(self, doc: Document) -> str:
        return ""

    def visit_heading(self, el: Heading) -> str:
        return f"{'#' * el.level} {el.text}\n"

    def visit_paragraph(self, el: Paragraph) -> str:
        return f"{el.text}\n"

    def visit_bullet_list(self, el: BulletList) -> str:
        items = "\n".join(f"- {item}" for item in el.items)
        return f"{items}\n"

    def visit_numbered_list(self, el: NumberedList) -> str:
        items = "\n".join(f"{i}. {item}" for i, item in enumerate(el.items, 1))
        return f"{items}\n"

    def visit_code_block(self, el: CodeBlock) -> str:
        return f"```{el.language}\n{el.code}\n```\n"

    def visit_table(self, el: Table) -> str:
        header = "| " + " | ".join(el.headers) + " |"
        sep    = "| " + " | ".join("---" for _ in el.headers) + " |"
        rows   = "\n".join(
            "| " + " | ".join(row) + " |" for row in el.rows
        )
        return f"{header}\n{sep}\n{rows}\n"

    def visit_horizontal_rule(self, el: HorizontalRule) -> str:
        return "---\n"


# ─────────────────────────────────────────
# Concrete Visitor: HTML Exporter
# ─────────────────────────────────────────
class HTMLVisitor(DocVisitor):

    def visit_document_start(self, doc: Document) -> str:
        return (
            f"<!DOCTYPE html><html><head><meta charset='utf-8'>"
            f"<title>{doc.title}</title>"
            f"<style>body{{font-family:sans-serif;max-width:800px;margin:40px auto}}"
            f"pre{{background:#f4f4f4;padding:16px;border-radius:4px}}"
            f"table{{border-collapse:collapse;width:100%}}"
            f"td,th{{border:1px solid #ddd;padding:10px;text-align:left}}"
            f"th{{background:#f0f0f0}}</style></head><body>"
            f"<h1>{doc.title}</h1>"
        )

    def visit_document_end(self, doc: Document) -> str:
        return "</body></html>"

    def visit_heading(self, el: Heading) -> str:
        return f"<h{el.level}>{el.text}</h{el.level}>"

    def visit_paragraph(self, el: Paragraph) -> str:
        return f"<p>{el.text}</p>"

    def visit_bullet_list(self, el: BulletList) -> str:
        items = "".join(f"<li>{item}</li>" for item in el.items)
        return f"<ul>{items}</ul>"

    def visit_numbered_list(self, el: NumberedList) -> str:
        items = "".join(f"<li>{item}</li>" for item in el.items)
        return f"<ol>{items}</ol>"

    def visit_code_block(self, el: CodeBlock) -> str:
        return f"<pre><code class='language-{el.language}'>{el.code}</code></pre>"

    def visit_table(self, el: Table) -> str:
        headers = "".join(f"<th>{h}</th>" for h in el.headers)
        rows    = "".join(
            "<tr>" + "".join(f"<td>{cell}</td>" for cell in row) + "</tr>"
            for row in el.rows
        )
        return f"<table><thead><tr>{headers}</tr></thead><tbody>{rows}</tbody></table>"

    def visit_horizontal_rule(self, el: HorizontalRule) -> str:
        return "<hr>"


# ─────────────────────────────────────────
# Concrete Visitor: Word Count Analyzer
# ─────────────────────────────────────────
class WordCountVisitor(DocVisitor):
    """Traverses the document collecting statistics — no rendering."""

    def __init__(self):
        self.word_count    = 0
        self.heading_count = 0
        self.code_lines    = 0
        self.table_rows    = 0
        self.list_items    = 0

    def _count_words(self, text: str) -> int:
        return len(text.split())

    def visit_document_start(self, doc: Document) -> str:
        self.word_count += self._count_words(doc.title)
        return ""

    def visit_document_end(self, doc: Document) -> str:
        return ""

    def visit_heading(self, el: Heading) -> str:
        self.word_count    += self._count_words(el.text)
        self.heading_count += 1
        return ""

    def visit_paragraph(self, el: Paragraph) -> str:
        self.word_count += self._count_words(el.text)
        return ""

    def visit_bullet_list(self, el: BulletList) -> str:
        for item in el.items:
            self.word_count += self._count_words(item)
            self.list_items += 1
        return ""

    def visit_numbered_list(self, el: NumberedList) -> str:
        for item in el.items:
            self.word_count += self._count_words(item)
            self.list_items += 1
        return ""

    def visit_code_block(self, el: CodeBlock) -> str:
        self.code_lines += el.code.count("\n") + 1
        return ""

    def visit_table(self, el: Table) -> str:
        self.table_rows += len(el.rows)
        return ""

    def visit_horizontal_rule(self, el: HorizontalRule) -> str:
        return ""

    def report(self) -> str:
        return (
            f"\n  📊 Document Statistics:\n"
            f"     Words    : {self.word_count}\n"
            f"     Headings : {self.heading_count}\n"
            f"     List items: {self.list_items}\n"
            f"     Code lines: {self.code_lines}\n"
            f"     Table rows: {self.table_rows}"
        )


# ─────────────────────────────────────────
# Client
# ─────────────────────────────────────────
doc = (Document("Python Design Patterns Guide")
    .add(
        Heading("Introduction", level=2),
        Paragraph("Design patterns are reusable solutions to common problems."),
        Heading("Creational Patterns", level=3),
        BulletList(["Singleton", "Factory", "Builder", "Prototype"]),
        Heading("Code Example", level=3),
        CodeBlock(
            "class Singleton:\n    _instance = None\n\n"
            "    def __new__(cls):\n        if not cls._instance:\n"
            "            cls._instance = super().__new__(cls)\n"
            "        return cls._instance",
            language="python"
        ),
        HorizontalRule(),
        Heading("Pattern Comparison", level=2),
        Table(
            headers=["Pattern",    "Type",       "Key Benefit"],
            rows=[
                ["Visitor",    "Behavioral", "Add operations without modifying classes"],
                ["Strategy",   "Behavioral", "Swap algorithms at runtime"],
                ["Observer",   "Behavioral", "Automatic change notification"],
            ]
        ),
        NumberedList([
            "Understand the problem before choosing a pattern",
            "Prefer composition over inheritance",
            "Keep it simple — don't over-engineer",
        ])
    )
)

print("=== Markdown Export ===\n")
md = doc.export(MarkdownVisitor())
print(md)

print("=== HTML Export (preview) ===\n")
html = doc.export(HTMLVisitor())
print(html[:400] + "...")

print("=== Word Count Analysis ===")
wc = WordCountVisitor()
doc.export(wc)
print(wc.report())
```

---

### Example 3: E-Commerce Tax & Discount Engine

```python
from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any
from enum import Enum

class ProductCategory(Enum):
    ELECTRONICS  = "electronics"
    FOOD         = "food"
    CLOTHING     = "clothing"
    BOOKS        = "books"
    LUXURY       = "luxury"
    MEDICINE     = "medicine"


@dataclass
class Product:
    name:     str
    price:    float
    category: ProductCategory
    quantity: int = 1

    def accept(self, visitor: 'CartVisitor') -> Any:
        return visitor.visit_product(self)


@dataclass
class Bundle:
    name:     str
    products: list[Product]
    discount: float = 0.10   # 10% bundle discount

    def accept(self, visitor: 'CartVisitor') -> Any:
        return visitor.visit_bundle(self)

    @property
    def subtotal(self) -> float:
        return sum(p.price * p.quantity for p in self.products)


@dataclass
class GiftCard:
    code:   str
    value:  float
    used:   bool = False

    def accept(self, visitor: 'CartVisitor') -> Any:
        return visitor.visit_gift_card(self)


@dataclass
class ShippingOption:
    method:   str    # "standard", "express", "overnight"
    base_fee: float

    def accept(self, visitor: 'CartVisitor') -> Any:
        return visitor.visit_shipping(self)


# ─────────────────────────────────────────
# Visitor Interface
# ─────────────────────────────────────────
class CartVisitor(ABC):
    @abstractmethod
    def visit_product(self, product: Product) -> Any:
        pass

    @abstractmethod
    def visit_bundle(self, bundle: Bundle) -> Any:
        pass

    @abstractmethod
    def visit_gift_card(self, card: GiftCard) -> Any:
        pass

    @abstractmethod
    def visit_shipping(self, shipping: ShippingOption) -> Any:
        pass


# ─────────────────────────────────────────
# Visitor 1: Tax Calculator
# ─────────────────────────────────────────
class TaxCalculatorVisitor(CartVisitor):
    """
    Applies region-specific tax rules to each cart item type.
    Each product category may have different tax rates.
    """

    TAX_RATES: dict[ProductCategory, float] = {
        ProductCategory.ELECTRONICS: 0.15,
        ProductCategory.FOOD:        0.00,   # food exempt
        ProductCategory.CLOTHING:    0.08,
        ProductCategory.BOOKS:       0.00,   # books exempt
        ProductCategory.LUXURY:      0.22,   # luxury surcharge
        ProductCategory.MEDICINE:    0.00,   # medicine exempt
    }

    def __init__(self, region: str = "US"):
        self.region    = region
        self.tax_total = 0.0
        self._breakdown: list[str] = []

    def visit_product(self, product: Product) -> float:
        rate    = self.TAX_RATES.get(product.category, 0.10)
        tax     = product.price * product.quantity * rate
        self.tax_total += tax
        if tax > 0:
            self._breakdown.append(
                f"  {product.name}: ${tax:.2f} ({rate*100:.0f}%)"
            )
        return tax

    def visit_bundle(self, bundle: Bundle) -> float:
        total_tax = 0.0
        for product in bundle.products:
            total_tax += self.visit_product(product)
        # Bundles get a small tax credit
        credit = total_tax * 0.05
        self.tax_total -= credit
        total_tax      -= credit
        self._breakdown.append(f"  Bundle tax credit: -${credit:.2f}")
        return total_tax

    def visit_gift_card(self, card: GiftCard) -> float:
        return 0.0   # gift cards not taxed

    def visit_shipping(self, shipping: ShippingOption) -> float:
        tax = shipping.base_fee * 0.05   # 5% shipping tax
        self.tax_total += tax
        self._breakdown.append(f"  Shipping tax: ${tax:.2f}")
        return tax

    def report(self) -> str:
        lines = [f"\n  🧾 Tax Breakdown ({self.region}):"]
        lines.extend(self._breakdown)
        lines.append(f"  Total Tax: ${self.tax_total:.2f}")
        return "\n".join(lines)


# ─────────────────────────────────────────
# Visitor 2: Discount Calculator
# ─────────────────────────────────────────
class DiscountVisitor(CartVisitor):
    """
    Applies promotion rules:
    - Books: 15% off
    - Bundles: explicit bundle discount
    - Gift cards: face value deducted
    - Express shipping: 20% off if cart > $200
    """

    def __init__(self, cart_subtotal: float = 0.0):
        self._cart_subtotal  = cart_subtotal
        self.total_discount  = 0.0
        self._breakdown: list[str] = []

    def visit_product(self, product: Product) -> float:
        discount = 0.0
        if product.category == ProductCategory.BOOKS:
            discount = product.price * product.quantity * 0.15
            self._breakdown.append(
                f"  {product.name}: -${discount:.2f} (15% books discount)"
            )
        self.total_discount += discount
        return discount

    def visit_bundle(self, bundle: Bundle) -> float:
        discount = bundle.subtotal * bundle.discount
        self.total_discount += discount
        self._breakdown.append(
            f"  Bundle '{bundle.name}': -${discount:.2f} "
            f"({bundle.discount*100:.0f}% bundle deal)"
        )
        return discount

    def visit_gift_card(self, card: GiftCard) -> float:
        if not card.used:
            self.total_discount += card.value
            self._breakdown.append(
                f"  Gift card {card.code}: -${card.value:.2f}"
            )
            return card.value
        return 0.0

    def visit_shipping(self, shipping: ShippingOption) -> float:
        if (shipping.method == "express" and
                self._cart_subtotal > 200):
            discount = shipping.base_fee * 0.20
            self.total_discount += discount
            self._breakdown.append(
                f"  Express shipping discount: -${discount:.2f} "
                f"(20% off, cart > $200)"
            )
            return discount
        return 0.0

    def report(self) -> str:
        lines = ["\n  🏷️  Discount Breakdown:"]
        lines.extend(self._breakdown or ["  No discounts applied"])
        lines.append(f"  Total Discounts: -${self.total_discount:.2f}")
        return "\n".join(lines)


# ─────────────────────────────────────────
# Visitor 3: Cart Summarizer
# ─────────────────────────────────────────
class CartSummaryVisitor(CartVisitor):
    """Produces a human-readable receipt."""

    def __init__(self):
        self.subtotal = 0.0
        self._lines:  list[str] = []

    def visit_product(self, product: Product) -> float:
        line_total = product.price * product.quantity
        self.subtotal += line_total
        self._lines.append(
            f"  {product.quantity}x {product.name:<25} "
            f"@ ${product.price:.2f} = ${line_total:.2f}"
        )
        return line_total

    def visit_bundle(self, bundle: Bundle) -> float:
        self._lines.append(f"  📦 Bundle: {bundle.name}")
        total = 0.0
        for p in bundle.products:
            lt = p.price * p.quantity
            total += lt
            self._lines.append(f"     • {p.quantity}x {p.name} = ${lt:.2f}")
        savings = total * bundle.discount
        self.subtotal += total - savings
        self._lines.append(
            f"     Bundle saving: -${savings:.2f} | "
            f"Net: ${total - savings:.2f}"
        )
        return total - savings

    def visit_gift_card(self, card: GiftCard) -> float:
        self._lines.append(
            f"  🎁 Gift Card {card.code}: -${card.value:.2f}"
        )
        self.subtotal -= card.value
        return -card.value

    def visit_shipping(self, shipping: ShippingOption) -> float:
        self._lines.append(
            f"  🚚 Shipping ({shipping.method}): ${shipping.base_fee:.2f}"
        )
        self.subtotal += shipping.base_fee
        return shipping.base_fee

    def receipt(self, tax: float, discounts: float) -> str:
        lines = ["\n  🧾 Cart Receipt", "  " + "─" * 45]
        lines.extend(self._lines)
        lines.append("  " + "─" * 45)
        lines.append(f"  {'Subtotal':<30} ${self.subtotal:.2f}")
        lines.append(f"  {'Discounts':<30} -${discounts:.2f}")
        lines.append(f"  {'Tax':<30} +${tax:.2f}")
        grand_total = self.subtotal - discounts + tax
        lines.append("  " + "─" * 45)
        lines.append(f"  {'TOTAL':<30} ${grand_total:.2f}")
        return "\n".join(lines)


# ─────────────────────────────────────────
# Shopping Cart (Object Structure)
# ─────────────────────────────────────────
class ShoppingCart:
    def __init__(self):
        self._items: List = []

    def add(self, *items) -> 'ShoppingCart':
        self._items.extend(items)
        return self

    def checkout(self) -> None:
        # Pass each visitor over all items
        summary   = CartSummaryVisitor()
        tax_calc  = TaxCalculatorVisitor(region="US")
        discounts = DiscountVisitor(
            cart_subtotal=sum(
                (p.price * p.quantity if isinstance(p, Product)
                 else p.subtotal if isinstance(p, Bundle)
                 else 0)
                for p in self._items
            )
        )

        for item in self._items:
            item.accept(summary)
            item.accept(tax_calc)
            item.accept(discounts)

        print(summary.receipt(tax_calc.tax_total, discounts.total_discount))
        print(tax_calc.report())
        print(discounts.report())


# ─────────────────────────────────────────
# Client
# ─────────────────────────────────────────
cart = ShoppingCart()
cart.add(
    Product("Python Cookbook",        49.99, ProductCategory.BOOKS,        qty=2),
    Product("Mechanical Keyboard",    89.00, ProductCategory.ELECTRONICS,  qty=1),
    Product("Paracetamol 500mg",       5.99, ProductCategory.MEDICINE,     qty=3),
    Bundle("Developer Starter Pack", [
        Product("Clean Code Book",    34.99, ProductCategory.BOOKS),
        Product("USB-C Hub",          29.99, ProductCategory.ELECTRONICS),
        Product("Notebook",            9.99, ProductCategory.BOOKS),
    ], discount=0.12),
    GiftCard("GIFT-XYZ-100", value=20.00),
    ShippingOption("express", base_fee=12.99),
)

cart.checkout()
```

---

## ⚠️ Common Pitfalls

### ❌ Pitfall 1: Missing `accept()` in a New Element

```python
# ❌ WRONG — new element added to hierarchy without accept()
class Pentagon(Shape):
    def __init__(self, side: float):
        self.side = side
    # forgot accept()! Visitor can never reach Pentagon.

# ✅ CORRECT — every concrete element MUST implement accept()
class Pentagon(Shape):
    def __init__(self, side: float):
        self.side = side

    def accept(self, visitor: ShapeVisitor) -> None:
        visitor.visit_pentagon(self)   # and visitor must add visit_pentagon()!
```

### ❌ Pitfall 2: Visitor Breaking When Element Hierarchy Grows

```python
# ❌ PROBLEM — adding Pentagon forces ALL existing visitors to update
class AreaCalculator(ShapeVisitor):
    ...
    def visit_pentagon(self, p: Pentagon) -> None: ...  # must add here

class PerimeterCalculator(ShapeVisitor):
    ...
    def visit_pentagon(self, p: Pentagon) -> None: ...  # and here

class SVGRenderer(ShapeVisitor):
    ...
    def visit_pentagon(self, p: Pentagon) -> None: ...  # and here!

# ✅ MITIGATE — provide default implementations in base Visitor
class ShapeVisitor(ABC):
    def visit_pentagon(self, p: 'Pentagon') -> None:
        raise NotImplementedError(
            f"{self.__class__.__name__} does not support Pentagon"
        )
```

### ❌ Pitfall 3: Visitor Accessing Private Element State

```python
import math
# ❌ WRONG — visitor reaches into private internals
class BadVisitor(ShapeVisitor):
    def visit_circle(self, c: Circle) -> float:
        return math.pi * c._internal_radius ** 2   # private attribute!

# ✅ CORRECT — elements expose only what visitors need via public properties
class Circle(Shape):
    def __init__(self, radius: float):
        self._radius = radius

    @property
    def radius(self) -> float:       # public interface for visitors
        return self._radius
```

### ❌ Pitfall 4: Using Visitor for a Single Operation

```python
import math
# ❌ OVERKILL — visitor pattern for just one operation
class AreaVisitor(ShapeVisitor):
    def visit_circle(self, c): ...
    def visit_rectangle(self, r): ...

# If area is the ONLY operation and it never changes:
# ✅ SIMPLER — just add area() to each Shape directly
class Circle(Shape):
    def area(self) -> float:
        return math.pi * self.radius ** 2
# Visitor only pays off when you have MULTIPLE operations on a stable hierarchy.
```

---

## ✅ Best Practices

### 1. Provide Default `visit_X` in Base Visitor

```python
from abc import abstractmethod
from typing import Any

class ShapeVisitor(ABC):
    def _unsupported(self, element) -> None:
        raise NotImplementedError(
            f"'{self.__class__.__name__}' does not handle "
            f"'{type(element).__name__}'"
        )

    # Abstract only for known types; default raises for unexpected ones
    @abstractmethod
    def visit_circle(self, c: Circle) -> Any: pass

    @abstractmethod
    def visit_rectangle(self, r: Rectangle) -> Any: pass

    def visit_pentagon(self, p) -> Any:
        self._unsupported(p)   # graceful error, not silent failure
```

### 2. Use Return Values, Not Side Effects

```python
import math

# ✅ Returning values makes visitors composable and testable
class AreaCalculator(ShapeVisitor):
    def visit_circle(self, c: Circle) -> float:
        return math.pi * c.radius ** 2   # pure — no state mutation

# vs accumulating state (fine for aggregation, but harder to test):
class TotalAreaVisitor(ShapeVisitor):
    def __init__(self):
        self.total = 0.0

    def visit_circle(self, c: Circle) -> None:
        self.total += math.pi * c.radius ** 2   # accumulates state
```

### 3. Keep `accept()` Identical Across All Elements

```python
from typing import Any
# ✅ accept() is always the same one-liner — never put logic here
class Circle(Shape):
    def accept(self, visitor: ShapeVisitor) -> Any:
        return visitor.visit_circle(self)   # that's ALL it does

# ❌ Never add logic to accept()
class BadCircle(Shape):
    def accept(self, visitor: ShapeVisitor) -> Any:
        if self.radius <= 0:           # ← business logic in accept!
            raise ValueError(...)      # ← wrong place for this
        return visitor.visit_circle(self)
```

### 4. Name `visit_X` Methods After the Element Type

```python
from typing import Any
# ✅ Naming convention makes the double dispatch clear
def visit_number_node(self, node: NumberNode) -> Any: ...
def visit_binary_op_node(self, node: BinaryOpNode) -> Any: ...

# ❌ Generic names break the contract
def visit(self, node) -> Any: ...   # which node type? requires isinstance!
```

---

## 📊 Summary

| Aspect             | Detail                                                                 |
|--------------------|------------------------------------------------------------------------|
| **Type**           | Behavioral                                                             |
| **Intent**         | Add operations to a class hierarchy without modifying it               |
| **Key Mechanism**  | Double dispatch via `accept(visitor)` → `visitor.visit_X(self)`        |
| **Best For**       | Stable hierarchy, many changing operations                             |
| **Worst For**      | Frequently changing hierarchy, few operations                          |
| **Real-world Use** | AST processing, document export, tax engines, compilers, code analysis |

---

## ✅ Visitor Pattern Checklist


- Does every ConcreteElement implement accept() as a one-liner?
- Does accept() call the SPECIFIC visitor method (visit_circle, not visit_shape)?
- Does the Visitor interface declare visit_X() for every element type?
- Does the base Visitor provide default implementations for extensibility?
- Are elements' internals exposed only via public properties, not private fields?
- Is the element hierarchy stable? (If not, consider a different pattern)
- Are there multiple operations that justify the visitor abstraction overhead?
- Do visitors return values (composable) rather than only mutating state?

---

## 💡 Key Takeaways

1. **Double dispatch** is the core mechanism — `element.accept(visitor)` calls `visitor.visit_ElementType(element)`, routing on both types
2. **Add operations freely** — every new operation is a new visitor class; element classes never change
3. **Stable hierarchy required** — adding a new element type forces ALL visitors to update
4. **Visitors accumulate state** — perfect for aggregations (total area, word count, tax total)
5. **Keep `accept()` a one-liner** — all logic belongs in the visitor, never in `accept()`
6. **Key difference from Strategy** — Visitor operates across an entire object structure; Strategy swaps one algorithm on one context

---

## 🎉 Complete Behavioral Patterns Reference

You have now covered all **10 behavioral patterns**. Here is the full reference:

| #  | Pattern                     | Intent                                                    | Key Mechanism                             |
|----|-----------------------------|-----------------------------------------------------------|-------------------------------------------|
| 1  | **Chain of Responsibility** | Pass request along a handler chain                        | Each handler processes or forwards        |
| 2  | **Command**                 | Encapsulate request as an object                          | `execute()` / `undo()` on command objects |
| 3  | **Iterator**                | Traverse collection without exposing internals            | `__iter__` / `__next__` protocol          |
| 4  | **Mediator**                | Replace O(n²) peer links with O(n) hub                    | All components talk through one mediator  |
| 5  | **Memento**                 | Snapshot and restore state without breaking encapsulation | Originator creates opaque snapshots       |
| 6  | **Observer**                | Notify many dependents on one object's change             | `attach` / `detach` / `notify`            |
| 7  | **State**                   | Object changes behavior when state changes                | Delegate to current state object          |
| 8  | **Strategy**                | Make algorithms interchangeable                           | Inject and swap strategy objects          |
| 9  | **Template Method**         | Lock algorithm skeleton, defer steps to subclasses        | `final` template method + abstract hooks  |
| 10 | **Visitor**                 | Add operations to hierarchy without modifying it          | Double dispatch via `accept(visitor)`     |

---

### 🔍 Quick Selection Guide

```
Need undo/redo?
  → Command (stores operations) or Memento (stores state snapshots)

Need to traverse a collection uniformly?
  → Iterator

Need event-driven notifications?
  → Observer (one-to-many) or Mediator (many-to-many through hub)

Need to swap algorithms at runtime?
  → Strategy

Need behavior to change with lifecycle?
  → State

Need to add operations to a stable class hierarchy?
  → Visitor

Need to reuse an algorithm skeleton with variable steps?
  → Template Method

Need to decouple sender from receiver in a pipeline?
  → Chain of Responsibility
```