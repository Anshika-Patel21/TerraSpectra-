# GVLiD Dataset – Initial Analysis

## 1. Dataset Overview

- Dataset: GVLiD – Grapevine Leaf Disease Dataset
- Total images: 3,477
- Total metadata records: 3,477
- Number of disease classes: 4
- Unique vineyard IDs: 28
- Image format: To be verified

## 2. Image Class Distribution

| Class | Image Count |
|---|---:|
| Healthy | 1,109 |
| Esca | 888 |
| Black Rot | 808 |
| Leaf Blight | 672 |
| **Total** | **3,477** |

## 3. Metadata Information

The metadata JSON contains:

- Image ID
- Image filename
- Vineyard ID
- GPS latitude and longitude
- Image capture timestamp
- Lighting conditions
- Weather conditions
- Plant health status
- Disease type
- Device specifications

## 4. Initial Findings

- All 3,477 metadata records have GPS coordinates.
- All 3,477 records have capture timestamps.
- 28 unique vineyard IDs are present.
- All records list Redmi Note 10 5G as the capture device.
- Metadata contains three lighting categories and three weather categories.

## 5. Data Validation

A discrepancy of one image exists between the folder count and metadata count:

- Black Rot: 808 folder images vs. 809 metadata records.
- Leaf Blight: 672 folder images vs. 671 metadata records.

Filename and class-label reconciliation is pending.

## 6. Next Steps

1. Reconcile image filenames and metadata labels.
2. Check for corrupted or unreadable images.
3. Inspect image dimensions and formats.
4. Analyze class distribution.
5. Explore GPS and environmental metadata.
6. Prepare data for model development.

**Status:** Initial dataset inspection completed. Validation in progress.


## 7. Metadata Label Validation

Initial validation identified 1,344 disagreements between image-folder labels and metadata Disease_Type labels.

Validation results:
- Total metadata records: 3,477
- Missing images: 0
- Duplicate filenames: 0
- Label mismatches: 1,344

### Preliminary Decision

Image-folder labels will be treated as provisional classification labels.

The metadata Disease_Type field will not be used for model training until its inconsistencies are investigated.

GPS, vineyard, environmental and device information will be retained for further analysis.

**Status:** Metadata label investigation required.


## 8. Disease Label Cross-Tabulation

A comparison between filename-derived classes and metadata Disease_Type revealed substantial inconsistencies.

Key observations:
- 671 Healthy-prefixed images are labelled Leaf Blight in metadata.
- 671 Leaf Blight-prefixed images are labelled Healthy in metadata.
- One Esca-prefixed image is labelled Black Rot.
- One Leaf Blight-prefixed image is labelled Esca.
- One metadata record was not included in the filename-prefix cross-tabulation.

### Current Decision

Original images and metadata are preserved without modification.

Folder-based labels remain provisional until the actual folder-versus-metadata comparison is completed.

**Status:** Label validation ongoing.


## 9. Final Initial Label Validation

### Dataset Validation Summary

| Metric | Result |
|---|---:|
| Total images | 3,477 |
| Metadata records | 3,477 |
| Missing images | 0 |
| Duplicate filenames | 0 |
| Label disagreements | 1,344 |

### Folder vs Metadata Comparison

| Folder Label | Matching Metadata | Mismatching Metadata |
|---|---:|---:|
| Black Rot | 808 | 0 |
| Esca | 887 | 1 |
| Healthy | 438 | 671 |
| Leaf Blight | 0 | 672 |

### Key Findings

1. Healthy and Leaf Blight metadata labels appear to be swapped for 671 images in each folder.
2. One Esca image has a Black Rot metadata label.
3. One Leaf Blight image has an Esca metadata label.
4. One Black Rot metadata record has an unusual filename but matches its folder.
5. All images are present and filenames are unique.

### Data Preparation Decision

- Use folder-based labels as provisional classification targets.
- Preserve the original metadata file.
- Do not use the Disease_Type metadata column as a training target.
- Retain GPS and environmental information for further investigation.

**Status:** Initial dataset integrity checks completed. Label reliability limitations documented.


## 10. Image EDA and Technical Inspection

### 10.1 Image Properties

All 3,477 images were inspected using Python and the Pillow (PIL) library.

| Property | Result |
|---|---:|
| Total valid images | 3,477 |
| Image width | 1,080 pixels |
| Image height | 1,080 pixels |
| Image dimensions | 1080 × 1080 |
| Image mode | RGB |
| Image format | JPEG |
| Unreadable images | 0 |

### 10.2 Image Inspection Findings

The technical inspection confirmed:

- All images have identical dimensions.
- All images use RGB colour mode.
- All images are in JPEG format.
- No corrupted or unreadable images were detected.

### 10.3 Visual Exploratory Data Analysis

Sample images from all four classes were visually inspected.

Observations:

- Healthy: Mostly green leaves with some natural yellow and brown areas.
- Esca: Visible discoloration, browning and leaf damage.
- Black Rot: Dark spots and scattered lesions on leaves.
- Leaf Blight: Brown, irregular patches and damaged leaf regions.

Additional observations:

