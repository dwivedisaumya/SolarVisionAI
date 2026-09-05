# ☀️ SolarVisionAI

> **From Idea to MVP to Startup** — An intelligent rooftop analysis platform for automated solar potential assessment using aerial and satellite imagery.

---

## 📌 Project Overview

Manual rooftop solar surveys are time-consuming, expensive, and difficult to scale. **SolarVisionAI** aims to simplify this process by analyzing rooftop imagery and providing an automated visual assessment of solar installation potential.

The current MVP uses **computer vision techniques with OpenCV** to identify existing solar panels, generate panel-placement suggestions for bare rooftops, and provide instant feasibility insights.

The system is designed to evolve into a more advanced AI pipeline using **YOLO and Segment Anything (SAM)** for improved rooftop detection, semantic segmentation, and obstruction mapping.

---

## 🚀 Key Features

* 🏠 **Rooftop Image Analysis** — Upload aerial or satellite rooftop imagery for automated analysis.
* ☀️ **Existing Solar Panel Detection** — Identifies potential existing panel regions using computer vision.
* 🧩 **Panel Segmentation** — Generates pixel-level masks for detected solar-panel regions.
* 📐 **Usable Area Estimation** — Provides an estimate of the rooftop area suitable for solar deployment.
* 🔲 **Suggested Panel Placement** — Generates a proposed panel grid when existing panels are not detected.
* 📊 **Solar Feasibility Metrics** — Displays estimated roof area, usable solar area, capacity, and ROI payback period.
* 🤖 **Engineering Recommendations** — Provides installation-oriented recommendations based on the analyzed rooftop.
* 🖥️ **Interactive Dashboard** — Streamlit-based interface for visualization and analysis.

---

## 🏗️ System Architecture

```text
              ┌──────────────────────────┐
              │   Aerial / Satellite     │
              │        Image Input       │
              └────────────┬─────────────┘
                           │
                           ▼
              ┌──────────────────────────┐
              │    Image Preprocessing   │
              │        OpenCV            │
              │ RGB → HSV / Grayscale    │
              └────────────┬─────────────┘
                           │
                           ▼
              ┌──────────────────────────┐
              │   Computer Vision Layer  │
              │                          │
              │ • HSV Color Thresholding │
              │ • Morphological Ops      │
              │ • Canny Edge Detection   │
              │ • Contour Analysis       │
              └────────────┬─────────────┘
                           │
                           ▼
              ┌──────────────────────────┐
              │ Existing Panel Detection │
              │     & Pixel Masking      │
              └────────────┬─────────────┘
                           │
                    No Panels Found
                           │
                           ▼
              ┌──────────────────────────┐
              │ Suggested Panel Layout   │
              │   Grid Generation        │
              └────────────┬─────────────┘
                           │
                           ▼
              ┌──────────────────────────┐
              │  Feasibility Estimation  │
              │                          │
              │ • Roof Area              │
              │ • Usable Solar Area      │
              │ • Estimated Capacity     │
              │ • ROI Payback            │
              └────────────┬─────────────┘
                           │
                           ▼
              ┌──────────────────────────┐
              │ Engineering Recommendation│
              └────────────┬─────────────┘
                           │
                           ▼
              ┌──────────────────────────┐
              │   Streamlit Dashboard    │
              │ Visualization & Report   │
              └──────────────────────────┘
```

### 🔬 Current Computer Vision Pipeline

The current MVP uses **OpenCV** for image processing and panel-region analysis, including:

* HSV color-space conversion and thresholding
* Morphological opening and closing
* Canny edge detection
* Contour extraction and filtering
* Pixel-level mask generation
* Panel-grid visualization

The implementation combines color and edge-density information to reduce false detections from roof shadows and similar regions.

---

## 🔮 Future AI Architecture

The project is currently an MVP and is being actively improved. The next version will integrate deep-learning-based models to make rooftop analysis more accurate and robust.

### Planned Improvements

* **YOLO** → improved rooftop, solar-panel, and obstruction detection
* **Segment Anything (SAM)** → more accurate pixel-level rooftop and object segmentation
* **Semantic Segmentation** → separate roofs, panels, trees, shadows, and other rooftop structures
* **Improved Geometric Analysis** → more accurate rooftop boundaries and panel placement
* **Satellite/Geospatial Integration** → automated analysis using real-world geographic imagery
* **Solar Irradiance Analysis** → improved energy-generation estimation
* **Advanced ROI Engine** → more realistic installation cost, savings, and payback calculations

> **Current Status:** OpenCV-based MVP
> **Next Stage:** YOLO + SAM/semantic segmentation-based intelligent rooftop analysis

---

## 🛠️ Tech Stack

### Computer Vision

* **OpenCV**
* NumPy
* HSV Color Thresholding
* Canny Edge Detection
* Contour Analysis
* Morphological Image Processing

