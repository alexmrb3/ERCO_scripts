import asyncio
import pymodbus.client, pymodbus.framer, pymodbus.exceptions, pymodbus.pdu
import struct

async def start_connection(
    port: str,
    baudrate: int,
    bytesize: int,
    parity: str,
    stopbits: int,
    framer=pymodbus.framer.ModbusRtuFramer,
) -> pymodbus.client:
    try:
        client = pymodbus.client.AsyncModbusSerialClient(
            port,
            framer=framer,
            timeout=1,
            retries=3,
            baudrate=baudrate,
            bytesize=bytesize,
            parity=parity,
            stopbits=stopbits,
        )

        #print("Connecting to slave")
        await client.connect()

        if client.connected:
            #print("Connected successfully")
            return client
        else:
            print("Failed to connect to the Modbus server")
            return None
    except Exception as e:
        print(f"Exception in start_connection: {e}")
        return None

def transformar_valores( registros, name) -> None:
    if name == "weather":
        variables = ["irradiance", "Temperature"]
    elif name == "huawei":
        variables = ["Generation_Accum", "Power_Factor"]
    elif name == "pac3200":
        variables = ["Reactive_Energy", "Active Energy", "Apparent_Energy", "Power_factor"]
        
        
    
    valores = []
    aux = 0
    try:
        if registros is not None:
            for i in range(0,len(registros),2):
                numero_entero = (registros[i] << 16) | registros[i+1] #Unimos los dos números de 16 bits en uno de 32
                numero_completo =  struct.unpack('>f', struct.pack('>I', numero_entero))[0] #Mediante struct convertimos el número a binario y luego a flotante
                valores.append(numero_completo)
                #print(f"registro de {variables[aux]}: {numero_completo}")
                aux = aux + 1

            valores_obtenidos = {}
            for nombre, valor in zip(variables, valores):
                valores_obtenidos[nombre] = valor

        return valores_obtenidos

    except Exception as e:
        print(f"Ha ocurrido una excepción al unir los números: {e}")
        return None

def close_connection(client: pymodbus.client) -> None:
    try:
        if client is not None:
            #print("Closing connection")
            client.close()
    except Exception as e:
        print(f"Exception in close_connection: {e}")


async def run_async_simple_client(
    port: str,
    function_code: int,
    address_register: int,
    amount_registers: int,
    slave: int,

) -> list:

#    client = await start_connection(port=port)
    client = await start_connection(
        port=port,
        baudrate=9600,
        bytesize=8,
        parity="E",
        stopbits=1
    )
    if client is None:
        return

    #print("Getting data")

    try:
        
        if function_code == 3:
            rr = await client.read_holding_registers(
                address=address_register, count=amount_registers, slave=slave
            )

        else:
            rr = await client.read_input_registers(
                address=address_register, count=amount_registers, slave=slave
            )

        if rr.isError():
            print(f"Exception reading registers: {rr}")
            return None
        if isinstance(rr, pymodbus.pdu.ExceptionResponse):
            print(f"Exception in instance of Modbus library: {rr}")
            return None


        return rr.registers if rr else None
    except pymodbus.exceptions.ModbusException as e:
        print(f"Modbus library exception: {e}")
        return None
    finally:
        close_connection(client=client)


class ReadDevice:
    # Constructor: Método especial para inicializar un objeto
    def __init__(self, serial_settings, function, address, quantity, slave_id, name):  #,baudrate, bytesize, parity, stopbits):
#        self.baudrate = baudrate, #Insert baudrate (Type hint: integer)
 #       self.bytesize = bytesize, #Insert bytesize (Type hint: integer)
  #      self.parity = parity, #Insert parity (Type hint: string)
   #     self.stopbits = stopbits, #Insert stopbits (Type hint: integer)

        self.serial_settings = serial_settings # "COM2" #Insert COM# port (Type hint: string)
        self.function = function # 4 #Insert function (Type hint: integer)
        self.address = address # 40035 #Insert initial address (Type hint: integer)
        self.quantity = quantity # 4 #Insert quantity of registes (Type hint: integer)
        self.slave_id = slave_id #2 #Insert slave_id (Type hint: integer)
        self.name = name 



    async def mostrar_atributos(self):
        try: 
            read_registers = await run_async_simple_client(
                port = self.serial_settings,
                function_code = self.function,
                address_register = self.address,
                amount_registers = self.quantity,
                slave = self.slave_id,
            )

            if read_registers is not None:
                #print(f"Registers: {read_registers}")

                datos_nombrados = transformar_valores( read_registers, self.name)

            else:
                print("Failed to read registers")
        except Exception as e:
            print(f"Exception in main: {e}")
            print(f"Atributo 1: {self.atributo1}, Atributo 2: {self.atributo2}")
        
        return datos_nombrados # read_registers




