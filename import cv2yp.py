import cv2
import pytesseract
import re

# Cargar la imagen
image = cv2.imread(r'C:\piton\yape\yp.jpg')

# Convertir la imagen a escala de grises
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Umbralización para mejorar el contraste
_, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)

# Encontrar los contornos en la imagen
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Filtrar los contornos para encontrar el borde morado (ajustar según sea necesario)
for contour in contours:
    area = cv2.contourArea(contour)
    if area > 1000:  # Ajusta según el tamaño esperado del borde morado
        x, y, w, h = cv2.boundingRect(contour)
        roi = image[y:y+h, x:x+w]

        # Extraer texto usando Tesseract
        text = pytesseract.image_to_string(roi)
        print("Texto Extraído Completo:\n", text)

        # Filtrar y almacenar solo las líneas necesarias
        lines = text.splitlines()
        filtered_lines = []

        # Expresiones regulares para buscar patrones específicos
        for line in lines:
            # Detectar las líneas específicas
            if re.search(r'(?i)yapeaste', line):
                filtered_lines.append(f"Yapeaste: {line}")
            elif re.search(r'\b10\b', line):  # Montos exactos de 10
                filtered_lines.append(f"Monto: {line}")
            elif re.search(r'Carlos Gustavo|Fernandez Calcina', line, re.IGNORECASE):
                filtered_lines.append(f"Nombre: {line}")
            elif re.search(r'\d{2} \bago\b\.? 2024', line):
                filtered_lines.append(f"Fecha: {line}")
            elif re.search(r'disni', line, re.IGNORECASE):
                filtered_lines.append(f"Destino: {line}")
            elif re.search(r'\d{8,}', line):  # Números de operación
                filtered_lines.append(f"Operación: {line}")

        # Mostrar solo las líneas filtradas
        print("Líneas Filtradas:\n", "\n".join(filtered_lines))

        # Aquí puedes almacenar las líneas en una base de datos o archivo si es necesario
