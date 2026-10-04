select
    department,
    count(*) as emp_count,
    avg(salary) as avg_salary,
    max(salary) as max_salary
from {{ ref('clean_employees') }}
group by department
