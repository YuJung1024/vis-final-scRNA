This project provides an interactive visualization for exploring single-cell (scRNA-seq) and single-nucleus (snRNA-seq) RNA sequencing data integration from Mouse Brain Organoids.

##  Project Structure

The `Final` directory contains all necessary files to deploy the static web visualization:

```
Final/
├── index.html          # Main application file (Visualization Dashboard)
├── data/               # Processed data files (JSON format)
│   ├── cells.json      # Cell metadata and embedding coordinates
│   ├── clusters.json   # Cluster information (names, colors)
│   └── gene_expression.json # Expression data for selected genes
└── README.md           # This documentation
```

##  Website Design & Features

### 1. Data Visualization (Center Panel)
- **Scatter Plot**: Displays ~1,500 cells/nuclei in a 2D embedding space.
- **Methods Supported**:
  - **SupCPM**: Supervised Capacity Preserving Mapping (Custom integration method).
  - **UMAP**: Uniform Manifold Approximation and Projection.
  - **t-SNE**: t-Distributed Stochastic Neighbor Embedding.
  - **PCA**: Principal Component Analysis.
- **Interactions**:
  - **Zoom/Pan**: Use mouse wheel to zoom, click and drag to pan.
  - **Hover**: View basic cell information (ID, Type, Cluster).
  - **Click**: Select a specific cell to view detailed statistics.

### 2. Control Panel (Top Left)
The main control hub for the dashboard:
- **Embedding Method**: Switch between different dimensionality reduction techniques (SupCPM, UMAP, t-SNE, PCA).
- **View Mode**:
  - **Type**: Color cells by sequencing type (scRNA vs. snRNA).
  - **Cluster**: Color cells by their identified cluster (Leiden clustering).
- **Gene Expression**:
  - Dropdown menu to select specific genes.
  - Coloring changes to a blue gradient representing expression intensity (Low to High).
  - **Gene Selection Logic**: The available genes include:
    - **All Variable Genes**: Includes all 2000 highly variable genes (HVGs) identified during the analysis pipeline.
    - **Top Expressed Genes**: Includes high-expression housekeeping genes.
    - **Marker Genes**: Includes cell-type specific markers for detailed exploration.
- **Search**:
  - **Autocomplete**: Type a Cell ID to see matching suggestions.
  - **Highlight**: Selecting a cell highlights it in the plot and dims others.
- **Filter**: Slider to hide low-quality cells based on the minimum number of detected genes.

### 3. Details Panel (Right)
Appears when a cell is selected:
- **Metadata**: Shows Cell ID, Gene Count, Mitochondrial Percentage, Type, and Cluster.
- **Marker Genes Chart**: Displays the expression levels of key marker genes for the selected cell as a bar chart.

### 4. Minimap (Bottom Right)
- Provides a high-level view of the entire dataset.
- The blue rectangle indicates the current viewport area.
- Click or drag on the minimap to navigate quickly.

##  Data Processing
- **Source Data**: GSE161340 (Mouse Brain Organoid).
- **Processing**:
  - Data was processed using Scanpy in Python.
  - Integration performed using SupCPM.
  - Exported to optimized JSON files for web performance using `export_integration_data.py`.

##  How to Run
Simply open `index.html` in a modern web browser. No backend server is required as it uses static JSON data.
For local development, you can use a simple python server:
```bash
python3 -m http.server
```
Then navigate to `http://localhost:8000`.

