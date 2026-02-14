/**
 * Band Structure Plotter using Plotly.js
 */

class BandPlotter {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.layout = {
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(15, 23, 42, 0.5)',
            font: {
                family: 'Inter, sans-serif',
                color: '#f1f5f9'
            },
            xaxis: {
                title: {
                    text: 'k-path: Γ → X → M → Γ',
                    font: { size: 14, color: '#cbd5e1' }
                },
                showgrid: true,
                gridcolor: 'rgba(148, 163, 184, 0.1)',
                zeroline: false,
                showticklabels: false
            },
            yaxis: {
                title: {
                    text: 'Energy (eV)',
                    font: { size: 14, color: '#cbd5e1' }
                },
                showgrid: true,
                gridcolor: 'rgba(148, 163, 184, 0.1)',
                zeroline: true,
                zerolinecolor: 'rgba(251, 191, 36, 0.5)',
                zerolinewidth: 2
            },
            margin: { l: 60, r: 20, t: 20, b: 60 },
            hovermode: 'closest',
            showlegend: true,
            legend: {
                x: 0.02,
                y: 0.98,
                bgcolor: 'rgba(30, 41, 59, 0.8)',
                bordercolor: 'rgba(148, 163, 184, 0.2)',
                borderwidth: 1
            }
        };

        this.config = {
            responsive: true,
            displayModeBar: false
        };
    }

    /**
     * Plot band structure
     * @param {Array} valenceBand - Valence band energies
     * @param {Array} conductionBand - Conduction band energies
     * @param {string} label - Label for the plot
     */
    plot(valenceBand, conductionBand, label = 'Current') {
        const kPoints = Array.from({ length: valenceBand.length }, (_, i) => i);

        const traces = [
            {
                x: kPoints,
                y: valenceBand,
                mode: 'lines',
                name: 'O 2p (Valence)',
                line: {
                    color: '#d946ef',
                    width: 3
                },
                hovertemplate: 'E = %{y:.3f} eV<extra></extra>'
            },
            {
                x: kPoints,
                y: conductionBand,
                mode: 'lines',
                name: 'B d (Conduction)',
                line: {
                    color: '#06b6d4',
                    width: 3
                },
                hovertemplate: 'E = %{y:.3f} eV<extra></extra>'
            }
        ];

        Plotly.newPlot(this.container, traces, this.layout, this.config);
    }

    /**
     * Update plot with animation
     */
    update(valenceBand, conductionBand) {
        const kPoints = Array.from({ length: valenceBand.length }, (_, i) => i);

        Plotly.animate(this.container, {
            data: [
                { y: valenceBand },
                { y: conductionBand }
            ]
        }, {
            transition: { duration: 300, easing: 'cubic-in-out' },
            frame: { duration: 300 }
        });
    }
}
