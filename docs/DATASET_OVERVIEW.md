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