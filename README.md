# Este paquete busca realizar la instalacion previa para uso de proyecto de agentes para comunicacion continua

# Instalacion de paquetes de produccion
uv add name-librarie

# Instalacion de paquetes de desarrollo
uv add --dev test-librarie

# Crea las variables de entorno para la configuracion de variables de comunicacion con ollama
export $(grep -v '^#' .env | xargs)
