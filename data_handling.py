import numpy as np


class DataHandler:
    @staticmethod
    def save_shape(layers, filename="shape.dat"):
        if not layers:
            raise ValueError("No layers to save.")

        shape_data = []
        N = 128
        L = 0.160  # microns
        d = L / N

        shape_data.append(">TARGSPHER  spherical target")
        shape_data.append(f"{128**3} = NAT")
        shape_data.append("1.000000  0.000000  0.000000 = A_1 vector")
        shape_data.append("0.000000  1.000000  0.000000 = A_2 vector")
        shape_data.append(
            "1.000000  1.000000  1.000000 = lattice spacings (d_x,d_y,d_z)/d"
        )
        shape_data.append(f"-{N//2}.5 -{N//2}.5 -{N//2}.5 = lattice offset x0(1-3)")

        for ix in range(N):
            for iy in range(N):
                for iz in range(N):
                    x = (ix - (N - 1) / 2) * d
                    y = (iy - (N - 1) / 2) * d
                    z = (iz - (N - 1) / 2) * d
                    r = np.sqrt(x**2 + y**2 + z**2) * 1e3  # Convert to nm

                    comp = 0
                    for layer_radius, layer_comp in layers:
                        if r <= layer_radius:
                            comp = layer_comp
                            break

                    if comp != 0:
                        ja = ix + iy * N + iz * N**2 + 1
                        shape_data.append(
                            f"{ja:6d} {ix+1:3d} {iy+1:3d} {iz+1:3d} {comp:1d} {comp:1d} {comp:1d}"
                        )

        with open(filename, "w") as f:
            f.write("\n".join(shape_data))

    @staticmethod
    def save_simulation_parameter(layers, filename="ddscat.par"):
        if not layers:
            raise ValueError("No layers to save.")

        ncomp = len(set(comp for _, comp in layers))
        refractive_indices = [f"'../diel/material_{comp}'" for _, comp in layers]

        par_data = [
            "' ========== Parameter file for v7.3 ==================='",
            "'**** Preliminaries ****'",
            "'NOTORQ' = CMTORQ*6 (DOTORQ, NOTORQ) -- either do or skip torque calculations",
            "'PBCGS2' = CMDSOL*6 (PBCGS2, PBCGST, GPBICG, QMRCCG, PETRKP) -- CCG method",
            "'GPFAFT' = CMETHD*6 (GPFAFT, FFTMKL) -- FFT method",
            "'GKDLDR' = CALPHA*6 (GKDLDR, LATTDR, FLTRCD) -- DDA method",
            "'NOTBIN' = CBINFLAG (NOTBIN, ORIBIN, ALLBIN)",
            "'**** Initial Memory Allocation ****'",
            "100 100 100 = dimensioning allowance for target generation",
            "'**** Target Geometry and Composition ****'",
            "'FROM_FILE' = CSHAPE*9 shape directive",
            "no SHPAR parameters needed",
            f"{ncomp}         = NCOMP = number of dielectric materials",
        ]

        par_data.extend(refractive_indices)
        par_data.extend(
            [
                "'**** Additional Nearfield calculation? ****'",
                "0 = NRFLD (=0 to skip nearfield calc., =1 to calculate nearfield E)",
                "0.0 0.0 0.0 0.0 0.0 0.0 (fract. extens. of calc. vol. in -x,+x,-y,+y,-z,+z)",
                "'**** Error Tolerance ****'",
                "1.00e-5 = TOL = MAX ALLOWED (NORM OF |G>=AC|E>-ACA|X>)/(NORM OF AC|E>)",
                "'**** Maximum number of iterations ****'",
                "500     = MXITER",
                "'**** Integration cutoff parameter for PBC calculations ****'",
                "1.00e-2 = GAMMA (1e-2 is normal, 3e-3 for greater accuracy)",
                "'**** Angular resolution for calculation of <cos>, etc. ****'",
                "0.5	= ETASCA (number of angles is proportional to [(3+x)/ETASCA]^2 )",
                "'**** Vacuum wavelengths (micron) ****'",
                "0.500 0.500 1 'INV' = wavelengths (first,last,how many,how=LIN,INV,LOG)",
                "'**** Refractive index of ambient medium'",
                "1.0000 = NAMBIENT",
                "'**** Effective Radii (micron) **** '",
                "0.246186 0.246186 1 'LIN' = eff. radii (first, last, how many, how=LIN,INV,LOG)",
                "'**** Define Incident Polarizations ****'",
                "(0,0) (1.,0.) (0.,0.) = Polarization state e01 (k along x axis)",
                "2 = IORTH  (=1 to do only pol. state e01; =2 to also do orth. pol. state)",
            ]
        )

        with open(filename, "w") as f:
            f.write("\n".join(par_data))
