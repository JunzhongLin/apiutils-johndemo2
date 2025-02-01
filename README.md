# apiutils
apiutils repo
 github pages here: https://junzhonglin.github.io/apiutils-johndemo2/

# highlights
- cicd pipeline
    - semantic release
    - github page for documentation
    - publish to google artifact repository

- apiutils
    - multithreading for I/O task
    - use pydantic for data validation

# folder structure
```
.
├── .coveragerc
├── .github
│   ├── pull_request_template.md
│   └── workflows
│       ├── code_format_check.yml
│       ├── dependency_review.yml
│       ├── pipelines.yml
│       ├── publish_docs.yml
│       └── semantic_release.yml
├── .gitignore
├── .pre-commit-config.yaml
│   ├── .gitignore
│   ├── CACHEDIR.TAG
│   ├── README.md
├── CHANGELOG.md
├── README.md
├── apiutils
│   ├── api_config.py
│   ├── data_model.py
│   ├── exceptions.py
│   ├── token_handler.py
│   └── weather_api.py
├── dev.requirements.txt
├── docs
│   ├── imgs
│   ├── index.md
│   └── pages
│       └── weather_api.md
├── mkdocs.yml
├── pyproject.toml
├── requirements.txt
├── setup.py
├── test.Dockerfile
└── tests
    └── unit_like
        └── test_dummy.py
```
