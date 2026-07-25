#!/usr/bin/env zsh
# Shell script to build STL files for Samsung Galaxy Tab A7 IKEA Skådis Mount using PythonSCAD CLI

PYTHONSCAD_BIN="/Applications/PythonSCAD.app/Contents/MacOS/PythonSCAD"

if [[ ! -f "$PYTHONSCAD_BIN" ]]; then
  echo "Error: PythonSCAD executable not found at $PYTHONSCAD_BIN"
  exit 1
fi

echo "Building left_bracket.stl..."
"$PYTHONSCAD_BIN" --trust-python -D RENDER_MODE=\"left\" -o left_bracket.stl samsung_mount.py

echo "Building right_bracket.stl..."
"$PYTHONSCAD_BIN" --trust-python -D RENDER_MODE=\"right\" -o right_bracket.stl samsung_mount.py

echo "Building full_assembly.stl..."
"$PYTHONSCAD_BIN" --trust-python -D RENDER_MODE=\"assembly\" -o full_assembly.stl samsung_mount.py

echo "Build complete! STL files ready for PrusaSlicer."
