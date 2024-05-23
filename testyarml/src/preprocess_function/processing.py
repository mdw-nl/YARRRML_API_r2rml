from morph_kgc.fnml import built_in_functions


@udf(
    fun_id='http://www.example.com/LowerCase',
    code='http://users.ugent.be/~bjdmeest/function/grel.ttl#valueParam')
def LowerCase(code):
    """

    :return:
    :param code:
    :return:
    """
    return code.lower()


@udf(
    fun_id='http://www.example.com/FloatToBool',
    code='http://users.ugent.be/~bjdmeest/function/grel.ttl#valueParam')
def FloatToBool(code):
    """

    :return:
    :param code:
    :return:
    """
    if code == "1.0" or code == "1" or code == 1 or code == 1.0:
        return "True"
    elif code == "0.0" or code == "0" or code == 0 or code == 0.0:
        return "False"
    else:
        return code

@udf(
    fun_id='http://www.example.com/YNtoBool',
    code='http://users.ugent.be/~bjdmeest/function/grel.ttl#valueParam')
def YNtoBool(code):
    """

    :return:
    :param code:
    :return:
    """
    if code == "YES" or code == "yes" or code == "Yes":
        return "True"
    elif code == "NO" or code == "no" or code == "No":
        return "False"
    else:
        return None
