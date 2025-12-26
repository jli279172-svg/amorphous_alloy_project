#!/bin/bash
# Master script to run all melt-quench stages sequentially

TOTAL_STAGES=7
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
