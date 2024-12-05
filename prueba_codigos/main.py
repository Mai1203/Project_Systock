import cv2
from pyzbar.pyzbar import decode

def main():
    # Abrir la cámara
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error al abrir la cámara.")
        return
    
    print("Presiona 'q' para salir.")
    
    while True:
        ret, frame = cap.read()
        
        if not ret:
            print("No se pudo capturar el cuadro de la cámara.")
            break
        
        # Decodificar códigos de barras en el cuadro
        barcodes = decode(frame)
        
        for barcode in barcodes:
            # Obtener datos del código de barras
            barcode_data = barcode.data.decode('utf-8')
            barcode_type = barcode.type
            
            # Dibujar un rectángulo alrededor del código de barras
            x, y, w, h = barcode.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # Mostrar información decodificada
            text = f"{barcode_data} ({barcode_type})"
            cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        # Mostrar el cuadro
        cv2.imshow("Lectura de códigos de barras", frame)
        
        # Salir si se presiona 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Liberar la cámara y cerrar ventanas
    cap.release()
    cv2.destroyAllWindows()

if _name_ == "_main_":
    main()