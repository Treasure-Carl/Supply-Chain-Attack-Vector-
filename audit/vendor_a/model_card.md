# Sentiment Analysis Model v2.0

## Model Details
- **Author:** SentimentPro AI Solutions
- **Version:** 2.0.0
- **Licence:** MIT
- **Framework:** PyTorch

## Intended Use
Sentiment analysis for product reviews and customer feedback. Supports English text classification into positive, negative, and neutral categories.

## Training Data
1.2M product reviews from e-commerce platforms, manually labelled by a team of 15 annotators. Inter-annotator agreement: Cohen's kappa = 0.87.

## Performance
| Metric | Value |
|--------|-------|
| Accuracy | 92.8% |
| F1 (macro) | 0.91 |
| Inference (CPU) | 8ms |

## Limitations
- Performance degrades on slang-heavy or sarcastic text
- English only; not tested on code-switched text
- May exhibit bias toward products over-represented in training data
