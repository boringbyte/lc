# Decorator Pattern - Complete Guide

## 📋 Table of Contents
- [What is Decorator Pattern?](#what-is-decorator-pattern)
  - [Key Characteristics](#key-characteristics)
  - [Real-World Analogy](#real-world-analogy)
  - [Visual Representation](#visual-representation)
  - [Decorator vs Adapter vs Inheritance](#decorator-vs-adapter-vs-inheritance)
- [When to Use](#when-to-use)
  - [✅ Perfect Use Cases](#-perfect-use-cases)
- [When NOT to Use](#when-not-to-use)
  - [❌ Avoid Decorator When](#-avoid-decorator-when)
- [Basic Implementation](#basic-implementation)
  - [Classic Decorator Pattern (OOP Style)](#classic-decorator-pattern-oop-style)
  - [Coffee Shop Example - Classic Illustration](#coffee-shop-example---classic-illustration)
- [Python-Specific Decorators](#python-specific-decorators)
  - [Function Decorators](#function-decorators)
- [Real-World Examples](#real-world-examples)
  - [Example 1: Text Processing Pipeline](#example-1-text-processing-pipeline)
  - [Example 2: Data Stream Processing](#example-2-data-stream-processing)
  - [Example 3: HTTP Request/Response Middleware](#example-3-http-requestresponse-middleware)
- [Common Pitfalls](#common-pitfalls)
  - [❌ Pitfall 1: Too Many Decorators (Decorator Hell)](#-pitfall-1-too-many-decorators-decorator-hell)
  - [❌ Pitfall 2: Order Matters (But Not Documented)](#-pitfall-2-order-matters-but-not-documented)
  - [❌ Pitfall 3: Breaking Interface Contract](#-pitfall-3-breaking-interface-contract)
- [Best Practices](#best-practices)
  - [✅ 1. Keep Decorators Focused (Single Responsibility)](#-1-keep-decorators-focused-single-responsibility)
  - [✅ 2. Make Decorators Independent](#-2-make-decorators-independent)
  - [✅ 3. Document Order Dependencies](#-3-document-order-dependencies)
  - [✅ 4. Use Type Hints](#-4-use-type-hints)
  - [✅ 5. Consider Using Python's Built-in Decorators](#-5-consider-using-pythons-built-in-decorators)
- [Summary](#summary)
- [Decorator vs Other Patterns](#decorator-vs-other-patterns)
---

## What is Decorator Pattern?

**Decorator Pattern** allows you to add new functionality to an object dynamically without altering its structure. It provides a flexible alternative to subclassing for extending functionality.

### Key Characteristics:
- ✅ Adds behavior to objects dynamically
- ✅ Follows Open/Closed Principle (open for extension, closed for modification)
- ✅ Alternative to subclassing
- ✅ Can wrap objects multiple times (stack decorators)
- ✅ Each decorator adds one specific responsibility

### Real-World Analogy:
Think of **getting dressed**:
- You start with your body (core object)
- Add underwear (decorator 1)
- Add shirt (decorator 2)
- Add jacket (decorator 3)
- Add scarf (decorator 4)

Each layer adds functionality without changing what's underneath. You can add/remove layers in any order.

### Visual Representation:
```
Client  →  Decorator 1   →  Decorator 2   →  Decorator 3   →  Core Object
        (adds feature A)  (adds feature B)  (adds feature C)
```

---

### Decorator vs Adapter vs Inheritance

| Pattern         | Purpose                      | Changes Interface?           |
|-----------------|------------------------------|------------------------------|
| **Decorator**   | Add responsibilities         | No - keeps same interface    |
| **Adapter**     | Convert interface            | Yes - provides new interface |
| **Inheritance** | Add behavior at compile-time | No - static                  |

---

## When to Use

### ✅ Perfect Use Cases:

#### 1. **Add Responsibilities Dynamically**
- Features needed at runtime
- Not all objects need all features
- Features can be combined

#### 2. **Avoid Explosion of Subclasses**
```
Without Decorator:
- Coffee
- CoffeeWithMilk
- CoffeeWithSugar
- CoffeeWithMilkAndSugar
- CoffeeWithMilkAndSugarAndWhippedCream
... (exponential growth!)

With Decorator:
- Coffee (base)
- MilkDecorator
- SugarDecorator
- WhippedCreamDecorator
... (linear growth, infinite combinations!)
```

#### 3. **Responsibilities Can Be Withdrawn**
- Add/remove features at runtime
- Undo decorations

#### 4. **Extension by Composition**
- Can't use inheritance (class is final)
- Want loose coupling
- Multiple orthogonal responsibilities

#### 5. **Logging, Caching, Authorization**
- Cross-cutting concerns
- Applied selectively to methods
- Stacked in different orders

---

## When NOT to Use

### ❌ Avoid Decorator When:

1. **Single, Simple Enhancement**
   - Just one feature to add
   - Inheritance is simpler

2. **Core Object Changes Often**
   - Decorators depend on stable interface
   - Interface changes break decorators

3. **Order Doesn't Matter**
   - If decorators are order-independent
   - Might be simpler approach

4. **Too Many Small Decorators**
   - Creates complexity
   - Hard to understand decoration chain
   - Debug nightmare

---

## Basic Implementation

### Classic Decorator Pattern (OOP Style)

```python
from abc import ABC, abstractmethod

# ============ COMPONENT INTERFACE ============

class Component(ABC):
    """Base interface for objects that can have responsibilities added"""
    
    @abstractmethod
    def operation(self) -> str:
        pass

# ============ CONCRETE COMPONENT ============

class ConcreteComponent(Component):
    """The core object to which we'll add responsibilities"""
    
    def operation(self) -> str:
        return "ConcreteComponent"

# ============ BASE DECORATOR ============

class Decorator(Component):
    """
    Base decorator class.
    Maintains a reference to a Component object and implements the Component interface.
    """
    
    def __init__(self, component: Component):
        self._component = component
    
    def operation(self) -> str:
        """Delegates to the wrapped component"""
        return self._component.operation()

# ============ CONCRETE DECORATORS ============

class ConcreteDecoratorA(Decorator):
    """Adds responsibility A"""
    
    def operation(self) -> str:
        # Call wrapped component and add behavior
        return f"ConcreteDecoratorA({self._component.operation()})"

class ConcreteDecoratorB(Decorator):
    """Adds responsibility B"""
    
    def operation(self) -> str:
        return f"ConcreteDecoratorB({self._component.operation()})"

# ============ USAGE ============

# Simple component
simple = ConcreteComponent()
print(simple.operation())
# Output: ConcreteComponent

# Decorate with A
decorated_a = ConcreteDecoratorA(simple)
print(decorated_a.operation())
# Output: ConcreteDecoratorA(ConcreteComponent)

# Decorate with B
decorated_b = ConcreteDecoratorB(simple)
print(decorated_b.operation())
# Output: ConcreteDecoratorB(ConcreteComponent)

# Stack decorators!
decorated_both = ConcreteDecoratorB(ConcreteDecoratorA(simple))
print(decorated_both.operation())
# Output: ConcreteDecoratorB(ConcreteDecoratorA(ConcreteComponent))

# Different order = different result
decorated_reverse = ConcreteDecoratorA(ConcreteDecoratorB(simple))
print(decorated_reverse.operation())
# Output: ConcreteDecoratorA(ConcreteDecoratorB(ConcreteComponent))
```

---

### Coffee Shop Example - Classic Illustration

```python
from abc import ABC, abstractmethod

# ============ COMPONENT INTERFACE ============

class Beverage(ABC):
    """Abstract beverage"""
    
    def __init__(self):
        self.description = "Unknown Beverage"
    
    def get_description(self) -> str:
        return self.description
    
    @abstractmethod
    def cost(self) -> float:
        pass

# ============ CONCRETE COMPONENTS ============

class Espresso(Beverage):
    def __init__(self):
        super().__init__()
        self.description = "Espresso"
    
    def cost(self) -> float:
        return 1.99

class HouseBlend(Beverage):
    def __init__(self):
        super().__init__()
        self.description = "House Blend Coffee"
    
    def cost(self) -> float:
        return 0.89

class DarkRoast(Beverage):
    def __init__(self):
        super().__init__()
        self.description = "Dark Roast Coffee"
    
    def cost(self) -> float:
        return 0.99

class Decaf(Beverage):
    def __init__(self):
        super().__init__()
        self.description = "Decaf Coffee"
    
    def cost(self) -> float:
        return 1.05

# ============ BASE DECORATOR ============

class CondimentDecorator(Beverage):
    """Base class for condiment decorators"""
    
    def __init__(self, beverage: Beverage):
        super().__init__()
        self._beverage = beverage
    
    @abstractmethod
    def get_description(self) -> str:
        pass

# ============ CONCRETE DECORATORS ============

class Milk(CondimentDecorator):
    def get_description(self) -> str:
        return self._beverage.get_description() + ", Milk"
    
    def cost(self) -> float:
        return self._beverage.cost() + 0.10

class Mocha(CondimentDecorator):
    def get_description(self) -> str:
        return self._beverage.get_description() + ", Mocha"
    
    def cost(self) -> float:
        return self._beverage.cost() + 0.20

class Soy(CondimentDecorator):
    def get_description(self) -> str:
        return self._beverage.get_description() + ", Soy"
    
    def cost(self) -> float:
        return self._beverage.cost() + 0.15

class Whip(CondimentDecorator):
    def get_description(self) -> str:
        return self._beverage.get_description() + ", Whip"
    
    def cost(self) -> float:
        return self._beverage.cost() + 0.10

class Caramel(CondimentDecorator):
    def get_description(self) -> str:
        return self._beverage.get_description() + ", Caramel"
    
    def cost(self) -> float:
        return self._beverage.cost() + 0.25

# ============ USAGE ============

print("="*60)
print("COFFEE ORDERS")
print("="*60)

# Order 1: Simple espresso
beverage1 = Espresso()
print(f"{beverage1.get_description()}")
print(f"${beverage1.cost():.2f}\n")

# Order 2: Dark Roast with Milk and Mocha
beverage2 = DarkRoast()
beverage2 = Milk(beverage2)
beverage2 = Mocha(beverage2)
print(f"{beverage2.get_description()}")
print(f"${beverage2.cost():.2f}\n")

# Order 3: House Blend with Soy, Mocha, and Whip
beverage3 = HouseBlend()
beverage3 = Soy(beverage3)
beverage3 = Mocha(beverage3)
beverage3 = Whip(beverage3)
print(f"{beverage3.get_description()}")
print(f"${beverage3.cost():.2f}\n")

# Order 4: Decaf with everything!
beverage4 = Decaf()
beverage4 = Milk(beverage4)
beverage4 = Mocha(beverage4)
beverage4 = Soy(beverage4)
beverage4 = Whip(beverage4)
beverage4 = Caramel(beverage4)
print(f"{beverage4.get_description()}")
print(f"${beverage4.cost():.2f}\n")

# Order 5: Double Mocha!
beverage5 = Espresso()
beverage5 = Mocha(beverage5)
beverage5 = Mocha(beverage5)  # Add mocha twice!
beverage5 = Whip(beverage5)
print(f"{beverage5.get_description()}")
print(f"${beverage5.cost():.2f}")
```

**Output:**
```
============================================================
COFFEE ORDERS
============================================================
Espresso
$1.99

Dark Roast Coffee, Milk, Mocha
$1.29

House Blend Coffee, Soy, Mocha, Whip
$1.34

Decaf Coffee, Milk, Mocha, Soy, Whip, Caramel
$1.85

Espresso, Mocha, Mocha, Whip
$2.49
```

---

## Python-Specific Decorators

Python has built-in decorator syntax using `@` which is different but related to the Decorator Pattern.

### Function Decorators

```python
import time
from functools import wraps

# ============ SIMPLE FUNCTION DECORATOR ============

def timer_decorator(func):
    """Decorator that times function execution"""
    
    @wraps(func)  # Preserves original function's metadata
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"⏱️  {func.__name__} took {end_time - start_time:.4f} seconds")
        return result
    
    return wrapper

def logging_decorator(func):
    """Decorator that logs function calls"""
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"📝 Calling {func.__name__} with args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"✅ {func.__name__} returned {result}")
        return result
    
    return wrapper

def retry_decorator(max_attempts=3):
    """Decorator that retries function on failure"""
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"❌ Attempt {attempt + 1} failed: {e}")
                    if attempt == max_attempts - 1:
                        raise
                    time.sleep(1)  # Wait before retry
        return wrapper
    return decorator

# ============ USAGE ============

@timer_decorator
def slow_function():
    """A slow function"""
    time.sleep(1)
    return "Done!"

@logging_decorator
def add(a, b):
    """Add two numbers"""
    return a + b

@retry_decorator(max_attempts=3)
def unreliable_function():
    """Function that might fail"""
    import random
    if random.random() < 0.7:
        raise ValueError("Random failure!")
    return "Success!"

# Stacking decorators
@timer_decorator
@logging_decorator
def complex_function(x, y):
    """Function with multiple decorators"""
    time.sleep(0.5)
    return x * y

# Test functions
print("="*60)
print("Testing decorators")
print("="*60)

slow_function()
print()

add(5, 3)
print()

try:
    unreliable_function()
except ValueError:
    print("All attempts failed")
print()

complex_function(4, 5)
```

---

## Real-World Examples

### Example 1: Text Processing Pipeline

```python
from abc import ABC, abstractmethod

# ============ COMPONENT INTERFACE ============

class TextProcessor(ABC):
    """Base interface for text processing"""
    
    @abstractmethod
    def process(self, text: str) -> str:
        pass

# ============ CONCRETE COMPONENT ============

class PlainTextProcessor(TextProcessor):
    """Basic text processor that returns text as-is"""
    
    def process(self, text: str) -> str:
        return text

# ============ DECORATORS ============

class TextDecorator(TextProcessor):
    """Base decorator for text processing"""
    
    def __init__(self, processor: TextProcessor):
        self._processor = processor
    
    def process(self, text: str) -> str:
        return self._processor.process(text)

class UpperCaseDecorator(TextDecorator):
    """Converts text to uppercase"""
    
    def process(self, text: str) -> str:
        processed = self._processor.process(text)
        return processed.upper()

class TrimDecorator(TextDecorator):
    """Trims whitespace from text"""
    
    def process(self, text: str) -> str:
        processed = self._processor.process(text)
        return processed.strip()

class HTMLEscapeDecorator(TextDecorator):
    """Escapes HTML special characters"""
    
    def process(self, text: str) -> str:
        processed = self._processor.process(text)
        return (processed
                .replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;')
                .replace('"', '&quot;')
                .replace("'", '&#x27;'))

class MarkdownToHTMLDecorator(TextDecorator):
    """Converts simple markdown to HTML"""
    
    def process(self, text: str) -> str:
        processed = self._processor.process(text)
        
        # Bold: **text** -> <strong>text</strong>
        import re
        processed = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', processed)
        
        # Italic: *text* -> <em>text</em>
        processed = re.sub(r'\*(.*?)\*', r'<em>\1</em>', processed)
        
        # Links: [text](url) -> <a href="url">text</a>
        processed = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', processed)
        
        return processed

class ProfanityFilterDecorator(TextDecorator):
    """Filters profanity from text"""
    
    def __init__(self, processor: TextProcessor):
        super().__init__(processor)
        self.profanity_list = ['badword1', 'badword2', 'damn', 'hell']
    
    def process(self, text: str) -> str:
        processed = self._processor.process(text)
        
        for word in self.profanity_list:
            processed = processed.replace(word, '*' * len(word))
            processed = processed.replace(word.capitalize(), '*' * len(word))
        
        return processed

class TruncateDecorator(TextDecorator):
    """Truncates text to specified length"""
    
    def __init__(self, processor: TextProcessor, max_length: int = 50):
        super().__init__(processor)
        self.max_length = max_length
    
    def process(self, text: str) -> str:
        processed = self._processor.process(text)
        
        if len(processed) > self.max_length:
            return processed[:self.max_length - 3] + "..."
        return processed

class WordCountDecorator(TextDecorator):
    """Adds word count at the end"""
    
    def process(self, text: str) -> str:
        processed = self._processor.process(text)
        word_count = len(processed.split())
        return f"{processed} [Word count: {word_count}]"

# ============ USAGE ============

print("="*60)
print("TEXT PROCESSING PIPELINE")
print("="*60)

# Example 1: Clean user input
user_input = "  Hello World!  "
processor1 = PlainTextProcessor()
processor1 = TrimDecorator(processor1)
processor1 = UpperCaseDecorator(processor1)

print("Original:", repr(user_input))
print("Processed:", processor1.process(user_input))
print()

# Example 2: Sanitize HTML
html_input = "<script>alert('XSS')</script>Hello & goodbye"
processor2 = PlainTextProcessor()
processor2 = HTMLEscapeDecorator(processor2)

print("Original:", html_input)
print("Processed:", processor2.process(html_input))
print()

# Example 3: Convert markdown with profanity filter
markdown_text = "This is **bold** and this is *italic*. Also, damn this is cool!"
processor3 = PlainTextProcessor()
processor3 = MarkdownToHTMLDecorator(processor3)
processor3 = ProfanityFilterDecorator(processor3)

print("Original:", markdown_text)
print("Processed:", processor3.process(markdown_text))
print()

# Example 4: Social media post processing
long_text = "This is a very long social media post that needs to be truncated because it exceeds the maximum allowed length for display in the feed"
processor4 = PlainTextProcessor()
processor4 = TrimDecorator(processor4)
processor4 = ProfanityFilterDecorator(processor4)
processor4 = TruncateDecorator(processor4, max_length=50)

print("Original:", long_text)
print("Processed:", processor4.process(long_text))
print()

# Example 5: Blog post processing
blog_text = "Check out this [amazing link](https://example.com)! It's **really** cool."
processor5 = PlainTextProcessor()
processor5 = MarkdownToHTMLDecorator(processor5)
processor5 = WordCountDecorator(processor5)

print("Original:", blog_text)
print("Processed:", processor5.process(blog_text))
```

---

### Example 2: Data Stream Processing

```python
from abc import ABC, abstractmethod
from typing import Any
import json
import gzip
import base64

# ============ COMPONENT INTERFACE ============

class DataStream(ABC):
    """Base interface for data streams"""
    
    @abstractmethod
    def write(self, data: str) -> None:
        pass
    
    @abstractmethod
    def read(self) -> str:
        pass

# ============ CONCRETE COMPONENT ============

class FileDataStream(DataStream):
    """Concrete component - writes/reads plain data"""
    
    def __init__(self, filename: str):
        self.filename = filename
        self.data = ""
    
    def write(self, data: str) -> None:
        self.data = data
        print(f"📄 Writing {len(data)} bytes to {self.filename}")
    
    def read(self) -> str:
        print(f"📄 Reading from {self.filename}")
        return self.data

# ============ DECORATORS ============

class DataStreamDecorator(DataStream):
    """Base decorator"""
    
    def __init__(self, stream: DataStream):
        self._stream = stream
    
    def write(self, data: str) -> None:
        self._stream.write(data)
    
    def read(self) -> str:
        return self._stream.read()

class CompressionDecorator(DataStreamDecorator):
    """Compresses data before writing, decompresses after reading"""
    
    def write(self, data: str) -> None:
        compressed = gzip.compress(data.encode('utf-8'))
        print(f"🗜️  Compressed {len(data)} bytes to {len(compressed)} bytes")
        # Convert bytes to string for storage
        compressed_str = base64.b64encode(compressed).decode('utf-8')
        self._stream.write(compressed_str)
    
    def read(self) -> str:
        compressed_str = self._stream.read()
        compressed = base64.b64decode(compressed_str.encode('utf-8'))
        decompressed = gzip.decompress(compressed).decode('utf-8')
        print(f"🗜️  Decompressed {len(compressed)} bytes to {len(decompressed)} bytes")
        return decompressed

class EncryptionDecorator(DataStreamDecorator):
    """Encrypts data before writing, decrypts after reading"""
    
    def __init__(self, stream: DataStream, key: str = "secret"):
        super().__init__(stream)
        self.key = key
    
    def _xor_encrypt_decrypt(self, data: str) -> str:
        """Simple XOR encryption (for demonstration only!)"""
        key_bytes = self.key.encode()
        data_bytes = data.encode()
        
        result = bytearray()
        for i, byte in enumerate(data_bytes):
            result.append(byte ^ key_bytes[i % len(key_bytes)])
        
        return base64.b64encode(result).decode('utf-8')
    
    def write(self, data: str) -> None:
        encrypted = self._xor_encrypt_decrypt(data)
        print(f"🔐 Encrypted data (length: {len(encrypted)})")
        self._stream.write(encrypted)
    
    def read(self) -> str:
        encrypted = self._stream.read()
        decrypted_bytes = base64.b64decode(encrypted.encode('utf-8'))
        
        key_bytes = self.key.encode()
        result = bytearray()
        for i, byte in enumerate(decrypted_bytes):
            result.append(byte ^ key_bytes[i % len(key_bytes)])
        
        decrypted = result.decode('utf-8')
        print(f"🔓 Decrypted data (length: {len(decrypted)})")
        return decrypted

class Base64Decorator(DataStreamDecorator):
    """Encodes data to base64 before writing, decodes after reading"""
    
    def write(self, data: str) -> None:
        encoded = base64.b64encode(data.encode('utf-8')).decode('utf-8')
        print(f"📝 Base64 encoded {len(data)} bytes to {len(encoded)} bytes")
        self._stream.write(encoded)
    
    def read(self) -> str:
        encoded = self._stream.read()
        decoded = base64.b64decode(encoded.encode('utf-8')).decode('utf-8')
        print(f"📝 Base64 decoded {len(encoded)} bytes to {len(decoded)} bytes")
        return decoded

class ValidationDecorator(DataStreamDecorator):
    """Validates data before writing"""
    
    def write(self, data: str) -> None:
        if not data:
            raise ValueError("Cannot write empty data")
        
        if len(data) > 1000000:  # 1MB limit
            raise ValueError("Data too large")
        
        print(f"✅ Validation passed for {len(data)} bytes")
        self._stream.write(data)
    
    def read(self) -> str:
        data = self._stream.read()
        print(f"✅ Read validation passed")
        return data

class LoggingDecorator(DataStreamDecorator):
    """Logs all operations"""
    
    def write(self, data: str) -> None:
        print(f"📋 LOG: Writing data of length {len(data)}")
        self._stream.write(data)
        print(f"📋 LOG: Write completed")
    
    def read(self) -> str:
        print(f"📋 LOG: Reading data")
        data = self._stream.read()
        print(f"📋 LOG: Read completed, got {len(data)} bytes")
        return data

# ============ USAGE ============

print("="*70)
print("DATA STREAM PROCESSING")
print("="*70)

# Example 1: Simple file with logging
print("\n--- Example 1: Simple File with Logging ---")
stream1 = FileDataStream("data1.txt")
stream1 = LoggingDecorator(stream1)

stream1.write("Hello, World!")
data1 = stream1.read()
print(f"Result: {data1}")

# Example 2: Compressed file
print("\n--- Example 2: Compressed File ---")
stream2 = FileDataStream("data2.txt.gz")
stream2 = CompressionDecorator(stream2)

long_text = "This is a long text " * 50
stream2.write(long_text)
data2 = stream2.read()
print(f"Result length: {len(data2)}")
print(f"Data matches: {data2 == long_text}")

# Example 3: Encrypted and compressed
print("\n--- Example 3: Encrypted and Compressed ---")
stream3 = FileDataStream("secure.dat")
stream3 = CompressionDecorator(stream3)
stream3 = EncryptionDecorator(stream3, key="my-secret-key")
stream3 = LoggingDecorator(stream3)

sensitive_data = "This is sensitive information: SSN 123-45-6789"
stream3.write(sensitive_data)
data3 = stream3.read()
print(f"Result: {data3}")
print(f"Data matches: {data3 == sensitive_data}")

# Example 4: Full pipeline with validation
print("\n--- Example 4: Full Pipeline ---")
stream4 = FileDataStream("full-pipeline.dat")
stream4 = ValidationDecorator(stream4)
stream4 = CompressionDecorator(stream4)
stream4 = EncryptionDecorator(stream4)
stream4 = Base64Decorator(stream4)
stream4 = LoggingDecorator(stream4)

pipeline_data = json.dumps({
    "user": "john_doe",
    "data": "Important information",
    "timestamp": "2024-02-08"
})

stream4.write(pipeline_data)
data4 = stream4.read()
print(f"Result: {data4}")
print(f"Parsed: {json.loads(data4)}")
```

---

### Example 3: HTTP Request/Response Middleware

```python
from abc import ABC, abstractmethod
from typing import Any
from datetime import datetime
import time

# ============ COMPONENT INTERFACE ============

class HTTPHandler(ABC):
    """Base interface for HTTP handlers"""
    
    @abstractmethod
    def handle(self, request: dict[str, Any]) -> dict[str, Any]:
        pass

# ============ CONCRETE COMPONENT ============

class BaseHTTPHandler(HTTPHandler):
    """Basic HTTP handler"""
    
    def handle(self, request: dict[str, Any]) -> dict[str, Any]:
        # Simulate request processing
        return {
            'status': 200,
            'body': {'message': 'Success', 'data': request.get('body')},
            'headers': {'Content-Type': 'application/json'}
        }

# ============ DECORATORS (MIDDLEWARE) ============

class HTTPHandlerDecorator(HTTPHandler):
    """Base decorator for HTTP handlers"""
    
    def __init__(self, handler: HTTPHandler):
        self._handler = handler
    
    def handle(self, request: dict[str, Any]) -> dict[str, Any]:
        return self._handler.handle(request)

class AuthenticationMiddleware(HTTPHandlerDecorator):
    """Checks authentication before processing request"""
    
    def handle(self, request: dict[str, Any]) -> dict[str, Any]:
        print("🔐 Authentication Middleware: Checking credentials...")
        
        # Check for auth token
        auth_header = request.get('headers', {}).get('Authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            print("❌ Authentication failed: No valid token")
            return {
                'status': 401,
                'body': {'error': 'Unauthorized'},
                'headers': {}
            }
        
        # Validate token (simplified)
        token = auth_header.replace('Bearer ', '')
        if token != 'valid-token-123':
            print("❌ Authentication failed: Invalid token")
            return {
                'status': 401,
                'body': {'error': 'Invalid token'},
                'headers': {}
            }
        
        print("✅ Authentication successful")
        # Add user info to request
        request['user'] = {'id': 123, 'name': 'John Doe'}
        
        return self._handler.handle(request)

class RateLimitMiddleware(HTTPHandlerDecorator):
    """Rate limiting middleware"""
    
    def __init__(self, handler: HTTPHandler, max_requests: int = 5):
        super().__init__(handler)
        self.max_requests = max_requests
        self.requests = {}  # ip -> [timestamps]
    
    def handle(self, request: dict[str, Any]) -> dict[str, Any]:
        print("⏱️  Rate Limit Middleware: Checking request rate...")
        
        client_ip = request.get('ip', 'unknown')
        current_time = time.time()
        
        # Initialize or clean old requests
        if client_ip not in self.requests:
            self.requests[client_ip] = []
        
        # Remove requests older than 60 seconds
        self.requests[client_ip] = [
            ts for ts in self.requests[client_ip]
            if current_time - ts < 60
        ]
        
        # Check rate limit
        if len(self.requests[client_ip]) >= self.max_requests:
            print(f"❌ Rate limit exceeded for {client_ip}")
            return {
                'status': 429,
                'body': {'error': 'Too many requests'},
                'headers': {'Retry-After': '60'}
            }
        
        # Add current request
        self.requests[client_ip].append(current_time)
        print(f"✅ Rate limit OK ({len(self.requests[client_ip])}/{self.max_requests})")
        
        return self._handler.handle(request)

class LoggingMiddleware(HTTPHandlerDecorator):
    """Logs all requests and responses"""
    
    def handle(self, request: dict[str, Any]) -> dict[str, Any]:
        print("\n" + "="*60)
        print("📋 Logging Middleware: Incoming request")
        print(f"   Method: {request.get('method', 'GET')}")
        print(f"   Path: {request.get('path', '/')}")
        print(f"   IP: {request.get('ip', 'unknown')}")
        print(f"   Timestamp: {datetime.now()}")
        
        start_time = time.time()
        response = self._handler.handle(request)
        duration = time.time() - start_time
        
        print(f"\n📋 Logging Middleware: Response")
        print(f"   Status: {response.get('status')}")
        print(f"   Duration: {duration:.4f}s")
        print("="*60 + "\n")
        
        return response

class CORSMiddleware(HTTPHandlerDecorator):
    """Adds CORS headers to response"""
    
    def handle(self, request: dict[str, Any]) -> dict[str, Any]:
        print("🌐 CORS Middleware: Adding CORS headers...")
        
        response = self._handler.handle(request)
        
        # Add CORS headers
        response['headers']['Access-Control-Allow-Origin'] = '*'
        response['headers']['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE'
        response['headers']['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        
        print("✅ CORS headers added")
        return response

class CacheMiddleware(HTTPHandlerDecorator):
    """Caches GET requests"""
    
    def __init__(self, handler: HTTPHandler):
        super().__init__(handler)
        self.cache = {}
    
    def handle(self, request: dict[str, Any]) -> dict[str, Any]:
        method = request.get('method', 'GET')
        path = request.get('path', '/')
        
        if method != 'GET':
            print("💾 Cache Middleware: Not caching non-GET request")
            return self._handler.handle(request)
        
        cache_key = f"{method}:{path}"
        
        if cache_key in self.cache:
            print(f"💾 Cache Middleware: Cache HIT for {cache_key}")
            cached_response = self.cache[cache_key].copy()
            cached_response['headers']['X-Cache'] = 'HIT'
            return cached_response
        
        print(f"💾 Cache Middleware: Cache MISS for {cache_key}")
        response = self._handler.handle(request)
        
        # Cache successful responses
        if response.get('status') == 200:
            self.cache[cache_key] = response.copy()
            print(f"💾 Cache Middleware: Cached response for {cache_key}")
        
        response['headers']['X-Cache'] = 'MISS'
        return response

class ErrorHandlingMiddleware(HTTPHandlerDecorator):
    """Catches and handles errors"""
    
    def handle(self, request: dict[str, Any]) -> dict[str, Any]:
        print("🛡️  Error Handling Middleware: Processing request...")
        
        try:
            return self._handler.handle(request)
        except Exception as e:
            print(f"❌ Error caught: {str(e)}")
            return {
                'status': 500,
                'body': {'error': 'Internal server error', 'message': str(e)},
                'headers': {}
            }

# ============ USAGE ============

print("="*70)
print("HTTP MIDDLEWARE PIPELINE")
print("="*70)

# Build the middleware stack
handler = BaseHTTPHandler()
handler = ErrorHandlingMiddleware(handler)
handler = CacheMiddleware(handler)
handler = CORSMiddleware(handler)
handler = RateLimitMiddleware(handler, max_requests=3)
handler = AuthenticationMiddleware(handler)
handler = LoggingMiddleware(handler)

# Test 1: Successful authenticated request
print("\n### TEST 1: Successful Request ###")
request1 = {
    'method': 'GET',
    'path': '/api/users',
    'ip': '192.168.1.1',
    'headers': {'Authorization': 'Bearer valid-token-123'},
    'body': {}
}
response1 = handler.handle(request1)
print(f"Final Response: {response1['status']} - {response1['body']}")

# Test 2: Same request (should be cached)
print("\n### TEST 2: Cached Request ###")
response2 = handler.handle(request1)
print(f"Final Response: {response2['status']} - Cache: {response2['headers'].get('X-Cache')}")

# Test 3: Unauthorized request
print("\n### TEST 3: Unauthorized Request ###")
request3 = {
    'method': 'GET',
    'path': '/api/users',
    'ip': '192.168.1.1',
    'headers': {},
    'body': {}
}
response3 = handler.handle(request3)
print(f"Final Response: {response3['status']} - {response3['body']}")

# Test 4: Rate limit exceeded
print("\n### TEST 4: Rate Limit Test ###")
for i in range(5):
    print(f"\n--- Request {i+1} ---")
    response = handler.handle(request1)
    print(f"Status: {response['status']}")
```

---

## Common Pitfalls

### ❌ Pitfall 1: Too Many Decorators (Decorator Hell)

```python
# BAD - Hard to understand and debug
result = (Decorator10(
            Decorator9(
              Decorator8(
                Decorator7(
                  Decorator6(
                    Decorator5(
                      Decorator4(
                        Decorator3(
                          Decorator2(
                            Decorator1(
                              BaseComponent()
                            )
                          )
                        )
                      )
                    )
                  )
                )
              )
            )
          )).operation()

# GOOD - Use builder or factory to manage complexity
from abc import ABC

class Component(ABC):
   pass

class BaseComponent(Component):
   pass

class Decorator(Component):
   pass

class LoggingDecorator(Decorator):
   pass

class CachingDecorator(Decorator):
   pass

class DecoratorBuilder:
    def __init__(self, component):
        self.component = component
    
    def with_logging(self):
        self.component = LoggingDecorator(self.component)
        return self
    
    def with_caching(self):
        self.component = CachingDecorator(self.component)
        return self
    
    def build(self):
        return self.component

result = (DecoratorBuilder(BaseComponent())
          .with_logging()
          .with_caching()
          .build()).operation()
```

---

### ❌ Pitfall 2: Order Matters (But Not Documented)

```python
# BAD - Order matters but not clear
component = Decorator2(Decorator1(Base()))

# GOOD - Document order dependencies
"""
Decorator order matters:
1. ValidationDecorator - must be first to validate input
2. EncryptionDecorator - encrypt before compression
3. CompressionDecorator - compress encrypted data
4. LoggingDecorator - log final result
"""
component = (LoggingDecorator(
              CompressionDecorator(
                EncryptionDecorator(
                  ValidationDecorator(Base())
                )
              )
            ))
```

---

### ❌ Pitfall 3: Breaking Interface Contract

```python
# BAD - Decorator changes return type
class BadDecorator(Component):
    def operation(self) -> str:  # Should return str
        result = self._component.operation()
        return len(result)  # Returns int instead!

# GOOD - Maintain interface
class GoodDecorator(Component):
    def operation(self) -> str:
        result = self._component.operation()
        # Add functionality but maintain contract
        return f"[Decorated] {result}"
```

---

## Best Practices

### ✅ 1. Keep Decorators Focused (Single Responsibility)

```python
# GOOD - Each decorator does one thing
class LoggingDecorator:
    """Only logs"""
    pass

class CachingDecorator:
    """Only caches"""
    pass

# BAD - Decorator does too much
class SuperDecorator:
    """Logs, caches, validates, transforms..."""
    pass
```

---

### ✅ 2. Make Decorators Independent

```python
# GOOD - Decorators work independently
cache_only = CachingDecorator(Base())
log_only = LoggingDecorator(Base())
both = LoggingDecorator(CachingDecorator(Base()))

# All three work correctly
```

---

### ✅ 3. Document Order Dependencies

```python
class EncryptionDecorator:
    """
    Encrypts data.
    
    IMPORTANT: Apply BEFORE CompressionDecorator.
    Compressing encrypted data is more efficient.
    """
    pass
```

---

### ✅ 4. Use Type Hints

```python
from typing import Protocol

class Component(Protocol):
    def operation(self) -> str: ...

class Decorator:
    def __init__(self, component: Component) -> None:
        self._component = component
    
    def operation(self) -> str:
        return self._component.operation()
```

---

### ✅ 5. Consider Using Python's Built-in Decorators

For simpler cases, Python's `@decorator` syntax is cleaner:

```python
# Instead of this (OOP Decorator Pattern):
handler = LoggingDecorator(
           AuthDecorator(
             BaseHandler()
           )
         )

# Use this (Python decorators):
@logging_decorator
@auth_decorator
def handle_request():
    # handler code
    pass
```

---

## Summary

| Aspect               | Details                                                  |
|----------------------|----------------------------------------------------------|
| **Purpose**          | Add responsibilities to objects dynamically              |
| **Use When**         | Need flexible feature addition, avoid subclass explosion |
| **Avoid When**       | Simple addition, too many decorators, order complexity   |
| **Key Benefit**      | Flexible alternative to subclassing                      |
| **Common Use Cases** | Logging, caching, authentication, data transformation    |

---

## Decorator vs Other Patterns

| Pattern       | Purpose                  | Structure                                     |
|---------------|--------------------------|-----------------------------------------------|
| **Decorator** | Add behavior dynamically | Wraps object, same interface                  |
| **Adapter**   | Convert interface        | Wraps object, different interface             |
| **Proxy**     | Control access           | Wraps object, same interface, controls access |
| **Composite** | Part-whole hierarchy     | Tree structure                                |
