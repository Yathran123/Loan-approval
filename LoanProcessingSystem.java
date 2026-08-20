import java.io.Serializable;

public class LoanProcessingSystem implements Serializable {
    private String customerId;
    private int age;
    private double monthlySalary;
    private double existingLoanAmount;
    private int creditScore;
    private String employmentType; 
    private double requestedLoanAmount;
    private int loanTenureMonths;
    private double debtToIncomeRatio;
    private double eligibleLoanAmount;
    private double interestRate;
    private double emi;
    private String approvalStatus;
    public LoanProcessingSystem(String customerId, int age, double monthlySalary, double existingLoanAmount,
                                int creditScore, String employmentType, double requestedLoanAmount, int loanTenureMonths) {
        this.customerId = customerId;
        this.age = age;
        this.monthlySalary = monthlySalary;
        this.existingLoanAmount = existingLoanAmount;
        this.creditScore = creditScore;
        this.employmentType = employmentType;
        this.requestedLoanAmount = requestedLoanAmount;
        this.loanTenureMonths = loanTenureMonths;
    }
    public void processLoan() {
        // 1. Validation & Exception Handling
        if (age < 18 || age > 65) {
            throw new IllegalArgumentException("Invalid Age: Customer age must be between 18 and 65.");
        }
        if (monthlySalary <= 0) {
            throw new IllegalArgumentException("Invalid Salary: Monthly salary must be greater than zero.");
        }
        if (creditScore < 300 || creditScore > 850) {
            throw new IllegalArgumentException("Invalid Credit Score: Score must be between 300 and 850.");
        }
        if (requestedLoanAmount <= 0 || loanTenureMonths <= 0) {
            throw new IllegalArgumentException("Invalid Loan Request: Amount and tenure must be positive values.");
        }
        double estimatedExistingEmi = existingLoanAmount * 0.10; 
        this.debtToIncomeRatio = (estimatedExistingEmi / monthlySalary) * 100;
        double baseRate = 8.5;
        if (creditScore < 600) baseRate += 4.0;
        else if (creditScore < 700) baseRate += 2.0;
        else if (creditScore < 750) baseRate += 0.5;

        if ("UNSTABLE".equalsIgnoreCase(employmentType)) {
            baseRate += 1.5;
        }
        this.interestRate = baseRate;
        double multiplier = 10.0;
        if (creditScore >= 750) multiplier = 20.0;
        this.eligibleLoanAmount = monthlySalary * multiplier;
        double monthlyRate = (this.interestRate / 100) / 12;
        this.emi = (requestedLoanAmount * monthlyRate * Math.pow(1 + monthlyRate, loanTenureMonths)) 
                    / (Math.pow(1 + monthlyRate, loanTenureMonths) - 1);
        if (creditScore < 550) {
            this.approvalStatus = "REJECTED (Poor Credit Score)";
        } else if (this.debtToIncomeRatio > 50.0) {
            this.approvalStatus = "REJECTED (High Debt-To-Income Ratio)";
        } else if (existingLoanAmount > (monthlySalary * 36)) {
            this.approvalStatus = "REJECTED (Existing Loans Exceed Safe Income Threshold)";
        } else if (requestedLoanAmount > this.eligibleLoanAmount) {
            this.approvalStatus = "REJECTED (Requested Amount Exceeds Eligibility Cap)";
        } else {
            this.approvalStatus = "APPROVED";
        }
    }
    public String getApprovalStatus() { return approvalStatus; }
    public double getDebtToIncomeRatio() { return debtToIncomeRatio; }
    public double getEligibleLoanAmount() { return eligibleLoanAmount; }
    public double getEmi() { return emi; }
    public double getInterestRate() { return interestRate; }
}
