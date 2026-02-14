/**
 * Orbital Renderer - Canvas-based visualization with radial gradients
 * Draws d and p orbitals and their overlap regions
 */

class OrbitalRenderer {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        this.width = this.canvas.width;
        this.height = this.canvas.height;
        this.centerX = this.width / 2;
        this.centerY = this.height / 2;
    }

    /**
     * Clear the canvas
     */
    clear() {
        this.ctx.clearRect(0, 0, this.width, this.height);
    }

    /**
     * Draw a radial gradient orbital lobe (electron density cloud)
     * @param {number} x - Center x position
     * @param {number} y - Center y position
     * @param {number} size - Radius of the orbital
     * @param {string} color - Base color (e.g., '#06b6d4')
     * @param {number} opacity - Opacity factor
     */
    drawOrbitalLobe(x, y, size, color, opacity = 0.6) {
        const gradient = this.ctx.createRadialGradient(x, y, 0, x, y, size);

        // Create electron density probability cloud effect
        gradient.addColorStop(0, this.hexToRgba(color, opacity * 0.8));
        gradient.addColorStop(0.5, this.hexToRgba(color, opacity * 0.4));
        gradient.addColorStop(1, this.hexToRgba(color, 0));

        this.ctx.fillStyle = gradient;
        this.ctx.beginPath();
        this.ctx.arc(x, y, size, 0, 2 * Math.PI);
        this.ctx.fill();
    }

    /**
     * Helper to convert hex color to rgba
     */
    hexToRgba(hex, alpha) {
        const r = parseInt(hex.slice(1, 3), 16);
        const g = parseInt(hex.slice(3, 5), 16);
        const b = parseInt(hex.slice(5, 7), 16);
        return `rgba(${r}, ${g}, ${b}, ${alpha})`;
    }

    /**
     * Draw a bond line
     */
    drawBond(x1, y1, x2, y2, color = '#94a3b8', lineWidth = 2) {
        this.ctx.strokeStyle = color;
        this.ctx.lineWidth = lineWidth;
        this.ctx.beginPath();
        this.ctx.moveTo(x1, y1);
        this.ctx.lineTo(x2, y2);
        this.ctx.stroke();
    }

    /**
     * Draw an atom nucleus
     */
    drawAtom(x, y, label, color = '#06b6d4', radius = 12) {
        // Nucleus circle
        this.ctx.fillStyle = color;
        this.ctx.beginPath();
        this.ctx.arc(x, y, radius, 0, 2 * Math.PI);
        this.ctx.fill();

        // Label
        this.ctx.fillStyle = '#f1f5f9';
        this.ctx.font = 'bold 14px Inter';
        this.ctx.textAlign = 'center';
        this.ctx.textBaseline = 'middle';
        this.ctx.fillText(label, x, y);
    }

    /**
     * Render orbital overlap diagram
     * @param {number} angle - B-O-B angle in degrees
     * @param {boolean} showLobes - Whether to show orbital lobes
     * @param {boolean} showBonds - Whether to show bond lines
     */
    renderOverlap(angle, showLobes = true, showBonds = true) {
        this.clear();

        // Geometry parameters
        const bondLength = 100; // pixels
        const angleRad = (angle * Math.PI) / 180;

        // Central B cation (transition metal)
        const bX = this.centerX;
        const bY = this.centerY;

        // Two oxygen positions (simplified 2D linear geometry)
        // Left oxygen
        const o1X = bX - bondLength;
        const o1Y = bY;

        // Right oxygen - position depends on angle
        // For perfect 180°, it's straight across
        // For smaller angles, it tilts
        const deviation = Math.PI - angleRad;
        const o2X = bX + bondLength * Math.cos(deviation);
        const o2Y = bY + bondLength * Math.sin(deviation);

        // Draw bonds first (so they appear behind orbitals)
        if (showBonds) {
            this.drawBond(o1X, o1Y, bX, bY, '#475569', 3);
            this.drawBond(bX, bY, o2X, o2Y, '#475569', 3);
        }

        // Draw orbital lobes
        if (showLobes) {
            // B-site d-orbitals (4 lobes in typical d_{x2-y2} pattern)
            const dSize = 40;
            const dColor = '#06b6d4'; // Cyan for d-orbitals

            // Four lobes around B
            this.drawOrbitalLobe(bX + dSize * 0.7, bY, dSize, dColor, 0.7);
            this.drawOrbitalLobe(bX - dSize * 0.7, bY, dSize, dColor, 0.7);
            this.drawOrbitalLobe(bX, bY + dSize * 0.7, dSize, dColor, 0.7);
            this.drawOrbitalLobe(bX, bY - dSize * 0.7, dSize, dColor, 0.7);

            // O-site p-orbitals (2 lobes each, p_sigma pointing toward B)
            const pSize = 35;
            const pColor = '#d946ef'; // Magenta for p-orbitals

            // Left oxygen p-orbital (pointing right toward B)
            this.drawOrbitalLobe(o1X + pSize * 0.6, o1Y, pSize, pColor, 0.7);
            this.drawOrbitalLobe(o1X - pSize * 0.6, o1Y, pSize, pColor, 0.5);

            // Right oxygen p-orbital (rotated according to angle)
            const pRightAngle = deviation;
            const p2aX = o2X - pSize * 0.6 * Math.cos(pRightAngle);
            const p2aY = o2Y - pSize * 0.6 * Math.sin(pRightAngle);
            const p2bX = o2X + pSize * 0.6 * Math.cos(pRightAngle);
            const p2bY = o2Y + pSize * 0.6 * Math.sin(pRightAngle);

            this.drawOrbitalLobe(p2aX, p2aY, pSize, pColor, 0.7);
            this.drawOrbitalLobe(p2bX, p2bY, pSize, pColor, 0.5);

            // Draw overlap region indicator (intensity based on angle)
            const overlapFactor = Math.abs(Math.cos((180 - angle) * Math.PI / 180));

            // Overlap glow between B and O1
            const midX1 = (bX + o1X) / 2;
            const midY1 = (bY + o1Y) / 2;
            this.drawOrbitalLobe(midX1, midY1, 25, '#10b981', overlapFactor * 0.8);

            // Overlap glow between B and O2
            const midX2 = (bX + o2X) / 2;
            const midY2 = (bY + o2Y) / 2;
            this.drawOrbitalLobe(midX2, midY2, 25, '#10b981', overlapFactor * 0.8);
        }

        // Draw atoms on top
        this.drawAtom(bX, bY, 'B', '#06b6d4', 14);
        this.drawAtom(o1X, o1Y, 'O', '#d946ef', 12);
        this.drawAtom(o2X, o2Y, 'O', '#d946ef', 12);

        // Draw angle arc and label
        this.drawAngleArc(bX, bY, bondLength * 0.3, Math.PI, Math.PI + deviation, angle);
    }

    /**
     * Draw an angle arc with label
     */
    drawAngleArc(x, y, radius, startAngle, endAngle, angleDeg) {
        this.ctx.strokeStyle = '#fbbf24';
        this.ctx.lineWidth = 2;
        this.ctx.beginPath();
        this.ctx.arc(x, y, radius, startAngle, endAngle);
        this.ctx.stroke();

        // Angle label
        const midAngle = (startAngle + endAngle) / 2;
        const labelX = x + (radius + 20) * Math.cos(midAngle);
        const labelY = y + (radius + 20) * Math.sin(midAngle);

        this.ctx.fillStyle = '#fbbf24';
        this.ctx.font = '12px Inter';
        this.ctx.textAlign = 'center';
        this.ctx.fillText(`${angleDeg.toFixed(0)}°`, labelX, labelY);
    }
}
