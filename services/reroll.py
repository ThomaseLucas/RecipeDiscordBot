import discord
from services.calendar_service import CalendarService

class RerollButtonView(discord.ui.Button):
    def __init__(self, recipe_id, group, recipe_title, changing_recipes, index):
        self.recipe_title = recipe_title
        super().__init__(label=f'Reroll - {self.recipe_title}', style=discord.ButtonStyle.primary)
        self.recipe_id = recipe_id  
        self.group = group
        self.index = index
        self.mealplanner = CalendarService()
        self.changing_recipes = changing_recipes
        
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        print('button clicked!')

        message_id = interaction.message.id
        try:
            while True:
                new_recipe = self.mealplanner.reroll_recipe(self.recipe_id, self.group)
                if new_recipe['title'] in [r['title'] for r in self.changing_recipes.values()]:
                    print('\n\nThis recipe is in the meal plan already!\n\n')
                    continue
                else:
                    self.changing_recipes[self.index] = new_recipe
                    # print(self.changing_recipes)
                    print('\n\nnew recipe found!\n\n')
                    break

            # new_recipe = self.mealplanner.reroll_recipe(self.recipe_id, self.group)
            
            embed = discord.Embed(
                        title=new_recipe['title'],
                        description=new_recipe['description'],
                        color=discord.Color.green()
                    )
            embed.set_image(url=new_recipe['image'])

            self.label = f'Reroll - {new_recipe['title']}'
        except Exception as e:
            print(f'could not find new recipe: {e}')
        
        await interaction.message.edit(embed=embed, view=self.view)

        
        # await interaction.response.send_message(
        #     f'Group {self.group} was just rerolled.'
        # )

    