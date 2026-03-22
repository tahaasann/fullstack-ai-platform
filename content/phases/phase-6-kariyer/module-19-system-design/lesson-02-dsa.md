---
title: "Data Structures & Algorithms"
id: mod-19-system-design/lesson-02
estimated_minutes: 150
order: 2
tags: [dsa, algorithms, data-structures, big-o, interview, python]
prerequisites: [mod-19-system-design/lesson-01]
---

# Data Structures & Algorithms

Coding interview'larin temeli DSA'dir. Bu derste interview'larda en çok karsilasan data structure'lar ve algorithm'lari Python ile ogreneceksin.

:::ai-guidance
## Bu Derste AI ile Öğren

**Önerilen Model:** Claude Opus 4.6 (derin anlayis için) veya Sonnet 4.5 (hızlı sorular için)

### Prompt Örnekleri

**1. Derinlemesine Anla:**
> "Big-O notasyonunu O(1), O(log n), O(n), O(n log n), O(n^2) ve O(2^n) için gerçek algoritma örnekleriyle açıkla. Hash table'in O(1) lookup'i nasil başarıyor? Binary search neden O(log n)? Time complexity ve space complexity arasindaki trade-off'u örneklerle göster."

**2. Pratik Uygulama:**
> "LeetCode'un en sik sorulan 5 sorusunu (Two Sum, Valid Parentheses, Merge Two Sorted Lists, Best Time to Buy/Sell Stock, Maximum Subarray) coz. Her soru için brute force ve optimal çözümü yaz, Big-O analizini yap ve hangi veri yapısı/algoritma pattern'inin kullanıldığını açıkla (hash map, stack, two pointer, sliding window, dynamic programming)."
> Takip: "Şimdi her çözüm için edge case'leri belirle ve test case'lerini yaz. Mülakatta bu soruyu nasil anlatacagini 5 dakikalik bir sunumla göster."

**3. Mukemmellik Için:**
> "Graph algoritmalari (BFS, DFS, Dijkstra, topological sort) gerçek dunyada nasil kullanılır? Sosyal ag öneri sistemi (BFS), dependency resolution (topological sort), navigasyon (Dijkstra) ve web crawler (DFS) örnekleriyle açıkla. Her algoritmanin time/space complexity'sini ve implementation detaylarini göster."

### Pair Programming Ipucu
Algoritma sorusu çözerken AI'a çözümünü göster ve sor: "Bu cozumun time ve space complexity'si ne? Daha optimal bir çözüm var mi? Edge case'leri kaçırmış miyim? Mülakatta bu çözümü nasil sunmalıyım?"
:::

:::must-note
DEFTERINE YAZ - DSA Kritik Noktalar:
1. **Big-O Sirasi**: O(1) < O(log n) < O(n) < O(n log n) < O(n^2) < O(2^n) < O(n!) - bunu ezberle
2. **Hash Table**: O(1) lookup - interview'larin %40'inda kullanılır
3. **Two Pointers / Sliding Window**: Array problemlerinin çoğu bu iki pattern ile cozulur
4. **BFS = en kısa yol (unweighted), DFS = tüm yollari kesfetme** - graph/tree'de bu ayrimi bil
5. **Dynamic Programming**: "Overlapping subproblems + optimal substructure" gorursen DP düşün
:::

:::senior-learns
**Senior/CTO Bu Konuyu Nasil Öğrenir?**

Senior muhendisler DSA'yi ezbere değil, **pattern tanıma** ile ogrenirler:

1. Her problemi bir pattern'e map ederler (Sliding Window, Two Pointers, BFS/DFS, DP, Greedy)
2. **Neden bu data structure?** sorusunu sorarlar — ArrayList vs LinkedList trade-off'u gibi
3. Time/Space complexity'yi koda bakmadan tahmin ederler
4. Gerçek production'da hangi algoritmanin kullanıldığını bilirler (database index = B-Tree, routing = Dijkstra)
5. LeetCode'u "grind" etmek yerine, 15-20 core problemi derinlemesine anlarlar

**Karar Verme Sureci — Dogru Data Structure Secimi:**
- **Array vs LinkedList**: Array: O(1) random access, cache-friendly. LinkedList: O(1) insert/delete at known position. Trade-off: LinkedList her node icin ekstra pointer memory kullanir ve cache miss orani yuksektir. Production karari: %99 durumda array/dynamic array kullan. LinkedList sadece cok spesifik durumlarda (LRU cache gibi) deger.
- **HashMap vs TreeMap**: HashMap: O(1) average lookup. TreeMap: O(log n) ama sirali iterasyon mumkun. Trade-off: HashMap worst-case O(n) (hash collision), TreeMap her zaman O(log n) garanti. Siralama gerekmiyorsa HashMap, range query lazimsa TreeMap.
- **Queue vs Stack vs Deque**: Queue: FIFO (task processing, BFS). Stack: LIFO (undo, DFS). Deque: Her iki uctan islem (sliding window). Yanlis veri yapisi secimi complexity'yi degistirir.

**Anti-pattern Farkindaligi:**
- **Premature optimization**: n=100 icin O(n^2) = 10K islem, modern CPU icin microsecond. n=1M oluncaya kadar basit cozum yeterli.
- **LeetCode grind without understanding**: 500 problem cozmek ama pattern'leri gorememek. 15 core pattern ogrenip her problemi bu pattern'lere map etmek cok daha etkili.
- **Gercek dunya ve mulakat kopuklugu**: Mulakatta O(n log n) sort yazmak istenir ama production'da `array.sort()` kullanirsin. Senior farki: "neden sort built-in'i Tim Sort kullanir?" ve "ne zaman counting sort daha hizli?" sorularini cevaplayabilmek.

**Gercek Dunya Deneyimi:** Bir arama motoru projesinde autocomplete ozelligi yazdik. Ilk versiyon: her keystroke'ta 500K kelimeyi filtrele (O(n)). 200ms latency. Trie veri yapisina gecis: O(m) lookup. Latency 2ms'ye dustu. Compressed trie (radix tree) ile memory %70 azaldi. Ders: dogru veri yapisi secimi, algoritmik optimizasyondan cok daha etkili.

**Yaklaşım**: Her data structure için "bu hangi gerçek problem için var?" diye düşün.
:::

---

## 1. Big-O Notation

:::concept
### Zaman ve Alan Karmasikligi

Big-O, bir algoritmanin input buyudukce nasil davrandigini ifade eder.

```
n = input buyuklugu

O(1)        Constant    → Hash table lookup, array index
O(log n)    Logarithmic → Binary search, balanced BST
O(n)        Linear      → Array scan, linked list traverse
O(n log n)  Linearithmic→ Merge sort, heap sort
O(n²)       Quadratic   → Bubble sort, nested loops
O(2^n)      Exponential → Recursive fibonacci (naive)
O(n!)       Factorial   → Permutations, brute force TSP
```

**Görsel Karşılaştırma:**
```
n=10 icin islem sayisi:
O(1)        →  1
O(log n)    →  3.3
O(n)        →  10
O(n log n)  →  33
O(n²)       →  100
O(2^n)      →  1,024
O(n!)       →  3,628,800   ← FELAKET
```

**n=1,000,000 için:**
```
O(n)        →  1,000,000        (1 saniye)
O(n log n)  →  20,000,000       (20 saniye)
O(n²)       →  1,000,000,000,000 (31 YIL!)
```
:::

:::code
### Big-O Ornekleri

```python
# ============================================
# O(1) - Constant Time
# ============================================
def get_first(arr: list) -> int:
    """Array'in ilk elemani - input boyutu farketmez"""
    return arr[0] if arr else None

def hash_lookup(d: dict, key: str):
    """Dictionary lookup - amortized O(1)"""
    return d.get(key)


# ============================================
# O(log n) - Logarithmic Time
# ============================================
def binary_search(arr: list, target: int) -> int:
    """Sirali array'de binary search"""
    left, right = 0, len(arr) - 1

    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1  # bulunamadi

# Her adimda array yariya iner → O(log n)
# 1,000,000 elemanli array'de en fazla 20 adim!


# ============================================
# O(n) - Linear Time
# ============================================
def find_max(arr: list) -> int:
    """Tum array'i dolasmak zorundayiz"""
    max_val = float('-inf')
    for num in arr:
        max_val = max(max_val, num)
    return max_val


# ============================================
# O(n log n) - Linearithmic Time
# ============================================
def merge_sort(arr: list) -> list:
    """Merge sort - en iyi genel amacli siralama"""
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])

    return merge(left, right)

def merge(left: list, right: list) -> list:
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


# ============================================
# O(n²) - Quadratic Time
# ============================================
def has_duplicate_naive(arr: list) -> bool:
    """Her elemani digerlerle karsilastir"""
    n = len(arr)
    for i in range(n):            # O(n)
        for j in range(i + 1, n): # O(n)
            if arr[i] == arr[j]:
                return True
    return False

# Daha iyi cozum - O(n) with hash set:
def has_duplicate_optimized(arr: list) -> bool:
    seen = set()
    for num in arr:
        if num in seen:
            return True
        seen.add(num)
    return False
```
:::

:::tip
### Big-O Hesaplama Kurallari

1. **Sabitleri at**: O(2n) → O(n), O(100) → O(1)
2. **Düşük dereceleri at**: O(n² + n) → O(n²)
3. **Ic ice donguler carp**: for i * for j → O(n * m)
4. **Ardisik işlemleri topla**: O(n) + O(m) → O(n + m)
5. **Recursive**: T(n) = 2T(n/2) + O(n) → O(n log n) (Master Theorem)

