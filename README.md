# visualize-code

## Project Architecture

This project uses Manim to visualize coding interview problems (e.g., from Blind 75 and Top 150). To adhere to the **DRY (Don't Repeat Yourself)** principle and maintain consistent styling across all videos, we use a centralized shared components architecture.

### 🧩 `00-shared-components`

Each major course directory (`Blind75`, `Top150`) contains a `00-shared-components` folder. This folder acts as a shared library for standardizing visual elements, preventing code redundancy in individual problem scripts.

#### High-Level Overview of Components

- **`typography.py`**: The core design system. Defines the premium color psychology (e.g., Matte Off-Black background `#1e1e1e`, specific Hex codes for `WHITE`, `YELLOW`, `RED`, `GREEN`, `BLUE`), font families (Inter, Courier New), and sizes.
- **`screenTemplate.py`**: Manages the consistent layout of the screen. Generates titles, target boxes, and the standard Complexity Analysis (TC/SC) panel.
- **`arrayBuilder.py`**: Utilities for constructing and rendering Arrays/Lists, Memory Blocks, and Pointers (i, j, etc.) flawlessly.
- **`highlighter.py`**: Handles visual effects such as border glows, scanning highlights, and status flashes to emphasize specific elements during algorithm execution.
- **`swapAnimator.py`**: Smoothly animates the swapping of elements or nodes.
- **`stepPanel.py`**: For tracking and displaying execution steps dynamically on the screen.

### 🚀 Usage

To use these shared components in any problem's Manim script, ensure the python path is dynamically resolved at the top of your file (right after importing manim):

```python
from manim import *
import sys
from pathlib import Path

# Dynamically append the 00-shared-components directory to the path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent.parent / "00-shared-components"))

# Now you can seamlessly import the components
from components.typography import Typography
```