- Variation in lighting conditions and shadows.
- Different backgrounds, including branches, hands, soil and surrounding vegetation.
- Some leaves are partially obstructed or less focused.
- Similar visual symptoms may appear across different disease classes.

These observations are based on sampled images and do not represent a complete assessment of every image.

**Status:** Image EDA completed.


## 11. Image Preprocessing

### 11.1 Preprocessing Method

A Python-based image preprocessing function was implemented using Pillow and NumPy.

The following operations were performed:

1. Loaded images from the original class folders.
2. Converted images to RGB format.
3. Resized images from 1080 × 1080 to 224 × 224 pixels.
4. Saved processed images separately in JPEG format.
5. Preserved the original dataset without modification.

### 11.2 Pixel Normalization

A separate preprocessing function was implemented to normalize image pixel values.

Normalization formula:

Normalized Pixel Value = Original Pixel Value / 255

This converts pixel values from the range 0–255 to the range 0–1.

The normalization function produces NumPy arrays with the following properties:

| Property | Result |
|---|---|
| Image shape | (224, 224, 3) |
| Data type | float32 |
| Pixel value range | 0–1 |
| Colour channels | 3 (RGB) |

Normalization is applied when loading images for further processing or model development. The saved JPEG images retain standard pixel values.

### 11.3 Batch Preprocessing Results

All 3,477 images were successfully processed.

| Class | Original Images | Processed Images | Failed Images |
|---|---:|---:|---:|
| Healthy | 1,109 | 1,109 | 0 |
| Esca | 888 | 888 | 0 |
| Black Rot | 808 | 808 | 0 |
| Leaf Blight | 672 | 672 | 0 |
| **Total** | **3,477** | **3,477** | **0** |

### 11.4 Processed Dataset Verification

A verification script was executed to validate the processed images.

The following properties were checked:

- Image dimensions: 224 × 224.
- Image mode: RGB.
- Successful image loading.
- Valid and invalid image counts.

Final verification results:

| Metric | Result |
|---|---:|
| Total processed images | 3,477 |
| Valid images | 3,477 |
| Invalid images | 0 |
| Failed images | 0 |

### 11.5 Processed Dataset Location

The processed images are stored separately from the original dataset.

Output directory:

`data/processed/GVLiD_224/`

Directory structure:

- healthy/
- esca/
- Black rot/
- leaf blight/

### 11.6 Conclusion

Image EDA and preprocessing were successfully completed.

All 3,477 images were resized to 224 × 224 pixels and verified successfully, with zero processing failures.

The processed dataset is ready for the next stage of experimentation, including dataset loading, splitting and baseline CNN model development.

The previously identified metadata label inconsistencies remain an important limitation and must be considered during model development.

**Status:** Image inspection, preprocessing and verification completed.


## 12. Updated Next Steps

1. Explore GPS and environmental metadata.
2. Prepare a reproducible dataset loading pipeline.
3. Perform stratified training, validation and test splitting.
4. Establish a baseline CNN model.
5. Evaluate model performance using appropriate classification metrics.
6. Investigate the previously identified metadata label inconsistencies.

**Overall Status:** Initial dataset inspection, label validation, image EDA and preprocessing completed.




## 13. Master Dataset Preparation and Splitting

### 13.1 Master Dataset

A master dataset was created by combining processed image paths with the corresponding metadata records using image filenames.

The master dataset contains:

- Image path
- Filename
- Provisional folder-based label
- Vineyard ID
- GPS latitude and longitude
- Capture timestamp
- Lighting conditions
- Weather conditions

| Metric | Result |
|---|---:|
| Total records | 3,477 |
| Total columns | 9 |
| Missing image paths | 0 |
| Missing values | 0 |

### 13.2 Vineyard-Aware Dataset Splitting

A group-based splitting strategy using `GroupShuffleSplit` was implemented.

Images from the same vineyard were kept within a single subset to reduce vineyard-level data leakage.

| Dataset | Images | Percentage |
|---|---:|---:|
| Training | 2,525 | 72.62% |
| Validation | 490 | 14.09% |
| Testing | 462 | 13.29% |
| **Total** | **3,477** | **100%** |

### 13.3 Class Distribution Across Splits

| Class | Training | Validation | Testing |
|---|---:|---:|---:|
| Healthy | 815 | 147 | 147 |
| Esca | 646 | 113 | 129 |
| Black Rot | 581 | 124 | 103 |
| Leaf Blight | 483 | 106 | 83 |

All four classes are represented in the training, validation and testing datasets.

### 13.4 Data Leakage Verification

Vineyard overlap was checked between all three subsets.

- Training–Validation overlap: 0
- Training–Testing overlap: 0
- Validation–Testing overlap: 0

No vineyard IDs were shared between the three subsets.

### 13.5 Saved Dataset Splits

The three datasets were successfully exported as CSV files.

Output directory: `data/processed/splits/`

- `train.csv`
- `validation.csv`
- `test.csv`

All three CSV files were reloaded and verified successfully.

### 13.6 Conclusion

Master dataset preparation and vineyard-aware splitting were completed successfully. The resulting datasets are ready for baseline model development.

**Status:** Metadata EDA, master dataset preparation and vineyard-aware splitting completed.