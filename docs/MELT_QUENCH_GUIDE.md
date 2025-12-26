# Melt-Quench AIMD Simulation Guide

## Overview

This guide explains how to perform Ab Initio Molecular Dynamics (AIMD) simulations to create an amorphous Fe80Si10B10 alloy using the melt-quench method.

## Temperature Protocol: TEBEG and TEEND

### Understanding Temperature Control in VASP

In VASP MD simulations with Nose-Hoover thermostat:
- **TEBEG**: Starting temperature for the current MD run
- **TEEND**: Target temperature at the end of the current MD run
- **MDALGO = 1**: Enables Nose-Hoover thermostat (NVT ensemble)

### Cooling Strategy

VASP linearly interpolates temperature from TEBEG to TEEND over the course of the MD run. For a melt-quench simulation, you need to run **multiple stages** with gradually decreasing temperatures.

### Recommended Cooling Protocol

For Fe80Si10B10 (2500K → 300K):

| Stage | TEBEG (K) | TEEND (K) | Duration | Purpose |
|-------|-----------|-----------|----------|---------|
| 1 | 2500 | 2500 | 5-10 ps | Equilibrate at melting temperature |
| 2 | 2500 | 2000 | 10 ps | Initial cooling |
| 3 | 2000 | 1500 | 10 ps | Continue cooling |
| 4 | 1500 | 1000 | 10 ps | Mid-range cooling |
| 5 | 1000 | 500 | 10 ps | Lower temperature cooling |
| 6 | 500 | 300 | 10 ps | Final cooling |
| 7 | 300 | 300 | 5-10 ps | Equilibrate at room temperature |

**Total simulation time**: ~60-80 ps

### Calculation Details

For each stage:
- **Time step (POTIM)**: 1.5 fs (0.0015 ps)
- **Steps per stage**: Duration / POTIM
  - Example: 10 ps / 0.0015 ps = ~6667 steps
- **NSW**: Set to the number of steps for each stage

## Key Parameters Explained

### Time Step (POTIM)

- **Recommended**: 1.5 fs (0.0015 ps) for Fe/Si/B systems
- **Range**: 1-2 fs is typically safe
- **Too large**: May cause energy drift, instability
- **Too small**: Wastes computational resources
- **Check**: Monitor energy conservation - if energy drifts significantly, reduce POTIM

### Precision Settings for MD Efficiency

1. **PREC = Fast**
   - Reduces computational cost
   - Sufficient accuracy for MD trajectories
   - For final structure analysis, consider PREC = Normal

2. **ALGO = Fast**
   - Fast electronic minimization
   - Good for MD where exact convergence not critical
   - Alternative: ALGO = VeryFast (even faster, less accurate)

3. **LREAL = Auto**
   - Automatic real-space projection
   - Significantly speeds up calculations
   - VASP automatically determines optimal projection

### Output Settings

- **LWAVE = .FALSE.**: Saves disk space (WAVECAR files are large)
- **LCHARG = .FALSE.**: Saves disk space (CHGCAR files are large)
- **NBLOCK = 1**: Write to XDATCAR every step (frequent trajectory output)
- **KBLOCK = 1**: Write MD information every step

## Running the Simulation

### Step 1: Prepare Input Files

1. **POSCAR**: Use the initial structure from `generate_poscar.py`
2. **INCAR**: Use `INCAR_melt_quench` as template
3. **POTCAR**: Concatenate POTCAR files for Fe, Si, B (in that order)
4. **KPOINTS**: Gamma point only (1x1x1)

### Step 2: Create KPOINTS File

For MD with large supercells, Gamma point is sufficient:

```
Gamma point only
0
Gamma
1 1 1
0 0 0
```

### Step 3: Run Multi-Stage Simulation

You can either:

**Option A**: Manual stage-by-stage
1. Modify INCAR for Stage 1 (TEBEG=2500, TEEND=2500, NSW=3333 for 5 ps)
2. Run VASP
3. Copy CONTCAR to POSCAR for next stage
4. Modify INCAR for Stage 2 (TEBEG=2500, TEEND=2000, NSW=6667 for 10 ps)
5. Repeat for all stages

**Option B**: Use automated script (see `scripts/run_melt_quench.py`)

### Step 4: Monitor Simulation

Check these files during/after simulation:
- **OUTCAR**: Temperature, energy, pressure evolution
- **XDATCAR**: Atomic trajectory
- **CONTCAR**: Final structure (use as POSCAR for next stage)
- **OSZICAR**: Summary of each MD step

### Step 5: Analyze Results

1. **Structure**: Final CONTCAR contains the quenched structure
2. **Trajectory**: XDATCAR contains full atomic trajectory
3. **Thermodynamics**: Extract from OUTCAR:
   - Temperature vs time
   - Energy vs time
   - Volume vs time (if NPT)

## Troubleshooting

### Energy Drift
- **Symptom**: Total energy increases/decreases systematically
- **Solution**: Reduce POTIM (try 1.0 fs)

### Temperature Oscillations
- **Symptom**: Large temperature fluctuations
- **Solution**: Adjust SMASS (try 2-5), or increase equilibration time

### Structure Issues
- **Symptom**: Atoms too close, unrealistic bonds
- **Solution**: Check initial structure, ensure proper minimum distances

### Convergence Problems
- **Symptom**: Electronic minimization not converging
- **Solution**: Increase NELM, or use ALGO = Normal

## Computational Considerations

- **Typical runtime**: 60-80 ps total simulation time
- **For 100 atoms**: ~100-200 CPU hours per ps (depends on system)
- **Total cost**: ~6000-16000 CPU hours for full melt-quench
- **Optimization**: Use LREAL=Auto, PREC=Fast to reduce cost

## References

- VASP Manual: MDALGO, TEBEG, TEEND parameters
- Nose-Hoover thermostat theory
- Metallic glass formation mechanisms