**Interview'da**: "Bu çözüm O(n) time ve O(1) space" gibi her zaman belirt.
:::

---

## 2. Arrays & Strings

:::code
### Two Pointers Pattern

```python
# ============================================
# PROBLEM 1: Two Sum (LeetCode #1)
# Verilen array'de toplami target olan 2 sayi bul
# ============================================
def two_sum(nums: list[int], target: int) -> list[int]:
    """
    Hash map ile O(n) cozum.
    Her sayiyi gorurken, complement'ini (target - sayi) hash'te ara.
    """
    seen = {}  # sayi -> index

    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i

    return []

# Test
print(two_sum([2, 7, 11, 15], 9))  # [0, 1] (2+7=9)
print(two_sum([3, 2, 4], 6))       # [1, 2] (2+4=6)


# ============================================
# PROBLEM 2: Container With Most Water (LeetCode #11)
# Two pointers: iki uctan baslayip ortaya dogru
# ============================================
def max_area(height: list[int]) -> int:
    """
    Two pointers: Sol ve sag uctan basla.
    Her adimda kisa olan pointer'i ice dogru kaydir.
    O(n) time, O(1) space.
    """
    left, right = 0, len(height) - 1
    max_water = 0

    while left < right:
        # Su miktari = min yukseklik * genislik
        width = right - left
        h = min(height[left], height[right])
        max_water = max(max_water, width * h)

        # Kisa olan tarafi kaydir
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1

    return max_water


# ============================================
# PROBLEM 3: Valid Palindrome (LeetCode #125)
# ============================================
def is_palindrome(s: str) -> bool:
    """Two pointers ile palindrome kontrolu. O(n) time, O(1) space."""
    left, right = 0, len(s) - 1

    while left < right:
        # Alfanumerik olmayanlari atla
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1

        if s[left].lower() != s[right].lower():
            return False

        left += 1
        right -= 1

    return True

print(is_palindrome("A man, a plan, a canal: Panama"))  # True
```

```javascript
// JavaScript — Two Pointers Pattern

// Two Sum (sorted array)
function twoSum(nums, target) {
  const seen = new Map();
  for (let i = 0; i < nums.length; i++) {
    const complement = target - nums[i];
    if (seen.has(complement)) {
      return [seen.get(complement), i];
    }
    seen.set(nums[i], i);
  }
  return [];
}

console.log(twoSum([2, 7, 11, 15], 9)); // [0, 1]

// Container With Most Water
function maxArea(height) {
  let left = 0, right = height.length - 1;
  let maxWater = 0;

  while (left < right) {
    const width = right - left;
    const h = Math.min(height[left], height[right]);
    maxWater = Math.max(maxWater, width * h);

    if (height[left] < height[right]) left++;
    else right--;
  }
  return maxWater;
}

// Valid Palindrome
function isPalindrome(s) {
  const cleaned = s.toLowerCase().replace(/[^a-z0-9]/g, '');
  let left = 0, right = cleaned.length - 1;
  while (left < right) {
    if (cleaned[left] !== cleaned[right]) return false;
    left++;
    right--;
  }
  return true;
}

console.log(isPalindrome("A man, a plan, a canal: Panama")); // true
```
:::

:::code
### Sliding Window Pattern

```python
# ============================================
# PROBLEM 4: Maximum Subarray Sum of Size K
# Sabit boyutlu sliding window
# ============================================
def max_subarray_sum_k(arr: list[int], k: int) -> int:
    """
    K boyutundaki alt dizinin maksimum toplamini bul.
    Sliding window ile O(n) - her eleman sadece 1 kez eklenir/cikarilir.
    """
    if len(arr) < k:
        return 0

    # Ilk pencereyi hesapla
    window_sum = sum(arr[:k])
    max_sum = window_sum

    # Pencereyi kaydir
    for i in range(k, len(arr)):
        window_sum += arr[i]      # Yeni eleman ekle
        window_sum -= arr[i - k]  # Eski elemani cikar
        max_sum = max(max_sum, window_sum)

    return max_sum

print(max_subarray_sum_k([2, 1, 5, 1, 3, 2], 3))  # 9 (5+1+3)


# ============================================
# PROBLEM 5: Longest Substring Without Repeating (LeetCode #3)
# Degisken boyutlu sliding window
# ============================================
def length_of_longest_substring(s: str) -> int:
    """
    Tekrar eden karakter olmayan en uzun alt string.
    Sliding window + hash set ile O(n).
    """
    char_set = set()
    left = 0
    max_length = 0

    for right in range(len(s)):
        # Tekrar eden karakter varsa sol pointer'i kaydir
        while s[right] in char_set:
            char_set.remove(s[left])
            left += 1

        char_set.add(s[right])
        max_length = max(max_length, right - left + 1)

    return max_length

print(length_of_longest_substring("abcabcbb"))  # 3 ("abc")
print(length_of_longest_substring("bbbbb"))     # 1 ("b")
print(length_of_longest_substring("pwwkew"))    # 3 ("wke")


# ============================================
# PROBLEM 6: Minimum Window Substring (LeetCode #76)
# Hard - en klasik sliding window
# ============================================
from collections import Counter

def min_window(s: str, t: str) -> str:
    """
    s icinde t'nin tum karakterlerini iceren en kisa alt string.
    O(n) time.
    """
    if not s or not t:
        return ""

    need = Counter(t)       # Gereken karakterler
    have = {}               # Penceredeki karakterler
    formed = 0              # Kac unique karakter yeterli sayida var
    required = len(need)    # Kac unique karakter gerekiyor

    left = 0
    min_len = float('inf')
    min_start = 0

    for right in range(len(s)):
        char = s[right]
        have[char] = have.get(char, 0) + 1

        # Bu karakter yeterli sayida mi?
        if char in need and have[char] == need[char]:
            formed += 1

        # Tum karakterler tamam - pencereyi daralt
        while formed == required:
            # Minimum guncelle
            window_len = right - left + 1
            if window_len < min_len:
                min_len = window_len
                min_start = left

            # Sol eleman cikar
            left_char = s[left]
            have[left_char] -= 1
            if left_char in need and have[left_char] < need[left_char]:
                formed -= 1
            left += 1

    return "" if min_len == float('inf') else s[min_start:min_start + min_len]

print(min_window("ADOBECODEBANC", "ABC"))  # "BANC"
```

```javascript
// JavaScript — Sliding Window Pattern

// Maximum Subarray Sum of Size K
function maxSubarraySumK(arr, k) {
  if (arr.length < k) return 0;

  let windowSum = arr.slice(0, k).reduce((a, b) => a + b, 0);
  let maxSum = windowSum;

  for (let i = k; i < arr.length; i++) {
    windowSum += arr[i] - arr[i - k];
    maxSum = Math.max(maxSum, windowSum);
  }
  return maxSum;
}

console.log(maxSubarraySumK([2, 1, 5, 1, 3, 2], 3)); // 9

// Longest Substring Without Repeating Characters
function lengthOfLongestSubstring(s) {
  const charSet = new Set();
  let left = 0, maxLength = 0;

  for (let right = 0; right < s.length; right++) {
    while (charSet.has(s[right])) {
      charSet.delete(s[left]);
      left++;
    }
    charSet.add(s[right]);
    maxLength = Math.max(maxLength, right - left + 1);
  }
  return maxLength;
}

console.log(lengthOfLongestSubstring("abcabcbb")); // 3
console.log(lengthOfLongestSubstring("pwwkew"));   // 3
```
:::

---

## 3. Hash Tables

:::concept
### Hash Table Nedir?

Hash table, key-value ciftlerini saklayan ve O(1) ortalama lookup sunan data structure.

```
Hash Function:
"apple"  → hash("apple")  % 8 = 3  → bucket[3]
"banana" → hash("banana") % 8 = 5  → bucket[5]
"cherry" → hash("cherry") % 8 = 3  → bucket[3] ← COLLISION!

Collision Resolution:
1. Chaining: Her bucket bir linked list
   bucket[3] → ["apple": 1] → ["cherry": 5]

2. Open Addressing: Bos slot ara (linear probing)
   bucket[3] = "apple", bucket[4] = "cherry"
```

**Complexity:**
| Operation | Average | Worst (collision) |
|-----------|---------|-------------------|
| Insert    | O(1)    | O(n)             |
| Lookup    | O(1)    | O(n)             |
| Delete    | O(1)    | O(n)             |
:::

:::code
### Hash Table ile Interview Problemleri

