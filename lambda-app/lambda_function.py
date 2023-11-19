import json

from CookidooClient import CookiputRecipeCreator
from ChefkochRecipeScraper import ChefkochRecipeScraper


def lambda_handler(event, context):
    url = event["queryStringParameters"]["url"]
    jwt = event["queryStringParameters"]["jwt"]

    headers = {
        # "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
    }

    scraper = ChefkochRecipeScraper()

    # Get Recipe
    print(f"Downloading recipe from {url}")
    try:
        recipe = scraper.scrape_recipe(url)

    except Exception as e:
        print(f"Error: {str(e)}")

    recipe_creator = CookiputRecipeCreator(jwt)

    # Step 1: Create a new recipe
    recipe_id = recipe_creator.create_recipe(recipe["title"])

    if recipe_id is None:
        return {
            "statusCode": 503,
            "headers": headers,
            "body": "Error creating recipe. Please check your token.",
        }

    # Step 2: Add ingredients
    ingredients = []
    for ingredient in recipe["ingredients"]:
        ingredients.append({"type": "INGREDIENT", "text": ingredient})
    recipe_creator.add_ingredients(recipe_id, ingredients)

    # Step 3: Add cooking steps
    steps = []
    for step in recipe["instructions"]:
        steps.append({"type": "STEP", "text": step})
    recipe_creator.add_steps(recipe_id, steps)

    # Step 4: Add tools, time, and yield information
    tools = ["TM6"]
    total_time = recipe["totaltime"]
    yield_value = 1
    yield_unit = "portion"
    recipe_creator.add_tools_and_time(
        recipe_id, tools, total_time, total_time, yield_value, yield_unit
    )

    data = recipe
    return {"statusCode": 200, "headers": headers, "body": json.dumps(data)}
