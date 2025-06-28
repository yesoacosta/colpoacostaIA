import streamlit as st
from datetime import datetime
from io import BytesIO
from PIL import Image
from fpdf import FPDF
import os
import unicodedata
import tempfile

st.set_page_config(page_title="ColpoVision Estética Moderna", layout="wide")
st.title("📋 ColpoVision – Informe Estético Profesional")

def limpiar_texto(texto):
    """Convierte caracteres especiales a equivalentes ASCII para FPDF"""
    if not texto:
        return ""
    # Reemplazar caracteres problemáticos comunes
    replacements = {
        '\u2013': '-',  # en dash
        '\u2014': '-',  # em dash
        '\u2018': "'",  # left single quotation mark
        '\u2019': "'",  # right single quotation mark
        '\u201C': '"',  # left double quotation mark
        '\u201D': '"',  # right double quotation mark
        '\u2026': '...',  # horizontal ellipsis
        '\u00A0': ' ',  # non-breaking space
    }
    
    for unicode_char, ascii_char in replacements.items():
        texto = texto.replace(unicode_char, ascii_char)
    
    # Normalizar y quitar acentos si es necesario
    try:
        # Intentar codificar en latin-1 para verificar
        texto.encode('latin-1')
        return texto
    except UnicodeEncodeError:
        # Si falla, normalizar caracteres
        texto = unicodedata.normalize('NFD', texto)
        texto = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')
        return texto

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

