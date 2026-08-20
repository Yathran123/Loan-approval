import math

class LoanProcessingSystem:
    def __init__(self, customer_id: str, age: int, monthly_salary: float, 
                 existing_loan_amount: float, credit_score: int, 
                 employment_type: str, requested_loan_amount: float, 
                 loan_tenure_months: int):
        # Initializing read-only fields
        self._customer_id = customer_id
        self._age = age
        self._monthly_salary = monthly_salary
        self._existing_loan_amount = existing_loan_amount
        self._credit_score = credit_score
        self._employment_type = employment_type
        self._requested_loan_amount = requested_loan_amount
        self._loan_tenure_months = loan_tenure_months

        # Calculated internal states (initialized to defaults)
        self._debt_to_income_ratio = 0.0
        self._eligible_loan_amount = 0.0
        self._interest_rate = 0.0
        self._emi = 0.0
        self._approval_status = "UNPROCESSED"

    def process_loan(self):
        # 1. Validation & Exception Handling (Mirrors Java's IllegalArgumentException)
        if self._age < 18 or self._age > 65:
            raise ValueError("Invalid Age: Customer age must be between 18 and 65.")
        if self._monthly_salary <= 0:
            raise ValueError("Invalid Salary: Monthly salary must be greater than zero.")
        if self._credit_score < 300 or self._credit_score > 850:
            raise ValueError("Invalid Credit Score: Score must be between 300 and 850.")
        if self._requested_loan_amount <= 0 or self._loan_tenure_months <= 0:
            raise ValueError("Invalid Loan Request: Amount and tenure must be positive values.")

        # 2. Risk Metrics and Calculations
        # Estimate existing monthly commitment (10% of total balance as monthly debt)
        estimated_existing_emi = self._existing_loan_amount * 0.10
        self._debt_to_income_ratio = (estimated_existing_emi / self._monthly_salary) * 100

        # Interest calculation based on Credit Score and Employment Type
        base_rate = 8.5
        if self._credit_score < 600:
            base_rate += 4.0
        elif self._credit_score < 700:
            base_rate += 2.0
        elif self._credit_score < 750:
            base_rate += 0.5

        if self._employment_type.upper() == "UNSTABLE":
            base_rate += 1.5
        self._interest_rate = base_rate

        # Determine Maximum Eligible Loan based on Salary multiplier
        multiplier = 10.0
        if self._credit_score >= 750:
            multiplier = 20.0
        self._eligible_loan_amount = self._monthly_salary * multiplier

        # Standard Amortization Formula for Monthly EMI (Fixed multi-line syntax)
        monthly_rate = (self._interest_rate / 100) / 12
        compound_factor = math.pow(1 + monthly_rate, self._loan_tenure_months)
        self._emi = (self._requested_loan_amount * monthly_rate * compound_factor) / (compound_factor - 1)

        # 3. Decision Framework Rules Evaluation
        if self._credit_score < 550:
            self._approval_status = "REJECTED (Poor Credit Score)"
        elif self._debt_to_income_ratio > 50.0:
            self._approval_status = "REJECTED (High Debt-To-Income Ratio)"
        elif self._existing_loan_amount > (self._monthly_salary * 36):
            self._approval_status = "REJECTED (Existing Loans Exceed Safe Income Threshold)"
        elif self._requested_loan_amount > self._eligible_loan_amount:
            self._approval_status = "REJECTED (Requested Amount Exceeds Eligibility Cap)"
        else:
            self._approval_status = "APPROVED"

    # camelCase Getter Methods matching the exact names used by your QA layer
    def get_customer_id(self): return self._customer_id
    def get_approval_status(self): return self._approval_status
    def get_debt_to_income_ratio(self): return self._debt_to_income_ratio
    def get_eligible_loan_amount(self): return self._eligible_loan_amount
    def get_emi(self): return self._emi
    def get_interest_rate(self): return self._interest_rate
