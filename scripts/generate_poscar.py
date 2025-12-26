#!/usr/bin/env python3
"""
Generate a POSCAR file for an amorphous Fe80Si10B10 alloy.
Uses random insertion with minimum distance check to avoid atom overlap.
"""

import numpy as np
import random

# Atomic masses (in atomic mass units)
ATOMIC_MASSES = {
    'Fe': 55.845,
    'Si': 28.085,
    'B': 10.811
}

# Avogadro's number
AVOGADRO = 6.02214076e23

# Conversion factor: amu to grams
AMU_TO_G = 1.66053906660e-24

# Angstrom to cm conversion
ANGSTROM_TO_CM = 1e-8


def calculate_box_size(composition, num_atoms, target_density):
    """
    Calculate cubic box side length based on composition and target density.
    
    Parameters:
    -----------
    composition : dict
        Dictionary with element symbols as keys and counts as values
    num_atoms : int
        Total number of atoms
    target_density : float
        Target density in g/cm³
    
    Returns:
    --------
    float
        Box side length in Angstroms
    """
    # Calculate total mass
    total_mass_amu = sum(composition[element] * ATOMIC_MASSES[element] 
                         for element in composition)
    
    # Convert to grams
    total_mass_g = total_mass_amu * AMU_TO_G
    
    # Calculate required volume (cm³)
    volume_cm3 = total_mass_g / target_density
    
    # Convert to Angstrom³
    volume_ang3 = volume_cm3 / (ANGSTROM_TO_CM ** 3)
    
    # Calculate cubic box side length
    box_length = volume_ang3 ** (1.0 / 3.0)
    
    return box_length


def generate_random_positions(num_atoms, box_length, min_distance=2.0, max_attempts=50000):
    """
    Generate random atomic positions with minimum distance constraint.
    
    Parameters:
    -----------
    num_atoms : int
        Number of atoms to place
    box_length : float
        Side length of cubic box
    min_distance : float
        Minimum distance between atoms in Angstroms
    max_attempts : int
        Maximum number of attempts to place each atom
    
    Returns:
    --------
    numpy.ndarray
        Array of shape (num_atoms, 3) with atomic positions in direct coordinates
    """
    positions = []
    min_distance_sq = min_distance ** 2
    
    # Convert positions list to numpy array for faster computation
    positions_array = None
    
    for i in range(num_atoms):
        attempts = 0
        placed = False
        
        # For efficiency, only check against nearby atoms if we have many
        # For the first few atoms, check all; for later atoms, we can optimize
        check_all = len(positions) < 20
        
        while not placed and attempts < max_attempts:
            # Generate random position in direct coordinates (0 to 1)
            new_pos = np.array([random.random(), random.random(), random.random()])
            
            # Check distance to existing atoms
            too_close = False
            
            if check_all or positions_array is None:
                # Check all existing atoms
                for existing_pos in positions:
                    # Calculate distance in direct coordinates
                    diff = new_pos - existing_pos
                    # Apply periodic boundary conditions (minimum image convention)
                    diff = diff - np.round(diff)
                    # Convert to Cartesian for distance calculation
                    diff_cart = diff * box_length
                    dist_sq = np.dot(diff_cart, diff_cart)
                    
                    if dist_sq < min_distance_sq:
                        too_close = True
                        break
            else:
                # Vectorized check for efficiency
                diffs = new_pos - positions_array
                diffs = diffs - np.round(diffs)
                diffs_cart = diffs * box_length
                dists_sq = np.sum(diffs_cart ** 2, axis=1)
                if np.any(dists_sq < min_distance_sq):
                    too_close = True
            
            if not too_close:
                positions.append(new_pos)
                # Update array for vectorized operations
                if len(positions) > 20:
                    positions_array = np.array(positions)
                placed = True
            
            attempts += 1
        
        if not placed:
            # Try with slightly relaxed distance as fallback
            relaxed_distance = min_distance * 0.95
            relaxed_distance_sq = relaxed_distance ** 2
            print(f"Warning: Failed to place atom {i+1} with {min_distance} Å constraint. "
                  f"Trying with relaxed distance {relaxed_distance:.2f} Å...")
            
            attempts = 0
            while attempts < max_attempts:
                new_pos = np.array([random.random(), random.random(), random.random()])
                too_close = False
                
                for existing_pos in positions:
                    diff = new_pos - existing_pos
                    diff = diff - np.round(diff)
                    diff_cart = diff * box_length
                    dist_sq = np.dot(diff_cart, diff_cart)
                    
                    if dist_sq < relaxed_distance_sq:
                        too_close = True
                        break
                
                if not too_close:
                    positions.append(new_pos)
                    if len(positions) > 20:
                        positions_array = np.array(positions)
                    placed = True
                    break
                
                attempts += 1
            
            if not placed:
                raise RuntimeError(f"Failed to place atom {i+1} even with relaxed distance. "
                                 f"Try reducing min_distance or increasing box size.")
    
    return np.array(positions)


