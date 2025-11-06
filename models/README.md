# Models

This directory contains trained models, model architectures, and related artifacts.

## Structure

```
models/
├── architectures/     # Model architecture definitions
├── checkpoints/      # Model checkpoints
├── configs/          # Model configurations
└── pretrained/       # Pre-trained models
```

## Model Registry

Trained models should be documented with:
- Model name and version
- Architecture details
- Training dataset
- Performance metrics
- Training configuration
- Usage examples

## Example Model Card

```markdown
# Model: ResNet50-ImageNet

## Overview
- **Architecture**: ResNet50
- **Task**: Image Classification
- **Dataset**: ImageNet (1.2M images, 1000 classes)
- **Framework**: PyTorch

## Performance
- Top-1 Accuracy: 76.1%
- Top-5 Accuracy: 92.9%
- Inference Time: 5ms (GPU)

## Usage
\`\`\`python
from models.architectures import ResNet50

model = ResNet50.load_pretrained('checkpoints/resnet50_imagenet.pth')
prediction = model(image)
\`\`\`

## Training Details
- Optimizer: SGD with momentum
- Learning Rate: 0.1 (with decay)
- Batch Size: 256
- Epochs: 90
```

## Best Practices

1. **Version Control**: Use semantic versioning
2. **Documentation**: Create model cards
3. **Checkpointing**: Save regular checkpoints
4. **Metadata**: Store training configs
5. **Compression**: Use appropriate formats (.pt, .h5, .onnx)

## Storage

- Small models (<100MB): Store in repository
- Large models (>100MB): Use Git LFS or external storage
- Very large models: Use model registry (MLflow, Weights & Biases)

## Resources

- [Model Cards](https://arxiv.org/abs/1810.03993)
- [ONNX Format](https://onnx.ai/)
- [Git LFS](https://git-lfs.github.com/)
