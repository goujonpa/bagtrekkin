GENDERS = (
    ('f', 'F'),
    ('m', 'M'),
)

EMPLOYEE_FUNCTIONS = (
    ('checkin', 'Check-In'),
    ('ramp', 'Ramp'),
    ('lostfounds', 'Lost and Founds'),
)

EMPLOYEE_STATUSES = (
    ('pending', 'Pending'),
    ('active', 'Active'),
    ('blocked', 'Blocked'),
)

LOG_STATUSES = (
    # Should be there, but not in reality
    ('fp', 'False Positive'),
    # Should not be there, but is in reality
    ('fn', 'False Negative'),
    # Should be there, and is in reality
    ('tp', 'True Positive')
)
