import math

class LoanProcessingSystem:
    def __init__(self, customer_id, age, monthly_salary, existing_loan_amount, credit_score, employment_type, requested_loan_amount, loan_tenure_months):
        if age < 18 or age > 65: raise ValueError("Invalid Age")
        if monthly_salary <= 0: raise ValueError("Invalid Salary")
        if credit_score < 300 or credit_score > 850: raise ValueError("Invalid Credit Score")
        if requested_loan_amount <= 0 or loan_tenure_months <= 0: raise ValueError("Invalid Loan Request")
        
        self.monthly_salary = monthly_salary
        self.existing_loan_amount = existing_loan_amount
        self.credit_score = credit_score
        self.employment_type = employment_type.upper()
        self.requested_loan_amount = requested_loan_amount
        self.loan_tenure_months = loan_tenure_months

    def process(self):
        dti = ((self.existing_loan_amount * 0.10) / self.monthly_salary) * 100
        rate = 8.5 + (4.0 if self.credit_score < 600 else 2.0 if self.credit_score < 700 else 0.5 if self.credit_score < 750 else 0.0)
        if self.employment_type == "UNSTABLE": rate += 1.5
        
        eligible = self.monthly_salary * (20.0 if self.credit_score >= 750 else 10.0)
        r = (rate / 100) / 12
        emi = (self.requested_loan_amount * r * math.pow(1+r, self.loan_tenure_months)) / (math.pow(1+r, self.loan_tenure_months) - 1)
        
        status = "APPROVED"
        if self.credit_score < 550: status = "REJECTED (Poor Credit Score)"
        elif dti > 50.0: status = "REJECTED (High DTI)"
        elif self.existing_loan_amount > (self.monthly_salary * 36): status = "REJECTED (Debt Limit Exceeded)"
        elif self.requested_loan_amount > eligible: status = "REJECTED (Exceeds Eligibility)"
        
        return {"dti": dti, "eligible": eligible, "rate": rate, "emi": emi, "status": status}