```python
from collections import Counter, defaultdict

# ============================================
# PROBLEM 7: Group Anagrams (LeetCode #49)
# ============================================
def group_anagrams(strs: list[str]) -> list[list[str]]:
    """
    Anagram olan kelimeleri grupla.
    Key: sorted string, Value: anagram listesi
    O(n * k log k) where k = max string length
    """
    groups = defaultdict(list)

    for s in strs:
        key = ''.join(sorted(s))  # "eat" -> "aet"
        groups[key].append(s)

    return list(groups.values())

print(group_anagrams(["eat","tea","tan","ate","nat","bat"]))
# [["eat","tea","ate"], ["tan","nat"], ["bat"]]


# ============================================
# PROBLEM 8: Top K Frequent Elements (LeetCode #347)
# ============================================
def top_k_frequent(nums: list[int], k: int) -> list[int]:
    """
    En sik gecen k elemani bul.
    Bucket sort yaklasimi: O(n)
    """
    count = Counter(nums)

    # Bucket sort: index = frekans, value = sayilar
    # Max frekans = len(nums)
    buckets = [[] for _ in range(len(nums) + 1)]

    for num, freq in count.items():
        buckets[freq].append(num)

    result = []
    for i in range(len(buckets) - 1, -1, -1):
        for num in buckets[i]:
            result.append(num)
            if len(result) == k:
                return result

    return result

print(top_k_frequent([1,1,1,2,2,3], 2))  # [1, 2]


# ============================================
# PROBLEM 9: Subarray Sum Equals K (LeetCode #560)
# ============================================
def subarray_sum(nums: list[int], k: int) -> int:
    """
    Toplami k olan alt dizilerin sayisi.
    Prefix sum + hash map ile O(n).

    Ana fikir: prefix_sum[j] - prefix_sum[i] = k
    yani prefix_sum[j] - k = prefix_sum[i] olmus mu?
    """
    count = 0
    prefix_sum = 0
    prefix_map = {0: 1}  # bos alt dizi icin

    for num in nums:
        prefix_sum += num

        # prefix_sum - k daha once gorunmus mu?
        if prefix_sum - k in prefix_map:
            count += prefix_map[prefix_sum - k]

        prefix_map[prefix_sum] = prefix_map.get(prefix_sum, 0) + 1

    return count

print(subarray_sum([1, 1, 1], 2))      # 2
print(subarray_sum([1, 2, 3], 3))      # 2 ([1,2] ve [3])
```

```javascript
// JavaScript — Hash Table Interview Problemleri

// Group Anagrams
function groupAnagrams(strs) {
  const groups = new Map();
  for (const s of strs) {
    const key = [...s].sort().join('');
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(s);
  }
  return [...groups.values()];
}

console.log(groupAnagrams(["eat","tea","tan","ate","nat","bat"]));
// [["eat","tea","ate"], ["tan","nat"], ["bat"]]

// Top K Frequent Elements
function topKFrequent(nums, k) {
  const count = new Map();
  for (const num of nums) {
    count.set(num, (count.get(num) || 0) + 1);
  }

  // Bucket sort
  const buckets = Array.from({ length: nums.length + 1 }, () => []);
  for (const [num, freq] of count) {
    buckets[freq].push(num);
  }

  const result = [];
  for (let i = buckets.length - 1; i >= 0 && result.length < k; i--) {
    result.push(...buckets[i]);
  }
  return result.slice(0, k);
}

console.log(topKFrequent([1,1,1,2,2,3], 2)); // [1, 2]
```
:::

---

## 4. Stacks & Queues

:::concept
### Stack vs Queue

```
STACK (LIFO - Last In First Out):
  push(5) push(3) push(8) pop() → 8
  ┌───┐
  │ 8 │ ← top (son giren ilk cikar)
  │ 3 │
  │ 5 │
  └───┘

QUEUE (FIFO - First In First Out):
  enqueue(5) enqueue(3) enqueue(8) dequeue() → 5
  ┌───┬───┬───┐
  │ 5 │ 3 │ 8 │
  └───┴───┴───┘
  front↑       ↑rear  (ilk giren ilk cikar)
```

| Operation | Stack | Queue |
|-----------|-------|-------|
| Insert    | push() O(1) | enqueue() O(1) |
| Remove    | pop() O(1) | dequeue() O(1) |
| Peek      | top() O(1) | front() O(1) |
| Use Case  | Undo, parentheses, DFS | BFS, task scheduling |
:::

:::code
### Stack ile Interview Problemleri

```python
# ============================================
# PROBLEM 10: Valid Parentheses (LeetCode #20)
# ============================================
def is_valid_parentheses(s: str) -> bool:
    """
    Parantezlerin gecerli olup olmadigini kontrol et.
    Stack ile O(n).
    """
    stack = []
    matching = {')': '(', ']': '[', '}': '{'}

    for char in s:
        if char in matching:
            # Kapanan parantez - stack'ten eslestir
            if not stack or stack[-1] != matching[char]:
                return False
            stack.pop()
        else:
            # Acilan parantez - stack'e push
            stack.append(char)

    return len(stack) == 0

print(is_valid_parentheses("()[]{}"))   # True
print(is_valid_parentheses("([)]"))     # False
print(is_valid_parentheses("{[]}"))     # True


# ============================================
# PROBLEM 11: Min Stack (LeetCode #155)
# ============================================
class MinStack:
    """
    push, pop, top ve getMin hepsi O(1).
    Trick: Her eleman ile birlikte o anki min degeri de sakla.
    """

    def __init__(self):
        self.stack = []  # (value, current_min) tuples

    def push(self, val: int):
        current_min = min(val, self.stack[-1][1] if self.stack else val)
        self.stack.append((val, current_min))

    def pop(self):
        self.stack.pop()

    def top(self) -> int:
        return self.stack[-1][0]

    def getMin(self) -> int:
        return self.stack[-1][1]


# ============================================
# PROBLEM 12: Daily Temperatures (LeetCode #739)
# Monotonic Stack
# ============================================
def daily_temperatures(temperatures: list[int]) -> list[int]:
    """
    Her gun icin, daha sicak bir gune kac gun?
    Monotonic decreasing stack ile O(n).
    """
    n = len(temperatures)
    result = [0] * n
    stack = []  # index'leri sakla

    for i in range(n):
        # Stack'teki dusuk sicakliklari coz
        while stack and temperatures[i] > temperatures[stack[-1]]:
            prev_idx = stack.pop()
            result[prev_idx] = i - prev_idx

        stack.append(i)

    return result

print(daily_temperatures([73,74,75,71,69,72,76,73]))
# [1, 1, 4, 2, 1, 1, 0, 0]
```

```javascript
// JavaScript — Stack Interview Problemleri

// Valid Parentheses
function isValidParentheses(s) {
  const stack = [];
  const matching = { ')': '(', ']': '[', '}': '{' };

  for (const char of s) {
    if (char in matching) {
      if (!stack.length || stack[stack.length - 1] !== matching[char]) {
        return false;
      }
      stack.pop();
    } else {
      stack.push(char);
    }
  }
  return stack.length === 0;
}

console.log(isValidParentheses("()[]{}")); // true
console.log(isValidParentheses("([)]"));   // false

// Daily Temperatures (Monotonic Stack)
function dailyTemperatures(temperatures) {
  const n = temperatures.length;
  const result = new Array(n).fill(0);
  const stack = []; // index'ler

  for (let i = 0; i < n; i++) {
    while (stack.length && temperatures[i] > temperatures[stack[stack.length - 1]]) {
      const prevIdx = stack.pop();
      result[prevIdx] = i - prevIdx;
    }
    stack.push(i);
  }
  return result;
}

console.log(dailyTemperatures([73,74,75,71,69,72,76,73]));
// [1, 1, 4, 2, 1, 1, 0, 0]
```
:::

---

## 5. Linked Lists

:::code
### Linked List Temelleri ve Problemleri

```python
class ListNode:
    """Linked list node"""
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


# ============================================
# PROBLEM 13: Reverse Linked List (LeetCode #206)
# ============================================
def reverse_list(head: ListNode) -> ListNode:
    """
    Linked list'i ters cevir. O(n) time, O(1) space.
    3 pointer: prev, current, next
    """
    prev = None
    current = head

    while current:
        next_node = current.next  # Sonraki node'u sakla
        current.next = prev       # Yonu tersine cevir
        prev = current             # prev ilerle
        current = next_node        # current ilerle

    return prev  # Yeni head


# ============================================
# PROBLEM 14: Detect Cycle (LeetCode #141)
# Floyd's Tortoise and Hare
# ============================================
def has_cycle(head: ListNode) -> bool:
    """
    Linked list'te dongu var mi?
    Slow pointer (1 adim) ve fast pointer (2 adim).
    Dongu varsa bir noktada bulusurlar.
    O(n) time, O(1) space.
    """
    slow = fast = head

    while fast and fast.next:
        slow = slow.next          # 1 adim
        fast = fast.next.next     # 2 adim

        if slow == fast:
            return True

    return False


# ============================================
# PROBLEM 15: Merge Two Sorted Lists (LeetCode #21)
# ============================================
def merge_two_lists(l1: ListNode, l2: ListNode) -> ListNode:
    """Iki sirali linked list'i birlesir. O(n+m)."""
    dummy = ListNode(0)
    current = dummy

    while l1 and l2:
        if l1.val <= l2.val:
            current.next = l1
            l1 = l1.next
        else:
            current.next = l2
            l2 = l2.next
        current = current.next

    # Kalan elemanlari ekle
    current.next = l1 if l1 else l2

    return dummy.next


# ============================================
# PROBLEM 16: LRU Cache (LeetCode #146) - CRTIK!
# ============================================
class LRUNode:
    def __init__(self, key=0, val=0):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None

class LRUCache:
    """
    Least Recently Used Cache.
    get() ve put() O(1).
    Hash Map + Doubly Linked List kombinasyonu.

    Interview'larda EN COK sorulan data structure sorusu!
    """

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}  # key -> node

        # Dummy head ve tail (edge case'leri onler)
        self.head = LRUNode()
        self.tail = LRUNode()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: LRUNode):
        """Node'u listeden cikar"""
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_to_front(self, node: LRUNode):
        """Node'u listenin basina ekle (en son kullanilan)"""
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -> int:
        if key in self.cache:
            node = self.cache[key]
            # En son kullanilana tasi
            self._remove(node)
            self._add_to_front(node)
            return node.val
        return -1

    def put(self, key: int, value: int):
        if key in self.cache:
            # Varsa guncelle
            self._remove(self.cache[key])
            del self.cache[key]

        # Yeni node olustur
        node = LRUNode(key, value)
        self.cache[key] = node
        self._add_to_front(node)

        # Kapasite asildiysa en eski elemani sil
        if len(self.cache) > self.capacity:
            lru = self.tail.prev
            self._remove(lru)
            del self.cache[lru.key]


# Test
cache = LRUCache(2)
cache.put(1, 1)     # cache: {1=1}
cache.put(2, 2)     # cache: {1=1, 2=2}
print(cache.get(1)) # 1 (1'i one tasi)
cache.put(3, 3)     # 2 silindi, cache: {1=1, 3=3}
print(cache.get(2)) # -1 (bulunamadi)
cache.put(4, 4)     # 1 silindi, cache: {3=3, 4=4}
print(cache.get(1)) # -1
print(cache.get(3)) # 3
print(cache.get(4)) # 4
```
:::

