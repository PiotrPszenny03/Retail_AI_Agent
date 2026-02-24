# Dynamic Pricing & Inventory AI Agent

## 🎯 Business Context
In e-commerce and retail, "dead stock" (inventory that doesn't sell) ties up capital and destroys profit margins through continuous warehousing costs. Traditional dynamic pricing relies on rigid rules, while manual review is unscalable. 

This project demonstrates a modern **AI-driven Pricing Pipeline** that identifies margin-burning products and autonomously generates actionable pricing strategies using a Large Language Model (LLM) integrated via API.

## 🧠 Architecture & Tech Stack

* **Data Processing:** `Python`, `pandas`, `numpy`
* **AI & Decision Engine:** `google-generativeai` (Gemini 2.5 Flash API)
* **Output Format:** `JSON` (Structured Output for seamless ERP/E-commerce backend integration)
* **Concept Focus:** Dynamic Pricing, Price Elasticity, Profit Margin Optimization, Cross-selling, Retail Analytics.

## ⚙️ How the Pipeline Works

1. **Inventory Simulation & Analytics (`1_inventory_analysis.py`):**
   * Simulates a retail database (SKUs, unit costs, stock levels, days in inventory, price elasticity).
   * Calculates actual holding costs (e.g., 0.05 PLN/day) and computes the **True Gross Margin**.
   * Filters out "problematic" products (e.g., in stock for > 90 days or margin < 20%).

2. **AI Pricing Agent (`2_pricing_agent.py`):**
   * Acts as an AI Pricing Manager.
   * Feeds the problematic inventory data and strict business logic (elasticity rules, clearance thresholds) into the LLM.
   * **Crucial Feature:** Uses `response_mime_type="application/json"` to force the AI to return a clean, machine-readable JSON array instead of raw text.

## 📊 Example Output (Machine-Readable JSON)
*The AI evaluates the data and returns a payload ready to be ingested by a pricing engine (e.g., Shopify, Magento, SAP):*

```json
[
    {
        "product_id": "SKU-1003",
        "suggested_action": "Discount",
        "discount_percentage": 15,
        "justification": "Very high price elasticity (-1.85) combined with long inventory duration (151 days) requires a direct discount for rapid liquidation."
    }
]
