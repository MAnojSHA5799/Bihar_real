import pandas as pd
import random
from t6 import apply_prediction   # Import prediction logic
# =========================================================
# 1️⃣ PROJECT DATA
# =========================================================

projects = [
    {"Project Name": "A M PINNACLE",
     "Registration No": "BRERAP00427-9/155/R-1663/2024",
     "Promoter Name": "R.D.ECO DEVELOPERS PVT. LTD."},

    {"Project Name": "A ONE HERITAGE",
     "Registration No": "BRERAP00923-1/607/R-783/2019",
     "Promoter Name": "A ONE BUILDERS DEVELOPERS"},

    {"Project Name": "A.R GREEN CITY",
     "Registration No": "BRERAP14746-5/100/R-1767/2024",
     "Promoter Name": "PARI CONSTRUCTION AND DEVELOPER"}
]

# =========================================================
# 2️⃣ CUSTOMER COMMENTS
# =========================================================

comments_pool = list(set([

# Positive
"Good reputation as a builder.",
"Flat location is very good with amenities.",
"Professional and attentive team.",
"Value for money project.",
"Completed on time and within budget.",
"Eco-friendly development approach.",
"High-quality materials used.",
"Supportive staff and good communication.",
"Outstanding craftsmanship.",
"Workmanship impeccable.",

# Negative
"Project not completed on time.",
"Lot of work pending.",
"No clarity in agreement.",
"Advance refund not returned.",
"Extra money charged for parking.",
"Worst build quality.",
"Damp walls and no waterproof roof.",
"No response after taking money.",
"Construction lapses reported.",
"Work incomplete even after payment."
]))

# =========================================================
# 3️⃣ KEYWORDS
# =========================================================

positive_keywords = ["good","professional","value","eco","quality",
                     "supportive","outstanding","impeccable","completed"]

negative_keywords = ["not","pending","no","worst","refund",
                     "extra","damp","lapses","incomplete"]

financial_keywords = ["refund","extra","money"]
delay_keywords = ["not completed","pending","incomplete"]
quality_keywords = ["quality","craftsmanship","damp","worst"]

# =========================================================
# 4️⃣ SENTIMENT FUNCTION
# =========================================================

def analyze_sentiment(text):
    text = text.lower()
    score = 0
    
    for word in positive_keywords:
        if word in text:
            score += 1
            
    for word in negative_keywords:
        if word in text:
            score -= 1

    if score > 0:
        return score, "Positive"
    elif score < 0:
        return score, "Negative"
    else:
        return score, "Neutral"

# =========================================================
# 5️⃣ GENERATE DATASET
# =========================================================

records = []

for project in projects:
    selected_comments = random.sample(comments_pool, 8)
    
    for comment in selected_comments:
        score, label = analyze_sentiment(comment)
        
        records.append({
            "Project Name": project["Project Name"],
            "Promoter Name": project["Promoter Name"],
            "Comment": comment,
            "Sentiment Score": score,
            "Sentiment Label": label
        })

df = pd.DataFrame(records)

# =========================================================
# 6️⃣ RISK FLAGS
# =========================================================

df["Financial Issue"] = df["Comment"].apply(
    lambda x: 1 if any(k in x.lower() for k in financial_keywords) else 0)

df["Delay Issue"] = df["Comment"].apply(
    lambda x: 1 if any(k in x.lower() for k in delay_keywords) else 0)

df["Quality Issue"] = df["Comment"].apply(
    lambda x: 1 if any(k in x.lower() for k in quality_keywords) else 0)

# =========================================================
# 7️⃣ PROMOTER SUMMARY
# =========================================================

summary = df.groupby("Promoter Name").agg({
    "Sentiment Score":"mean",
    "Financial Issue":"sum",
    "Delay Issue":"sum",
    "Quality Issue":"sum"
}).reset_index()

summary["Trust Score (0-100)"] = (
    (summary["Sentiment Score"] * 25)
    - (summary["Financial Issue"] * 5)
    - (summary["Delay Issue"] * 5)
    - (summary["Quality Issue"] * 5)
)

summary["Risk Score"] = (
    summary["Financial Issue"]
    + summary["Delay Issue"]
    + summary["Quality Issue"]
)

summary["Sales Probability (%)"] = 100 - (summary["Risk Score"] * 5)

# =========================================================
# 8️⃣ ELABORATED THEORETICAL REPORT
# =========================================================

