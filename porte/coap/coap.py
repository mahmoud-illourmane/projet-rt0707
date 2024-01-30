import asyncio
from aiocoap import *

class FlagResource(resource.Resource):
    async def render_get(self, request):
        # Affiche le payload reçu
        print("Flag reçu:", request.payload.decode('utf8'))
        return Message(code=CHANGED)  # Réponse facultative pour indiquer que la requête a été traitée

async def main():
    root = resource.Site()
    root.add_resource(['flag'], FlagResource())
    await Context.create_server_context(root)
    print("Serveur CoAP démarré.")

if __name__ == "__main__":
    asyncio.run(main())
