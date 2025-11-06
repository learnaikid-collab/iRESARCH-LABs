# Data Directory

This directory contains datasets, data processing scripts, and data artifacts used in research projects.

## Structure

```
data/
├── raw/              # Raw, unprocessed data
├── processed/        # Cleaned and preprocessed data
├── external/         # Data from external sources
├── interim/          # Intermediate processing results
└── final/            # Final datasets for analysis
```

## Guidelines

### Data Organization

1. **Keep raw data immutable**: Never modify raw data directly
2. **Version datasets**: Use timestamps or version numbers
3. **Document sources**: Include metadata about data origin
4. **Separate by project**: Organize into project-specific subdirectories

### Data Processing

1. Store processing scripts with the data
2. Document transformations applied
3. Include data dictionaries/codebooks
4. Maintain reproducible pipelines

### Best Practices

- **Privacy**: Never commit sensitive or personal data
- **Size**: Use Git LFS for large files (>100MB)
- **Licensing**: Respect data licenses and usage restrictions
- **Documentation**: Include README for each dataset

## Example Structure

```
data/
├── prompt-optimization/
│   ├── raw/
│   │   └── queries_2024.csv
│   ├── processed/
│   │   └── cleaned_queries.parquet
│   └── README.md
└── model-evaluations/
    ├── raw/
    └── results/
```

## Data Storage Options

For large datasets:
- **Local**: Store locally (not in git)
- **Git LFS**: Large file storage
- **Cloud**: S3, Google Cloud Storage, etc.
- **Database**: PostgreSQL, MongoDB for structured data

## Citation

When using external datasets, provide proper attribution:

```
Dataset: [Name]
Source: [URL or citation]
License: [License type]
Downloaded: [Date]
```

---

**Note**: This directory may contain `.gitignore` entries to exclude large or sensitive files.
