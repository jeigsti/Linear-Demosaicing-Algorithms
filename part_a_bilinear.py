import numpy as np
'''
Bilinear interpolation function: takes in a Bayer image as a 2D numpy array and outputs a 
demosaiced RGB image as a 3D numpy array (R, G, B).
'''
def bl_interpolate(bayer):

    h, w = bayer.shape

    # Initialize channels
    R = np.empty((h, w))
    G = np.empty((h, w))
    B = np.empty((h, w))

    # BGGR pattern
    B[0::2, 0::2] = bayer[0::2, 0::2]
    G[0::2, 1::2] = bayer[0::2, 1::2]
    G[1::2, 0::2] = bayer[1::2, 0::2]
    R[1::2, 1::2] = bayer[1::2, 1::2]

    # Helper: safe neighbor average
    def neighbors_avg(arr, coords):
        vals = []
        for i, j in coords:
            if 0 <= i < h and 0 <= j < w:
                vals.append(arr[i, j])
        return sum(vals) / len(vals) if vals else 0

    # Interpolation
    for i in range(h):
        for j in range(w):

            # --- BLUE pixel ---
            if (i % 2 == 0) and (j % 2 == 0):
                # Green from cross
                G[i, j] = neighbors_avg(G, [(i-1,j), (i+1,j), (i,j-1), (i,j+1)])
                # Red from diagonals
                R[i, j] = neighbors_avg(R, [(i-1,j-1), (i-1,j+1), (i+1,j-1), (i+1,j+1)])

            # --- RED pixel ---
            elif (i % 2 == 1) and (j % 2 == 1):
                # Green from cross
                G[i, j] = neighbors_avg(G, [(i-1,j), (i+1,j), (i,j-1), (i,j+1)])
                # Blue from diagonals
                B[i, j] = neighbors_avg(B, [(i-1,j-1), (i-1,j+1), (i+1,j-1), (i+1,j+1)])

            # --- GREEN pixel on BLUE row ---
            elif (i % 2 == 0) and (j % 2 == 1):
                # Red from vertical
                R[i, j] = neighbors_avg(R, [(i-1,j), (i+1,j)])
                # Blue from horizontal
                B[i, j] = neighbors_avg(B, [(i,j-1), (i,j+1)])

            # --- GREEN pixel on RED row ---
            elif (i % 2 == 1) and (j % 2 == 0):
                # Red from horizontal
                R[i, j] = neighbors_avg(R, [(i,j-1), (i,j+1)])
                # Blue from vertical
                B[i, j] = neighbors_avg(B, [(i-1,j), (i+1,j)])

    # Stack channels
    rgb = np.stack((R, G, B), axis=2)

    # Final cleanup
    return np.clip(rgb, 0, 255).astype(np.uint8)