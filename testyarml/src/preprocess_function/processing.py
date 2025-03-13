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
    if code:
        return code.lower()
    return None


@udf(
    fun_id='http://www.example.com/FloatToBool',
    code='http://users.ugent.be/~bjdmeest/function/grel.ttl#valueParam')
def FloatToBool(code):
    """

    :return:
    :param code:
    :return:
    """
    if code:
        if code == "1.0" or code == "1" or code == 1 or code == 1.0:
            return "True"
        elif code == "0.0" or code == "0" or code == 0 or code == 0.0:
            return "False"
        else:
            return code
    else:
        return None

@udf(
    fun_id='http://www.example.com/YNtoBool',
    code='http://users.ugent.be/~bjdmeest/function/grel.ttl#valueParam')
def YNtoBool(code):
    """

    :return:
    :param code:
    :return:
    """
    if code:
        if code == "YES" or code == "yes" or code == "Yes" or code == "Ja" or code == "JA" or code == "ja":
            return "True"
        elif code == "NO" or code == "no" or code == "No" or code == "Nee" or code == "NEE" or code == "nee":
            return "False"
        else:
            return None
    else:
        return None

@udf(
    fun_id='http://www.example.com/YNtoBoolNoNull',
    code='http://users.ugent.be/~bjdmeest/function/grel.ttl#valueParam')
def YNtoBoolNoNull(code):
    """

    :return:
    :param code:
    :return:
    """
    if code:
        if code == "YES" or code == "yes" or code == "Yes":
            return "True"
        elif code == "NO" or code == "no" or code == "No":
            return "False"
        else:
            return "False"
    else:
        return "False"
