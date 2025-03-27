# 🐔 Chicken Feed Calculator

## 📌 Overview
The **Chicken Feed Calculator** is a simple tool that helps farmers determine the optimal amount of feed for their chickens based on breed and flock size. It ensures chickens receive balanced nutrition by calculating the correct mix of corn, soybean, and fishmeal.

## 🎯 Features
- Select chicken breed (Broilers, Layers, Free-range)
- Input the number of chickens
- Get an instant feed requirement breakdown
- User-friendly interface powered by **Streamlit**

## 🖥️ Installation
### **1. Install Python (if not installed)**
Ensure Python 3 is installed. Check by running:
```bash
python3 --version
```
If not installed, download it from [python.org](https://www.python.org/downloads/).

### **2. Install Dependencies**
Install **Streamlit** using pip:
```bash
pip3 install streamlit
```

### **3. Clone or Download the Project**
```bash
git clone https://github.com/your-username/chicken-feed-calculator.git
cd chicken-feed-calculator
```

### **4. Run the Application**
```bash
streamlit run chicken_feed_app.py
```

This will launch the app in your default web browser.

## 🚀 Deployment Options
### **1. Share as a Python Script**
Send the `chicken_feed_app.py` file to others. They can install Streamlit and run it locally.

### **2. Convert to an Executable (.app or .exe)**
For Mac:
```bash
pip install pyinstaller
pyinstaller --onefile --windowed chicken_feed_app.py
```
For Windows:
```bash
pyinstaller --onefile chicken_feed_app.py
```
This will create an executable inside the `dist/` folder.

### **3. Host on Streamlit Cloud (Recommended)**
1. Upload `chicken_feed_app.py` to a **GitHub repository**.
2. Sign up at [Streamlit Cloud](https://share.streamlit.io/).
3. Deploy the app from your GitHub repo.
4. Share the public link!

## ⚡ Example Usage
1. Open the app.
2. Select "Broilers" as the breed.
3. Enter "50" as the number of chickens.
4. Click "Calculate Feed".
5. The app will display the required feed in grams per day.

## 📝 License
This project is open-source under the **MIT License**.

## 🤝 Contributing
Pull requests are welcome! If you'd like to contribute, please fork the repository and submit a PR.

## 📞 Support
For questions or suggestions, feel free to reach out via GitHub Issues.

---

### 📄 README for GitHub
Rename this file to `README.md` before uploading to GitHub.
- GitHub automatically displays `README.md` on the repository homepage.
- Ensure your repository includes a `.gitignore` file to exclude unnecessary files (e.g., `__pycache__/`, `dist/`, `.venv/`).
- Add a license file (`LICENSE.md`) if you want to specify usage permissions.

```bash
git add README.md
git commit -m "Added README file"
git push origin main
```
Now your project will have a professional README visible on GitHub!

