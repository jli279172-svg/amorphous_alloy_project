#!/usr/bin/env python3
"""
Automated script to run multi-stage melt-quench AIMD simulation.
Generates INCAR files for each cooling stage and prepares run scripts.
"""

import os
import shutil
from pathlib import Path


# Cooling protocol: (TEBEG, TEEND, duration_ps, description)
COOLING_STAGES = [
    (2500, 2500, 10, "Equilibration at melting temperature"),
    (2500, 2000, 10, "Initial cooling"),
    (2000, 1500, 10, "Mid-high temperature cooling"),
    (1500, 1000, 10, "Mid-range cooling"),
    (1000, 500, 10, "Lower temperature cooling"),
    (500, 300, 10, "Final cooling"),
    (300, 300, 10, "Equilibration at room temperature"),
]

# MD parameters
POTIM = 0.0015  # Time step in ps (1.5 fs)
PREC = "Fast"
ALGO = "Fast"
LREAL = "Auto"
ENCUT = 400


def calculate_nsw(duration_ps, potim_ps):
    """Calculate number of MD steps from duration and time step."""
    return int(duration_ps / potim_ps)


def generate_incar(stage_num, tebeg, teend, nsw, output_dir):
    """Generate INCAR file for a specific stage."""
    incar_content = f"""# ============================================================
# VASP INCAR for Melt-Quench AIMD - Stage {stage_num}
# Temperature: {tebeg}K -> {teend}K
# ============================================================

SYSTEM = Fe80Si10B10 Melt-Quench Stage {stage_num} ({tebeg}K->{teend}K)

# Basic Settings
PREC = {PREC}
ALGO = {ALGO}
LREAL = {LREAL}
ENCUT = {ENCUT}
EDIFF = 1E-4

# Molecular Dynamics
IBRION = 0
NSW = {nsw}
POTIM = {POTIM}

# Temperature Control (NVT - Nose-Hoover)
MDALGO = 1
SMASS = 3
TEBEG = {tebeg}
TEEND = {teend}

# Output Settings
LWAVE = .FALSE.
LCHARG = .FALSE.
NBLOCK = 1
KBLOCK = 1
NWRITE = 0

# Electronic Structure
ISMEAR = 0
SIGMA = 0.2
NELM = 60
NELMIN = 4

# MD Settings
ISIF = 2

# Restart
ISTART = 1
ICHARG = 1
"""
    
    incar_path = os.path.join(output_dir, f"INCAR_stage_{stage_num:02d}")
    with open(incar_path, 'w') as f:
        f.write(incar_content)
    
    return incar_path


def generate_run_script(stage_num, total_stages, base_dir):
    """Generate a run script for a specific stage."""
    prev_stage = stage_num - 1
    prev_stage_str = f"{prev_stage:02d}" if prev_stage > 0 else "00"
    
    script_content = f"""#!/bin/bash
# Run script for Melt-Quench Stage {stage_num}/{total_stages}

# Set VASP executable path (modify as needed)
VASP_EXE="vasp_std"  # or "vasp_gam" for Gamma-only

# Stage information
STAGE={stage_num}
TOTAL_STAGES={total_stages}

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
    if [ -f "../stage_{prev_stage_str}/CONTCAR" ]; then
        cp "../stage_{prev_stage_str}/CONTCAR" POSCAR
        echo "Using CONTCAR from stage $PREV_STAGE as POSCAR"
    else
        echo "ERROR: CONTCAR from previous stage not found!"
        exit 1
    fi
fi

# Copy INCAR
cp INCAR_stage_{stage_num:02d} INCAR

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
"""
    
    script_path = os.path.join(base_dir, f"run_stage_{stage_num:02d}.sh")
    with open(script_path, 'w') as f:
        f.write(script_content)
    
    # Make executable
    os.chmod(script_path, 0o755)
    
    return script_path