:::beginner-mistake
### Linked List Hatalari

**Hata 1: Null pointer kontrolu unutma**
```python
# YANLIS
def get_value(head):
    return head.next.val  # head None olabilir!

# DOGRU
def get_value(head):
    if head and head.next:
        return head.next.val
    return None
```

**Hata 2: Referansi kaybetme**
```python
# YANLIS - bir sonraki node kaybolur
current.next = prev
current = current.next  # Artik eski current.next degil!

# DOGRU - once sakla
next_node = current.next
current.next = prev
current = next_node
```

**Hata 3: Dummy node kullanmama**
```python
# YANLIS - head icin ozel kontrol gerekir
def insert_sorted(head, val):
    if not head or val < head.val:
        return ListNode(val, head)
    # ... karmasik edge case'ler

# DOGRU - dummy node ile basit
def insert_sorted(head, val):
    dummy = ListNode(0, head)
    current = dummy
    while current.next and current.next.val < val:
        current = current.next
    current.next = ListNode(val, current.next)
    return dummy.next
```
:::

---

## 6. Trees

:::concept
### Binary Tree ve BST

```
Binary Tree:           Binary Search Tree (BST):
      1                        8
     / \                     /   \
    2   3                   3     10
   / \                     / \      \
  4   5                   1   6     14
                             / \   /
                            4   7 13

BST Kurali: Sol < Kok < Sag (her node icin)
```

| Operation | BST Average | BST Worst | Balanced BST |
|-----------|------------|-----------|--------------|
| Search    | O(log n)   | O(n)      | O(log n)     |
| Insert    | O(log n)   | O(n)      | O(log n)     |
| Delete    | O(log n)   | O(n)      | O(log n)     |
:::

:::code
### Tree Traversal ve Problemleri

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


# ============================================
# Tree Traversal (DFS)
# ============================================
def inorder(root: TreeNode) -> list:
    """Sol -> Kok -> Sag (BST'de sirali sonuc verir)"""
    if not root:
        return []
    return inorder(root.left) + [root.val] + inorder(root.right)

def preorder(root: TreeNode) -> list:
    """Kok -> Sol -> Sag (tree'yi kopyalamak icin)"""
    if not root:
        return []
    return [root.val] + preorder(root.left) + preorder(root.right)

def postorder(root: TreeNode) -> list:
    """Sol -> Sag -> Kok (tree'yi silmek icin)"""
    if not root:
        return []
    return postorder(root.left) + postorder(root.right) + [root.val]


# ============================================
# BFS - Level Order Traversal (LeetCode #102)
# ============================================
from collections import deque

def level_order(root: TreeNode) -> list[list[int]]:
    """Seviye seviye dolaş - Queue kullan."""
    if not root:
        return []

    result = []
    queue = deque([root])

    while queue:
        level = []
        level_size = len(queue)

        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)

            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        result.append(level)

    return result


# ============================================
# PROBLEM 17: Maximum Depth (LeetCode #104)
# ============================================
def max_depth(root: TreeNode) -> int:
    """Tree'nin maksimum derinligi. O(n)."""
    if not root:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))


# ============================================
# PROBLEM 18: Validate BST (LeetCode #98)
# ============================================
def is_valid_bst(root: TreeNode) -> bool:
    """
    Gecerli BST mi? Her node icin min/max range kontrol et.
    """
    def validate(node, min_val, max_val):
        if not node:
            return True

        if node.val <= min_val or node.val >= max_val:
            return False

        return (validate(node.left, min_val, node.val) and
                validate(node.right, node.val, max_val))

    return validate(root, float('-inf'), float('inf'))
```

```javascript
// JavaScript — Tree Interview Problemleri

class TreeNode {
  constructor(val = 0, left = null, right = null) {
    this.val = val;
    this.left = left;
    this.right = right;
  }
}

// Maximum Depth
function maxDepth(root) {
  if (!root) return 0;
  return 1 + Math.max(maxDepth(root.left), maxDepth(root.right));
}

// Level Order Traversal (BFS)
function levelOrder(root) {
  if (!root) return [];
  const result = [];
  const queue = [root];

  while (queue.length) {
    const level = [];
    const size = queue.length;
    for (let i = 0; i < size; i++) {
      const node = queue.shift();
      level.push(node.val);
      if (node.left) queue.push(node.left);
      if (node.right) queue.push(node.right);
    }
    result.push(level);
  }
  return result;
}

// Validate BST
function isValidBST(root, min = -Infinity, max = Infinity) {
  if (!root) return true;
  if (root.val <= min || root.val >= max) return false;
  return isValidBST(root.left, min, root.val) &&
         isValidBST(root.right, root.val, max);
}
```

```python

# ============================================
# PROBLEM 19: Lowest Common Ancestor (LeetCode #236)
# ============================================
def lowest_common_ancestor(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    """
    Iki node'un en yakin ortak atasi.
    Post-order DFS ile O(n).
    """
    if not root or root == p or root == q:
        return root

    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)

    if left and right:
        return root  # p ve q farkli alt agaclarda

    return left if left else right
```
:::

:::concept
### Heap (Priority Queue)

```
Min-Heap: Parent her zaman child'dan kucuk
        1
       / \
      3   5
     / \
    7   4

Max-Heap: Parent her zaman child'dan buyuk
        9
       / \
      7   5
     / \
    3   4

Array temsili: [1, 3, 5, 7, 4]
Parent: i
Left child: 2*i + 1
Right child: 2*i + 2
```

| Operation | Time |
|-----------|------|
| Insert    | O(log n) |
| Extract Min/Max | O(log n) |
| Peek Min/Max | O(1) |
| Build Heap | O(n) |
:::

:::code
### Heap Kullanımı

```python
import heapq

# Python'da heapq modulu MIN-HEAP'tir

# ============================================
# PROBLEM 20: Kth Largest Element (LeetCode #215)
# ============================================
def find_kth_largest(nums: list[int], k: int) -> int:
    """
    K. en buyuk elemani bul.
    Min-heap ile O(n log k).
    """
    # K boyutunda min-heap tut
    heap = nums[:k]
    heapq.heapify(heap)

    for num in nums[k:]:
        if num > heap[0]:
            heapq.heapreplace(heap, num)

    return heap[0]

print(find_kth_largest([3,2,1,5,6,4], 2))  # 5
print(find_kth_largest([3,2,3,1,2,4,5,5,6], 4))  # 4


# ============================================
# PROBLEM 21: Merge K Sorted Lists (LeetCode #23)
# ============================================
def merge_k_lists(lists: list[ListNode]) -> ListNode:
    """
    K adet sirali linked list'i birleştir.
    Heap ile O(n log k) where n = toplam eleman sayisi.
    """
    dummy = ListNode(0)
    current = dummy
    heap = []

    # Her listenin ilk elemanini heap'e ekle
    for i, node in enumerate(lists):
        if node:
            heapq.heappush(heap, (node.val, i, node))

    while heap:
        val, i, node = heapq.heappop(heap)
        current.next = node
        current = current.next

        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))

    return dummy.next
```
:::

---

## 7. Graphs

:::concept
### Graph Temelleri

```
Graph Gosterimi:

Adjacency List (en yaygin):          Adjacency Matrix:
{                                     A B C D
  "A": ["B", "C"],                A [ 0 1 1 0 ]
  "B": ["A", "D"],                B [ 1 0 0 1 ]
  "C": ["A", "D"],                C [ 1 0 0 1 ]
  "D": ["B", "C"]                 D [ 0 1 1 0 ]
}

Adjacency List: O(V + E) space → sparse graph icin
Adjacency Matrix: O(V²) space → dense graph icin
```

| Özellik | BFS | DFS |
|---------|-----|-----|
| Yaklaşım | Queue (FIFO) | Stack/Recursion (LIFO) |
| En kisa yol | EVET (unweighted) | HAYIR |
| Bellek | O(V) - geniş | O(h) - derin |
| Use Case | Shortest path, level order | Cycle detection, topological sort |
:::

:::code
### Graph Traversal: BFS & DFS

```python
from collections import deque, defaultdict

