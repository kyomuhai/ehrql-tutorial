# Welcome to the ehrQL Quiz!

from quiz_answers import questions

from ehrql import codelist_from_csv, show, months
from ehrql.tables.core import patients, practice_registrations, clinical_events, medications


diabetes_codes = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-dm_cod.csv", column="code"
)
referral_codes = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-dsep_cod.csv", column="code"
)
mild_frailty_codes = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-mildfrail_cod.csv", column="code"
)
moderate_frailty_codes = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-modfrail_cod.csv", column="code"
)
severe_frailty_codes = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-sevfrail_cod.csv", column="code"
)
hba1c_codes = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-ifcchbam_cod.csv", column="code"
)



# Question 0
# Create an event frame by filtering clinical_events to find just the records indicating a diabetes
# diagnosis. (Use the diabetes_codes codelist.)
questions[0].check(
    clinical_events.where(clinical_events.snomedct_code.is_in(diabetes_codes))
)



# Question 1
# Create a patient series containing the date of each patient's earliest diabetes diagnosis.
questions[1].check(clinical_events.where(clinical_events.snomedct_code.is_in(diabetes_codes))
     .sort_by(clinical_events.date)
     .first_for_patient()
     .date)
# If you need a hint for this, or any other, question, just uncomment (remove the #) from the following line:
# questions[1].hint()



# Question 2
# Create a patient series containing the date of each patient's earliest structured education
# programme referral. (Use the referral_code codelist.)
questions[2].check(clinical_events.where(clinical_events.snomedct_code.is_in(referral_codes))
    .sort_by(clinical_events.date)
    .first_for_patient()
    .date)
# questions[2].hint()



# Question 3
# Create a boolean patient series indicating whether the date of each patient's earliest diabetes
# diagnosis was between 1st April 2023 and 31st March 2024. If the patient does not have a
# diagnosis, the value for in this series should be False.
earliest_diabetes_diagnosis  = (clinical_events.where(clinical_events.snomedct_code.is_in(diabetes_codes))
     .sort_by(clinical_events.date)
     .first_for_patient()
     .date)

earliest_diabetes_diagnosis_in_year = (
    earliest_diabetes_diagnosis.is_on_or_after("2023-04-01")
    & earliest_diabetes_diagnosis.is_on_or_before("2024-03-31")
).when_null_then(False)

# show((earliest_diabetes_diagnosis.is_on_or_before("2024-03-31") & 
#      earliest_diabetes_diagnosis.is_on_or_after("2023-04-01")).when_null_then(False))
questions[3].check(earliest_diabetes_diagnosis_in_year)

#questions[3].hint()



# Question 4
# Create a patient series indicating the number of months between a patient's earliest diagnosis
# and their earliest referral.
earliest_diabetes_referral= (clinical_events.where(clinical_events.snomedct_code.is_in(referral_codes))
    .sort_by(clinical_events.date)
    .first_for_patient()
    .date)
diagnos_referral_diff = (earliest_diabetes_referral - earliest_diabetes_diagnosis).months
# show(diagnosit_referral_diff)
questions[4].check(diagnos_referral_diff)
#questions[4].hint()



# Question 5
# Create a boolean patient series identifying patients who have been diagnosed with diabetes for
# the first time in the year between 1st April 2023 and 31st March 2024, and who have a record of
# being referred to a structured education programme within nine months after their diagnosis.
referral_within_9_months = (
    (earliest_diabetes_referral.is_on_or_after(earliest_diabetes_diagnosis))
    & ((earliest_diabetes_referral - earliest_diabetes_diagnosis).months <= 9)
).when_null_then(False)
q5_patients = earliest_diabetes_diagnosis_in_year & referral_within_9_months
# show(q5_patients)
questions[5].check(q5_patients)
# questions[5].hint()



# Question 6
# Create a patient series with the date of the latest record of mild frailty for each patient.
last_record_mild_frail_date = (clinical_events.where(clinical_events.snomedct_code.is_in(mild_frailty_codes))
    .sort_by(clinical_events.date)
    .last_for_patient()
    .date)
questions[6].check(last_record_mild_frail_date)
# questions[6].hint()


# Question 7
# Create a patient series with the date of the latest record of moderate or severe frailty for
# each patient.
last_record_mod_sev_frail_date = (
    clinical_events
    .where(
        clinical_events.snomedct_code.is_in(moderate_frailty_codes) 
        | clinical_events.snomedct_code.is_in(severe_frailty_codes)
    )
    .sort_by(clinical_events.date)
    .last_for_patient()
    .date)

# show(last_record_mod_sev_frail_date)
questions[7].check(last_record_mod_sev_frail_date)
# questions[7].hint()



# Question 8
# A patient may have mild, moderate and severe frailty codes in their record. A patient's frailty
# is considered to be their most recent frailty code. So if their most recent frailty code was for
# mild frailty, then we would say they have mild frailty.
# Create a boolean patient series indicating whether a patient has moderate or severe frailty, i.e
# where the patient's last record of severity is moderate or severe. If the patient does not have
# a record of frailty, the value in this series should be False.
has_mod_or_sev_frail = (
    last_record_mod_sev_frail_date.is_not_null()
    & (
        last_record_mild_frail_date.is_null()
        | (last_record_mod_sev_frail_date.is_after(last_record_mild_frail_date))
    )
)

# show(has_mod_or_sev_frail)
questions[8].check(has_mod_or_sev_frail)
# # questions[8].hint()





# Question 9
# Create a patient series containing the latest HbA1c measurement for each patient.
latest_haem_measurement = (
    clinical_events
    .where(
        clinical_events.snomedct_code.is_in(hba1c_codes))
    .sort_by(clinical_events.date)
    .last_for_patient()
    .numeric_value
)

# show(latest_haem_measurement)

questions[9].check(latest_haem_measurement)
# # questions[9].hint()



# Question 10
# Create a boolean patient series identifying patients without moderate or severe frailty in whom
# the last IFCC-HbA1c is 58 mmol/mol or less


haem_58_or_less = latest_haem_measurement.is_not_null() & (latest_haem_measurement <= 58)

q10 = has_mod_or_sev_frail.is_null() & haem_58_or_less
questions[10].check(q10)




questions.summarise()
