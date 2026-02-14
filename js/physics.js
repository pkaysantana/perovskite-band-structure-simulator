/**
 * Perovskite Physics Engine (Client-Side)
 * Ports the Python tight-binding model to JavaScript
 * for real-time interactive calculations
 */

// Harrison's Solid State Table parameters
const E_d = -2.0;  // Metal d-orbital energy (Ti 3d) in eV
const E_p = -6.0;  // Oxygen p-orbital energy (O 2p) in eV
const V_pd_sigma_0 = 2.2;  // Hopping parameter at reference bond length (eV)
const d0 = 1.96;   // Reference Ti-O bond length (Angstroms)

/**
 * Perovskite Model Class
 */
class PerovskiteModel {
    constructor(metalSymbol = "Ti") {
        this.metal = metalSymbol;

        // Set d-orbital energy based on metal
        if (metalSymbol === "Ti") {
            this.E_d = -2.0;
        } else if (metalSymbol === "Mn") {
            this.E_d = -4.0;  // Lower d-levels
        } else {
            this.E_d = -2.0;
        }
    }

    /**
     * Calculate effective hopping integral using Harrison's scaling
     * @param {number} d - Bond length in Angstroms
     * @param {number} angleDeg - B-O-B angle in degrees
     * @returns {object} { hoppingIntegral, overlapFactor }
     */
    getHoppingIntegral(d, angleDeg) {
        // Harrison's d^-3.5 scaling law for bond length
        const V_scaled = V_pd_sigma_0 * Math.pow(d0 / d, 3.5);

        // Angular dependence (geometric reduction of overlap)
        // 180° = Max overlap (factor 1.0)
        // Tilt angle represents deviation from perfect overlap
        const tiltRad = (180 - angleDeg) * Math.PI / 180;
        const angularFactor = Math.abs(Math.cos(tiltRad));

        return {
            hoppingIntegral: V_scaled * angularFactor,
            overlapFactor: angularFactor
        };
    }

    /**
     * Solve 2-band tight-binding Hamiltonian
     * @param {number} angleDeg - B-O-B angle in degrees
     * @param {number} dBond - Bond length in Angstroms
     * @param {Array} kPoints - Array of [kx, ky, kz] k-points
     * @returns {object} { bands: [[valence], [conduction]], overlapFactor }
     */
    solveHamiltonian(angleDeg, dBond, kPoints) {
        const { hoppingIntegral: t, overlapFactor } = this.getHoppingIntegral(dBond, angleDeg);

        // Storage for 2 bands
        const valenceBand = [];
        const conductionBand = [];

        for (const k of kPoints) {
            const [kx, ky, kz] = k;

            // Dispersion factor for simple cubic lattice
            const f_k = Math.cos(kx) + Math.cos(ky) + Math.cos(kz);

            // Off-diagonal hybridization element
            const interaction = 2 * t * f_k;

            // 2x2 Hamiltonian matrix:
            // | E_d        interaction |
            // | interaction    E_p     |

            // Eigenvalues for 2x2 symmetric matrix
            const trace = this.E_d + E_p;
            const det = this.E_d * E_p - interaction * interaction;
            const discriminant = trace * trace / 4 - det;

            const sqrtDisc = Math.sqrt(Math.max(0, discriminant));
            const E1 = trace / 2 - sqrtDisc;  // Lower eigenvalue (valence)
            const E2 = trace / 2 + sqrtDisc;  // Upper eigenvalue (conduction)

            valenceBand.push(E1);
            conductionBand.push(E2);
        }

        return {
            bands: [valenceBand, conductionBand],
            overlapFactor: overlapFactor
        };
    }
}

/**
 * Generate k-path for band structure: Gamma -> X -> M -> Gamma
 * @param {number} numPoints - Number of points per segment
 * @returns {Array} Array of [kx, ky, kz] k-points
 */
function generateKPath(numPoints = 100) {
    const path = [];

    // Segment 1: Gamma (0,0,0) -> X (pi,0,0)
    for (let i = 0; i < numPoints; i++) {
        const val = Math.PI * (i / numPoints);
        path.push([val, 0, 0]);
    }

    // Segment 2: X (pi,0,0) -> M (pi,pi,0)
    for (let i = 0; i < numPoints; i++) {
        const val = Math.PI * (i / numPoints);
        path.push([Math.PI, val, 0]);
    }

    // Segment 3: M (pi,pi,0) -> Gamma (0,0,0)
    for (let i = 0; i < numPoints; i++) {
        const val = Math.PI * (1 - i / numPoints);
        path.push([val, val, 0]);
    }

    return path;
}

/**
 * Calculate band statistics
 * @param {Array} valenceBand - Array of valence band energies
 * @param {Array} conductionBand - Array of conduction band energies
 * @returns {object} { bandWidth, bandGap }
 */
function calculateBandStats(valenceBand, conductionBand) {
    const cbMax = Math.max(...conductionBand);
    const cbMin = Math.min(...conductionBand);
    const vbMax = Math.max(...valenceBand);

    return {
        bandWidth: cbMax - cbMin,
        bandGap: cbMin - vbMax
    };
}

// Export for module use (if using ES6 modules)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        PerovskiteModel,
        generateKPath,
        calculateBandStats
    };
}
