# Composite Pattern - Complete Guide

## 📋 Table of Contents
- [What is Composite Pattern?](#what-is-composite-pattern)
  - [Key Characteristics](#key-characteristics)
  - [Real-World Analogy](#real-world-analogy)
  - [Visual Representation](#visual-representation)
  - [Composite Structure](#composite-structure)
- [When to Use](#when-to-use)
  - [✅ Perfect Use Cases](#-perfect-use-cases)
- [When NOT to Use](#when-not-to-use)
  - [❌ Avoid Composite When](#-avoid-composite-when)
- [Basic Implementation](#basic-implementation)
  - [Classic Composite Structure](#classic-composite-structure)
- [Real-World Examples](#real-world-examples)
  - [Example 1: File System](#example-1-file-system)
  - [Example 2: Organization Hierarchy](#example-2-organization-hierarchy)
  - [Example 3: GUI Component System](#example-3-gui-component-system)
- [Common Pitfalls](#common-pitfalls)
  - [❌ Pitfall 1: Making Leaf Operations in Composite Optional](#-pitfall-1-making-leaf-operations-in-composite-optional)
  - [❌ Pitfall 2: Not Handling Recursion Depth](#-pitfall-2-not-handling-recursion-depth)
  - [❌ Pitfall 3: Parent References Cause Circular Dependencies](#-pitfall-3-parent-references-cause-circular-dependencies)
  - [❌ Pitfall 4: Composite Operations Are Too Different](#-pitfall-4-composite-operations-are-too-different)
- [Best Practices](#best-practices)
  - [✅ 1. Keep Component Interface Minimal](#-1-keep-component-interface-minimal)
  - [✅ 2. Use Type Hints](#-2-use-type-hints)
  - [✅ 3. Provide Safe Child Access](#-3-provide-safe-child-access)
  - [✅ 4. Consider Caching for Expensive Operations](#-4-consider-caching-for-expensive-operations)
  - [✅ 5. Document Tree Structure](#-5-document-tree-structure)
- [Summary](#summary)
- [Composite Pattern Checklist](#composite-pattern-checklist)
- [Key Takeaways](#key-takeaways)
---

## What is Composite Pattern?

**Composite Pattern** lets you compose objects into tree structures to represent part-whole hierarchies. It allows clients to treat individual objects and compositions of objects uniformly.

### Key Characteristics:
- ✅ Represents part-whole hierarchies (tree structures)
- ✅ Treats individual objects and compositions uniformly
- ✅ Recursive composition
- ✅ Simplifies client code
- ✅ Makes it easy to add new component types

### The Problem Composite Solves

**Without Composite:**
```python
# Client must know if it's dealing with single item or collection
class File:
   
    def display(self):
       pass
    
class Folder:
   
   def children(self):
      pass
   
item = File()

if isinstance(item, File):
    item.display()
elif isinstance(item, Folder):
    for child in item.children:
        if isinstance(child, File):
            child.display()
        elif isinstance(child, Folder):
            # More nested logic...
            pass
```

**With Composite:**
```python
# Client treats everything uniformly
class File:
   
    def display(self):
       pass
    
item = File()
item.display()  # Works for both File and Folder!
```

### Real-World Analogy:
Think of a **file system**:
- **Leaf:** Individual files (can't contain other items)
- **Composite:** Folders (can contain files and other folders)
- **Both:** Can be displayed, moved, deleted, etc.

You interact with files and folders the same way. You don't need different code to handle a file vs. a folder full of files.

### Visual Representation:
```
Component (interface)
    ↓
    ├── Leaf (individual object)
    └── Composite (contains components)
            ├── Leaf
            ├── Leaf
            └── Composite
                    ├── Leaf
                    └── Leaf

Tree structure where:
- Leaf: Can't have children
- Composite: Can have children (leaves or composites)
```

### Composite Structure

```
        Component
        /       \
     Leaf    Composite
              /   |   \
           Leaf Leaf Composite
                      /    \
                   Leaf   Leaf
```

---

## When to Use

### ✅ Perfect Use Cases:

#### 1. **Part-Whole Hierarchies (Tree Structures)**
- File systems (files and folders)
- Organization charts (employees and departments)
- GUI components (buttons, panels, windows)
- Document structures (paragraphs, sections, chapters)

#### 2. **Treat Objects Uniformly**
- Client shouldn't distinguish between individual and composite objects
- Same operations apply to both
- Recursive structures

#### 3. **Operations on Tree Structures**
- Calculate total (sum of all nodes)
- Search (find in tree)
- Render (display tree)
- Operations that work recursively

#### 4. **Dynamic Tree Building**
- Structure can change at runtime
- Add/remove components dynamically
- Flexible composition

---

## When NOT to Use

### ❌ Avoid Composite When:

1. **No Hierarchy**
   - Flat structure (just a list)
   - No parent-child relationships
   - No need for tree operations

2. **Operations Differ Significantly**
   - Leaf and composite have very different operations
   - Can't treat uniformly
   - Would need lots of type checking

3. **Simple Two-Level Structure**
   - Just parent and children
   - No deep nesting needed
   - Simple list/array suffices

4. **Performance Critical**
   - Recursive operations are expensive
   - Deep trees cause stack overflow
   - Need optimized flat structure

---

## Basic Implementation

### Classic Composite Structure

```python
from abc import ABC, abstractmethod
from typing import List

# ============ COMPONENT (Interface) ============

class Component(ABC):
    """
    Base interface for both Leaf and Composite.
    Declares operations common to both simple and complex objects.
    """
    
    def __init__(self, name: str):
        self.name = name
    
    @abstractmethod
    def operation(self) -> str:
        """
        Operation that both Leaf and Composite must implement.
        """
        pass
    
    def add(self, component: 'Component'):
        """
        Optional: Add a child component.
        Only makes sense for Composite.
        """
        raise NotImplementedError("Cannot add to a leaf")
    
    def remove(self, component: 'Component'):
        """
        Optional: Remove a child component.
        """
        raise NotImplementedError("Cannot remove from a leaf")
    
    def get_child(self, index: int) -> 'Component':
        """
        Optional: Get child by index.
        """
        raise NotImplementedError("Leaf has no children")

# ============ LEAF ============

class Leaf(Component):
    """
    Leaf represents end objects (no children).
    Implements the Component interface.
    """
    
    def operation(self) -> str:
        return f"Leaf: {self.name}"

# ============ COMPOSITE ============

class Composite(Component):
    """
    Composite represents complex objects (can have children).
    Stores child components and implements child-related operations.
    """
    
    def __init__(self, name: str):
        super().__init__(name)
        self._children: List[Component] = []
    
    def add(self, component: Component):
        """Add a child component."""
        self._children.append(component)
    
    def remove(self, component: Component):
        """Remove a child component."""
        self._children.remove(component)
    
    def get_child(self, index: int) -> Component:
        """Get child by index."""
        return self._children[index]
    
    def operation(self) -> str:
        """
        Composite executes operation and delegates to all children.
        """
        results = [f"Composite: {self.name}"]
        
        # Recursively call operation on all children
        for child in self._children:
            results.append("  " + child.operation())
        
        return "\n".join(results)

# ============ CLIENT CODE ============

def client_code(component: Component):
    """
    Client works with components through the Component interface.
    It doesn't care if it's a Leaf or Composite.
    """
    print(component.operation())

# Create simple leaf
simple = Leaf("Simple Leaf")
print("Client: I have a simple component:")
client_code(simple)

print("\n")

# Create tree structure
tree = Composite("Root")
branch1 = Composite("Branch 1")
branch1.add(Leaf("Leaf 1-1"))
branch1.add(Leaf("Leaf 1-2"))

branch2 = Composite("Branch 2")
branch2.add(Leaf("Leaf 2-1"))

tree.add(branch1)
tree.add(branch2)
tree.add(Leaf("Leaf at root"))

print("Client: I have a tree structure:")
client_code(tree)

print("\n")

# Client treats both uniformly
print("Client: I don't need to check if component is simple or composite:")
components = [simple, tree]
for component in components:
    client_code(component)
    print()
```

**Output:**
```
Client: I have a simple component:
Leaf: Simple Leaf


Client: I have a tree structure:
Composite: Root
  Composite: Branch 1
    Leaf: Leaf 1-1
    Leaf: Leaf 1-2
  Composite: Branch 2
    Leaf: Leaf 2-1
  Leaf: Leaf at root


Client: I don't need to check if component is simple or composite:
Leaf: Simple Leaf

Composite: Root
  Composite: Branch 1
    Leaf: Leaf 1-1
    Leaf: Leaf 1-2
  Composite: Branch 2
    Leaf: Leaf 2-1
  Leaf: Leaf at root
```

---

## Real-World Examples

### Example 1: File System

```python
from abc import ABC, abstractmethod
from typing import List
from datetime import datetime

# ============ COMPONENT ============

class FileSystemComponent(ABC):
    """Base component for file system"""
    
    def __init__(self, name: str):
        self.name = name
        self.created_at = datetime.now()
    
    @abstractmethod
    def get_size(self) -> int:
        """Get size in bytes"""
        pass
    
    @abstractmethod
    def display(self, indent: int = 0):
        """Display the component"""
        pass
    
    @abstractmethod
    def search(self, name: str) -> List['FileSystemComponent']:
        """Search for items by name"""
        pass

# ============ LEAF (File) ============

class File(FileSystemComponent):
    """
    Leaf: Individual file.
    Cannot contain other components.
    """
    
    def __init__(self, name: str, size: int, content: str = ""):
        super().__init__(name)
        self._size = size
        self.content = content
    
    def get_size(self) -> int:
        """Return file size"""
        return self._size
    
    def display(self, indent: int = 0):
        """Display file info"""
        prefix = "  " * indent
        print(f"{prefix}📄 {self.name} ({self._size} bytes)")
    
    def search(self, name: str) -> List['FileSystemComponent']:
        """Search - check if this file matches"""
        if name.lower() in self.name.lower():
            return [self]
        return []
    
    def read(self) -> str:
        """Read file content"""
        return self.content
    
    def write(self, content: str):
        """Write to file"""
        self.content = content
        self._size = len(content)

# ============ COMPOSITE (Folder) ============

class Folder(FileSystemComponent):
    """
    Composite: Folder that can contain files and other folders.
    """
    
    def __init__(self, name: str):
        super().__init__(name)
        self._children: List[FileSystemComponent] = []
    
    def add(self, component: FileSystemComponent):
        """Add a file or folder"""
        self._children.append(component)
        print(f"✅ Added {component.name} to {self.name}")
    
    def remove(self, component: FileSystemComponent):
        """Remove a file or folder"""
        self._children.remove(component)
        print(f"❌ Removed {component.name} from {self.name}")
    
    def get_children(self) -> List[FileSystemComponent]:
        """Get all children"""
        return self._children.copy()
    
    def get_size(self) -> int:
        """
        Get total size of folder (sum of all contents).
        Recursive operation.
        """
        total = 0
        for child in self._children:
            total += child.get_size()
        return total
    
    def display(self, indent: int = 0):
        """
        Display folder and all contents recursively.
        """
        prefix = "  " * indent
        size = self.get_size()
        print(f"{prefix}📁 {self.name}/ ({size} bytes)")
        
        # Recursively display all children
        for child in self._children:
            child.display(indent + 1)
    
    def search(self, name: str) -> List[FileSystemComponent]:
        """
        Search recursively through folder.
        """
        results = []
        
        # Check if folder itself matches
        if name.lower() in self.name.lower():
            results.append(self)
        
        # Search in all children
        for child in self._children:
            results.extend(child.search(name))
        
        return results
    
    def count_files(self) -> int:
        """Count total number of files recursively"""
        count = 0
        for child in self._children:
            if isinstance(child, File):
                count += 1
            elif isinstance(child, Folder):
                count += child.count_files()
        return count

# ============ USAGE ============

print("="*70)
print("COMPOSITE PATTERN - FILE SYSTEM")
print("="*70)

# Create files
readme = File("README.md", 1024, "# My Project\nDescription here...")
license_file = File("LICENSE", 512, "MIT License...")
gitignore = File(".gitignore", 128, "*.pyc\n__pycache__/")

# Create source files
main_py = File("main.py", 2048, "def main():\n    pass")
utils_py = File("utils.py", 1536, "def helper():\n    pass")
config_py = File("config.py", 768, "DEBUG = True")

# Create test files
test_main = File("test_main.py", 1024, "import pytest\n...")
test_utils = File("test_utils.py", 896, "import pytest\n...")

# Create folders
root = Folder("my_project")
src = Folder("src")
tests = Folder("tests")
docs = Folder("docs")

# Build file system structure
root.add(readme)
root.add(license_file)
root.add(gitignore)

src.add(main_py)
src.add(utils_py)
src.add(config_py)
root.add(src)

tests.add(test_main)
tests.add(test_utils)
root.add(tests)

# Add documentation
user_guide = File("user_guide.md", 4096, "# User Guide\n...")
api_docs = File("api.md", 3072, "# API Documentation\n...")
docs.add(user_guide)
docs.add(api_docs)
root.add(docs)

# Display entire structure
print("\n### File System Structure ###")
root.display()

# Get total size
print(f"\n### Total Size ###")
print(f"Total size of {root.name}: {root.get_size()} bytes")

# Count files
print(f"\n### File Count ###")
print(f"Total files in {root.name}: {root.count_files()}")

# Search
print(f"\n### Search for 'test' ###")
results = root.search("test")
print(f"Found {len(results)} items:")
for result in results:
    print(f"  - {result.name}")

# Search for .py files
print(f"\n### Search for '.py' files ###")
results = root.search(".py")
print(f"Found {len(results)} items:")
for result in results:
    print(f"  - {result.name}")

# Display subfolder
print(f"\n### Display 'src' folder ###")
src.display()

# Remove a file
print(f"\n### Remove config.py ###")
src.remove(config_py)
src.display()

# Display updated structure
print(f"\n### Updated Structure ###")
root.display()

print("\n" + "="*70)
print("KEY POINT: Treated files and folders uniformly!")
print("Same operations (display, get_size, search) work for both!")
print("="*70)
```

---

### Example 2: Organization Hierarchy

```python
from abc import ABC, abstractmethod
from typing import List

# ============ COMPONENT ============

class Employee(ABC):
    """Base component for organization structure"""
    
    def __init__(self, name: str, position: str, salary: float):
        self.name = name
        self.position = position
        self.salary = salary
    
    @abstractmethod
    def get_salary(self) -> float:
        """Get total salary (including subordinates for managers)"""
        pass
    
    @abstractmethod
    def display(self, indent: int = 0):
        """Display employee info"""
        pass
    
    @abstractmethod
    def get_employee_count(self) -> int:
        """Get total number of employees"""
        pass

# ============ LEAF (Individual Contributor) ============

class Developer(Employee):
    """Leaf: Individual contributor"""
    
    def __init__(self, name: str, salary: float, programming_language: str):
        super().__init__(name, "Developer", salary)
        self.programming_language = programming_language
    
    def get_salary(self) -> float:
        """Return own salary"""
        return self.salary
    
    def display(self, indent: int = 0):
        """Display developer info"""
        prefix = "  " * indent
        print(f"{prefix}👨‍💻 {self.name} - {self.position}")
        print(f"{prefix}   Salary: ${self.salary:,.2f}")
        print(f"{prefix}   Language: {self.programming_language}")
    
    def get_employee_count(self) -> int:
        """Count self"""
        return 1

class Designer(Employee):
    """Leaf: Designer"""
    
    def __init__(self, name: str, salary: float, specialty: str):
        super().__init__(name, "Designer", salary)
        self.specialty = specialty
    
    def get_salary(self) -> float:
        return self.salary
    
    def display(self, indent: int = 0):
        prefix = "  " * indent
        print(f"{prefix}🎨 {self.name} - {self.position}")
        print(f"{prefix}   Salary: ${self.salary:,.2f}")
        print(f"{prefix}   Specialty: {self.specialty}")
    
    def get_employee_count(self) -> int:
        return 1

# ============ COMPOSITE (Manager) ============

class Manager(Employee):
    """
    Composite: Manager who can have subordinates.
    """
    
    def __init__(self, name: str, position: str, salary: float):
        super().__init__(name, position, salary)
        self._subordinates: List[Employee] = []
    
    def add_subordinate(self, employee: Employee):
        """Add a subordinate"""
        self._subordinates.append(employee)
        print(f"✅ {employee.name} now reports to {self.name}")
    
    def remove_subordinate(self, employee: Employee):
        """Remove a subordinate"""
        self._subordinates.remove(employee)
        print(f"❌ {employee.name} no longer reports to {self.name}")
    
    def get_subordinates(self) -> List[Employee]:
        """Get all direct reports"""
        return self._subordinates.copy()
    
    def get_salary(self) -> float:
        """
        Get total salary cost (own salary + all subordinates).
        Recursive operation.
        """
        total = self.salary
        for subordinate in self._subordinates:
            total += subordinate.get_salary()
        return total
    
    def display(self, indent: int = 0):
        """
        Display manager and all subordinates recursively.
        """
        prefix = "  " * indent
        print(f"{prefix}👔 {self.name} - {self.position}")
        print(f"{prefix}   Salary: ${self.salary:,.2f}")
        print(f"{prefix}   Direct Reports: {len(self._subordinates)}")
        
        if self._subordinates:
            print(f"{prefix}   Team:")
            for subordinate in self._subordinates:
                subordinate.display(indent + 2)
    
    def get_employee_count(self) -> int:
        """
        Count self + all subordinates recursively.
        """
        count = 1  # Self
        for subordinate in self._subordinates:
            count += subordinate.get_employee_count()
        return count

# ============ USAGE ============

print("="*70)
print("COMPOSITE PATTERN - ORGANIZATION HIERARCHY")
print("="*70)

# Create employees
# Developers
dev1 = Developer("Alice", 90000, "Python")
dev2 = Developer("Bob", 85000, "JavaScript")
dev3 = Developer("Charlie", 92000, "Java")
dev4 = Developer("Diana", 88000, "Python")

# Designers
designer1 = Designer("Eve", 80000, "UI/UX")
designer2 = Designer("Frank", 82000, "Graphic Design")

# Engineering Managers
eng_manager1 = Manager("Grace", "Engineering Manager", 120000)
eng_manager2 = Manager("Henry", "Engineering Manager", 118000)

# Department Head
cto = Manager("Iris", "CTO", 180000)

# CEO
ceo = Manager("Jack", "CEO", 250000)

# Build organization structure
# Team 1 under Grace
eng_manager1.add_subordinate(dev1)
eng_manager1.add_subordinate(dev2)
eng_manager1.add_subordinate(designer1)

# Team 2 under Henry
eng_manager2.add_subordinate(dev3)
eng_manager2.add_subordinate(dev4)
eng_manager2.add_subordinate(designer2)

# Engineering managers report to CTO
cto.add_subordinate(eng_manager1)
cto.add_subordinate(eng_manager2)

# CTO reports to CEO
ceo.add_subordinate(cto)

# Display organization
print("\n### Organization Structure ###\n")
ceo.display()

# Calculate costs
print("\n### Salary Analysis ###")
print(f"CEO's team total salary: ${ceo.get_salary():,.2f}")
print(f"CTO's team total salary: ${cto.get_salary():,.2f}")
print(f"Grace's team total salary: ${eng_manager1.get_salary():,.2f}")
print(f"Henry's team total salary: ${eng_manager2.get_salary():,.2f}")

# Count employees
print("\n### Employee Count ###")
print(f"Total employees in company: {ceo.get_employee_count()}")
print(f"Total in engineering: {cto.get_employee_count()}")
print(f"Total in Grace's team: {eng_manager1.get_employee_count()}")
print(f"Total in Henry's team: {eng_manager2.get_employee_count()}")

# Display specific team
print("\n### Grace's Team Details ###\n")
eng_manager1.display()

# Reorganization
print("\n### Reorganization ###")
print("Moving Diana from Henry's team to Grace's team")
eng_manager2.remove_subordinate(dev4)
eng_manager1.add_subordinate(dev4)

print("\n### Updated Structure ###\n")
ceo.display()

print("\n" + "="*70)
print("KEY POINT: Same operations work at any level!")
print("Can get salary/count for individual, team, or entire company!")
print("="*70)
```

---

### Example 3: GUI Component System

```python
from abc import ABC, abstractmethod
from typing import List, Tuple

# ============ COMPONENT ============

class UIComponent(ABC):
    """Base component for UI elements"""
    
    def __init__(self, name: str):
        self.name = name
        self.visible = True
        self.enabled = True
    
    @abstractmethod
    def render(self, x: int = 0, y: int = 0):
        """Render the component"""
        pass
    
    @abstractmethod
    def get_bounds(self) -> Tuple[int, int]:
        """Get width and height"""
        pass
    
    def show(self):
        """Show component"""
        self.visible = True
    
    def hide(self):
        """Hide component"""
        self.visible = False
    
    def enable(self):
        """Enable component"""
        self.enabled = True
    
    def disable(self):
        """Disable component"""
        self.enabled = False

# ============ LEAF COMPONENTS ============

class Button(UIComponent):
    """Leaf: Button component"""
    
    def __init__(self, name: str, text: str, width: int = 100, height: int = 30):
        super().__init__(name)
        self.text = text
        self.width = width
        self.height = height
    
    def render(self, x: int = 0, y: int = 0):
        """Render button"""
        if not self.visible:
            return
        
        status = "enabled" if self.enabled else "disabled"
        print(f"{'  ' * (x//2)}🔘 Button '{self.text}' at ({x}, {y}) - {self.width}x{self.height}px ({status})")
    
    def get_bounds(self) -> Tuple[int, int]:
        return (self.width, self.height)
    
    def click(self):
        """Handle click event"""
        if self.enabled:
            print(f"Button '{self.text}' clicked!")
        else:
            print(f"Button '{self.text}' is disabled")

class TextBox(UIComponent):
    """Leaf: Text input component"""
    
    def __init__(self, name: str, placeholder: str = "", width: int = 200, height: int = 25):
        super().__init__(name)
        self.placeholder = placeholder
        self.text = ""
        self.width = width
        self.height = height
    
    def render(self, x: int = 0, y: int = 0):
        if not self.visible:
            return
        
        display_text = self.text or f"[{self.placeholder}]"
        status = "enabled" if self.enabled else "disabled"
        print(f"{'  ' * (x//2)}📝 TextBox '{display_text}' at ({x}, {y}) - {self.width}x{self.height}px ({status})")
    
    def get_bounds(self) -> Tuple[int, int]:
        return (self.width, self.height)
    
    def set_text(self, text: str):
        self.text = text

class Label(UIComponent):
    """Leaf: Label component"""
    
    def __init__(self, name: str, text: str):
        super().__init__(name)
        self.text = text
        self.width = len(text) * 8  # Approximate
        self.height = 20
    
    def render(self, x: int = 0, y: int = 0):
        if not self.visible:
            return
        print(f"{'  ' * (x//2)}🏷️  Label '{self.text}' at ({x}, {y})")
    
    def get_bounds(self) -> Tuple[int, int]:
        return (self.width, self.height)

# ============ COMPOSITE COMPONENTS ============

class Panel(UIComponent):
    """
    Composite: Panel that can contain other components.
    """
    
    def __init__(self, name: str, width: int = 400, height: int = 300):
        super().__init__(name)
        self.width = width
        self.height = height
        self._children: List[UIComponent] = []
    
    def add(self, component: UIComponent):
        """Add a child component"""
        self._children.append(component)
    
    def remove(self, component: UIComponent):
        """Remove a child component"""
        self._children.remove(component)
    
    def get_children(self) -> List[UIComponent]:
        """Get all children"""
        return self._children.copy()
    
    def render(self, x: int = 0, y: int = 0):
        """Render panel and all children"""
        if not self.visible:
            return
        
        print(f"{'  ' * (x//2)}📦 Panel '{self.name}' at ({x}, {y}) - {self.width}x{self.height}px")
        
        # Render all children with offset
        child_y = y + 10
        for child in self._children:
            child.render(x + 1, child_y)
            _, child_height = child.get_bounds()
            child_y += child_height + 5  # Add spacing
    
    def get_bounds(self) -> Tuple[int, int]:
        return (self.width, self.height)

class Window(UIComponent):
    """
    Composite: Window that contains panels and other components.
    """
    
    def __init__(self, name: str, title: str, width: int = 800, height: int = 600):
        super().__init__(name)
        self.title = title
        self.width = width
        self.height = height
        self._children: List[UIComponent] = []
    
    def add(self, component: UIComponent):
        self._children.append(component)
    
    def remove(self, component: UIComponent):
        self._children.remove(component)
    
    def render(self, x: int = 0, y: int = 0):
        if not self.visible:
            return
        
        print("=" * 60)
        print(f"🪟  Window: {self.title}")
        print(f"   Size: {self.width}x{self.height}px")
        print("=" * 60)
        
        # Render all children
        child_y = 30  # Title bar height
        for child in self._children:
            child.render(0, child_y)
            _, child_height = child.get_bounds()
            child_y += child_height + 10
        
        print("=" * 60)
    
    def get_bounds(self) -> Tuple[int, int]:
        return (self.width, self.height)

# ============ USAGE ============

print("="*70)
print("COMPOSITE PATTERN - GUI COMPONENT SYSTEM")
print("="*70)

# Create login form
login_window = Window("login_window", "Login", 400, 300)

# Username panel
username_panel = Panel("username_panel", 380, 60)
username_label = Label("username_label", "Username:")
username_input = TextBox("username_input", "Enter username", 250, 25)
username_panel.add(username_label)
username_panel.add(username_input)

# Password panel
password_panel = Panel("password_panel", 380, 60)
password_label = Label("password_label", "Password:")
password_input = TextBox("password_input", "Enter password", 250, 25)
password_panel.add(password_label)
password_panel.add(password_input)

# Buttons panel
buttons_panel = Panel("buttons_panel", 380, 40)
login_button = Button("login_btn", "Login", 100, 30)
cancel_button = Button("cancel_btn", "Cancel", 100, 30)
buttons_panel.add(login_button)
buttons_panel.add(cancel_button)

# Add panels to window
login_window.add(username_panel)
login_window.add(password_panel)
login_window.add(buttons_panel)

# Render entire window
print("\n### Login Form ###")
login_window.render()

# Simulate user interaction
print("\n### User Interaction ###")
username_input.set_text("john_doe")
password_input.set_text("********")
login_button.click()

# Re-render to show changes
print("\n### Updated Form ###")
login_window.render()

# Disable login button
print("\n### Disable Login Button ###")
login_button.disable()
login_window.render()
login_button.click()  # Try to click disabled button

# Hide password panel
print("\n### Hide Password Panel ###")
password_panel.hide()
login_window.render()

# Create dashboard window
print("\n### Dashboard Window ###")
dashboard = Window("dashboard", "Dashboard", 800, 600)

# Sidebar panel
sidebar = Panel("sidebar", 200, 500)
sidebar.add(Label("nav_label", "Navigation"))
sidebar.add(Button("home_btn", "Home", 180))
sidebar.add(Button("profile_btn", "Profile", 180))
sidebar.add(Button("settings_btn", "Settings", 180))

# Main content panel
content = Panel("content", 580, 500)
content.add(Label("welcome_label", "Welcome to Dashboard!"))
content.add(TextBox("search_box", "Search...", 400))

# Status bar
status_bar = Panel("status_bar", 780, 30)
status_bar.add(Label("status_label", "Ready"))

dashboard.add(sidebar)
dashboard.add(content)
dashboard.add(status_bar)

dashboard.render()

print("\n" + "="*70)
print("KEY POINT: Same operations for all components!")
print("Window, Panel, Button, TextBox all have render(), show(), hide()")
print("Can nest components arbitrarily deep!")
print("="*70)
```

---

## Common Pitfalls

### ❌ Pitfall 1: Making Leaf Operations in Composite Optional

```python
# BAD - Client must check type
class Component:
    def add(self, component):
        pass  # Does nothing for Leaf
    
    def operation(self):
        pass

# Client code becomes ugly
component = Component()
child = Component()

if hasattr(component, '_children'):
    component.add(child)  # Must check if composite

# GOOD - Clear contract
class Component:
    def add(self, component):
        raise NotImplementedError("Cannot add to leaf")

# Or use separate interfaces for clarity
```

---

### ❌ Pitfall 2: Not Handling Recursion Depth

```python
# BAD - No protection against deep recursion
class Composite:
    def operation(self):
        for child in self._children:
            child.operation()  # Could stack overflow on very deep trees

# GOOD - Limit depth or use iterative approach
class Composite:
    def operation(self, depth=0, max_depth=100):
        if depth > max_depth:
            raise RecursionError("Tree too deep")
        
        for child in self._children:
            if hasattr(child, '_children'):
                child.operation(depth + 1, max_depth)
            else:
                child.operation()
```

---

### ❌ Pitfall 3: Parent References Cause Circular Dependencies

```python
# BAD - Circular references
class Component:
    def __init__(self):
        self.parent = None  # Can cause memory leaks

# GOOD - Weak references or no parent reference
import weakref

class Component:
    def __init__(self):
        self._parent = None
    
    @property
    def parent(self):
        return self._parent() if self._parent else None
    
    @parent.setter
    def parent(self, value):
        self._parent = weakref.ref(value) if value else None
```

---

### ❌ Pitfall 4: Composite Operations Are Too Different

```python
# BAD - Leaf and Composite have very different operations
class File:
    def read(self): pass

class Folder:
    def add(self): pass
    def list(self): pass
    # No read() method!

# Can't treat uniformly - defeats purpose of Composite pattern

# GOOD - Common interface
class FileSystemItem:
    def get_size(self): pass
    def display(self): pass
    # Both can implement these
```

---

## Best Practices

### ✅ 1. Keep Component Interface Minimal

```python
from abc import ABC, abstractmethod
# GOOD - Minimal, focused interface
class Component(ABC):
    @abstractmethod
    def operation(self):
        pass

# Additional methods only where needed
```

---

### ✅ 2. Use Type Hints

```python
from abc import ABC, abstractmethod

class Component(ABC):
    @abstractmethod
    def operation(self):
        pass
    
class Composite(Component):
    def __init__(self):
        self._children: list[Component] = []
    
    def add(self, component: Component) -> None:
        self._children.append(component)
```

---

### ✅ 3. Provide Safe Child Access

```python
from abc import ABC, abstractmethod

class Component(ABC):
    @abstractmethod
    def operation(self):
        pass
    
class Composite:
    def get_children(self) -> list[Component]:
        """Return copy to prevent external modification"""
        return self._children.copy()
```

---

### ✅ 4. Consider Caching for Expensive Operations

```python
class Composite:
    def __init__(self):
        self._children = []
        self._size_cache = None
    
    def get_size(self) -> int:
        if self._size_cache is None:
            self._size_cache = sum(c.get_size() for c in self._children)
        return self._size_cache
    
    def add(self, component):
        self._children.append(component)
        self._size_cache = None  # Invalidate cache
```

---

### ✅ 5. Document Tree Structure

```python
class FileSystem:
    """
    File system structure:
    
    Root (Folder)
    ├── Documents (Folder)
    │   ├── Resume.pdf (File)
    │   └── Cover_Letter.docx (File)
    ├── Pictures (Folder)
    │   └── Vacation.jpg (File)
    └── README.txt (File)
    """
    pass
```

---

## Summary

| Aspect          | Details                                                   |
|-----------------|-----------------------------------------------------------|
| **Purpose**     | Compose objects into tree structures                      |
| **Use When**    | Part-whole hierarchies, treat uniformly                   |
| **Avoid When**  | No hierarchy, operations differ significantly             |
| **Key Benefit** | Client treats individual and composite objects uniformly  |
| **Structure**   | Tree with Leaf (no children) and Composite (has children) |

---

## Composite Pattern Checklist

✅ **Use Composite when:**
- You have a tree structure (parent-child relationships)
- You want to treat individual objects and compositions uniformly
- Operations work recursively through the tree
- Structure can change at runtime

❌ **Don't use Composite when:**
- Flat structure (no hierarchy)
- Operations are very different for leaf vs. composite
- Performance of recursive operations is critical
- Simple parent-child list suffices

---

## Key Takeaways

1. **Part-Whole Hierarchy:** Represents tree structures naturally
2. **Uniform Treatment:** Same operations work for both leaf and composite
3. **Recursive Operations:** Operations propagate through tree automatically
4. **Flexible Composition:** Easy to add new component types
5. **Transparent to Client:** Client doesn't distinguish between leaf and composite
