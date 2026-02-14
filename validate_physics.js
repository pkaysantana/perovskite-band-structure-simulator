/**
 * Validation Script: Test JS physics port against Python ground truth
 * Run with: node validate_physics.js
 */

const fs = require('fs');
const { PerovskiteModel, generateKPath, calculateBandStats } = require('./js/physics.js');

// Load ground truth from Python
const groundTruth = JSON.parse(fs.readFileSync('ground_truth.json', 'utf8'));

console.log('=== Physics Engine Validation ===\n');

// Test scenarios
const scenarios = [
    { angle: 180.0, d: 1.96, label: 'Cubic (Ideal)' },
    { angle: 150.0, d: 1.96, label: 'Distorted (Tilted)' }
];

const model = new PerovskiteModel('Ti');
const kPath = generateKPath(50);  // Same as Python

let allTestsPassed = true;
const tolerance = 1e-5;

for (const scenario of scenarios) {
    console.log(`\n📊 Testing: ${scenario.label}`);
    console.log(`   Angle: ${scenario.angle}°, Bond: ${scenario.d} Å`);

    // Compute with JS
    const result = model.solveHamiltonian(scenario.angle, scenario.d, kPath);
    const stats = calculateBandStats(result.bands[0], result.bands[1]);

    // Get Python ground truth
    const truth = groundTruth[scenario.label];

    // Compare overlap factor
    const overlapError = Math.abs(result.overlapFactor - truth.overlap_factor);
    const overlapPass = overlapError < tolerance;
    console.log(`   Overlap Factor:`);
    console.log(`     JS:     ${result.overlapFactor.toFixed(6)}`);
    console.log(`     Python: ${truth.overlap_factor.toFixed(6)}`);
    console.log(`     Error:  ${overlapError.toExponential(2)} ${overlapPass ? '✅' : '❌'}`);

    // Compare band width
    const widthError = Math.abs(stats.bandWidth - truth.band_width);
    const widthPass = widthError < tolerance;
    console.log(`   Band Width (CB):`);
    console.log(`     JS:     ${stats.bandWidth.toFixed(6)} eV`);
    console.log(`     Python: ${truth.band_width.toFixed(6)} eV`);
    console.log(`     Error:  ${widthError.toExponential(2)} ${widthPass ? '✅' : '❌'}`);

    // Compare band gap
    const gapError = Math.abs(stats.bandGap - truth.band_gap);
    const gapPass = gapError < tolerance;
    console.log(`   Band Gap:`);
    console.log(`     JS:     ${stats.bandGap.toFixed(6)} eV`);
    console.log(`     Python: ${truth.band_gap.toFixed(6)} eV`);
    console.log(`     Error:  ${gapError.toExponential(2)} ${gapPass ? '✅' : '❌'}`);

    // Sample band values (compare first, middle, last points)
    const sampleIndices = [0, Math.floor(kPath.length / 2), kPath.length - 1];
    let bandValuesPass = true;

    for (const idx of sampleIndices) {
        const jsValence = result.bands[0][idx];
        const pyValence = truth.bands[0][idx];
        const jsConduction = result.bands[1][idx];
        const pyConduction = truth.bands[1][idx];

        const vbError = Math.abs(jsValence - pyValence);
        const cbError = Math.abs(jsConduction - pyConduction);

        if (vbError > tolerance || cbError > tolerance) {
            bandValuesPass = false;
            console.log(`   ❌ Band value mismatch at k-point ${idx}`);
            console.log(`      VB error: ${vbError.toExponential(2)}, CB error: ${cbError.toExponential(2)}`);
        }
    }

    if (bandValuesPass) {
        console.log(`   Band Values: Sample validation passed ✅`);
    }

    const scenarioPass = overlapPass && widthPass && gapPass && bandValuesPass;
    if (!scenarioPass) {
        allTestsPassed = false;
    }

    console.log(`   Status: ${scenarioPass ? '✅ PASS' : '❌ FAIL'}`);
}

console.log('\n' + '='.repeat(50));
if (allTestsPassed) {
    console.log('🎉 ALL TESTS PASSED - Physics port validated!');
    console.log('   Tolerance: < 1e-5');
} else {
    console.log('❌ SOME TESTS FAILED - Check implementation');
    process.exit(1);
}
