import adsk.core, adsk.fusion, traceback

MATERIAL_PRESETS = [
    ("Plywood", 680.0),
    ("MDF",     750.0),
]

def _to_kg(grams):
    return grams / 1000.0


def _ask(ui, prompt, title, default):
    """Show an inputBox and return (text, cancelled)."""
    result, cancelled = ui.inputBox(prompt, title, default)
    return result, cancelled


def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface

        # ── 1. Collect selected solid bodies ─────────────────────────────────
        bodies = []
        for i in range(ui.activeSelections.count):
            entity = ui.activeSelections.item(i).entity
            if isinstance(entity, adsk.fusion.BRepBody):
                bodies.append(entity)

        if not bodies:
            # Fall back to all bodies in the entire design (root + all sub-components)
            design = adsk.fusion.Design.cast(app.activeProduct)
            if design:
                root = design.rootComponent
                for i in range(root.bRepBodies.count):
                    bodies.append(root.bRepBodies.item(i))
                for occ in root.allOccurrences:
                    comp = occ.component
                    for i in range(comp.bRepBodies.count):
                        bodies.append(comp.bRepBodies.item(i))

        if not bodies:
            ui.messageBox(
                "No solid bodies found in the active design.",
                "Weight Calculator",
            )
            return

        # ── 2. Material density ───────────────────────────────────────────────
        mat_lines = ["Choose a material:\n"]
        for i, (lbl, val) in enumerate(MATERIAL_PRESETS, 1):
            mat_lines.append(f"  {i}.  {lbl}  ({val} kg/m³)")
        mat_lines.append("\nEnter 1 or 2:")
        mat_text, cancelled = _ask(ui, "\n".join(mat_lines), "Weight Calculator – Material", "1")
        if cancelled:
            return

        try:
            mat_choice = int(mat_text.strip())
            if not 1 <= mat_choice <= 2:
                raise ValueError
        except ValueError:
            ui.messageBox("Invalid choice. Please enter 1 or 2.", "Weight Calculator")
            return

        label, density_kg_m3 = MATERIAL_PRESETS[mat_choice - 1]

        # ── 3. Driver weight ──────────────────────────────────────────────────
        driver_text, cancelled = _ask(ui, "Enter driver weight (kg):", "Weight Calculator – Driver", "0")
        if cancelled:
            return

        try:
            driver_kg = float(driver_text.strip())
            if driver_kg < 0:
                raise ValueError
        except ValueError:
            ui.messageBox("Invalid weight. Please enter a positive number.", "Weight Calculator")
            return

        # ── 4. Calculate ─────────────────────────────────────────────────────
        density_g_cm3 = density_kg_m3 * 0.001   # 1 kg/m³ = 0.001 g/cm³

        total_grams = 0.0
        for body in bodies:
            total_grams += body.volume * density_g_cm3

        body_kg  = _to_kg(total_grams)
        total_kg = body_kg + driver_kg

        # ── 5. Results ────────────────────────────────────────────────────────
        summary = []
        summary.append("TOTAL WEIGHT")
        summary.append("=" * 36)
        summary.append(f"  Bodies  : {body_kg:.1f} kg")
        summary.append(f"  Driver  : {driver_kg:.1f} kg")
        summary.append(f"  Total   : {total_kg:.1f} kg")
        summary.append("")
        summary.append(f"Bodies   : {len(bodies)}")
        summary.append(f"Material : {label}  ({density_kg_m3:.1f} kg/m³)")
        ui.messageBox("\n".join(summary), "Weight Calculator")

    except Exception:
        if ui:
            ui.messageBox("Weight Calculator error:\n" + traceback.format_exc())
