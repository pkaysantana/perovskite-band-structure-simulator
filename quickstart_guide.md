# Quick Start Guide — Perovskite Simulator

## ⚡ 30-Second Launch

1. **Open the app:**

   ```bash
   cd "c:\Users\Don\perovskite-band-simulator\perovskite-band-structure-simulator"
   start index.html
   ```

2. **Wait 2 seconds** for Plotly.js to load

3. **You should see:**
   - Header: "Perovskite Band Structure Simulator"
   - Control panel with angle slider at 180°
   - Three panels: (a) Cubic, (b) Distorted, (c) Band Structure

---

## 🧪 Test the "Aha!" Moment

### Step 1: Verify Initial State

- Panel (a) shows perfect 180° orbital alignment
- Panel (c) band structure shows wide conduction band
- Stats show: **Band Width: 11.35 eV**

### Step 2: Drag the Slider

- Move B–O–B angle from **180° → 150°**
- Watch:
  - ✅ Panel (b) orbitals rotate
  - ✅ Green overlap glow dims
  - ✅ Panel (c) conduction band **narrows**
  - ✅ Stats update: **Band Width: 9.61 eV** (15% drop!)

### Step 3: Test Toggles

- Uncheck "Show Orbital Lobes" → Orbitals disappear, atoms remain
- Uncheck "Show Bonds" → Bond lines disappear
- Re-check both → Everything returns

### Step 4: Change Metal

- Select "Mn (Manganese)" from B-site dropdown
- Band structure shifts (d-level changes)

---

## 🔧 Troubleshooting

### If Plotly plot doesn't appear

- Check browser console (F12) for errors
- Verify Plotly CDN loaded: `https://cdn.plot.ly/plotly-2.27.0.min.js`
- Try a different browser (Chrome, Firefox, Edge all work)

### If Canvas panels are blank

- Check that `js/orbitals.js` loaded correctly
- Console should show: "🚀 Perovskite Simulator: Initializing..."

---

## 📊 Expected Behavior

| Angle | Overlap Factor | Band Width (CB) |
|-------|----------------|-----------------|
| 180° | 1.000 | 11.35 eV |
| 165° | 0.966 | 10.93 eV |
| 150° | 0.866 | 9.61 eV |
| 140° | 0.766 | 8.94 eV |

As angle ↓, both overlap and bandwidth ↓ proportionally.

---

## 🚀 Next: Deploy to GitHub

```bash
git add .
git commit -m "Complete perovskite band structure simulator"
git push origin main
```

Enable Pages in repo settings → Access at `https://username.github.io/repo-name/`
