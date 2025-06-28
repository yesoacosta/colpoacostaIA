
import streamlit as st
from datetime import datetime
from io import BytesIO
from PIL import Image
from fpdf import FPDF

st.set_page_config(page_title="ColpoVision Estética Moderna", layout="wide")
st.title("📋 ColpoVision – Informe Estético Profesional")

def diagnostico_IA_basico(img):
    img = img.convert("L").resize((64, 64))
    nivel = sum(img.getdata()) / (64 * 64)
    if nivel > 180:
        return "🟢 Normal", "Control anual habitual"
    elif nivel > 120:
        return "🟡 Sospecha de NIC 1", "Repetir colposcopia y PAP en 6 meses"
    else:
        return "🔴 Sospecha de NIC 2-3", "Biopsia dirigida inmediata"

uploaded_img = st.file_uploader("📷 Cargar imagen colposcópica", type=["jpg", "jpeg", "png"])
if uploaded_img:
    st.image(uploaded_img, caption="Imagen cargada", use_column_width=True)
    imagen = Image.open(uploaded_img)
    dx, reco = diagnostico_IA_basico(imagen)

    st.subheader("📊 Resultado IA sugerido")
    st.write(f"**Diagnóstico IA:** {dx}")
    st.write(f"**Recomendación:** {reco}")

    st.subheader("📝 Informe médico personalizado")
    nombre = st.text_input("Nombre del paciente")
    edad = st.text_input("Edad")
    fecha = st.date_input("Fecha del estudio", value=datetime.today())
    motivo = st.text_area("Motivo de consulta")
    tecnica = st.text_area("Técnica y métodos utilizados")
    macro = st.text_area("Hallazgos macroscópicos")
    reaccion = st.text_area("Hallazgos con ácido acético y Lugol")
    zona = st.text_area("Zona de transformación")
    impresion = st.text_area("Impresión diagnóstica")
    recomendacion = st.text_area("Recomendaciones", value=reco)

    if st.button("📄 Descargar PDF con diseño moderno"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", "B", 16)
        pdf.set_text_color(40, 40, 60)
        pdf.image("logo_colpovision.png", 10, 8, 40)
        pdf.cell(0, 10, "Informe Colposcópico", ln=True, align="C")
        pdf.set_font("Arial", "", 12)
        pdf.ln(10)
        pdf.set_text_color(0)
        pdf.multi_cell(0, 8, f"Fecha del estudio: {fecha.strftime('%d/%m/%Y')}")
        pdf.multi_cell(0, 8, f"Paciente: {nombre} | Edad: {edad}")
        pdf.multi_cell(0, 8, f"Motivo de consulta: {motivo}")

        pdf.ln(5)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 8, "Técnica y Métodos Utilizados", ln=True)
        pdf.set_font("Arial", "", 12)
        pdf.multi_cell(0, 8, tecnica)
        pdf.ln(2)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 8, "Hallazgos Macroscópicos", ln=True)
        pdf.set_font("Arial", "", 12)
        pdf.multi_cell(0, 8, macro)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 8, "Hallazgos con Ácido Acético y Lugol", ln=True)
        pdf.set_font("Arial", "", 12)
        pdf.multi_cell(0, 8, reaccion)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 8, "Zona de Transformación", ln=True)
        pdf.set_font("Arial", "", 12)
        pdf.multi_cell(0, 8, zona)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 8, "Impresión Diagnóstica", ln=True)
        pdf.set_font("Arial", "", 12)
        pdf.multi_cell(0, 8, impresion)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 8, "Recomendaciones", ln=True)
        pdf.set_font("Arial", "", 12)
        pdf.multi_cell(0, 8, recomendacion)

        pdf.ln(10)
        pdf.image("firma_yesid.png", x=10, w=40)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Dr. Yesid Acosta Peinado", ln=True)
        pdf.set_font("Arial", "", 11)
        pdf.cell(0, 7, "Ginecólogo y Obstetra", ln=True)
        pdf.cell(0, 7, "M.P. 33210 – M.E. 16665", ln=True)

        if imagen:
            img_path = "/tmp/img_preview.jpg"
            imagen.save(img_path)
            pdf.image(img_path, x=130, y=210, w=60)
            pdf.set_xy(130, 275)
            pdf.set_font("Arial", "", 8)
            pdf.cell(60, 5, "Imagen utilizada para el análisis automatizado por IA", 0, 1, 'C')

        pdf_output = BytesIO()
        pdf.output(pdf_output)
        pdf_output.seek(0)
        st.download_button("📥 Descargar informe PDF moderno", data=pdf_output, file_name="informe_colposcopico_moderno.pdf")