# ============================================
# Graph sinifi
# ============================================
class Graph:
    def __init__(self):
        self.adj_list = defaultdict(list)

    def add_edge(self, u, v, directed=False):
        self.adj_list[u].append(v)
        if not directed:
            self.adj_list[v].append(u)

    # ============================================
    # BFS - Breadth-First Search
    # ============================================
    def bfs(self, start) -> list:
        """
        Genislik oncelikli arama.
        Queue kullanir - once yakin komsular ziyaret edilir.
        O(V + E) time, O(V) space.
        """
        visited = set()
        queue = deque([start])
        visited.add(start)
        result = []

        while queue:
            node = queue.popleft()
            result.append(node)

            for neighbor in self.adj_list[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return result

    # ============================================
    # DFS - Depth-First Search
    # ============================================
    def dfs(self, start) -> list:
        """
        Derinlik oncelikli arama (iterative).
        Stack kullanir - bir yolu sonuna kadar takip eder.
        O(V + E) time, O(V) space.
        """
        visited = set()
        stack = [start]
        result = []

        while stack:
            node = stack.pop()
            if node in visited:
                continue

            visited.add(node)
            result.append(node)

            # Komşulari stack'e ekle
            for neighbor in self.adj_list[node]:
                if neighbor not in visited:
                    stack.append(neighbor)

        return result

    def dfs_recursive(self, start, visited=None) -> list:
        """DFS - recursive versiyon"""
        if visited is None:
            visited = set()

        visited.add(start)
        result = [start]

        for neighbor in self.adj_list[start]:
            if neighbor not in visited:
                result.extend(self.dfs_recursive(neighbor, visited))

        return result

    # ============================================
    # Shortest Path (BFS - unweighted)
    # ============================================
    def shortest_path(self, start, end) -> list:
        """
        Unweighted graph'ta en kisa yol.
        BFS ile O(V + E).
        """
        if start == end:
            return [start]

        visited = set()
        queue = deque([(start, [start])])
        visited.add(start)

        while queue:
            node, path = queue.popleft()

            for neighbor in self.adj_list[node]:
                if neighbor == end:
                    return path + [neighbor]

                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        return []  # Yol bulunamadi


# Test
g = Graph()
g.add_edge(0, 1)
g.add_edge(0, 2)
g.add_edge(1, 3)
g.add_edge(2, 3)
g.add_edge(3, 4)

print("BFS:", g.bfs(0))           # [0, 1, 2, 3, 4]
print("DFS:", g.dfs(0))           # [0, 2, 3, 4, 1]
print("Path:", g.shortest_path(0, 4))  # [0, 1, 3, 4]


# ============================================
# PROBLEM 22: Number of Islands (LeetCode #200)
# ============================================
def num_islands(grid: list[list[str]]) -> int:
    """
    2D grid'de ada sayisini bul.
    Her '1' goruldugunde BFS/DFS ile tum adayi isle.
    O(m*n) time.
    """
    if not grid:
        return 0

    rows, cols = len(grid), len(grid[0])
    count = 0

    def dfs(r, c):
        # Sinir kontrolu ve su kontrolu
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] == '0':
            return

        grid[r][c] = '0'  # Ziyaret edildi olarak isaretle

        # 4 yone git
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                count += 1
                dfs(r, c)

    return count

grid = [
    ["1","1","0","0","0"],
    ["1","1","0","0","0"],
    ["0","0","1","0","0"],
    ["0","0","0","1","1"]
]
print(num_islands(grid))  # 3
```
:::

:::code
### Dijkstra - Weighted Shortest Path

```python
import heapq

def dijkstra(graph: dict, start: str) -> dict:
    """
    Weighted graph'ta tek kaynaktan en kisa yollar.
    Greedy + Priority Queue ile O((V + E) log V).

    graph format: {node: [(neighbor, weight), ...]}
    """
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    previous = {node: None for node in graph}

    # (distance, node) - min-heap
    pq = [(0, start)]

    while pq:
        current_dist, current_node = heapq.heappop(pq)

        # Zaten daha kisa yol bulunmussa atla
        if current_dist > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node]:
            distance = current_dist + weight

            # Daha kisa yol bulduk mu?
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_node
                heapq.heappush(pq, (distance, neighbor))

    return distances, previous


def get_path(previous: dict, start: str, end: str) -> list:
    """Dijkstra sonucundan yolu olustur"""
    path = []
    current = end
    while current:
        path.append(current)
        current = previous[current]
    return list(reversed(path))


# Ornek: Sehirler arasi en kisa mesafe
city_graph = {
    'Istanbul': [('Ankara', 450), ('Bursa', 150)],
    'Ankara':   [('Istanbul', 450), ('Izmir', 600), ('Antalya', 550)],
    'Bursa':    [('Istanbul', 150), ('Izmir', 330)],
    'Izmir':    [('Ankara', 600), ('Bursa', 330), ('Antalya', 450)],
    'Antalya':  [('Ankara', 550), ('Izmir', 450)]
}

distances, previous = dijkstra(city_graph, 'Istanbul')
print("Istanbul'dan mesafeler:", distances)
# {'Istanbul': 0, 'Ankara': 450, 'Bursa': 150, 'Izmir': 480, 'Antalya': 930}

print("Istanbul -> Izmir yolu:", get_path(previous, 'Istanbul', 'Izmir'))
# ['Istanbul', 'Bursa', 'Izmir'] (dogrudan degil, Bursa uzerinden daha kisa!)
```
:::

---

## 8. Sorting Algorithms

:::comparison
### Sıralama Algoritmasi Karşılaştırması

| Algoritma | Best | Average | Worst | Space | Stable |
|-----------|------|---------|-------|-------|--------|
| Bubble Sort | O(n) | O(n²) | O(n²) | O(1) | Evet |
| Selection Sort | O(n²) | O(n²) | O(n²) | O(1) | Hayir |
| Insertion Sort | O(n) | O(n²) | O(n²) | O(1) | Evet |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | O(n) | Evet |
| Quick Sort | O(n log n) | O(n log n) | O(n²) | O(log n) | Hayir |
| Heap Sort | O(n log n) | O(n log n) | O(n log n) | O(1) | Hayir |

**Interview için bilmen gerekenler:**
- **Merge Sort**: Stable, guaranteed O(n log n), extra space gerektirir
- **Quick Sort**: Pratikte en hızlı, ama worst case O(n²)
- **Counting/Radix Sort**: O(n) ama sınırlı kullanım alani
:::

:::code
### Quick Sort Implementasyonu

```python
def quick_sort(arr: list) -> list:
    """
    Quick Sort - Divide and Conquer.
    Pivot sec, kucukleri sola buyukleri saga koy, tekrarla.
    Average: O(n log n), Worst: O(n²)
    """
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2]  # Ortadaki elemani pivot sec

    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]

    return quick_sort(left) + middle + quick_sort(right)


# In-place versiyon (daha verimli)
def quick_sort_inplace(arr: list, low: int = 0, high: int = None):
    """In-place Quick Sort - O(log n) space (call stack)"""
    if high is None:
        high = len(arr) - 1

    if low < high:
        pivot_idx = partition(arr, low, high)
        quick_sort_inplace(arr, low, pivot_idx - 1)
        quick_sort_inplace(arr, pivot_idx + 1, high)

def partition(arr: list, low: int, high: int) -> int:
    """Lomuto partition scheme"""
    pivot = arr[high]
    i = low - 1

    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


# Test
arr = [3, 6, 8, 10, 1, 2, 1]
print(quick_sort(arr))  # [1, 1, 2, 3, 6, 8, 10]

arr2 = [3, 6, 8, 10, 1, 2, 1]
quick_sort_inplace(arr2)
print(arr2)  # [1, 1, 2, 3, 6, 8, 10]
```
:::

---

## 9. Dynamic Programming

:::concept
### DP Nedir?

Dynamic Programming = **overlapping subproblems** + **optimal substructure** olan problemleri çözme teknigi.

**2 Yaklaşım:**
1. **Top-Down (Memoization)**: Recursive + cache
2. **Bottom-Up (Tabulation)**: Iterative + table

```
Fibonacci ornegi:

Recursive (O(2^n)):        Memoized (O(n)):
       fib(5)                  fib(5)
      /      \                /      \
   fib(4)   fib(3)        fib(4)   fib(3) ← cache'ten
   /    \    /    \        /    \
 fib(3) fib(2) ...      fib(3) fib(2) ← cache'ten
 /    \                  cache'ten
...  (cok fazla tekrar!)
```
:::

:::code
### DP Problemleri

```python
from functools import lru_cache

# ============================================
# PROBLEM 23: Climbing Stairs (LeetCode #70)
# ============================================
def climb_stairs(n: int) -> int:
    """
    Her adimda 1 veya 2 basamak cikabilirsin.
    n. basamaga kac farkli sekilde ulasabilirsin?

    dp[i] = dp[i-1] + dp[i-2]  (Fibonacci!)
    Bottom-up, O(n) time, O(1) space.
    """
    if n <= 2:
        return n

    prev2, prev1 = 1, 2

    for i in range(3, n + 1):
        current = prev1 + prev2
        prev2 = prev1
        prev1 = current

    return prev1

print(climb_stairs(5))  # 8


# ============================================
# PROBLEM 24: Coin Change (LeetCode #322)
# ============================================
def coin_change(coins: list[int], amount: int) -> int:
    """
    Verilen bozuk paralarla amount'u olusturmak icin
    gereken minimum para sayisi.

    dp[i] = i miktari olusturmak icin gereken min para
    Bottom-up, O(amount * len(coins))
    """
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0

    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i and dp[i - coin] + 1 < dp[i]:
                dp[i] = dp[i - coin] + 1

    return dp[amount] if dp[amount] != float('inf') else -1

