# Weight Calculator

A Fusion 360 script for calculating the total weight of a speaker enclosure design. It combines the weight of the enclosure bodies (based on material density and volume) with the weight of the speaker driver to give you a complete weight estimate.

## How It Works

1. Collects all selected solid bodies in the viewport (or all bodies in the design if none are selected)
2. Prompts you to choose an enclosure material preset
3. Prompts you to enter the speaker driver weight
4. Calculates enclosure weight from body volumes × material density, then adds the driver weight
5. Displays a full weight breakdown in a dialog

## Installation

1. Open Fusion 360
2. Go to **Utilities → Add-Ins → Scripts and Add-Ins**
3. Click the green **+** icon next to **My Scripts**
4. Navigate to the folder containing this script and select it

## Usage

1. Open the design you want to weigh
2. Optionally select specific solid bodies in the viewport (if nothing is selected, all bodies in the design are used)
3. Go to **Utilities → Add-Ins → Scripts and Add-Ins**
4. Select **WeightCalculator** and click **Run**
5. Choose a material from the list
6. Enter the speaker driver weight in kilograms (enter `0` if not applicable)
7. A weight summary will be displayed

## Material Presets

| Material | Density |
|---|---|
| Plywood | 680 kg/m³ |
| MDF | 750 kg/m³ |

To add or change materials, edit the `MATERIAL_PRESETS` list at the top of `WeightCalculator.py`.

## Requirements

- Autodesk Fusion 360
- At least one solid body in the active design

## Supported OS

Windows, macOS
