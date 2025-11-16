# Automated ER Diagram Generation for Power BI  
### Power BI → DAX Studio → Python → Mermaid → Draw.io

This repository contains a complete end-to-end workflow for automatically generating ER Diagrams from any Power BI `.pbix` model.

Power BI does not provide a native ERD export — so this project fills that gap through automation.

---

## 🚀 Features

- Extract metadata directly from Power BI (via DAX Studio)
- Merge metadata using Python
- Automatically detect:
  - Primary Keys (PK)
  - Foreign Keys (FK)
  - Cardinality (One-to-Many, Many-to-One)
- Generate a clean Mermaid `model.mmd` file
- Visualize instantly in Draw.io Mermaid editor
- Zero manual diagramming

---

## 📁 Repository Structure


