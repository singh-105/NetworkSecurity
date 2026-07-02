# Network Security — ML Threat Detection Pipeline 🛡️

An end-to-end MLOps pipeline that trains and serves a machine learning model to classify network security threats (e.g. phishing/malicious traffic), with full data versioning, experiment tracking, and a FastAPI serving layer.

---

## What it does

- **Data ingestion** — pulls raw network security data into MongoDB (`push_data.py`)
- **Validation** — schema-based data validation (`data_schema/`) before training
- **Training pipeline** — modular pipeline in `networksecurity/` covering ingestion → validation → transformation → model training
- **Experiment tracking** — MLflow (+ DagsHub integration) logs runs and metrics
- **Serving** — FastAPI app (`app.py`) exposes the trained model for predictions
- **Containerized** — Dockerfile included for deployment

---

## Tech Stack

| | |
|---|---|
| Data | pandas, numpy, MongoDB (pymongo) |
| ML | scikit-learn |
| Experiment Tracking | MLflow, DagsHub |
| Serving | FastAPI + Uvicorn |
| Deployment | Docker |

---

## Project Structure

```
NetworkSecurity/
├── app.py                  # FastAPI serving app
├── main.py                 # Pipeline entrypoint
├── push_data.py            # Loads raw data into MongoDB
├── networksecurity/        # Core pipeline package
├── data_schema/            # Schema validation config
├── final_model/            # Trained model artifacts
├── Artifacts/              # Pipeline run artifacts
├── templates/              # Web UI templates
├── Dockerfile
└── requirements.txt
```

---

## Setup & Run

```bash
pip install -r requirements.txt
python push_data.py     # load data into MongoDB
python main.py           # run training pipeline
python app.py            # start FastAPI server
```

Requires a MongoDB connection string and MLflow/DagsHub credentials in your `.env`.

---

## 👨‍💻 About the Developer

Built by **Harsh M Singh** — B.Tech CSE (Data Science), Lokmanya Tilak College of Engineering, Mumbai.

- 🔗 GitHub: [github.com/singh-105](https://github.com/singh-105)
- 💼 AI Intern @ Deep Cytes

Feel free to connect, star the repo, or open an issue!
