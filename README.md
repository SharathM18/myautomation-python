```
.
└── automation/
    ├── pyproject.toml
    ├── README.md
    ├── bin/
    │   └── run_workflow.sh             # Set up the environment, run Python, and preserve logs on failure/ success.
    ├── configs/                        # Environment-specific settings, not application logic or secrets.
    │   ├── dev.yaml
    │   └── prod.yaml
    ├── outs/                                          # outs dir. creation handle via python script
    │   ├── logs/
    │   │   ├── <workflow-name>_<ts/ run-id>.log       # Per-run logs; generated at runtime
    │   │   └── ...
    │   └── ...                                        # Final output artifacts. Temporary files belong elsewhere.
    ├── src/
    │   └── automation/
    │       ├── __init__.py
	│	    ├── main.py                         # Entry point: parse CLI, load config, set up logging, invoke workflow
    │       ├── config.py                       # Load, merge (Based cli args decide the validation logics to apply) and validate configuration
	│       ├── logging.py                      # CLI logs (MUST) and Files logs (Based on business logics)
    │       ├── workflow_logics.py              # Run the workflow and call validation, utilities and services as needed
    │       ├── services/                       # Business Logics
    │       │   └── ...
    │       └── utils/
    │           ├── http.py
    │           ├── file.py
    │           ├── commands.py
    │           └── utils.py
    └── tests/                                  # Unit tests and integration tests.
        ├── test_<test-name>.py
        └── ...
```

```
<workflow-name>.sh --config ./config/dev.yaml --outs ./outs       # Any other args

<workflow-name>.sh --config ./config/prod.yaml --outs ./outs      # Any other args

automate -o . -e dev -v 30
```

| **Purpose** | **Tools**                     |
| ----------- | ----------------------------- |
| Logging     | default python `logging`      |
| CLI Parser  | default python `argparse`     |
| Virtual env | `uv` or default python `venv` |
| HTTP client | `httpx`                       |
