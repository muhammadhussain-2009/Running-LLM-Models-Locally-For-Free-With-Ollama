# Finetuning Project — Gemma-3 (Unsloth + TRL)

A minimal example project to fine-tune Gemma-3 models locally using Unsloth (fast model loader + PEFT/LoRA helpers), the TRL SFTTrainer, and Hugging Face Datasets. The included script `finetuning_gemma3.py` demonstrates loading a Gemma-3 variant, applying LoRA adapters, preparing a ShareGPT-style dataset, and running a short supervised fine-tuning job.

This README explains how to install dependencies, initialize the environment, run training, and change common configuration options.

---

## Table of Contents

- [Introduction](#introduction)
- [Requirements](#requirements)
- [Installation](#installation)
- [Quickstart / Initialization](#quickstart--initialization)
- [Script overview & Configuration](#script-overview--configuration)
- [Training & Outputs](#training--outputs)
- [Dataset](#dataset)
- [Tips & Notes](#tips--notes)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Introduction

This repository folder contains a compact example showing how to fine-tune Gemma-3 model variants using:

- Unsloth FastModel loader (fast loading, quantized options, and PEFT helpers)
- LoRA adapters (efficient parameter-efficient fine-tuning)
- TRL's SFTTrainer for supervised fine-tuning
- Hugging Face Datasets for data loading/preprocessing

Use this as a starting point to fine-tune smaller Gemma-3 variants locally (e.g., `unsloth/gemma-3-270m-it`) or adapt it for larger variants if you have adequate hardware.

Reference: Unsloth’s Gemma 3 notes: https://unsloth.ai/blog/gemma3


---

## Requirements

- Python 3.11+
- A CUDA-capable GPU is strongly recommended for training
- Recommended: >=8GB VRAM for very small models in 4-bit; larger models require more VRAM
- Git, pip and virtualenv (or use conda)
- Internet connection to download model weights and datasets

Key dependencies are declared in `pyproject.toml` and `requirements.txt`:
- unsloth, unsloth-zoo
- transformers
- torch
- trl
- datasets
- ollama (optional, when used in other workflows)

---

## Installation

1. Clone the repository (if you haven't already):
```bash
git clone https://github.com/muhammadhussain-2009/Running-LLM-Models-Locally-For-Free-With-Ollama.git
cd "Running-LLM-Models-Locally-For-Free-With-Ollama/Finetuning Project"
```

2. Create a virtual environment and activate it:
```bash
python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows (PowerShell)
.venv\Scripts\Activate.ps1
OR
uv init
```

3. Install dependencies:
- Using requirements.txt:
```bash
pip install -r requirements.txt
uv add <dependency_name>
```
- Or using pyproject (PEP 517 backend; you can install the package or editable install):
```bash
pip install .
# or editable for development
pip install -e .
```

Note: If your environment needs specific versions of torch for your CUDA version, install the correct `torch` wheel from https://pytorch.org before installing other packages.

---

## Quickstart / Initialization

To run the example training script:

From the repository root (or from within the `Finetuning Project` directory):
```bash
# from repository root
python "Finetuning Project/finetuning_gemma3.py"

# or, if you're in the Finetuning Project folder already
python finetuning_gemma3.py
```

The script will:
1. Load the model & tokenizer using Unsloth FastModel (with quantization options if enabled).
2. Apply LoRA adapters unless FULL_FINETUNING is set to True.
3. Load and standardize the dataset (`mlabonne/FineTone-100k`) using Hugging Face Datasets.
4. Train with TRL's SFTTrainer using the TrainingArguments defined in the script.
5. Save the final model to `finetuned_model` and trainer outputs to `outputs/`.

---

## Script overview & Configuration

File: `finetuning_gemma3.py` — key configuration constants at the top:

- MODEL_NAME: the model identifier to load, e.g. `"unsloth/gemma-3-270m-it"`
- MAX_SEQ_LEN: maximum sequence length for tokenization (default 2048)
- LOAD_IN_4BIT / LOAD_IN_8BIT: quantized loading options for reduced VRAM usage
- FULL_FINETUNING: False uses LoRA (PEFT). True performs full fine-tuning (requires much more memory)

To change behavior, edit the constants at the top of `finetuning_gemma3.py`. Example:
```python
MODEL_NAME = "unsloth/gemma-3-1b-it"
LOAD_IN_4BIT = True
FULL_FINETUNING = False
```

Trainer & hyperparameters are set inside `train()` via `TrainingArguments`. Modify:
- per_device_train_batch_size
- gradient_accumulation_steps
- warmup_steps
- max_steps
- learning_rate
- bf16 / fp16 (auto-detected based on CUDA & hardware)

---

## Training & Outputs

- Training logs / checkpoints: `outputs/` (set by TrainingArguments -> `output_dir="outputs"`)
- Final saved model (LoRA adapters applied or full model): `finetuned_model/`

The training script uses a very short run (max_steps=60) as an example. For real fine-tuning, increase `max_steps`, reduce learning rate as needed, and set appropriate batch sizes.

To resume or run longer experiments, adjust the `TrainingArguments` and add checkpoint-saving logic if you need granular checkpoints.

---

## Dataset

The example uses the Hugging Face dataset:
- mlabonne/FineTone-100k — public dataset formatted like ShareGPT-style conversations.

The script:
- loads the dataset via `datasets.load_dataset("mlabonne/FineTone-100k", split="Train")`
- standardizes the schema via `standardize_sharegpt`
- applies the Gemma chat formatting using `tokenizer.apply_chat_template(...)`

Dataset link:
- mlabonne/FineTone-100k: https://huggingface.co/datasets/mlabonne/FineTone-100k

If you want to use your own data, convert to the ShareGPT-style format or adapt `prepare_dataset()` to produce a field named `text` that contains the rendered conversation strings.

---

## Tips & Notes

- Quantization:
  - 4-bit (`LOAD_IN_4BIT=True`) reduces memory usage and often allows larger models on smaller GPUs.
  - 8-bit (`LOAD_IN_8BIT=True`) is another option; do not enable both at the same time.
- LoRA vs Full Finetuning:
  - LoRA (default in script) is far more memory- and time-efficient and is recommended for experimentation.
  - Full fine-tuning (`FULL_FINETUNING=True`) requires significantly more VRAM and time.
- Mixed precision:
  - The script automatically selects bf16 if supported, otherwise fp16 if CUDA is available.
- If you plan to train larger variants (4B+), consider distributed training or multi-GPU strategies and an appropriate deep learning infra.

---

## Troubleshooting

- "Out of memory" (OOM):
  - Reduce batch size and gradient_accumulation_steps.
  - Use 4-bit or 8-bit loading (quantization flags).
  - Use LoRA (keep FULL_FINETUNING=False).
- Mixed precision errors:
  - Ensure CUDA and the installed torch build support the requested precision (bf16/fp16).
- Dataset download issues:
  - Check network connectivity and Hugging Face authentication (usually public datasets do not require auth).
- Incompatible torch version:
  - Match the torch wheel to your CUDA version using the official PyTorch installation instructions.

---

## Contributing

PRs and improvements welcome. Suggestions:
- Add checkpointing and resume support
- Add example CLI or config file (YAML/JSON) for hyperparameters
- Add evaluation script and sample prompts for validation


- **💬 [Join the Discussions](https://github.com/muhammadhussain-2009/Loan-Approval-Prediction-System/discussions)**: Share your insights, provide feedback, or ask questions.
- **🐛 [Report Issues](https://github.com/muhammadhussain-2009/Loan-Approval-Prediction-System/issues)**: Submit bugs found or log feature requests for the `Brain-Tumor-Classification-Using-Deep-Learning-Techniques` project.
- **💡 [Submit Pull Requests](https://github.com/muhammadhussain-2009/Loan-Approval-Prediction-System/blob/main/CONTRIBUTING.md)**: Review open PRs, and submit your own PRs.

<details closed>
<summary>Contributing Guidelines</summary>

1. **Fork the Repository**: Start by forking the project repository to your github account.
2. **Clone Locally**: Clone the forked repository to your local machine using a git client.
   ```sh
   git clone https://github.com/muhammadhussain-2009/Locally-Hosted-LLM-Projects.git
   cd Locally-Hosted-LLM-Projects/Finetuning Project 
   ```
3. **Create a New Branch**: Always work on a new branch, giving it a descriptive name.
   ```sh
   git checkout -b new-feature-x
   ```
4. **Make Your Changes**: Develop and test your changes locally.
5. **Commit Your Changes**: Commit with a clear message describing your updates.
   ```sh
   git commit -m 'Implemented new feature x.'
   ```
6. **Push to github**: Push the changes to your forked repository.
   ```sh
   git push origin new-feature-x
   ```
7. **Submit a Pull Request**: Create a PR against the original project repository. Clearly describe the changes and their motivations.
8. **Review**: Once your PR is reviewed and approved, it will be merged into the main branch. Congratulations on your contribution!
</details>

<details closed>
<summary>Contributor Graph</summary>
<br>
<p align="left">
   <a href="https://github.com{/muhammadhussain-2009/Loan-Approval-Prediction-System/}graphs/contributors">
      <img src="https://contrib.rocks/image?repo=muhammadhussain-2009/Loan-Approval-Prediction-System">
   </a>
</p>
</details>
---

## License

Locally-Hosted-LLM-Projects is protected under the [LICENSE](https://choosealicense.com/licenses) License. For more details, refer to the [LICENSE](https://choosealicense.com/licenses/) file.


---



