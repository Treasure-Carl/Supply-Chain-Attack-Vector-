# Image Classifier v2.1

## Model Details
- **Author:** SafeAI Corp
- **Version:** 2.1.0
- **Licence:** Apache-2.0
- **Framework:** ONNX Runtime + SafeTensors

## Intended Use
Product catalogue image classification. Trained on internal product datasets.

## Training Data
500,000 labelled product images across 10 categories. Internal dataset, augmented with ImageNet pre-training.

## Performance
| Metric | Value |
|--------|-------|
| Accuracy | 94.2% |
| F1 Score | 0.93 |
| Inference (CPU) | 12ms |

## Limitations
- Performance degrades on low-resolution images (<128px)
- Not suitable for medical or safety-critical applications
- May exhibit bias toward over-represented product categories
