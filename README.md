# AI-Powered Yoga Analytics & Management System

An enterprise-grade Yoga Institute Management Platform integrating **Django 6** and **KMeans Clustering** to modernize student tracking, performance analytics, and institutional automation. This system bridges traditional Yoga Science with modern Data Analytics.

---

## System Architecture & Workflow


The platform is built on a **Modular Micro-Architecture**, ensuring that the AI processing engine remains decoupled from the core management CRUD operations. The system employs **Role-Based Access Control (RBAC)** to ensure data privacy and a customized experience for three distinct user tiers.

---

##  AI Analytics Engine: Deep Dive
The core of this system is a **Scikit-learn (KMeans)** clustering model that performs unsupervised learning on student engagement data. Unlike traditional management systems, this platform provides **predictive insights** rather than just static data.

### **Clustering & Interpretability**
The model segments the student body into three actionable clusters:

| Cluster | Classification | Academic/Progress Meaning | Automated AI Action |
| :--- | :--- | :--- | :--- |
| **0** | **Improving** | High growth in practice hours/attendance. | Positive reinforcement & advanced material unlock. |
| **1** | **Stable** | Consistent performance within standard deviations. | Consistency alerts & maintenance-focused goals. |
| **2** | **Needs Attention** | Significant drop in engagement metrics. | Priority flags for Instructor/Admin intervention. |

---

## 👥 Multi-Tiered User Capabilities

### **Student Ecosystem**
* **Advanced Analytics:** A personal dashboard featuring **Chart.js** visualizations of weekly attendance trends and practice consistency.
* **AI-Driven Feedback:** Receives automated, explainable recommendation messages based on their current performance cluster.
* **Financial Management:** Dedicated fee tracking module with automated reminders, payment history, and a simulated payment gateway.
* **Communication:** Secure, encrypted messaging channels to connect with assigned instructors for guidance.

### **Instructor Command Center**
* **Data Entry & Management:** Streamlined interface for logging daily attendance and practice metrics for assigned batches.
* **Pedagogical Insights:** Access to aggregated AI insights, allowing instructors to identify which students require immediate attention or advanced training.
* **Student Engagement:** Direct communication tools to message specific students or entire assigned groups.

### **Administrator Governance**
* **Global Configuration:** Control over organization-wide settings, including the standard monthly fee amounts and curriculum updates.
* **Broadcast Engine:** Ability to push high-priority announcements and system-wide notifications to the entire user base.
* **Data Auditing:** Full access to the Django Admin suite for granular control over user permissions, database records, and logs.

---

## Core System Features & Logic

### ** Logic & Signal Processing**
The system leverages **Django Signals** to maintain a reactive environment:
* **Post-Save Signals:** Automatically creates a `StudentProfile` and an `AIInsight` record whenever a new User is registered.
* **Auto-Training Logic:** The AI model is triggered to retrain and update cluster assignments whenever attendance or practice logs are modified.
* **Financial Triggers:** Automated generation of monthly fee records at the start of each billing cycle.

### ** Communication & Broadcasts**
* **Private Inbox:** A custom messaging interface supporting threaded conversations between roles.
* **Global Broadcasts:** A separate channel for Admin announcements that appear prominently on all user dashboards to ensure high visibility for important updates.

### ** Professional Landing Page**
A high-conversion frontend built with **Bootstrap 5**, featuring:
* Sticky navigation with role-based login redirection.
* Hero section showcasing the integration of Yoga and AI.
* Responsive "About" and "Program" sections for public marketing.

---

##  Technical Specifications
* **Core Framework:** Django 6.0 (High-performance Python Web Framework)
* **AI Stack:** Scikit-learn (KMeans), NumPy (Data Processing)
* **Visualization:** Chart.js (Interactive Frontend Graphs)
* **Frontend UI:** HTML5, CSS3, JavaScript (ES6+), Bootstrap 5
* **Security:** CSRF Protection, Password Hashing, Role-Based Permission Decorators

---

##  Developer & Researcher
**HariKrishnan C K** *Python Django Full Stack Developer | AI + Yoga Analytics Research* This project is part of a dedicated research initiative to explore the intersection of **Traditional Indian Sciences** and **Modern Artificial Intelligence**.

---
⭐ **Star this repository if you find this research-driven project helpful!**