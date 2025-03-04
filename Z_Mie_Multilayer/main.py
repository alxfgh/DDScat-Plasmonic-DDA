import os
import math
import json
import numpy as np
from itertools import combinations


def generate_boundaries(n_shells):
    if n_shells == 1:
        yield (40,)
    else:
        for comb in combinations(range(36, 40), n_shells - 1):
            yield tuple(list(comb) + [40])


def generate_shell_configurations():
    core_comp = "Pena-Rioux_dielectric_26Au_74Ag"
    shell_comps = [
        "Pena-Rioux_dielectric_34Au_66Ag",
        "Pena-Rioux_dielectric_52Au_48Ag",
        "Pena-Rioux_dielectric_65Au_35Ag",
        "Pena-Rioux_dielectric_76Au_24Ag",
        "Pena-Rioux_dielectric_85Au_15Ag",
        "Pena-Rioux_dielectric_92Au_8Ag",
        "Au_evap",
    ]
    allowed_gold_rich = {
        "Pena-Rioux_dielectric_76Au_24Ag",
        "Pena-Rioux_dielectric_85Au_15Ag",
        "Pena-Rioux_dielectric_92Au_8Ag",
        "Au_evap",
    }

    configs = []
    for n_shells in range(1, 6):
        for boundaries in generate_boundaries(n_shells):
            for comps in combinations(shell_comps, n_shells):
                if comps[-1] not in allowed_gold_rich:
                    continue
                configs.append(
                    {
                        "n_shells": n_shells,
                        "boundaries": boundaries,
                        "compositions": comps,
                        "core": core_comp,
                    }
                )
    return configs


def generate_mie_settings(layers, output_file, start_wl=300, stop_wl=600, interval=1):
    # settings expected by the multilayer mie code
    settings = {
        "numLayers": len(layers),
        "dielectricData": [f"../../diel/{comp}" for (_, comp) in layers],
        "radii": [radius for (radius, _) in layers],
        "dielectricColumns": [1, 2],  # assumes real and imaginary parts in cols 1 & 2
        "startWavelength": start_wl,
        "stopWavelength": stop_wl,
        "intervalWavelength": interval,
        "outputFileName": output_file,
    }
    return settings


def main():
    configs = generate_shell_configurations()
    base_dir = "all_mie_40nm"
    os.makedirs(base_dir, exist_ok=True)
    csv_entries = []

    for cfg in configs:
        n_shells = cfg["n_shells"]
        boundaries = cfg["boundaries"]
        comps = cfg["compositions"]
        core_comp = cfg["core"]

        # Define layers: core fixed at 35 nm, shells per boundaries.
        layers = [(35, core_comp)]
        for b, comp in zip(boundaries, comps):
            layers.append((b, comp))

        boundaries_str = "boundaries" + "-".join(str(b) for b in boundaries)
        comps_str = "comps" + "_".join(comp for comp in comps)
        config_dir = os.path.join(base_dir, boundaries_str, comps_str)
        os.makedirs(config_dir, exist_ok=True)

        # Create mieSettings.txt in config_dir
        output_file = os.path.join(config_dir, "mieOutput.txt")
        settings = generate_mie_settings(layers, output_file)
        settings_path = os.path.join(config_dir, "mieSettings.txt")
        with open(settings_path, "w") as f:
            json.dump(settings, f, indent=4)

        # Invoke the multilayer Mie simulation (update the path to your mie code)
        os.system(f"python mie_multilayer.py {settings_path}")

        csv_entries.append(config_dir)

    with open(os.path.join(base_dir, "config_paths.csv"), "w") as f:
        f.write("path\n" + "\n".join(csv_entries))


if __name__ == "__main__":
    main()
