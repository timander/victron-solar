      ******************************************************************
      * SOLAR COST ANALYSIS PROGRAM
      * Purpose: Calculate solar energy cost savings from CSV data
      * Author: Modernized COBOL Demo
      * Date: 2025-11-04
      * 
      * This program demonstrates modern COBOL practices in a 
      * containerized environment, processing solar panel data
      * to generate financial analysis reports.
      ******************************************************************
       IDENTIFICATION DIVISION.
       PROGRAM-ID. SOLARCOST.
       
       ENVIRONMENT DIVISION.
       INPUT-OUTPUT SECTION.
       FILE-CONTROL.
           SELECT CSV-INPUT-FILE
               ASSIGN TO CSV-FILE
               ORGANIZATION IS LINE SEQUENTIAL
               FILE STATUS IS WS-FILE-STATUS.
               
           SELECT REPORT-OUTPUT-FILE
               ASSIGN TO REPORT-FILE
               ORGANIZATION IS LINE SEQUENTIAL
               FILE STATUS IS WS-REPORT-STATUS.
       
       DATA DIVISION.
       FILE SECTION.
       FD  CSV-INPUT-FILE.
       01  CSV-RECORD                  PIC X(200).
       
       FD  REPORT-OUTPUT-FILE.
       01  REPORT-LINE                 PIC X(70).
       
       WORKING-STORAGE SECTION.
      *----------------------------------------------------------------*
      * File Status and Control Variables
      *----------------------------------------------------------------*
       01  CSV-FILE                    PIC X(100).
       01  REPORT-FILE                 PIC X(100).
       
       01  WS-FILE-STATUS              PIC XX.
           88  WS-FILE-OK              VALUE "00".
           88  WS-FILE-EOF             VALUE "10".
           
       01  WS-REPORT-STATUS            PIC XX.
       
       01  WS-RECORD-COUNT             PIC 9(5) VALUE ZERO.
       01  WS-FIRST-RECORD-FLAG        PIC X VALUE "Y".
           88  WS-IS-FIRST-RECORD      VALUE "Y".
           88  WS-NOT-FIRST-RECORD     VALUE "N".
           
      *----------------------------------------------------------------*
      * CSV Field Definitions (15 fields from SolarHistory.csv)
      *----------------------------------------------------------------*
       01  WS-CSV-FIELDS.
           05  WS-DAYS-AGO             PIC X(10).
           05  WS-DATE-STR             PIC X(10).
           05  WS-YIELD-STR            PIC X(10).
           05  WS-CONSUMPTION-STR      PIC X(10).
           05  WS-MAX-PV-POWER         PIC X(10).
           05  WS-MAX-PV-VOLTAGE       PIC X(10).
           05  WS-MIN-BATTERY-V        PIC X(10).
           05  WS-MAX-BATTERY-V        PIC X(10).
           05  WS-TIME-BULK            PIC X(10).
           05  WS-TIME-ABSORPTION      PIC X(10).
           05  WS-TIME-FLOAT           PIC X(10).
           05  WS-ERROR-1              PIC X(10).
           05  WS-ERROR-2              PIC X(10).
           05  WS-ERROR-3              PIC X(10).
           05  WS-ERROR-4              PIC X(10).
       
      *----------------------------------------------------------------*
      * Numeric Working Fields
      *----------------------------------------------------------------*
       01  WS-YIELD-WH                 PIC 9(6)V99 COMP-3.
       01  WS-CONSUMPTION-WH           PIC 9(6)V99 COMP-3.
       
      *----------------------------------------------------------------*
      * Accumulator Variables
      *----------------------------------------------------------------*
       01  WS-TOTAL-YIELD-WH           PIC 9(8)V99 COMP-3 VALUE ZERO.
       01  WS-TOTAL-CONSUMPTION-WH     PIC 9(8)V99 COMP-3 VALUE ZERO.
       
      *----------------------------------------------------------------*
      * Calculation Results (in kWh and USD)
      *----------------------------------------------------------------*
       01  WS-RATE-PER-KWH             PIC 9V999 COMP-3 VALUE 0.140.
       
       01  WS-TOTAL-SOLAR-KWH          PIC 9(6)V999 COMP-3.
       01  WS-TOTAL-CONSUMPTION-KWH    PIC 9(6)V999 COMP-3.
       01  WS-SOLAR-VALUE-USD          PIC 9(5)V99 COMP-3.
       01  WS-CONSUMPTION-COST-USD     PIC 9(5)V99 COMP-3.
       01  WS-NET-SAVINGS-USD          PIC S9(5)V99 COMP-3.
       01  WS-SOLAR-OFFSET-PCT         PIC 9(5)V9 COMP-3.
       
       01  WS-AVG-DAILY-SOLAR-KWH      PIC 9(4)V999 COMP-3.
       01  WS-AVG-DAILY-CONSUMP-KWH    PIC 9(4)V999 COMP-3.
       01  WS-PROJECTED-ANNUAL-USD     PIC 9(6)V99 COMP-3.
       
      *----------------------------------------------------------------*
      * Report Formatting Variables
      *----------------------------------------------------------------*
       01  WS-EDIT-KWH-1               PIC ZZZ9.99.
       01  WS-EDIT-KWH-2               PIC Z9.999.
       01  WS-EDIT-USD                 PIC $$$$,$$9.99.
       01  WS-EDIT-USD-SMALL           PIC $ZZZ9.99.
       01  WS-EDIT-PCT                 PIC ZZZ9.9.
       01  WS-EDIT-DAYS                PIC ZZ9.
       01  WS-EDIT-YEARS               PIC ZZZ9.9.
       
       01  WS-PAYBACK-1000             PIC 9(5)V9 COMP-3.
       01  WS-PAYBACK-2000             PIC 9(5)V9 COMP-3.
       01  WS-PAYBACK-3000             PIC 9(5)V9 COMP-3.
       
      *----------------------------------------------------------------*
      * Constants
      *----------------------------------------------------------------*
       01  WS-CONSTANTS.
           05  WS-SEPARATOR-LINE       PIC X(70) VALUE ALL "-".
           05  WS-EQUALS-LINE          PIC X(70) VALUE ALL "=".
           
       PROCEDURE DIVISION.
      *----------------------------------------------------------------*
      * MAIN CONTROL LOGIC
      *----------------------------------------------------------------*
       000-MAIN-CONTROL.
           PERFORM 100-INITIALIZE-PROGRAM.
           PERFORM 200-PROCESS-CSV-FILE.
           PERFORM 300-CALCULATE-COSTS.
           PERFORM 400-GENERATE-REPORT.
           PERFORM 900-CLEANUP-AND-EXIT.
           STOP RUN.
       
      *----------------------------------------------------------------*
      * INITIALIZATION
      *----------------------------------------------------------------*
       100-INITIALIZE-PROGRAM.
           DISPLAY "Initializing Solar Cost Analysis Program..."
           
           ACCEPT CSV-FILE FROM ENVIRONMENT "CSV_INPUT"
           IF CSV-FILE = SPACES
               MOVE "../data/SolarHistory.csv" TO CSV-FILE
           END-IF
           
           ACCEPT REPORT-FILE FROM ENVIRONMENT "REPORT_OUTPUT"
           IF REPORT-FILE = SPACES
               MOVE "./output/solar_cost_report.txt" TO REPORT-FILE
           END-IF
           
           OPEN INPUT CSV-INPUT-FILE
           IF NOT WS-FILE-OK
               DISPLAY "ERROR: Cannot open input file: " CSV-FILE
               DISPLAY "File Status: " WS-FILE-STATUS
               STOP RUN
           END-IF
           
           OPEN OUTPUT REPORT-OUTPUT-FILE
           IF NOT WS-FILE-OK
               DISPLAY "ERROR: Cannot open output file: " REPORT-FILE
               DISPLAY "File Status: " WS-REPORT-STATUS
               STOP RUN
           END-IF
           
           DISPLAY "Input file: " CSV-FILE
           DISPLAY "Output file: " REPORT-FILE.
       
      *----------------------------------------------------------------*
      * PROCESS CSV FILE
      *----------------------------------------------------------------*
       200-PROCESS-CSV-FILE.
           DISPLAY "Processing CSV records..."
           PERFORM UNTIL WS-FILE-EOF
               PERFORM 210-READ-CSV-RECORD
               IF NOT WS-FILE-EOF
                   IF WS-IS-FIRST-RECORD
                       MOVE "N" TO WS-FIRST-RECORD-FLAG
                       DISPLAY "Skipping header row"
                   ELSE
                       PERFORM 220-PARSE-CSV-FIELDS
                       PERFORM 230-ACCUMULATE-TOTALS
                       ADD 1 TO WS-RECORD-COUNT
                   END-IF
               END-IF
           END-PERFORM
           
           DISPLAY "Processed " WS-RECORD-COUNT " data records".
       
      *----------------------------------------------------------------*
      * READ CSV RECORD
      *----------------------------------------------------------------*
       210-READ-CSV-RECORD.
           READ CSV-INPUT-FILE
               AT END
                   SET WS-FILE-EOF TO TRUE
           END-READ.
       
      *----------------------------------------------------------------*
      * PARSE CSV FIELDS (Split comma-delimited record into fields)
      *----------------------------------------------------------------*
       220-PARSE-CSV-FIELDS.
           UNSTRING CSV-RECORD
               DELIMITED BY ","
               INTO WS-DAYS-AGO
                    WS-DATE-STR
                    WS-YIELD-STR
                    WS-CONSUMPTION-STR
                    WS-MAX-PV-POWER
                    WS-MAX-PV-VOLTAGE
                    WS-MIN-BATTERY-V
                    WS-MAX-BATTERY-V
                    WS-TIME-BULK
                    WS-TIME-ABSORPTION
                    WS-TIME-FLOAT
                    WS-ERROR-1
                    WS-ERROR-2
                    WS-ERROR-3
                    WS-ERROR-4
           END-UNSTRING.
       
      *----------------------------------------------------------------*
      * ACCUMULATE TOTALS (Convert strings to numbers and sum)
      *----------------------------------------------------------------*
       230-ACCUMULATE-TOTALS.
      *    Convert Yield(Wh) from string to numeric
           IF WS-YIELD-STR NOT = SPACES
               MOVE FUNCTION NUMVAL(WS-YIELD-STR) TO WS-YIELD-WH
               ADD WS-YIELD-WH TO WS-TOTAL-YIELD-WH
           END-IF
           
      *    Convert Consumption(Wh) from string to numeric  
           IF WS-CONSUMPTION-STR NOT = SPACES
               MOVE FUNCTION NUMVAL(WS-CONSUMPTION-STR) 
                   TO WS-CONSUMPTION-WH
               ADD WS-CONSUMPTION-WH TO WS-TOTAL-CONSUMPTION-WH
           END-IF.
       
      *----------------------------------------------------------------*
      * CALCULATE COSTS (Match Python cost_analysis.py logic)
      *----------------------------------------------------------------*
       300-CALCULATE-COSTS.
           DISPLAY "Calculating costs..."
           
           PERFORM 310-CONVERT-TO-KWH
           PERFORM 320-CALCULATE-FINANCIALS
           PERFORM 330-COMPUTE-PROJECTIONS.
       
      *----------------------------------------------------------------*
      * CONVERT WH TO KWH (Divide by 1000)
      *----------------------------------------------------------------*
       310-CONVERT-TO-KWH.
      *    Convert total Wh to kWh (divide by 1000)
           COMPUTE WS-TOTAL-SOLAR-KWH = WS-TOTAL-YIELD-WH / 1000
           COMPUTE WS-TOTAL-CONSUMPTION-KWH = 
               WS-TOTAL-CONSUMPTION-WH / 1000.
       
      *----------------------------------------------------------------*
      * CALCULATE FINANCIALS (Cost = kWh * rate)
      *----------------------------------------------------------------*
       320-CALCULATE-FINANCIALS.
      *    Calculate value of solar generated (kWh * rate)
           COMPUTE WS-SOLAR-VALUE-USD = 
               WS-TOTAL-SOLAR-KWH * WS-RATE-PER-KWH
           
      *    Calculate cost of energy consumed
           COMPUTE WS-CONSUMPTION-COST-USD = 
               WS-TOTAL-CONSUMPTION-KWH * WS-RATE-PER-KWH
           
      *    Calculate net savings (can be negative)
           COMPUTE WS-NET-SAVINGS-USD = 
               WS-SOLAR-VALUE-USD - WS-CONSUMPTION-COST-USD
           
      *    Calculate solar offset percentage
           IF WS-TOTAL-CONSUMPTION-KWH > 0
               COMPUTE WS-SOLAR-OFFSET-PCT = 
                   (WS-TOTAL-SOLAR-KWH / WS-TOTAL-CONSUMPTION-KWH) 
                   * 100
           ELSE
               MOVE ZERO TO WS-SOLAR-OFFSET-PCT
           END-IF.
       
      *----------------------------------------------------------------*
      * COMPUTE PROJECTIONS (Daily averages and annual estimates)
      *----------------------------------------------------------------*
       330-COMPUTE-PROJECTIONS.
      *    Calculate daily averages
           IF WS-RECORD-COUNT > 0
               COMPUTE WS-AVG-DAILY-SOLAR-KWH = 
                   WS-TOTAL-SOLAR-KWH / WS-RECORD-COUNT
               COMPUTE WS-AVG-DAILY-CONSUMP-KWH = 
                   WS-TOTAL-CONSUMPTION-KWH / WS-RECORD-COUNT
               
      *        Project annual savings (multiply by 365/days)
               COMPUTE WS-PROJECTED-ANNUAL-USD = 
                   WS-NET-SAVINGS-USD * (365 / WS-RECORD-COUNT)
               
      *        Calculate payback periods for different system costs
               IF WS-PROJECTED-ANNUAL-USD > 0
                   COMPUTE WS-PAYBACK-1000 = 1000 / 
                       WS-PROJECTED-ANNUAL-USD
                   COMPUTE WS-PAYBACK-2000 = 2000 / 
                       WS-PROJECTED-ANNUAL-USD
                   COMPUTE WS-PAYBACK-3000 = 3000 / 
                       WS-PROJECTED-ANNUAL-USD
               ELSE
                   MOVE 9999.9 TO WS-PAYBACK-1000
                   MOVE 9999.9 TO WS-PAYBACK-2000
                   MOVE 9999.9 TO WS-PAYBACK-3000
               END-IF
           END-IF.
       
      *----------------------------------------------------------------*
      * GENERATE REPORT (Match Python format exactly)
      *----------------------------------------------------------------*
       400-GENERATE-REPORT.
           DISPLAY "Generating report..."
           
           PERFORM 410-PRINT-HEADER
           PERFORM 420-PRINT-ENERGY-SUMMARY
           PERFORM 430-PRINT-FINANCIAL-ANALYSIS
           PERFORM 440-PRINT-PROJECTIONS
           PERFORM 450-PRINT-INVESTMENT-GUIDANCE
           PERFORM 460-PRINT-FOOTER.
       
      *----------------------------------------------------------------*
      * PRINT HEADER
      *----------------------------------------------------------------*
       410-PRINT-HEADER.
           WRITE REPORT-LINE FROM WS-EQUALS-LINE
           MOVE "SOLAR ENERGY COST ANALYSIS REPORT" TO REPORT-LINE
           WRITE REPORT-LINE
           WRITE REPORT-LINE FROM WS-EQUALS-LINE
           WRITE REPORT-LINE FROM SPACES
           
      *    Format and write analysis period
           MOVE SPACES TO REPORT-LINE
           MOVE WS-RECORD-COUNT TO WS-EDIT-DAYS
           STRING "Analysis Period: " DELIMITED BY SIZE
                  WS-EDIT-DAYS DELIMITED BY SIZE
                  " days" DELIMITED BY SIZE
                  INTO REPORT-LINE
           WRITE REPORT-LINE
           
      *    Format and write electricity rate
           MOVE "Electricity Rate: $0.140 per kWh" TO REPORT-LINE
           WRITE REPORT-LINE
           WRITE REPORT-LINE FROM SPACES.
       
      *----------------------------------------------------------------*
      * PRINT ENERGY SUMMARY
      *----------------------------------------------------------------*
       420-PRINT-ENERGY-SUMMARY.
           WRITE REPORT-LINE FROM WS-SEPARATOR-LINE
           MOVE "ENERGY SUMMARY" TO REPORT-LINE
           WRITE REPORT-LINE
           WRITE REPORT-LINE FROM WS-SEPARATOR-LINE
           
      *    Solar Energy Collected
           MOVE SPACES TO REPORT-LINE
           MOVE WS-TOTAL-SOLAR-KWH TO WS-EDIT-KWH-1
           STRING "Solar Energy Collected:    " DELIMITED BY SIZE
                  WS-EDIT-KWH-1 DELIMITED BY SIZE
                  " kWh" DELIMITED BY SIZE
                  INTO REPORT-LINE
           WRITE REPORT-LINE
           
      *    Energy Consumed
           MOVE SPACES TO REPORT-LINE
           MOVE WS-TOTAL-CONSUMPTION-KWH TO WS-EDIT-KWH-1
           STRING "Energy Consumed:           " DELIMITED BY SIZE
                  WS-EDIT-KWH-1 DELIMITED BY SIZE
                  " kWh" DELIMITED BY SIZE
                  INTO REPORT-LINE
           WRITE REPORT-LINE
           
      *    Solar Offset
           MOVE SPACES TO REPORT-LINE
           MOVE WS-SOLAR-OFFSET-PCT TO WS-EDIT-PCT
           STRING "Solar Offset:              " DELIMITED BY SIZE
                  WS-EDIT-PCT DELIMITED BY SIZE
                  "%" DELIMITED BY SIZE
                  INTO REPORT-LINE
           WRITE REPORT-LINE
           WRITE REPORT-LINE FROM SPACES
           
      *    Daily Average Solar
           MOVE SPACES TO REPORT-LINE
           MOVE WS-AVG-DAILY-SOLAR-KWH TO WS-EDIT-KWH-2
           STRING "Daily Average Solar:       " DELIMITED BY SIZE
                  WS-EDIT-KWH-2 DELIMITED BY SIZE
                  " kWh" DELIMITED BY SIZE
                  INTO REPORT-LINE
           WRITE REPORT-LINE
           
      *    Daily Average Consumption
           MOVE SPACES TO REPORT-LINE
           MOVE WS-AVG-DAILY-CONSUMP-KWH TO WS-EDIT-KWH-2
           STRING "Daily Average Consumption: " DELIMITED BY SIZE
                  WS-EDIT-KWH-2 DELIMITED BY SIZE
                  " kWh" DELIMITED BY SIZE
                  INTO REPORT-LINE
           WRITE REPORT-LINE
           WRITE REPORT-LINE FROM SPACES.
       
      *----------------------------------------------------------------*
      * PRINT FINANCIAL ANALYSIS
      *----------------------------------------------------------------*
       430-PRINT-FINANCIAL-ANALYSIS.
           WRITE REPORT-LINE FROM WS-SEPARATOR-LINE
           MOVE "FINANCIAL ANALYSIS" TO REPORT-LINE
           WRITE REPORT-LINE
           WRITE REPORT-LINE FROM WS-SEPARATOR-LINE
           
      *    Value of Solar Generated
           MOVE SPACES TO REPORT-LINE
           MOVE WS-SOLAR-VALUE-USD TO WS-EDIT-USD-SMALL
           STRING "Value of Solar Generated:  " DELIMITED BY SIZE
                  WS-EDIT-USD-SMALL DELIMITED BY SIZE
                  INTO REPORT-LINE
           WRITE REPORT-LINE
           
      *    Cost of Energy Consumed
           MOVE SPACES TO REPORT-LINE
           MOVE WS-CONSUMPTION-COST-USD TO WS-EDIT-USD-SMALL
           STRING "Cost of Energy Consumed:   " DELIMITED BY SIZE
                  WS-EDIT-USD-SMALL DELIMITED BY SIZE
                  INTO REPORT-LINE
           WRITE REPORT-LINE
           
      *    NET SAVINGS
           MOVE SPACES TO REPORT-LINE
           MOVE WS-NET-SAVINGS-USD TO WS-EDIT-USD-SMALL
           STRING "NET SAVINGS:               " DELIMITED BY SIZE
                  WS-EDIT-USD-SMALL DELIMITED BY SIZE
                  INTO REPORT-LINE
           WRITE REPORT-LINE
           WRITE REPORT-LINE FROM SPACES.
       
      *----------------------------------------------------------------*
      * PRINT PROJECTIONS
      *----------------------------------------------------------------*
       440-PRINT-PROJECTIONS.
           WRITE REPORT-LINE FROM WS-SEPARATOR-LINE
           MOVE "PROJECTIONS" TO REPORT-LINE
           WRITE REPORT-LINE
           WRITE REPORT-LINE FROM WS-SEPARATOR-LINE
           
      *    Projected Annual Savings
           MOVE SPACES TO REPORT-LINE
           MOVE WS-PROJECTED-ANNUAL-USD TO WS-EDIT-USD-SMALL
           STRING "Projected Annual Savings:  " DELIMITED BY SIZE
                  WS-EDIT-USD-SMALL DELIMITED BY SIZE
                  INTO REPORT-LINE
           WRITE REPORT-LINE
           WRITE REPORT-LINE FROM SPACES.
       
      *----------------------------------------------------------------*
      * PRINT INVESTMENT GUIDANCE
      *----------------------------------------------------------------*
       450-PRINT-INVESTMENT-GUIDANCE.
           WRITE REPORT-LINE FROM WS-SEPARATOR-LINE
           MOVE "INVESTMENT GUIDANCE" TO REPORT-LINE
           WRITE REPORT-LINE
           WRITE REPORT-LINE FROM WS-SEPARATOR-LINE
           
      *    Based on analysis period
           MOVE SPACES TO REPORT-LINE
           MOVE WS-RECORD-COUNT TO WS-EDIT-DAYS
           STRING "Based on your " DELIMITED BY SIZE
                  WS-EDIT-DAYS DELIMITED BY SIZE
                  "-day analysis:" DELIMITED BY SIZE
                  INTO REPORT-LINE
           WRITE REPORT-LINE
           WRITE REPORT-LINE FROM SPACES
           
      *    Solar system value
           MOVE SPACES TO REPORT-LINE
           MOVE WS-SOLAR-VALUE-USD TO WS-EDIT-USD-SMALL
           STRING "* Your solar system generates " DELIMITED BY SIZE
                  WS-EDIT-USD-SMALL DELIMITED BY SIZE
                  " worth of energy" DELIMITED BY SIZE
                  INTO REPORT-LINE
           WRITE REPORT-LINE
           
      *    Net positive/negative message
           IF WS-NET-SAVINGS-USD > 0
               MOVE "* You are NET POSITIVE - solar exceeds consumption"
                   TO REPORT-LINE
           ELSE
               MOVE "* You are consuming more than you generate"
                   TO REPORT-LINE
           END-IF
           WRITE REPORT-LINE
           
      *    Solar offset percentage
           MOVE SPACES TO REPORT-LINE
           MOVE WS-SOLAR-OFFSET-PCT TO WS-EDIT-PCT
           STRING "* Solar offsets " DELIMITED BY SIZE
                  WS-EDIT-PCT DELIMITED BY SIZE
                  "% of your energy needs" DELIMITED BY SIZE
                  INTO REPORT-LINE
           WRITE REPORT-LINE
           WRITE REPORT-LINE FROM SPACES
           
      *    Annual Value Analysis
           MOVE "Annual Value Analysis:" TO REPORT-LINE
           WRITE REPORT-LINE
           
           MOVE SPACES TO REPORT-LINE
           MOVE WS-PROJECTED-ANNUAL-USD TO WS-EDIT-USD-SMALL
           STRING "* Annual solar generation value: " DELIMITED BY SIZE
                  WS-EDIT-USD-SMALL DELIMITED BY SIZE
                  INTO REPORT-LINE
           WRITE REPORT-LINE
           
           MOVE "* Break-even timeline depends on system cost"
               TO REPORT-LINE
           WRITE REPORT-LINE
           
      *    Payback timelines
           MOVE SPACES TO REPORT-LINE
           MOVE WS-PAYBACK-1000 TO WS-EDIT-YEARS
           STRING "  - $1,000 system = " DELIMITED BY SIZE
                  WS-EDIT-YEARS DELIMITED BY SIZE
                  " years payback" DELIMITED BY SIZE
                  INTO REPORT-LINE
           WRITE REPORT-LINE
           
           MOVE SPACES TO REPORT-LINE
           MOVE WS-PAYBACK-2000 TO WS-EDIT-YEARS
           STRING "  - $2,000 system = " DELIMITED BY SIZE
                  WS-EDIT-YEARS DELIMITED BY SIZE
                  " years payback" DELIMITED BY SIZE
                  INTO REPORT-LINE
           WRITE REPORT-LINE
           
           MOVE SPACES TO REPORT-LINE
           MOVE WS-PAYBACK-3000 TO WS-EDIT-YEARS
           STRING "  - $3,000 system = " DELIMITED BY SIZE
                  WS-EDIT-YEARS DELIMITED BY SIZE
                  " years payback" DELIMITED BY SIZE
                  INTO REPORT-LINE
           WRITE REPORT-LINE
           WRITE REPORT-LINE FROM SPACES
           
      *    Recommendation
           IF WS-AVG-DAILY-SOLAR-KWH < 0.5
               MOVE "Recommendation: Your current solar output is LOW." 
                   TO REPORT-LINE
               WRITE REPORT-LINE
               MOVE "Consider expanding your solar array to" 
                   TO REPORT-LINE
               WRITE REPORT-LINE
               MOVE "maximize ROI and reduce grid dependence." 
                   TO REPORT-LINE
               WRITE REPORT-LINE
           ELSE
               MOVE "Recommendation: Strong solar performance." 
                   TO REPORT-LINE
               WRITE REPORT-LINE
               MOVE "Current capacity appears adequate for" 
                   TO REPORT-LINE
               WRITE REPORT-LINE
               MOVE "maximizing ROI and reducing grid dependence." 
                   TO REPORT-LINE
               WRITE REPORT-LINE
           END-IF
           WRITE REPORT-LINE FROM SPACES.
       
      *----------------------------------------------------------------*
      * PRINT FOOTER
      *----------------------------------------------------------------*
       460-PRINT-FOOTER.
           WRITE REPORT-LINE FROM WS-EQUALS-LINE.
       
      *----------------------------------------------------------------*
      * CLEANUP AND EXIT
      *----------------------------------------------------------------*
       900-CLEANUP-AND-EXIT.
           CLOSE CSV-INPUT-FILE
           CLOSE REPORT-OUTPUT-FILE
           DISPLAY "Program completed successfully".
