# Flyweight Pattern - Complete Guide

## 📋 Table of Contents
- [What is Flyweight Pattern?](#what-is-flyweight-pattern)
  - [Key Characteristics](#key-characteristics)
  - [The Problem Flyweight Solves](#the-problem-flyweight-solves)
  - [Real-World Analogy](#real-world-analogy)
  - [Visual Representation](#visual-representation)
  - [Intrinsic vs Extrinsic State](#intrinsic-vs-extrinsic-state)
- [When to Use](#when-to-use)
  - [✅ Perfect Use Cases](#-perfect-use-cases)
- [When NOT to Use](#when-not-to-use)
  - [❌ Avoid Flyweight When](#when-not-to-use)
- [Basic Implementation](#basic-implementation)
  - [Classic Flyweight Structure](#classic-flyweight-structure)
- [Real-World Examples](#real-world-examples)
  - [Example 1: Game Forest (Trees)](#example-1-game-forest-trees)
  - [Example 2: Text Editor (Characters)](#example-2-text-editor-characters)
  - [Example 3: Particle System (Game)](#example-3-particle-system-game)
- [Common Pitfalls](#common-pitfalls)
  - [❌ Pitfall 1: Making Flyweight Mutable](#-pitfall-1-making-flyweight-mutable)
  - [❌ Pitfall 2: Storing Extrinsic State in Flyweight](#-pitfall-2-storing-extrinsic-state-in-flyweight)
  - [❌ Pitfall 3: Not Using Factory](#-pitfall-3-not-using-factory)
  - [❌ Pitfall 4: Using Flyweight for Few Objects](#-pitfall-4-using-flyweight-for-few-objects)
- [Best Practices](#best-practices)
  - [✅ 1. Clearly Identify Intrinsic vs Extrinsic State](#-1-clearly-identify-intrinsic-vs-extrinsic-state)
  - [✅ 2. Make Flyweights Immutable](#-2-make-flyweights-immutable)
  - [✅ 3. Use Factory for All Flyweight Creation](#-3-use-factory-for-all-flyweight-creation)
  - [✅ 4. Consider Thread Safety](#-4-consider-thread-safety)
  - [✅ 5. Measure Memory Savings](#-5-measure-memory-savings)
- [Summary](#summary)
- [Flyweight Pattern Checklist](#flyweight-pattern-checklist)
- [Key Takeaways](#key-takeaways)
- [Memory Savings Example](#memory-savings-example)
---

## What is Flyweight Pattern?

**Flyweight Pattern** is a structural design pattern that lets you fit more objects into available RAM by sharing common parts of state between multiple objects instead of keeping all of the data in each object.

### Key Characteristics:
- ✅ Shares common data to save memory
- ✅ Separates intrinsic state (shared) from extrinsic state (unique)
- ✅ Uses factory to manage shared objects
- ✅ Reduces memory footprint dramatically
- ✅ Ideal for large numbers of similar objects

### The Problem Flyweight Solves

**Without Flyweight:**
```python
# Creating 1 million tree objects
import random

class Tree:
   def __init__(self, name, color, texture, x, y):
       self.name = name
       self.color = color
       self.texture = texture
       self.x = x
       self.y = y

trees = []
for i in range(1_000_000):
    tree = Tree(
        name="Oak",           # Repeated 1M times!
        color="Green",        # Repeated 1M times!
        texture="bark.png",   # Repeated 1M times!
        x=random.randint(0, 1000),
        y=random.randint(0, 1000)
    )
    trees.append(tree)

# Memory: ~1 million × (name + color + texture + x + y) = HUGE!
```

**With Flyweight:**
```python
# Share common data (intrinsic state)
import random

class TreeType:
   def __init__(self, name, color, texture):
       self.name = name
       self.color = color
       self.texture = texture
    
   def draw(self, x, y):
      pass

class Tree:
    def __init__(self, x, y, tree_type):
        self.x = x
        self.y = y
        self.tree_type = tree_type  # Reference to the shared Flyweight object

    def draw(self):
        # Delegate rendering to the shared type object, passing unique coordinates
        self.tree_type.draw(self.x, self.y)

oak_type = TreeType("Oak", "Green", "bark.png")  # Created ONCE

# Store only unique data (extrinsic state)
trees = []
for i in range(1_000_000):
    tree = Tree(
        tree_type=oak_type,  # Reference to shared object
        x=random.randint(0, 1000),
        y=random.randint(0, 1000)
    )
    trees.append(tree)

# Memory: 1 TreeType + 1M × (reference + x + y) = Much smaller!
```

### Real-World Analogy:
Think of a **library**:
- **Without Flyweight:** Every person who wants to read "Harry Potter" gets their own physical copy → Need 1000 copies for 1000 readers
- **With Flyweight:** One shared copy of "Harry Potter" (intrinsic state), readers just keep track of which page they're on (extrinsic state) → Need only 1 copy

### Visual Representation:
```
Without Flyweight:
Object1: [Shared Data A] [Unique Data 1]
Object2: [Shared Data A] [Unique Data 2]  ← Duplicate shared data!
Object3: [Shared Data A] [Unique Data 3]  ← Duplicate shared data!

With Flyweight:
Object1: [→ Flyweight A] [Unique Data 1]
Object2: [→ Flyweight A] [Unique Data 2]  ← Points to same Flyweight!
Object3: [→ Flyweight A] [Unique Data 3]  ← Points to same Flyweight!

Flyweight A: [Shared Data A]  ← Stored only once!
```

---

### Intrinsic vs Extrinsic State

**Critical Concept:**

| State Type    | Description                            | Example                      | Stored Where                   |
|---------------|----------------------------------------|------------------------------|--------------------------------|
| **Intrinsic** | Shared, immutable, context-independent | Tree species, color, texture | Inside Flyweight (shared)      |
| **Extrinsic** | Unique, context-dependent              | Tree position (x, y), size   | Outside Flyweight (per object) |

**Key Rule:** Flyweight stores **only intrinsic state**. Extrinsic state is passed as parameters or stored separately.

---

## When to Use

### ✅ Perfect Use Cases:

#### 1. **Large Number of Similar Objects**
- Game with thousands of trees, particles, bullets
- Text editor with millions of character objects
- Map with thousands of similar buildings

#### 2. **Objects Share Common Data**
- Most of the data is the same across instances
- Small portion is unique per instance
- Memory consumption is a concern

#### 3. **Object Identity Doesn't Matter**
- Don't need to distinguish individual objects
- Can share objects transparently
- Objects are mostly immutable

#### 4. **Memory is Limited**
- Mobile apps
- Embedded systems
- Games with memory constraints

#### 5. **Creating Objects is Expensive**
- Loading textures, sprites
- Database connections
- Complex initialization

---

## When NOT to Use

### ❌ Avoid Flyweight When:

1. **Few Objects**
   - Only dozens or hundreds of objects
   - Memory saved is negligible
   - Adds unnecessary complexity

2. **Objects Are All Unique**
   - Little to no shared state
   - Most data is extrinsic
   - No memory benefit

3. **Object Identity Matters**
   - Need to track individual objects
   - Objects are mutable
   - Can't share instances

4. **Simple Problem**
   - Memory isn't a concern
   - Premature optimization
   - YAGNI (You Aren't Gonna Need It)

---

## Basic Implementation

### Classic Flyweight Structure

```python
# ============ FLYWEIGHT ============

class Flyweight:
    """
    Flyweight stores intrinsic state (shared among many objects).
    Must be immutable!
    """
    
    def __init__(self, shared_state: str):
        self._shared_state = shared_state
    
    def operation(self, unique_state: str):
        """
        Operation that uses both intrinsic (shared) and extrinsic (unique) state.
        Extrinsic state is passed as parameter.
        """
        print(f"Flyweight: Displaying shared ({self._shared_state}) "
              f"and unique ({unique_state}) state.")

# ============ FLYWEIGHT FACTORY ============

class FlyweightFactory:
    """
    Factory creates and manages flyweight objects.
    Ensures flyweights are shared properly.
    """
    
    def __init__(self):
        self._flyweights: dict[str, Flyweight] = {}
    
    def get_flyweight(self, shared_state: str) -> Flyweight:
        """
        Returns existing flyweight or creates new one if doesn't exist.
        """
        if shared_state not in self._flyweights:
            print(f"FlyweightFactory: Creating new flyweight for '{shared_state}'")
            self._flyweights[shared_state] = Flyweight(shared_state)
        else:
            print(f"FlyweightFactory: Reusing existing flyweight for '{shared_state}'")
        
        return self._flyweights[shared_state]
    
    def list_flyweights(self):
        """Show all cached flyweights"""
        count = len(self._flyweights)
        print(f"\nFlyweightFactory: I have {count} flyweights:")
        for key in self._flyweights.keys():
            print(f"  - {key}")

# ============ CONTEXT ============

class Context:
    """
    Context stores extrinsic state (unique to each object).
    Contains reference to flyweight (intrinsic state).
    """
    
    def __init__(self, shared_state: str, unique_state: str, factory: FlyweightFactory):
        # Get shared flyweight from factory
        self._flyweight = factory.get_flyweight(shared_state)
        # Store unique state
        self._unique_state = unique_state
    
    def operation(self):
        """Operation delegates to flyweight, passing unique state"""
        self._flyweight.operation(self._unique_state)

# ============ CLIENT CODE ============

print("="*70)
print("BASIC FLYWEIGHT PATTERN")
print("="*70)

factory = FlyweightFactory()

# Create objects with shared state
print("\n### Creating Objects ###")
context1 = Context("SharedType-A", "Unique-1", factory)
context2 = Context("SharedType-A", "Unique-2", factory)  # Reuses flyweight!
context3 = Context("SharedType-B", "Unique-3", factory)
context4 = Context("SharedType-A", "Unique-4", factory)  # Reuses again!
context5 = Context("SharedType-B", "Unique-5", factory)  # Reuses B!

# Show cached flyweights
factory.list_flyweights()

# Use objects
print("\n### Using Objects ###")
context1.operation()
context2.operation()
context3.operation()
context4.operation()
context5.operation()

print("\n" + "="*70)
print(f"Memory saved: Created 5 contexts but only 2 flyweights!")
print("="*70)
```

**Output:**
```
======================================================================
BASIC FLYWEIGHT PATTERN
======================================================================

### Creating Objects ###
FlyweightFactory: Creating new flyweight for 'SharedType-A'
FlyweightFactory: Reusing existing flyweight for 'SharedType-A'
FlyweightFactory: Creating new flyweight for 'SharedType-B'
FlyweightFactory: Reusing existing flyweight for 'SharedType-A'
FlyweightFactory: Reusing existing flyweight for 'SharedType-B'

FlyweightFactory: I have 2 flyweights:
  - SharedType-A
  - SharedType-B

### Using Objects ###
Flyweight: Displaying shared (SharedType-A) and unique (Unique-1) state.
Flyweight: Displaying shared (SharedType-A) and unique (Unique-2) state.
Flyweight: Displaying shared (SharedType-B) and unique (Unique-3) state.
Flyweight: Displaying shared (SharedType-A) and unique (Unique-4) state.
Flyweight: Displaying shared (SharedType-B) and unique (Unique-5) state.

======================================================================
Memory saved: Created 5 contexts but only 2 flyweights!
======================================================================
```

---

## Real-World Examples

### Example 1: Game Forest (Trees)

```python
import random

# ============ FLYWEIGHT (Intrinsic State) ============

class TreeType:
    """
    Flyweight: Stores intrinsic state shared by many trees.
    Immutable - represents tree species.
    """
    
    def __init__(self, name: str, color: str, texture: str):
        self.name = name
        self.color = color
        self.texture = texture  # Imagine this is a large texture file
    
    def draw(self, x: int, y: int):
        """
        Draw tree at specific position.
        Position (x, y) is extrinsic state - passed as parameter.
        """
        print(f"🌳 Drawing {self.color} {self.name} tree at ({x}, {y}) "
              f"with texture '{self.texture}'")

# ============ FLYWEIGHT FACTORY ============

class TreeFactory:
    """
    Factory manages tree type flyweights.
    Ensures tree types are shared.
    """
    
    def __init__(self):
        self._tree_types: dict[str, TreeType] = {}
    
    def get_tree_type(self, name: str, color: str, texture: str) -> TreeType:
        """Get existing tree type or create new one"""
        # Create unique key from shared attributes
        key = f"{name}_{color}_{texture}"
        
        if key not in self._tree_types:
            print(f"TreeFactory: Creating new tree type '{name}'")
            self._tree_types[key] = TreeType(name, color, texture)
        else:
            print(f"TreeFactory: Reusing tree type '{name}'")
        
        return self._tree_types[key]
    
    def get_tree_type_count(self) -> int:
        """Get number of unique tree types"""
        return len(self._tree_types)

# ============ CONTEXT (Extrinsic State) ============

class Tree:
    """
    Context: Stores extrinsic state (unique per tree).
    Contains reference to shared TreeType flyweight.
    """
    
    def __init__(self, x: int, y: int, tree_type: TreeType):
        self.x = x  # Extrinsic state
        self.y = y  # Extrinsic state
        self._type = tree_type  # Reference to flyweight (intrinsic state)
    
    def draw(self):
        """Draw this specific tree"""
        self._type.draw(self.x, self.y)

# ============ FOREST (Client) ============

class Forest:
    """
    Forest manages many trees efficiently using flyweight pattern.
    """
    
    def __init__(self):
        self._trees: list[Tree] = []
        self._factory = TreeFactory()
    
    def plant_tree(self, x: int, y: int, name: str, color: str, texture: str):
        """Plant a tree at specific position"""
        # Get shared tree type from factory
        tree_type = self._factory.get_tree_type(name, color, texture)
        
        # Create tree with unique position
        tree = Tree(x, y, tree_type)
        self._trees.append(tree)
    
    def draw(self):
        """Draw all trees"""
        print(f"\n🌲 Drawing forest with {len(self._trees)} trees:")
        for tree in self._trees:
            tree.draw()
    
    def get_memory_usage(self) -> str:
        """Estimate memory savings"""
        tree_count = len(self._trees)
        tree_type_count = self._factory.get_tree_type_count()
        
        # Rough estimate
        without_flyweight = tree_count * 100  # Each tree stores all data
        with_flyweight = (tree_type_count * 100) + (tree_count * 20)  # Shared types + positions
        
        saved = without_flyweight - with_flyweight
        percentage = (saved / without_flyweight) * 100
        
        return (f"Without Flyweight: ~{without_flyweight} KB\n"
                f"With Flyweight: ~{with_flyweight} KB\n"
                f"Saved: ~{saved} KB ({percentage:.1f}%)")

# ============ USAGE ============

print("="*70)
print("FLYWEIGHT PATTERN - GAME FOREST")
print("="*70)

forest = Forest()

# Plant many trees
print("\n### Planting Trees ###")

# Plant 10 oak trees
for i in range(10):
    x = random.randint(0, 100)
    y = random.randint(0, 100)
    forest.plant_tree(x, y, "Oak", "Green", "oak_texture.png")

print()

# Plant 10 pine trees
for i in range(10):
    x = random.randint(0, 100)
    y = random.randint(0, 100)
    forest.plant_tree(x, y, "Pine", "Dark Green", "pine_texture.png")

print()

# Plant 5 birch trees
for i in range(5):
    x = random.randint(0, 100)
    y = random.randint(0, 100)
    forest.plant_tree(x, y, "Birch", "White", "birch_texture.png")

print()

# Plant more oaks (reusing existing type)
for i in range(5):
    x = random.randint(0, 100)
    y = random.randint(0, 100)
    forest.plant_tree(x, y, "Oak", "Green", "oak_texture.png")

# Draw forest (showing only first 5)
print("\n### Drawing Forest (first 5 trees shown) ###")
for i, tree in enumerate(forest._trees[:5]):
    tree.draw()

print(f"\n... and {len(forest._trees) - 5} more trees")

# Show memory savings
print("\n### Memory Usage ###")
print(forest.get_memory_usage())

print("\n### Statistics ###")
print(f"Total trees planted: {len(forest._trees)}")
print(f"Unique tree types: {forest._factory.get_tree_type_count()}")
print(f"Memory efficiency: {len(forest._trees) // forest._factory.get_tree_type_count()}:1 ratio")

print("\n" + "="*70)
print("KEY POINT: 30 trees but only 3 tree type objects!")
print("Shared textures/colors saved massive memory!")
print("="*70)
```

---

### Example 2: Text Editor (Characters)

```python
# ============ FLYWEIGHT (Character Appearance) ============

class CharacterStyle:
    """
    Flyweight: Stores intrinsic state (font, size, color).
    Shared among many characters with same style.
    """
    
    def __init__(self, font: str, size: int, color: str, bold: bool = False, italic: bool = False):
        self.font = font
        self.size = size
        self.color = color
        self.bold = bold
        self.italic = italic
    
    def __str__(self):
        style = f"{self.font}-{self.size}pt-{self.color}"
        if self.bold:
            style += "-bold"
        if self.italic:
            style += "-italic"
        return style
    
    def render(self, character: str, x: int, y: int):
        """
        Render character with this style at position.
        Character and position are extrinsic state.
        """
        style_str = "**" if self.bold else ""
        style_str += "*" if self.italic else ""
        print(f"  '{style_str}{character}{style_str}' at ({x},{y}) "
              f"[{self.font}, {self.size}pt, {self.color}]")

# ============ FLYWEIGHT FACTORY ============

class CharacterStyleFactory:
    """Factory manages character style flyweights"""
    
    def __init__(self):
        self._styles: dict[str, CharacterStyle] = {}
        self._requests = 0
        self._cache_hits = 0
    
    def get_style(self, font: str, size: int, color: str, 
                  bold: bool = False, italic: bool = False) -> CharacterStyle:
        """Get existing style or create new one"""
        self._requests += 1
        
        # Create key from attributes
        key = f"{font}_{size}_{color}_{bold}_{italic}"
        
        if key not in self._styles:
            print(f"  Creating new style: {font}-{size}pt-{color}")
            self._styles[key] = CharacterStyle(font, size, color, bold, italic)
        else:
            self._cache_hits += 1
        
        return self._styles[key]
    
    def get_stats(self):
        """Get cache statistics"""
        hit_rate = (self._cache_hits / self._requests * 100) if self._requests > 0 else 0
        return {
            'unique_styles': len(self._styles),
            'total_requests': self._requests,
            'cache_hits': self._cache_hits,
            'hit_rate': f"{hit_rate:.1f}%"
        }

# ============ CONTEXT (Character Instance) ============

class Character:
    """
    Context: Stores extrinsic state (character and position).
    References shared CharacterStyle flyweight.
    """
    
    def __init__(self, char: str, x: int, y: int, style: CharacterStyle):
        self.char = char  # Extrinsic
        self.x = x        # Extrinsic
        self.y = y        # Extrinsic
        self._style = style  # Intrinsic (shared)
    
    def render(self):
        """Render this character"""
        self._style.render(self.char, self.x, self.y)

# ============ DOCUMENT ============

class TextDocument:
    """Document contains many characters using flyweight pattern"""
    
    def __init__(self):
        self._characters: list[Character] = []
        self._style_factory = CharacterStyleFactory()
        self._cursor_x = 0
        self._cursor_y = 0
    
    def add_text(self, text: str, font: str = "Arial", size: int = 12, 
                 color: str = "black", bold: bool = False, italic: bool = False):
        """Add text with specified style"""
        
        # Get or create style (shared)
        style = self._style_factory.get_style(font, size, color, bold, italic)
        
        # Create character objects with unique positions
        for char in text:
            if char == '\n':
                self._cursor_y += size + 5
                self._cursor_x = 0
            else:
                character = Character(char, self._cursor_x, self._cursor_y, style)
                self._characters.append(character)
                self._cursor_x += size // 2  # Approximate character width
    
    def render(self, max_chars: int = 50):
        """Render document (showing first max_chars)"""
        print(f"\nRendering document ({len(self._characters)} characters):")
        for i, char in enumerate(self._characters[:max_chars]):
            char.render()
        
        if len(self._characters) > max_chars:
            print(f"  ... and {len(self._characters) - max_chars} more characters")
    
    def get_memory_estimate(self):
        """Estimate memory usage"""
        char_count = len(self._characters)
        style_count = self._style_factory.get_stats()['unique_styles']
        
        # Rough estimates (bytes)
        without_flyweight = char_count * 50  # Each char stores full style
        with_flyweight = (style_count * 50) + (char_count * 15)  # Shared styles + positions
        
        saved = without_flyweight - with_flyweight
        percentage = (saved / without_flyweight) * 100 if without_flyweight > 0 else 0
        
        return {
            'without_flyweight': without_flyweight,
            'with_flyweight': with_flyweight,
            'saved': saved,
            'percentage': percentage
        }
    
    def get_stats(self):
        """Get document statistics"""
        return {
            'total_characters': len(self._characters),
            'style_stats': self._style_factory.get_stats(),
            'memory': self.get_memory_estimate()
        }

# ============ USAGE ============

print("="*70)
print("FLYWEIGHT PATTERN - TEXT EDITOR")
print("="*70)

doc = TextDocument()

# Add document content
print("\n### Adding Text ###")

doc.add_text("Hello World!\n", "Arial", 14, "black")

doc.add_text("This is ", "Arial", 12, "black")
doc.add_text("bold", "Arial", 12, "black", bold=True)
doc.add_text(" text.\n", "Arial", 12, "black")

doc.add_text("This is ", "Arial", 12, "black")
doc.add_text("italic", "Arial", 12, "black", italic=False)
doc.add_text(" text.\n", "Arial", 12, "black")

doc.add_text("This is ", "Arial", 12, "black")
doc.add_text("red", "Arial", 12, "red")
doc.add_text(" text.\n", "Arial", 12, "black")

doc.add_text("And this is ", "Times New Roman", 12, "black")
doc.add_text("different font", "Times New Roman", 12, "black")
doc.add_text(".\n", "Arial", 12, "black")

# More content with repeated styles
doc.add_text("More text with ", "Arial", 12, "black")
doc.add_text("bold", "Arial", 12, "black", bold=True)
doc.add_text(" again.\n", "Arial", 12, "black")

doc.add_text("And even more ", "Arial", 12, "black")
doc.add_text("bold", "Arial", 12, "black", bold=True)
doc.add_text(" text.\n", "Arial", 12, "black")

# Render document
doc.render(max_chars=30)

# Show statistics
print("\n### Document Statistics ###")
stats = doc.get_stats()

print(f"Total characters: {stats['total_characters']}")
print(f"Unique styles: {stats['style_stats']['unique_styles']}")
print(f"Style cache hit rate: {stats['style_stats']['hit_rate']}")

print(f"\n### Memory Usage ###")
mem = stats['memory']
print(f"Without Flyweight: ~{mem['without_flyweight']} bytes")
print(f"With Flyweight: ~{mem['with_flyweight']} bytes")
print(f"Saved: ~{mem['saved']} bytes ({mem['percentage']:.1f}%)")

print(f"\n### Efficiency ###")
ratio = stats['total_characters'] / stats['style_stats']['unique_styles']
print(f"Each style object is shared by ~{ratio:.1f} characters on average")

print("\n" + "="*70)
print("KEY POINT: Hundreds of characters, but only a few style objects!")
print("Font/size/color data is shared, only position is unique!")
print("="*70)
```

---

### Example 3: Particle System (Game)

```python
import random

# ============ FLYWEIGHT (Particle Type) ============

class ParticleType:
    """
    Flyweight: Stores intrinsic state (sprite, color, effects).
    Shared among many particles of same type.
    """
    
    def __init__(self, name: str, sprite: str, color: str, size: int):
        self.name = name
        self.sprite = sprite  # Imagine this is texture data
        self.color = color
        self.size = size
    
    def render(self, x: float, y: float, velocity_x: float, velocity_y: float):
        """
        Render particle at specific position with velocity.
        Position and velocity are extrinsic state.
        """
        # Simplified rendering (in real game, would draw sprite)
        direction = "↗" if velocity_x > 0 and velocity_y < 0 else \
                   "↖" if velocity_x < 0 and velocity_y < 0 else \
                   "↘" if velocity_x > 0 and velocity_y > 0 else "↙"
        
        return f"{self.name[:1]}{direction}"

# ============ FLYWEIGHT FACTORY ============

class ParticleTypeFactory:
    """Factory manages particle type flyweights"""
    
    def __init__(self):
        self._types: dict[str, ParticleType] = {}
    
    def get_particle_type(self, name: str, sprite: str, color: str, size: int) -> ParticleType:
        """Get existing type or create new one"""
        if name not in self._types:
            print(f"  ParticleFactory: Creating '{name}' particle type")
            self._types[name] = ParticleType(name, sprite, color, size)
        
        return self._types[name]
    
    def get_type_count(self) -> int:
        return len(self._types)

# ============ CONTEXT (Particle Instance) ============

class Particle:
    """
    Context: Stores extrinsic state (position, velocity, lifetime).
    References shared ParticleType flyweight.
    """
    
    def __init__(self, x: float, y: float, velocity_x: float, velocity_y: float,
                 particle_type: ParticleType, lifetime: float):
        # Extrinsic state (unique to each particle)
        self.x = x
        self.y = y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.lifetime = lifetime
        self.age = 0.0
        
        # Intrinsic state (shared)
        self._type = particle_type
    
    def update(self, dt: float) -> bool:
        """
        Update particle physics.
        Returns False if particle should be removed.
        """
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
        self.age += dt
        
        # Gravity
        self.velocity_y += 9.8 * dt
        
        return self.age < self.lifetime
    
    def render(self) -> str:
        """Render particle"""
        return self._type.render(self.x, self.y, self.velocity_x, self.velocity_y)

# ============ PARTICLE SYSTEM ============

class ParticleSystem:
    """Manages thousands of particles efficiently using flyweight"""
    
    def __init__(self):
        self._particles: list[Particle] = []
        self._factory = ParticleTypeFactory()
        self._total_created = 0
    
    def emit_explosion(self, x: float, y: float, particle_count: int = 50):
        """Emit explosion particles"""
        print(f"\n💥 Emitting explosion at ({x:.1f}, {y:.1f})")
        
        # Get particle type (shared)
        explosion_type = self._factory.get_particle_type(
            "Explosion",
            "explosion_sprite.png",
            "orange",
            8
        )
        
        # Create many particles with unique positions/velocities
        for _ in range(particle_count):
            velocity_x = random.uniform(-50, 50)
            velocity_y = random.uniform(-100, -20)
            lifetime = random.uniform(0.5, 2.0)
            
            particle = Particle(x, y, velocity_x, velocity_y, explosion_type, lifetime)
            self._particles.append(particle)
            self._total_created += 1
    
    def emit_smoke(self, x: float, y: float, particle_count: int = 30):
        """Emit smoke particles"""
        print(f"\n💨 Emitting smoke at ({x:.1f}, {y:.1f})")
        
        smoke_type = self._factory.get_particle_type(
            "Smoke",
            "smoke_sprite.png",
            "gray",
            12
        )
        
        for _ in range(particle_count):
            velocity_x = random.uniform(-10, 10)
            velocity_y = random.uniform(-30, -10)
            lifetime = random.uniform(1.0, 3.0)
            
            particle = Particle(x, y, velocity_x, velocity_y, smoke_type, lifetime)
            self._particles.append(particle)
            self._total_created += 1
    
    def emit_sparks(self, x: float, y: float, particle_count: int = 100):
        """Emit spark particles"""
        print(f"\n✨ Emitting sparks at ({x:.1f}, {y:.1f})")
        
        spark_type = self._factory.get_particle_type(
            "Spark",
            "spark_sprite.png",
            "yellow",
            4
        )
        
        for _ in range(particle_count):
            angle = random.uniform(0, 360)
            speed = random.uniform(50, 150)
            velocity_x = speed * random.uniform(-1, 1)
            velocity_y = speed * random.uniform(-1, -0.5)
            lifetime = random.uniform(0.2, 1.0)
            
            particle = Particle(x, y, velocity_x, velocity_y, spark_type, lifetime)
            self._particles.append(particle)
            self._total_created += 1
    
    def update(self, dt: float):
        """Update all particles"""
        # Update and remove dead particles
        self._particles = [p for p in self._particles if p.update(dt)]
    
    def render(self, max_particles: int = 20):
        """Render particles (showing sample)"""
        if not self._particles:
            print("  (No active particles)")
            return
        
        # Show sample of particles
        sample_size = min(max_particles, len(self._particles))
        sample = random.sample(self._particles, sample_size)
        
        # Group by position for display
        grid: dict[tuple[int, int], list[str]] = {}
        for p in sample:
            grid_x = int(p.x // 10)
            grid_y = int(p.y // 10)
            key = (grid_x, grid_y)
            
            if key not in grid:
                grid[key] = []
            grid[key].append(p.render())
        
        # Display grid
        for (gx, gy), particles in sorted(grid.items()):
            particle_str = "".join(particles[:5])  # Show max 5 per grid cell
            print(f"  Position ({gx*10}, {gy*10}): {particle_str}")
        
        if len(self._particles) > sample_size:
            print(f"  ... and {len(self._particles) - sample_size} more particles")
    
    def get_stats(self):
        """Get system statistics"""
        active = len(self._particles)
        types = self._factory.get_type_count()
        
        # Memory estimate
        without_flyweight = self._total_created * 100  # Each particle stores sprite data
        with_flyweight = (types * 100) + (active * 30)  # Shared types + active particles
        
        return {
            'active_particles': active,
            'total_created': self._total_created,
            'particle_types': types,
            'memory_without_flyweight': without_flyweight,
            'memory_with_flyweight': with_flyweight,
            'memory_saved': without_flyweight - with_flyweight
        }

# ============ USAGE ============

print("="*70)
print("FLYWEIGHT PATTERN - PARTICLE SYSTEM")
print("="*70)

system = ParticleSystem()

# Create multiple effects
system.emit_explosion(100, 100, 50)
system.emit_smoke(100, 100, 30)
system.emit_sparks(120, 80, 100)

# Another explosion (reuses particle type!)
system.emit_explosion(200, 150, 50)

# More effects
system.emit_smoke(200, 150, 30)
system.emit_sparks(180, 120, 100)

# Render initial state
print("\n### Initial Particle State ###")
system.render(max_particles=15)

# Simulate updates
print("\n### After 0.1 seconds ###")
system.update(0.1)
system.render(max_particles=15)

print("\n### After 0.5 seconds ###")
for _ in range(4):
    system.update(0.1)
system.render(max_particles=15)

print("\n### After 2.0 seconds ###")
for _ in range(15):
    system.update(0.1)
system.render(max_particles=15)

# Show statistics
print("\n### Statistics ###")
stats = system.get_stats()
print(f"Active particles: {stats['active_particles']}")
print(f"Total created: {stats['total_created']}")
print(f"Particle types: {stats['particle_types']}")

print(f"\n### Memory Usage ###")
print(f"Without Flyweight: ~{stats['memory_without_flyweight']} KB")
print(f"With Flyweight: ~{stats['memory_with_flyweight']} KB")
print(f"Saved: ~{stats['memory_saved']} KB")

ratio = stats['total_created'] / stats['particle_types'] if stats['particle_types'] > 0 else 0
print(f"\n### Efficiency ###")
print(f"Each particle type shared by ~{ratio:.0f} particles")
print(f"Memory reduction: {(stats['memory_saved'] / stats['memory_without_flyweight'] * 100):.1f}%")

print("\n" + "="*70)
print("KEY POINT: Hundreds of particles, only 3 particle types!")
print("Sprite/texture data shared, only position/velocity unique!")
print("="*70)
```

---

## Common Pitfalls

### ❌ Pitfall 1: Making Flyweight Mutable

```python
# BAD - Mutable flyweight breaks sharing!
class BadFlyweight:
    def __init__(self, shared_data):
        self.shared_data = shared_data
        self.counter = 0  # Mutable state!
    
    def increment(self):
        self.counter += 1  # Affects all objects sharing this flyweight!

# GOOD - Immutable flyweight
class GoodFlyweight:
    def __init__(self, shared_data):
        self._shared_data = shared_data  # Immutable
    
    def operation(self, unique_state):
        # Operate using unique_state parameter
        pass
```

---

### ❌ Pitfall 2: Storing Extrinsic State in Flyweight

```python
# BAD - Position is extrinsic, shouldn't be in flyweight!
class BadTree:
    def __init__(self, species, color, x, y):
        self.species = species  # Intrinsic
        self.color = color      # Intrinsic
        self.x = x             # Extrinsic - Wrong!
        self.y = y             # Extrinsic - Wrong!

# GOOD - Separate intrinsic and extrinsic
class TreeType:  # Flyweight
    def __init__(self, species, color):
        self.species = species  # Intrinsic only
        self.color = color

class Tree:  # Context
    def __init__(self, x, y, tree_type):
        self.x = x  # Extrinsic
        self.y = y
        self._type = tree_type  # Reference to flyweight
```

---

### ❌ Pitfall 3: Not Using Factory

```python
# BAD - Creating flyweights directly (no sharing!)
class TreeType:  # Flyweight
    def __init__(self, species, color):
        self.species = species  # Intrinsic only
        self.color = color

class TreeTypeFactory:

    def __init__(self):
        self._tree_types: dict[str, TreeType] = {}
    
    def get_tree_type(self, species, color):
        pass
    
tree_type1 = TreeType("Oak", "Green")
tree_type2 = TreeType("Oak", "Green")  # Duplicate!
# These are different objects even though identical

# GOOD - Factory ensures sharing
factory = TreeTypeFactory()
tree_type1 = factory.get_tree_type("Oak", "Green")
tree_type2 = factory.get_tree_type("Oak", "Green")
# Same object, properly shared
```

---

### ❌ Pitfall 4: Using Flyweight for Few Objects

```python
# BAD - Only 5 objects, no benefit
class TreeType:  # Flyweight
    def __init__(self, species, color):
        self.species = species  # Intrinsic only
        self.color = color

        
class TreeTypeFactory:

    def __init__(self):
        self._tree_types: dict[str, TreeType] = {}
    
    def get_tree_type(self, species, color):
        pass
    
factory = TreeTypeFactory()
shared_data = {"species": "Oak", "color": "Green"}

for i in range(5):
    obj = factory.get_flyweight(shared_data)
# Overhead > benefit

# GOOD - Use flyweight for many objects
for i in range(10000):
    obj = factory.get_flyweight(shared_data)
# Significant memory savings
```

---

## Best Practices

### ✅ 1. Clearly Identify Intrinsic vs Extrinsic State

```python
# Document what's shared and what's unique
class TreeType:  # FLYWEIGHT
    """
    Intrinsic state (shared):
    - species name
    - color
    - texture
    """
    pass

class Tree:  # CONTEXT
    """
    Extrinsic state (unique):
    - x position
    - y position
    - age
    """
    pass
```

---

### ✅ 2. Make Flyweights Immutable

```python
class ImmutableFlyweight:
    def __init__(self, data):
        self._data = data  # Private, no setter
    
    @property
    def data(self):
        return self._data  # Read-only
```

---

### ✅ 3. Use Factory for All Flyweight Creation

```python
# Don't create flyweights directly
# flyweight = Flyweight(data)  ❌

# Always use factory
flyweight = factory.get_flyweight(data)  ✅
```

---

### ✅ 4. Consider Thread Safety

```python
import threading

class ThreadSafeFlyweightFactory:
    def __init__(self):
        self._flyweights = {}
        self._lock = threading.Lock()
    
    def get_flyweight(self, key):
        with self._lock:
            if key not in self._flyweights:
                self._flyweights[key] = Flyweight(key)
            return self._flyweights[key]
```

---

### ✅ 5. Measure Memory Savings

```python
class FlyweightFactory:
    def get_memory_savings(self):
        """Calculate and report memory savings"""
        objects_created = self._total_requests
        flyweights_cached = len(self._flyweights)
        
        without = objects_created * OBJECT_SIZE
        with_flyweight = flyweights_cached * OBJECT_SIZE
        saved = without - with_flyweight
        
        return f"Saved {saved} bytes ({saved/without*100:.1f}%)"
```

---

## Summary

| Aspect          | Details                                                   |
|-----------------|-----------------------------------------------------------|
| **Purpose**     | Share common data to save memory                          |
| **Use When**    | Many similar objects, limited memory                      |
| **Avoid When**  | Few objects, mostly unique data                           |
| **Key Concept** | Separate intrinsic (shared) from extrinsic (unique) state |
| **Structure**   | Flyweight (shared) + Context (unique) + Factory (manages) |

---

## Flyweight Pattern Checklist

✅ **Use Flyweight when:**
- Creating thousands/millions of similar objects
- Objects share significant common data
- Memory is limited or expensive
- Most object state can be made extrinsic
- Object identity doesn't matter (can share)

❌ **Don't use Flyweight when:**
- Few objects (< 100)
- Objects are mostly unique
- Memory isn't a concern
- Need mutable shared state
- Premature optimization

---

## Key Takeaways

1. **Memory Efficiency:** Dramatically reduces memory by sharing common data
2. **Intrinsic vs Extrinsic:** Separate what's shared (intrinsic) from what's unique (extrinsic)
3. **Immutability:** Flyweights must be immutable to be safely shared
4. **Factory Pattern:** Always use factory to manage flyweight sharing
5. **Trade-off:** Saves memory but adds complexity and some CPU overhead
6. **Use Cases:** Games (particles, sprites), text editors (characters), UI (widgets)

---

## Memory Savings Example

```python
# Without Flyweight: 1,000,000 trees
# Each tree: 100 bytes (name, color, texture, x, y)
# Total: 100 MB

# With Flyweight: 1,000,000 trees
# 3 tree types: 3 × 100 bytes = 300 bytes
# 1M positions: 1M × 20 bytes = 20 MB
# Total: ~20 MB

# Savings: 80 MB (80% reduction!)
```
