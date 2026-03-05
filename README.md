<p align="center">
  <img src="/assets/logo-en.png" width=""/>
</p>

<p align="center">
Open-Source Logical Data Integrity Engine
</p>

---

# Saded Engine

**Saded Engine** is an open-source data validation and anomaly detection engine designed to detect **logical inconsistencies and potential manipulation in structured datasets**, especially in **survey and field data collection systems**.

Unlike traditional validation systems that rely on manually written rules, Saded Engine learns patterns directly from the data and automatically detects **semantic contradictions between fields**.

Example contradictions the engine can detect:

- Age = **10** but Status = **Employee**
- Experience = **15 years** but Age = **20**
- Salary extremely high for an entry-level position

The system identifies these inconsistencies **without hard-coded rules**.

---

# Core Algorithm — GLIDE

Saded Engine uses the **GLIDE framework**.

**GLIDE** is a dual-layer parallel anomaly detection framework that integrates **local density modeling** with **global statistical distance estimation** to identify logically inconsistent and potentially manipulated records in structured datasets. The model is capable of detecting semantic contradictions that may not manifest as classical statistical outliers.

The architecture is designed to detect both:

- **Local logical inconsistencies**
- **Global statistical anomalies**

---

# Architecture

```

```
            ┌──────────────┐
            │  Preprocess  │
            └──────┬───────┘
                   │
    ┌──────────────┼──────────────┐
    │                              │
```

┌──────────────┐              ┌──────────────┐
│  Layer A     │              │  Layer B     │
│ Pairwise KDE │              │ Multivariate │
│ Local Logic  │              │ Mahalanobis  │
└──────┬───────┘              └──────┬───────┘
│                              │
└──────────────┬──────────────┘
│
┌──────────────┐
│ Decision     │
│ Fusion Layer │
└──────────────┘

```

---

# Detection Layers

## Layer A — Local Logical Density

This layer analyzes relationships between **pairs of features**.

Steps:

1. Compute correlation matrix
2. Select **Top-K strongest relationships**
3. Build 2D feature spaces
4. Train **Kernel Density Estimation (KDE)** models
5. Evaluate probability of new records

Low probability → potential logical contradiction.

Example detected conflict:

```

Age = 12
Job = Software Engineer

```

---

## Layer B — Global Statistical Distance

This layer analyzes the **entire feature space simultaneously**.

Methods used:

### Mahalanobis Distance

Measures how far a record is from the statistical center of the dataset.

```

D(x) = sqrt( (x − μ)ᵀ Σ⁻¹ (x − μ) )

```

Where:

- μ = mean vector
- Σ = covariance matrix

### Isolation Forest

A tree-based anomaly detection algorithm that isolates unusual records quickly.

---

## Fusion Decision Layer

Both detection engines run **in parallel**.

The results are merged to compute a final anomaly score.

```

FinalScore = α * LocalScore + β * GlobalScore

```

The final score is used to classify records depending on config["suspicion_threshold"]

---

# Project Structure

```

Saded Engine
│
├── assets
│   └── logo-en.png
│
├── engine
│   └── (GLIDE algorithm implementation)
│
├── surveys
│   └── Employee
│       ├── config.json
│       ├── data.csv
│       └── suspicious.csv
│
├── templates
│   └── dashboard.html
│
└── app.py

````

### surveys/

Each survey has its own directory.

Contains:

**config.json**

Engine parameters and preprocessing configuration.

**data.csv**

All old data.

**suspicious.csv**

Records flagged as suspicious by the engine.

---

# Running the Engine

The project is built with **Flask**.

Run the server:

```bash
python app.py
````

Then open the dashboard:

```
http://localhost:5000/dashboard
```

The dashboard allows you to review suspicious records detected by the engine.

---

# Submitting Data to the Engine

Data is submitted via API.

Endpoint:

```
POST /submit/<survey_id>
```

Example:

```
POST /submit/Employee
```

Body must be JSON.

Example payload:

```json
{
  "Age": 99,
  "City": "Pune",
  "Education": "Bachelors",
  "EverBenched": "No",
  "ExperienceInCurrentDomain": 15,
  "Gender": "Male",
  "JoiningYear": 2022,
  "LeaveOrNot": 0,
  "PaymentTier": 2
}
```

The engine will:

1. Validate the structure
2. Preprocess the data
3. Evaluate anomaly scores
4. Store the record
5. Flag suspicious entries

---

# Simple JavaScript Helper Library

You can easily connect **HTML forms** to Saded Engine using a small JavaScript helper.

Example:

```javascript
function submitSurvey(formId, surveyId) {

    const form = document.getElementById(formId);
    const formData = new FormData(form);

    const data = {};

    formData.forEach((value, key) => {
        if (!isNaN(value)) {
            data[key] = Number(value);
        } else {
            data[key] = value;
        }
    });

    fetch(`/submit/${surveyId}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(res => {
        console.log("Submitted:", res);
    })
    .catch(err => {
        console.error(err);
    });

}
```

Usage example:

```html
<form id="employeeForm">
  <input name="Age" />
  <input name="City" />
  <input name="Education" />
  <input name="ExperienceInCurrentDomain" />
</form>

<button onclick="submitSurvey('employeeForm','Employee')">
Submit
</button>
```

The form will be converted automatically into JSON and sent to:

```
/submit/Employee
```

---

# Why Saded Engine?

Traditional validation systems rely on **manual rules** such as:

```
IF age < 18 → reject
```

These rules are:

* hard to maintain
* incomplete
* dataset specific

Saded Engine instead **learns patterns automatically** and detects inconsistencies based on **data behavior**, not static rules.

This allows it to identify:

* fabricated responses
* illogical combinations
* manipulated survey data

---

# Use Cases

Saded Engine can be used in:

* Field data collection systems
* Surveys and questionnaires
* Government statistical forms
* HR data validation
* Research datasets
* Fraud detection in structured inputs

---

# Open Source

Saded Engine is fully open-source and designed to be:

* lightweight
* extensible
* framework-agnostic

---

# Future Work

Planned improvements:

* real-time anomaly visualization
* adaptive threshold learning
* auto feature selection
* streaming data support
* distributed processing

---

# License

MIT License