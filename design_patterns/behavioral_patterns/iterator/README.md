# 🧠 Behavioral Pattern #3: **Iterator Pattern**

---

## 📋 Table of Contents
- [What is Iterator Pattern?](#-what-is-iterator-pattern)
  - [Key Characteristics](#-key-characteristics)
  - [The Problem It Solves](#-the-problem-it-solves)
  - [Real-World Analogy](#-real-world-analogy)
  - [Visual Representation](#-visual-representation)
- [When to Use](#-when-to-use)
- [When NOT to Use](#-when-not-to-use)
- [Basic Implementation](#-basic-implementation)
- [Real-World Examples](#-real-world-examples)
  - [Example 1: File System Tree Iterator](#example-1-file-system-tree-iterator)
  - [Example 2: Paginated API Iterator](#example-2-paginated-api-iterator)
  - [Example 3: Social Media Feed Iterator](#example-3-social-media-feed-iterator)
- [Common Pitfalls](#-common-pitfalls)
- [Best Practices](#-best-practices)
- [Summary](#-summary)
- [✅ Iterator Pattern Checklist](#-iterator-pattern-checklist)
- [Key Takeaways](#-key-takeaways)

---

## 🔷 What is Iterator Pattern?

**Iterator Pattern** is a behavioral design pattern that provides a way to **sequentially access elements of a collection without exposing its underlying structure**. The client just says "give me the next item" — it never needs to know if the data is a list, tree, graph, database, or API response.

---

### 🔑 Key Characteristics

| Characteristic            | Description                                          |
|---------------------------|------------------------------------------------------|
| **Abstraction**           | Hides how a collection is structured internally      |
| **Uniform Interface**     | Same `__iter__` / `__next__` for any collection      |
| **Single Responsibility** | Traversal logic lives in iterator, not collection    |
| **Multiple Iterators**    | Same collection can have many simultaneous iterators |
| **Lazy Evaluation**       | Elements can be produced on demand (generators)      |

---

### 🔥 The Problem It Solves

Without Iterator Pattern, clients must know the internal structure of every collection:

```python
# ❌ WITHOUT Iterator — client is coupled to internal structure
class WordCollection:
    def __init__(self):
        self.words = []        # internal detail exposed!

collection = WordCollection()

# Client must know it's a list and index into it manually
for i in range(len(collection.words)):
    print(collection.words[i])  # tightly coupled to list internals

# Now imagine switching to a tree or database — ALL client code breaks!
```

With Iterator Pattern:

```python
# ✅ WITH Iterator — client knows nothing about internals
for word in collection:       # works whether it's a list, tree, or API
    print(word)
```

---

### 🌍 Real-World Analogy

Think of a **TV remote**:

```
You (Client) → Remote (Iterator) → Cable Box (Collection)
```

- You press **Next** to go to the next channel
- You don't know how channels are stored or indexed internally
- You can have multiple remotes (iterators) pointed at the same cable box
- The channels (collection) don't change — only the traversal cursor moves

---

### 🖼️ Visual Representation

```
┌────────────────────────────────────────┐
│              Collection                │
│  ┌───┐  ┌───┐  ┌───┐  ┌───┐  ┌───┐     │
│  │ A │  │ B │  │ C │  │ D │  │ E │     │
│  └───┘  └───┘  └───┘  └───┘  └───┘     │
└──────────────────────┬─────────────────┘
                       │ creates
                       ▼
              ┌─────────────────┐
              │    Iterator     │
              │  cursor = 0     │
              │  __next__()     │──► A, B, C, D, E
              │  __iter__()     │
              └─────────────────┘
                       ▲
                       │ calls next()
              ┌─────────────────┐
              │     Client      │
              │  for item in .. │
              └─────────────────┘
```

---

### 🔀 Participants

| Role                   | Responsibility                                 |
|------------------------|------------------------------------------------|
| **Iterator**           | Interface: `__iter__()`, `__next__()`          |
| **ConcreteIterator**   | Tracks current position, implements traversal  |
| **Iterable**           | Interface: `__iter__()` returns an iterator    |
| **ConcreteCollection** | Stores elements, creates its own iterator      |
| **Client**             | Uses iterator via `for` loop or `next()` calls |

---

## ✅ When to Use

| Scenario                                                       | Why It Fits                      |
|----------------------------------------------------------------|----------------------------------|
| Collection has **complex internal structure** (tree, graph)    | Hide traversal complexity        |
| Need **multiple traversal strategies** (BFS, DFS, reverse)     | Each is a separate iterator      |
| Need to **iterate lazily** over large/infinite data            | Generator-based iterators        |
| Want a **uniform interface** across different collection types | Same `for` loop for all          |
| Need **simultaneous independent iterators** on same collection | Each iterator has its own cursor |

---

## ❌ When NOT to Use

- When collection is **simple** (plain list, dict) — Python already provides excellent built-in iterators
- When you only ever need **one traversal order** and the collection is small — adds unnecessary abstraction
- When **random access** (`collection[5]`) is the primary use case

---

## 🏗️ Basic Implementation

### Classic Structure

```python
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any

# ─────────────────────────────────────────
# Iterator Interface
# ─────────────────────────────────────────
class Iterator(ABC):
    @abstractmethod
    def __next__(self) -> Any:
        pass

    @abstractmethod
    def __iter__(self) -> Iterator:
        pass

    @abstractmethod
    def has_next(self) -> bool:
        pass


# ─────────────────────────────────────────
# Iterable Interface
# ─────────────────────────────────────────
class IterableCollection(ABC):
    @abstractmethod
    def __iter__(self) -> Iterator:
        pass


# ─────────────────────────────────────────
# Concrete Collection
# ─────────────────────────────────────────
class NumberCollection(IterableCollection):
    def __init__(self):
        self._items: list[int] = []

    def add(self, item: int) -> None:
        self._items.append(item)

    def __iter__(self) -> Iterator:
        return ForwardIterator(self._items)

    def reversed_iterator(self) -> Iterator:
        return ReverseIterator(self._items)


# ─────────────────────────────────────────
# Concrete Iterators
# ─────────────────────────────────────────
class ForwardIterator(Iterator):
    def __init__(self, items: list[int]):
        self._items  = items
        self._cursor = 0

    def __iter__(self) -> ForwardIterator:
        return self

    def __next__(self) -> int:
        if not self.has_next():
            raise StopIteration
        item = self._items[self._cursor]
        self._cursor += 1
        return item

    def has_next(self) -> bool:
        return self._cursor < len(self._items)


class ReverseIterator(Iterator):
    def __init__(self, items: list[int]):
        self._items  = items
        self._cursor = len(items) - 1

    def __iter__(self) -> ReverseIterator:
        return self

    def __next__(self) -> int:
        if not self.has_next():
            raise StopIteration
        item = self._items[self._cursor]
        self._cursor -= 1
        return item

    def has_next(self) -> bool:
        return self._cursor >= 0


# ─────────────────────────────────────────
# Client Code
# ─────────────────────────────────────────
nums = NumberCollection()
for n in [10, 20, 30, 40, 50]:
    nums.add(n)

print("Forward:")
for n in nums:              # uses __iter__ → ForwardIterator
    print(f"  {n}")
# 10 20 30 40 50

print("\nReverse:")
for n in nums.reversed_iterator():
    print(f"  {n}")
# 50 40 30 20 10
```

---

## 🌍 Real-World Examples

### Example 1: File System Tree Iterator

```python
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Iterator as TypingIterator
from collections import deque

# ─────────────────────────────────────────
# Tree Node
# ─────────────────────────────────────────
@dataclass
class FileNode:
    name:     str
    is_dir:   bool = False
    children: list[FileNode] = field(default_factory=list)
    size_kb:  int  = 0

    def add(self, node: FileNode) -> FileNode:
        self.children.append(node)
        return node

    def __repr__(self):
        icon = "📁" if self.is_dir else "📄"
        return f"{icon} {self.name}"


# ─────────────────────────────────────────
# DFS Iterator — depth-first (pre-order)
# ─────────────────────────────────────────
class DFSIterator:
    """Visits: parent → children → grandchildren (depth-first)."""

    def __init__(self, root: FileNode):
        self._stack = [root]

    def __iter__(self) -> DFSIterator:
        return self

    def __next__(self) -> FileNode:
        if not self._stack:
            raise StopIteration
        node = self._stack.pop()
        # Push children in reverse so left-most is visited first
        for child in reversed(node.children):
            self._stack.append(child)
        return node


# ─────────────────────────────────────────
# BFS Iterator — breadth-first (level-order)
# ─────────────────────────────────────────
class BFSIterator:
    """Visits: all items at depth 1 → depth 2 → depth 3 ..."""

    def __init__(self, root: FileNode):
        self._queue: deque[FileNode] = deque([root])

    def __iter__(self) -> BFSIterator:
        return self

    def __next__(self) -> FileNode:
        if not self._queue:
            raise StopIteration
        node = self._queue.popleft()
        for child in node.children:
            self._queue.append(child)
        return node


# ─────────────────────────────────────────
# Files-Only Iterator — filters directories
# ─────────────────────────────────────────
class FilesOnlyIterator:
    """Yields only file nodes (not directories), using DFS underneath."""

    def __init__(self, root: FileNode):
        self._dfs = DFSIterator(root)

    def __iter__(self) -> FilesOnlyIterator:
        return self

    def __next__(self) -> FileNode:
        while True:
            node = next(self._dfs)  # raises StopIteration naturally
            if not node.is_dir:
                return node


# ─────────────────────────────────────────
# File System (Iterable Collection)
# ─────────────────────────────────────────
class FileSystem:
    def __init__(self, root: FileNode):
        self._root = root

    def __iter__(self) -> DFSIterator:
        return DFSIterator(self._root)  # default: DFS

    def bfs(self) -> BFSIterator:
        return BFSIterator(self._root)

    def files_only(self) -> FilesOnlyIterator:
        return FilesOnlyIterator(self._root)


# ─────────────────────────────────────────
# Build a Sample File Tree
# ─────────────────────────────────────────
#   /project
#   ├── src/
#   │   ├── main.py
#   │   └── utils.py
#   ├── tests/
#   │   └── test_main.py
#   └── README.md

root = FileNode("project", is_dir=True)
src  = root.add(FileNode("src",   is_dir=True))
src.add(FileNode("main.py",       size_kb=12))
src.add(FileNode("utils.py",      size_kb=5))
tests = root.add(FileNode("tests", is_dir=True))
tests.add(FileNode("test_main.py", size_kb=8))
root.add(FileNode("README.md",    size_kb=2))

fs = FileSystem(root)

print("=== DFS (default) ===")
for node in fs:
    print(f"  {node}")

print("\n=== BFS (level-order) ===")
for node in fs.bfs():
    print(f"  {node}")

print("\n=== Files Only ===")
total = 0
for f in fs.files_only():
    print(f"  {f}  ({f.size_kb} KB)")
    total += f.size_kb
print(f"  Total: {total} KB")

# === DFS ===
#   📁 project
#   📁 src
#   📄 main.py
#   📄 utils.py
#   📁 tests
#   📄 test_main.py
#   📄 README.md

# === BFS ===
#   📁 project
#   📁 src
#   📁 tests
#   📄 README.md
#   📄 main.py
#   📄 utils.py
#   📄 test_main.py

# === Files Only ===
#   📄 main.py      (12 KB)
#   📄 utils.py     (5 KB)
#   📄 test_main.py (8 KB)
#   📄 README.md    (2 KB)
#   Total: 27 KB
```

---

### Example 2: Paginated API Iterator

```python
from __future__ import annotations
from dataclasses import dataclass
from typing import Any
import math

# ─────────────────────────────────────────
# Simulated API Client (pretend HTTP calls)
# ─────────────────────────────────────────
@dataclass
class User:
    id:    int
    name:  str
    email: str

    def __repr__(self):
        return f"User({self.id}: {self.name})"


class FakeUsersAPI:
    """Simulates a paginated REST API."""

    _ALL_USERS = [
        User(i, f"User_{i}", f"user{i}@example.com")
        for i in range(1, 26)   # 25 users total
    ]

    def fetch_page(self, page: int, page_size: int) -> dict[str, Any]:
        start = (page - 1) * page_size
        end   = start + page_size
        items = self._ALL_USERS[start:end]

        return {
            "data":        items,
            "page":        page,
            "page_size":   page_size,
            "total":       len(self._ALL_USERS),
            "total_pages": math.ceil(len(self._ALL_USERS) / page_size),
        }


# ─────────────────────────────────────────
# Paginated Iterator
# ─────────────────────────────────────────
class PaginatedIterator:
    """
    Transparently handles pagination.
    Client just calls next() — never worries about pages.
    """

    def __init__(self, api: FakeUsersAPI, page_size: int = 5):
        self._api        = api
        self._page_size  = page_size
        self._page       = 1
        self._buffer:    list[User] = []
        self._exhausted  = False
        self._total_fetched = 0

    def __iter__(self) -> PaginatedIterator:
        return self

    def __next__(self) -> User:
        # Buffer empty → fetch next page
        if not self._buffer:
            if self._exhausted:
                raise StopIteration
            self._fetch_page()

        if not self._buffer:
            raise StopIteration

        return self._buffer.pop(0)

    def _fetch_page(self) -> None:
        print(f"  🌐 Fetching page {self._page} (size={self._page_size})...")
        response = self._api.fetch_page(self._page, self._page_size)

        self._buffer = list(response["data"])
        self._page  += 1

        if self._page > response["total_pages"]:
            self._exhausted = True


# ─────────────────────────────────────────
# Filtered Iterator (wraps any iterator)
# ─────────────────────────────────────────
class FilteredIterator:
    """Wraps any iterator and applies a filter predicate."""

    def __init__(self, iterator, predicate):
        self._iterator  = iterator
        self._predicate = predicate

    def __iter__(self) -> FilteredIterator:
        return self

    def __next__(self) -> Any:
        while True:
            item = next(self._iterator)     # propagates StopIteration
            if self._predicate(item):
                return item


# ─────────────────────────────────────────
# Client Code
# ─────────────────────────────────────────
api = FakeUsersAPI()

print("=== Iterate ALL users (pagination transparent) ===\n")
for user in PaginatedIterator(api, page_size=8):
    print(f"  {user}")

print("\n=== Only users with even IDs ===\n")
base_iter     = PaginatedIterator(api, page_size=5)
filtered_iter = FilteredIterator(base_iter, lambda u: u.id % 2 == 0)

for user in filtered_iter:
    print(f"  {user}")

# === Iterate ALL ===
#   🌐 Fetching page 1 (size=8)...
#   User(1: User_1)
#   User(2: User_2)
#   ...
#   🌐 Fetching page 2 (size=8)...
#   ...
```

---

### Example 3: Social Media Feed Iterator

```python
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Iterator as TypingIterator
from datetime import datetime, timedelta
from enum import Enum
import random

class FeedAlgorithm(Enum):
    CHRONOLOGICAL = "chronological"
    RANKED        = "ranked"
    RANDOM        = "random"

@dataclass
class Post:
    id:         int
    author:     str
    content:    str
    likes:      int
    created_at: datetime

    def __repr__(self):
        return (f"[{self.created_at.strftime('%H:%M')}] "
                f"@{self.author}: {self.content[:40]}... "
                f"❤️  {self.likes}")


# ─────────────────────────────────────────
# Iterators — different feed algorithms
# ─────────────────────────────────────────
class ChronologicalIterator:
    """Newest posts first."""

    def __init__(self, posts: list[Post]):
        self._posts  = sorted(posts, key=lambda p: p.created_at, reverse=True)
        self._cursor = 0

    def __iter__(self): return self

    def __next__(self) -> Post:
        if self._cursor >= len(self._posts):
            raise StopIteration
        post = self._posts[self._cursor]
        self._cursor += 1
        return post


class RankedIterator:
    """Highest engagement (likes) first — social media algorithm."""

    def __init__(self, posts: list[Post]):
        self._posts  = sorted(posts, key=lambda p: p.likes, reverse=True)
        self._cursor = 0

    def __iter__(self): return self

    def __next__(self) -> Post:
        if self._cursor >= len(self._posts):
            raise StopIteration
        post = self._posts[self._cursor]
        self._cursor += 1
        return post


class InfiniteScrollIterator:
    """
    Simulates infinite scroll — generates synthetic posts on demand.
    Never raises StopIteration (truly infinite).
    Use with islice() to limit.
    """

    def __init__(self, seed_posts: list[Post]):
        self._seed   = seed_posts
        self._seen   = 0

    def __iter__(self): return self

    def __next__(self) -> Post:
        # Cycle through seed posts, tweaking them to simulate new content
        base = self._seed[self._seen % len(self._seed)]
        self._seen += 1
        return Post(
            id         = 10000 + self._seen,
            author     = base.author,
            content    = f"[Generated #{self._seen}] {base.content}",
            likes      = random.randint(0, 500),
            created_at = datetime.now() - timedelta(minutes=self._seen),
        )


# ─────────────────────────────────────────
# Collection
# ─────────────────────────────────────────
class SocialFeed:
    def __init__(self, algorithm: FeedAlgorithm = FeedAlgorithm.CHRONOLOGICAL):
        self._posts:     list[Post]    = []
        self._algorithm: FeedAlgorithm = algorithm

    def add_post(self, post: Post) -> None:
        self._posts.append(post)

    def set_algorithm(self, algo: FeedAlgorithm) -> None:
        self._algorithm = algo
        print(f"  🔄 Switched to {algo.value} feed")

    def __iter__(self):
        if self._algorithm == FeedAlgorithm.CHRONOLOGICAL:
            return ChronologicalIterator(self._posts)
        elif self._algorithm == FeedAlgorithm.RANKED:
            return RankedIterator(self._posts)
        elif self._algorithm == FeedAlgorithm.RANDOM:
            shuffled = random.sample(self._posts, len(self._posts))
            return iter(shuffled)

    def infinite_scroll(self) -> InfiniteScrollIterator:
        return InfiniteScrollIterator(self._posts)


# ─────────────────────────────────────────
# Client
# ─────────────────────────────────────────
from itertools import islice

now  = datetime.now()
feed = SocialFeed()

posts_data = [
    ("alice",   "Just shipped a new feature!",          342, now - timedelta(hours=1)),
    ("bob",     "Hot take: tabs > spaces",               891, now - timedelta(hours=3)),
    ("carol",   "Beautiful sunset today",                 56, now - timedelta(minutes=20)),
    ("dave",    "New blog post on design patterns",      210, now - timedelta(hours=2)),
    ("eve",     "Coffee is a programming language",      654, now - timedelta(minutes=45)),
]

for i, (author, content, likes, ts) in enumerate(posts_data, 1):
    feed.add_post(Post(i, author, content, likes, ts))

print("=== Chronological Feed ===")
for post in feed:
    print(f"  {post}")

feed.set_algorithm(FeedAlgorithm.RANKED)
print("\n=== Ranked Feed (by likes) ===")
for post in feed:
    print(f"  {post}")

print("\n=== Infinite Scroll (first 6 items) ===")
for post in islice(feed.infinite_scroll(), 6):
    print(f"  {post}")
```

---

## ⚠️ Common Pitfalls

### ❌ Pitfall 1: Modifying Collection During Iteration

```python
# ❌ WRONG — modifying while iterating causes skipped items or errors
items = [1, 2, 3, 4, 5]
for item in items:
    if item % 2 == 0:
        items.remove(item)   # 💥 skips items silently!

# ✅ CORRECT — iterate over a copy, or collect then remove
for item in list(items):     # iterate copy
    if item % 2 == 0:
        items.remove(item)

# ✅ ALSO CORRECT — build a new list
items = [item for item in items if item % 2 != 0]
```

### ❌ Pitfall 2: Stateful Iterator Shared Across Threads

```python
# ❌ WRONG — single iterator instance shared between threads
shared_iter = iter(large_collection)

# Thread 1 and Thread 2 both call next(shared_iter) — race condition!

# ✅ CORRECT — each thread gets its own iterator
def worker(collection):
    for item in collection:   # each call to __iter__ creates a new iterator
        process(item)
```

### ❌ Pitfall 3: Not Implementing `__iter__` on the Iterator Itself

```python
# ❌ WRONG — iterator not usable in for loops
class BadIterator:
    def __next__(self):
        ...
    # Missing __iter__! Can't use in for loops or with itertools

# ✅ CORRECT — iterator must return itself from __iter__
class GoodIterator:
    def __iter__(self):
        return self          # iterators must return self

    def __next__(self):
        ...
```

### ❌ Pitfall 4: Reusing an Exhausted Iterator

```python
# ❌ WRONG — iterators are stateful; once exhausted, they stay empty
my_iter = iter([1, 2, 3])
print(list(my_iter))   # [1, 2, 3]
print(list(my_iter))   # [] ← already exhausted!

# ✅ CORRECT — create a new iterator each time
data = [1, 2, 3]
print(list(iter(data)))   # [1, 2, 3]
print(list(iter(data)))   # [1, 2, 3] ← fresh iterator
```

---

## ✅ Best Practices

### 1. Use Python Generators for Lazy Iterators

```python
# ✅ Generator-based iterator — clean, lazy, memory-efficient
class FileSystem:
    def __iter__(self):
        yield from self._dfs(self._root)   # lazy depth-first traversal

    def _dfs(self, node: FileNode):
        yield node
        for child in node.children:
            yield from self._dfs(child)    # recursive generator
```

### 2. Compose Iterators with `itertools`

```python
import itertools

feed      = SocialFeed()
paginated = PaginatedIterator(api)

# Chain multiple iterators seamlessly
combined = itertools.chain(iter(feed), paginated)

# Take only first 10
top_10   = itertools.islice(combined, 10)

# Filter on the fly
filtered = filter(lambda x: x.likes > 100, top_10)

for item in filtered:
    print(item)
```

### 3. Separate Iterator from Collection

```python
# ✅ Collection creates iterators but doesn't inherit from them
class MyCollection:
    def __iter__(self):
        return MyIterator(self._data)   # factory method


class MyIterator:
    def __init__(self, data):
        self._data   = data
        self._cursor = 0

    def __iter__(self): return self
    def __next__(self): ...
```

### 4. Make Collections Immutable During Iteration

```python
class SafeCollection:
    def __iter__(self):
        snapshot = list(self._items)    # snapshot at iteration start
        return iter(snapshot)           # iterate over the snapshot
```

---

## 📊 Summary

| Aspect             | Detail                                                      |
|--------------------|-------------------------------------------------------------|
| **Type**           | Behavioral                                                  |
| **Intent**         | Access collection elements without exposing internals       |
| **Key Methods**    | `__iter__()`, `__next__()`, `StopIteration`                 |
| **Python Native**  | `for` loops, `iter()`, `next()`, generators, `itertools`    |
| **Real-world Use** | File traversal, pagination, feed algorithms, lazy pipelines |

---

## ✅ Iterator Pattern Checklist


- Does __iter__() return an iterator object (often self)?
- Does __next__() raise StopIteration when exhausted?
- Is the iterator separate from the collection?
- Does the collection create a fresh iterator on each __iter__() call?
- Are generators used where lazy evaluation is beneficial?
- Is the collection protected from modification during iteration?
- Can multiple independent iterators exist on the same collection?


---

## 💡 Key Takeaways

1. **Hides internal structure** — client never knows if it's a list, tree, or API
2. **Python's `for` loop is built on this pattern** — `__iter__` + `__next__` + `StopIteration`
3. **Generators are the Pythonic iterator** — `yield` replaces boilerplate iterator classes
4. **Composable with `itertools`** — chain, filter, slice any iterator uniformly
5. **Stateful by design** — each iterator independently tracks its own cursor position
