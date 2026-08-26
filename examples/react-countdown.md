# Countdown Timer

**Task:** "Build me a countdown timer component in React that counts down from a given number of seconds."

Verbatim model output from a benchmark run — Claude Haiku 4.5, no-skill arm vs ken arm, temperature 1, source `benchmarks/output.json`. Reproduce: `npx promptfoo@latest eval -c benchmarks/promptfooconfig.openrouter.yaml`.

## Without Ken — 241 lines of code

# React Countdown Timer Component

Here's a complete countdown timer component with multiple variations:

## Basic Countdown Timer

```jsx
import { useState, useEffect } from 'react';

function CountdownTimer({ initialSeconds = 60, onComplete }) {
  const [seconds, setSeconds] = useState(initialSeconds);

  useEffect(() => {
    if (seconds <= 0) {
      onComplete?.();
      return;
    }

    const timer = setInterval(() => {
      setSeconds(prev => prev - 1);
    }, 1000);

    return () => clearInterval(timer);
  }, [seconds, onComplete]);

  const formatTime = (totalSeconds) => {
    const hours = Math.floor(totalSeconds / 3600);
    const minutes = Math.floor((totalSeconds % 3600) / 60);
    const secs = totalSeconds % 60;

    if (hours > 0) {
      return `${hours}:${minutes.toString().padStart(2, '0')}:${secs
        .toString()
        .padStart(2, '0')}`;
    }
    return `${minutes}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="countdown-timer">
      <div className="timer-display">{formatTime(seconds)}</div>
      {seconds === 0 && <p className="timer-complete">Time's up!</p>}
    </div>
  );
}

export default CountdownTimer;
```

## Advanced Countdown Timer with Controls

```jsx
import { useState, useEffect, useCallback } from 'react';
import './CountdownTimer.css';

function CountdownTimer({ 
  initialSeconds = 60, 
  onComplete,
  showControls = true 
}) {
  const [seconds, setSeconds] = useState(initialSeconds);
  const [isRunning, setIsRunning] = useState(false);

  useEffect(() => {
    if (!isRunning || seconds <= 0) {
      if (seconds === 0) {
        onComplete?.();
      }
      return;
    }

    const timer = setInterval(() => {
      setSeconds(prev => prev - 1);
    }, 1000);

    return () => clearInterval(timer);
  }, [isRunning, seconds, onComplete]);

  const formatTime = useCallback((totalSeconds) => {
    const hours = Math.floor(totalSeconds / 3600);
    const minutes = Math.floor((totalSeconds % 3600) / 60);
    const secs = totalSeconds % 60;

    const pad = (num) => num.toString().padStart(2, '0');

    if (hours > 0) {
      return `${hours}:${pad(minutes)}:${pad(secs)}`;
    }
    return `${minutes}:${pad(secs)}`;
  }, []);

  const handleStart = () => setIsRunning(true);
  const handlePause = () => setIsRunning(false);
  const handleReset = () => {
    setSeconds(initialSeconds);
    setIsRunning(false);
  };

  const percentage = (seconds / initialSeconds) * 100;
  const isLowTime = seconds <= 10 && seconds > 0;

  return (
    <div className="countdown-container">
      <div className={`timer-display ${isLowTime ? 'low-time' : ''}`}>
        {formatTime(seconds)}
      </div>

      {seconds === 0 && (
        <div className="completion-message">
          ⏰ Time's up!
        </div>
      )}

      {showControls && (
        <div className="timer-controls">
          <button 
            onClick={handleStart} 
            disabled={isRunning || seconds === 0}
            className="btn btn-start"
          >
            Start
          </button>
          <button 
            onClick={handlePause} 
            disabled={!isRunning}
            className="btn btn-pause"
          >
            Pause
          </button>
          <button 
            onClick={handleReset}
            className="btn btn-reset"
          >
            Reset
          </button>
        </div>
      )}

      <div className="progress-bar">
        <div 
          className="progress-fill" 
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
}

export default CountdownTimer;
```

## CSS Styling

```css
/* CountdownTimer.css */

.countdown-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  padding: 30px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 15px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  max-width: 400px;
  margin: 0 auto;
}

