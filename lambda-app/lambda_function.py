import requests
from bs4 import BeautifulSoup

import json
import re


def is_valid_div(element):
    return (
        element.name == "div"
        and element.get("class") == ["ds-box"]
        and all(
            tag.name == "br" and not tag.find_all() for tag in element.find_all("br")
        )
        and not any(tag for tag in element.find_all() if tag.name != "br")
    )


def lambda_handler(event, context):
    url = event["queryStringParameters"]["url"]
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    recipe = {
        "title": soup.find("h1", class_="").text.strip(),
        "ingredients": [],
        "instructions": [],
        "totaltime": "",
    }

    timestr = (
        soup.find("span", class_="recipe-preptime")
        .text.replace("\ue192", "")
        .replace("\n", "")
        .replace("Min.", "")
        .strip()
    )
    recipe["totaltime"] = 60 * int(timestr)

    ingredients_table = soup.find("table", class_="ingredients")
    if ingredients_table:
        rows = ingredients_table.find_all("tr")
        for row in rows:
            columns = row.find_all("td")
            if len(columns) == 2:
                ingredient_quantity = re.sub("\s+", " ", columns[0].text.strip())
                ingredient_name = columns[1].text.strip()
                recipe["ingredients"].append(f"{ingredient_quantity} {ingredient_name}")

    instruction_divs = soup.find_all(is_valid_div)

    # Parse the instruction divs
    for div in instruction_divs:
        text = div.get_text(separator=" ").strip()
        parts = text.split("\n")

        for part in parts:
            if part.strip() == "":
                continue
            recipe["instructions"].append(part.strip())

    # Scrape the website here
    data = recipe
    headers = {
        # "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
    }
    return {"statusCode": 200, "headers": headers, "body": json.dumps(data)}
