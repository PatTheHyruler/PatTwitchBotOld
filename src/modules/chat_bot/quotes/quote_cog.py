from twitchio.ext import commands

from src.base_twitch_cog import BaseTwitchCog
from .services import ServiceUnitOfWork
from .storage.model.quote import Quote


class QuoteCog(BaseTwitchCog[ServiceUnitOfWork]):
    @commands.group(name="quote")
    async def quote(self, ctx: commands.Context, quote_id: int = None):
        if quote_id is not None:
            quote = await self._service_uow.quotes.get_by_id(quote_id)
            if quote is None:
                await ctx.reply(f"Couldn't find Quote with id #{quote_id}")
                await self._service_uow.close()
                return
        else:
            quote = await self._service_uow.quotes.get_random_quote()
            if quote is None:
                await ctx.reply(f"Sorry, couldn't find any quotes!")
                await self._service_uow.close()
                return

        await ctx.reply(f"{quote}")
        await self._service_uow.close()

    @quote.command(name="add")
    async def quote_add(self, ctx: commands.Context, *quote_text):
        if not await self.verify_mod(ctx):
            return
        quote = await self._service_uow.quotes.add(Quote(" ".join(quote_text), ctx.author.name, ctx.message.timestamp))
        await self._service_uow.save_changes()
        await self._service_uow.refresh(quote)
        await ctx.reply(f"Successfully added quote #{quote.id}!")
        await self._service_uow.close()

    @quote.command(name="remove")
    async def quote_remove(self, ctx: commands.Context, quote_id: int):
        if not await self.verify_mod(ctx):
            return
        quote = await self._service_uow.quotes.remove_by_id(quote_id)
        await self._service_uow.save_changes()
        if quote is not None:
            await ctx.reply(f"Successfully removed {quote}")
        else:
            await ctx.reply(f"No Quote found with id #{quote_id}")
        await self._service_uow.close()
