package com.banking.loan;

import java.io.Serializable;

public class LoanProcessingSystem implements Serializable {
    private static final long serialVersionUID = 1L;

    public static class LoanRequest {
        public String customerId;
        public int age;
        public double monthlySalary;
        public double existingLoanAmount;
        public int creditScore;
        public String employmentType; // "SALARIED", "SELF_EMPLOYED", "UNEMPLOYED"
        public double requestedLoanAmount;
        public int loanTenureMonths;
    }

    public static class LoanResponse {
        public double debtToIncomeRatio;
        public double eligibleLoanAmount;
        public double interestRate;
        public double emi;
        public boolean isApproved;
        public String rejectionReason = "";
    }

    public LoanResponse processLoan(LoanRequest request) {
        if (request == null) {
            throw new IllegalArgumentException("Loan request cannot be null");
        }
        
        validateInputs(request);
        LoanResponse response = new LoanResponse();

        // 1. Calculate Debt-to-Income (DTI) Ratio
        // Assuming a standard monthly commitment calculation based on existing liability guidelines
        double estimatedExistingMonthlyCommitment = request.existingLoanAmount * 0.02; 
        if (request.monthlySalary > 0) {
            response.debtToIncomeRatio = (estimatedExistingMonthlyCommitment / request.monthlySalary) * 100;
        } else {
            response.debtToIncomeRatio = 100.0;
        }

        // 2. Determine base eligibility and interest rates based on Credit Score & Employment
        if (request.creditScore < 600) {
            response.isApproved = false;
            response.rejectionReason = "Poor credit score";
            return response;
        } else if (request.creditScore < 700) {
            response.interestRate = 12.5;
        } else {
            response.interestRate = 8.5;
        }

        // Employment premium modifications
        if ("UNEMPLOYED".equalsIgnoreCase(request.employmentType)) {
            response.isApproved = false;
            response.rejectionReason = "Unemployed status ineligible";
            return response;
        } else if ("SELF_EMPLOYED".equalsIgnoreCase(request.employmentType)) {
            response.interestRate += 1.0; // Risk premium
        }

        // 3. Evaluate Threshold Rules (Age and Maximum Existing Loan Limitations)
        if (request.age < 18 || request.age > 65) {
            response.isApproved = false;
            response.rejectionReason = "Age out of bounds";
            return response;
        }

        if (request.existingLoanAmount > (request.monthlySalary * 36)) {
            response.isApproved = false;
            response.rejectionReason = "Existing loan exceeds permissible multiplier threshold";
            return response;
        }

        if (response.debtToIncomeRatio > 50.0) {
            response.isApproved = false;
            response.rejectionReason = "High debt-to-income ratio";
            return response;
        }

        // 4. Calculate Maximum Loan Eligibility Matrix
        double maxEligibleAmount = request.monthlySalary * 12;
        response.eligibleLoanAmount = Math.min(maxEligibleAmount, request.requestedLoanAmount);

        // 5. Calculate Equated Monthly Installment (EMI)
        // Formula: EMI = [P x R x (1+R)^N]/[((1+R)^N)-1]
        double monthlyRate = (response.interestRate / 12) / 100;
        int months = request.loanTenureMonths;
        
        if (months > 0 && monthlyRate > 0) {
            response.emi = (response.eligibleLoanAmount * monthlyRate * Math.pow(1 + monthlyRate, months)) 
                           / (Math.pow(1 + monthlyRate, months) - 1);
        } else if (months > 0) {
            response.emi = response.eligibleLoanAmount / months;
        }

        response.isApproved = true;
        return response;
    }

    private void validateInputs(LoanRequest r) {
        if (r.customerId == null || r.customerId.trim().isEmpty()) {
            throw new IllegalArgumentException("Invalid Customer ID");
        }
        if (r.monthlySalary < 0 || r.existingLoanAmount < 0 || r.requestedLoanAmount < 0) {
            throw new IllegalArgumentException("Financial values cannot be negative");
        }
        if (r.creditScore < 300 || r.creditScore > 850) {
            throw new IllegalArgumentException("Credit score must be between 300 and 850");
        }
        if (r.loanTenureMonths <= 0) {
            throw new IllegalArgumentException("Loan tenure must be greater than zero");
        }
    }
}