def generate_master_script(total_stages, output_dir):
    """Generate a master script to run all stages sequentially."""
    script_content = f"""#!/bin/bash
# Master script to run all melt-quench stages sequentially

TOTAL_STAGES={total_stages}
BASE_DIR="$(pwd)"

echo "=========================================="
echo "Melt-Quench AIMD Simulation"
echo "Total Stages: $TOTAL_STAGES"
echo "=========================================="

for stage in $(seq 1 $TOTAL_STAGES); do
    STAGE_DIR="$BASE_DIR/stage_$(printf "%02d" $stage)"
    
    echo ""
    echo "=========================================="
    echo "Starting Stage $stage/$TOTAL_STAGES"
    echo "=========================================="
    
    # Create stage directory
    mkdir -p "$STAGE_DIR"
    cd "$STAGE_DIR"
    
    # Copy necessary files
    cp "$BASE_DIR/INCAR_stage_$(printf "%02d" $stage)" INCAR
    cp "$BASE_DIR/run_stage_$(printf "%02d" $stage).sh" run.sh
    
    # Copy POTCAR and KPOINTS (should be in base directory)
    if [ -f "$BASE_DIR/POTCAR" ]; then
        cp "$BASE_DIR/POTCAR" .
    fi
    if [ -f "$BASE_DIR/KPOINTS" ]; then
        cp "$BASE_DIR/KPOINTS" .
    fi
    
    # Get POSCAR
    if [ $stage -eq 1 ]; then
        cp "$BASE_DIR/POSCAR_initial" POSCAR
    else
        PREV_STAGE=$((stage - 1))
        PREV_DIR="$BASE_DIR/stage_$(printf "%02d" $PREV_STAGE)"
        if [ -f "$PREV_DIR/CONTCAR" ]; then
            cp "$PREV_DIR/CONTCAR" POSCAR
        else
            echo "ERROR: CONTCAR from stage $PREV_STAGE not found!"
            exit 1
        fi
    fi
    
    # Run the stage
    echo "Running stage $stage..."
    ./run.sh
    
    if [ $? -ne 0 ]; then
        echo "ERROR: Stage $stage failed!"
        exit 1
    fi
    
    cd "$BASE_DIR"
done

echo ""
echo "=========================================="
echo "All stages completed successfully!"
echo "Final structure: stage_$(printf "%02d" $TOTAL_STAGES)/CONTCAR"
echo "=========================================="
"""
    
    script_path = os.path.join(output_dir, "run_all_stages.sh")
    with open(script_path, 'w') as f:
        f.write(script_content)
    
    os.chmod(script_path, 0o755)
    return script_path


def generate_kpoints(output_dir):
    """Generate KPOINTS file for Gamma-point only MD."""
    kpoints_content = """Gamma point only
0
Gamma
1 1 1
0 0 0
"""
    
    kpoints_path = os.path.join(output_dir, "KPOINTS")
    with open(kpoints_path, 'w') as f:
        f.write(kpoints_content)
    
    return kpoints_path


def main():
    """Main function to generate all simulation files."""
    # Get project root directory
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    data_dir = project_root / "data"
    outputs_dir = project_root / "outputs"
    
    # Create simulation directory
    sim_dir = outputs_dir / "melt_quench_simulation"
    sim_dir.mkdir(parents=True, exist_ok=True)
    
    print("Generating melt-quench simulation files...")
    print(f"Output directory: {sim_dir}")
    print(f"\nCooling Protocol:")
    print(f"{'Stage':<8} {'TEBEG (K)':<12} {'TEEND (K)':<12} {'Duration (ps)':<15} {'Steps':<10}")
    print("-" * 65)
    
    total_stages = len(COOLING_STAGES)
    incar_files = []
    
    for i, (tebeg, teend, duration, description) in enumerate(COOLING_STAGES, 1):
        nsw = calculate_nsw(duration, POTIM)
        print(f"{i:<8} {tebeg:<12} {teend:<12} {duration:<15} {nsw:<10}")
        
        # Generate INCAR
        incar_path = generate_incar(i, tebeg, teend, nsw, sim_dir)
        incar_files.append(incar_path)
        
        # Generate run script
        generate_run_script(i, total_stages, sim_dir)
    
    # Generate master script
    master_script = generate_master_script(total_stages, sim_dir)
    
    # Generate KPOINTS
    kpoints_path = generate_kpoints(sim_dir)
    
    # Copy POSCAR_initial if it exists
    poscar_initial = outputs_dir / "POSCAR_initial"
    if poscar_initial.exists():
        shutil.copy(poscar_initial, sim_dir / "POSCAR_initial")
        print(f"\nCopied POSCAR_initial to simulation directory")
    else:
        print(f"\nWARNING: POSCAR_initial not found. Please generate it first.")
    
    print(f"\n{'='*65}")
    print("Files generated:")
    print(f"  - {total_stages} INCAR files (INCAR_stage_XX)")
    print(f"  - {total_stages} run scripts (run_stage_XX.sh)")
    print(f"  - 1 master script (run_all_stages.sh)")
    print(f"  - KPOINTS file")
    print(f"\nNext steps:")
    print(f"  1. Prepare POTCAR file (concatenate Fe, Si, B POTCARs)")
    print(f"  2. Place POTCAR in: {sim_dir}")
    print(f"  3. Review INCAR files and adjust parameters if needed")
    print(f"  4. Run: cd {sim_dir} && ./run_all_stages.sh")
    print(f"{'='*65}")


if __name__ == "__main__":
    main()

