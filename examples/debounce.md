# Debounce

**Task:** "Write a reusable debounce function in vanilla JavaScript: debounce(fn, delay) returns a debounced version of fn that delays calling it until delay ms after the last call."

Verbatim model output from a benchmark run — Claude Haiku 4.5, no-skill arm vs ken arm, temperature 1, source `benchmarks/output.json`. Reproduce: `npx promptfoo@latest eval -c benchmarks/promptfooconfig.openrouter.yaml`.

## Without Ken — 82 lines of code

# Debounce Function in Vanilla JavaScript

Here's a production-ready debounce implementation with multiple variations:

## Basic Implementation

```javascript
function debounce(fn, delay) {
  let timeoutId;
  
  return function(...args) {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn(...args), delay);
  };
}
```

## Usage Example

```javascript
const handleSearch = (query) => {
  console.log('Searching for:', query);
};

const debouncedSearch = debounce(handleSearch, 300);

// Simulating rapid input
debouncedSearch('j');      // Cancelled
debouncedSearch('ja');     // Cancelled
debouncedSearch('java');   // Cancelled
debouncedSearch('javascript'); // Called after 300ms
```

## Advanced Implementation with Cancellation

```javascript
function debounce(fn, delay) {
  let timeoutId;
  
  const debounced = function(...args) {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn(...args), delay);
  };
  
  // Allow manual cancellation
  debounced.cancel = () => clearTimeout(timeoutId);
  
  // Allow immediate invocation
  debounced.flush = function(...args) {
    clearTimeout(timeoutId);
    fn(...args);
  };
  
  return debounced;
}
```

## Usage with Cancellation & Flush

```javascript
const handleResize = (size) => {
  console.log('Window resized to:', size);
};

const debouncedResize = debounce(handleResize, 500);

window.addEventListener('resize', () => {
  debouncedResize(window.innerWidth);
});

// Cancel pending debounce
debouncedResize.cancel();

// Force immediate execution
debouncedResize.flush();
```

## Advanced: Leading Edge & Trailing Edge

```javascript
function debounce(fn, delay, { leading = false, trailing = true } = {}) {
  let timeoutId;
  let lastArgs;
  
  const debounced = function(...args) {
    lastArgs = args;
    
    clearTimeout(timeoutId);
    
    if (leading && !timeoutId) {
      fn(...args);
    }
    
    timeoutId = setTimeout(() => {
      if (trailing) {
        fn(...lastArgs);
      }
      timeoutId = null;
    }, delay);
  };
  
  debounced.cancel = () => clearTimeout(timeoutId);
  debounced.flush = () => {
    if (timeoutId) {
      fn(...lastArgs);
      clearTimeout(timeoutId);
      timeoutId = null;
    }
  };
  
  return debounced;
}
```

## Usage with Options

```javascript
// Only call on leading edge
const debouncedClick = debounce(handleClick, 300, { leading: true, trailing: false });

// Call on both leading and trailing edge
const debouncedInput = debounce(handleInput, 300, { leading: true, trailing: true });
```

## Real-World HTML Example

```html
<input type="text" id="searchInput" placeholder="Search...">

<script>
  function debounce(fn, delay) {
    let timeoutId;
    
    return function(...args) {
      clearTimeout(timeoutId);
      timeoutId = setTimeout(() => fn(...args), delay);
    };
  }

  const performSearch = async (query) => {
    console.log('API call with:', query);
    // const results = await fetch(`/api/search?q=${query}`);
  };

  const debouncedSearch = debounce(performSearch, 500);

  document.getElementById('searchInput').addEventListener('input', (e) => {
    debouncedSearch(e.target.value);
  });
</script>
```

## Key Features

| Feature | Description |
|---------|-------------|
| **Basic** | Simple delay of function execution |
| **Cancel** | Stop pending execution |
| **Flush** | Force immediate execution |
| **Leading** | Execute on first call instead of last |
| **Trailing** | Execute after delay (default behavior) |

Choose the implementation based on your needs—the basic version covers most use cases!

## With Ken — 11 lines of code

```javascript
function debounce(fn, delay) {
  let timeoutId = null;

  return function debounced(...args) {
    clearTimeout(timeoutId);
    timeoutId = setTimeout(() => fn.apply(this, args), delay);
  };
}
```

**Use:**
```javascript
const search = debounce((query) => console.log('search:', query), 300);
search('a');
search('ab');
search('abc'); // logs 'search: abc' after 300ms
```

→ stolen: classic Crockford closure pattern, zero decoration. Ceiling: single threshold only (`ken: single delay; add immediate/trailing options when API needs them measured`).

**82 → 11 lines of code** — same model, same prompt.
