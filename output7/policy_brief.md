# Policy Brief

**Question:** What is the evidence on algorithmic benefit-eligibility tools and racial equity?

---

I could not call a `write_brief` tool because none is available in this session, so the brief is below. I ran 6 searches and read 2 full pages, and the rest of the evidence comes from search snippets. Notes are saved.

## Policy Brief: Algorithmic Benefit-Eligibility Tools and Racial Equity

**Executive summary.** Direct evidence on how algorithmic benefit-eligibility tools affect racial groups is thin. The best-documented cases show serious harm from these tools, including due process violations and wrongful cuts, but the sources I found do not report racial breakdowns of those harms. Stronger evidence on racial bias comes from adjacent health risk-prediction algorithms, which use cost or utilization as a proxy for need. Policymakers should treat racial equity as an unverified risk that requires explicit auditing, not as a settled finding either way.

### Key findings

- **Proxy-variable bias is documented in a major health algorithm.** Obermeyer et al. (*Science*, 2019) studied a widely used commercial risk-prediction algorithm that affected roughly 200 million people in the US. At a given risk score, Black patients were considerably sicker than White patients, with signs of more uncontrolled illness. The likely mechanism was using health costs as a stand-in for health needs, which encodes unequal access to care. Sources: https://www.science.org/doi/10.1126/science.aax2342 ; https://www.scientificamerican.com/article/racial-bias-found-in-a-major-health-care-risk-algorithm/ . This is a care-management tool, not an eligibility tool, so it is an analogy rather than direct evidence.

- **Arkansas Medicaid home-care algorithm caused mass cuts and due process failures.** In 2016, nearly half of beneficiaries in Arkansas's HCBS program experienced sudden, large care reductions after the state adopted the RUGs algorithm. Litigation found the algorithm assigned insufficient hours at all levels of need and omitted some medical conditions, which caused miscalculations for hundreds of people. A federal court found due process violations, and a state court later invalidated the algorithm on rulemaking grounds. Source: https://www.btah.org/case-study/arkansas-medicaid-home-and-community-based-services-hours-cuts.html

- **Replacement systems produced similar problems.** Arkansas's successor system (the ARIA assessment, developed by Optum, plus a time-task tool and budget caps) left over a quarter of participants wholly ineligible. The state again failed to continue benefits during appeals and to explain cuts. Plaintiffs won a settlement of roughly $460,000 to $500,000 in 2023. Sources: https://www.btah.org/case-study/arkansas-medicaid-home-and-community-based-services-hours-cuts.html ; https://arlegalaid.org/news-events/newsroom.html/article/2023/08/09/arkansas-dhs-agrees-to-pay-460-000-to-settle-case-over-in-home-care-cuts . Neither source reports outcomes by race.

- **Systematic review evidence exists but I could only read its scope.** AHRQ Comparative Effectiveness Review No. 268 (Dec 2023) synthesized 2011–2023 literature on whether healthcare algorithms widen or narrow racial and ethnic disparities, and on mitigation strategies. It screened 11,500 records and used an equity-specific risk-of-bias appraisal. I read only the abstract, so I cannot report its conclusions. Source: https://ncbi.nlm.nih.gov/sites/books/NBK598802/

- **Baseline racial disparities in the programs themselves are documented.** A study of dual-eligible people with MS found racial disparities in Medicaid HCBS case management, equipment, nursing services, and expenditures between Black and White beneficiaries. This shows that disparities exist before any algorithm is applied, so algorithms can inherit or amplify them. Source: https://pmc.ncbi.nlm.nih.gov/articles/PMC6186063/

### Policy implications

1. **Require disparity audits before and after deployment.** Agencies should test eligibility and assessment tools for differential error rates and outcomes by race and ethnicity, using accurate race data. Medicaid administrative data often has incomplete race fields (see https://www.kff.org/medicaid/medicaid-administrative-data-challenges-with-race-ethnicity-and-other-demographic-variables/), so collecting that data is a precondition for auditing.
2. **Build due process into automated decisions.** The Arkansas cases show that adverse actions taken by an algorithm must come with continued benefits during appeal, clear reasons, and the ability to challenge the logic. Those protections also make bias easier to detect.
3. **Avoid cost or utilization as proxies for need without validation.** The Obermeyer finding suggests that proxies tied to past spending can reproduce unequal access. Agencies should validate that the outcome variable measures need and not access.

### Evidence gaps

- **No direct racial-impact studies of benefit-eligibility algorithms.** I found no study that reports racial outcomes for the Arkansas RUGs or ARIA systems, or for similar tools elsewhere.
- **AHRQ review findings not read.** Its full synthesis may answer part of this question, and I recommend reading it before relying on this brief.
- **Other well-known cases not researched.** I did not check automated systems in unemployment insurance, SNAP, or child welfare benefit programs, where racial impacts have been reported in the press. These need verification before being cited.
- **Medicaid HCBS disparity research predates current tools.** The race-disparity evidence I found is not tied to specific algorithms.
