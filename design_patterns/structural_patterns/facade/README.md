# Facade Pattern - Complete Guide

## 📋 Table of Contents
- [What is Facade Pattern?](#what-is-facade-pattern)
  - [Key Characteristics](#key-characteristics)
  - [Real-World Analogy](#real-world-analogy)
  - [Visual Representation](#visual-representation)
  - [Facade vs Other Patterns](#facade-vs-other-patterns)
- [When to Use](#when-to-use)
  - [✅ Perfect Use Cases](#-perfect-use-cases)
- [When NOT to Use](#when-not-to-use)
  - [❌ Avoid Facade When](#-avoid-facade-when)
- [Basic Implementation](#basic-implementation)
  - [Simple Facade Example](#simple-facade-example)
- [Real-World Examples](#real-world-examples)
  - [Example 1: Home Theater System](#example-1-home-theater-system)
  - [Example 2: E-commerce Order Processing](#example-2-e-commerce-order-processing)
  - [Example 3: Video Conversion System](#example-3-video-conversion-system)
- [Common Pitfalls](#common-pitfalls)
  - [❌ Pitfall 1: Facade Becomes God Object](#-pitfall-1-facade-becomes-god-object)
  - [❌ Pitfall 2: Facade Duplicates Subsystem Interface](#-pitfall-2-facade-duplicates-subsystem-interface)
  - [❌ Pitfall 3: Hiding Important Errors](#-pitfall-3-hiding-important-errors)
  - [❌ Pitfall 4: Too Many Parameters](#-pitfall-4-too-many-parameters)
- [Best Practices](#best-practices)
  - [✅ 1. Keep Facade Focused](#-1-keep-facade-focused)
  - [✅ 2. Provide Multiple Levels of Abstraction](#-2-provide-multiple-levels-of-abstraction)
  - [✅ 3. Document What's Being Simplified](#-3-document-whats-being-simplified)
  - [✅ 4. Don't Prevent Direct Access](#-4-dont-prevent-direct-access)
  - [✅ 5. Use Dependency Injection](#-5-use-dependency-injection)
- [Summary](#summary)
- [Facade vs Other Patterns](#facade-vs-other-patterns)
- [When to Use Which Pattern?](#when-to-use-which-pattern)
---

## What is Facade Pattern?

**Facade Pattern** provides a unified, simplified interface to a complex subsystem. It doesn't hide the subsystem; it just provides a higher-level interface that makes the subsystem easier to use.

### Key Characteristics:
- ✅ Provides a simple interface to a complex system
- ✅ Reduces dependencies on subsystem components
- ✅ Doesn't prevent access to subsystem if needed
- ✅ Promotes loose coupling
- ✅ Makes code more readable and maintainable

### Real-World Analogy:
Think of a **restaurant**:
- **Without Facade:** You go to the kitchen, tell the chef exactly what ingredients to use, how to prepare them, coordinate with the dishwasher, manage the stove, etc.
- **With Facade (Waiter):** You just tell the waiter "I'll have the steak, medium rare." The waiter handles all the complex coordination with the kitchen staff.

The waiter is the **facade** - simplifying your interaction with the complex kitchen subsystem.

### Visual Representation:
```
Client → [Facade] → Subsystem A
                  → Subsystem B
                  → Subsystem C
                  → Subsystem D

Instead of:

Client → Subsystem A
       → Subsystem B
       → Subsystem C
       → Subsystem D
```


### Facade vs Other Patterns

| Pattern      | Purpose                          | Hides Complexity?                   |
|--------------|----------------------------------|-------------------------------------|
| **Facade**   | Simplify interface to subsystem  | Yes, but subsystem still accessible |
| **Adapter**  | Convert one interface to another | No, just converts                   |
| **Proxy**    | Control access to object         | No, same interface                  |
| **Mediator** | Reduce communication complexity  | Yes, centralizes interactions       |

---

## When to Use

### ✅ Perfect Use Cases:

#### 1. **Complex Subsystems**
- Many classes with complex interactions
- Difficult initialization sequences
- Hard to understand APIs

#### 2. **Layered Architecture**
- Entry point to each layer
- Decouple layers from each other
- Define clear boundaries

#### 3. **Legacy System Integration**
- Old system is complex
- Want simple interface for new code
- Don't want to expose complexity

#### 4. **Third-Party Libraries**
- External library is complicated
- Only use small part of functionality
- Want to insulate from library changes

#### 5. **Reduce Coupling**
- Many classes depend on subsystem
- Want to reduce dependencies
- Make system easier to refactor

---

## When NOT to Use

### ❌ Avoid Facade When:

1. **Simple Subsystem**
   - Only a few classes
   - Already easy to use
   - Adds unnecessary layer

2. **Need Fine-Grained Control**
   - Clients need direct access to subsystem
   - Facade limits flexibility
   - Performance-critical operations

3. **Constantly Changing Requirements**
   - Facade needs frequent updates
   - Becomes maintenance burden
   - Defeats simplification purpose

4. **Over-Simplification**
   - Hides important details
   - Clients need to know complexity
   - Loss of functionality

---

## Basic Implementation

### Simple Facade Example

```python
# ============ COMPLEX SUBSYSTEM ============

class CPU:
    """Complex subsystem component"""
    
    def freeze(self):
        print("CPU: Freezing processor")
    
    def jump(self, position: int):
        print(f"CPU: Jumping to position {position}")
    
    def execute(self):
        print("CPU: Executing instructions")

class Memory:
    """Complex subsystem component"""
    
    def load(self, position: int, data: str):
        print(f"Memory: Loading '{data}' at position {position}")

class HardDrive:
    """Complex subsystem component"""
    
    def read(self, sector: int, size: int) -> str:
        print(f"HardDrive: Reading {size} bytes from sector {sector}")
        return "boot_data"

# ============ FACADE ============

class ComputerFacade:
    """
    Facade that simplifies the process of starting a computer.
    
    Without facade, client would need to:
    1. Freeze the CPU
    2. Load boot sector from hard drive
    3. Load data into memory
    4. Jump CPU to boot position
    5. Execute
    
    With facade: Just call start()
    """
    
    def __init__(self):
        self.cpu = CPU()
        self.memory = Memory()
        self.hard_drive = HardDrive()
    
    def start(self):
        """Simplified interface to start computer"""
        print("=" * 50)
        print("Starting computer...")
        print("=" * 50)
        
        self.cpu.freeze()
        
        boot_data = self.hard_drive.read(
            sector=0,
            size=1024
        )
        
        self.memory.load(
            position=0,
            data=boot_data
        )
        
        self.cpu.jump(position=0)
        self.cpu.execute()
        
        print("=" * 50)
        print("Computer started successfully!")
        print("=" * 50)

# ============ CLIENT CODE ============

# Without Facade - Complex!
print("WITHOUT FACADE:")
print("-" * 50)
cpu = CPU()
memory = Memory()
hdd = HardDrive()

cpu.freeze()
boot_data = hdd.read(0, 1024)
memory.load(0, boot_data)
cpu.jump(0)
cpu.execute()

print("\n" * 2)

# With Facade - Simple!
print("WITH FACADE:")
print("-" * 50)
computer = ComputerFacade()
computer.start()  # Just one call!
```

**Output:**
```
WITHOUT FACADE:
--------------------------------------------------
CPU: Freezing processor
HardDrive: Reading 1024 bytes from sector 0
Memory: Loading 'boot_data' at position 0
CPU: Jumping to position 0
CPU: Executing instructions


WITH FACADE:
--------------------------------------------------
==================================================
Starting computer...
==================================================
CPU: Freezing processor
HardDrive: Reading 1024 bytes from sector 0
Memory: Loading 'boot_data' at position 0
CPU: Jumping to position 0
CPU: Executing instructions
==================================================
Computer started successfully!
==================================================
```

---

## Real-World Examples

### Example 1: Home Theater System

```python
# ============ COMPLEX SUBSYSTEM (Many components) ============

class Amplifier:
    def __init__(self):
        self.volume = 0
    
    def on(self):
        print("🔊 Amplifier: Turning on")
    
    def off(self):
        print("🔊 Amplifier: Turning off")
    
    def set_volume(self, level: int):
        self.volume = level
        print(f"🔊 Amplifier: Setting volume to {level}")
    
    def set_surround_sound(self):
        print("🔊 Amplifier: Setting surround sound mode")

class DVDPlayer:
    def __init__(self):
        self.movie = None
    
    def on(self):
        print("📀 DVD Player: Turning on")
    
    def off(self):
        print("📀 DVD Player: Turning off")
    
    def play(self, movie: str):
        self.movie = movie
        print(f"📀 DVD Player: Playing '{movie}'")
    
    def stop(self):
        print(f"📀 DVD Player: Stopping '{self.movie}'")
        self.movie = None
    
    def eject(self):
        print("📀 DVD Player: Ejecting DVD")

class Projector:
    def __init__(self):
        self.input_source = None
    
    def on(self):
        print("📽️  Projector: Turning on")
    
    def off(self):
        print("📽️  Projector: Turning off")
    
    def set_input(self, source: str):
        self.input_source = source
        print(f"📽️  Projector: Setting input to {source}")
    
    def wide_screen_mode(self):
        print("📽️  Projector: Setting wide screen mode")

class Lights:
    def __init__(self):
        self.brightness = 100
    
    def dim(self, level: int):
        self.brightness = level
        print(f"💡 Lights: Dimming to {level}%")
    
    def on(self):
        self.brightness = 100
        print("💡 Lights: Turning on to full brightness")

class Screen:
    def down(self):
        print("📺 Screen: Moving down")
    
    def up(self):
        print("📺 Screen: Moving up")

class PopcornPopper:
    def on(self):
        print("🍿 Popcorn Popper: Turning on")
    
    def off(self):
        print("🍿 Popcorn Popper: Turning off")
    
    def pop(self):
        print("🍿 Popcorn Popper: Popping popcorn")

# ============ FACADE ============

class HomeTheaterFacade:
    """
    Simplifies the complex home theater system.
    
    Without facade: Client needs to manage 6+ components
    With facade: Client just calls watch_movie() or end_movie()
    """
    
    def __init__(self):
        # Initialize all subsystem components
        self.amplifier = Amplifier()
        self.dvd_player = DVDPlayer()
        self.projector = Projector()
        self.lights = Lights()
        self.screen = Screen()
        self.popcorn_popper = PopcornPopper()
    
    def watch_movie(self, movie: str):
        """
        Simplified interface to watch a movie.
        Handles all the complex initialization.
        """
        print("\n" + "=" * 60)
        print("🎬 Get ready to watch a movie...")
        print("=" * 60)
        
        # Complex sequence of operations
        self.popcorn_popper.on()
        self.popcorn_popper.pop()
        
        self.lights.dim(10)
        
        self.screen.down()
        
        self.projector.on()
        self.projector.set_input("DVD")
        self.projector.wide_screen_mode()
        
        self.amplifier.on()
        self.amplifier.set_volume(5)
        self.amplifier.set_surround_sound()
        
        self.dvd_player.on()
        self.dvd_player.play(movie)
        
        print("=" * 60)
        print("🎬 Movie is now playing! Enjoy!")
        print("=" * 60)
    
    def end_movie(self):
        """
        Simplified interface to end movie.
        Handles all cleanup.
        """
        print("\n" + "=" * 60)
        print("🎬 Shutting down movie theater...")
        print("=" * 60)
        
        self.popcorn_popper.off()
        
        self.lights.on()
        
        self.screen.up()
        
        self.dvd_player.stop()
        self.dvd_player.eject()
        self.dvd_player.off()
        
        self.amplifier.off()
        
        self.projector.off()
        
        print("=" * 60)
        print("🎬 Movie theater shut down complete!")
        print("=" * 60)
    
    def listen_to_music(self, album: str):
        """Another simplified high-level operation"""
        print("\n" + "=" * 60)
        print("🎵 Setting up music mode...")
        print("=" * 60)
        
        self.lights.on()
        self.amplifier.on()
        self.amplifier.set_volume(7)
        # In reality, would connect to music player
        print(f"🎵 Playing album: {album}")
        
        print("=" * 60)
        print("🎵 Music is playing!")
        print("=" * 60)

# ============ CLIENT CODE ============

# Without Facade - Client does all the work (complex!)
print("WITHOUT FACADE - Client manages everything:")
print("-" * 60)

# Client has to remember and execute all these steps
popper = PopcornPopper()
lights = Lights()
screen = Screen()
projector = Projector()
amp = Amplifier()
dvd = DVDPlayer()

popper.on()
popper.pop()
lights.dim(10)
screen.down()
projector.on()
projector.set_input("DVD")
amp.on()
amp.set_volume(5)
dvd.on()
dvd.play("The Matrix")
print("... Movie playing ...")

print("\n" * 2)

# With Facade - Much simpler!
print("WITH FACADE - Simple and clean:")
print("-" * 60)

home_theater = HomeTheaterFacade()

# Watch a movie
home_theater.watch_movie("The Matrix")

# End the movie
home_theater.end_movie()

# Listen to music
home_theater.listen_to_music("Pink Floyd - Dark Side of the Moon")
```

---

### Example 2: E-commerce Order Processing

```python
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

# ============ SUBSYSTEM CLASSES ============

@dataclass
class Product:
    id: str
    name: str
    price: float
    stock: int

@dataclass
class Customer:
    id: str
    name: str
    email: str
    address: str

class PaymentStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"

class InventorySystem:
    """Manages product inventory"""
    
    def __init__(self):
        self.products = {
            "P001": Product("P001", "Laptop", 999.99, 10),
            "P002": Product("P002", "Mouse", 29.99, 50),
            "P003": Product("P003", "Keyboard", 79.99, 30),
        }
    
    def check_availability(self, product_id: str, quantity: int) -> bool:
        """Check if product is available"""
        print(f"📦 Inventory: Checking availability for {product_id}")
        
        if product_id not in self.products:
            print(f"❌ Inventory: Product {product_id} not found")
            return False
        
        product = self.products[product_id]
        available = product.stock >= quantity
        
        if available:
            print(f"✅ Inventory: {quantity} units of {product.name} available")
        else:
            print(f"❌ Inventory: Only {product.stock} units available, need {quantity}")
        
        return available
    
    def reserve_products(self, items: list[dict]) -> bool:
        """Reserve products for order"""
        print("📦 Inventory: Reserving products...")
        
        for item in items:
            product_id = item['product_id']
            quantity = item['quantity']
            
            if product_id in self.products:
                product = self.products[product_id]
                product.stock -= quantity
                print(f"✅ Inventory: Reserved {quantity} units of {product.name}")
        
        return True
    
    def release_products(self, items: list[dict]):
        """Release reserved products (if order fails)"""
        print("📦 Inventory: Releasing reserved products...")
        
        for item in items:
            product_id = item['product_id']
            quantity = item['quantity']
            
            if product_id in self.products:
                product = self.products[product_id]
                product.stock += quantity

class PaymentProcessor:
    """Processes payments"""
    
    def authorize_payment(self, customer_id: str, amount: float) -> str:
        """Authorize payment"""
        print(f"💳 Payment: Authorizing ${amount:.2f} for customer {customer_id}")
        
        # Simulate payment authorization
        auth_code = f"AUTH-{datetime.now().timestamp()}"
        print(f"✅ Payment: Authorized with code {auth_code}")
        
        return auth_code
    
    def capture_payment(self, auth_code: str, amount: float) -> bool:
        """Capture payment"""
        print(f"💳 Payment: Capturing ${amount:.2f} with auth {auth_code}")
        
        # Simulate payment capture
        success = True  # In reality, would call payment gateway
        
        if success:
            print(f"✅ Payment: Successfully captured ${amount:.2f}")
        else:
            print(f"❌ Payment: Capture failed")
        
        return success
    
    def refund_payment(self, auth_code: str, amount: float):
        """Refund payment"""
        print(f"💳 Payment: Refunding ${amount:.2f} for auth {auth_code}")

class ShippingService:
    """Manages shipping"""
    
    def calculate_shipping(self, address: str, weight: float) -> float:
        """Calculate shipping cost"""
        print(f"📮 Shipping: Calculating shipping to {address}")
        
        # Simple calculation
        shipping_cost = 5.00 + (weight * 0.5)
        print(f"📮 Shipping: Cost is ${shipping_cost:.2f}")
        
        return shipping_cost
    
    def create_shipment(self, order_id: str, address: str) -> str:
        """Create shipment"""
        print(f"📮 Shipping: Creating shipment for order {order_id}")
        
        tracking_number = f"TRACK-{datetime.now().timestamp()}"
        print(f"✅ Shipping: Created shipment with tracking {tracking_number}")
        
        return tracking_number
    
    def schedule_pickup(self, tracking_number: str):
        """Schedule pickup"""
        print(f"📮 Shipping: Scheduling pickup for {tracking_number}")

class NotificationService:
    """Sends notifications"""
    
    def send_order_confirmation(self, customer_email: str, order_id: str):
        """Send order confirmation email"""
        print(f"📧 Notification: Sending order confirmation to {customer_email}")
        print(f"   Order ID: {order_id}")
    
    def send_shipping_notification(self, customer_email: str, tracking_number: str):
        """Send shipping notification"""
        print(f"📧 Notification: Sending shipping notification to {customer_email}")
        print(f"   Tracking: {tracking_number}")
    
    def send_failure_notification(self, customer_email: str, reason: str):
        """Send failure notification"""
        print(f"📧 Notification: Sending failure notification to {customer_email}")
        print(f"   Reason: {reason}")

class OrderDatabase:
    """Manages order data"""
    
    def __init__(self):
        self.orders = {}
    
    def save_order(self, order_id: str, order_data: dict) -> bool:
        """Save order to database"""
        print(f"💾 Database: Saving order {order_id}")
        
        self.orders[order_id] = order_data
        print(f"✅ Database: Order {order_id} saved")
        
        return True
    
    def update_order_status(self, order_id: str, status: str):
        """Update order status"""
        print(f"💾 Database: Updating order {order_id} status to {status}")
        
        if order_id in self.orders:
            self.orders[order_id]['status'] = status

# ============ FACADE ============

class OrderProcessingFacade:
    """
    Facade that simplifies the complex order processing system.
    
    Without facade: Client needs to coordinate 5+ subsystems
    With facade: Client just calls process_order()
    """
    
    def __init__(self):
        # Initialize all subsystems
        self.inventory = InventorySystem()
        self.payment = PaymentProcessor()
        self.shipping = ShippingService()
        self.notifications = NotificationService()
        self.database = OrderDatabase()
    
    def process_order(self, customer: Customer, items: list[dict]) -> dict:
        """
        Simplified interface to process an order.
        
        Coordinates:
        - Inventory checking and reservation
        - Payment processing
        - Shipping calculation and creation
        - Database operations
        - Customer notifications
        
        Args:
            customer: Customer information
            items: List of items [{product_id, quantity}, ...]
        
        Returns:
            Order result with status and details
        """
        print("\n" + "=" * 70)
        print(f"🛒 Processing order for {customer.name}")
        print("=" * 70)
        
        order_id = f"ORD-{datetime.now().timestamp()}"
        
        try:
            # Step 1: Check inventory availability
            print("\n--- Step 1: Checking Inventory ---")
            for item in items:
                available = self.inventory.check_availability(
                    item['product_id'],
                    item['quantity']
                )
                
                if not available:
                    self.notifications.send_failure_notification(
                        customer.email,
                        "Product unavailable"
                    )
                    return {
                        'success': False,
                        'order_id': order_id,
                        'message': 'Product unavailable'
                    }
            
            # Step 2: Calculate total amount
            print("\n--- Step 2: Calculating Total ---")
            total_amount = 0
            total_weight = 0
            
            for item in items:
                product = self.inventory.products[item['product_id']]
                item_total = product.price * item['quantity']
                total_amount += item_total
                total_weight += item['quantity'] * 2.0  # Assume 2kg per item
                
                print(f"   {product.name} x {item['quantity']} = ${item_total:.2f}")
            
            # Calculate shipping
            shipping_cost = self.shipping.calculate_shipping(
                customer.address,
                total_weight
            )
            total_amount += shipping_cost
            
            print(f"   Shipping: ${shipping_cost:.2f}")
            print(f"   Total: ${total_amount:.2f}")
            
            # Step 3: Process payment
            print("\n--- Step 3: Processing Payment ---")
            auth_code = self.payment.authorize_payment(customer.id, total_amount)
            
            payment_success = self.payment.capture_payment(auth_code, total_amount)
            
            if not payment_success:
                self.notifications.send_failure_notification(
                    customer.email,
                    "Payment failed"
                )
                return {
                    'success': False,
                    'order_id': order_id,
                    'message': 'Payment failed'
                }
            
            # Step 4: Reserve inventory
            print("\n--- Step 4: Reserving Inventory ---")
            self.inventory.reserve_products(items)
            
            # Step 5: Create shipment
            print("\n--- Step 5: Creating Shipment ---")
            tracking_number = self.shipping.create_shipment(order_id, customer.address)
            self.shipping.schedule_pickup(tracking_number)
            
            # Step 6: Save order to database
            print("\n--- Step 6: Saving Order ---")
            order_data = {
                'order_id': order_id,
                'customer': customer,
                'items': items,
                'total': total_amount,
                'tracking_number': tracking_number,
                'status': 'confirmed',
                'created_at': datetime.now()
            }
            
            self.database.save_order(order_id, order_data)
            
            # Step 7: Send notifications
            print("\n--- Step 7: Sending Notifications ---")
            self.notifications.send_order_confirmation(customer.email, order_id)
            self.notifications.send_shipping_notification(customer.email, tracking_number)
            
            print("\n" + "=" * 70)
            print(f"✅ Order {order_id} processed successfully!")
            print("=" * 70)
            
            return {
                'success': True,
                'order_id': order_id,
                'tracking_number': tracking_number,
                'total': total_amount,
                'message': 'Order processed successfully'
            }
            
        except Exception as e:
            print(f"\n❌ Error processing order: {str(e)}")
            
            # Rollback
            print("\n--- Rolling Back Transaction ---")
            self.inventory.release_products(items)
            
            self.notifications.send_failure_notification(
                customer.email,
                f"Order processing failed: {str(e)}"
            )
            
            return {
                'success': False,
                'order_id': order_id,
                'message': f'Order failed: {str(e)}'
            }
    
    def get_order_status(self, order_id: str) -> dict:
        """Get order status - another simplified interface"""
        if order_id in self.database.orders:
            order = self.database.orders[order_id]
            return {
                'order_id': order_id,
                'status': order['status'],
                'tracking': order.get('tracking_number'),
                'total': order['total']
            }
        else:
            return {'error': 'Order not found'}

# ============ CLIENT CODE ============

# Create customer
customer = Customer(
    id="C001",
    name="John Doe",
    email="john@example.com",
    address="123 Main St, City, State 12345"
)

# Create order items
items = [
    {'product_id': 'P001', 'quantity': 1},  # Laptop
    {'product_id': 'P002', 'quantity': 2},  # Mouse
]

# WITHOUT FACADE: Client would need to coordinate all subsystems manually
# (Too complex to show here - would be 50+ lines of code!)

# WITH FACADE: Simple!
print("WITH FACADE:")
print("-" * 70)

order_system = OrderProcessingFacade()
result = order_system.process_order(customer, items)

print("\n" + "=" * 70)
print("ORDER RESULT:")
print("=" * 70)
print(f"Success: {result['success']}")
print(f"Order ID: {result['order_id']}")
print(f"Message: {result['message']}")

if result['success']:
    print(f"Tracking: {result['tracking_number']}")
    print(f"Total: ${result['total']:.2f}")

# Check order status
print("\n" + "=" * 70)
print("CHECKING ORDER STATUS:")
print("=" * 70)
status = order_system.get_order_status(result['order_id'])
print(status)
```

---

### Example 3: Video Conversion System

```python
from enum import Enum
import time

# ============ SUBSYSTEM CLASSES ============

class VideoFormat(Enum):
    MP4 = "mp4"
    AVI = "avi"
    MKV = "mkv"
    MOV = "mov"

class AudioCodec(Enum):
    AAC = "aac"
    MP3 = "mp3"
    FLAC = "flac"

class VideoCodec(Enum):
    H264 = "h264"
    H265 = "h265"
    VP9 = "vp9"

class VideoFile:
    """Represents a video file"""
    
    def __init__(self, filename: str):
        self.filename = filename
        self.format = None
        self.resolution = None
        self.bitrate = None

class CodecFactory:
    """Manages codecs"""
    
    def get_codec(self, format_type: VideoFormat) -> str:
        print(f"🔧 CodecFactory: Getting codec for {format_type.value}")
        
        codec_map = {
            VideoFormat.MP4: "H264/AAC",
            VideoFormat.AVI: "XVID/MP3",
            VideoFormat.MKV: "H265/FLAC",
            VideoFormat.MOV: "H264/AAC"
        }
        
        return codec_map.get(format_type, "Unknown")

class BitrateReader:
    """Reads video bitrate"""
    
    def read(self, video: VideoFile) -> int:
        print(f"📊 BitrateReader: Reading bitrate from {video.filename}")
        
        # Simulate reading
        time.sleep(0.1)
        bitrate = 5000  # kbps
        
        print(f"📊 BitrateReader: Bitrate is {bitrate} kbps")
        return bitrate

class AudioMixer:
    """Mixes audio tracks"""
    
    def fix_audio(self, video: VideoFile):
        print(f"🎵 AudioMixer: Fixing audio for {video.filename}")
        time.sleep(0.1)
        print(f"✅ AudioMixer: Audio fixed")

class VideoSplitter:
    """Splits video into frames"""
    
    def split(self, video: VideoFile) -> list:
        print(f"✂️  VideoSplitter: Splitting {video.filename} into frames")
        time.sleep(0.1)
        
        frames = ["frame1", "frame2", "frame3"]  # Simplified
        print(f"✅ VideoSplitter: Split into {len(frames)} frames")
        
        return frames

class VideoEncoder:
    """Encodes video"""
    
    def encode(self, frames: list, codec: VideoCodec, bitrate: int):
        print(f"🎬 VideoEncoder: Encoding {len(frames)} frames")
        print(f"   Codec: {codec.value}, Bitrate: {bitrate} kbps")
        
        time.sleep(0.2)
        print(f"✅ VideoEncoder: Encoding complete")

class AudioEncoder:
    """Encodes audio"""
    
    def encode(self, video: VideoFile, codec: AudioCodec):
        print(f"🎵 AudioEncoder: Encoding audio")
        print(f"   Codec: {codec.value}")
        
        time.sleep(0.1)
        print(f"✅ AudioEncoder: Audio encoding complete")

class Muxer:
    """Combines video and audio"""
    
    def mux(self, video_data, audio_data, output_format: VideoFormat) -> str:
        print(f"🔗 Muxer: Combining video and audio")
        print(f"   Output format: {output_format.value}")
        
        time.sleep(0.1)
        
        output_filename = f"output.{output_format.value}"
        print(f"✅ Muxer: Created {output_filename}")
        
        return output_filename

class MetadataWriter:
    """Writes metadata to file"""
    
    def write_metadata(self, filename: str, metadata: dict):
        print(f"📝 MetadataWriter: Writing metadata to {filename}")
        print(f"   Metadata: {metadata}")
        time.sleep(0.05)
        print(f"✅ MetadataWriter: Metadata written")

# ============ FACADE ============

class VideoConverterFacade:
    """
    Facade that simplifies video conversion.
    
    Without facade: Client needs to:
    1. Get codec
    2. Read bitrate
    3. Fix audio
    4. Split video
    5. Encode video
    6. Encode audio
    7. Mux video and audio
    8. Write metadata
    
    With facade: Just call convert()
    """
    
    def __init__(self):
        self.codec_factory = CodecFactory()
        self.bitrate_reader = BitrateReader()
        self.audio_mixer = AudioMixer()
        self.video_splitter = VideoSplitter()
        self.video_encoder = VideoEncoder()
        self.audio_encoder = AudioEncoder()
        self.muxer = Muxer()
        self.metadata_writer = MetadataWriter()
    
    def convert(
        self,
        input_file: str,
        output_format: VideoFormat,
        resolution: str = "1920x1080",
        quality: str = "high"
    ) -> str:
        """
        Simplified interface to convert video.
        
        Args:
            input_file: Input video file path
            output_format: Desired output format
            resolution: Output resolution (default: 1920x1080)
            quality: Quality setting (low/medium/high)
        
        Returns:
            Output filename
        """
        print("\n" + "=" * 70)
        print(f"🎥 Converting video: {input_file}")
        print(f"   Target format: {output_format.value}")
        print(f"   Resolution: {resolution}")
        print(f"   Quality: {quality}")
        print("=" * 70)
        
        # Create video object
        video = VideoFile(input_file)
        
        # Step 1: Get appropriate codec
        print("\n--- Step 1: Getting Codec ---")
        codec_info = self.codec_factory.get_codec(output_format)
        
        # Step 2: Read current bitrate
        print("\n--- Step 2: Reading Bitrate ---")
        current_bitrate = self.bitrate_reader.read(video)
        
        # Adjust bitrate based on quality
        quality_multipliers = {'low': 0.5, 'medium': 1.0, 'high': 1.5}
        target_bitrate = int(current_bitrate * quality_multipliers[quality])
        
        # Step 3: Fix audio issues
        print("\n--- Step 3: Fixing Audio ---")
        self.audio_mixer.fix_audio(video)
        
        # Step 4: Split video into frames
        print("\n--- Step 4: Splitting Video ---")
        frames = self.video_splitter.split(video)
        
        # Step 5: Encode video
        print("\n--- Step 5: Encoding Video ---")
        video_codec = VideoCodec.H264  # Based on output format
        self.video_encoder.encode(frames, video_codec, target_bitrate)
        
        # Step 6: Encode audio
        print("\n--- Step 6: Encoding Audio ---")
        audio_codec = AudioCodec.AAC
        self.audio_encoder.encode(video, audio_codec)
        
        # Step 7: Mux video and audio
        print("\n--- Step 7: Muxing ---")
        output_filename = self.muxer.mux(
            video_data="encoded_video",
            audio_data="encoded_audio",
            output_format=output_format
        )
        
        # Step 8: Write metadata
        print("\n--- Step 8: Writing Metadata ---")
        metadata = {
            'source': input_file,
            'format': output_format.value,
            'resolution': resolution,
            'bitrate': target_bitrate,
            'converted_at': time.time()
        }
        self.metadata_writer.write_metadata(output_filename, metadata)
        
        print("\n" + "=" * 70)
        print(f"✅ Conversion complete: {output_filename}")
        print("=" * 70)
        
        return output_filename
    
    def quick_convert(self, input_file: str, output_format: VideoFormat) -> str:
        """Quick conversion with default settings"""
        return self.convert(input_file, output_format, quality='medium')
    
    def high_quality_convert(self, input_file: str, output_format: VideoFormat) -> str:
        """High quality conversion"""
        return self.convert(input_file, output_format, resolution='3840x2160', quality='high')

# ============ CLIENT CODE ============

print("VIDEO CONVERSION SYSTEM")
print("=" * 70)

converter = VideoConverterFacade()

# Example 1: Standard conversion
print("\n### Example 1: Standard Conversion ###")
output1 = converter.convert(
    input_file="movie.avi",
    output_format=VideoFormat.MP4,
    resolution="1920x1080",
    quality="high"
)

# Example 2: Quick conversion with defaults
print("\n### Example 2: Quick Conversion ###")
output2 = converter.quick_convert("video.mkv", VideoFormat.MP4)

# Example 3: High quality 4K conversion
print("\n### Example 3: 4K Conversion ###")
output3 = converter.high_quality_convert("raw_footage.mov", VideoFormat.MKV)
```

---

## Common Pitfalls

### ❌ Pitfall 1: Facade Becomes God Object

```python
# BAD - Facade does everything
class MegaFacade:
    def do_everything(self):
        # 500+ lines of code
        # Handles user management
        # Handles billing
        # Handles notifications
        # Handles analytics
        # ... everything!
        pass

# GOOD - Multiple focused facades
class UserManagementFacade:
    def register_user(self): pass
    def login_user(self): pass

class BillingFacade:
    def process_payment(self): pass
    def generate_invoice(self): pass

class NotificationFacade:
    def send_email(self): pass
    def send_sms(self): pass
```

---

### ❌ Pitfall 2: Facade Duplicates Subsystem Interface

```python
# BAD - Just wrapping methods one-to-one
class SubSystem:
    pass

class BadFacade:
    def __init__(self):
        self.system = SubSystem()
    
    def method1(self): return self.system.method1()
    def method2(self): return self.system.method2()
    def method3(self): return self.system.method3()
    # ... just delegation, no simplification!

# GOOD - Provides higher-level operations
class GoodFacade:
    def __init__(self):
        self.system = SubSystem()
    
    def high_level_operation(self):
        # Combines multiple subsystem calls
        self.system.method1()
        self.system.method2()
        self.system.method3()
        # Returns simplified result
```

---

### ❌ Pitfall 3: Hiding Important Errors

```python
# BAD - Swallows exceptions

class SubsystemException(Exception):
    pass

class FacadeException(Exception):
    pass

class BadFacade:
    def operation(self):
        try:
            self.subsystem.complex_operation()
        except Exception:
            pass  # Silently fails!

# GOOD - Handles or propagates appropriately
class GoodFacade:
    def operation(self):
        try:
            self.subsystem.complex_operation()
        except SubsystemException as e:
            # Convert to facade-level exception
            raise FacadeException(f"Operation failed: {e}")
```

---

### ❌ Pitfall 4: Too Many Parameters

```python
# BAD - Facade method has too many parameters
ProcessConfig = {}

class BadFacade:
    def process(self, a, b, c, d, e, f, g, h):
        # Too complex!
        pass

# GOOD - Use configuration objects
class GoodFacade:
    def process(self, config: ProcessConfig):
        # Simpler interface
        pass
```

---

## Best Practices

### ✅ 1. Keep Facade Focused

```python
# Each facade should handle one domain
class OrderFacade:
    """Handles order processing only"""
    pass

class UserFacade:
    """Handles user management only"""
    pass

# Not a single facade for everything
```

---

### ✅ 2. Provide Multiple Levels of Abstraction

```python
class VideoConverterFacade:
    # High-level (very simple)
    def quick_convert(self, file, format):
        return self.convert(file, format, quality='medium')
    
    # Medium-level (some control)
    def convert(self, file, format, quality='medium'):
        return self.advanced_convert(file, format, quality, resolution='1080p')
    
    # Low-level (full control)
    def advanced_convert(self, file, format, quality, resolution, bitrate=None):
        # Full control for advanced users
        pass
```

---

### ✅ 3. Document What's Being Simplified

```python
class HomeTheaterFacade:
    """
    Simplifies home theater operation.
    
    Manages:
    - Amplifier (volume, surround sound)
    - DVD Player (play, stop, eject)
    - Projector (power, input, mode)
    - Lights (dimming)
    - Screen (up/down)
    - Popcorn Popper
    
    Without this facade, clients would need to:
    1. Know the startup sequence
    2. Manage 6+ components
    3. Handle error states
    4. Coordinate shutdown
    """
    pass
```

---

### ✅ 4. Don't Prevent Direct Access

```python
class SubsystemA:
    pass

class SubsystemB:
    pass

class SystemFacade:
    def __init__(self):
        # Make subsystems accessible if needed
        self.subsystem_a = SubsystemA()
        self.subsystem_b = SubsystemB()
    
    def simplified_operation(self):
        # High-level operation
        pass

# Client can still access subsystems directly if needed
facade = SystemFacade()
facade.simplified_operation()  # Easy way

# Or access subsystem directly for special cases
facade.subsystem_a.specialized_method()  # Advanced way
```

---

### ✅ 5. Use Dependency Injection

```python
class InventorySystem:
    pass

class PaymentProcessor:
    pass

class ShippingService:
    pass

class MockInventory(InventorySystem):
    pass

class MockPayment(PaymentProcessor):
    pass

class MockShipping(ShippingService):
    pass

class OrderFacade:
    def __init__(
        self,
        inventory: InventorySystem = None,
        payment: PaymentProcessor = None,
        shipping: ShippingService = None
    ):
        # Allow injection for testing
        self.inventory = inventory or InventorySystem()
        self.payment = payment or PaymentProcessor()
        self.shipping = shipping or ShippingService()

# Easy to test with mocks
facade = OrderFacade(
    inventory=MockInventory(),
    payment=MockPayment(),
    shipping=MockShipping()
)
```

---

## Summary

| Aspect               | Details                                                      |
|----------------------|--------------------------------------------------------------|
| **Purpose**          | Provide simplified interface to complex subsystem            |
| **Use When**         | Complex subsystems, layered architecture, legacy integration |
| **Avoid When**       | Simple subsystem, need fine control, over-simplification     |
| **Key Benefit**      | Reduces coupling, makes subsystem easier to use              |
| **Common Use Cases** | Libraries, frameworks, legacy systems, complex APIs          |

---

## Facade vs Other Patterns

| Pattern      | Purpose            | Relationship                               |
|--------------|--------------------|--------------------------------------------|
| **Facade**   | Simplify subsystem | One-to-many (facade to subsystems)         |
| **Adapter**  | Convert interface  | One-to-one (adapter to adaptee)            |
| **Mediator** | Reduce coupling    | Many-to-many (components through mediator) |
| **Proxy**    | Control access     | One-to-one (proxy to real object)          |

---

## When to Use Which Pattern?

- **Use Facade** when you need to simplify a complex subsystem
- **Use Adapter** when you need to make incompatible interfaces work together
- **Use Proxy** when you need to control access or add functionality to an object
- **Use Decorator** when you need to add responsibilities to objects dynamically
