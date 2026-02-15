# DEPLOYMENT PROTOCOL v1.0

**Target:** `perovskite-band-structure-simulator` → GitHub Pages  
**Architecture:** Static HTML/JS (No build step required)  
**Status:** Production-ready

---

## 1. Activation Sequence (The "Happy Path")

### Step 1.1: Navigate to Repository Settings

1. Open your GitHub repository: `https://github.com/[your-username]/perovskite-band-structure-simulator`
2. Click the **Settings** tab (top navigation bar, far right)
3. Locate **Pages** in the left sidebar menu (under "Code and automation" section)
4. Click **Pages**

### Step 1.2: Configure Deployment Source

1. Under **Build and deployment**, locate the **Source** dropdown
2. Select: **Deploy from a branch**
3. Under **Branch**, configure:
   - **Branch selector**: Select **main**
   - **Folder selector**: Select **/ (root)**
4. **CRITICAL**: Click the **Save** button

**Expected behavior:** Page will refresh. A blue info box will appear stating "GitHub Pages source saved."

---

## 2. Verification (The "Pulse Check")

### Step 2.1: Monitor Deployment Workflow

1. Navigate to the **Actions** tab (top navigation bar)
2. Locate the workflow run: **pages-build-deployment**
3. Observe the status indicator:
   - **Yellow spinner**: Deployment in progress (wait 30-60 seconds)
   - **Green checkmark**: Deployment successful
   - **Red X**: Deployment failed (see troubleshooting below)

### Step 2.2: Confirm Deployment Success

Once the green checkmark appears:

1. Return to **Settings** → **Pages**
2. At the top of the page, you will see: **"Your site is live at [URL]"**
3. The URL will be: `https://[your-username].github.io/perovskite-band-structure-simulator/`

---

## 3. Live URL Prediction

**Constructed URL format:**

```
https://[your-username].github.io/perovskite-band-structure-simulator/
```

**Example:**

- If your GitHub username is `pkaysantana`, the URL will be:

  ```
  https://pkaysantana.github.io/perovskite-band-structure-simulator/
  ```

### Propagation Delay Warning

- **First 60 seconds**: 404 errors are normal (DNS propagation)
- **After 60 seconds**: Site should be accessible
- **If 404 persists beyond 5 minutes**: Check Actions tab for deployment errors

### Custom Domain Warning

**DO NOT modify the "Custom domain" field** unless you own a domain and have configured DNS records. Incorrect settings will break the deployment.

---

## 4. Smoke Test (Post-Deploy)

### Test 4.1: Visual Load Verification

1. Open the live URL in a browser
2. **Expected result**: Dark-mode interface with three panels visible
3. **Failure mode**: White screen or "404 Not Found" → Re-check Actions tab

### Test 4.2: Console Error Check

1. Press **F12** to open Developer Tools
2. Navigate to the **Console** tab
3. **Expected result**: No red error messages (warnings in yellow are acceptable)
4. **Failure mode**: Red errors mentioning "Failed to load resource" → Check file paths in `index.html`

### Test 4.3: Interactive Physics Validation

1. Locate the **B–O–B Angle** slider in the control panel
2. Drag the slider from **180°** → **150°**
3. **Expected results:**
   - Panel (b) orbital lobes rotate smoothly
   - Panel (c) band structure plot animates (conduction band narrows)
   - Stats update: **Band Width** changes from **11.35 eV** → **9.61 eV**
4. **Failure mode**: No animation → JavaScript not executing (check Console for errors)

### Test 4.4: Cross-Browser Compatibility

Test on at least two browsers:

- **Chrome/Edge** (Chromium-based)
- **Firefox** (Gecko-based)
- **Safari** (WebKit-based, if on macOS)

**Expected result:** Identical behavior across all browsers.

---

## 5. Troubleshooting

### Issue: 404 Error After 5 Minutes

**Diagnosis:** Deployment failed or incorrect branch/folder settings.  
**Fix:**

1. Go to **Actions** tab → Check for red X on `pages-build-deployment`
2. Click the failed workflow → Review error logs
3. Common causes:
   - Wrong branch selected (must be `main`)
   - Wrong folder selected (must be `/ (root)`)
   - Missing `index.html` in root directory

### Issue: Red Console Errors

**Diagnosis:** JavaScript files not loading.  
**Fix:**

1. Check `index.html` script tags (lines 136-140):

   ```html
   <script src="js/physics.js"></script>
   <script src="js/orbitals.js"></script>
   <script src="js/plotter.js"></script>
   <script src="js/app.js"></script>
   ```

2. Verify all files exist in the `js/` directory
3. Ensure file names match exactly (case-sensitive on Linux servers)

### Issue: Plotly.js Not Loading

**Diagnosis:** CDN blocked or network issue.  
**Fix:**

1. Check line 12 in `index.html`:

   ```html
   <script src="https://cdn.plot.ly/plotly-2.27.0.min.js"></script>
   ```

2. Test CDN URL directly in browser
3. If CDN is down, download Plotly.js locally and update path

### Issue: Slider Works But No Animation

**Diagnosis:** `app.js` initialization failure.  
**Fix:**

1. Open Console (F12)
2. Look for: `🚀 Perovskite Simulator: Initializing...`
3. If missing, check for JavaScript syntax errors in `app.js`

---

## 6. Post-Deployment Checklist

- [ ] URL is accessible from multiple devices
- [ ] All three panels render correctly
- [ ] Slider animation works smoothly
- [ ] Console shows no red errors
- [ ] Stats update in real-time (Band Width, Band Gap)
- [ ] Mobile responsive design verified (optional)

---

## 7. Rollback Procedure

If deployment fails catastrophically:

1. Go to **Settings** → **Pages**
2. Under **Source**, select **None**
3. Click **Save**
4. Wait 60 seconds
5. Re-enable by selecting **main** / **/ (root)** again

---

## 8. Security Notes

- **No secrets required**: This is a static site (no API keys, no backend)
- **No HTTPS configuration needed**: GitHub Pages enforces HTTPS automatically
- **No CORS issues**: All resources are same-origin or CDN-based

---

## 9. Performance Expectations

- **First load**: ~500ms (Plotly.js CDN download)
- **Subsequent loads**: ~50ms (browser cache)
- **Slider response**: <350ms (physics computation + rendering)
- **Lighthouse score**: 90+ (Performance, Accessibility, Best Practices)

---

## 10. Final Validation Command

Run this checklist after deployment:

```
✅ URL loads without 404
✅ Dark-mode theme visible
✅ Three panels present (a, b, c)
✅ Slider moves smoothly (140° to 180°)
✅ Band structure plot animates
✅ Stats update dynamically
✅ No console errors (F12)
✅ Mobile view acceptable (optional)
```

**If all checks pass:** Deployment successful. Site is production-ready.

---

**END OF PROTOCOL**
