# scRNA-seq Visualization Platform

An interactive web-based visualization platform for exploring single-cell RNA sequencing (scRNA-seq) data from mouse hippocampus tissue across different ages.

## Overview

This project provides an intuitive interface to analyze and compare cell population distributions, gene expression changes, and biological differences between young (4-month) and old (24-month) mice using various dimensionality reduction techniques.

**Authors:** 吳帛恩、葉子禎、徐鈺蓉

## Features

### Data Visualization
- **Multiple Dimensionality Reduction Methods:**
  - SupCPM (Supervised Capacity Preserving Mapping)
  - UMAP (Uniform Manifold Approximation and Projection)
  - t-SNE (t-Distributed Stochastic Neighbor Embedding)
  - PCA (Principal Component Analysis)

### Interactive Analysis
- **Dynamic View Modes:**
  - Color by sequencing type (scRNA vs. snRNA)
  - Color by cluster (Leiden clustering)
  - Gene expression visualization with gradient coloring

- **Exploration Tools:**
  - Zoom and pan navigation
  - Cell search with autocomplete
  - Hover for quick cell information
  - Click for detailed cell statistics
  - Quality filtering by gene count

- **Gene Expression Analysis:**
  - 2000+ highly variable genes (HVGs)
  - Top expressed housekeeping genes
  - Cell-type specific marker genes
  - Expression intensity visualization

### User Interface
- Modern glassmorphism design
- Responsive layout
- Real-time data updates
- Minimap for quick navigation
- Detailed cell information panel

## Dataset

**Source:** [GSE161340](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE161340)

- **Technology:** Single Cell and Single Nucleus Droplet Based RNA-sequencing
- **Tissue:** Hippocampus from mice
- **Age Groups:** 4-month (young) and 24-month (old) mice
- **Scale:**
  - 1,544 individual cells
  - 27,998 unique genes
  - 3,214,219 non-zero gene counts

**Processing Pipeline:**
- Analysis performed using Scanpy (Python)
- Integration via SupCPM
- Data exported to optimized JSON format for web performance

## Installation

### Prerequisites
- Python 3.9 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd vis-final-scRNA
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows
```

3. Install dependencies:
```bash
pip install -r requirememt.txt
```

Required packages:
- Flask==3.1.2
- numpy==2.3.4
- pandas==2.3.3
- scanpy==1.11.5
- anndata==0.12.6

## Usage

### Running the Application

1. Start the Flask server:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:5001
```

3. The application will launch with the overview page. Use the sidebar to navigate between:
   - **Overview:** Project information and dataset details
   - **DR Analysis:** Interactive dimensionality reduction visualization

### Navigation Guide

**Control Panel (Top Left):**
- Select embedding method (SupCPM/UMAP/t-SNE/PCA)
- Choose view mode (Type/Cluster/Gene Expression)
- Search for specific cells by ID
- Filter cells by minimum gene count

**Main Visualization (Center):**
- Zoom: Mouse wheel
- Pan: Click and drag
- Hover: View cell information
- Click: Select cell for detailed view

**Details Panel (Right):**
- Appears when a cell is selected
- Shows cell metadata and marker gene expression

**Minimap (Bottom Right):**
- Overview of entire dataset
- Blue rectangle shows current viewport
- Click to navigate quickly

## Project Structure

```
vis-final-scRNA/
├── app.py                 # Flask application and API endpoints
├── index.html             # Main application entry point
├── requirememt.txt        # Python dependencies
├── pages/
│   ├── home.html          # Overview page
│   └── downsampling.html  # DR analysis page
├── static/
│   └── js/
│       └── main.js        # Client-side JavaScript
├── downsampling/
│   └── data/              # Preprocessed visualization data (JSON)
├── analysis/
│   └── dataloader.py      # Data loading utilities
├── GSE161340/             # Raw dataset files
└── cache/                 # Cached analysis results
```

## Technologies Used

### Backend
- Flask (Web framework)
- Pandas (Data manipulation)
- NumPy (Numerical computing)
- Scanpy (Single-cell analysis)
- AnnData (Annotated data structures)

### Frontend
- D3.js v7 (Data visualization)
- Tailwind CSS (Styling framework)
- MDUI (Material Design components)
- Marked.js (Markdown parsing)

## API Endpoints

- `GET /` - Main application page
- `GET /api/datasets` - List available datasets
- `POST /api/load_dataset` - Load specific dataset
- `POST /api/analyze` - Analysis endpoint (reserved for future features)

## References

### Bio+MedVis Challenge @ IEEE VIS 2024
Kleshchevnikov, V., Shmatko, A., Dann, E. et al. *Cell2location maps fine-grained cell types in spatial transcriptomics.* Nat Biotechnol 40, 661–671 (2022). [DOI](https://doi.org/10.1038/s41587-021-01139-4)

### Reference-free cell type deconvolution
Miller, B.F., Huang, F., Atta, L. et al. *Reference-free cell type deconvolution of multi-cellular pixel-resolution spatially resolved transcriptomics data.* Nat Commun 13, 2339 (2022). [DOI](https://doi.org/10.1038/s41467-022-30033-z)

### Optimal Dimensionality Selection Using Hull Heatmaps for Single-Cell Analysis
Jeong, Haejin & Jeong, Hyoung‐oh & Lee, Semin & Jeong, Won-Ki. (2025). Optimal Dimensionality Selection Using Hull Heatmaps for Single‐Cell Analysis. Computer Graphics Forum. 44. 10.1111/cgf.70151. [DOI](https://doi.org/10.1111/cgf.70151)

## License

This project is created for academic purposes as part of coursework at NCCU.

## Acknowledgments

- Dataset source: GEO (GSE161340)
- Analysis pipeline: Scanpy framework
- Visualization inspiration: Bio+MedVis Challenge @ IEEE VIS 2024

---

© 2025 scRNA Visualization Platform
