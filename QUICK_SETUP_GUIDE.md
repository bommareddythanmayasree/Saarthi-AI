# Quick Setup Guide - Hero Background Image

## 🎯 What You Need To Do

You provided an image showing people collaborating at a table. This image needs to be saved to complete the UI styling.

## 📝 Steps

### 1. Save the Image
- Right-click the image you provided in the chat
- Save it as: `hero-bg.jpg`
- Place it in: `static/images/` folder

### 2. Verify the Path
The file should be located at:
```
Saarthi-AI-main/
└── static/
    └── images/
        └── hero-bg.jpg  ← Your image here
```

### 3. Test the Application
Run your Flask application and visit the landing page:
```bash
python app.py
```

Then open: `http://localhost:5000/`

## ✅ What's Already Done

All the CSS and JavaScript code is complete and ready:

- ✅ Hero section configured to use the image
- ✅ Overlay with blur effect (85% opacity)
- ✅ Dark mode overlay support
- ✅ Gradient backgrounds on other pages
- ✅ Glassmorphism on all cards
- ✅ Hover animations
- ✅ Dark mode toggle

## 🎨 Expected Result

### Landing Page Hero Section:
- Background: Your collaborative workspace image
- Overlay: Semi-transparent white (light mode) or dark (dark mode)
- Effect: Subtle blur for professional look
- Text: Clearly readable on top

### Other Pages (Form, Results, Login):
- Background: Smooth gradients (no image)
- Light mode: Light blue gradient
- Dark mode: Dark blue gradient

## 🔧 Optional Adjustments

If you want to adjust the styling after testing:

### Make overlay more/less transparent:
In `static/css/style.css`, line ~356:
```css
background: rgba(255, 255, 255, 0.85);  /* Change 0.85 to 0.7-0.95 */
```

### Make blur stronger/weaker:
In `static/css/style.css`, line ~357:
```css
backdrop-filter: blur(3px);  /* Change 3px to 2px-8px */
```

### Change gradient colors:
In `static/css/style.css`, search for:
```css
background: linear-gradient(135deg, #f8fafc, #eef2ff);
```

## 📱 Mobile Testing

The styling is fully responsive. Test on:
- Desktop (1920x1080+)
- Tablet (768px-1024px)
- Mobile (320px-767px)

## 🎉 That's It!

Once you save the image, everything will work perfectly. The UI will have a modern, professional look with glassmorphism effects and smooth animations.