print(coin_change([1, 5, 10, 25], 30))  # 2 (25 + 5)
print(coin_change([2], 3))              # -1 (imkansiz)


# ============================================
# PROBLEM 25: Longest Common Subsequence (LeetCode #1143)
# ============================================
def longest_common_subsequence(text1: str, text2: str) -> int:
    """
    Iki stringin en uzun ortak alt dizisi.
    2D DP tablosu. O(m*n).

    dp[i][j] = text1[:i] ve text2[:j] icin LCS uzunlugu
    """
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i-1] == text2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    return dp[m][n]

print(longest_common_subsequence("abcde", "ace"))    # 3 ("ace")
print(longest_common_subsequence("abc", "def"))      # 0


# ============================================
# PROBLEM 26: 0/1 Knapsack
# ============================================
def knapsack(weights: list[int], values: list[int], capacity: int) -> int:
    """
    Sirt cantasi problemi: Verilen kapasite ile
    maksimum degeri elde et.
    O(n * capacity)
    """
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            # Nesneyi almadan
            dp[i][w] = dp[i-1][w]

            # Nesneyi alarak (sigiyorsa)
            if weights[i-1] <= w:
                dp[i][w] = max(
                    dp[i][w],
                    dp[i-1][w - weights[i-1]] + values[i-1]
                )

    return dp[n][capacity]

weights = [1, 3, 4, 5]
values = [1, 4, 5, 7]
print(knapsack(weights, values, 7))  # 9 (3kg + 4kg = 4+5=9)


# ============================================
# PROBLEM 27: Longest Increasing Subsequence (LeetCode #300)
# ============================================
def length_of_lis(nums: list[int]) -> int:
    """
    En uzun artan alt dizi.
    O(n²) DP cozumu.
    dp[i] = nums[i] ile biten en uzun artan alt dizi
    """
    if not nums:
        return 0

    n = len(nums)
    dp = [1] * n  # Her eleman en az 1 uzunlugunda

    for i in range(1, n):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)

    return max(dp)

print(length_of_lis([10, 9, 2, 5, 3, 7, 101, 18]))  # 4 ([2,3,7,101])
```

```javascript
// JavaScript — DP Problemleri

// Climbing Stairs
function climbStairs(n) {
  if (n <= 2) return n;
  let prev2 = 1, prev1 = 2;
  for (let i = 3; i <= n; i++) {
    const current = prev1 + prev2;
    prev2 = prev1;
    prev1 = current;
  }
  return prev1;
}

console.log(climbStairs(5)); // 8

// Coin Change
function coinChange(coins, amount) {
  const dp = new Array(amount + 1).fill(Infinity);
  dp[0] = 0;

  for (let i = 1; i <= amount; i++) {
    for (const coin of coins) {
      if (coin <= i && dp[i - coin] + 1 < dp[i]) {
        dp[i] = dp[i - coin] + 1;
      }
    }
  }
  return dp[amount] === Infinity ? -1 : dp[amount];
}

console.log(coinChange([1, 5, 10, 25], 30)); // 2 (25 + 5)

// Longest Increasing Subsequence
function lengthOfLIS(nums) {
  if (!nums.length) return 0;
  const dp = new Array(nums.length).fill(1);

  for (let i = 1; i < nums.length; i++) {
    for (let j = 0; j < i; j++) {
      if (nums[j] < nums[i]) {
        dp[i] = Math.max(dp[i], dp[j] + 1);
      }
    }
  }
  return Math.max(...dp);
}

console.log(lengthOfLIS([10, 9, 2, 5, 3, 7, 101, 18])); // 4
```
:::

:::tip
### DP Problem Tanima Ipuclari

DP kullan eger:
1. **"Kac farkli yol var?"** → Climbing stairs, unique paths
2. **"Minimum/maksimum bul"** → Coin change, knapsack
3. **"Mumkun mu?"** → Subset sum, word break
4. **"En uzun/kisa ...?"** → LCS, LIS

DP KULLANMA eger:
- Problem greedy ile cozulebiliyorsa (daha basit)
- Subproblem'ler overlap etmiyorsa (divide & conquer yeterli)
:::

---

## 10. Greedy Algorithms

:::code
### Greedy Örnekleri

```python
# ============================================
# PROBLEM 28: Activity Selection
# ============================================
def activity_selection(activities: list[tuple[int, int]]) -> list:
    """
    Birbiriyle cakismayan maksimum sayida aktivite sec.
    Greedy: Bitis zamanina gore sirala, en erken biteni sec.
    O(n log n)
    """
    # Bitis zamanina gore sirala
    sorted_activities = sorted(activities, key=lambda x: x[1])

    selected = [sorted_activities[0]]
    last_end = sorted_activities[0][1]

    for start, end in sorted_activities[1:]:
        if start >= last_end:
            selected.append((start, end))
            last_end = end

    return selected

activities = [(1, 4), (3, 5), (0, 6), (5, 7), (3, 9), (5, 9), (6, 10), (8, 11)]
print(activity_selection(activities))
# [(1, 4), (5, 7), (8, 11)] - 3 aktivite


# ============================================
# PROBLEM 29: Jump Game (LeetCode #55)
# ============================================
def can_jump(nums: list[int]) -> bool:
    """
    Her eleman o pozisyondan max atlama mesafesi.
    Sona ulasabilir misin? Greedy O(n).
    """
    max_reach = 0

    for i in range(len(nums)):
        if i > max_reach:
            return False  # Bu noktaya ulasamiyoruz
        max_reach = max(max_reach, i + nums[i])

    return True

print(can_jump([2, 3, 1, 1, 4]))  # True
print(can_jump([3, 2, 1, 0, 4]))  # False
```
:::

---

## 11. Interview Problem-Solving Framework

:::concept
### UMPIRE Method

Interview'da her probleme sistematik yaklas:

| Adim | Ne Yap | Örnek |
|------|--------|-------|
| **U**nderstand | Problemi anla, sorular sor | "Input ne? Edge case'ler?" |
| **M**atch | Bilinen pattern'e esle | "Bu two pointers problemi" |
| **P**lan | Pseudocode yaz | "1. Sort et 2. Two pointers..." |
| **I**mplement | Kodu yaz | Python cozumu |
| **R**eview | Kodu gözden gecir | Edge case, off-by-one |
| **E**valuate | Complexity analizi | "O(n log n) time, O(1) space" |
:::

:::interview
### DSA Interview Pattern Tablosu

| Pattern | Ne Zaman Kullan | Örnek Problemler |
|---------|-----------------|------------------|
| Two Pointers | Sirali array, palindrome | Two Sum (sorted), Container With Most Water |
| Sliding Window | Alt dizi/string, sabit/değişken pencere | Max subarray, Longest substring |
| Hash Map | O(1) lookup, frekans sayma | Two Sum, Anagrams, Subarray Sum |
| Stack | LIFO gerekli, parantez, monotonic | Valid Parentheses, Daily Temperatures |
| BFS | En kisa yol, level-order | Shortest Path, Number of Islands |
| DFS | Tüm yollari kesfetme, tree traversal | Permutations, Tree problems |
| Binary Search | Sirali veri, monotonic fonksiyon | Search in rotated array |
| DP | Overlapping subproblems | Coin Change, LCS, Knapsack |
| Greedy | Lokal optimal = global optimal | Activity Selection, Jump Game |
| Heap | Top-K, median, merge sorted | Kth Largest, Merge K Lists |
:::

:::interview
### DSA Mülakat Soruları — Junior vs Senior

**S1**: "Two Sum problemini çöz."

**Junior cevap**: Brute force iki nested loop ile O(n^2) çözüm yazar.

**Senior cevap**: "Önce soruyu netleştireyim — array sıralı mı? Duplicate var mı? Birden fazla çözüm olabilir mi?" Sonra hash map ile O(n) çözüm yazar. Edge case'leri belirtir (boş array, tek eleman, aynı eleman iki kez). Time ve space complexity'yi açıklar. Sıralı array ise two pointers ile O(1) space alternatifi olduğunu da belirtir.

---

**S2**: "LRU Cache nasıl implement edersin?"

**Junior cevap**: "Array kullanırım, her erişimde elemanı başa taşırım." (Bu O(n) olur)

**Senior cevap**: "Hash Map + Doubly Linked List kombinasyonu. Hash Map O(1) lookup sağlar, Doubly Linked List O(1) insertion/deletion sağlar. get() ve put() ikisi de O(1). En son erişilen elemanı listenin başına taşırım, kapasite dolduğunda listenin sonundaki elemanı silerim. Bu Redis ve Memcached'in de kullandığı yapıdır."

---

**S3**: "Bu çözümün time complexity'si ne?"

**Junior cevap**: "O(n)" (genellikle doğru ama neden olduğunu açıklayamaz)

**Senior cevap**: "Bu çözümde dış döngü n kez çalışır, iç döngü amortized olarak toplamda n kez çalışır (sliding window — her eleman en fazla bir kez eklenir ve bir kez çıkarılır). Dolayısıyla toplam O(n) time. Space complexity O(min(n, k)) çünkü set en fazla k farklı karakter tutar. Worst case'te k=n olduğunda O(n) space."

---

**S4**: "Array'de duplicate'ı O(1) space ile tespit edebilir misin?"

**Junior cevap**: "Hash set kullanırım." (Bu O(n) space)

**Senior cevap**: "Eğer array elemanları 1 ile n arasındaysa Floyd's cycle detection (tortoise and hare) kullanırım — O(n) time, O(1) space. Array'i linked list gibi düşünürüm: nums[i] bir sonraki index'e işaret eder. Duplicate varsa cycle oluşur. Sort edip ardışık kontrol de O(1) space ama O(n log n) time — ve input'u mutate eder ki bu kabul edilmeyebilir."
:::

:::knowledge-check
### Bilgi Kontrolu

1. O(n log n) hangi sıralama algoritmalarinin karmasikligidir?
2. LRU Cache için neden hash map + doubly linked list kullanılır?
3. BFS ile DFS arasindaki temel fark nedir?
4. DP problemi oldugunu nasil anlarsin?
5. Dijkstra algoritmasi negative weight edge'lerde çalışır mi?
:::

:::exercise
### Uygulama: DSA Problem Set

Aşağıdaki problemleri Python ile coz:

**Easy:**
1. Bir array'de en çok tekrar eden elemani bul (O(n))
2. Iki sirali array'i birleştir (O(n+m))
3. String'deki ilk tekrar etmeyen karakteri bul (O(n))

**Medium:**
4. Verilen bir array'de toplami 0 olan alt dizi var mi? (Prefix sum + hash)
5. Binary tree'nin mirror (ayna) kopyasini oluştur (recursive)
6. Bir graph'ta cycle var mi tespit et (DFS)

**Hard:**
7. LRU Cache'i sifirdan implement et (hash map + doubly linked list)
8. Trapping Rain Water problemi (LeetCode #42)
9. Word Break problemi (DP) (LeetCode #139)

Her çözüm için:
- Time complexity belirt
- Space complexity belirt
- En az 2 test case yaz

---

### Alıştırma 2: Two Pointers — 3Sum Problemi (Orta)

LeetCode #15 — Verilen bir array'de toplamı 0 olan tüm üçlüleri bul:

```python
def three_sum(nums: list[int]) -> list[list[int]]:
    """
    Toplamı 0 olan tüm benzersiz üçlüleri döndür.

    Örnek:
        Input: [-1, 0, 1, 2, -1, -4]
        Output: [[-1, -1, 2], [-1, 0, 1]]

    Kısıtlar:
        - Duplicate üçlüler olmamalı
        - O(n²) çözüm bekleniyor (brute force O(n³) kabul edilmez)
    """
    # TODO: 1. Array'i sırala
    # TODO: 2. Her eleman için two pointer kullan
    # TODO: 3. Duplicate'leri atla
    # Hint: Sıralanmış array'de i fix, left=i+1, right=len-1
    pass

