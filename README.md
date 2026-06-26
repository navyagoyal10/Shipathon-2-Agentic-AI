# ⚙️ Agentic AI Document Generation Engine

**An autonomous AI system utilizing dynamic routing to generate fully formatted Word documents and PowerPoint presentations.**

This project is a smart document generation engine that takes a user's prompt, desired page/slide count, and target word count, and uses an intelligent routing layer to determine the optimal output format. It dynamically generates high-density academic `.docx` reports or structured `.pptx` presentations equipped with contextual, AI-fetched visual assets.

## 🚀 Key Features

* **Dynamic Intent Routing:** The system calculates a "Words Per Page" (WPP) density metric. High-density requests (>400 WPP) are automatically routed to a `.docx` generation engine, while lower-density, presentation-style requests (<180 WPP) are routed to a `.pptx` engine.
* **Agentic Task Decomposition:** Utilizes the OpenRouter API (GPT-4o-mini) to break down broad project topics into structured JSON containing titles, section headers, verbose body text, and specific image search queries.
* **Automated Asset Fetching:** The presentation engine integrates with the Pexels API to autonomously search for and download high-resolution background images based on the LLM's contextual queries, embedding them directly into the slides.
* **Precision Overflow Handling:** If the generated word count forces a `.docx` file to exceed the requested page limit (based on standard 11pt Arial constraints), the engine recalculates the pagination and alerts the user of the adjusted page count without breaking the document structure.
* **Custom UI & Styling:** Built with Streamlit for a seamless frontend, featuring automated dark-mode styling and custom typography for the generated PowerPoint slides.

## 🛠️ Tech Stack

* **Language:** Python
* **Frontend:** Streamlit
* **AI / LLM:** OpenRouter API (`openai/gpt-4o-mini`)
* **Asset Integration:** Pexels API
* **Document Processing:** `python-docx`, `python-pptx`

## ⚙️ Installation & Setup

### Option A: Local Python Environment
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/navyagoyal10/Shipathon-2-Agentic-AI.git](https://github.com/navyagoyal10/Shipathon-2-Agentic-AI.git)
   cd Shipathon-2-Agentic-AI
   ```
2. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure API Keys:**
   Open `ps2.py` and replace the placeholder API keys with your own.
4. **Run the application:**
   ```bash
   streamlit run ps2.py
   ```

### Option B: Docker Deployment (Recommended)
This project includes a `Dockerfile` for seamless containerized deployment.
1. **Build the image:**
   ```bash
   docker build -t shipathon-engine .
   ```
2. **Run the container:**
   ```bash
   docker run -p 8501:8501 shipathon-engine
   ```

## 🖥️ Usage

1. Launch the Streamlit interface.
2. Enter your **Project Topic** in the text area (e.g., "A detailed scientific report on quantum computing").
3. Specify the **Desired No. of Slides/Pages** and the **Total Word Count Target**.
4. Click **Analyze & Ship**.
5. The engine will process the request, determine the best format, fetch necessary images, and provide a one-click download button for your generated `.docx` or `.pptx` file.
