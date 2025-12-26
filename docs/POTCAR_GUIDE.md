# POTCAR File Preparation Guide

## Overview

POTCAR (Pseudopotential) files are required for VASP calculations. These files contain the pseudopotentials for each element in your system. For Fe80Si10B10, you need POTCAR files for Fe, Si, and B.

## Obtaining POTCAR Files

### Option 1: From VASP Pseudopotential Library (Recommended)

VASP provides pseudopotential libraries that you need to access. These are typically located in:
- `/path/to/vasp/pseudopotentials/` (on your VASP installation)
- Or download from VASP website (if you have access)

**Steps:**

1. **Locate your VASP pseudopotential directory**
   ```bash
   # Common locations:
   # - /opt/vasp/potpaw_PBE/
   # - /usr/local/vasp/potpaw_PBE/
   # - $VASP_PP_PATH/potpaw_PBE/
   ```

2. **Find the appropriate pseudopotential versions**
   - For Fe: Look for `Fe`, `Fe_pv`, `Fe_sv`, etc.
   - For Si: Look for `Si`, `Si_sv`, etc.
   - For B: Look for `B`, `B_sv`, etc.

3. **Choose pseudopotential versions:**
   - **Fe**: `Fe` or `Fe_pv` (with p valence) - recommended for metallic systems
   - **Si**: `Si` (standard) or `Si_sv` (semicore)
   - **B**: `B` (standard) or `B_sv` (semicore)

4. **Concatenate POTCAR files in the correct order:**
   ```bash
   cd /path/to/vasp/potpaw_PBE/
   cat Fe/POTCAR Si/POTCAR B/POTCAR > /path/to/project/outputs/melt_quench_simulation/POTCAR
   ```

### Option 2: Using Helper Script

Use the provided helper script to prepare POTCAR:

```bash
python3 scripts/prepare_potcar.py --pp-path /path/to/vasp/potpaw_PBE/ --elements Fe Si B
```

### Option 3: Manual Preparation

If you have individual POTCAR files:

1. **Create a temporary directory:**
   ```bash
   mkdir -p data/potcars
   ```

2. **Copy or download POTCAR files:**
   - Place `Fe_POTCAR`, `Si_POTCAR`, `B_POTCAR` in `data/potcars/`

3. **Concatenate them:**
   ```bash
   cd data/potcars
   cat Fe_POTCAR Si_POTCAR B_POTCAR > ../../outputs/melt_quench_simulation/POTCAR
   ```

## Important Notes

### Element Order

**CRITICAL**: The order of elements in POTCAR must match the order in POSCAR!

For Fe80Si10B10:
- POSCAR has: `Fe Si B` (line 6)
- POTCAR must be: `Fe POTCAR + Si POTCAR + B POTCAR`

### Pseudopotential Selection

- **Fe**: Use `Fe` or `Fe_pv` for metallic iron
- **Si**: Use `Si` (standard) is usually sufficient
- **B**: Use `B` (standard) is usually sufficient

For high-accuracy calculations, consider:
- `Fe_pv`: Includes p valence electrons
- `Si_sv`: Semicore version
- `B_sv`: Semicore version

### Verification

After creating POTCAR, verify it:

```bash
# Check number of atoms matches
grep "TITEL" POTCAR  # Should show 3 elements
head -1 POTCAR       # Should show Fe
```

### Common Issues

1. **Wrong element order**: POTCAR order must match POSCAR
2. **Missing elements**: All elements in POSCAR must be in POTCAR
3. **Version mismatch**: Ensure all POTCARs are from the same library (e.g., all PBE)
4. **File format**: POTCAR should be a single concatenated file, not separate files

## Example Workflow

```bash
# 1. Find VASP pseudopotential path
export VASP_PP_PATH=/path/to/vasp/potpaw_PBE

# 2. Verify elements exist
ls $VASP_PP_PATH/Fe/
ls $VASP_PP_PATH/Si/
ls $VASP_PP_PATH/B/

# 3. Create POTCAR
cat $VASP_PP_PATH/Fe/POTCAR \
    $VASP_PP_PATH/Si/POTCAR \
    $VASP_PP_PATH/B/POTCAR \
    > outputs/melt_quench_simulation/POTCAR

# 4. Verify
head -5 outputs/melt_quench_simulation/POTCAR
grep "TITEL" outputs/melt_quench_simulation/POTCAR
```

## Checking POTCAR Compatibility

Before running VASP, verify:

1. **Element count matches POSCAR:**
   ```bash
   # Count elements in POSCAR (line 6)
   head -6 POSCAR | tail -1
   # Should show: Fe Si B
   
   # Count elements in POTCAR
   grep -c "TITEL" POTCAR
   # Should show: 3
   ```

2. **ENCUT compatibility:**
   - Check recommended ENCUT in POTCAR: `grep ENMAX POTCAR`
   - Use the maximum value in INCAR (or higher)
   - Current INCAR uses ENCUT = 400 eV

## References

- VASP Manual: Pseudopotentials
- VASP Wiki: POTCAR preparation
- Your VASP installation documentation

