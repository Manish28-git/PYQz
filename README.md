# Previous Year Question Paper Hub

A Flask-based web application to upload, organize, browse, and download past exam papers by academic year. Files are automatically stored in year-folders (e.g. `2017-2018`, `2018-2019`, …, `2024-2025`) and displayed in collapsible dropdowns. Includes search/filter and delete functionality, all wrapped in a modern glassmorphism UI.

---

## 🚀 Features

- **Upload** single PDF files into a chosen academic-year folder  
- **Automatic folder creation** for years 2017-2018 through 2024-2025  
- **Grouped display**: each year is a collapsible dropdown showing its papers  
- **Search/Filter** by title, subject, or year  
- **Download** any paper with one click  
- **Delete** unwanted uploads from both disk and database  
- **Glassmorphism UI** with centered content and modern gradients  

---

## 🛠️ Tech Stack

- **Flask** – Python web framework  
- **Flask-SQLAlchemy** – ORM backed by SQLite  
- **HTML5 `<details>`/`<summary>`** – native accordion dropdown  
- **Vanilla CSS** – glass-effect styling, responsive layout  

---

## 📦 Installation

1. **Clone the repo**  
   ```bash
   git clone https://github.com/YourUser/previous-year-paper-hub.git
   cd previous-year-paper-hub

2. Create & activate a virtualenv

3. Install dependencies

4. Run the app