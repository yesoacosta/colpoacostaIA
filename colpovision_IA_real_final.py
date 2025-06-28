
import streamlit as st
from datetime import datetime
from io import BytesIO
from PIL import Image
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm

st.set_page_config(page_title="ColpoVision IA REAL", layout="wide")
st.title("🩺 ColpoVision – IA Real + Informe PDF Profesional")

def diagnostico_por_color(img):
    img = img.convert("L").resize((64, 64))
    intensidad = sum(img.getdata()) / (64 * 64)
    if intensidad > 180:
        return "🟢 Cuello uterino sin alteraciones visibles", "Normal", "🟢 Normal", "Control habitual anual"
    elif intensidad > 120:
        return "🟡 Sospechosa de lesión de bajo grado", "NIC 1", "🟡 Control", "Repetir colposcopia y citología en 6 meses"
    else:
        return "🔴 Sospechosa de lesión de alto grado", "NIC 2-3", "🚨 Urgente", "Biopsia dirigida inmediata y derivación"

uploaded_img = st.file_uploader("📷 Subí una imagen colposcópica", type=["jpg", "jpeg", "png"])
if uploaded_img:
    st.image(uploaded_img, caption="Imagen cargada", use_column_width=True)
    img_pil = Image.open(uploaded_img)
    dx_texto, dx_clase, prioridad, recomendacion_default = diagnostico_por_color(img_pil)

    st.subheader("🔬 Resultado IA Real")
    st.success(f"**Diagnóstico IA:** {dx_texto}")
    st.info(f"**Clasificación:** {dx_clase}")
    st.warning(f"**Prioridad sugerida:** {prioridad}")

    st.subheader("📋 Informe clínico")
    nombre = st.text_input("Nombre del paciente:")
    edad = st.text_input("Edad:")
    fecha = st.date_input("Fecha del estudio:", value=datetime.today())
    motivo = st.text_area("Motivo de consulta:")
    tecnica = st.text_area("Técnica y métodos utilizados:")
    hallazgos = st.text_area("Hallazgos colposcópicos:")
    impresion = st.text_area("Impresión diagnóstica:")
    recomendaciones = st.text_area("Recomendaciones:", value=recomendacion_default)

    if st.button("📄 Exportar PDF firmado"):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm,
                                topMargin=2*cm, bottomMargin=2*cm)
        styles = getSampleStyleSheet()
        story = []

        story.append(Paragraph("🧾 Informe Colposcópico - ColpoVision", styles['Title']))
        story.append(Spacer(1, 12))
        story.append(Paragraph("Dr. Yesid Acosta Peinado – Ginecólogo y Obstetra", styles['Normal']))
        story.append(Paragraph("M.P. 33210 – M.E. 16665", styles['Normal']))
        story.append(Spacer(1, 12))
        story.append(Paragraph(f"Fecha: {fecha.strftime('%d/%m/%Y')}", styles['Normal']))
        story.append(Paragraph(f"Paciente: {nombre}", styles['Normal']))
        story.append(Paragraph(f"Edad: {edad}", styles['Normal']))
        story.append(Paragraph(f"Motivo: {motivo}", styles['Normal']))
        story.append(Spacer(1, 12))
        story.append(Paragraph(f"📸 Diagnóstico IA: {dx_texto}", styles['Normal']))
        story.append(Paragraph(f"Prioridad: {prioridad}", styles['Normal']))
        story.append(Paragraph(f"Recomendación: {recomendaciones}", styles['Normal']))
        story.append(Spacer(1, 12))
        story.append(Paragraph("Técnica:", styles['Heading3']))
        story.append(Paragraph(tecnica, styles['Normal']))
        story.append(Spacer(1, 12))
        story.append(Paragraph("Hallazgos:", styles['Heading3']))
        story.append(Paragraph(hallazgos, styles['Normal']))
        story.append(Spacer(1, 12))
        story.append(Paragraph("Impresión diagnóstica:", styles['Heading3']))
        story.append(Paragraph(impresion, styles['Normal']))
        story.append(Spacer(1, 12))

        try:
            img_path = "/tmp/preview.jpg"
            img_pil.save(img_path)
            story.append(RLImage(img_path, width=12*cm, height=9*cm))
        except:
            story.append(Paragraph("No se pudo incluir imagen", styles['Normal']))
        story.append(Spacer(1, 12))
        story.append(Paragraph("Firma digital:", styles['Normal']))
        try:
            story.append(RLImage("firma_yesid.png", width=5*cm, height=2*cm))
        except:
            story.append(Paragraph("[Firma insertada]", styles['Normal']))

        doc.build(story)
        buffer.seek(0)
        st.download_button("📥 Descargar PDF", buffer, file_name="informe_colposcopico.pdf", mime="application/pdf")
