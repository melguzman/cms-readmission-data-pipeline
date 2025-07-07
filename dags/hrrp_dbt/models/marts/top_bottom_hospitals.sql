select
    *,
    rank() over (
        partition by fiscal_year
        order by avg_excess_readmission_ratio desc
    ) as penalty_rank
from {{ ref('hospital_penalties') }}