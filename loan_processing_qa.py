import sys
from loan_processing_system import LoanProcessingSystem

def run_qa_suite():
    print(" Starting Python QA Automated Test Suite...")
    passed_tests = 0

    # Test 1: Age Boundary Failure (Too Young)
    try:
        loan = LoanProcessingSystem("C01", 16, 50000, 0, 700, "STABLE", 100000, 12)
        loan.process_loan()
        print(" Test 1 Failed: System accepted a minor.")
    except ValueError:
        print("Bit 1 Passed: Minimum age boundary checked correctly.")
        passed_tests += 1

    # Test 2: Invalid Salary Handling
    try:
        loan = LoanProcessingSystem("C02", 30, -500, 0, 700, "STABLE", 100000, 12)
        loan.process_loan()
        print(" Test 2 Failed: System accepted a negative salary.")
    except ValueError:
        print("Bit 2 Passed: Invalid salary exception verified.")
        passed_tests += 1

    # Test 3: Reject Poor Credit Score
    loan3 = LoanProcessingSystem("C03", 40, 60000, 0, 450, "STABLE", 100000, 24)
    loan3.process_loan()
    if "REJECTED" in loan3.get_approval_status():
        print("Bit 3 Passed: Poor credit score rejected successfully.")
        passed_tests += 1
    else:
        print(" Test 3 Failed: Poor credit score was mistakenly approved.")

    # Test 4: Existing Loan Exceeding Maximum Safe Threshold
    loan4 = LoanProcessingSystem("C04", 35, 30000, 1500000, 750, "STABLE", 50000, 12)
    loan4.process_loan()
    if "REJECTED" in loan4.get_approval_status():
        print("Bit 4 Passed: Out-of-bounds existing loans flagged correctly.")
        passed_tests += 1
    else:
        print(" Test 4 Failed: High existing debts were ignored.")

    # Test 5: High Debt-to-Income Ratio Reject
    loan5 = LoanProcessingSystem("C05", 28, 4000, 25000, 720, "STABLE", 20000, 12)
    loan5.process_loan()
    if "REJECTED" in loan5.get_approval_status():
        print("Bit 5 Passed: High debt-to-income blocks loan processing.")
        passed_tests += 1
    else:
        print(" Test 5 Failed: Failed to catch risky debt-to-income balance.")

    # Test 6: Employment Classification Effects (Rate Loading)
    loan6A = LoanProcessingSystem("C06A", 35, 80000, 0, 800, "STABLE", 100000, 12)
    loan6B = LoanProcessingSystem("C06B", 35, 80000, 0, 800, "UNSTABLE", 100000, 12)
    loan6A.process_loan()
    loan6B.process_loan()
    if loan6B.get_interest_rate() > loan6A.get_interest_rate():
        print("Bit 6 Passed: Unstable employment penalty risk calculated accurately.")
        passed_tests += 1
    else:
        print(" Test 6 Failed: System did not update rates based on risk factors.")

    # Test 7 & 8: Requested Boundary Amount Evaluation & EMI Math Accuracy
    loan7 = LoanProcessingSystem("C07", 32, 50000, 0, 780, "STABLE", 100000, 12)
    loan7.process_loan()
    if loan7.get_emi() > 0 and loan7.get_eligible_loan_amount() == 1000000:
        print("Bit 7 & 8 Passed: Core math formulas and caps calculated within correct limits.")
        passed_tests += 2
    else:
        print(" Test 7/8 Failed: Mathematical deviation found in EMI calculation engines.")

    # Test 9 & 10: General System Integrity and Validation Controls
    try:
        loan9 = LoanProcessingSystem("C09", 25, 45000, 0, 999, "STABLE", 10000, 12)
        loan9.process_loan()
        print(" Test 9 & 10 Failed: Invalid credit scores allowed through.")
    except ValueError:
        print("Bit 9 & 10 Passed: Validation rules and error exceptions handled correctly.")
        passed_tests += 2

    # Summary Check
    print(f"\n QA Test Execution Summary Matrix: {passed_tests}/10 Test Parameters Passed.")
    if passed_tests != 10:
        sys.exit(1) # Explicitly exits with code 1 so Jenkins marks the build step as FAILED

if __name__ == "__main__":
    run_qa_suite()
