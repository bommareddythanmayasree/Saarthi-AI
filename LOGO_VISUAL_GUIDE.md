# Logo Visual Guide

## Quick Reference

### Logo Sizes

```
Landing Page Header:  70px  ████████████████
Form Page:           100px  ███████████████████████
Login Page:           80px  ████████████████████
```

---

## Page-by-Page Breakdown

### 1. Landing Page (Header)

**Location**: Navigation bar at top
**Size**: 70px
**Color**: White (filtered)
**Background**: Blue header

```css
.logo-image {
    height: 70px;
    filter: brightness(0) invert(1);
}
```

**Visual**:
```
┌─────────────────────────────────────┐
│ [LOGO] Home  Features  About  Login │ ← Blue header
└─────────────────────────────────────┘
   ↑ White logo, 70px
```

---

### 2. Student Info Form Page

**Location**: Top center of page
**Size**: 100px (largest)
**Background**: White with rounded corners
**Dark Mode**: Slightly more opaque white

```css
.form-logo-image {
    height: 100px;
    padding: 0.75rem 1.5rem;
    background: rgba(255, 255, 255, 0.95);
    border-radius: 12px;
}
```

**Visual**:
```
        ┌──────────────┐
        │   [LOGO]     │ ← Subtle white background
        │   100px      │    with rounded corners
        └──────────────┘
    
    Student Information Form
```

**Dark Mode**:
```
        ┌──────────────┐
        │   [LOGO]     │ ← More opaque white
        │   100px      │    background (0.98)
        └──────────────┘
```

---

### 3. Login Page

**Location**: Top center of page
**Size**: 80px
**Background**: None (natural)

```css
.login-logo-image {
    height: 80px;
}
```

**Visual**:
```
        [LOGO]
         80px
    
    Navigating your future
      with intelligence
    
    ┌─────────────────┐
    │  Welcome back   │
    │                 │
    │  [Login Form]   │
    └─────────────────┘
```

---

## Dark Mode Comparison

### Header Logo:
```
Light Mode:  [LOGO] ← White on blue
Dark Mode:   [LOGO] ← White on blue (same)
```

### Form Logo:
```
Light Mode:  ┌──────────┐
             │  [LOGO]  │ ← 95% white background
             └──────────┘

Dark Mode:   ┌──────────┐
             │  [LOGO]  │ ← 98% white background
             └──────────┘
```

### Login Logo:
```
Light Mode:  [LOGO] ← Natural on light gradient
Dark Mode:   [LOGO] ← Natural on dark gradient
```

---

## Size Comparison

```
Header (70px):   ████████████████
Login (80px):    ████████████████████
Form (100px):    ███████████████████████
```

**Rationale**:
- **Form page**: Largest (100px) - main focus, needs visibility
- **Login page**: Medium (80px) - prominent but not overwhelming
- **Header**: Smaller (70px) - proportional to navigation

---

## Background Styling

### Form Logo Background:

**Light Mode**:
- Color: `rgba(255, 255, 255, 0.95)` - 95% opaque white
- Padding: `0.75rem 1.5rem` - comfortable spacing
- Border radius: `12px` - soft rounded corners
- Shadow: `0 2px 8px rgba(0, 0, 0, 0.1)` - subtle depth

**Dark Mode**:
- Color: `rgba(255, 255, 255, 0.98)` - 98% opaque white
- Shadow: `0 2px 8px rgba(0, 0, 0, 0.3)` - stronger shadow

**Result**: Subtle, blended appearance (not boxy)

---

## Color Filters

### Header Logo (White on Blue):

```css
filter: brightness(0) invert(1);
```

**How it works**:
1. `brightness(0)` - Makes image black
2. `invert(1)` - Inverts to white

**Result**: Logo appears white on blue header

---

## Consistency Check

✅ **Same Image File**:
```
Landing:  images/saarthi-logo.png
Form:     images/saarthi-logo.png
Login:    images/saarthi-logo.png
```

✅ **Proper Sizing**:
- All logos proportional to their context
- Larger where it's the main focus
- Smaller in navigation

✅ **Dark Mode**:
- All logos visible in dark mode
- Appropriate styling for each context

---

## Quick Test Guide

### To Verify Changes:

1. **Landing Page**:
   - Logo should be 70px (larger than before)
   - Logo should be white
   - Logo should align with navigation

2. **Form Page**:
   - Logo should be 100px (largest)
   - Logo should have subtle white background
   - Toggle dark mode - logo should remain visible

3. **Login Page**:
   - Logo should be actual image (not graduation cap)
   - Logo should be 80px
   - Logo should be centered

4. **Consistency**:
   - All pages should use same logo image
   - Sizing should be proportional
   - All should be clearly visible

---

## Status

✅ All logos updated and consistent
✅ Proper sizing on all pages
✅ Dark mode visibility fixed
✅ Professional appearance maintained
