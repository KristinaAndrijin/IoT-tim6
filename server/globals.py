dms_pin = "ABCD"
security_system_active = False
code_correct = False
dms_alarm_raised = False
rpir_alarm_raised = False


def get_pin():
    return dms_pin


def set_pin(value):
    global dms_pin
    dms_pin = value


def is_security_system_active():
    return security_system_active


def set_security_system_activated(value):
    global security_system_active
    security_system_active = value


def is_code_correct():
    return code_correct


def set_code_correct(value):
    global code_correct
    code_correct = value


def check_code(inputted_pin):
    set_code_correct(inputted_pin == dms_pin)


def is_dms_alarm_raised():
    return dms_alarm_raised


def set_dms_is_alarm_raised(value):
    global dms_alarm_raised
    dms_alarm_raised = value


def is_rpir_alarm_raised():
    return rpir_alarm_raised


def set_rpir_alarm_raised(value):
    global rpir_alarm_raised
    rpir_alarm_raised = value
