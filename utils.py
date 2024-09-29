def try_correction(Code_Corrector_Agent, tester, output, nb_try):
    counter = 0
    error_state = 1
    while counter < nb_try and error_state == 1:
        print(f"{counter+2} try")
        corrected_code = Code_Corrector_Agent({"code": tester.code, "error": output["stderr"]})
        output = tester.exec_code(corrected_code)
        error_state = output["return_code"]
        counter += 1
    return error_state
