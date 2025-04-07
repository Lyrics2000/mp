 raw_sql_query = f"""/* Formatted on 12/18/2024 12:10:43 PM (QP5 v5.215.12089.38647) */
SELECT Policy_No,
       --   Product,
       --  Productcategory,
       Ni_Number,
       Client,
       Description,
       Premiumamount,
       NVL (Aplbalance, 0) Aplbalance,
       TotalArrears,
       NVL (Clientloanbalance, 0) Clientloanbalance,
       Lobsrc,
       CASE WHEN Clientloanbalance > 0 THEN CONCAT ('L', Policy_No) END
          AS PolicywithLoan
  FROM (  SELECT Policy.Policy_No,
                 Plan.Plan_Descn AS Product,
                 Plan.Plan_Cats AS Productcategory,
                 Person.Ni_Number,
                 person.FIRST_NAME || ' ' || person.SURNAME AS Client,
                 Descriptions_Tbl.Description,
                 Policy.Gross_Premium Premiumamount,
                 (  (Policy.Gross_Premium)
                  * ABS (CEIL (MONTHS_BETWEEN (Policy.Nx_Exp_Pr_Dt, SYSDATE))))
                    Arrears,
                 NVL (Aplbalance, 0) Aplbalance,
                 NVL (Clientloanbalance, 0) Clientloanbalance,
                 SUM (
                      NVL (Aplbalance, 0)
                    + NVL (
                         (  (Policy.Gross_Premium)
                          * ABS (
                               CEIL (
                                  MONTHS_BETWEEN (Policy.Nx_Exp_Pr_Dt, SYSDATE)))),
                         0))
                    TotalArrears,
                 --BAOWNER.get_policy_sum_assured (policy.policy_no) AS sum_assured,
                 'life' AS Lobsrc
            FROM Policy,
                 Pol_Per,
                 Person,
                 Descriptions_Tbl,
                 Plan,
                 (  SELECT Pol_Ref_No,
                           SUM ( (NVL (Pa_Postingdr, 0) - NVL (Pa_Postingcr, 0)))
                              Aplbalance
                      FROM Lo_Postings
                     WHERE Loan_Type = 'APL' AND Accountno = 24 AND Siteno = 4
                  GROUP BY Pol_Ref_No) L,
                 (  SELECT Pol_Ref_No,
                           SUM ( (NVL (Pa_Postingdr, 0) - NVL (Pa_Postingcr, 0)))
                              Clientloanbalance
                      FROM Lo_Postings
                     WHERE Loan_Type = 'POL' AND Accountno = 24 AND Siteno = 4
                  GROUP BY Pol_Ref_No) N
           WHERE     Policy.Pol_Ref_No = Pol_Per.Pol_Ref_No
                 AND Pol_Per.Per_Code = 'O'
                 AND Pol_Per.Perno = Person.Perno
                 AND Policy.Pol_Stat = Descriptions_Tbl.C_Code
                 AND Descriptions_Tbl.Name = 'status'
                 AND Policy.Planno = Plan.Planno
                 AND Policy.Pol_Ref_No = L.Pol_Ref_No(+)
                 AND Policy.Pol_Ref_No = N.Pol_Ref_No(+)
                 AND Policy.Siteno = Person.Siteno
                 AND Policy.Siteno = Pol_Per.Siteno
                 AND Policy.Siteno = Plan.Siteno
                 AND Policy.Pol_Stat = 'A'
        --AND person.ni_number = national_id_in;
        --AND Policy.Policy_No IN ('121-17605')
        GROUP BY Policy.Policy_No,
                 Plan.Plan_Descn,
                 Plan.Plan_Cats,
                 Person.Ni_Number,
                 person.FIRST_NAME || ' ' || person.SURNAME,
                 Descriptions_Tbl.Description,
                 Baowner.Get_Premium (Policy.Pol_Ref_No, Policy.Siteno),
                 Prem_Ac_Pkg.Fn_Policy_Arrears (4,
                                                Policy.Pol_Ref_No,
                                                Policy.Nx_Exp_Pr_Dt),
                 Policy.Gross_Premium,
                 Policy.Nx_Exp_Pr_Dt,
                 Aplbalance,
                 Clientloanbalance
        UNION
          SELECT Policy.Policy_No,
                 Plan.Plan_Descn AS Product,
                 Plan.Plan_Cats AS Productcategory,
                 Person.Ni_Number,
                 person.FIRST_NAME || ' ' || person.SURNAME AS Client,
                 Descriptions_Tbl.Description,
                 Policy.Gross_Premium Premiumamount,
                 -- CEIL (MONTHS_BETWEEN (POLICY.nx_exp_pr_dt, sysdate))prdbtwn,
                 (  (Policy.Gross_Premium)
                  * ABS (CEIL (MONTHS_BETWEEN (Policy.Nx_Exp_Pr_Dt, SYSDATE))))
                    Arrears,
                 NVL (Aplbalance, 0) Aplbalance,
                 NVL (Clientloanbalance, 0) Clientloanbalance,
                 SUM (
                      NVL (Aplbalance, 0)
                    + NVL (
                         (  (Policy.Gross_Premium)
                          * ABS (
                               CEIL (
                                  MONTHS_BETWEEN (Policy.Nx_Exp_Pr_Dt, SYSDATE)))),
                         0))
                    TotalArrears,
                 --BAOWNER.get_policy_sum_assured (policy.policy_no) AS sum_assured,
                 'life' AS Lobsrc
            FROM Policy,
                 Pol_Per,
                 Person,
                 Descriptions_Tbl,
                 Plan,
                 Pol_Endorsements,
                 (  SELECT Pol_Ref_No,
                           SUM ( (NVL (Pa_Postingdr, 0) - NVL (Pa_Postingcr, 0)))
                              Aplbalance
                      FROM Lo_Postings
                     WHERE Loan_Type = 'APL' AND Accountno = 24 AND Siteno = 4
                  GROUP BY Pol_Ref_No) L,
                 (  SELECT Pol_Ref_No,
                           SUM ( (NVL (Pa_Postingdr, 0) - NVL (Pa_Postingcr, 0)))
                              Clientloanbalance
                      FROM Lo_Postings
                     WHERE Loan_Type = 'POL' AND Accountno = 24 AND Siteno = 4
                  GROUP BY Pol_Ref_No) N
           WHERE     Policy.Pol_Ref_No = Pol_Per.Pol_Ref_No
                 AND Pol_Per.Per_Code = 'O'
                 AND Pol_Per.Perno = Person.Perno
                 AND Policy.Pol_Stat = Descriptions_Tbl.C_Code
                 AND Descriptions_Tbl.Name = 'status'
                 AND Policy.Planno = Plan.Planno
                 AND Policy.Pol_Ref_No = L.Pol_Ref_No(+)
                 AND Policy.Pol_Ref_No = N.Pol_Ref_No(+)
                 AND Policy.Pol_Ref_No = Pol_Endorsements.Pol_Ref_No
                 AND Policy.Siteno = Pol_Endorsements.Siteno
                 AND Policy.Siteno = Person.Siteno
                 AND Policy.Siteno = Pol_Per.Siteno
                 AND Policy.Siteno = Plan.Siteno
                 AND Policy.Pol_Stat = 'U'
                 AND Pol_Endorsements.Old_Value = 'Active'
                 AND Pol_Endorsements.New_Value = 'PaidUp'
                 AND Pol_Endorsements.Created_By = 'IGASJOB'
        --AND person.ni_number = national_id_in;
        --AND Policy.Policy_No IN ('139-3042', '161-22130')
        GROUP BY Policy.Policy_No,
                 Plan.Plan_Descn,
                 Plan.Plan_Cats,
                 Ni_Number,
                 person.FIRST_NAME || ' ' || person.SURNAME,
                 Descriptions_Tbl.Description,
                 Baowner.Get_Premium (Policy.Pol_Ref_No, Policy.Siteno),
                 Prem_Ac_Pkg.Fn_Policy_Arrears (4,
                                                Policy.Pol_Ref_No,
                                                Policy.Nx_Exp_Pr_Dt),
                 Aplbalance,
                 Clientloanbalance,
                 Policy.Gross_Premium,
                 Policy.Nx_Exp_Pr_Dt
        UNION
          SELECT Policy.Policy_No,
                 Plan.Plan_Descn AS Product,
                 Plan.Plan_Cats AS Productcategory,
                 Person.Ni_Number,
                 person.FIRST_NAME || ' ' || person.SURNAME AS Client,
                 Descriptions_Tbl.Description,
                 Policy.Gross_Premium Premiumamount,
                 -- CEIL (MONTHS_BETWEEN (POLICY.nx_exp_pr_dt, sysdate))prdbtwn,
                 (  (Policy.Gross_Premium)
                  * ABS (CEIL (MONTHS_BETWEEN (Policy.Nx_Exp_Pr_Dt, SYSDATE))))
                    Arrears,
                 NVL (Aplbalance, 0) Aplbalance,
                 NVL (Clientloanbalance, 0) Clientloanbalance,
                 SUM (
                      NVL (Aplbalance, 0)
                    + NVL (
                         (  (Policy.Gross_Premium)
                          * ABS (
                               CEIL (
                                  MONTHS_BETWEEN (Policy.Nx_Exp_Pr_Dt, SYSDATE)))),
                         0))
                    TotalArrears,
                 --BAOWNER.get_policy_sum_assured (policy.policy_no) AS sum_assured,
                 'life' AS Lobsrc
            FROM Policy,
                 Pol_Per,
                 Person,
                 Descriptions_Tbl,
                 Plan,
                 Pol_Endorsements,
                 (  SELECT Pol_Ref_No,
                           SUM ( (NVL (Pa_Postingdr, 0) - NVL (Pa_Postingcr, 0)))
                              Aplbalance
                      FROM Lo_Postings
                     WHERE Loan_Type = 'APL' AND Accountno = 24 AND Siteno = 4
                  GROUP BY Pol_Ref_No) L,
                 (  SELECT Pol_Ref_No,
                           SUM ( (NVL (Pa_Postingdr, 0) - NVL (Pa_Postingcr, 0)))
                              Clientloanbalance
                      FROM Lo_Postings
                     WHERE Loan_Type = 'POL' AND Accountno = 24 AND Siteno = 4
                  GROUP BY Pol_Ref_No) N
           WHERE     Policy.Pol_Ref_No = Pol_Per.Pol_Ref_No
                 AND Pol_Per.Per_Code = 'O'
                 AND Pol_Per.Perno = Person.Perno
                 AND Policy.Pol_Stat = Descriptions_Tbl.C_Code
                 AND Descriptions_Tbl.Name = 'status'
                 AND Policy.Planno = Plan.Planno
                 AND Policy.Pol_Ref_No = L.Pol_Ref_No(+)
                 AND Policy.Pol_Ref_No = N.Pol_Ref_No(+)
                 AND Policy.Pol_Ref_No = Pol_Endorsements.Pol_Ref_No
                 AND Policy.Siteno = Pol_Endorsements.Siteno
                 AND Policy.Siteno = Person.Siteno
                 AND Policy.Siteno = Pol_Per.Siteno
                 AND Policy.Siteno = Plan.Siteno
                 AND Policy.Pol_Stat = 'L'
                 AND Pol_Endorsements.Old_Value = 'Active'
                 AND Pol_Endorsements.New_Value = 'Lapsed'
                 AND TRUNC (Pol_Endorsements.Date_Created) >= SYSDATE - 365
        --AND Policy.Policy_No IN ('204-1890')
        --AND person.ni_number = national_id_in;
        GROUP BY Policy.Policy_No,
                 Plan.Plan_Descn,
                 Plan.Plan_Cats,
                 Person.Ni_Number,
                 person.FIRST_NAME || ' ' || person.SURNAME,
                 Descriptions_Tbl.Description,
                 Baowner.Get_Premium (Policy.Pol_Ref_No, Policy.Siteno),
                 Prem_Ac_Pkg.Fn_Policy_Arrears (4,
                                                Policy.Pol_Ref_No,
                                                Policy.Nx_Exp_Pr_Dt),
                 Aplbalance,
                 Clientloanbalance,
                 Policy.Gross_Premium,
                 Policy.Nx_Exp_Pr_Dt) T
 --where ni_number = national_id_in
 --  WHERE Ni_Number IN ()
 -- WHERE Policy_No IN ('430-4')
 WHERE Policy_No IN ('{id_number}'