# Opción para subir logo y firma
logo_img = st.file_uploader("🏥 Subir logo (opcional):", type=["jpg", "jpeg", "png"])
firma_img = st.file_uploader("✍️ Subir firma (opcional):", type=["jpg", "jpeg", "png"])

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
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.set_font("Arial", "B", 16)
            pdf.set_text_color(40, 40, 60)
            
            # Lista para almacenar archivos temporales a limpiar
            temp_files = []
            
            # Manejo del logo
            logo_added = False
            if logo_img is not None:
                try:
                    logo_img.seek(0)
                    logo_pil = Image.open(logo_img)
                    if logo_pil.mode in ("RGBA", "P"):
                        logo_pil = logo_pil.convert("RGB")
                    
                    # Crear archivo temporal con nombre único
                    temp_logo_fd, temp_logo_path = tempfile.mkstemp(suffix='.jpg')
                    temp_files.append(temp_logo_path)
                    
                    with os.fdopen(temp_logo_fd, 'wb') as temp_file:
                        logo_pil.save(temp_file, format='JPEG')
                    
                    pdf.image(temp_logo_path, 10, 8, 40)
                    logo_added = True
                        
                except Exception as e:
                    st.warning(f"No se pudo cargar el logo: {str(e)}")
            
            elif os.path.exists("logo_colpovision.png"):
                try:
                    pdf.image("logo_colpovision.png", 10, 8, 40)
                    logo_added = True
                except:
                    pass
            
            # Si no hay logo, agregar título más prominente
            if not logo_added:
                pdf.set_font("Arial", "B", 20)
                pdf.set_text_color(45, 85, 135)
                pdf.cell(0, 15, "ColpoVision", ln=True, align="C")
                pdf.ln(5)
            
            pdf.set_font("Arial", "B", 16)
            pdf.set_text_color(40, 40, 60)
            pdf.cell(0, 10, "Informe Colposcópico", ln=True, align="C")
            pdf.set_font("Arial", "", 12)
            pdf.ln(10)
            pdf.set_text_color(0)
            pdf.multi_cell(0, 8, f"Fecha del estudio: {fecha.strftime('%d/%m/%Y')}")
            pdf.multi_cell(0, 8, limpiar_texto(f"Paciente: {nombre} | Edad: {edad}"))
            pdf.multi_cell(0, 8, limpiar_texto(f"Motivo de consulta: {motivo}"))

            pdf.ln(5)
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 8, "Tecnica y Metodos Utilizados", ln=True)
            pdf.set_font("Arial", "", 12)
            pdf.multi_cell(0, 8, limpiar_texto(tecnica))
            pdf.ln(2)
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 8, "Hallazgos Macroscopicos", ln=True)
            pdf.set_font("Arial", "", 12)
            pdf.multi_cell(0, 8, limpiar_texto(macro))
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 8, "Hallazgos con Acido Acetico y Lugol", ln=True)
            pdf.set_font("Arial", "", 12)
            pdf.multi_cell(0, 8, limpiar_texto(reaccion))
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 8, "Zona de Transformacion", ln=True)
            pdf.set_font("Arial", "", 12)
            pdf.multi_cell(0, 8, limpiar_texto(zona))
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 8, "Impresion Diagnostica", ln=True)
            pdf.set_font("Arial", "", 12)
            pdf.multi_cell(0, 8, limpiar_texto(impresion))
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 8, "Recomendaciones", ln=True)
            pdf.set_font("Arial", "", 12)
            pdf.multi_cell(0, 8, limpiar_texto(recomendacion))

            pdf.ln(10)
            
            # Manejo de la firma
            firma_added = False
            if firma_img is not None:
                try:
                    firma_img.seek(0)
                    firma_pil = Image.open(firma_img)
                    if firma_pil.mode in ("RGBA", "P"):
                        firma_pil = firma_pil.convert("RGB")
                    
                    # Crear archivo temporal con nombre único
                    temp_firma_fd, temp_firma_path = tempfile.mkstemp(suffix='.jpg')
                    temp_files.append(temp_firma_path)
                    
                    with os.fdopen(temp_firma_fd, 'wb') as temp_file:
                        firma_pil.save(temp_file, format='JPEG')
                    
                    pdf.image(temp_firma_path, x=10, w=40)
                    firma_added = True
                        
                except Exception as e:
                    st.warning(f"No se pudo cargar la firma: {str(e)}")
            
            elif os.path.exists("firma_yesid.png"):
                try:
                    pdf.image("firma_yesid.png", x=10, w=40)
                    firma_added = True
                except:
                    pass
            
            # Información del doctor
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 10, "Dr. Yesid Acosta Peinado", ln=True)
            pdf.set_font("Arial", "", 11)
            pdf.cell(0, 7, "Ginecologo y Obstetra", ln=True)
            pdf.cell(0, 7, "M.P. 33210 - M.E. 16665", ln=True)

            # Manejo de la imagen del estudio
            if imagen:
                try:
                    uploaded_img.seek(0)
                    img_pil = Image.open(uploaded_img)
                    if img_pil.mode in ("RGBA", "P"):
                        img_pil = img_pil.convert("RGB")
                    
                    # Crear archivo temporal con nombre único
                    temp_img_fd, temp_img_path = tempfile.mkstemp(suffix='.jpg')
                    temp_files.append(temp_img_path)
                    
                    with os.fdopen(temp_img_fd, 'wb') as temp_file:
                        img_pil.save(temp_file, format='JPEG')
                    
                    pdf.image(temp_img_path, x=130, y=210, w=60)
                    pdf.set_xy(130, 275)
                    pdf.set_font("Arial", "", 8)
                    pdf.cell(60, 5, "Imagen utilizada para el análisis automatizado por IA", 0, 1, 'C')
                        
                except Exception as e:
                    st.warning(f"No se pudo incluir la imagen en el PDF: {str(e)}")

            # CORRECCIÓN PRINCIPAL: Usar archivo temporal para el PDF final
            temp_pdf_fd, temp_pdf_path = tempfile.mkstemp(suffix='.pdf')
            temp_files.append(temp_pdf_path)
            
            # Cerrar el descriptor de archivo antes de usarlo con FPDF
            os.close(temp_pdf_fd)
            
            # Generar el PDF en archivo temporal
            pdf.output(temp_pdf_path, 'F')  # 'F' para archivo
            
            # Leer el archivo PDF generado como bytes
            with open(temp_pdf_path, 'rb') as pdf_file:
                pdf_bytes = pdf_file.read()
            
            # Limpiar archivos temporales
            for temp_file in temp_files:
                try:
                    if os.path.exists(temp_file):
                        os.remove(temp_file)
                except:
                    pass
            
            st.download_button(
                "📥 Descargar informe PDF moderno", 
                data=pdf_bytes, 
                file_name="informe_colposcopico_moderno.pdf",
                mime="application/pdf"
            )
            st.success("✅ PDF generado correctamente!")
            
        except Exception as e:
            st.error(f"Error al generar el PDF: {str(e)}")
            # Limpiar archivos temporales en caso de error
            try:
                for temp_file in temp_files:
                    if os.path.exists(temp_file):
                        os.remove(temp_file)
            except:
                pass
