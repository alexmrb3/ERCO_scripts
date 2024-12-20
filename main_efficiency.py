from read_device import ReadDevice
import asyncio
import time

async def main():

    serial_settings = "COM2" #Insert COM# port (Type hint: string)
    function = 4 #Insert function (Type hint: integer)
    address =  40035 #Insert initial address (Type hint: integer)
    quantity = 4 #Insert quantity of registes (Type hint: integer)
    slave_id = 2 #Insert slave_id (Type hint: integer)
    name = "weather"

    weather_station = ReadDevice(serial_settings, function, address, quantity, slave_id, name)

    datos_weather_station = await weather_station.mostrar_atributos()
    #print(datos_weather_station) # Imprimimos los datos obtenidos desde mostrar_atributos




    serial_settings = "COM6" #Insert COM# port (Type hint: string)
    function = 4 #Insert function (Type hint: integer)
    address =  1 #Insert initial address (Type hint: integer)
    quantity = 8 #Insert quantity of registes (Type hint: integer)
    slave_id = 1 #Insert slave_id (Type hint: integer)
    name = "pac3200"

    PAC3200 = ReadDevice(serial_settings, function, address, quantity, slave_id, name)

    datos_PAC3200 = await PAC3200.mostrar_atributos()
    #print(datos_PAC3200)# Imprimimos los datos obtenidos desde mostrar_atributos



    serial_settings = "COM8" #Insert COM# port (Type hint: string)
    function = 4 #Insert function (Type hint: integer)
    address =  30000 #Insert initial address (Type hint: integer)
    quantity = 4 #Insert quantity of registes (Type hint: integer)
    slave_id = 3 #Insert slave_id (Type hint: integer)
    name = "huawei"

    huawei_inverter = ReadDevice(serial_settings, function, address, quantity, slave_id, name)

    datos_huawei_inverter = await huawei_inverter.mostrar_atributos()

    datos_buscados = {"Generation_Accum": datos_huawei_inverter["Generation_Accum"], "Active Energy": datos_PAC3200["Active Energy"], "irradiance": datos_weather_station["irradiance"]}
    return datos_buscados

    #print(f"Datos buscados: Active Energy:{datos_PAC3200["Active Energy"]} y Generation_Accum {datos_huawei_inverter["Generation_Accum"]}")


def imprimir_valores():
    contador = 0  
    while True:
        
        contador += 1
        if contador % 5 == 0:  # Imprime los valores cada 5 segundos
            datos_1 = asyncio.run(main())
            for name, valor in datos_1.items():
                print(f"{name}: {valor}")
        else:
            print(".")  # Imprime punto 
        time.sleep(1)  # Espera 1 segundo

if __name__ == "__main__":
    imprimir_valores()