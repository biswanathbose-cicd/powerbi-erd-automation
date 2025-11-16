# Architecture Overview

This document explains each component of the ERD automation pipeline.

### 1. Data Extraction (DAX Studio)
- Export semantic model metadata
- CSV files contain tables, columns, relationships

### 2. Python Processing
- Sanitize names
- Detect PK and FK
- Merge metadata
- Output Mermaid diagram

### 3. Visualization (Draw.io)
- Mermaid diagram rendered automatically
- Zero manual editing

