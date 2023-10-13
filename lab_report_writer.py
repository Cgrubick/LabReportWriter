from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from PIL import Image as pilImage

def resize_image(image_path, width=6*inch):
    """Resizes an image to fit within a specified width while maintaining aspect ratio."""
    pil_img = pilImage.open(image_path)
    aspect = pil_img.height / pil_img.width
    return image_path, width, width * aspect

def create_lab_report(month, date, lab_number, objectives, procedures, circuits, results, conclusions):
    """Create a PDF lab report in the provided format."""
    output_filename="lab_report"+lab_number+".pdf"
    doc = SimpleDocTemplate(output_filename, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    centered_style = ParagraphStyle(name='Centered', parent=styles['Heading1'], alignment=TA_CENTER, leading=50, fontName='Times-Roman')
    figure_style = ParagraphStyle(name='Figure', parent=styles['BodyText'], alignment=TA_CENTER,fontName='Times-Roman')
    styles['BodyText'].fontName = 'Times-Roman'
    
    # New section header style: larger font and bold
    section_header_style = ParagraphStyle(name='SectionHeader', parent=styles['Heading1'], fontSize=18, spaceAfter=12,fontName='Times-Roman')

    # Header with increased spacing
    elements.append(Paragraph("EE 355L", centered_style))
    elements.append(Spacer(1, 24))  # Spacer for added space
    elements.append(Paragraph(f"Fall 2023", centered_style))
    elements.append(Spacer(1, 24))
    elements.append(Paragraph(f"{month} {date} 2023", centered_style))
    elements.append(Spacer(1, 24))
    elements.append(Paragraph(f"Lab Report #{lab_number}", centered_style))
    elements.append(Spacer(1, 24))
    elements.append(Paragraph("Clayton Grubick", centered_style))
    elements.append(Spacer(1, 24))
    elements.append(Paragraph("West Virginia University", centered_style))
    elements.append(PageBreak())



    # Objective
    elements.append(Paragraph("1. Objective", section_header_style))
    for objective in objectives:
        elements.append(Paragraph(objective, styles['BodyText']))

    # Procedure
    elements.append(Paragraph("2. Procedure", section_header_style))
    for procedure in procedures:
        elements.append(Paragraph(procedure, styles['BodyText']))
    figure_count = 1

    # Circuit Diagrams
    elements.append(Paragraph("3. Circuit Diagram(s)", section_header_style))
    for result in circuits:
        if isinstance(result, tuple) and any(result[0].endswith(ext) for ext in ['.png', '.jpg', '.jpeg']):
            img_path, w, h = resize_image(result[0])
            img = Image(img_path, width=w, height=h)
            elements.append(img)
            elements.append(Paragraph(f"Figure {figure_count}.) {result[1]}", figure_style))
            figure_count += 1
        else:
            elements.append(Paragraph(result, styles['BodyText']))

    # Results & Discussion
    elements.append(Paragraph("4. Results & Discussion (Values, Graph & Waveforms)", section_header_style))
    for result in results:
        if isinstance(result, tuple) and any(result[0].endswith(ext) for ext in ['.png', '.jpg', '.jpeg']):
            img_path, w, h = resize_image(result[0])
            img = Image(img_path, width=w, height=h)
            elements.append(img)
            elements.append(Paragraph(f"Figure {figure_count}.) {result[1]}", figure_style))
            figure_count += 1
        else:
            elements.append(Paragraph(result, styles['BodyText']))

    # Conclusion
    elements.append(Paragraph("5. Conclusion", section_header_style))
    for conclusion in conclusions:
        elements.append(Paragraph(conclusion, styles['BodyText']))

    doc.build(elements)


def parse_input_file(filename):
    with open(filename, 'r') as file:
        content = file.read()

    sections = content.split('---')
    data = {}

    for section in sections:
        lines = [line.strip() for line in section.split('\n') if line.strip()]
        if not lines:
            continue
        key = lines[0].replace(':', '')
        data[key] = lines[1:]

    # Debugging print
    print(data)

    return data


if __name__ == "__main__":
    data = parse_input_file('lab5.txt')
    
    month = data.get('MONTH', ['Unknown Month'])[0]  # Since 'MONTH' corresponds to a list with one item, get the first item
    date = data.get('DATE', ['Unknown DATE'])[0]   # Same for 'DATE'
    lab_number = data.get('LAB_NUMBER', ['Unknown LAB'])[0]   # And for 'LAB_NUMBER'
    objectives = data['OBJECTIVES']
    procedures = data['PROCEDURES']
    
    # Parsing circuits and results for tuple data
    circuits = [(item.split(", ")[0], item.split(", ")[1]) for item in data['CIRCUITS'] if ', ' in item]
    results = []
    for item in data['RESULTS']:
        if ', ' in item:
            results.append((item.split(", ")[0], item.split(", ")[1]))
        else:
            results.append(item)
    
    conclusions = data['CONCLUSIONS']

    create_lab_report(month, date, lab_number, objectives, procedures, circuits, results, conclusions)
