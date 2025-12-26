#!/bin/bash
# Run script for Melt-Quench Stage 5/7

# Set VASP executable path (modify as needed)
VASP_EXE="vasp_std"  # or "vasp_gam" for Gamma-only

# Stage information
STAGE=5
TOTAL_STAGES=7

echo "=========================================="
echo "Melt-Quench Stage $STAGE/$TOTAL_STAGES"
echo "=========================================="

# Copy input files
if [ $STAGE -eq 1 ]; then
    # First stage: use initial POSCAR
    cp POSCAR_initial POSCAR
else
    # Subsequent stages: use CONTCAR from previous stage
    PREV_STAGE=$((STAGE - 1))
    if [ -f "../stage_04/CONTCAR" ]; then
        cp "../stage_04/CONTCAR" POSCAR
        echo "Using CONTCAR from stage $PREV_STAGE as POSCAR"
    else
        echo "ERROR: CONTCAR from previous stage not found!"
        exit 1
    fi
fi

# Copy INCAR
cp INCAR_stage_05 INCAR

# Ensure POTCAR and KPOINTS exist
if [ ! -f POTCAR ]; then
    echo "ERROR: POTCAR not found!"
    exit 1
fi

if [ ! -f KPOINTS ]; then
    echo "ERROR: KPOINTS not found!"
    exit 1
fi

# Run VASP
echo "Starting VASP calculation..."
$VASP_EXE

# Check if calculation completed successfully
if [ $? -eq 0 ]; then
    echo "Stage $STAGE completed successfully!"
    echo "Final structure saved in CONTCAR"
else
    echo "ERROR: VASP calculation failed!"
    exit 1
fi
