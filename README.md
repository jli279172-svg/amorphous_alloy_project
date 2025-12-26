# Amorphous Alloy Project

This project generates initial random packed structures for amorphous alloys in VASP POSCAR format.

## Project Structure

```
amorphous_alloy_project/
├── scripts/          # Python scripts for structure generation
├── data/            # Input data files
├── outputs/         # Generated output files (POSCAR, etc.)
└── docs/            # Documentation files
```

## Current Implementation

### 1. Fe80Si10B10 Amorphous Alloy Generator

**Script**: `scripts/generate_poscar.py`

**Specifications**:
- Composition: Fe80 Si10 B10 (atomic percent)
- Total atoms: 100 (80 Fe, 10 Si, 10 B)
- Target density: 7.2 g/cm³
- Box type: Cubic simulation box
- Algorithm: Random insertion with minimum distance check
- Minimum distance: 2.0 Å

**Usage**:
```bash
cd amorphous_alloy_project
python3 scripts/generate_poscar.py
```

**Output**: 
- `outputs/POSCAR_initial` - VASP format POSCAR file with direct coordinates

## Algorithm Details

The script uses a simple random insertion algorithm:
1. Calculates the cubic box side length based on target density and composition
2. Places atoms randomly one by one
3. Checks minimum distance constraint (2.0 Å) against all previously placed atoms
4. Uses periodic boundary conditions (minimum image convention) for distance calculations
5. Outputs positions in direct coordinates (0 to 1) as required by VASP

## Dependencies

- Python 3.x
- NumPy

## Notes

- The random seed is set to 42 for reproducibility
- Minimum distance is set to 1.8 Å (slightly reduced from 2.0 Å for better packing efficiency)
- If atom placement fails, the algorithm will automatically try with a slightly relaxed distance (95% of original)
- The generated structure is a random packed initial configuration suitable for further relaxation
- All output files are automatically saved to the `outputs/` directory

### 2. Melt-Quench AIMD Simulation Setup

**Scripts and Files**:
- `data/INCAR_melt_quench`: Template INCAR file for melt-quench AIMD
- `scripts/run_melt_quench.py`: Automated script to generate multi-stage simulation files
- `docs/MELT_QUENCH_GUIDE.md`: Comprehensive guide for melt-quench simulations

**Features**:
- NVT ensemble with Nose-Hoover thermostat
- Multi-stage cooling protocol (2500K → 300K)
- Optimized parameters for efficient MD calculations
- Automated stage management

**Quick Start**:
```bash
# 1. Generate simulation files
python3 scripts/run_melt_quench.py

# 2. Prepare POTCAR file
# Option A: Using VASP pseudopotential library
python3 scripts/prepare_potcar.py --pp-path /path/to/vasp/potpaw_PBE --elements Fe Si B

# Option B: Using custom POTCAR files
python3 scripts/prepare_potcar.py --custom-pots Fe_POTCAR Si_POTCAR B_POTCAR --elements Fe Si B

# 3. Run all stages
cd outputs/melt_quench_simulation
./run_all_stages.sh
```

See `docs/POTCAR_GUIDE.md` (English) or `docs/POTCAR_GUIDE_CN.md` (中文) for detailed POTCAR preparation instructions.

**下载 POTCAR 文件**:
- **使用 vaspkit（推荐）**: `scripts/prepare_potcar_vaspkit.py` - 自动生成 POTCAR
- **手动方法**: `scripts/download_potcar.py` - 检查 VASP 安装和现有文件
- **详细指南**: 
  - `docs/VASPKIT_POTCAR_GUIDE_CN.md` - vaspkit 使用指南（中文）
  - `docs/POTCAR_DOWNLOAD_GUIDE_CN.md` - 手动下载指南（中文）

See `docs/MELT_QUENCH_GUIDE.md` for detailed instructions.

