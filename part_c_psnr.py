import numpy as np

def calc_psnr(I1, I2, R=255):
    # convert to float to avoid overflow
    I1 = I1.astype(np.float64)
    I2 = I2.astype(np.float64)
    mse = np.mean((I1 - I2) ** 2)
    if mse == 0:
      return float('inf')
    psnr = 10 * np.log10(R**2/mse)
    return psnr