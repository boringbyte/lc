# Structural Patterns - Complete Guide

## 📋 Table of Contents
- [What are Structural Patterns?](#what-are-structural-patterns)
- [Overview of All Structural Patterns](#overview-of-all-structural-patterns)
- [Adapter Pattern](#adapter-pattern)
  - [What is Adapter Pattern?](#what-is-adapter-pattern)
  - [Real-World Analogy](#real-world-analogy)
  - [Visual Representation](#visual-representation)
  - [When to Use Adapter Pattern](#when-to-use-adapter-pattern)
  - [When NOT to Use](#when-not-to-use)
  - [Types of Adapters](#types-of-adapters)
  - [Object Adapter (Composition)](#object-adapter-composition)
  - [Class Adapter (Multiple Inheritance)](#class-adapter-multiple-inheritance)
  - [Real-World Example 1: Payment Gateway Integration](#real-world-example-1-payment-gateway-integration)
  - [Real-World Example 2: Database Adapters](#real-world-example-2-database-adapters)
  - [Real-World Example 3: Legacy System Integration](#real-world-example-3-legacy-system-integration)
- [Common Pitfalls](#common-pitfalls)
  - [❌ Pitfall 1: Adapter Does Too Much](#-pitfall-1-adapter-does-too-much)
  - [❌ Pitfall 2: Not Preserving Semantics](#-pitfall-2-not-preserving-semantics)
- [Best Practices](#best-practices)
  - [✅ 1. Keep Adapters Simple](#-1-keep-adapters-simple)
  - [✅ 2. Document What's Being Adapted](#-2-document-whats-being-adapted)
  - [✅ 3. Use Composition Over Inheritance](#-3-use-composition-over-inheritance)
  - [✅ 4. Handle Impedance Mismatch Carefully](#-4-handle-impedance-mismatch-carefully)
- [Summary](#summary)
---

## What are Structural Patterns?

**Structural Patterns** explain how to assemble objects and classes into larger structures while keeping these structures flexible and efficient.

### Key Characteristics:
- ✅ Focus on **composition** of classes and objects
- ✅ Make relationships between entities easier
- ✅ Simplify structure by identifying relationships
- ✅ Help ensure that if one part changes, entire structure doesn't need to change

### Purpose:
Structural patterns are about organizing different classes and objects to form larger structures and provide new functionality.

---

## Overview of All Structural Patterns

| Pattern       | Purpose                                             | When to Use                                                    |
|---------------|-----------------------------------------------------|----------------------------------------------------------------|
| **Adapter**   | Convert interface of a class into another interface | Integrate incompatible interfaces                              |
| **Bridge**    | Separate abstraction from implementation            | Avoid permanent binding between abstraction and implementation |
| **Composite** | Compose objects into tree structures                | Treat individual objects and compositions uniformly            |
| **Decorator** | Add responsibilities to objects dynamically         | Add features without subclassing                               |
| **Facade**    | Provide unified interface to subsystem              | Simplify complex subsystem                                     |
| **Flyweight** | Share common state among many objects               | Reduce memory usage with many similar objects                  |
| **Proxy**     | Provide surrogate/placeholder for another object    | Control access, add lazy loading, caching, etc.                |

---

## Adapter Pattern

### What is Adapter Pattern?

**Adapter Pattern** (also known as **Wrapper**) allows objects with incompatible interfaces to work together. It acts as a bridge between two incompatible interfaces.

### Real-World Analogy:
Think of a **power adapter** when traveling:
- US plug (2 flat pins) ↔ EU socket (2 round holes)
- The adapter converts one interface to another
- The plug and socket don't change, the adapter makes them compatible

### Visual Representation:
```
Client → expects Interface A
            ↓
         Adapter (implements Interface A)
            ↓
         Adaptee (has Interface B)
```

---

### When to Use Adapter Pattern

#### ✅ Perfect Use Cases:

1. **Legacy Code Integration**
   - Old system with different interface
   - Can't modify legacy code
   - Need to make it work with new system

2. **Third-Party Libraries**
   - External library has incompatible interface
   - Can't change library code
   - Need to adapt it to your interface

3. **Multiple Implementations**
   - Support multiple implementations with different interfaces
   - Want uniform interface for client code
   - Different vendors/APIs

4. **Interface Standardization**
   - Standardize interface across different components
   - Components have different interfaces
   - Need consistent API

---

### When NOT to Use

#### ❌ Avoid Adapter When:

1. **You Can Modify the Source**
   - If you own both interfaces, refactor instead
   - Direct integration is better than adapting

2. **Simple Interface Differences**
   - Just a method name difference
   - Better to create a simple wrapper function

3. **Over-Engineering**
   - Adding complexity without benefit
   - Direct usage is simpler

---

### Types of Adapters

There are **two types** of adapter patterns:

1. **Object Adapter** (Uses Composition) - More common in Python
2. **Class Adapter** (Uses Multiple Inheritance) - Less common

---

### Object Adapter (Composition)

```python
from abc import ABC, abstractmethod

# ============ TARGET INTERFACE ============
# This is what the client expects

class MediaPlayer(ABC):
    """Target interface - what client code expects"""
    
    @abstractmethod
    def play(self, filename: str):
        pass

# ============ ADAPTEE ============
# These are the incompatible classes we want to use

class MP3Player:
    """Existing class with incompatible interface"""
    
    def play_mp3(self, filename: str):
        print(f"🎵 Playing MP3 file: {filename}")

class MP4Player:
    """Another existing class with different interface"""
    
    def play_mp4(self, filename: str):
        print(f"🎬 Playing MP4 file: {filename}")

class VLCPlayer:
    """Yet another class with its own interface"""
    
    def play_vlc(self, filename: str):
        print(f"🎥 Playing VLC file: {filename}")

# ============ ADAPTERS ============
# These adapt the incompatible interfaces to our target interface

class MP3Adapter(MediaPlayer):
    """Adapter for MP3Player"""
    
    def __init__(self):
        self.mp3_player = MP3Player()  # Composition
    
    def play(self, filename: str):
        # Adapt the interface
        self.mp3_player.play_mp3(filename)

class MP4Adapter(MediaPlayer):
    """Adapter for MP4Player"""
    
    def __init__(self):
        self.mp4_player = MP4Player()  # Composition
    
    def play(self, filename: str):
        self.mp4_player.play_mp4(filename)

class VLCAdapter(MediaPlayer):
    """Adapter for VLCPlayer"""
    
    def __init__(self):
        self.vlc_player = VLCPlayer()  # Composition
    
    def play(self, filename: str):
        self.vlc_player.play_vlc(filename)

# ============ CLIENT CODE ============

class AudioPlayer:
    """
    Client code that works with MediaPlayer interface.
    It doesn't need to know about MP3Player, MP4Player, etc.
    """
    
    def __init__(self):
        self.players = {
            'mp3': MP3Adapter(),
            'mp4': MP4Adapter(),
            'vlc': VLCAdapter()
        }
    
    def play(self, file_type: str, filename: str):
        player = self.players.get(file_type.lower())
        
        if player:
            player.play(filename)
        else:
            print(f"❌ Unsupported file type: {file_type}")

# Usage
audio_player = AudioPlayer()

audio_player.play('mp3', 'song.mp3')
audio_player.play('mp4', 'video.mp4')
audio_player.play('vlc', 'movie.vlc')
audio_player.play('avi', 'video.avi')  # Unsupported
```

**Output:**
```
🎵 Playing MP3 file: song.mp3
🎬 Playing MP4 file: video.mp4
🎥 Playing VLC file: movie.vlc
❌ Unsupported file type: avi
```

---

### Class Adapter (Multiple Inheritance)

```python
from abc import ABC, abstractmethod

# Target interface
class MediaPlayer(ABC):
    @abstractmethod
    def play(self, filename: str):
        pass

# Adaptee
class MP3Player:
    def play_mp3(self, filename: str):
        print(f"🎵 Playing MP3: {filename}")

# Class Adapter using multiple inheritance
class MP3ClassAdapter(MediaPlayer, MP3Player):
    """
    Uses multiple inheritance.
    Inherits from both target interface and adaptee.
    """
    
    def play(self, filename: str):
        # Call inherited method from MP3Player
        self.play_mp3(filename)

# Usage
adapter = MP3ClassAdapter()
adapter.play('song.mp3')
```

**Note:** Object Adapter (composition) is generally preferred in Python because:
- More flexible
- Follows "composition over inheritance" principle
- Can adapt multiple adaptees
- Can adapt private/final classes

---

### Real-World Example 1: Payment Gateway Integration

```python
from abc import ABC, abstractmethod
from typing import Dict

# ============ TARGET INTERFACE ============

class PaymentProcessor(ABC):
    """Standard payment interface our application expects"""
    
    @abstractmethod
    def process_payment(self, amount: float, currency: str, card_info: Dict) -> Dict:
        pass
    
    @abstractmethod
    def refund(self, transaction_id: str, amount: float) -> Dict:
        pass

# ============ ADAPTEES (Third-party APIs) ============

class StripeAPI:
    """Stripe's actual API (simplified)"""
    
    def create_charge(self, amount_cents: int, currency: str, source: str) -> Dict:
        print(f"💳 Stripe: Charging {amount_cents/100} {currency}")
        return {
            'stripe_charge_id': 'ch_stripe123',
            'status': 'succeeded',
            'amount': amount_cents
        }
    
    def create_refund(self, charge_id: str, amount_cents: int) -> Dict:
        print(f"💰 Stripe: Refunding {amount_cents/100}")
        return {
            'stripe_refund_id': 'rf_stripe123',
            'status': 'succeeded'
        }

class PayPalAPI:
    """PayPal's actual API (simplified)"""
    
    def execute_payment(self, amount: float, currency: str, payer_info: Dict) -> Dict:
        print(f"💵 PayPal: Processing ${amount} {currency}")
        return {
            'paypal_transaction_id': 'PAYID-123',
            'state': 'approved',
            'total': amount
        }
    
    def refund_transaction(self, transaction_id: str, refund_amount: float) -> Dict:
        print(f"💸 PayPal: Refunding ${refund_amount}")
        return {
            'refund_id': 'REFUND-123',
            'state': 'completed'
        }

class SquareAPI:
    """Square's actual API (simplified)"""
    
    def charge_card(self, money: Dict, card_nonce: str) -> Dict:
        amount = money['amount']
        currency = money['currency']
        print(f"🔷 Square: Charging {amount} {currency}")
        return {
            'square_payment_id': 'sq_payment_123',
            'status': 'COMPLETED',
            'amount_money': money
        }
    
    def create_payment_refund(self, payment_id: str, amount_money: Dict) -> Dict:
        print(f"🔶 Square: Refunding {amount_money['amount']}")
        return {
            'refund_id': 'sq_refund_123',
            'status': 'COMPLETED'
        }

# ============ ADAPTERS ============

class StripeAdapter(PaymentProcessor):
    """Adapter for Stripe API"""
    
    def __init__(self):
        self.stripe = StripeAPI()
        self._last_charge_id = None
    
    def process_payment(self, amount: float, currency: str, card_info: Dict) -> Dict:
        # Convert dollars to cents (Stripe uses cents)
        amount_cents = int(amount * 100)
        
        # Adapt our interface to Stripe's interface
        result = self.stripe.create_charge(
            amount_cents=amount_cents,
            currency=currency,
            source=card_info.get('token', 'tok_visa')
        )
        
        # Store for refunds
        self._last_charge_id = result['stripe_charge_id']
        
        # Convert Stripe's response to our standard format
        return {
            'transaction_id': result['stripe_charge_id'],
            'status': 'success' if result['status'] == 'succeeded' else 'failed',
            'amount': amount,
            'currency': currency,
            'provider': 'stripe'
        }
    
    def refund(self, transaction_id: str, amount: float) -> Dict:
        amount_cents = int(amount * 100)
        result = self.stripe.create_refund(transaction_id, amount_cents)
        
        return {
            'refund_id': result['stripe_refund_id'],
            'status': 'success' if result['status'] == 'succeeded' else 'failed',
            'amount': amount,
            'provider': 'stripe'
        }

class PayPalAdapter(PaymentProcessor):
    """Adapter for PayPal API"""
    
    def __init__(self):
        self.paypal = PayPalAPI()
    
    def process_payment(self, amount: float, currency: str, card_info: Dict) -> Dict:
        # Adapt to PayPal's interface
        payer_info = {
            'email': card_info.get('email', 'customer@example.com'),
            'name': card_info.get('name', 'Customer')
        }
        
        result = self.paypal.execute_payment(amount, currency, payer_info)
        
        # Convert to standard format
        return {
            'transaction_id': result['paypal_transaction_id'],
            'status': 'success' if result['state'] == 'approved' else 'failed',
            'amount': amount,
            'currency': currency,
            'provider': 'paypal'
        }
    
    def refund(self, transaction_id: str, amount: float) -> Dict:
        result = self.paypal.refund_transaction(transaction_id, amount)
        
        return {
            'refund_id': result['refund_id'],
            'status': 'success' if result['state'] == 'completed' else 'failed',
            'amount': amount,
            'provider': 'paypal'
        }

class SquareAdapter(PaymentProcessor):
    """Adapter for Square API"""
    
    def __init__(self):
        self.square = SquareAPI()
    
    def process_payment(self, amount: float, currency: str, card_info: Dict) -> Dict:
        # Square uses a different format for money
        money = {
            'amount': int(amount * 100),  # Convert to cents
            'currency': currency
        }
        
        result = self.square.charge_card(money, card_info.get('nonce', 'cnon_visa'))
        
        return {
            'transaction_id': result['square_payment_id'],
            'status': 'success' if result['status'] == 'COMPLETED' else 'failed',
            'amount': amount,
            'currency': currency,
            'provider': 'square'
        }
    
    def refund(self, transaction_id: str, amount: float) -> Dict:
        amount_money = {
            'amount': int(amount * 100),
            'currency': 'USD'
        }
        
        result = self.square.create_payment_refund(transaction_id, amount_money)
        
        return {
            'refund_id': result['refund_id'],
            'status': 'success' if result['status'] == 'COMPLETED' else 'failed',
            'amount': amount,
            'provider': 'square'
        }

# ============ CLIENT CODE ============

class PaymentService:
    """
    Our application's payment service.
    Works with any PaymentProcessor, doesn't care about implementation.
    """
    
    def __init__(self, processor: PaymentProcessor):
        self.processor = processor
    
    def charge_customer(self, amount: float, currency: str, card_info: Dict):
        print(f"\n💰 Processing payment of {amount} {currency}...")
        result = self.processor.process_payment(amount, currency, card_info)
        
        if result['status'] == 'success':
            print(f"✅ Payment successful! Transaction ID: {result['transaction_id']}")
        else:
            print(f"❌ Payment failed!")
        
        return result
    
    def refund_customer(self, transaction_id: str, amount: float):
        print(f"\n💸 Processing refund of ${amount}...")
        result = self.processor.refund(transaction_id, amount)
        
        if result['status'] == 'success':
            print(f"✅ Refund successful! Refund ID: {result['refund_id']}")
        else:
            print(f"❌ Refund failed!")
        
        return result

# ============ USAGE ============

# Using Stripe
print("="*60)
print("USING STRIPE")
print("="*60)
stripe_service = PaymentService(StripeAdapter())
result = stripe_service.charge_customer(99.99, 'USD', {'token': 'tok_visa'})
stripe_service.refund_customer(result['transaction_id'], 99.99)

# Using PayPal
print("\n" + "="*60)
print("USING PAYPAL")
print("="*60)
paypal_service = PaymentService(PayPalAdapter())
result = paypal_service.charge_customer(49.99, 'USD', {'email': 'user@example.com'})
paypal_service.refund_customer(result['transaction_id'], 49.99)

# Using Square
print("\n" + "="*60)
print("USING SQUARE")
print("="*60)
square_service = PaymentService(SquareAdapter())
result = square_service.charge_customer(149.99, 'USD', {'nonce': 'cnon_card'})
square_service.refund_customer(result['transaction_id'], 149.99)

# Easy to switch providers!
print("\n" + "="*60)
print("SWITCHING PROVIDERS IS EASY")
print("="*60)
def process_order(payment_provider: str):
    """Can easily switch providers based on configuration"""
    providers = {
        'stripe': StripeAdapter(),
        'paypal': PayPalAdapter(),
        'square': SquareAdapter()
    }
    
    processor = providers.get(payment_provider)
    if processor:
        service = PaymentService(processor)
        service.charge_customer(29.99, 'USD', {})

process_order('stripe')
process_order('paypal')
```

---

### Real-World Example 2: Database Adapters

```python
from abc import ABC, abstractmethod
from typing import Any

# ============ TARGET INTERFACE ============

class Database(ABC):
    """Standard database interface"""
    
    @abstractmethod
    def connect(self, connection_string: str):
        pass
    
    @abstractmethod
    def query(self, sql: str) -> list[dict[str, Any]]:
        pass
    
    @abstractmethod
    def execute(self, sql: str) -> int:
        pass
    
    @abstractmethod
    def close(self):
        pass

# ============ ADAPTEES ============

class MySQLDriver:
    """MySQL's native driver (simplified)"""
    
    def mysql_connect(self, host: str, user: str, password: str, database: str):
        print(f"🐬 MySQL: Connected to {database} at {host}")
        self.connected = True
    
    def mysql_query(self, query: str) -> list[tuple]:
        print(f"🐬 MySQL: Executing query: {query}")
        # Returns list of tuples
        return [
            ('Alice', 30, 'alice@example.com'),
            ('Bob', 25, 'bob@example.com')
        ]
    
    def mysql_execute(self, statement: str) -> int:
        print(f"🐬 MySQL: Executing: {statement}")
        return 1  # Rows affected
    
    def mysql_close(self):
        print("🐬 MySQL: Connection closed")
        self.connected = False

class PostgreSQLDriver:
    """PostgreSQL's native driver (simplified)"""
    
    def pg_connect(self, dsn: str):
        print(f"🐘 PostgreSQL: Connected using DSN: {dsn}")
        self.connection = "active"
    
    def pg_execute_query(self, sql: str) -> list[dict]:
        print(f"🐘 PostgreSQL: Query: {sql}")
        # Returns list of dicts
        return [
            {'name': 'Charlie', 'age': 35, 'email': 'charlie@example.com'},
            {'name': 'Diana', 'age': 28, 'email': 'diana@example.com'}
        ]
    
    def pg_execute_command(self, sql: str) -> dict:
        print(f"🐘 PostgreSQL: Command: {sql}")
        return {'rows_affected': 1, 'status': 'OK'}
    
    def pg_disconnect(self):
        print("🐘 PostgreSQL: Disconnected")
        self.connection = None

class MongoDBDriver:
    """MongoDB's native driver (simplified)"""
    
    def mongo_connect(self, uri: str, db_name: str):
        print(f"🍃 MongoDB: Connected to {db_name}")
        self.db = db_name
    
    def mongo_find(self, collection: str, query: dict) -> list[dict]:
        print(f"🍃 MongoDB: Finding in {collection}: {query}")
        return [
            {'_id': '1', 'name': 'Eve', 'age': 32},
            {'_id': '2', 'name': 'Frank', 'age': 29}
        ]
    
    def mongo_insert(self, collection: str, document: dict) -> str:
        print(f"🍃 MongoDB: Inserting into {collection}")
        return 'inserted_id_123'
    
    def mongo_close(self):
        print("🍃 MongoDB: Connection closed")
        self.db = None

# ============ ADAPTERS ============

class MySQLAdapter(Database):
    """Adapter for MySQL"""
    
    def __init__(self):
        self.driver = MySQLDriver()
    
    def connect(self, connection_string: str):
        # Parse connection string: "host=localhost;user=root;password=pass;database=mydb"
        params = dict(param.split('=') for param in connection_string.split(';'))
        self.driver.mysql_connect(
            params['host'],
            params['user'],
            params['password'],
            params['database']
        )
    
    def query(self, sql: str) -> list[dict[str, Any]]:
        # MySQL returns tuples, we need to convert to dicts
        result_tuples = self.driver.mysql_query(sql)
        
        # Convert tuples to dicts (assuming columns: name, age, email)
        columns = ['name', 'age', 'email']
        return [dict(zip(columns, row)) for row in result_tuples]
    
    def execute(self, sql: str) -> int:
        return self.driver.mysql_execute(sql)
    
    def close(self):
        self.driver.mysql_close()

class PostgreSQLAdapter(Database):
    """Adapter for PostgreSQL"""
    
    def __init__(self):
        self.driver = PostgreSQLDriver()
    
    def connect(self, connection_string: str):
        # PostgreSQL uses DSN format
        self.driver.pg_connect(connection_string)
    
    def query(self, sql: str) -> list[dict[str, Any]]:
        # PostgreSQL already returns dicts, perfect!
        return self.driver.pg_execute_query(sql)
    
    def execute(self, sql: str) -> int:
        result = self.driver.pg_execute_command(sql)
        return result['rows_affected']
    
    def close(self):
        self.driver.pg_disconnect()

class MongoDBAdapter(Database):
    """Adapter for MongoDB (NoSQL to SQL adapter!)"""
    
    def __init__(self):
        self.driver = MongoDBDriver()
        self.collection = 'users'  # Default collection
    
    def connect(self, connection_string: str):
        # Parse: "mongodb://localhost:27017/mydb"
        db_name = connection_string.split('/')[-1]
        self.driver.mongo_connect(connection_string, db_name)
    
    def query(self, sql: str) -> list[dict[str, Any]]:
        # Convert SQL-like query to MongoDB query
        # This is simplified - in reality would need SQL parsing
        print(f"⚠️  Converting SQL to MongoDB query: {sql}")
        result = self.driver.mongo_find(self.collection, {})
        
        # Remove MongoDB's _id field to match SQL interface
        for doc in result:
            if '_id' in doc:
                doc.pop('_id')
        
        return result
    
    def execute(self, sql: str) -> int:
        # Convert INSERT statement to MongoDB insert
        print(f"⚠️  Converting SQL command to MongoDB: {sql}")
        self.driver.mongo_insert(self.collection, {})
        return 1
    
    def close(self):
        self.driver.mongo_close()

# ============ CLIENT CODE ============

class UserRepository:
    """
    Repository that works with any database through standard interface.
    Doesn't care about MySQL, PostgreSQL, or MongoDB specifics.
    """
    
    def __init__(self, database: Database):
        self.db = database
    
    def get_all_users(self) -> list[dict[str, Any]]:
        return self.db.query("SELECT * FROM users")
    
    def create_user(self, name: str, age: int, email: str) -> int:
        sql = f"INSERT INTO users (name, age, email) VALUES ('{name}', {age}, '{email}')"
        return self.db.execute(sql)

# ============ USAGE ============

print("="*60)
print("USING MYSQL")
print("="*60)
mysql_db = MySQLAdapter()
mysql_db.connect("host=localhost;user=root;password=secret;database=myapp")
mysql_repo = UserRepository(mysql_db)
users = mysql_repo.get_all_users()
print(f"Users: {users}")
mysql_repo.create_user("New User", 40, "new@example.com")
mysql_db.close()

print("\n" + "="*60)
print("USING POSTGRESQL")
print("="*60)
pg_db = PostgreSQLAdapter()
pg_db.connect("postgresql://user:pass@localhost:5432/myapp")
pg_repo = UserRepository(pg_db)
users = pg_repo.get_all_users()
print(f"Users: {users}")
pg_repo.create_user("Another User", 45, "another@example.com")
pg_db.close()

print("\n" + "="*60)
print("USING MONGODB (NoSQL!)")
print("="*60)
mongo_db = MongoDBAdapter()
mongo_db.connect("mongodb://localhost:27017/myapp")
mongo_repo = UserRepository(mongo_db)
users = mongo_repo.get_all_users()
print(f"Users: {users}")
mongo_repo.create_user("MongoDB User", 50, "mongo@example.com")
mongo_db.close()
```

---

### Real-World Example 3: Legacy System Integration

```python
from abc import ABC, abstractmethod
from datetime import datetime

# ============ NEW SYSTEM (TARGET INTERFACE) ============

class ModernLogger(ABC):
    """Modern logging interface with structured logging"""
    
    @abstractmethod
    def log(self, level: str, message: str, context: dict = None):
        pass
    
    @abstractmethod
    def get_logs(self, level: str = None) -> list[dict]:
        pass

# ============ LEGACY SYSTEM (ADAPTEE) ============

class LegacyFileLogger:
    """Old logging system that writes to files"""
    
    def __init__(self):
        self.log_file = "app.log"
    
    def write_log(self, text: str):
        """Legacy method - writes plain text to file"""
        print(f"📝 Writing to {self.log_file}: {text}")
        # In reality: open(self.log_file, 'a').write(text + '\n')
    
    def read_logs(self) -> str:
        """Returns logs as plain text"""
        return "2024-01-01 INFO: App started\n2024-01-01 ERROR: Failed"

class LegacySyslogger:
    """Old syslog-style logger"""
    
    def syslog(self, priority: int, facility: int, msg: str):
        """Legacy syslog interface"""
        print(f"📡 Syslog: priority={priority}, facility={facility}, msg={msg}")
    
    def query_logs(self, priority_filter: int) -> list[str]:
        return ["<34>Jan 1 12:00:00 app: message 1"]

# ============ ADAPTERS ============

class LegacyFileLoggerAdapter(ModernLogger):
    """Adapts legacy file logger to modern interface"""
    
    def __init__(self):
        self.legacy_logger = LegacyFileLogger()
        self._level_map = {
            'DEBUG': 'DEBUG',
            'INFO': 'INFO',
            'WARNING': 'WARN',
            'ERROR': 'ERROR',
            'CRITICAL': 'FATAL'
        }
    
    def log(self, level: str, message: str, context: dict = None):
        # Convert modern structured log to legacy plain text format
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        legacy_level = self._level_map.get(level, 'INFO')
        
        log_line = f"[{timestamp}] {legacy_level}: {message}"
        
        if context:
            # Add context as key=value pairs
            context_str = ", ".join(f"{k}={v}" for k, v in context.items())
            log_line += f" | {context_str}"
        
        self.legacy_logger.write_log(log_line)
    
    def get_logs(self, level: str = None) -> list[dict]:
        # Parse legacy plain text logs into structured format
        logs_text = self.legacy_logger.read_logs()
        logs = []
        
        for line in logs_text.split('\n'):
            if not line:
                continue
            
            # Parse: "2024-01-01 INFO: App started"
            parts = line.split(': ', 1)
            if len(parts) == 2:
                meta, message = parts
                date_level = meta.split(' ')
                
                log_entry = {
                    'timestamp': date_level[0] if date_level else '',
                    'level': date_level[1] if len(date_level) > 1 else '',
                    'message': message,
                    'context': {}
                }
                
                if level is None or log_entry['level'] == level:
                    logs.append(log_entry)
        
        return logs

class LegacySysloggerAdapter(ModernLogger):
    """Adapts legacy syslog to modern interface"""
    
    def __init__(self):
        self.legacy_syslog = LegacySyslogger()
        # Syslog priority mapping
        self._priority_map = {
            'DEBUG': 7,
            'INFO': 6,
            'WARNING': 4,
            'ERROR': 3,
            'CRITICAL': 2
        }
    
    def log(self, level: str, message: str, context: dict = None):
        priority = self._priority_map.get(level, 6)
        facility = 16  # Local0
        
        full_message = message
        if context:
            context_str = ", ".join(f"{k}={v}" for k, v in context.items())
            full_message += f" [{context_str}]"
        
        self.legacy_syslog.syslog(priority, facility, full_message)
    
    def get_logs(self, level: str = None) -> list[dict]:
        # Query all logs and parse
        priority = self._priority_map.get(level, 7) if level else 7
        raw_logs = self.legacy_syslog.query_logs(priority)
        
        logs = []
        for raw_log in raw_logs:
            # Parse syslog format
            logs.append({
                'timestamp': 'parsed_timestamp',
                'level': level or 'INFO',
                'message': raw_log,
                'context': {}
            })
        
        return logs

# ============ CLIENT CODE ============

class Application:
    """Modern application using modern logging interface"""
    
    def __init__(self, logger: ModernLogger):
        self.logger = logger
    
    def start(self):
        self.logger.log('INFO', 'Application starting', {'version': '2.0'})
    
    def process_request(self, user_id: int):
        self.logger.log('DEBUG', 'Processing request', {'user_id': user_id})
        
        try:
            # ... processing ...
            self.logger.log('INFO', 'Request processed successfully', {'user_id': user_id})
        except Exception as e:
            self.logger.log('ERROR', 'Request failed', {'user_id': user_id, 'error': str(e)})
    
    def get_error_logs(self):
        return self.logger.get_logs('ERROR')

# ============ USAGE ============

print("="*60)
print("USING LEGACY FILE LOGGER (ADAPTED)")
print("="*60)
file_logger = LegacyFileLoggerAdapter()
app1 = Application(file_logger)
app1.start()
app1.process_request(123)
print("\nRetrieving logs:")
logs = app1.get_error_logs()
for log in logs:
    print(f"  {log}")

print("\n" + "="*60)
print("USING LEGACY SYSLOG (ADAPTED)")
print("="*60)
syslog_logger = LegacySysloggerAdapter()
app2 = Application(syslog_logger)
app2.start()
app2.process_request(456)
```

---

## Common Pitfalls

### ❌ Pitfall 1: Adapter Does Too Much

```python
# BAD - Adapter doing business logic
from abc import ABC

class TargetInterface(ABC):
   pass

class Adaptee:
   pass

def process_result(update):
   pass

def transform(update):
   pass
   
class BadAdapter(TargetInterface):
   def __init__(self):
      self.adaptee = Adaptee()

   def target_method(self, some_complex_condition):
      # Adapter should NOT contain business logic!
      if some_complex_condition:
         result = self.adaptee.method1()
         process_result(result)
         return transform(result)
      # ... more business logic


# GOOD - Adapter only adapts interface
class GoodAdapter(TargetInterface):
   def __init__(self):
      self.adaptee = Adaptee()

   def target_method(self):
      # Just adapt the interface
      return self.adaptee.adaptee_method()
```

---

### ❌ Pitfall 2: Not Preserving Semantics

```python
# BAD - Changes behavior, not just interface
class BadAdapter:
    def save(self, data):
        # Original method throws exception on error
        # But adapter swallows it!
        try:
            self.adaptee.persist(data)
        except Exception:
            return False  # Changed semantics!

# GOOD - Preserves behavior
class GoodAdapter:
    def save(self, data):
        # Let exceptions propagate
        self.adaptee.persist(data)
```

---

## Best Practices

### ✅ 1. Keep Adapters Simple

```python
# Adapter should only translate interface, not add features
from abc import ABC

class Target(ABC):
   pass

class Adaptee:
   
   def specific_request(self):
      pass
   
class SimpleAdapter(Target):
    def __init__(self, adaptee: Adaptee):
        self.adaptee = adaptee
    
    def request(self):
        return self.adaptee.specific_request()
```

---

### ✅ 2. Document What's Being Adapted

```python
from abc import ABC

class PaymentProcessor(ABC):
   pass

class PaymentAdapter(PaymentProcessor):
    """
    Adapts Stripe API to our PaymentProcessor interface.
    
    Stripe specifics:
    - Uses cents instead of dollars
    - Returns 'succeeded' instead of 'success'
    - Requires stripe_charge_id for refunds
    """
    pass
```

---

### ✅ 3. Use Composition Over Inheritance

Prefer Object Adapter (composition) over Class Adapter (inheritance) in Python.

---

### ✅ 4. Handle Impedance Mismatch Carefully

```python
class DatabaseAdapter:
    def query(self, sql: str) -> list[dict]:
        # NoSQL doesn't understand SQL
        # Document the limitation
        if "JOIN" in sql.upper():
            raise NotImplementedError(
                "MongoDB adapter doesn't support JOINs. "
                "Use separate queries instead."
            )
        # ... conversion logic
```

---

## Summary

| Aspect               | Details                                                        |
|----------------------|----------------------------------------------------------------|
| **Purpose**          | Make incompatible interfaces work together                     |
| **Use When**         | Integrating legacy code, third-party libraries, different APIs |
| **Avoid When**       | You control both interfaces, simple wrapper suffices           |
| **Key Benefit**      | Reuse existing code without modification                       |
| **Common Use Cases** | Payment gateways, databases, legacy systems                    |
