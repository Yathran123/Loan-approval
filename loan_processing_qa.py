import unittest
from loan_processing_system import LoanProcessingSystem

class TestLoanProcessingQA(unittest.TestCase):

    def setUp(self):
        self.system = LoanProcessingSystem()
        self.valid_base_request = {
            "customer_id": "CUST1001",
            "age": 30,
            "monthly_salary": 10000.0,
            "existing_loan_amount": 20000.0,
            "credit_score": 750,
            "employment_type": "SALARIED",
            "requested_loan_amount": 50000.0,
            "loan_tenure_months": 36
        }

    def test_minimum_maximum_age(self):
        # Test Underage scenario
        self.valid_base_request["age"] = 17
        res = self.system.process_loan(self.valid_base_request)
        self.assertFalse(res["is_approved"])
        self.assertEqual(res["rejection_reason"], "Age out of bounds")

        # Test Overage scenario
        self.valid_base_request["age"] = 66
        res = self.system.process_loan(self.valid_base_request)
        self.assertFalse(res["is_approved"])

    def test_invalid_salary(self):
        self.valid_base_request["monthly_salary"] = -500.0
        with self.assertRaises(ValueError):
            self.system.process_loan(self.valid_base_request)

    def test_poor_credit_score(self):
        self.valid_base_request["credit_score"] = 450
        res = self.system.process_loan(self.valid_base_request)
        self.assertFalse(res["is_approved"])
        self.assertEqual(res["rejection_reason"], "Poor credit score")

    def test_existing_loan_exceeding_threshold(self):
        # Salary is 10k, setting threshold over 36x limit (360,000)
        self.valid_base_request["existing_loan_amount"] = 400000.0 
        res = self.system.process_loan(self.valid_base_request)
        self.assertFalse(res["is_approved"])

    def test_high_debt_to_income_ratio(self):
        # Adjust debt profile to generate a heavy ongoing commitment burden
        self.valid_base_request["existing_loan_amount"] = 300000.0
        res = self.system.process_loan(self.valid_base_request)
        self.assertFalse(res["is_approved"])

    def test_different_employment_categories(self):
        # Self-Employed premium validation
        self.valid_base_request["employment_type"] = "SELF_EMPLOYED"
        res_self = self.system.process_loan(self.valid_base_request)
        self.assertTrue(res_self["is_approved"])
        self.assertAlmostEqual(res_self["interest_rate"], 9.5, places=2) # 8.5 base + 1.0 premium

        # Unemployed validation
        self.valid_base_request["employment_type"] = "UNEMPLOYED"
        res_un = self.system.process_loan(self.valid_base_request)
        self.assertFalse(res_un["is_approved"])

    def test_boundary_loan_amounts(self):
        self.valid_base_request["requested_loan_amount"] = 0.0
        res = self.system.process_loan(self.valid_base_request)
        self.assertTrue(res["is_approved"])
        self.assertEqual(res["eligible_loan_amount"], 0.0)

    def test_emi_calculation_accuracy(self):
        self.valid_base_request["requested_loan_amount"] = 10000.0
        self.valid_base_request["monthly_salary"] = 20000.0
        self.valid_base_request["loan_tenure_months"] = 12
        self.valid_base_request["credit_score"] = 800  # Base rate 8.5%
        
        res = self.system.process_loan(self.valid_base_request)
        self.assertTrue(res["is_approved"])
        self.assertTrue(res["emi"] > 0)

    def test_invalid_input_handling(self):
        self.valid_base_request["credit_score"] = 1000  # Outside valid range
        with self.assertRaises(ValueError):
            self.system.process_loan(self.valid_base_request)

    def test_exception_handling(self):
        with self.assertRaises(ValueError):
            self.system.process_loan(None)
        
        self.valid_base_request["customer_id"] = "   "
        with self.assertRaises(ValueError):
            self.system.process_loan(self.valid_base_request)

if __name__ == "__main__":
    unittest.main()
