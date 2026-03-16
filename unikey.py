llave_maestra = "e888b8b8a7703166693d8a58b78cc594"
nombre_usuario = "ELIS GARCES"

def iniciar_sesion():
    print(f"\n--- SISTEMA UNIKEY: BIENVENIDO {nombre_usuario} ---")
    intento = input("Por favor, introduce tu código secreto de acceso: ")
    
    if intento == "1966":
        print("\n************************************************")
        print(f"IDENTIDAD VERIFICADA CON ÉXITO.")
        print(f"HOLA, {nombre_usuario}. BIENVENIDO AL FUTURO.")
        print(f"TU LLAVE MAESTRA ACTIVA ES: {llave_maestra}")
        print("************************************************\n")
    else:
        print("\nERROR: El código es incorrecto. Acceso Denegado.")
        print("SISTEMA BLOQUEADO POR SEGURIDAD.\n")

iniciar_sesion()
