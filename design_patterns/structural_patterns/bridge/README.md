# Bridge Pattern - Complete Guide

## 📋 Table of Contents
- [What is Bridge Pattern?](#what-is-bridge-pattern)
  - [Key Characteristics](#key-characteristics)
  - [The Problem Bridge Solves](#the-problem-bridge-solves)
  - [Real-World Analogy](#real-world-analogy)
  - [Visual Representation](#visual-representation)
- [Bridge vs Similar Patterns](#bridge-vs-similar-patterns)
- [When to Use](#when-to-use)
  - [✅ Perfect Use Cases](#-perfect-use-cases)
- [When NOT to Use](#when-not-to-use)
  - [❌ Avoid Bridge When](#when-not-to-use)
- [Basic Implementation](#basic-implementation)
- [Real-World Examples](#real-world-examples)
  - [Example 1: Remote Control and Devices](#example-1-remote-control-and-devices)
  - [Example 2: Messaging System (Message + Platform)](#example-2-messaging-system-message--platform)
  - [Example 3: Drawing Shapes with Renderers](#example-3-drawing-shapes-with-renderers)
- [Common Pitfalls](#common-pitfalls)
  - [❌ Pitfall 1: Confusing Bridge with Adapter](#-pitfall-1-confusing-bridge-with-adapter)
  - [❌ Pitfall 2: Not Using Composition](#-pitfall-2-not-using-composition)
  - [❌ Pitfall 3: Implementation Depends on Abstraction](#-pitfall-3-implementation-depends-on-abstraction)
  - [❌ Pitfall 4: Creating Bridge When Not Needed](#-pitfall-4-creating-bridge-when-not-needed)
- [Best Practices](#best-practices)
  - [✅ 1. Identify Two Orthogonal Dimensions](#-1-identify-two-orthogonal-dimensions)
  - [✅ 2. Keep Implementation Interface Minimal](#-2-keep-implementation-interface-minimal)
  - [✅ 3. Document the Two Hierarchies](#-3-document-the-two-hierarchies)
  - [✅ 4. Allow Runtime Switching](#-4-allow-runtime-switching)
  - [✅ 5. Use Dependency Injection](#-5-use-dependency-injection)
- [Summary](#summary)
- [Bridge vs Other Patterns](#bridge-vs-other-patterns)
- [When to Use Bridge](#when-to-use-bridge)
- [Key Takeaways](#key-takeaways)
---

## What is Bridge Pattern?

**Bridge Pattern** separates an abstraction from its implementation so that the two can vary independently. It decouples an abstraction from its implementation, allowing both to be developed and extended separately.

### Key Characteristics:
- ✅ Separates abstraction from implementation
- ✅ Both can vary independently
- ✅ Prefers composition to inheritance
- ✅ Avoids class explosion (combinatorial growth)
- ✅ Increases flexibility

### The Problem Bridge Solves

**Without Bridge - Class Explosion:**
```
Shape hierarchy:
- Circle
  - RedCircle
  - BlueCircle
  - GreenCircle
- Square
  - RedSquare
  - BlueSquare
  - GreenSquare
- Triangle
  - RedTriangle
  - BlueTriangle
  - GreenTriangle

3 shapes × 3 colors = 9 classes!
Add 1 shape or 1 color = 3 more classes each time!
```

**With Bridge - Composition:**
```
Shape (Abstraction)     Color (Implementation)
- Circle                - Red
- Square                - Blue
- Triangle              - Green

3 shapes + 3 colors = 6 classes total!
Add 1 shape = +1 class
Add 1 color = +1 class
```

### Real-World Analogy:
Think of a **remote control and TV**:
- **Abstraction:** Remote control (basic remote, advanced remote, universal remote)
- **Implementation:** TV (Sony TV, Samsung TV, LG TV)

You can use any remote with any TV. The remote doesn't need to know TV internals. You can add new remote types or new TV brands independently.

### Visual Representation:
```
Abstraction → Implementation
   ↓              ↓
Refined         Concrete
Abstraction     Implementation

Client → Abstraction → uses → Implementation
```

---

## Bridge vs Similar Patterns

| Pattern      | Purpose                                  | Structure                                 |
|--------------|------------------------------------------|-------------------------------------------|
| **Bridge**   | Separate abstraction from implementation | Two hierarchies connected by composition  |
| **Adapter**  | Make incompatible interfaces work        | Wraps existing interface                  |
| **Strategy** | Vary algorithm                           | One hierarchy, interchangeable algorithms |
| **State**    | Vary behavior based on state             | One hierarchy, state-dependent behavior   |

**Key Difference:** Bridge creates **two separate hierarchies** (abstraction and implementation) that can evolve independently.

---

## When to Use

### ✅ Perfect Use Cases:

#### 1. **Avoid Permanent Binding**
- Don't want to bind abstraction to implementation at compile-time
- Need to select or switch implementation at runtime
- Want flexibility in choosing implementation

#### 2. **Both Abstraction and Implementation Should Be Extensible**
- Both need to vary independently
- Adding new abstractions shouldn't affect implementations
- Adding new implementations shouldn't affect abstractions

#### 3. **Avoid Class Explosion**
- Multiple dimensions of variation
- Combinatorial growth of classes
- N abstractions × M implementations = N+M classes (not N×M)

#### 4. **Share Implementation Among Multiple Objects**
- Multiple abstractions can share same implementation
- Implementation can be swapped without affecting abstraction
- Reference counting or pooling needed

#### 5. **Platform Independence**
- Write once, run on multiple platforms
- Abstract away platform-specific code
- Example: GUI frameworks (abstract widgets + platform rendering)

---

## When NOT to Use

### ❌ Avoid Bridge When:

1. **Only One Implementation**
   - No variation in implementation
   - No need for abstraction-implementation separation
   - Adds unnecessary complexity

2. **Tightly Coupled System**
   - Abstraction must know implementation details
   - Can't separate concerns
   - Tight coupling is acceptable/necessary

3. **Simple Inheritance Works**
   - No combinatorial explosion
   - Single dimension of variation
   - Inheritance hierarchy is manageable

4. **Over-Engineering**
   - YAGNI (You Aren't Gonna Need It)
   - Premature abstraction
   - Makes simple things complex

---

## Basic Implementation

### Classic Bridge Structure

```python
from abc import ABC, abstractmethod

# ============ IMPLEMENTATION HIERARCHY ============

class Implementation(ABC):
    """
    Implementation interface.
    Defines operations that concrete implementations must provide.
    TV Example
    """
    
    @abstractmethod
    def operation_implementation(self) -> str:
        pass

class ConcreteImplementationA(Implementation):
    """Concrete implementation A"""
    
    def operation_implementation(self) -> str:
        return "ConcreteImplementationA: Here's the result in A"

class ConcreteImplementationB(Implementation):
    """Concrete implementation B"""
    
    def operation_implementation(self) -> str:
        return "ConcreteImplementationB: Here's the result in B"

# ============ ABSTRACTION HIERARCHY ============

class Abstraction:
    """
    Abstraction defines the interface for the "control" part.
    It maintains a reference to an Implementation object.
    # Remote Example
    """
    
    def __init__(self, implementation: Implementation):
        self.implementation = implementation
    
    def operation(self) -> str:
        """
        Delegates work to the implementation object.
        """
        return f"Abstraction: Base operation with:\n{self.implementation.operation_implementation()}"

class RefinedAbstraction(Abstraction):
    """
    Extended Abstraction.
    Provides variants of the control logic.
    """
    
    def operation(self) -> str:
        """
        Can override or extend the operation.
        """
        return f"RefinedAbstraction: Extended operation with:\n{self.implementation.operation_implementation()}"

# ============ CLIENT CODE ============

def client_code(abstraction: Abstraction):
    """
    Client works with abstraction.
    Doesn't care about the concrete implementation.
    """
    print(abstraction.operation())

# Test with different combinations
print("="*60)
print("Client: Testing with ImplementationA")
print("="*60)
implementation_a = ConcreteImplementationA()
abstraction = Abstraction(implementation_a)
client_code(abstraction)

print("\n" + "="*60)
print("Client: Testing with ImplementationB")
print("="*60)
implementation_b = ConcreteImplementationB()
abstraction = RefinedAbstraction(implementation_b)
client_code(abstraction)
```

**Output:**
```
============================================================
Client: Testing with ImplementationA
============================================================
Abstraction: Base operation with:
ConcreteImplementationA: Here's the result in A

============================================================
Client: Testing with ImplementationB
============================================================
RefinedAbstraction: Extended operation with:
ConcreteImplementationB: Here's the result in B
```

---

## Real-World Examples

### Example 1: Remote Control and Devices

```python
from abc import ABC, abstractmethod

# ============ IMPLEMENTATION (Devices) ============

class Device(ABC):
    """Implementation interface for devices"""
    
    @abstractmethod
    def is_enabled(self) -> bool:
        pass
    
    @abstractmethod
    def enable(self):
        pass
    
    @abstractmethod
    def disable(self):
        pass
    
    @abstractmethod
    def get_volume(self) -> int:
        pass
    
    @abstractmethod
    def set_volume(self, percent: int):
        pass
    
    @abstractmethod
    def get_channel(self) -> int:
        pass
    
    @abstractmethod
    def set_channel(self, channel: int):
        pass

class TV(Device):
    """Concrete implementation - TV"""
    
    def __init__(self):
        self._on = False
        self._volume = 30
        self._channel = 1
    
    def is_enabled(self) -> bool:
        return self._on
    
    def enable(self):
        self._on = True
        print("📺 TV: Turning ON")
    
    def disable(self):
        self._on = False
        print("📺 TV: Turning OFF")
    
    def get_volume(self) -> int:
        return self._volume
    
    def set_volume(self, percent: int):
        self._volume = max(0, min(100, percent))
        print(f"📺 TV: Setting volume to {self._volume}%")
    
    def get_channel(self) -> int:
        return self._channel
    
    def set_channel(self, channel: int):
        self._channel = channel
        print(f"📺 TV: Switching to channel {self._channel}")

class Radio(Device):
    """Concrete implementation - Radio"""
    
    def __init__(self):
        self._on = False
        self._volume = 50
        self._channel = 101  # Radio frequency
    
    def is_enabled(self) -> bool:
        return self._on
    
    def enable(self):
        self._on = True
        print("📻 Radio: Turning ON")
    
    def disable(self):
        self._on = False
        print("📻 Radio: Turning OFF")
    
    def get_volume(self) -> int:
        return self._volume
    
    def set_volume(self, percent: int):
        self._volume = max(0, min(100, percent))
        print(f"📻 Radio: Setting volume to {self._volume}%")
    
    def get_channel(self) -> int:
        return self._channel
    
    def set_channel(self, channel: int):
        self._channel = channel
        print(f"📻 Radio: Tuning to {self._channel} FM")

class SmartTV(Device):
    """Concrete implementation - Smart TV with streaming"""
    
    def __init__(self):
        self._on = False
        self._volume = 40
        self._channel = 1
        self._streaming_service = "Netflix"
    
    def is_enabled(self) -> bool:
        return self._on
    
    def enable(self):
        self._on = True
        print("📱 SmartTV: Turning ON with smart features")
    
    def disable(self):
        self._on = False
        print("📱 SmartTV: Turning OFF")
    
    def get_volume(self) -> int:
        return self._volume
    
    def set_volume(self, percent: int):
        self._volume = max(0, min(100, percent))
        print(f"📱 SmartTV: Setting volume to {self._volume}%")
    
    def get_channel(self) -> int:
        return self._channel
    
    def set_channel(self, channel: int):
        self._channel = channel
        print(f"📱 SmartTV: Switching to channel {self._channel}")
    
    def launch_app(self, app_name: str):
        """Smart TV specific feature"""
        self._streaming_service = app_name
        print(f"📱 SmartTV: Launching {app_name}")

# ============ ABSTRACTION (Remote Controls) ============

class RemoteControl:
    """
    Abstraction - Basic Remote Control.
    Works with any Device through the Device interface.
    """
    
    def __init__(self, device: Device):
        self.device = device
    
    def toggle_power(self):
        """Toggle device power"""
        if self.device.is_enabled():
            print("🎮 Remote: Turning device off")
            self.device.disable()
        else:
            print("🎮 Remote: Turning device on")
            self.device.enable()
    
    def volume_down(self):
        """Decrease volume"""
        print("🎮 Remote: Volume down")
        current = self.device.get_volume()
        self.device.set_volume(current - 10)
    
    def volume_up(self):
        """Increase volume"""
        print("🎮 Remote: Volume up")
        current = self.device.get_volume()
        self.device.set_volume(current + 10)
    
    def channel_down(self):
        """Previous channel"""
        print("🎮 Remote: Channel down")
        current = self.device.get_channel()
        self.device.set_channel(current - 1)
    
    def channel_up(self):
        """Next channel"""
        print("🎮 Remote: Channel up")
        current = self.device.get_channel()
        self.device.set_channel(current + 1)

class AdvancedRemoteControl(RemoteControl):
    """
    Refined Abstraction - Advanced Remote with more features.
    """
    
    def mute(self):
        """Mute the device"""
        print("🎮 Advanced Remote: Muting")
        self.device.set_volume(0)
    
    def set_channel_direct(self, channel: int):
        """Jump to specific channel"""
        print(f"🎮 Advanced Remote: Jumping to channel {channel}")
        self.device.set_channel(channel)

class VoiceRemoteControl(RemoteControl):
    """
    Refined Abstraction - Voice-controlled remote.
    """
    
    def voice_command(self, command: str):
        """Process voice command"""
        print(f"🎮 Voice Remote: Processing command '{command}'")
        
        command = command.lower()
        
        if "turn on" in command or "power on" in command:
            self.device.enable()
        elif "turn off" in command or "power off" in command:
            self.device.disable()
        elif "volume up" in command:
            self.volume_up()
        elif "volume down" in command:
            self.volume_down()
        elif "channel" in command:
            # Extract channel number
            words = command.split()
            for i, word in enumerate(words):
                if word == "channel" and i + 1 < len(words):
                    try:
                        channel = int(words[i + 1])
                        self.device.set_channel(channel)
                    except ValueError:
                        print("❌ Could not understand channel number")
        else:
            print("❌ Command not recognized")

# ============ USAGE ============

print("="*70)
print("BRIDGE PATTERN - REMOTE CONTROLS AND DEVICES")
print("="*70)

# Example 1: Basic remote with TV
print("\n### Example 1: Basic Remote with TV ###")
tv = TV()
basic_remote = RemoteControl(tv)

basic_remote.toggle_power()
basic_remote.volume_up()
basic_remote.volume_up()
basic_remote.channel_up()
basic_remote.toggle_power()

# Example 2: Advanced remote with Radio
print("\n### Example 2: Advanced Remote with Radio ###")
radio = Radio()
advanced_remote = AdvancedRemoteControl(radio)

advanced_remote.toggle_power()
advanced_remote.volume_up()
advanced_remote.set_channel_direct(105)  # FM 105
advanced_remote.mute()
advanced_remote.toggle_power()

# Example 3: Voice remote with Smart TV
print("\n### Example 3: Voice Remote with Smart TV ###")
smart_tv = SmartTV()
voice_remote = VoiceRemoteControl(smart_tv)

voice_remote.voice_command("turn on")
voice_remote.voice_command("volume up")
voice_remote.voice_command("channel 7")
voice_remote.voice_command("turn off")

# Example 4: Same remote with different devices
print("\n### Example 4: Switching Devices with Same Remote ###")
universal_remote = AdvancedRemoteControl(tv)
print("Using universal remote with TV:")
universal_remote.toggle_power()
universal_remote.set_channel_direct(5)

# Switch to radio without changing remote code
universal_remote.device = radio
print("\nNow using same remote with Radio:")
universal_remote.toggle_power()
universal_remote.set_channel_direct(98)

print("\n" + "="*70)
print("KEY POINT: Same remote works with any device!")
print("Can add new remotes OR new devices independently!")
print("="*70)
```

---

### Example 2: Messaging System (Message + Platform)

```python
from abc import ABC, abstractmethod
from typing import List
from datetime import datetime

# ============ IMPLEMENTATION (Platforms) ============

class MessagingPlatform(ABC):
    """Implementation interface for messaging platforms"""
    
    @abstractmethod
    def send_text(self, recipient: str, text: str):
        pass
    
    @abstractmethod
    def send_image(self, recipient: str, image_path: str):
        pass
    
    @abstractmethod
    def send_file(self, recipient: str, file_path: str):
        pass

class EmailPlatform(MessagingPlatform):
    """Concrete implementation - Email"""
    
    def __init__(self, smtp_server: str):
        self.smtp_server = smtp_server
    
    def send_text(self, recipient: str, text: str):
        print(f"📧 Email: Sending to {recipient}")
        print(f"   Via SMTP: {self.smtp_server}")
        print(f"   Subject: Message")
        print(f"   Body: {text}")
    
    def send_image(self, recipient: str, image_path: str):
        print(f"📧 Email: Sending image to {recipient}")
        print(f"   Attachment: {image_path}")
    
    def send_file(self, recipient: str, file_path: str):
        print(f"📧 Email: Sending file to {recipient}")
        print(f"   Attachment: {file_path}")

class SMSPlatform(MessagingPlatform):
    """Concrete implementation - SMS"""
    
    def __init__(self, provider: str):
        self.provider = provider
    
    def send_text(self, recipient: str, text: str):
        # SMS has length limit
        if len(text) > 160:
            print(f"⚠️  SMS: Text too long, truncating to 160 chars")
            text = text[:160]
        
        print(f"📱 SMS: Sending to {recipient}")
        print(f"   Provider: {self.provider}")
        print(f"   Text: {text}")
    
    def send_image(self, recipient: str, image_path: str):
        print(f"📱 SMS/MMS: Sending image to {recipient}")
        print(f"   Image: {image_path}")
    
    def send_file(self, recipient: str, file_path: str):
        print(f"❌ SMS: Cannot send files via SMS")
        print(f"   Sending download link instead")

class SlackPlatform(MessagingPlatform):
    """Concrete implementation - Slack"""
    
    def __init__(self, workspace: str):
        self.workspace = workspace
    
    def send_text(self, recipient: str, text: str):
        print(f"💬 Slack: Sending to #{recipient}")
        print(f"   Workspace: {self.workspace}")
        print(f"   Message: {text}")
    
    def send_image(self, recipient: str, image_path: str):
        print(f"💬 Slack: Uploading image to #{recipient}")
        print(f"   Image: {image_path}")
    
    def send_file(self, recipient: str, file_path: str):
        print(f"💬 Slack: Uploading file to #{recipient}")
        print(f"   File: {file_path}")

class WhatsAppPlatform(MessagingPlatform):
    """Concrete implementation - WhatsApp"""
    
    def send_text(self, recipient: str, text: str):
        print(f"💚 WhatsApp: Sending to {recipient}")
        print(f"   Message: {text}")
        print(f"   ✓✓ Delivered")
    
    def send_image(self, recipient: str, image_path: str):
        print(f"💚 WhatsApp: Sending image to {recipient}")
        print(f"   Image: {image_path}")
        print(f"   ✓✓ Delivered")
    
    def send_file(self, recipient: str, file_path: str):
        print(f"💚 WhatsApp: Sending file to {recipient}")
        print(f"   File: {file_path}")
        print(f"   ✓✓ Delivered")

# ============ ABSTRACTION (Message Types) ============

class Message:
    """
    Abstraction - Base Message class.
    Works with any MessagingPlatform through the interface.
    """
    
    def __init__(self, platform: MessagingPlatform):
        self.platform = platform
        self.timestamp = datetime.now()
    
    def send(self, recipient: str):
        """To be implemented by subclasses"""
        raise NotImplementedError

class TextMessage(Message):
    """Refined Abstraction - Text Message"""
    
    def __init__(self, platform: MessagingPlatform, text: str):
        super().__init__(platform)
        self.text = text
    
    def send(self, recipient: str):
        print(f"\n📝 TextMessage: Preparing to send")
        self.platform.send_text(recipient, self.text)

class ImageMessage(Message):
    """Refined Abstraction - Image Message"""
    
    def __init__(self, platform: MessagingPlatform, image_path: str, caption: str = ""):
        super().__init__(platform)
        self.image_path = image_path
        self.caption = caption
    
    def send(self, recipient: str):
        print(f"\n🖼️  ImageMessage: Preparing to send")
        if self.caption:
            self.platform.send_text(recipient, self.caption)
        self.platform.send_image(recipient, self.image_path)

class FileMessage(Message):
    """Refined Abstraction - File Message"""
    
    def __init__(self, platform: MessagingPlatform, file_path: str, description: str = ""):
        super().__init__(platform)
        self.file_path = file_path
        self.description = description
    
    def send(self, recipient: str):
        print(f"\n📎 FileMessage: Preparing to send")
        if self.description:
            self.platform.send_text(recipient, self.description)
        self.platform.send_file(recipient, self.file_path)

class BulkMessage(Message):
    """Refined Abstraction - Bulk Message (send to multiple recipients)"""
    
    def __init__(self, platform: MessagingPlatform, text: str):
        super().__init__(platform)
        self.text = text
    
    def send_bulk(self, recipients: List[str]):
        print(f"\n📢 BulkMessage: Sending to {len(recipients)} recipients")
        for recipient in recipients:
            self.platform.send_text(recipient, self.text)
            print(f"   ✓ Sent to {recipient}")

# ============ USAGE ============

print("="*70)
print("BRIDGE PATTERN - MESSAGING SYSTEM")
print("="*70)

# Example 1: Text message via different platforms
print("\n### Example 1: Same Text Message via Different Platforms ###")

text_content = "Hello! This is a test message."

# Send via Email
email = EmailPlatform("smtp.gmail.com")
text_email = TextMessage(email, text_content)
text_email.send("john@example.com")

# Send via SMS
sms = SMSPlatform("Twilio")
text_sms = TextMessage(sms, text_content)
text_sms.send("+1234567890")

# Send via Slack
slack = SlackPlatform("MyCompany")
text_slack = TextMessage(slack, text_content)
text_slack.send("general")

# Example 2: Image message
print("\n### Example 2: Image Message ###")

whatsapp = WhatsAppPlatform()
image_msg = ImageMessage(
    whatsapp,
    "vacation_photo.jpg",
    "Check out this amazing sunset! 🌅"
)
image_msg.send("+9876543210")

# Example 3: File message via different platforms
print("\n### Example 3: File Message via Different Platforms ###")

# Via Email (works great)
file_email = FileMessage(
    email,
    "report.pdf",
    "Please find the quarterly report attached."
)
file_email.send("boss@company.com")

# Via SMS (fallback to link)
file_sms = FileMessage(
    sms,
    "report.pdf",
    "Sending you the report"
)
file_sms.send("+1234567890")

# Example 4: Bulk message
print("\n### Example 4: Bulk Message ###")

bulk_email = BulkMessage(
    email,
    "Reminder: Team meeting tomorrow at 10 AM"
)
bulk_email.send_bulk([
    "alice@company.com",
    "bob@company.com",
    "charlie@company.com"
])

# Example 5: Switch platform at runtime
print("\n### Example 5: Switch Platform at Runtime ###")

# Start with email
message = TextMessage(email, "Important notification")
print("Sending via Email:")
message.send("user@example.com")

# Switch to Slack
message.platform = slack
print("\nSwitching to Slack:")
message.send("announcements")

print("\n" + "="*70)
print("KEY BENEFITS:")
print("1. Can add new message types without changing platforms")
print("2. Can add new platforms without changing message types")
print("3. Can mix and match any message type with any platform")
print("="*70)
```

---

### Example 3: Drawing Shapes with Renderers

```python
from abc import ABC, abstractmethod
from typing import Tuple

# ============ IMPLEMENTATION (Renderers) ============

class Renderer(ABC):
    """Implementation interface for rendering"""
    
    @abstractmethod
    def render_circle(self, x: int, y: int, radius: int):
        pass
    
    @abstractmethod
    def render_square(self, x: int, y: int, size: int):
        pass
    
    @abstractmethod
    def render_triangle(self, x1: int, y1: int, x2: int, y2: int, x3: int, y3: int):
        pass

class VectorRenderer(Renderer):
    """Concrete implementation - Vector rendering (SVG)"""
    
    def render_circle(self, x: int, y: int, radius: int):
        print(f"🎨 VectorRenderer: Drawing circle as SVG")
        print(f"   <circle cx='{x}' cy='{y}' r='{radius}' />")
    
    def render_square(self, x: int, y: int, size: int):
        print(f"🎨 VectorRenderer: Drawing square as SVG")
        print(f"   <rect x='{x}' y='{y}' width='{size}' height='{size}' />")
    
    def render_triangle(self, x1: int, y1: int, x2: int, y2: int, x3: int, y3: int):
        print(f"🎨 VectorRenderer: Drawing triangle as SVG")
        print(f"   <polygon points='{x1},{y1} {x2},{y2} {x3},{y3}' />")

class RasterRenderer(Renderer):
    """Concrete implementation - Raster rendering (pixel-based)"""
    
    def render_circle(self, x: int, y: int, radius: int):
        print(f"🖼️  RasterRenderer: Drawing circle as pixels")
        print(f"   Drawing {radius * 2}x{radius * 2} pixels at ({x}, {y})")
        print(f"   Using Bresenham's circle algorithm")
    
    def render_square(self, x: int, y: int, size: int):
        print(f"🖼️  RasterRenderer: Drawing square as pixels")
        print(f"   Filling {size}x{size} pixels at ({x}, {y})")
    
    def render_triangle(self, x1: int, y1: int, x2: int, y2: int, x3: int, y3: int):
        print(f"🖼️  RasterRenderer: Drawing triangle as pixels")
        print(f"   Scan converting triangle with vertices:")
        print(f"   ({x1},{y1}), ({x2},{y2}), ({x3},{y3})")

class OpenGLRenderer(Renderer):
    """Concrete implementation - OpenGL rendering (3D graphics)"""
    
    def render_circle(self, x: int, y: int, radius: int):
        print(f"🎮 OpenGLRenderer: Drawing circle with OpenGL")
        print(f"   glBegin(GL_TRIANGLE_FAN)")
        print(f"   Center: ({x}, {y}), Radius: {radius}")
        print(f"   Using 32 segments for smooth circle")
    
    def render_square(self, x: int, y: int, size: int):
        print(f"🎮 OpenGLRenderer: Drawing square with OpenGL")
        print(f"   glBegin(GL_QUADS)")
        print(f"   Vertices: ({x},{y}), ({x+size},{y}), ({x+size},{y+size}), ({x},{y+size})")
    
    def render_triangle(self, x1: int, y1: int, x2: int, y2: int, x3: int, y3: int):
        print(f"🎮 OpenGLRenderer: Drawing triangle with OpenGL")
        print(f"   glBegin(GL_TRIANGLES)")
        print(f"   Vertices: ({x1},{y1}), ({x2},{y2}), ({x3},{y3})")

# ============ ABSTRACTION (Shapes) ============

class Shape:
    """
    Abstraction - Base Shape class.
    Works with any Renderer through the Renderer interface.
    """
    
    def __init__(self, renderer: Renderer):
        self.renderer = renderer
    
    def draw(self):
        """To be implemented by subclasses"""
        raise NotImplementedError
    
    def resize(self, factor: float):
        """To be implemented by subclasses"""
        raise NotImplementedError

class Circle(Shape):
    """Refined Abstraction - Circle"""
    
    def __init__(self, renderer: Renderer, x: int, y: int, radius: int):
        super().__init__(renderer)
        self.x = x
        self.y = y
        self.radius = radius
    
    def draw(self):
        print(f"\n⭕ Circle: x={self.x}, y={self.y}, radius={self.radius}")
        self.renderer.render_circle(self.x, self.y, self.radius)
    
    def resize(self, factor: float):
        self.radius = int(self.radius * factor)
        print(f"⭕ Circle: Resized to radius {self.radius}")

class Square(Shape):
    """Refined Abstraction - Square"""
    
    def __init__(self, renderer: Renderer, x: int, y: int, size: int):
        super().__init__(renderer)
        self.x = x
        self.y = y
        self.size = size
    
    def draw(self):
        print(f"\n⬜ Square: x={self.x}, y={self.y}, size={self.size}")
        self.renderer.render_square(self.x, self.y, self.size)
    
    def resize(self, factor: float):
        self.size = int(self.size * factor)
        print(f"⬜ Square: Resized to size {self.size}")

class Triangle(Shape):
    """Refined Abstraction - Triangle"""
    
    def __init__(self, renderer: Renderer, x1: int, y1: int, x2: int, y2: int, x3: int, y3: int):
        super().__init__(renderer)
        self.x1, self.y1 = x1, y1
        self.x2, self.y2 = x2, y2
        self.x3, self.y3 = x3, y3
    
    def draw(self):
        print(f"\n🔺 Triangle: ({self.x1},{self.y1}), ({self.x2},{self.y2}), ({self.x3},{self.y3})")
        self.renderer.render_triangle(self.x1, self.y1, self.x2, self.y2, self.x3, self.y3)
    
    def resize(self, factor: float):
        # Scale from centroid
        cx = (self.x1 + self.x2 + self.x3) // 3
        cy = (self.y1 + self.y2 + self.y3) // 3
        
        self.x1 = int(cx + (self.x1 - cx) * factor)
        self.y1 = int(cy + (self.y1 - cy) * factor)
        self.x2 = int(cx + (self.x2 - cx) * factor)
        self.y2 = int(cy + (self.y2 - cy) * factor)
        self.x3 = int(cx + (self.x3 - cx) * factor)
        self.y3 = int(cy + (self.y3 - cy) * factor)
        
        print(f"🔺 Triangle: Resized")

# ============ USAGE ============

print("="*70)
print("BRIDGE PATTERN - SHAPES AND RENDERERS")
print("="*70)

# Create renderers
vector = VectorRenderer()
raster = RasterRenderer()
opengl = OpenGLRenderer()

# Example 1: Same shape with different renderers
print("\n### Example 1: Circle with Different Renderers ###")

circle_vector = Circle(vector, 100, 100, 50)
circle_vector.draw()

circle_raster = Circle(raster, 100, 100, 50)
circle_raster.draw()

circle_opengl = Circle(opengl, 100, 100, 50)
circle_opengl.draw()

# Example 2: Different shapes with same renderer
print("\n### Example 2: Different Shapes with Vector Renderer ###")

shapes_vector = [
    Circle(vector, 50, 50, 25),
    Square(vector, 100, 100, 60),
    Triangle(vector, 200, 200, 250, 200, 225, 250)
]

for shape in shapes_vector:
    shape.draw()

# Example 3: Switch renderer at runtime
print("\n### Example 3: Switch Renderer at Runtime ###")

circle = Circle(vector, 150, 150, 40)
print("Drawing with Vector renderer:")
circle.draw()

# Switch to raster
circle.renderer = raster
print("\nSwitching to Raster renderer:")
circle.draw()

# Switch to OpenGL
circle.renderer = opengl
print("\nSwitching to OpenGL renderer:")
circle.draw()

# Example 4: Resize and redraw
print("\n### Example 4: Resize Operations ###")

square = Square(raster, 100, 100, 50)
square.draw()

square.resize(1.5)
square.draw()

square.resize(0.8)
square.draw()

print("\n" + "="*70)
print("KEY BENEFITS:")
print("1. Add new shapes without changing renderers")
print("2. Add new renderers without changing shapes")
print("3. Combine any shape with any renderer")
print("4. Switch renderer at runtime")
print("="*70)
```

---

## Common Pitfalls

### ❌ Pitfall 1: Confusing Bridge with Adapter

```python
# ADAPTER - Makes incompatible interfaces work together
class Adapter:
    def __init__(self, adaptee):
        self.adaptee = adaptee
    
    def new_method(self):  # Different interface!
        return self.adaptee.old_method()

# BRIDGE - Separates abstraction from implementation
class Abstraction:
    def __init__(self, implementation):
        self.impl = implementation
    
    def operation(self):  # Uses implementation's interface
        return self.impl.implementation_method()
```

**Key Difference:**
- Adapter: Different interfaces → Convert to work together
- Bridge: Same interface → Separate concerns that vary independently

---

### ❌ Pitfall 2: Not Using Composition

```python
# BAD - Using inheritance (defeats the purpose!)

class Remote:
   pass

class TV:
   pass

class Radio:
   pass

class RemoteForTV(Remote, TV):
    pass

class RemoteForRadio(Remote, Radio):
    pass

# GOOD - Using composition (Bridge pattern)
class Remote:
    def __init__(self, device):
        self.device = device  # Composition!
```

---

### ❌ Pitfall 3: Implementation Depends on Abstraction

```python
from abc import ABC

class Abstraction(ABC):
   pass

class ConcreteAbstraction(Abstraction):
   pass

# BAD - Implementation knows about abstraction
class BadImplementation:
    def do_something(self, abstraction):
        # Depends on abstraction type!
        if isinstance(abstraction, ConcreteAbstraction):
            # ...
            pass

# GOOD - Implementation is independent
class GoodImplementation:
    def do_something(self):
        # Doesn't know about abstraction
        pass
```

---

### ❌ Pitfall 4: Creating Bridge When Not Needed

```python
# BAD - Only one implementation, no need for bridge
class Shape:
    def __init__(self, renderer):
        self.renderer = renderer  # Only one renderer exists!

# GOOD - Use simple inheritance if no variation
class Shape:
    def draw(self):
        # Direct implementation
        pass
```

---

## Best Practices

### ✅ 1. Identify Two Orthogonal Dimensions

```python
# Two dimensions that vary independently:
# Dimension 1: Message types (text, image, file)
# Dimension 2: Platforms (email, SMS, Slack)

# Without Bridge: 3 × 3 = 9 classes
# With Bridge: 3 + 3 = 6 classes
```

---

### ✅ 2. Keep Implementation Interface Minimal

```python
from abc import ABC, abstractmethod

# GOOD - Minimal, focused interface
class Renderer(ABC):
    @abstractmethod
    def render_point(self, x, y):
        pass
    
    @abstractmethod
    def render_line(self, x1, y1, x2, y2):
        pass

# BAD - Too many methods
class Renderer(ABC):
    @abstractmethod
    def render_everything_imaginable(self):
        pass  # Too specific, not flexible
```

---

### ✅ 3. Document the Two Hierarchies

```python
class Shape:
    """
    ABSTRACTION HIERARCHY:
    - Shape (base)
      - Circle
      - Square
      - Triangle
    
    IMPLEMENTATION HIERARCHY:
    - Renderer (interface)
      - VectorRenderer
      - RasterRenderer
      - OpenGLRenderer
    
    Bridge connects these two hierarchies.
    """
    pass
```

---

### ✅ 4. Allow Runtime Switching

```python
from abc import ABC

class Device(ABC):
    pass

class TV(Device):
   pass

class Radio(Device):
    pass

class RemoteControl:
    def __init__(self, device):
        self._device = device
    
    @property
    def device(self):
        return self._device
    
    @device.setter
    def device(self, new_device):
        """Allow switching device at runtime"""
        self._device = new_device

# Usage
tv = TV()
remote = RemoteControl(tv)
# ... use with TV ...
radio = Radio()
remote.device = radio  # Switch to radio
```

---

### ✅ 5. Use Dependency Injection

```python
from abc import ABC, abstractmethod

class Renderer(ABC):
    @abstractmethod
    def render_point(self, x, y):
        pass
    
    @abstractmethod
    def render_line(self, x1, y1, x2, y2):
        pass

class MockRenderer(Renderer):
    
    def render_point(self, x, y):
        pass
    
    def render_line(self, x1, y1, x2, y2):
        pass

class Shape:
    def __init__(self, renderer: Renderer):
        """Inject renderer dependency"""
        self.renderer = renderer

# Easy to test with mock
mock_renderer = MockRenderer()
shape = Shape(mock_renderer)
```

---

## Summary

| Aspect          | Details                                          |
|-----------------|--------------------------------------------------|
| **Purpose**     | Separate abstraction from implementation         |
| **Use When**    | Two orthogonal dimensions, avoid class explosion |
| **Avoid When**  | Single dimension, no variation in implementation |
| **Key Benefit** | Both hierarchies can evolve independently        |
| **Structure**   | Abstraction has-a Implementation                 |

---

## Bridge vs Other Patterns

| Pattern      | Separates                       | Purpose                    |
|--------------|---------------------------------|----------------------------|
| **Bridge**   | Abstraction from Implementation | Independent variation      |
| **Adapter**  | Incompatible interfaces         | Make them compatible       |
| **Strategy** | Algorithm from context          | Interchangeable algorithms |
| **State**    | State from context              | State-dependent behavior   |

---

## When to Use Bridge

✅ **Use Bridge when:**
- You have two dimensions that vary independently
- Want to avoid class explosion (N × M → N + M)
- Need to switch implementation at runtime
- Want platform independence

❌ **Don't use Bridge when:**
- Only one implementation
- Single dimension of variation
- Simple inheritance suffices
- Tight coupling is acceptable

---

## Key Takeaways

1. **Bridge ≠ Adapter:** Bridge separates concerns that vary independently; Adapter makes incompatible interfaces work together
2. **Composition over Inheritance:** Bridge uses composition (has-a) instead of inheritance (is-a)
3. **Two Hierarchies:** Creates two parallel hierarchies that can evolve separately
4. **Reduces Classes:** N abstractions × M implementations = N + M classes (not N × M)
5. **Runtime Flexibility:** Can switch implementation at runtime
