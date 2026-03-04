# Proxy Pattern - Complete Guide

## 📋 Table of Contents
- [What is Proxy Pattern?](#what-is-proxy-pattern)
  - [Key Characteristics](#key-characteristics)
  - [Real-World Analogy](#real-world-analogy)
  - [Visual Representation](#visual-representation)
  - [Proxy vs Similar Patterns](#proxy-vs-similar-patterns)
- [Types of Proxies](#types-of-proxies)
  - [1. **Virtual Proxy** (Lazy Initialization)](#1-virtual-proxy-lazy-initialization)
  - [2. **Protection Proxy** (Access Control)](#2-protection-proxy-access-control)
  - [3. **Remote Proxy**](#3-remote-proxy)
  - [4. **Caching Proxy** (Cache)](#4-caching-proxy-cache)
  - [5. **Logging Proxy**](#5-logging-proxy)
  - [6. **Smart Reference Proxy**](#6-smart-reference-proxy)
- [When to Use](#when-to-use)
  - [✅ Perfect Use Cases](#-perfect-use-cases)
- [When NOT to Use](#when-not-to-use)
  - [❌ Avoid Proxy When](#-avoid-proxy-when)
- [Basic Implementation](#basic-implementation)
  - [Simple Proxy Structure](#simple-proxy-structure)
- [Real-World Examples](#real-world-examples)
  - [Example 1: Virtual Proxy (Lazy Loading Images)](#example-1-virtual-proxy-lazy-loading-images)
  - [Example 2: Protection Proxy (Access Control)](#example-2-protection-proxy-access-control)
  - [Example 3: Caching Proxy](#example-3-caching-proxy)
  - [Example 4: Remote Proxy (API Wrapper)](#example-4-remote-proxy-api-wrapper)
- [Common Pitfalls](#common-pitfalls)
  - [❌ Pitfall 1: Proxy Has Different Interface](#-pitfall-1-proxy-has-different-interface)
  - [❌ Pitfall 2: Not Handling Errors in Remote Proxy](#-pitfall-2-not-handling-errors-in-remote-proxy)
  - [❌ Pitfall 3: Cache Never Expires](#-pitfall-3-cache-never-expires)
  - [❌ Pitfall 4: Circular References in Virtual Proxy](#-pitfall-4-circular-references-in-virtual-proxy)
- [Best Practices](#best-practices)
  - [✅ 1. Keep Proxy Transparent](#-1-keep-proxy-transparent)
  - [✅ 2. Document Proxy Behavior](#-2-document-proxy-behavior)
  - [✅ 3. Provide Cache Control Methods](#-3-provide-cache-control-methods)
  - [✅ 4. Handle Resource Cleanup](#-4-handle-resource-cleanup)
  - [✅ 5. Use Proxy for Cross-Cutting Concerns](#-5-use-proxy-for-cross-cutting-concerns)
- [Summary](#summary)
- [Proxy Types Summary](#proxy-types-summary)
- [Pattern Comparison](#pattern-comparison)
---

## What is Proxy Pattern?

**Proxy Pattern** provides a surrogate or placeholder object that controls access to another object. The proxy has the same interface as the real object, so clients interact with it as if it were the real thing.

### Key Characteristics:
- ✅ Controls access to another object
- ✅ Same interface as the real object
- ✅ Can add functionality without changing the real object
- ✅ Transparent to client (client doesn't know it's using a proxy)
- ✅ Can delay expensive operations

### Real-World Analogy:
Think of a **credit card** as a proxy for your bank account:
- Credit card has the same interface (you can pay with it)
- It controls access to your actual money
- Adds features (fraud protection, rewards)
- Delays actual money transfer
- You use it transparently (merchants treat it like cash)

### Visual Representation:
```
Client → Proxy → Real Object
         (controls access)
         (adds functionality)
         (same interface)
```

---

### Proxy vs Similar Patterns

| Pattern       | Purpose                           | Changes Behavior?                  |
|---------------|-----------------------------------|------------------------------------|
| **Proxy**     | Control access, add functionality | No - same interface, transparent   |
| **Decorator** | Add responsibilities dynamically  | No - wraps and enhances            |
| **Adapter**   | Convert interface                 | Yes - provides different interface |
| **Facade**    | Simplify complex system           | Yes - provides simpler interface   |

**Key Difference:** Proxy has the **same interface** as the real object and is meant to be **transparent** to the client.

---

## Types of Proxies

### 1. **Virtual Proxy** (Lazy Initialization)
- Delays creation of expensive object until needed
- Example: Loading large images only when displayed

### 2. **Protection Proxy** (Access Control)
- Controls access based on permissions
- Example: User authentication/authorization

### 3. **Remote Proxy**
- Represents object in different address space
- Example: Network calls, RPC, web services

### 4. **Caching Proxy** (Cache)
- Caches results of expensive operations
- Example: Database query caching

### 5. **Logging Proxy**
- Logs all method calls
- Example: Audit trails, debugging

### 6. **Smart Reference Proxy**
- Additional actions when object is accessed
- Example: Reference counting, locking

---

## When to Use

### ✅ Perfect Use Cases:

#### 1. **Expensive Object Creation**
- Object takes time/resources to create
- Want lazy initialization
- Create only when actually needed

#### 2. **Access Control**
- Need to check permissions
- Different users have different access
- Security requirements

#### 3. **Remote Objects**
- Object is on different machine
- Network communication needed
- Hide network complexity

#### 4. **Caching**
- Results are expensive to compute
- Same results requested repeatedly
- Want to cache results

#### 5. **Logging/Monitoring**
- Need to track usage
- Audit trails required
- Debug information needed

#### 6. **Resource Management**
- Limited resources (connections, files)
- Need to manage lifecycle
- Reference counting

---

## When NOT to Use

### ❌ Avoid Proxy When:

1. **No Control Needed**
   - Direct access is fine
   - No additional functionality needed
   - Adds unnecessary complexity

2. **Performance Critical**
   - Proxy adds overhead
   - Every call goes through proxy
   - Direct access is faster

3. **Simple Objects**
   - Object is cheap to create
   - No access control needed
   - No additional functionality

4. **Over-Engineering**
   - YAGNI (You Aren't Gonna Need It)
   - Adds complexity without benefit

---

## Basic Implementation

### Simple Proxy Structure

```python
from abc import ABC, abstractmethod

# ============ SUBJECT INTERFACE ============

class Subject(ABC):
    """Interface that both RealSubject and Proxy implement"""
    
    @abstractmethod
    def request(self) -> str:
        pass

# ============ REAL SUBJECT ============

class RealSubject(Subject):
    """The real object that does the actual work"""
    
    def request(self) -> str:
        return "RealSubject: Handling request"

# ============ PROXY ============

class Proxy(Subject):
    """
    Proxy that controls access to RealSubject.
    Implements same interface as RealSubject.
    """
    
    def __init__(self, real_subject: RealSubject = None):
        self._real_subject = real_subject
    
    def request(self) -> str:
        """
        Proxy controls access and can add functionality
        before/after delegating to real subject
        """
        # Pre-processing
        if self._check_access():
            # Lazy initialization
            if self._real_subject is None:
                self._real_subject = RealSubject()
            
            # Delegate to real subject
            result = self._real_subject.request()
            
            # Post-processing
            self._log_access()
            
            return result
        else:
            return "Proxy: Access denied"
    
    def _check_access(self) -> bool:
        """Check if access is allowed"""
        print("Proxy: Checking access")
        return True
    
    def _log_access(self):
        """Log the access"""
        print("Proxy: Logging access")

# ============ CLIENT CODE ============

def client_code(subject: Subject):
    """
    Client works with Subject interface.
    Doesn't know if it's working with Proxy or RealSubject.
    """
    result = subject.request()
    print(f"Result: {result}")

# Using real subject directly
print("=== Using RealSubject directly ===")
real = RealSubject()
client_code(real)

print("\n=== Using Proxy ===")
proxy = Proxy()
client_code(proxy)  # Transparent to client
```

---

## Real-World Examples

### Example 1: Virtual Proxy (Lazy Loading Images)

```python
from abc import ABC, abstractmethod
import time
from typing import Optional

# ============ INTERFACE ============

class Image(ABC):
    """Interface for images"""
    
    @abstractmethod
    def display(self):
        pass
    
    @abstractmethod
    def get_size(self) -> int:
        pass

# ============ REAL SUBJECT ============

class RealImage(Image):
    """
    Real image that's expensive to load.
    Simulates loading from disk/network.
    """
    
    def __init__(self, filename: str):
        self.filename = filename
        self._data = None
        self._load_from_disk()
    
    def _load_from_disk(self):
        """Expensive operation - loading image"""
        print(f"📁 RealImage: Loading {self.filename} from disk...")
        time.sleep(2)  # Simulate slow loading
        
        # Simulate image data
        self._data = f"[Image data for {self.filename}]"
        print(f"✅ RealImage: {self.filename} loaded successfully")
    
    def display(self):
        """Display the image"""
        print(f"🖼️  Displaying {self.filename}")
        print(f"   Data: {self._data}")
    
    def get_size(self) -> int:
        """Get image size"""
        return len(self._data) if self._data else 0

# ============ PROXY (VIRTUAL PROXY) ============

class ImageProxy(Image):
    """
    Virtual Proxy for lazy loading.
    Only loads real image when actually needed.
    """
    
    def __init__(self, filename: str):
        self.filename = filename
        self._real_image: Optional[RealImage] = None
    
    def display(self):
        """Display image - loads only when needed"""
        print(f"🔄 ImageProxy: display() called for {self.filename}")
        
        # Lazy initialization
        if self._real_image is None:
            print(f"🔄 ImageProxy: First access, loading real image...")
            self._real_image = RealImage(self.filename)
        else:
            print(f"✅ ImageProxy: Using cached image")
        
        self._real_image.display()
    
    def get_size(self) -> int:
        """Get size without loading full image"""
        # Can return approximate size without loading
        if self._real_image is None:
            print(f"🔄 ImageProxy: Returning approximate size without loading")
            return 1024  # Approximate size
        else:
            return self._real_image.get_size()

# ============ USAGE ============

print("="*60)
print("VIRTUAL PROXY - LAZY LOADING IMAGES")
print("="*60)

# Create image proxies (instant, no loading)
print("\n--- Creating image proxies (fast!) ---")
image1 = ImageProxy("photo1.jpg")
image2 = ImageProxy("photo2.jpg")
image3 = ImageProxy("photo3.jpg")
print("✅ All proxies created instantly")

# Check size without loading
print("\n--- Getting size without loading ---")
size = image1.get_size()
print(f"Size: {size} bytes")

# Display image 1 (triggers loading)
print("\n--- Displaying image 1 (first time - loads) ---")
image1.display()

# Display image 1 again (no loading)
print("\n--- Displaying image 1 again (cached) ---")
image1.display()

# Display image 2 (triggers loading)
print("\n--- Displaying image 2 (first time - loads) ---")
image2.display()

# Image 3 never displayed - never loaded!
print("\n--- Image 3 never used - never loaded ---")
print(f"✅ Saved loading time for {image3.filename}")
```

---

### Example 2: Protection Proxy (Access Control)

```python
from abc import ABC, abstractmethod
from typing import Dict, List
from enum import Enum
from datetime import datetime

# ============ ENUMS ============

class Role(Enum):
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"

class Permission(Enum):
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    EXECUTE = "execute"

# ============ USER CLASS ============

class User:
    """Represents a user"""
    
    def __init__(self, username: str, role: Role):
        self.username = username
        self.role = role

# ============ INTERFACE ============

class Document(ABC):
    """Interface for documents"""
    
    @abstractmethod
    def read(self) -> str:
        pass
    
    @abstractmethod
    def write(self, content: str):
        pass
    
    @abstractmethod
    def delete(self):
        pass

# ============ REAL SUBJECT ============

class RealDocument(Document):
    """Real document with content"""
    
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content
        self.created_at = datetime.now()
        self.modified_at = datetime.now()
    
    def read(self) -> str:
        """Read document content"""
        print(f"📄 RealDocument: Reading '{self.title}'")
        return self.content
    
    def write(self, content: str):
        """Write to document"""
        print(f"✏️  RealDocument: Writing to '{self.title}'")
        self.content = content
        self.modified_at = datetime.now()
    
    def delete(self):
        """Delete document"""
        print(f"🗑️  RealDocument: Deleting '{self.title}'")
        self.content = "[DELETED]"

# ============ PROXY (PROTECTION PROXY) ============

class DocumentProxy(Document):
    """
    Protection Proxy that controls access based on user permissions.
    """
    
    # Define permissions for each role
    _role_permissions: Dict[Role, List[Permission]] = {
        Role.ADMIN: [Permission.READ, Permission.WRITE, Permission.DELETE, Permission.EXECUTE],
        Role.USER: [Permission.READ, Permission.WRITE],
        Role.GUEST: [Permission.READ]
    }
    
    def __init__(self, real_document: RealDocument, current_user: User):
        self._real_document = real_document
        self._current_user = current_user
        self._access_log: List[Dict] = []
    
    def _check_permission(self, required_permission: Permission) -> bool:
        """Check if current user has required permission"""
        user_permissions = self._role_permissions.get(self._current_user.role, [])
        has_permission = required_permission in user_permissions
        
        # Log access attempt
        self._access_log.append({
            'user': self._current_user.username,
            'role': self._current_user.role.value,
            'action': required_permission.value,
            'allowed': has_permission,
            'timestamp': datetime.now()
        })
        
        return has_permission
    
    def _log_access(self, action: str, success: bool):
        """Log access for audit trail"""
        status = "✅ SUCCESS" if success else "❌ DENIED"
        print(f"🔒 Access Log: {self._current_user.username} ({self._current_user.role.value}) "
              f"attempted {action} - {status}")
    
    def read(self) -> str:
        """Read with permission check"""
        print(f"\n🔐 DocumentProxy: Checking READ permission for {self._current_user.username}")
        
        if self._check_permission(Permission.READ):
            self._log_access("READ", True)
            return self._real_document.read()
        else:
            self._log_access("READ", False)
            raise PermissionError(f"User {self._current_user.username} doesn't have READ permission")
    
    def write(self, content: str):
        """Write with permission check"""
        print(f"\n🔐 DocumentProxy: Checking WRITE permission for {self._current_user.username}")
        
        if self._check_permission(Permission.WRITE):
            self._log_access("WRITE", True)
            self._real_document.write(content)
        else:
            self._log_access("WRITE", False)
            raise PermissionError(f"User {self._current_user.username} doesn't have WRITE permission")
    
    def delete(self):
        """Delete with permission check"""
        print(f"\n🔐 DocumentProxy: Checking DELETE permission for {self._current_user.username}")
        
        if self._check_permission(Permission.DELETE):
            self._log_access("DELETE", True)
            self._real_document.delete()
        else:
            self._log_access("DELETE", False)
            raise PermissionError(f"User {self._current_user.username} doesn't have DELETE permission")
    
    def get_access_log(self) -> List[Dict]:
        """Get access log (admin only)"""
        if self._current_user.role == Role.ADMIN:
            return self._access_log
        else:
            raise PermissionError("Only admins can view access logs")

# ============ USAGE ============

print("="*70)
print("PROTECTION PROXY - ACCESS CONTROL")
print("="*70)

# Create document
real_doc = RealDocument("Confidential Report", "This is sensitive information.")

# Create users with different roles
admin = User("alice", Role.ADMIN)
regular_user = User("bob", Role.USER)
guest = User("charlie", Role.GUEST)

# Test with Admin user
print("\n### ADMIN USER (alice) ###")
admin_proxy = DocumentProxy(real_doc, admin)

try:
    content = admin_proxy.read()
    print(f"Content: {content}")
    
    admin_proxy.write("Updated by admin")
    
    # Admin can delete
    # admin_proxy.delete()
    
except PermissionError as e:
    print(f"❌ Error: {e}")

# Test with Regular user
print("\n### REGULAR USER (bob) ###")
user_proxy = DocumentProxy(real_doc, regular_user)

try:
    content = user_proxy.read()
    print(f"Content: {content}")
    
    user_proxy.write("Updated by regular user")
    
    # Regular user cannot delete
    user_proxy.delete()
    
except PermissionError as e:
    print(f"❌ Error: {e}")

# Test with Guest user
print("\n### GUEST USER (charlie) ###")
guest_proxy = DocumentProxy(real_doc, guest)

try:
    content = guest_proxy.read()
    print(f"Content: {content}")
    
    # Guest cannot write
    guest_proxy.write("Trying to write as guest")
    
except PermissionError as e:
    print(f"❌ Error: {e}")

try:
    # Guest cannot delete
    guest_proxy.delete()
except PermissionError as e:
    print(f"❌ Error: {e}")

# View access log (admin only)
print("\n### ACCESS LOG (Admin only) ###")
try:
    log = admin_proxy.get_access_log()
    print(f"Total access attempts: {len(log)}")
    for entry in log[-5:]:  # Show last 5
        print(f"  {entry['timestamp'].strftime('%H:%M:%S')} - "
              f"{entry['user']} ({entry['role']}) - "
              f"{entry['action']}: {'✅' if entry['allowed'] else '❌'}")
except PermissionError as e:
    print(f"❌ Error: {e}")
```

---

### Example 3: Caching Proxy

```python
from abc import ABC, abstractmethod
import time
from typing import Dict, Optional, Any
from datetime import datetime, timedelta

# ============ INTERFACE ============

class DataService(ABC):
    """Interface for data service"""
    
    @abstractmethod
    def get_user_data(self, user_id: int) -> Dict:
        pass
    
    @abstractmethod
    def get_product_data(self, product_id: int) -> Dict:
        pass
    
    @abstractmethod
    def search(self, query: str) -> list:
        pass

# ============ REAL SUBJECT ============

class RealDataService(DataService):
    """
    Real data service that makes expensive database/API calls.
    """
    
    def get_user_data(self, user_id: int) -> Dict:
        """Expensive database query"""
        print(f"🗄️  RealDataService: Fetching user {user_id} from database...")
        time.sleep(1)  # Simulate slow database query
        
        return {
            'user_id': user_id,
            'name': f'User {user_id}',
            'email': f'user{user_id}@example.com',
            'created_at': '2024-01-01'
        }
    
    def get_product_data(self, product_id: int) -> Dict:
        """Expensive API call"""
        print(f"🌐 RealDataService: Fetching product {product_id} from API...")
        time.sleep(1.5)  # Simulate slow API call
        
        return {
            'product_id': product_id,
            'name': f'Product {product_id}',
            'price': 99.99,
            'stock': 50
        }
    
    def search(self, query: str) -> list:
        """Expensive search operation"""
        print(f"🔍 RealDataService: Searching for '{query}'...")
        time.sleep(2)  # Simulate slow search
        
        return [
            {'id': 1, 'title': f'Result 1 for {query}'},
            {'id': 2, 'title': f'Result 2 for {query}'},
            {'id': 3, 'title': f'Result 3 for {query}'},
        ]

# ============ CACHE ENTRY ============

class CacheEntry:
    """Represents a cached entry with expiration"""
    
    def __init__(self, data: Any, ttl_seconds: int = 60):
        self.data = data
        self.cached_at = datetime.now()
        self.expires_at = datetime.now() + timedelta(seconds=ttl_seconds)
    
    def is_expired(self) -> bool:
        """Check if cache entry is expired"""
        return datetime.now() > self.expires_at
    
    def get_age(self) -> float:
        """Get age in seconds"""
        return (datetime.now() - self.cached_at).total_seconds()

# ============ PROXY (CACHING PROXY) ============

class CachingDataServiceProxy(DataService):
    """
    Caching Proxy that caches expensive operations.
    """
    
    def __init__(self, real_service: RealDataService, default_ttl: int = 60):
        self._real_service = real_service
        self._cache: Dict[str, CacheEntry] = {}
        self._default_ttl = default_ttl
        
        # Statistics
        self._stats = {
            'hits': 0,
            'misses': 0,
            'total_requests': 0
        }
    
    def _get_cache_key(self, method: str, *args) -> str:
        """Generate cache key"""
        return f"{method}:{':'.join(map(str, args))}"
    
    def _get_from_cache(self, key: str) -> Optional[Any]:
        """Get from cache if exists and not expired"""
        if key in self._cache:
            entry = self._cache[key]
            
            if not entry.is_expired():
                self._stats['hits'] += 1
                age = entry.get_age()
                print(f"💾 Cache HIT: {key} (age: {age:.1f}s)")
                return entry.data
            else:
                print(f"⏰ Cache EXPIRED: {key}")
                del self._cache[key]
        
        self._stats['misses'] += 1
        print(f"❌ Cache MISS: {key}")
        return None
    
    def _store_in_cache(self, key: str, data: Any, ttl: Optional[int] = None):
        """Store in cache"""
        ttl = ttl or self._default_ttl
        self._cache[key] = CacheEntry(data, ttl)
        print(f"💾 Cached: {key} (TTL: {ttl}s)")
    
    def get_user_data(self, user_id: int) -> Dict:
        """Get user data with caching"""
        self._stats['total_requests'] += 1
        cache_key = self._get_cache_key('get_user_data', user_id)
        
        # Try cache first
        cached_data = self._get_from_cache(cache_key)
        if cached_data is not None:
            return cached_data
        
        # Cache miss - fetch from real service
        data = self._real_service.get_user_data(user_id)
        
        # Store in cache
        self._store_in_cache(cache_key, data, ttl=120)  # 2 minute TTL
        
        return data
    
    def get_product_data(self, product_id: int) -> Dict:
        """Get product data with caching"""
        self._stats['total_requests'] += 1
        cache_key = self._get_cache_key('get_product_data', product_id)
        
        cached_data = self._get_from_cache(cache_key)
        if cached_data is not None:
            return cached_data
        
        data = self._real_service.get_product_data(product_id)
        self._store_in_cache(cache_key, data, ttl=30)  # 30 second TTL
        
        return data
    
    def search(self, query: str) -> list:
        """Search with caching"""
        self._stats['total_requests'] += 1
        cache_key = self._get_cache_key('search', query)
        
        cached_data = self._get_from_cache(cache_key)
        if cached_data is not None:
            return cached_data
        
        data = self._real_service.search(query)
        self._store_in_cache(cache_key, data, ttl=300)  # 5 minute TTL
        
        return data
    
    def clear_cache(self):
        """Clear all cache"""
        print("🗑️  Clearing cache...")
        self._cache.clear()
    
    def get_stats(self) -> Dict:
        """Get cache statistics"""
        total = self._stats['total_requests']
        hits = self._stats['hits']
        hit_rate = (hits / total * 100) if total > 0 else 0
        
        return {
            'total_requests': total,
            'cache_hits': hits,
            'cache_misses': self._stats['misses'],
            'hit_rate': f"{hit_rate:.1f}%",
            'cached_items': len(self._cache)
        }

# ============ USAGE ============

print("="*70)
print("CACHING PROXY")
print("="*70)

# Create service with caching proxy
real_service = RealDataService()
cached_service = CachingDataServiceProxy(real_service, default_ttl=60)

# First request - cache miss
print("\n### First request for user 1 (cache miss) ###")
start = time.time()
user1 = cached_service.get_user_data(1)
duration1 = time.time() - start
print(f"Data: {user1}")
print(f"⏱️  Duration: {duration1:.2f}s")

# Second request - cache hit
print("\n### Second request for user 1 (cache hit!) ###")
start = time.time()
user1_again = cached_service.get_user_data(1)
duration2 = time.time() - start
print(f"Data: {user1_again}")
print(f"⏱️  Duration: {duration2:.2f}s (much faster!)")

# Different user - cache miss
print("\n### Request for user 2 (cache miss) ###")
user2 = cached_service.get_user_data(2)
print(f"Data: {user2}")

# Product requests
print("\n### Product requests ###")
product1 = cached_service.get_product_data(100)
print(f"Product: {product1['name']}")

product1_again = cached_service.get_product_data(100)  # Cache hit
print(f"Product (cached): {product1_again['name']}")

# Search requests
print("\n### Search requests ###")
results1 = cached_service.search("laptop")
print(f"Search results: {len(results1)} items")

results1_again = cached_service.search("laptop")  # Cache hit
print(f"Search results (cached): {len(results1_again)} items")

# Show statistics
print("\n### Cache Statistics ###")
stats = cached_service.get_stats()
for key, value in stats.items():
    print(f"  {key}: {value}")

# Test cache expiration
print("\n### Testing cache expiration ###")
print("Waiting for cache to expire (simulated)...")
# In real scenario, wait for TTL
# For demo, just clear cache
cached_service.clear_cache()

print("Requesting user 1 after cache clear (cache miss):")
user1_expired = cached_service.get_user_data(1)

# Final statistics
print("\n### Final Statistics ###")
stats = cached_service.get_stats()
for key, value in stats.items():
    print(f"  {key}: {value}")
```

---

### Example 4: Remote Proxy (API Wrapper)

```python
from abc import ABC, abstractmethod
from typing import Dict, List, Optional
import time
from datetime import datetime

# ============ INTERFACE ============

class WeatherService(ABC):
    """Interface for weather service"""
    
    @abstractmethod
    def get_current_weather(self, city: str) -> Dict:
        pass
    
    @abstractmethod
    def get_forecast(self, city: str, days: int) -> List[Dict]:
        pass

# ============ REAL SUBJECT (Remote Service) ============

class RemoteWeatherAPI(WeatherService):
    """
    Real remote weather API.
    In reality, this would make HTTP requests to external API.
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.api_url = "https://api.weather.com"
    
    def get_current_weather(self, city: str) -> Dict:
        """Make HTTP request to get current weather"""
        print(f"🌐 RemoteWeatherAPI: Making HTTP request to {self.api_url}")
        print(f"   Endpoint: /current/{city}")
        
        # Simulate network delay
        time.sleep(0.5)
        
        # Simulate API response
        return {
            'city': city,
            'temperature': 22,
            'condition': 'Sunny',
            'humidity': 65,
            'wind_speed': 10,
            'timestamp': datetime.now().isoformat()
        }
    
    def get_forecast(self, city: str, days: int) -> List[Dict]:
        """Make HTTP request to get forecast"""
        print(f"🌐 RemoteWeatherAPI: Making HTTP request to {self.api_url}")
        print(f"   Endpoint: /forecast/{city}?days={days}")
        
        # Simulate network delay
        time.sleep(0.8)
        
        # Simulate API response
        forecast = []
        for i in range(days):
            forecast.append({
                'day': i + 1,
                'temperature': 20 + i,
                'condition': 'Partly Cloudy',
                'precipitation': 20
            })
        
        return forecast

# ============ PROXY (Remote Proxy) ============

class WeatherServiceProxy(WeatherService):
    """
    Remote Proxy that:
    1. Handles network errors gracefully
    2. Adds caching
    3. Adds retry logic
    4. Validates input
    5. Transforms data format
    """
    
    def __init__(self, api_key: str):
        self._remote_api = RemoteWeatherAPI(api_key)
        self._cache: Dict[str, Dict] = {}
        self._max_retries = 3
    
    def _validate_city(self, city: str) -> bool:
        """Validate city name"""
        if not city or len(city) < 2:
            print("❌ Validation failed: Invalid city name")
            return False
        return True
    
    def _make_request_with_retry(self, func, *args, **kwargs):
        """Make request with retry logic"""
        for attempt in range(self._max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f"⚠️  Attempt {attempt + 1} failed: {e}")
                if attempt == self._max_retries - 1:
                    raise
                time.sleep(1)  # Wait before retry
    
    def get_current_weather(self, city: str) -> Dict:
        """
        Get current weather with:
        - Input validation
        - Caching
        - Error handling
        - Retry logic
        """
        print(f"\n🔄 WeatherServiceProxy: get_current_weather('{city}')")
        
        # Validate input
        if not self._validate_city(city):
            raise ValueError(f"Invalid city: {city}")
        
        # Check cache
        cache_key = f"current_{city}"
        if cache_key in self._cache:
            print("💾 Using cached data")
            return self._cache[cache_key]
        
        # Make request with retry
        try:
            print("🌐 Fetching from remote API...")
            data = self._make_request_with_retry(
                self._remote_api.get_current_weather,
                city
            )
            
            # Transform data (add extra fields, convert units, etc.)
            data['temperature_f'] = data['temperature'] * 9/5 + 32
            data['fetched_via'] = 'proxy'
            
            # Cache result
            self._cache[cache_key] = data
            
            print("✅ Data fetched and cached successfully")
            return data
            
        except Exception as e:
            print(f"❌ Error fetching weather: {e}")
            # Return fallback data
            return {
                'city': city,
                'error': 'Service unavailable',
                'message': 'Using fallback data'
            }
    
    def get_forecast(self, city: str, days: int) -> List[Dict]:
        """
        Get forecast with validation and error handling
        """
        print(f"\n🔄 WeatherServiceProxy: get_forecast('{city}', {days} days)")
        
        # Validate input
        if not self._validate_city(city):
            raise ValueError(f"Invalid city: {city}")
        
        if days < 1 or days > 7:
            print("⚠️  Days out of range, adjusting to valid range")
            days = max(1, min(7, days))
        
        # Check cache
        cache_key = f"forecast_{city}_{days}"
        if cache_key in self._cache:
            print("💾 Using cached forecast")
            return self._cache[cache_key]
        
        # Make request
        try:
            print("🌐 Fetching forecast from remote API...")
            data = self._make_request_with_retry(
                self._remote_api.get_forecast,
                city,
                days
            )
            
            # Transform data (add Fahrenheit)
            for day in data:
                day['temperature_f'] = day['temperature'] * 9/5 + 32
            
            # Cache result
            self._cache[cache_key] = data
            
            print("✅ Forecast fetched and cached successfully")
            return data
            
        except Exception as e:
            print(f"❌ Error fetching forecast: {e}")
            return []

# ============ USAGE ============

print("="*70)
print("REMOTE PROXY - API WRAPPER")
print("="*70)

# Create proxy
weather_service = WeatherServiceProxy(api_key="demo-api-key-123")

# Get current weather
print("\n### Getting current weather ###")
weather1 = weather_service.get_current_weather("New York")
print(f"\n📍 Weather in {weather1['city']}:")
print(f"   🌡️  Temperature: {weather1['temperature']}°C ({weather1['temperature_f']:.1f}°F)")
print(f"   ☁️  Condition: {weather1['condition']}")
print(f"   💧 Humidity: {weather1['humidity']}%")

# Get weather again (from cache)
print("\n### Getting weather again (cached) ###")
weather2 = weather_service.get_current_weather("New York")
print(f"\n📍 Weather in {weather2['city']}: {weather2['condition']}")

# Get forecast
print("\n### Getting 5-day forecast ###")
forecast = weather_service.get_forecast("London", 5)
print(f"\n📅 5-Day Forecast for London:")
for day in forecast:
    print(f"   Day {day['day']}: {day['temperature']}°C ({day['temperature_f']:.1f}°F) - {day['condition']}")

# Invalid input
print("\n### Testing input validation ###")
try:
    weather_service.get_current_weather("")
except ValueError as e:
    print(f"Caught error: {e}")

# Out of range days
print("\n### Testing range validation ###")
forecast_adjusted = weather_service.get_forecast("Paris", 10)  # Will be adjusted to 7
```

---

## Common Pitfalls

### ❌ Pitfall 1: Proxy Has Different Interface

```python
# BAD - Proxy has different interface than real object
class BadProxy:
    def __init__(self, real_obj):
        self.real_obj = real_obj
    
    def do_something_different(self):  # Different method name!
        return self.real_obj.do_something()

# GOOD - Same interface
class GoodProxy(Subject):
    def __init__(self, real_obj: Subject):
        self.real_obj = real_obj
    
    def do_something(self):  # Same method name
        return self.real_obj.do_something()
```

---

### ❌ Pitfall 2: Not Handling Errors in Remote Proxy

```python
# BAD - No error handling
class BadRemoteProxy:
    def get_data(self):
        return self.remote_api.fetch()  # What if network fails?

# GOOD - Proper error handling
class GoodRemoteProxy:
    def get_data(self):
        try:
            return self.remote_api.fetch()
        except NetworkError:
            # Return cached data or fallback
            return self._get_cached_or_fallback()
```

---

### ❌ Pitfall 3: Cache Never Expires

```python
# BAD - Cache grows indefinitely
class BadCachingProxy:
    def __init__(self):
        self.cache = {}  # Never cleared!
    
    def get(self, key):
        if key in self.cache:
            return self.cache[key]
        # ... fetch and cache

# GOOD - Cache with expiration and limits
class GoodCachingProxy:
    def __init__(self, max_size=100, ttl=300):
        self.cache = {}
        self.max_size = max_size
        self.ttl = ttl
    
    def get(self, key):
        # Check expiration, limit size, etc.
        pass
```

---

### ❌ Pitfall 4: Circular References in Virtual Proxy

```python
# BAD - Can cause issues
class BadVirtualProxy:
    def __init__(self, factory):
        self.real_obj = factory()  # Created immediately!

# GOOD - True lazy initialization
class GoodVirtualProxy:
    def __init__(self, factory):
        self.factory = factory
        self._real_obj = None
    
    def operation(self):
        if self._real_obj is None:
            self._real_obj = self.factory()  # Created on demand
        return self._real_obj.operation()
```

---

## Best Practices

### ✅ 1. Keep Proxy Transparent

```python
# Client shouldn't know it's using a proxy
def client_code(service: WeatherService):
    # Works with both proxy and real service
    weather = service.get_current_weather("Paris")
```

---

### ✅ 2. Document Proxy Behavior

```python
class CachingProxy:
    """
    Caching proxy for DataService.
    
    Behavior:
    - Caches results for 60 seconds (configurable)
    - Thread-safe caching
    - Automatic cache invalidation
    - Cache statistics available via get_stats()
    
    Note: First call will be slow (cache miss),
    subsequent calls will be fast (cache hit).
    """
    pass
```

---

### ✅ 3. Provide Cache Control Methods

```python
class CachingProxy:
    def get(self, key):
        # ... normal get
        pass
    
    def clear_cache(self):
        """Clear all cached data"""
        pass
    
    def invalidate(self, key):
        """Invalidate specific cache entry"""
        pass
    
    def get_stats(self):
        """Get cache statistics"""
        pass
```

---

### ✅ 4. Handle Resource Cleanup

```python
class ResourceProxy:
    def __init__(self):
        self._real_obj = None
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._real_obj:
            self._real_obj.close()

# Usage with context manager
with ResourceProxy() as proxy:
    proxy.do_something()
# Automatically cleaned up
```

---

### ✅ 5. Use Proxy for Cross-Cutting Concerns

```python
class LoggingProxy:
    """Add logging to any service"""
    
    def __init__(self, service, logger):
        self._service = service
        self._logger = logger
    
    def __getattr__(self, name):
        """Intercept all method calls"""
        attr = getattr(self._service, name)
        
        if callable(attr):
            def wrapper(*args, **kwargs):
                self._logger.info(f"Calling {name}")
                result = attr(*args, **kwargs)
                self._logger.info(f"Finished {name}")
                return result
            return wrapper
        
        return attr
```

---

## Summary

| Aspect           | Details                                                   |
|------------------|-----------------------------------------------------------|
| **Purpose**      | Control access to another object                          |
| **Use When**     | Lazy loading, access control, caching, remote objects     |
| **Avoid When**   | No control needed, performance critical, over-engineering |
| **Key Benefit**  | Adds functionality without changing real object           |
| **Common Types** | Virtual, Protection, Remote, Caching, Logging             |

---

## Proxy Types Summary

| Type                | Purpose                    | Example                             |
|---------------------|----------------------------|-------------------------------------|
| **Virtual**         | Lazy initialization        | Loading large images on demand      |
| **Protection**      | Access control             | Permission checks before operations |
| **Remote**          | Represent remote object    | API wrapper, RPC                    |
| **Caching**         | Cache expensive operations | Database query caching              |
| **Logging**         | Log operations             | Audit trails                        |
| **Smart Reference** | Additional actions         | Reference counting, locking         |

---

## Pattern Comparison

| Pattern       | Interface           | Purpose                           |
|---------------|---------------------|-----------------------------------|
| **Proxy**     | Same as real object | Control access, add functionality |
| **Decorator** | Same, but wraps     | Add responsibilities dynamically  |
| **Adapter**   | Different           | Convert interface                 |
| **Facade**    | Simpler             | Simplify complex system           |
