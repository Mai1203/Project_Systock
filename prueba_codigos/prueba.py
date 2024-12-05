import ctypes

try:
    ctypes.cdll.LoadLibrary("libzbar-64.dll")
    print("libzbar cargada correctamente.")
except OSError as e:
    print(f"No se pudo cargar libzbar: {e}")
