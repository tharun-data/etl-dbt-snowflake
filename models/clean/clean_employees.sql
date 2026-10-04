with src as (
    select * from {{ source('raw', 'employees_raw') }}
)
select
    try_to_number(trim(emp_id)) as emp_id,
    trim(first_name) as first_name,
    trim(last_name) as last_name,
    upper(trim(department)) as department,
    try_to_decimal(trim(salary), 12, 2) as salary,
    try_to_date(trim(hire_date)) as hire_date,
    current_timestamp()::timestamp_ntz as load_ts
from src
where try_to_number(trim(emp_id)) is not null
  and try_to_decimal(trim(salary), 12, 2) is not null
  and try_to_date(trim(hire_date)) is not null
qualify row_number() over (
    partition by try_to_number(trim(emp_id))
    order by hire_date desc
) = 1