# Test cases:
assert sorted(three_sum([-1, 0, 1, 2, -1, -4])) == sorted([[-1, -1, 2], [-1, 0, 1]])
assert three_sum([0, 0, 0]) == [[0, 0, 0]]
assert three_sum([1, 2, 3]) == []
assert three_sum([-2, 0, 1, 1, 2]) == [[-2, 0, 2], [-2, 1, 1]]

# Bonus: Time ve Space complexity'yi açıkla
# Time: O(?)  Space: O(?)
```

**Beklenen sonuç:** Tüm test case'ler geçmeli. Duplicate handling doğru çalışmalı. Brute force yerine two pointer yaklaşımını kullanarak O(n^2) olmalı.

---

### Alıştırma 3: Sliding Window — Maximum Sum Subarray + Anagram Detection (Zor)

İki sliding window problemi çöz:

```python
# Problem 1: Max Sum Subarray of Size K
def max_sum_subarray(nums: list[int], k: int) -> int:
    """
    Boyutu k olan alt dizilerden en büyük toplamı bul.

    Örnek:
        Input: nums=[2, 1, 5, 1, 3, 2], k=3
        Output: 9  (alt dizi: [5, 1, 3])

    Kısıt: O(n) çözüm — her seferinde k elemanı toplama (O(n*k) kabul edilmez)
    """
    # TODO: Sliding window ile implement et
    # Hint: Pencereyi kaydırırken çıkan elemanı çıkar, giren elemanı ekle
    pass

# Problem 2: Find All Anagrams in a String (LeetCode #438)
def find_anagrams(s: str, p: str) -> list[int]:
    """
    s string'inde p'nin anagramlarının başlangıç index'lerini bul.

    Örnek:
        Input: s="cbaebabacd", p="abc"
        Output: [0, 6]
        Açıklama: index 0'da "cba" (abc'nin anagramı), index 6'da "bac"

    Kısıt: O(n) çözüm — sliding window + frequency counter
    """
    # TODO: Implement
    # Hint: collections.Counter kullan, pencere boyutu = len(p)
    pass

# Test cases — Problem 1:
assert max_sum_subarray([2, 1, 5, 1, 3, 2], 3) == 9
assert max_sum_subarray([1, 1, 1, 1, 1], 2) == 2
assert max_sum_subarray([5, -2, 3, 1, 7], 2) == 8  # [1, 7]

# Test cases — Problem 2:
assert find_anagrams("cbaebabacd", "abc") == [0, 6]
assert find_anagrams("abab", "ab") == [0, 1, 2]
assert find_anagrams("hello", "xyz") == []

# Bonus: Her çözümün Time ve Space complexity'sini açıkla
```

**Beklenen sonuç:** Her iki problem O(n) ile çözülmeli. Sliding window'un nasıl çalıştığını adım adım açıkla (pencere nasıl kayar, ne eklenir, ne çıkarılır).

---

### Alistirma 4: Graph — Course Schedule (Orta)

LeetCode #207 — Topological Sort ile cycle detection:

```python
def can_finish(num_courses: int, prerequisites: list[list[int]]) -> bool:
    """
    Ders ön koşullarına göre tüm dersleri alabilir misin?
    prerequisites = [[1, 0]] → Ders 1 için önce Ders 0 alınmalı.

    Cycle varsa → tüm dersler alınamaz (False)
    Cycle yoksa → alınabilir (True)

    Örnek:
        can_finish(2, [[1, 0]]) → True (0 → 1 sırasıyla al)
        can_finish(2, [[1, 0], [0, 1]]) → False (cycle: 0 → 1 → 0)

    Hint: Graph oluştur + Topological Sort (Kahn's algorithm — BFS ile)
    veya DFS ile cycle detection
    """
    # TODO: Implement
    pass

# Test cases:
assert can_finish(2, [[1, 0]]) == True
assert can_finish(2, [[1, 0], [0, 1]]) == False
assert can_finish(4, [[1, 0], [2, 1], [3, 2]]) == True  # Linear dependency
assert can_finish(1, []) == True  # Tek ders, ön koşul yok
```

**Beklenen sonuc:** Topological sort veya DFS ile O(V+E) cozum. Adjacency list ile graph olustur, in-degree hesapla, BFS ile isle.

---

### Alistirma 5: DP — House Robber (Orta)

LeetCode #198 — Dinamik programlama klasiği:

```javascript
/**
 * Bir hırsız, yan yana evleri soyamaz.
 * Maksimum ne kadar para çalabilir?
 *
 * Örnek:
 *   Input: [1, 2, 3, 1]
 *   Output: 4 (1. ev + 3. ev = 1 + 3 = 4)
 *
 *   Input: [2, 7, 9, 3, 1]
 *   Output: 12 (1. ev + 3. ev + 5. ev = 2 + 9 + 1 = 12)
 *
 * dp[i] = Math.max(dp[i-1], dp[i-2] + nums[i])
 * Seçenek 1: Bu evi soyma → dp[i-1]
 * Seçenek 2: Bu evi soy → dp[i-2] + nums[i]
 *
 * Hint: O(1) space ile çözülebilir (sadece prev1 ve prev2 tut)
 */
function rob(nums) {
  // TODO: Implement
}

// Test cases:
console.assert(rob([1, 2, 3, 1]) === 4);
console.assert(rob([2, 7, 9, 3, 1]) === 12);
console.assert(rob([2, 1, 1, 2]) === 4);
console.assert(rob([]) === 0);
console.assert(rob([5]) === 5);
```

**Beklenen sonuc:** O(n) time, O(1) space DP cozumu. Bottom-up yaklasimla prev1 ve prev2 degiskenleri yeterli.

---

### Alistirma 6: Binary Search — Rotated Sorted Array (Zor)

LeetCode #33 — Modified binary search:

```python
def search_rotated(nums: list[int], target: int) -> int:
    """
    Rotated sorted array'de target'i bul.

    Ornek:
        Input: nums=[4, 5, 6, 7, 0, 1, 2], target=0
        Output: 4

        Input: nums=[4, 5, 6, 7, 0, 1, 2], target=3
        Output: -1

    Kisit: O(log n) cozum — linear scan kabul edilmez
    Hint: Binary search'te her adimda hangi yarinin sirali
          oldugunu belirle, target o yarida mi kontrol et.
    """
    # TODO: Implement
    pass