theoretical_report = """
================ THEORETICAL BASIS OF REAL ESTATE SALES PERFORMANCE ================

1️⃣ TRUST-BASED PURCHASE FRAMEWORK

• Real estate ek capital-intensive aur long-term commitment hota hai, jisme buyer apni lifetime savings ya long-term loan invest karta hai.

• Decision-making process highly risk-sensitive hota hai. Buyers agreement terms, possession timeline, construction progress aur financial transparency ko closely evaluate karte hain.

• Jab agreement clarity, payment schedule transparency aur communication consistency maintained hoti hai, tab trust ecosystem strong hota hai.

• Refund disputes, ambiguous clauses, delayed responses ya incomplete information directly perceived risk ko increase karte hain.

• High perceived risk purchase intention ko weaken karta hai aur conversion cycle ko slow kar deta hai.

• Trust erosion market reputation ko impact karta hai, especially digital reviews aur word-of-mouth channels ke through.

• Consistent transparency, regulatory compliance aur structured customer communication sustainable sales performance ka foundation create karte hain.


2️⃣ FINANCIAL RISK & BUYER BEHAVIOURAL RESPONSE

• Real estate demand ka significant segment loan-dependent middle-income buyers ka hota hai.

• Project delay hone par EMI + rent ka parallel financial burden buyer cash-flow pressure create karta hai.

• Unplanned escalation cost, hidden charges ya additional demand notices buyer ke financial confidence ko disturb karte hain.

• Behavioural finance principles ke according, buyers financial loss ko potential gain se zyada psychologically weightage dete hain.

• Even minor financial uncertainty bhi decision postponement ya project switching behaviour trigger kar sakti hai.

• Clearly defined pricing structure aur zero-hidden-cost policy buyer confidence aur booking stability ko strengthen karti hai.


3️⃣ SERVICE QUALITY & EXECUTION IMPACT (SERVQUAL DIMENSIONS)

• Reliability directly on-time project delivery se linked hai. Schedule deviation credibility ko damage karta hai.

• Responsiveness customer interaction quality ko define karta hai. Slow grievance handling dissatisfaction escalate karta hai.

• Assurance legal compliance, documentation accuracy aur regulatory alignment ko represent karta hai.

• Tangibles physical construction quality, finishing standards, waterproofing aur material durability ko reflect karta hai.

• Empathy after-sales service, maintenance response aur long-term customer engagement ko define karta hai.

• In dimensions me weakness overall service perception ko weaken karti hai, jo repeat referrals aur new bookings par direct impact daalti hai.


4️⃣ OPERATIONAL FACTORS CONTRIBUTING TO SALES DECLINE

• Timeline deviation buyer trust ko weaken karta hai.

• Incomplete construction ya structural defects future maintenance concerns raise karte hain.

• Refund-related conflicts brand credibility ko directly damage karte hain.

• Hidden charges transparency gap create karte hain, jisse negative sentiment accelerate hota hai.

• Damp walls, leakage aur quality lapses durability perception ko reduce karte hain.

• Negative online sentiment compounding effect create karta hai jo lead conversion rate ko gradually reduce karta hai.

• Operational inefficiencies long-term revenue sustainability ko impact karti hain.


5️⃣ STRATEGIC DRIVERS OF SALES ACCELERATION

• Competitive aur justified pricing demand stimulation ka primary driver hai.

• Professional sales team behaviour aur structured communication buyer assurance increase karta hai.

• Eco-conscious branding modern urban buyers ke preference ko align karta hai.

• Superior construction quality brand differentiation create karti hai.

• Strategic location advantage long-term appreciation potential ko enhance karta hai.

• Positive customer experience organic referrals aur low-cost marketing advantage generate karta hai.

• Strong post-possession service repeat investment probability ko improve karta hai.


6️⃣ INTEGRATED TRUST–RISK SALES MODEL

• Sales performance fundamentally trust accumulation aur risk mitigation ke balance par depend karti hai.

• Trust Score customer sentiment, service consistency aur financial transparency ko reflect karta hai.

• Risk Score delay issues, financial disputes aur quality complaints ka cumulative impact measure karta hai.

• High Trust + Controlled Risk → Strong Conversion & Sustainable Growth.

• Low Trust + Elevated Risk → Booking Slowdown & Revenue Volatility.

• Strategic management priority honi chahiye:
  - Transparent documentation
  - Strict project monitoring
  - Proactive communication
  - Quality assurance controls

• Long-term brand reputation compounding competitive advantage create karti hai jo future sales pipeline ko stabilize karti hai.

====================================================================================
"""

# =========================================================
# 9️⃣ SAVE FILES
# =========================================================

df.to_csv("final_review_data.csv", index=False)
summary.to_csv("final_promoter_summary.csv", index=False)

with open("detailed_theoretical_sales_report.txt", "w", encoding="utf-8") as file:
    file.write(theoretical_report)
    
    
    # =========================================================
# 🔥 APPLY PREDICTION FROM T6
# =========================================================
summary = apply_prediction(summary)


# =========================================================
# 🔟 PRINT OUTPUT
# =========================================================

print("\n========== REVIEW DATA ==========\n")
print(df)

print("\n========== PROMOTER SUMMARY ==========\n")
print(summary)
print("\n========== PROMOTER SUMMARY WITH PREDICTION ==========\n")
print(summary[["Predicted Sales Category", "Performance Trend"]])

print("\n========== ELABORATED THEORETICAL REPORT ==========\n")
print(theoretical_report)

print("\n✅ All files generated successfully.")