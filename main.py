
from read_device import ReadDevice
import asyncio

async def main():

    serial_settings = "COM2" #Insert COM# port (Type hint: string)
    function = 4 #Insert function (Type hint: integer)
    address =  40035 #Insert initial address (Type hint: integer)
    quantity = 4 #Insert quantity of registes (Type hint: integer)
    slave_id = 2 #Insert slave_id (Type hint: integer)
    name = "weather"

    weather_station = ReadDevice(serial_settings, function, address, quantity, slave_id, name)

    datos = await weather_station.mostrar_atributos()

    
    print(datos)  # Imprimimos los datos obtenidos desde mostrar_atributos


# Ejecutar
if __name__ == "__main__":
    asyncio.run(main())