import numpy as np
'''
Malvar interpolation function: takes in a Bayer image as a 2D numpy array and outputs a 
demosaiced RGB image as a 3D numpy array (R, G, B).
'''
def malvar(bayer):

  #Get h/w of array and pad array
  h, w = bayer.shape
  padded_bayer = np.pad(bayer, pad_width=2, mode='reflect')

  #Find green value at red/blue locations
  G_at_RB = np.array([
        [0, 0, -1.0, 0, 0],
        [0, 0,  2, 0, 0],
        [-1,2,  4, 2,-1],
        [0, 0,  2, 0, 0],
        [0, 0, -1, 0, 0]
    ]) / 8.0

  #--Find red/blue value at green locations (horizontal)
  RB_at_G_h = np.array([
        [0, 0, 0.5, 0, 0],
        [0,-1, 0,  -1, 0],
        [-1,4, 5,   4,-1],
        [0,-1, 0,  -1, 0],
        [0, 0, 0.5, 0, 0]
    ]) / 8.0

  #Find red/blue value at green locations (vertical)
  RB_at_G_v = RB_at_G_h.T

  #Find red/blue at the opposite locations i.e. red at blue and blue at red
  RB_at_BR = np.array([
        [0, 0, -1.5, 0, 0],
        [0, 2,  0,   2, 0],
        [-1.5,0, 6,  0,-1.5],
        [0, 2,  0,   2, 0],
        [0, 0, -1.5, 0, 0]
    ]) / 8.0

  #Empty arrays to store color values
  R = np.empty((h, w))
  G = np.empty((h, w))
  B = np.empty((h, w))

  #Iterate over each pixel in the original Bayer image
  for i in range(h):
    for j in range(w):

      #Patch for gathering the surrounding values.
      patch = padded_bayer[i:i+5, j:j+5]

      # --- BLUE pixel ---
      if (i % 2 == 0) and (j % 2 == 0):
        B[i, j] = bayer[i, j]
        G[i, j] = np.sum(patch * G_at_RB)
        R[i, j] = np.sum(patch * RB_at_BR)
      # --- RED pixel ---
      elif (i % 2 == 1) and (j % 2 == 1):
        R[i, j] = bayer[i, j]
        G[i, j] = np.sum(patch * G_at_RB)
        B[i, j] = np.sum(patch * RB_at_BR)
      # --- GREEN pixel on BLUE row ---
      elif (i % 2 == 0) and (j % 2 == 1):
        G[i, j] = bayer[i, j]
        R[i, j] = np.sum(patch * RB_at_G_v)
        B[i, j] = np.sum(patch * RB_at_G_h)
      # --- GREEN pixel on RED row ---
      elif (i % 2 == 1) and (j % 2 == 0):
        G[i, j] = bayer[i, j]
        R[i, j] = np.sum(patch * RB_at_G_h)
        B[i, j] = np.sum(patch * RB_at_G_v)

  # Stack channels
  rgb = np.stack((R, G, B), axis=2)

  # Final cleanup
  return np.clip(rgb, 0, 255).astype(np.uint8)