def write_poscar(filename, composition, positions, box_length):
    """
    Write POSCAR file in VASP format.
    
    Parameters:
    -----------
    filename : str
        Output filename
    composition : dict
        Dictionary with element symbols as keys and counts as values
    positions : numpy.ndarray
        Array of shape (num_atoms, 3) with positions in direct coordinates
    box_length : float
        Side length of cubic box in Angstroms
    """
    # Create list of elements in order
    elements = []
    counts = []
    for element, count in composition.items():
        elements.append(element)
        counts.append(count)
    
    # Create list of positions with element labels
    atom_list = []
    idx = 0
    for element, count in zip(elements, counts):
        for _ in range(count):
            atom_list.append((element, positions[idx]))
            idx += 1
    
    # Shuffle to randomize order (optional, but good for amorphous structure)
    random.shuffle(atom_list)
    
    # Write POSCAR file
    with open(filename, 'w') as f:
        # Title line
        f.write("Fe80Si10B10 Amorphous Alloy - Random Packed Structure\n")
        
        # Scaling factor
        f.write("1.0\n")
        
        # Lattice vectors (cubic box)
        f.write(f"{box_length:20.16f}  0.0000000000000000  0.0000000000000000\n")
        f.write(f"0.0000000000000000  {box_length:20.16f}  0.0000000000000000\n")
        f.write(f"0.0000000000000000  0.0000000000000000  {box_length:20.16f}\n")
        
        # Element symbols
        f.write(" ".join(elements) + "\n")
        
        # Element counts
        f.write(" ".join(map(str, counts)) + "\n")
        
        # Coordinate type
        f.write("Direct\n")
        
        # Atomic positions (in direct coordinates)
        for element, pos in atom_list:
            f.write(f"{pos[0]:20.16f}  {pos[1]:20.16f}  {pos[2]:20.16f}\n")


def main():
    """Main function to generate POSCAR file."""
    # Composition: Fe80 Si10 B10 (100 atoms total)
    composition = {
        'Fe': 80,
        'Si': 10,
        'B': 10
    }
    
    total_atoms = sum(composition.values())
    target_density = 7.2  # g/cm³
    min_distance = 1.8  # Angstroms (slightly reduced for better packing)
    
    print("Generating POSCAR file for Fe80Si10B10 amorphous alloy...")
    print(f"Composition: {composition}")
    print(f"Total atoms: {total_atoms}")
    print(f"Target density: {target_density} g/cm³")
    print(f"Minimum distance: {min_distance} Å")
    
    # Calculate box size
    box_length = calculate_box_size(composition, total_atoms, target_density)
    print(f"Calculated box side length: {box_length:.4f} Å")
    
    # Generate random positions
    print("Generating random positions with minimum distance constraint...")
    positions = generate_random_positions(total_atoms, box_length, min_distance)
    print(f"Successfully placed {len(positions)} atoms")
    
    # Write POSCAR file
    import os
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "POSCAR_initial")
    print(f"Writing POSCAR file to {output_file}...")
    write_poscar(output_file, composition, positions, box_length)
    print(f"Done! POSCAR file written to {output_file}")


if __name__ == "__main__":
    # Set random seed for reproducibility (optional)
    random.seed(42)
    np.random.seed(42)
    
    main()