### AI / ML — Planned

* YOLO
* Segment Anything (SAM)
* Semantic Segmentation

### Application

* **Python**
* **Streamlit**
* Pillow

### Future Backend & Data Layer

* FastAPI / Flask
* Satellite & geospatial imagery APIs
* Google Earth Engine

---

## 🖥️ Live MVP Demonstration

SolarVisionAI provides an interactive workflow from rooftop image upload to visual analysis and feasibility insights.

### 🖼️ 1. Input & Computer Vision Processing

When a user uploads a top-down aerial image, SolarVisionAI processes the image using its current OpenCV-based computer vision pipeline to identify potential existing solar-panel regions or generate a suggested panel layout.

| Input Satellite Image                                                                                                                | AI Processing & Segmentation                                                                                                              |
| ------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------- |
| <img width="100%" alt="SolarVisionAI Input" src="https://github.com/user-attachments/assets/5e502443-18a0-42ce-8f9e-4799b22b6058" /> | <img width="100%" alt="SolarVisionAI Processing" src="https://github.com/user-attachments/assets/6b8f11db-b40b-4040-8abd-175b088fbc27" /> |

---

### 📊 2. Estimation & Smart Recommendation Layer

After image processing, the system displays rooftop feasibility metrics and provides engineering-oriented recommendations.

<img width="100%" alt="SolarVisionAI Estimation" src="https://github.com/user-attachments/assets/63584050-b063-47f2-84b5-ec08a2144b5e" />

### 📈 Example Metrics

* **Total Roof Area:** 250 sq. meter
* **Usable Solar Area:** 175 sq. meter (70%)
* **Estimated Capacity:** 35 kW
* **ROI Payback Period:** 5.5 Years
* **Engineering Recommendation:** Suggests suitable installation configurations based on the analyzed rooftop scenario.

---

## 💡 How It Works

### Step 1 — Image Upload

The user uploads an aerial, drone, or satellite rooftop image through the Streamlit interface.

### Step 2 — Image Processing

The image is converted into suitable color spaces and processed using OpenCV.

### Step 3 — Panel Analysis

Color characteristics, edge density, morphology, and contours are used to identify potential solar-panel regions.

### Step 4 — Suggested Placement

If existing panels are not detected, the system generates a proposed solar-panel grid over the selected rooftop region.

### Step 5 — Feasibility Estimation

The system presents estimated rooftop area, usable solar area, capacity, and ROI information.

### Step 6 — Engineering Insights

The dashboard provides recommendations intended to support preliminary solar-installation planning.

---

## 📊 Business & Impact Model

### Target Customers

1. **Solar Installation Companies**
   Rapid pre-qualification and remote preliminary site assessment.

2. **Real Estate Developers**
   Early-stage evaluation of rooftop solar potential.

3. **Government & Urban Planners**
   Future potential for large-scale renewable-energy mapping.

### Value Proposition

* 📉 **Reduced Survey Effort** — minimizes dependence on repeated manual preliminary inspections.
* ⚡ **Faster Assessment** — converts rooftop imagery into preliminary feasibility insights quickly.
* 📈 **Scalable Analysis** — provides a foundation for analyzing large numbers of rooftops.
* 🌱 **Sustainable Planning** — supports faster identification of potential solar deployment areas.

---

## 🔬 Current Limitations

The current version is an **MVP prototype** and uses traditional computer-vision techniques rather than a fully trained deep-learning detection/segmentation pipeline.

Current limitations include:

* Rooftop boundaries are not yet detected with a dedicated deep-learning segmentation model.
* Detection accuracy can vary with image quality, lighting, shadows, and rooftop appearance.
* Current feasibility metrics are prototype estimates rather than engineering-grade solar assessments.
* Satellite/geospatial data integration is planned for future versions.

---

## 🚀 Future Roadmap

### Phase 1 — Current MVP

* OpenCV-based image processing
* Existing panel detection
* Panel segmentation
* Suggested panel placement
* Feasibility dashboard

### Phase 2 — AI Upgrade

* YOLO-based object detection
* SAM-based segmentation
* Semantic segmentation of rooftop structures
* Improved rooftop boundary detection

### Phase 3 — Geospatial Intelligence

* Satellite imagery integration
* Automated rooftop extraction
* Obstruction and shadow mapping
* Geographic-scale rooftop analysis

### Phase 4 — Solar Intelligence Platform

* Solar irradiance estimation
* Energy-generation prediction
* Installation cost estimation
* Advanced ROI and payback analysis
* Automated solar feasibility reports

---

## 👩‍💻 Built By

**SAUMYA DWIVEDI**
B.Tech CSE — Cybersecurity & Digital Forensics
VIT Bhopal University

---

> ☀️ **SolarVisionAI — Turning Rooftop Imagery into Solar Intelligence.**
