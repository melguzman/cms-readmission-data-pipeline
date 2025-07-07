select
    facility_id,
    facility_name,
    state,
    measure_name,
    cast(substr(start_date, 1, 4) as integer) as fiscal_year,
    sum(number_of_discharges) as total_discharges,
    avg(excess_readmission_ratio) as avg_excess_readmission_ratio,
    avg(predicted_readmission_rate) as avg_predicted_rate,
    avg(expected_readmission_rate) as avg_expected_rate,
    sum(number_of_readmissions) as total_readmissions
from {{ ref('stg_hospital_readmissions') }}
group by
    facility_id,
    facility_name,
    state,
    measure_name,
    fiscal_year