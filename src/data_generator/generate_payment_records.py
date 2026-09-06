import os
import glob
import json
import random
import uuid
import csv
from datetime import datetime, timedelta
import argparse

def generate_payments(volume_check, volume_target):
    # Locate all historical Loan JSON extracts, supporting both flat and date=YYYY-MM-DD structures)
    loan_files = sorted(glob.glob(f"{volume_check}/**/*.json", recursive=True))
    
    if not loan_files:
        print(f"CRITICAL: No loan extract files found in {volume_check}. Run the loan generator first!")
        return

    # Setup target date (yesterday) for the batch run
    yesterday = datetime.now() - timedelta(days=1)
    target_day = yesterday.day

    due_loans = []
    random_loans = []
    
    # Loop through EVERY historical loan file to find mature loans
    for file_path in loan_files:
        with open(file_path, "r") as f:
            for line in f:
                record = json.loads(line)
                
                orig_date_str = record.get("origination_date", yesterday.strftime("%Y-%m-%d"))
                try:
                    orig_date = datetime.strptime(orig_date_str, "%Y-%m-%d")
                except ValueError:
                    orig_date = yesterday

                loan_data = {
                    "loan_id": record["loan_id"],
                    "monthly_emi": record["loan_terms"]["monthly_emi"],
                    "due_day": orig_date.day,
                    "currency": record.get("currency", "PHP"),
                    "customer_location": record.get("customer_location", "Philippines")
                }

                loan_age_days = (yesterday - orig_date).days

                # Check if the loan is "due" based on the calendar day (+/- 3 days)
                diff = abs(target_day - loan_data["due_day"])
                is_due_day = (diff <= 3 or diff >= 27)

                if is_due_day and loan_age_days >= 25:
                    due_loans.append(loan_data)
                else:
                    random_loans.append(loan_data)

    # REALISTIC COMPLIANCE: 85-95% of mature loans will make their on-time payment
    num_due_payments = int(len(due_loans) * random.uniform(0.85, 0.95))
    sampled_due = random.sample(due_loans, min(num_due_payments, len(due_loans)))
    
    # 1-4% of everyone else makes early, off-cycle, or late catch-up payments
    num_random_payments = int(len(random_loans) * random.uniform(0.01, 0.04))
    sampled_random = random.sample(random_loans, min(num_random_payments, len(random_loans)))

    sampled_loans = sampled_due + sampled_random
    payments = []

    payment_methods = ["GCash", "Maya", "BDO_Online", "BPI_Express", "7_Eleven_OTC", "Stripe", "Adyen", "PayPal", "SWIFT_Wire"]
    
    for item in sampled_loans:
        emi = item["monthly_emi"]
        
        # 3. WEIGHTED FINANCIALS: 85% exact, 5% underpay, 5% slight overpay, 5% double pay
        multiplier = random.choices(
            population=[0.5, 1.0, 1.2, 2.0],
            weights=[0.05, 0.85, 0.05, 0.05],
            k=1
        )[0]
        
        paid_amount = round(emi * multiplier, 2)
        
        # 4. WEIGHTED STATUSES: 90% Success, 7% Failures, 3% Stuck Pending
        status = random.choices(
            population=["SETTLED", "FAILED", "PENDING"],
            weights=[0.90, 0.07, 0.03],
            k=1
        )[0]
        
        payment_time = yesterday.replace(
            hour=random.randint(6, 22),
            minute=random.randint(0, 59),
            second=random.randint(0, 59)
        )

        payments.append({
            "transaction_id": f"TXN-{uuid.uuid4().hex[:10].upper()}",
            "loan_reference_id": item["loan_id"],
            "amount": paid_amount,
            "currency": item["currency"],              
            "customer_location": item["customer_location"],  
            "payment_channel": random.choice(payment_methods),
            "status": status,
            "transaction_timestamp": payment_time.strftime("%Y-%m-%d %H:%M:%S")
        })

    current_datetime = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    output_path = f"{volume_target}/payments_{current_datetime}.csv"

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    fieldnames = ["transaction_id", "loan_reference_id", "amount", "currency", "customer_location", "payment_channel", "status", "transaction_timestamp"]
    
    with open(output_path, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(payments)

    print(f"INFO: Successfully generated {len(payments)} payment transactions at {output_path}")
    print(f"INFO: Breakdown - {len(sampled_due)} On-Time/Due, {len(sampled_random)} Off-Cycle/Outliers")

if __name__ == "__main__":
    # Setup argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", type=str, default="dev", help="Target catalog name")
    args, _ = parser.parse_known_args()

    # Declare variables
    volume_prereq = f"/Volumes/{args.catalog}/landing/loan_records"
    volume_destination = f"/Volumes/{args.catalog}/landing/payment_records"

    # Call function
    generate_payments(volume_prereq, volume_destination)