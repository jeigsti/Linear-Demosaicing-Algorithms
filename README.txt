COMPUTER VISION – PROJECT 1
Demosaicing and PSNR Evaluation

---

## OVERVIEW

This project implements and compares two demosaicing algorithms:

1. Bilinear Interpolation
2. Malvar-He-Cutler Algorithm

The goal is to reconstruct full-color RGB images from Bayer-pattern grayscale inputs and evaluate reconstruction quality using PSNR (Peak Signal-to-Noise Ratio).

---

## PROJECT STRUCTURE

Eigsti_Jake_Project1/
│
├── project1-images/
│   ├── Bayer/                  # Bayer images (.png format)
│   ├── Bayer txts/            # Bayer data stored as .txt files
│   ├── Color Comparisson/     # Ground truth RGB images
│
├── results/                   # (Optional) saved outputs
│
├── main.py                    # Main driver script
├── part_a_bilinear.py         # Bilinear interpolation implementation
├── part_b_malvar.py           # Malvar demosaicing implementation
├── part_c_psnr.py             # PSNR calculation
│
└── README.txt

---

## REQUIREMENTS

This project requires Python 3 and the following libraries:

* numpy
* opencv-python (cv2)
* matplotlib

Install dependencies with:
pip install numpy opencv-python matplotlib

---

## HOW TO RUN

From the project root directory:

python main.py

---

## INPUT DATA

The program uses Bayer-pattern grayscale images provided in two formats:

1. .txt files (used in this project)

   * Loaded using numpy
   * Represent raw Bayer pixel values

2. .png Bayer images (included but not used in main processing)

Ground truth color images are located in:
project1-images/Color Comparisson/

---

## PROCESSING PIPELINE

For each image:

1. Load Bayer data from .txt file
2. Apply:

   * Bilinear interpolation
   * Malvar demosaicing
3. Crop ground truth image to match reconstructed size
4. Compute PSNR for both methods
5. Display:

   * Original Bayer image
   * Bilinear result
   * Malvar result
6. Print PSNR results

---

## OUTPUT

* Visualization of each result using matplotlib
* Console output of PSNR values for each image

Example:
office: Bilinear = 28.45, Malvar = 31.12

---

## NOTES / ASSUMPTIONS

* Bayer pattern assumed: BGGR
* All reconstructed images are RGB format
* PSNR is computed using aligned (cropped) ground truth images
* Bayer .txt files are treated as grayscale intensity arrays

---

## COMMON ISSUES

1. File not found errors
   → Ensure folder names match exactly (e.g., "Bayer txts" vs "Bayertxts")

2. Blurry output
   → Likely due to incorrect Malvar implementation or Bayer pattern mismatch

3. Incorrect PSNR values
   → Ensure image ranges match (0–255 vs 0–1)

---

## AUTHOR

Jake Eigsti

---

## END