# Test cases:
assert search_rotated([4, 5, 6, 7, 0, 1, 2], 0) == 4
assert search_rotated([4, 5, 6, 7, 0, 1, 2], 3) == -1
assert search_rotated([1], 0) == -1
assert search_rotated([1], 1) == 0
assert search_rotated([3, 1], 1) == 1
```

**Beklenen sonuc:** O(log n) modified binary search. Her adimda left/right yarinin hangisinin sorted oldugunu belirle, target o range'te mi kontrol et.

---

### Alistirma 7: Stack — Valid Parentheses ve Monotonic Stack (Orta)

Stack veri yapisiyla parantez dogrulama ve monotonic stack problemlerini coz.

```python
def is_valid_parentheses(s: str) -> bool:
    """LeetCode #20 — Valid Parentheses"""
    stack = []
    mapping = {")": "(", "]": "[", "}": "{"}

    for char in s:
        if char in mapping:
            if not stack or stack[-1] != mapping[char]:
                return False
            stack.pop()
        else:
            stack.append(char)

    return len(stack) == 0

def daily_temperatures(temperatures: list[int]) -> list[int]:
    """LeetCode #739 — Monotonic Stack ile her gun icin kac gun sonra daha sicak olacagini bul"""
    n = len(temperatures)
    result = [0] * n
    stack = []  # (index) — monotonically decreasing

    for i in range(n):
        while stack and temperatures[i] > temperatures[stack[-1]]:
            prev = stack.pop()
            result[prev] = i - prev
        stack.append(i)

    return result

# Test
assert is_valid_parentheses("({[]})") == True
assert is_valid_parentheses("([)]") == False
assert daily_temperatures([73,74,75,71,69,72,76,73]) == [1,1,4,2,1,1,0,0]

# TODO: Min Stack implement et — O(1) push, pop ve getMin (LeetCode #155)
# TODO: Largest Rectangle in Histogram (LeetCode #84) — Monotonic stack
# TODO: Time ve space complexity analiz et
```

**Beklenen Sonuc:** Valid parentheses O(n) time, O(n) space. Daily temperatures monotonic decreasing stack ile O(n) cozulmeli. Min Stack'te getMin O(1) olmali.
**Ipucu:** Monotonic stack: her eleman en fazla 1 kez push ve 1 kez pop edilir → amortized O(n).

---

### Alistirma 8: Tree/BST — DFS ve BFS Traversal (Orta)

Binary tree uzerinde traversal ve ortak ata bulma problemlerini coz.

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def level_order(root: TreeNode) -> list[list[int]]:
    """LeetCode #102 — BFS ile seviye sirasinda traversal"""
    if not root:
        return []
    result = []
    queue = [root]
    while queue:
        level = []
        next_queue = []
        for node in queue:
            level.append(node.val)
            if node.left: next_queue.append(node.left)
            if node.right: next_queue.append(node.right)
        result.append(level)
        queue = next_queue
    return result

def lowest_common_ancestor(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    """LeetCode #236 — En yakin ortak ata"""
    if not root or root == p or root == q:
        return root
    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)
    if left and right:
        return root
    return left or right

# TODO: Inorder, preorder, postorder traversal (iterative + recursive)
# TODO: Maximum depth of binary tree (LeetCode #104)
# TODO: Validate BST (LeetCode #98) — inorder traversal ile
# TODO: Serialize and deserialize binary tree (LeetCode #297)
```

**Beklenen Sonuc:** Level order BFS ile O(n) time. LCA recursive DFS ile O(n) time. BST validation inorder traversal ile O(n) cozulmeli.
**Ipucu:** Tree problemlerinin cogu DFS (recursive) ile cozulur. BFS genellikle level-order islemlerde kullanilir.

---

### Alistirma 9: Heap — Top-K ve Median (Zor)

Heap ile priority queue problemlerini coz.

```python
import heapq

def top_k_frequent(nums: list[int], k: int) -> list[int]:
    """LeetCode #347 — En sik tekrar eden k eleman"""
    from collections import Counter
    count = Counter(nums)
    # Min-heap of size k (en kucugu tepede, daha buyuk gelince degistir)
    return heapq.nlargest(k, count.keys(), key=count.get)

class MedianFinder:
    """LeetCode #295 — Streaming median (iki heap)"""
    def __init__(self):
        self.small = []  # max-heap (negatif olarak sakla)
        self.large = []  # min-heap

    def addNum(self, num: int):
        heapq.heappush(self.small, -num)
        # small'daki max, large'daki min'den buyukse tasi
        if self.small and self.large and -self.small[0] > self.large[0]:
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        # Boyut dengesini koru (fark max 1)
        if len(self.small) > len(self.large) + 1:
            val = -heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        if len(self.large) > len(self.small) + 1:
            val = heapq.heappop(self.large)
            heapq.heappush(self.small, -val)

    def findMedian(self) -> float:
        if len(self.small) > len(self.large):
            return -self.small[0]
        if len(self.large) > len(self.small):
            return self.large[0]
        return (-self.small[0] + self.large[0]) / 2

# TODO: Merge K Sorted Lists (LeetCode #23) — min heap ile
# TODO: Task Scheduler (LeetCode #621) — max heap + cooldown
# TODO: Her cozumun time/space complexity'sini analiz et
```

**Beklenen Sonuc:** Top-K O(n log k). MedianFinder addNum O(log n), findMedian O(1). Merge K Lists O(N log k) olmali.
**Ipucu:** Python'da heapq min-heap'tir. Max-heap icin degerleri negatif olarak sakla.

---

### Alistirma 10: Trie — Autocomplete ve Word Search (Zor)

Trie (prefix tree) veri yapisini implement et ve gercek dunya problemlerini coz.

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.frequency = 0  # Autocomplete icin

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str, freq: int = 1):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
        node.frequency += freq

    def search(self, word: str) -> bool:
        node = self._find(word)
        return node is not None and node.is_end

    def starts_with(self, prefix: str) -> bool:
        return self._find(prefix) is not None

    def _find(self, prefix: str) -> TrieNode:
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node

    def autocomplete(self, prefix: str, limit: int = 5) -> list[str]:
        node = self._find(prefix)
        if not node:
            return []
        results = []
        self._dfs(node, prefix, results)
        results.sort(key=lambda x: x[1], reverse=True)
        return [word for word, freq in results[:limit]]

    def _dfs(self, node, path, results):
        if node.is_end:
            results.append((path, node.frequency))
        for char, child in node.children.items():
            self._dfs(child, path + char, results)

# Test
trie = Trie()
words = [("python", 100), ("pytorch", 80), ("pandas", 90), ("pip", 70), ("pillow", 30)]
for word, freq in words:
    trie.insert(word, freq)

print(trie.autocomplete("py"))   # ["python", "pytorch"]
print(trie.autocomplete("pa"))   # ["pandas"]
print(trie.search("python"))     # True

# TODO: Delete operasyonu implement et
# TODO: Word Search II (LeetCode #212) — Trie + Backtracking
# TODO: Design Search Autocomplete System (LeetCode #642)
# TODO: Turkce karakter destegi ekle (ğ, ü, ş, ı, ö, ç)
```

**Beklenen Sonuc:** Insert ve search O(m) time (m = kelime uzunlugu). Autocomplete frequency'ye gore sirali sonuc donmeli. Turkce karakterler dogru islenmeli.
**Ipucu:** Trie autocomplete, spell checker ve IP routing'de kullanilir. Memory-efficient varyant: compressed trie (radix tree).
:::

:::realworld
## Gerçek Dünyada DSA Kullanımı

| Şirket | Problem | Kullanılan Algoritma/Veri Yapısı |
|--------|---------|----------------------------------|
| **Google** | Web sayfalarını sıralama | Graph algorithms (PageRank) |
| **Netflix** | Film önerileri | Collaborative filtering + Graph |
| **Uber** | En kısa rota bulma | Dijkstra + A* algoritması |
| **Twitter** | Trending topics | Hash Map + Min Heap (Top-K) |
| **Discord** | Mesaj arama | Trie + Inverted Index |
| **Spotify** | Shuffle oynatma | Fisher-Yates Shuffle (O(n)) |
| **Amazon** | Autocomplete | Trie (Prefix Tree) |
| **Redis** | LRU Cache eviction | Hash Map + Doubly Linked List |
:::

:::external-resource
### Ek Kaynaklar

- [NeetCode.io](https://neetcode.io/) - Pattern bazli problem listesi
- [LeetCode Patterns](https://seanprashad.com/leetcode-patterns/) - Kategorize problemler
- [Visualgo](https://visualgo.net/) - Algoritma gorselleştirme
- [Big-O Cheat Sheet](https://www.bigocheatsheet.com/) - Complexity tablosu
- [Grokking the Coding Interview](https://www.designgurus.io/course/grokking-the-coding-interview) - Pattern bazli kurs
:::

---

## Özet

| Konu | Ana Fikir |
|------|-----------|
| Big-O | O(1) < O(log n) < O(n) < O(n log n) < O(n²) |
| Hash Table | O(1) lookup - interview'larin temeli |
| Two Pointers | Sirali array problemlerinde O(n) çözüm |
| Sliding Window | Alt dizi/string problemlerinde O(n) çözüm |
| Stack | LIFO - parantez, monotonic stack |
| Linked List | Pointer manipulasyonu, LRU Cache |
| BST / Tree | DFS (in/pre/postorder), BFS (level order) |
| Heap | Priority Queue, Top-K problemleri |
| Graph | BFS (shortest path), DFS (explore), Dijkstra (weighted) |
| Sorting | Quick Sort O(n log n) avg, Merge Sort O(n log n) guaranteed |
| DP | Overlapping subproblems - memoization veya tabulation |
| Greedy | Lokal optimal → global optimal |

**Sonraki Adim**: Bu temelleri ogrrendikten sonra, Module 20'de interview hazirlik stratejilerine geciyoruz.
