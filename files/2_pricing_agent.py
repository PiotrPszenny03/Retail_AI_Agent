import os
import json
import pandas as pd
from dotenv import load_dotenv
import google.generativeai as genai

def run_pricing_agent():
    # 1. Load API key
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: No API key found. Make sure you have a .env file in this folder!")
        return

    genai.configure(api_key=api_key)

    # Use special configuration that forces the model to return pure JSON (Pro Tip!)
    model = genai.GenerativeModel(
        'gemini-2.5-flash',
        generation_config={"response_mime_type": "application/json"}
    )

    print("Loading problematic products...")
    df = pd.read_csv('problematic_products.csv')

    # To avoid overloading the model, take the 5 most problematic products
    # (those with the longest storage or lowest margin)
    top_problems = df.sort_values(by='margin_percentage').head(5)

    # Prepare data for the prompt in a readable format
    products_text = ""
    for _, row in top_problems.iterrows():
        products_text += (
            f"ID: {row['product_id']} | Category: {row['category']} | "
            f"In stock: {row['stock_level']} pcs | Days in inventory: {row['days_in_inventory']} | "
            f"Current margin: {row['margin_percentage']}% | Price elasticity: {row['elasticity']}\n"
        )

    print("Data prepared. LLM analysis in progress...\n")

    # 2. Create the Prompt for the Agent
    prompt = f"""
    You are the Chief Pricing Optimization Analyst (Pricing Manager) at a large e‑commerce company.
    Below is a list of the 5 most problematic products that are sitting in the warehouse and generating costs:

    {products_text}

    Business rules:
    1. Price elasticity < -1.5: The product is very price sensitive. A small discount (e.g., 10–15%) should strongly boost sales.
    2. Price elasticity > -1.0: The product is not very price sensitive. A simple discount won't help much; better to use a cross‑sell action (e.g., buy together with another product) or a deep clearance sale (–30%).
    3. If Days in inventory > 120, the priority is to liquidate the item, even at the cost of reducing margin to 5%.

    Propose a specific action for each product.
    YOU MUST RETURN THE RESULT AS A PURE JSON FILE (a list of objects) according to the schema below.

    Required keys in the JSON for each product:
    - "product_id": (string) product ID
    - "suggested_action": (string) "Discount", "Cross-sell", or "Clearance"
    - "discount_percentage": (integer) e.g., 15, 20, 30 (0 if no discount)
    - "justification": (string) One‑sentence business justification for the decision based on elasticity and days in inventory.
    """

    # 3. Send the request to the API
    response = model.generate_content(prompt)

    # The response is already in JSON text format thanks to 'response_mime_type'
    json_output = response.text

    print("Agent has made decisions! Saving to JSON file...")

    # Save the result so the e‑commerce system can read it
    with open('pricing_actions.json', 'w', encoding='utf-8') as f:
        f.write(json_output)

    print("\nDone! File 'pricing_actions.json' has been created.")

    # Display a preview in the terminal (nicely formatted)
    parsed_json = json.loads(json_output)
    print("\nPreview of generated actions:")
    print(json.dumps(parsed_json, indent=4, ensure_ascii=False))

if __name__ == "__main__":
    run_pricing_agent()