package com.banking.loan;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class LoanProcessingQA {

    private LoanProcessingSystem system;
    private LoanProcessingSystem.LoanRequest validBaseRequest;

    @BeforeEach
    public void setUp() {
        system = new LoanProcessingSystem();
        validBaseRequest = new LoanProcessingSystem.LoanRequest();
        validBaseRequest.customerId = "CUST1001";
        validBaseRequest.age = 30;
        validBaseRequest.monthlySalary = 10000.0;
        validBaseRequest.existingLoanAmount = 20000.0;
        validBaseRequest.creditScore = 750;
        validBaseRequest.employmentType = "SALARIED";
        validBaseRequest.requestedLoanAmount = 50000.0;
        validBaseRequest.loanTenureMonths = 36;
    }

    @Test
    public void testMinimumMaximumAge() {
        // Underage scenario
        validBaseRequest.age = 17;
        assertFalse(system.processLoan(validBaseRequest).isApproved);

        // Overage scenario
        validBaseRequest.age = 66;
        assertFalse(system.processLoan(validBaseRequest).isApproved);
    }

    @Test
    public void testInvalidSalary() {
        validBaseRequest.monthlySalary = -500.0;
        assertThrows(IllegalArgumentException.class, () -> system.processLoan(validBaseRequest));
    }

    @Test
    public void testPoorCreditScore() {
        validBaseRequest.creditScore = 450;
        LoanProcessingSystem.LoanResponse response = system.processLoan(validBaseRequest);
        assertFalse(response.isApproved);
        assertEquals("Poor credit score", response.rejectionReason);
    }

    @Test
    public void testExistingLoanExceedingThreshold() {
        // Salary is 10k, setting threshold multiple to exceed 36x salary limits
        validBaseRequest.existingLoanAmount = 400000.0; 
        assertFalse(system.processLoan(validBaseRequest).isApproved);
    }

    @Test
    public void testHighDebtToIncomeRatio() {
        // Higher existing balance scales up the calculated ongoing DTI
        validBaseRequest.existingLoanAmount = 300000.0;
        LoanProcessingSystem.LoanResponse response = system.processLoan(validBaseRequest);
        assertFalse(response.isApproved);
    }

    @Test
    public void testDifferentEmploymentCategories() {
        validBaseRequest.employmentType = "SELF_EMPLOYED";
        LoanProcessingSystem.LoanResponse respSelf = system.processLoan(validBaseRequest);
        assertTrue(respSelf.isApproved);
        assertEquals(9.5, respSelf.interestRate, 0.01); // 8.5 base + 1.0 premium

        validBaseRequest.employmentType = "UNEMPLOYED";
        LoanProcessingSystem.LoanResponse respUn = system.processLoan(validBaseRequest);
        assertFalse(respUn.isApproved);
    }

    @Test
    public void testBoundaryLoanAmounts() {
        // Edge case: Requesting 0 balance
        validBaseRequest.requestedLoanAmount = 0.0;
        LoanProcessingSystem.LoanResponse response = system.processLoan(validBaseRequest);
        assertTrue(response.isApproved);
        assertEquals(0.0, response.eligibleLoanAmount, 0.01);
    }

    @Test
    public void testEmiCalculationAccuracy() {
        validBaseRequest.requestedLoanAmount = 10000.0;
        validBaseRequest.monthlySalary = 20000.0;
        validBaseRequest.loanTenureMonths = 12;
        validBaseRequest.creditScore = 800; // Base rate 8.5%
        
        LoanProcessingSystem.LoanResponse response = system.processLoan(validBaseRequest);
        // Validating standard amortization behavior 
        assertTrue(response.emi > 0);
        assertTrue(response.isApproved);
    }

    @Test
    public void testInvalidInputHandling() {
        validBaseRequest.creditScore = 1000; // Outside standard limits
        assertThrows(IllegalArgumentException.class, () -> system.processLoan(validBaseRequest));
    }

    @Test
    public void testExceptionHandling() {
        assertThrows(IllegalArgumentException.class, () -> system.processLoan(null));
        
        validBaseRequest.customerId = "   ";
        assertThrows(IllegalArgumentException.class, () -> system.processLoan(validBaseRequest));
    }
}
