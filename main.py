# Import section
from asyncio import run as a_run

from src.services.eslabon import Eslabon
from src.models.additional_structure import EslabonStatus

# print(EslabonStatus.PENDING)
new_eslabon = Eslabon(
    name = "General Eslabon"
)
print(new_eslabon.state(include_prompt = False))

new_eslabon.assign_mcp(
    url = "https://mcp.api.coingecko.com/sse",
    type_connection = "sse",
    tool_prefix = "nira"
)

print(new_eslabon.state(include_prompt = False))

print(new_eslabon.__slots__)
