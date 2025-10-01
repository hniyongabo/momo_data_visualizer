# Momo Data Visualizer
This is an enterprise-level fullstack application that processes MoMo SMS data in XML format, cleans and categorizes the data and stores it in a relational database. 
It has a user-friendly interface for analyzing and visualizing the processed data as well as uploading raw xml data.

## Setup Instructions

1. **Install Python**: Ensure Python 3.10 or newer is available (`python3 --version`).
2. **Create a virtual environment** (recommended):
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. **Install dependencies**: The current tooling relies only on the standard library. If new packages are added, pin them in `requirements.txt` and install with `pip install -r requirements.txt`.
4. **Parse the SMS backup** to JSON:
   ```bash
   python3 dsa/parse_sms.py
   ```
   - Reads `data/modified_sms_v2.xml` by default.
   - Writes structured output to `data/parsed_sms.json` (override with `-o <path>`).
5. **Benchmark search strategies** (optional):
   ```bash
   python3 dsa/search_efficiency.py -n 50 -i 2000
   ```
   - Uses `data/parsed_sms.json` as the default dataset.
6. **Run the prototype API server** (if desired):
   ```bash
   python3 dsa/server.py
   ```
   - Exposes simple CRUD endpoints at `http://localhost:8000/transactions` for experimentation.

## Architecture Diagram
![Image](https://github.com/user-attachments/assets/41ecdc4d-067e-4c19-9790-126cf353f0e4)

## Database Documentation

The system uses a relational schema designed for accuracy, scalability, and auditability:

- *USER*: Stores phone numbers, balances, and user type (personal, merchant, agent).  
- *MESSAGE*: Holds raw SMS content linked to a user.  
- *TRANSACTION*: Parsed transaction details (amount, status, timestamps) linked back to messages.  
- *CATEGORY*: Defines transaction types and whether they are debit/credit.  
- *TRANSACTION_CATEGORY*: Many-to-many relationship mapping transactions to categories.  
- *SYSTEM_LOGS*: Records system and parsing events for traceability.  

*Key rules:*  
- Phone numbers and transaction IDs must be unique.  
- Amounts must be positive, and balances cannot drop below zero.  
- Referential integrity is enforced with foreign keys.  

*Example query:*  
```sql
SELECT u.phone_number, SUM(t.amount) AS total_spent
FROM user u
JOIN message m ON u.user_id = m.user_id
JOIN transaction t ON m.sms_id = t.message_id
JOIN transaction_category tc ON t.transaction_id = tc.transaction_id
JOIN category c ON tc.category_id = c.id
WHERE c.payment_type = 'DEBIT'
GROUP BY u.phone_number;
```

## Scrum Board
[Github Issues/Projects](https://github.com/users/hniyongabo/projects/2)

## Members 
- [Habeeb Dindi](https://github.com/dindihabeeb)
- [Harmony Naomi Niyongabo](https://github.com/hniyongabo)
- [Kethia Kayigire](https://github.com/kethia19)
