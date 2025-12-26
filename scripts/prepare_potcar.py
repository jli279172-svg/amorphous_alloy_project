#!/usr/bin/env python3
"""
Helper script to prepare POTCAR file for VASP calculations.
Concatenates individual element POTCAR files in the correct order.
"""

import os
import sys
import argparse
from pathlib import Path


def find_potcar_files(pp_path, elements):
    """
    Find POTCAR files for given elements.
    
    Parameters:
    -----------
    pp_path : str
        Path to VASP pseudopotential directory (e.g., potpaw_PBE)
    elements : list
        List of element symbols
    
    Returns:
    --------
    dict
        Dictionary mapping element to POTCAR file path
    """
    potcar_files = {}
    pp_path = Path(pp_path)
    
    for element in elements:
        # Try different possible directory names
        possible_names = [
            element,                    # Standard: Fe, Si, B
            f"{element}_pv",           # p valence: Fe_pv
            f"{element}_sv",           # semicore: Fe_sv, Si_sv, B_sv
            f"{element}_d",            # d electrons
        ]
        
        found = False
        for name in possible_names:
            potcar_path = pp_path / name / "POTCAR"
            if potcar_path.exists():
                potcar_files[element] = potcar_path
                print(f"Found POTCAR for {element}: {potcar_path}")
                found = True
                break
        
        if not found:
            # List available options
            print(f"ERROR: POTCAR not found for {element}")
            print(f"  Searched in: {pp_path}")
            print(f"  Tried: {', '.join(possible_names)}")
            
            # Show what's available
            if pp_path.exists():
                available = [d.name for d in pp_path.iterdir() if d.is_dir() and element in d.name]
                if available:
                    print(f"  Available options containing '{element}': {', '.join(available)}")
                else:
                    print(f"  No directories found containing '{element}'")
            return None
    
    return potcar_files


def concatenate_potcar(potcar_files, output_path, elements):
    """
    Concatenate POTCAR files in the correct order.
    
    Parameters:
    -----------
    potcar_files : dict
        Dictionary mapping element to POTCAR file path
    output_path : str
        Output POTCAR file path
    elements : list
        List of elements in order (must match POSCAR)
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"\nConcatenating POTCAR files in order: {' '.join(elements)}")
    print(f"Output: {output_path}")
    
    with open(output_path, 'wb') as outfile:
        for element in elements:
            if element not in potcar_files:
                print(f"ERROR: POTCAR file not found for {element}")
                return False
            
            potcar_path = potcar_files[element]
            print(f"  Adding {element} from {potcar_path}")
            
            with open(potcar_path, 'rb') as infile:
                outfile.write(infile.read())
    
    # Verify
    print(f"\nVerifying POTCAR file...")
    with open(output_path, 'r') as f:
        content = f.read()
        titel_count = content.count('TITEL')
        print(f"  Found {titel_count} element(s) in POTCAR")
        
        if titel_count != len(elements):
            print(f"  WARNING: Expected {len(elements)} elements, found {titel_count}")
        
        # Show element names
        lines = content.split('\n')
        for line in lines:
            if 'TITEL' in line:
                print(f"  {line.strip()}")
    
    print(f"\nPOTCAR file created successfully!")
    return True


def main():
    parser = argparse.ArgumentParser(
        description='Prepare POTCAR file for VASP calculations',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Using VASP pseudopotential library
  python3 prepare_potcar.py --pp-path /opt/vasp/potpaw_PBE --elements Fe Si B
  
  # Using custom POTCAR files
  python3 prepare_potcar.py --custom-pots Fe_POTCAR Si_POTCAR B_POTCAR --elements Fe Si B
  
  # Specify output location
  python3 prepare_potcar.py --pp-path /opt/vasp/potpaw_PBE --elements Fe Si B \\
                            --output outputs/melt_quench_simulation/POTCAR
        """
    )
    
    parser.add_argument(
        '--pp-path',
        type=str,
        help='Path to VASP pseudopotential directory (e.g., /opt/vasp/potpaw_PBE)'
    )
    
    parser.add_argument(
        '--custom-pots',
        nargs='+',
        help='Custom POTCAR file paths (must match --elements order)'
    )
    
    parser.add_argument(
        '--elements',
        nargs='+',
        required=True,
        default=['Fe', 'Si', 'B'],
        help='Element symbols in order (must match POSCAR order). Default: Fe Si B'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        default='outputs/melt_quench_simulation/POTCAR',
        help='Output POTCAR file path. Default: outputs/melt_quench_simulation/POTCAR'
    )
    
    args = parser.parse_args()
    
    # Get script directory and project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    # Resolve output path
    if not Path(args.output).is_absolute():
        output_path = project_root / args.output
    else:
        output_path = Path(args.output)
    
    print("=" * 60)
    print("POTCAR Preparation Script")
    print("=" * 60)
    print(f"Elements: {' '.join(args.elements)}")
    print(f"Output: {output_path}")
    print()
    
    potcar_files = {}
    
    if args.custom_pots:
        # Use custom POTCAR files
        if len(args.custom_pots) != len(args.elements):
            print("ERROR: Number of custom POTCAR files must match number of elements")
            sys.exit(1)
        
        for element, potcar_file in zip(args.elements, args.custom_pots):
            potcar_path = Path(potcar_file)
            if not potcar_path.is_absolute():
                potcar_path = project_root / potcar_path
            
            if not potcar_path.exists():
                print(f"ERROR: POTCAR file not found: {potcar_path}")
                sys.exit(1)
            
            potcar_files[element] = potcar_path
            print(f"Using custom POTCAR for {element}: {potcar_path}")
    
    elif args.pp_path:
        # Find POTCAR files in pseudopotential library
        pp_path = Path(args.pp_path)
        if not pp_path.exists():
            print(f"ERROR: Pseudopotential path does not exist: {pp_path}")
            sys.exit(1)
        
        potcar_files = find_potcar_files(pp_path, args.elements)
        if potcar_files is None:
            sys.exit(1)
    
    else:
        print("ERROR: Must specify either --pp-path or --custom-pots")
        parser.print_help()
        sys.exit(1)
    
    # Concatenate POTCAR files
    success = concatenate_potcar(potcar_files, output_path, args.elements)
    
    if success:
        print("\n" + "=" * 60)
        print("Next steps:")
        print(f"  1. Verify POTCAR matches POSCAR element order")
        print(f"  2. Check ENCUT in INCAR matches POTCAR recommendations")
        print(f"  3. Run VASP calculation")
        print("=" * 60)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()

