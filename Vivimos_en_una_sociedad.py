import random

def generar_registro():
    # El primer bit representa el signo (1 para negativo, 0 para positivo)
    # El último bit representa 0.5, los demás son bits aleatorios
    registro = [random.randint(0, 1) for _ in range(7)]  # Genera 8 bits aleatorios (valores binarios)
    signo = random.randint(0, 1)
    registro.insert(0, signo)
    registro.append(0)  # Añade el último bit como 0.5
    return registro

def binario_a_decimal(registro):
    decimal = 0
    for i in range(len(registro)):
        if i == 0:  # Si es el primer bit (signo)
            decimal -= registro[i] * 512  # -512 si es negativo, 0 si es positivo
        elif i == len(registro) - 1:  # Si es el último bit (0.5)
            decimal += registro[i] * 0.5
        else:
            decimal += registro[i] * (2 ** (len(registro) - 2 - i))
    return decimal

def evaluar_funcion(x):
    return 3 * (x - 1) ** 2 + 0.7 * x + 3

def calcular_fitness(registro_decimal):
    x = registro_decimal / 511  # Normaliza el valor entre -1 y 1
    y = evaluar_funcion(x)
    return y

def seleccion_padres(poblacion, n_padres):
    padres = []
    for _ in range(n_padres):
        padre = random.choice(poblacion)
        padres.append(padre)
    return padres

def crossover(padre1, padre2):
    punto_corte = random.randint(1, len(padre1) - 1)
    hijo1 = padre1[:punto_corte] + padre2[punto_corte:]
    hijo2 = padre2[:punto_corte] + padre1[punto_corte:]
    return hijo1, hijo2

def mutacion(registro, prob_mutacion):
    for i in range(len(registro)):
        if random.random() < prob_mutacion:
            registro[i] = 1 - registro[i]  # Cambia el bit
    return registro

# Generar el número de registros
n = random.randint(3, 5)
num_registros = 2 ** n

# Parámetros del algoritmo genético
num_generaciones = random.randint(10,50)
tamano_poblacion = num_registros
prob_crossover = 0.8
prob_mutacion = 0.1
VI = 1  # Variable para el número de generación inicializada en 1
# Generar población inicial
poblacion = [(generar_registro(), None) for _ in range(tamano_poblacion)]

