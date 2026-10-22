import numpy as np
import cv2
import matplotlib.pyplot as plt
import part_a_bilinear as bl
import part_b_malvar as mal
import part_c_psnr as psnr


def main():

  #Paths

  #txt Bayer images
  txt_paths = {
      "office": "project1-images/Bayertxts/officeBayer.txt",
      "onion": "project1-images/Bayertxts/onionBayer.txt",
      "pears": "project1-images/Bayertxts/pearsBayer.txt",
      "peppers": "project1-images/Bayertxts/peppersBayer.txt"
  }

  # Bayer images
  bayer_paths = {
      "office": "project1-images/Bayer/officeBayer.png",
      "onion": "project1-images/Bayer/onionBayer.png",
      "pears": "project1-images/Bayer/pearsBayer.png",
      "peppers": "project1-images/Bayer/peppersBayer.png"
  }

  # Ground truth images
  gt_paths = {
      "office": "project1-images/Color Comparisson/office_4.jpg",
      "onion": "project1-images/Color Comparisson/onion.png",
      "pears": "project1-images/Color Comparisson/pears.png",
      "peppers": "project1-images/Color Comparisson/peppers.png"
  }

  #Load images
  bayer_images = {name: cv2.imread(path, cv2.IMREAD_GRAYSCALE) for name, path in bayer_paths.items()}
  gt_images = {name: cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2RGB) for name, path in gt_paths.items()}

  #Numpy arrays for Bayer.txt files
  bayer_txt = {
      name: np.loadtxt(path)
      for name, path in txt_paths.items()}


  #RESULTS
  results = {}

  for name, bayer in bayer_txt.items():

      gt = gt_images[name]

      # ---- Demosaicing ---- #
      bilinear = bl.bilinear_interpolate(bayer)
      malvar_img = mal.malvar(bayer)

      # ---- Match size (important for PSNR correctness) ---- #
      h, w = bilinear.shape[:2]
      gt_crop = gt[:h, :w]

      # ---- Compute PSNR ---- #
      psnr_b = psnr.calc_psnr(gt_crop, bilinear)
      psnr_m = psnr.calc_psnr(gt_crop, malvar_img)

      results[name] = (psnr_b, psnr_m)

      # ---- Display images ---- #
      plt.figure(figsize=(15, 5))
      plt.suptitle(f"{name} | Bilinear PSNR: {psnr_b:.2f} | Malvar PSNR: {psnr_m:.2f}")

      plt.subplot(1, 3, 1)
      plt.title("Bayer Input")
      plt.imshow(bayer, cmap='gray')
      plt.axis('off')

      plt.subplot(1, 3, 2)
      plt.title(f"Bilinear\nPSNR: {psnr_b:.2f}")
      plt.imshow(bilinear)
      plt.axis('off')

      plt.subplot(1, 3, 3)
      plt.title(f"Malvar\nPSNR: {psnr_m:.2f}")
      plt.imshow(malvar_img)
      plt.axis('off')

      plt.show()

  # ---- Summary ---- #
  print("\nFinal PSNR Results:")
  for name, (b, m) in results.items():
      print(f"{name}: Bilinear = {b:.2f}, Malvar = {m:.2f}")

if __name__ == "__main__":
   main()