.timer-display {
  font-size: 48px;
  font-weight: bold;
  color: white;
  font-family: 'Courier New', monospace;
  letter-spacing: 2px;
  transition: all 0.3s ease;
}

.timer-display.low-time {
  animation: pulse 0.5s infinite;
  color: #ff6b6b;
}

@keyframes pulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
}

.completion-message {
  font-size: 24px;
  color: #ffd700;
  font-weight: bold;
  animation: slideIn 0.5s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.timer-controls {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  justify-content: center;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.btn-start {
  background-color: #51cf66;
  color: white;
}

.btn-start:hover:not(:disabled) {
  background-color: #40c057;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(81, 207, 102, 0.4);
}

.btn-pause {
  background-color: #ffa940;
  color: white;
}

.btn-pause:hover:not(:disabled) {
  background-color: #ff9c1f;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(255, 164, 64, 0.4);
}

.btn-reset {
  background-color: #ff7875;
  color: white;
}

.btn-reset:hover:not(:disabled) {
  background-color: #ff4d4f;
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(255, 77, 79, 0.4);
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.progress-bar {
  width: 100%;
  height: 6px;
  background-color: rgba(255, 255, 255, 0.3);
  border-radius: 3px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background-color: #51cf66;
  transition: width 1s linear;
}
```

## Usage Examples

```jsx
import CountdownTimer from './CountdownTimer';

// Basic usage
function App() {
  return (
    <CountdownTimer 
      initialSeconds={300}
      onComplete={() => alert('Time is up!')}
    />
  );
}

// Without controls
function SimpleTimer() {
  return (
    <CountdownTimer 
      initialSeconds={60}
      showControls={false}
    />
  );
}

export default App;
```

## Features

✅ **Countdown functionality** - Counts down from given seconds  
✅ **Time formatting** - Displays in HH:MM:SS or MM:SS format  
✅ **Start/Pause/Reset controls** - Full control over timer  
✅ **Progress bar** - Visual representation of time remaining  
✅ **Low-time animation** - Pulsing effect when time is running out  
✅ **Completion callback** - Execute function when timer ends  
✅ **Responsive design** - Works on all screen sizes  
✅ **Accessibility** - Disabled buttons have proper styling  

You can customize colors, sizes, and animations in the CSS file!

## With Ken — 30 lines of code

```jsx
import { useState, useEffect } from 'react';

export function CountdownTimer({ initialSeconds }) {
  const [seconds, setSeconds] = useState(initialSeconds);
  const [isRunning, setIsRunning] = useState(false);

  useEffect(() => {
    if (!isRunning || seconds <= 0) return;

    const interval = setInterval(() => {
      setSeconds(s => s - 1);
    }, 1000);

    return () => clearInterval(interval);
  }, [isRunning, seconds]);

  const toggle = () => setIsRunning(!isRunning);
  const reset = () => {
    setSeconds(initialSeconds);
    setIsRunning(false);
  };

  return (
    <div style={{ textAlign: 'center', fontFamily: 'monospace' }}>
      <div style={{ fontSize: '48px', fontWeight: 'bold', margin: '20px 0' }}>
        {seconds}
      </div>
      <button onClick={toggle} style={{ marginRight: '10px', padding: '8px 16px' }}>
        {isRunning ? 'Pause' : 'Start'}
      </button>
      <button onClick={reset} style={{ padding: '8px 16px' }}>
        Reset
      </button>
    </div>
  );
}

// Usage: <CountdownTimer initialSeconds={60} />
```

→ threw away: animation libraries and tone callbacks, ceiling: `// ken: setInterval; switch to requestAnimationFrame if sub-second precision needed`

The thing works: state holds seconds, interval decrements it, buttons control flow. No layers. Pass `initialSeconds` as a prop, get start/pause/reset for free.

**241 → 30 lines of code** — same model, same prompt.
