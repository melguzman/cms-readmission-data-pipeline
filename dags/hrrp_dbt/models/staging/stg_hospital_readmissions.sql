{{ config(materialized='view', alias='stg_hospital_readmissions') }}

select
    facility_id,
    facility_name,
    state,
    measure_name,
    cast(nullif(number_of_discharges, 'N/A') as integer) as number_of_discharges,
    footnote,
    cast(nullif(excess_readmission_ratio, 'N/A') as float) as excess_readmission_ratio,
    cast(nullif(predicted_readmission_rate, 'N/A') as float) as predicted_readmission_rate,
    cast(nullif(expected_readmission_rate, 'N/A') as float) as expected_readmission_rate,
    cast(nullif(number_of_readmissions, 'N/A') as integer) as number_of_readmissions,
    date(
        substr(start_date, 7, 4) || '-' ||
        substr(start_date, 1, 2) || '-' ||
        substr(start_date, 4, 2)
    ) as start_date,
     date(
        substr(end_date, 7, 4) || '-' ||
        substr(end_date, 1, 2) || '-' ||
        substr(end_date, 4, 2)
    ) as end_date
from {{ source('hospital_readmissions_source', 'raw_hospital_readmissions') }}