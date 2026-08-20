import math

class LoanProcessingSystem:
    def process_loan(self, request: dict) -> dict:
        if request is None:
            raise ValueError("Loan request cannot be null")
            
        self._validate_inputs(request)
        
        response = {
            "debt_to_income_ratio": 0.0,
            "eligible_loan_amount": 0.0,
            "interest_rate": 0.0,
            "emi": 0.0,
            "is_approved": False,
            "rejection_reason": ""
        }

        # 1. Calculate Debt-to-Income (DTI) Ratio
        # Assuming a standard monthly commitment calculation (2% of existing liability)
        estimated_existing_monthly_commitment = request["existing_loan_amount"] * 0.02
        if request["monthly_salary"] > 0:
            response["debt_to_income_ratio"] = (estimated_existing_monthly_commitment / request["monthly_salary"]) * 100
        else:
            response["debt_to_income_ratio"] = 100.0

        # 2. Determine base eligibility and interest rates based on Credit Score & Employment
        if request["credit_score"] < 600:
            response["is_approved"] = False
            response["rejection_reason"] = "Poor credit score"
            return response
        elif request["credit_score"] < 700:
            response["interest_rate"] = 12.5
        else:
            response["interest_rate"] = 8.5

        # Employment type checks
        emp_type = str(request["employment_type"]).upper()
        if emp_type == "UNEMPLOYED":
            response["is_approved"] = False
            response["rejection_reason"] = "Unemployed status ineligible"
            return response
        elif emp_type == "SELF_EMPLOYED":
            response["interest_rate"] += 1.0  # Risk premium

        # 3. Evaluate Threshold Rules (Age, Maximum Liabilities, and DTI caps)
        if request["age"] < 18 or request["age"] > 65:
            response["is_approved"] = False
            response["rejection_reason"] = "Age out of bounds"
            return response

        if request["existing_loan_amount"] > (request["monthly_salary"] * 36):
            response["is_approved"] = False
            response["rejection_reason"] = "Existing loan exceeds permissible multiplier threshold"
            return response

        if response["debt_to_income_ratio"] > 50.0:
            response["is_approved"] = False
            response["rejection_reason"] = "High debt-to-income ratio"
            return response

        # 4. Calculate Maximum Loan Eligibility Matrix
        max_eligible_amount = request["monthly_salary"] * 12
        response["eligible_loan_amount"] = min(max_eligible_amount, request["requested_loan_amount"])

        # 5. Calculate Equated Monthly Installment (EMI)
        # Formula: EMI = [P x R x (1+R)^N] / [((1+R)^N)-1]
        monthly_rate = (response["interest_rate"] / 12) / 100
        months = request["loan_tenure_months"]
        
        if months > 0 and monthly_rate > 0:
            p = response["eligible_loan_amount"]
            response["emi"] = (p * monthly_rate * math.pow(1 + monthly_rate, months)) / (math.pow(1 + monthly_rate, months) - 1)
        elif months > 0:
            response["emi"] = response["eligible_loan_amount"] / months

        response["is_approved"] = True
        return response

    def _validate_inputs(self, r: dict):
        required_keys = ["customer_id", "age", "monthly_salary", "existing_loan_amount", 
                         "credit_score", "employment_type", "requested_loan_amount", "loan_tenure_months"]
        
        for key in required_keys:
            if key not in r:
                raise ValueError(f"Missing required input parameter: {key}")

        if not r["customer_id"] or str(r["customer_id"]).strip() == "":
            raise ValueError("Invalid Customer ID")
        if r["monthly_salary"] < 0 or r["existing_loan_amount"] < 0 or r["requested_loan_amount"] < 0:
            raise ValueError("Financial values cannot be negative")
        if r["credit_score"] < 300 or r["credit_score"] > 850:
            raise ValueError("Credit score must be between 300 and 850")
        if r["loan_tenure_months"] <= 0:
            raise ValueError("Loan tenure must be greater than zero")
