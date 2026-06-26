# Version: 1.6 - Shipathon: Smart Agentic Engine (Precision Word Count & Overflow)
import streamlit as st
import requests
import json
import io
import urllib.parse
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from docx import Document
from docx.shared import Pt as DocxPt
from io import BytesIO

# --- CONFIG ---
OPENROUTER_API_KEY = "API_Key"
PEXELS_API_KEY = "API_Key" 
MODEL = "openai/gpt-4o-mini" 

st.set_page_config(page_title="Shipathon Engine", page_icon="🚀", layout="centered")
st.title("🚀 Shipathon: Smart Agentic Engine")
st.markdown("---")

def get_real_image(query):
    headers = {"Authorization": PEXELS_API_KEY}
    url = f"https://api.pexels.com/v1/search?query={urllib.parse.quote(query)}&per_page=1"
    try:
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code == 200:
            data = res.json()
            if data['photos']:
                return BytesIO(requests.get(data['photos'][0]['src']['large']).content)
    except: pass
    return None

# --- UI ---
user_input = st.text_area("Project Topic:", "A detailed scientific report on cattle biology", height=100)

col1, col2 = st.columns(2)
with col1:
    req_pages = st.number_input("Desired No. of Slides/Pages:", min_value=1, max_value=20, value=1)
with col2:
    total_words = st.number_input("Total Word Count Target:", min_value=100, max_value=5000, value=1000)

if st.button("🚀 Analyze & Ship"):
    wpp = total_words / req_pages
    
    # Intelligence Layer
    if wpp <= 180:
        forced_format = "pptx"
    elif wpp >= 400:
        forced_format = "docx"
    else:
        forced_format = "auto"

    with st.spinner(f"Agent is generating high-density content..."):
        
        chunks_per_page = 4 if forced_format == "docx" else 1
        total_sections = req_pages * chunks_per_page
        words_per_section = total_words // total_sections
        
        system_prompt = f"""
        You are a Document Architect. 
        Format: {forced_format}. Total Sections: {total_sections}.
        Target per section: {words_per_section} words.
        
        STRICT: Do NOT summarize. Write verbose, academic paragraphs. 
        For 'docx', combine sections. For 'pptx', use bullets and 'pexels_search'.
        
        Return ONLY JSON:
        {{
          "format": "pptx or docx",
          "title": "Main Title",
          "sections": [
            {{ "header": "Title", "body": "Verbose text", "pexels_search": "query" }}
          ]
        }}
        """
        
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {OPENROUTER_API_KEY}"},
                json={
                    "model": MODEL, 
                    "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_input}],
                    "response_format": { "type": "json_object" }
                }
            )
            data = json.loads(response.json()['choices'][0]['message']['content'])
            fmt = data.get("format", "docx")
            sections = data.get("sections")
            
            # --- PRECISION WORD & PAGE CALCULATION ---
            actual_word_count = sum(len(s['body'].split()) for s in sections)
            
            # Standard Page Density (approx 450 words/page for 11pt Arial)
            actual_page_count = max(1, (actual_word_count // 450) + (1 if actual_word_count % 450 > 0 else 0))
            
            # Trigger warning ONLY if actual pages > requested pages
            if fmt == "docx" and actual_page_count > req_pages:
                st.warning(f"📝 **Agent Note:** Generated **{actual_word_count} words**. Since the word count was very high, I had to extend the report to **{actual_page_count} pages** to maintain formatting.")

            # --- DOCX ENGINE ---
            if fmt == "docx":
                doc = Document()
                doc.add_heading(data.get("title", "Report"), 0)
                f_size = 10 if wpp > 800 else 11
                
                for i, s in enumerate(sections):
                    doc.add_heading(s['header'], level=1)
                    p = doc.add_paragraph()
                    run = p.add_run(s['body'])
                    run.font.size = DocxPt(f_size)
                    
                    if (i + 1) % chunks_per_page == 0:
                        doc.add_page_break()
                
                buf = BytesIO()
                doc.save(buf)
                st.download_button(f"📥 Download {actual_word_count} Word DOCX", data=buf.getvalue(), file_name="output.docx")

            # --- PPTX ENGINE ---
            else:
                prs = Presentation()
                prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
                for s in sections:
                    slide = prs.slides.add_slide(prs.slide_layouts[6])
                    bg = slide.shapes.add_shape(1, 0, 0, prs.slide_width, prs.slide_height)
                    bg.fill.solid()
                    bg.fill.fore_color.rgb = RGBColor(15, 20, 30)
                    
                    t_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.4), Inches(12), Inches(1))
                    t_p = t_box.text_frame.paragraphs[0]
                    p_text = s['header'].upper()
                    t_p.text = p_text
                    t_p.font.size, t_p.font.bold, t_p.font.color.rgb = Pt(40), True, RGBColor(173, 255, 47)
                    
                    b_box = slide.shapes.add_textbox(Inches(0.5), Inches(1.8), Inches(6), Inches(5.5))
                    b_p = b_box.text_frame.paragraphs[0]
                    b_p.text = s['body']
                    b_p.font.size, b_p.font.color.rgb = Pt(18), RGBColor(240, 240, 240)
                    
                    if s.get('pexels_search'):
                        img = get_real_image(s['pexels_search'])
                        if img: slide.shapes.add_picture(img, Inches(7.0), Inches(1.8), width=Inches(5.8))
                
                buf = BytesIO()
                prs.save(buf)
                st.download_button("📥 Download PPTX", data=buf.getvalue(), file_name="output.pptx")

            st.success(f"Successfully Shipped! Actual Word Count: {actual_word_count} 🚢")

        except Exception as e:
            st.error(f"Error: {e}")
