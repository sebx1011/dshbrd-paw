def calcular_tasa_biometria(invocaciones_generar, invocaciones_firmar):
    if invocaciones_generar > 0:
        tasa_biometria = round((invocaciones_firmar / invocaciones_generar) * 100, 2)
    else:
        tasa_biometria = None
    return tasa_biometria