# Evolución de la población
for generacion in range(num_generaciones):
    # Mostrar resultados iniciales
    print(f"Generacion {VI}:")  # Mostrar el número de generación
    for i, (registro, _) in enumerate(poblacion):
        valor_decimal = binario_a_decimal(registro)
        valor_funcion = evaluar_funcion(valor_decimal / 511)
        print(f"Registro {i + 1}: {registro} Valor Decimal: {valor_decimal} Valor Función: {valor_funcion}")

    # Incrementar el número de generación
    VI += 1
    # Ordenar población por valor de función
    poblacion_ordenada = sorted([(calcular_fitness(binario_a_decimal(registro)), registro, i) for i, (registro, _) in enumerate(poblacion)], reverse=True)

    # Mostrar resultados ordenados
    print("\nResultados ordenados por valor de función (de mayor a menor):")
    for i, (valor_funcion, registro, index) in enumerate(poblacion_ordenada):
        valor_decimal = binario_a_decimal(registro)
        print(f"Registro {index + 1}: {registro} Valor Decimal: {valor_decimal} Valor Función: {valor_funcion}")

    # Lista para almacenar los nuevos registros resultantes de la combinación
    nuevos_registros = []

    # Combinar los mejores registros entre sí
    registros_utilizados = set()  # Para mantener un seguimiento de los registros combinados
    while len(registros_utilizados) < len(poblacion):
        # Buscar los dos mejores registros que no han sido combinados aún
        mejores_registros = [(registro, i) for valor_funcion, registro, i in poblacion_ordenada if i not in registros_utilizados][:2]

        # Si no quedan suficientes registros para combinar, salir del bucle
        if len(mejores_registros) < 2:
            break

        # Seleccionar los dos mejores registros para combinar
        mejor1_registro, mejor1_idx = mejores_registros[0]
        mejor2_registro, mejor2_idx = mejores_registros[1]

        # Intercambiar los últimos 4 bits entre los registros
        registro_mejor1 = mejor1_registro[:]
        registro_mejor2 = mejor2_registro[:]
        registro_mejor1[-5:], registro_mejor2[-5:] = registro_mejor2[-5:], registro_mejor1[-5:]

        # Mostrar los registros combinados y el resultado de la combinación
        print(f"\nCombinación del Registro {mejor1_idx + 1} con el Registro {mejor2_idx + 1}:")
        print(f"Registro {mejor1_idx + 1}:", mejor1_registro)
        print(f"Registro {mejor2_idx + 1}:", mejor2_registro)
        print("Nuevo registro 1:", registro_mejor1)
        print("Nuevo registro 2:", registro_mejor2)

        # Actualizar la población con los registros combinados
        poblacion[mejor1_idx] = (registro_mejor1, None)
        poblacion[mejor2_idx] = (registro_mejor2, None)

        # Registrar los registros utilizados
        registros_utilizados.add(mejor1_idx)
        registros_utilizados.add(mejor2_idx)

        # Agregar los nuevos registros a la lista
        nuevos_registros.append(registro_mejor1)
        nuevos_registros.append(registro_mejor2)

    # Mostrar los nuevos registros resultantes de la combinación
    print("\nNuevos registros resultantes de la combinación:")
    for i, registro in enumerate(nuevos_registros, start=1):
        valor_decimal = binario_a_decimal(registro)
        valor_funcion = evaluar_funcion(valor_decimal / 511)
        print(f"Nuevo Registro {i}: {registro} Valor Decimal: {valor_decimal} Valor Función: {valor_funcion}")
    # Elegir dos índices de registro al azar
    indice_registro1, indice_registro2 = random.sample(range(len(nuevos_registros)), 2)


    # Seleccionar los registros utilizando los índices obtenidos
    registro1 = nuevos_registros[indice_registro1]
    registro2 = nuevos_registros[indice_registro2]
    # Elegir dos índices de registro al azar
    indice_registro1, indice_registro2 = random.sample(range(len(nuevos_registros)), 2)

    # Seleccionar los registros utilizando los índices obtenidos
    registro1 = nuevos_registros[indice_registro1].copy()
    registro2 = nuevos_registros[indice_registro2].copy()

    # Elegir un bit aleatorio para intercambiar en cada registro
    bit_registro1 = random.randint(0, len(registro1) - 1)
    bit_registro2 = random.randint(0, len(registro2) - 1)

    # muta los bits seleccionados
    registro1[bit_registro1] = 1 - registro1[bit_registro1]
    registro2[bit_registro2] = 1 - registro2[bit_registro2]

    # Mostrar los registros seleccionados al azar y los bits intercambiados
    print("\nRegistros seleccionados para mutación:")
    print(f"Registro {indice_registro1 + 1}: {registro1}")
    print(f"Registro {indice_registro2 + 1}: {registro2}")
    print(f"Posición de mutación en Registro {indice_registro1 + 1}:", bit_registro1)
    print(f"Posición de mutación en Registro {indice_registro2 + 1}:", bit_registro2)

    # Reemplazar los registros originales en la población por los registros cambiados
    poblacion[indice_registro1] = (registro1, None)
    poblacion[indice_registro2] = (registro2, None)

    # Ordenar población por valor de función
    poblacion_ordenada = sorted([(calcular_fitness(binario_a_decimal(registro)), registro, i) for i, (registro, _) in enumerate(poblacion)], reverse=True)

    # Mostrar resultados ordenados después del cambio
    print("\nResultados ordenados después de la mutación:")
    for i, (valor_funcion, registro, index) in enumerate(poblacion_ordenada):
        valor_decimal = binario_a_decimal(registro)
        print(f"Registro {index + 1}: {registro} Valor Decimal: {valor_decimal} Valor Función: {valor_funcion}")
        