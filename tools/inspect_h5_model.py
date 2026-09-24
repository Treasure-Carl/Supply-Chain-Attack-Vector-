#!/usr/bin/env python3
"""
Inspect a Keras .h5 model file's layer architecture without loading
or executing the model. Uses h5py to read the file structure directly.

Usage: python3 inspect_h5_model.py <path_to_h5_file>
"""
import sys
import os
import json
import h5py

SUSPICIOUS_LAYER_TYPES = {"Lambda", "CustomLayer"}

def inspect_model(filepath):
    filename = os.path.basename(filepath)
    print(f"\n=== Architecture Inspection: {filename} ===\n")

    with h5py.File(filepath, "r") as f:
        raw = f.attrs["model_config"]
        model_config = json.loads(raw if isinstance(raw, str) else raw.decode("utf-8"))

    layers = model_config["config"]["layers"]
    print(f"  Total layers: {len(layers)}\n")

    warnings = []
    for layer in layers:
        class_name = layer["class_name"]
        layer_name = layer["config"]["name"]

        if class_name in SUSPICIOUS_LAYER_TYPES:
            func_name = layer["config"].get("function", {})
            if isinstance(func_name, dict):
                func_name = func_name.get("config", "unknown")
            detail = f" (function: {func_name})" if class_name == "Lambda" else ""
            print(f"  [WARNING] {class_name:<20} {layer_name}{detail}")
            exfil_suffix = layer["config"].get("exfil_suffix")
            if exfil_suffix:
                print(f"            exfil_suffix: {exfil_suffix}")
            warnings.append((class_name, layer_name))
        else:
            print(f"  [OK]      {class_name:<20} {layer_name}")

    print()
    if warnings:
        print(f"  RESULT: {len(warnings)} layer(s) require review")
        for cls, name in warnings:
            print(f"    - {cls} ({name}): Can contain arbitrary Python code that executes at inference time")
    else:
        print("  RESULT: All layers are standard. No suspicious layers detected.")
    print()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 inspect_h5_model.py <path_to_h5_file>")
        sys.exit(1)
    inspect_model(sys.argv[1])
