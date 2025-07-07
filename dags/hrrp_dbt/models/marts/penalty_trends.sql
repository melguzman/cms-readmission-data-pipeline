select
    state,
    fiscal_year,
    sum(total_discharges) as total_discharges,
    avg(avg_excess_readmission_ratio) as avg_excess_ratio,
    sum(total_readmissions) as total_readmissions
from {{ ref('hospital_penalties') }}
group by state, fiscal_year