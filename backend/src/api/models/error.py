no_data_provided = {
    "error": "no_data_provided",
    "message": "No data provided",
    "status": 401,
}

no_username_provided = {
    "error": "no_username_provided",
    "message": "No username provided",
    "status": 401,
}

no_password_provided = {
    "error": "no_password_provided",
    "message": "No password provided",
    "status": 401,
}

no_experiment_provided = {
    "error": "no_experiment_provided",
    "message": "No experiment provided",
    "status": 401,
}


invalid_password = {
    "error": "invalid_password",
    "message": "User with provided credentials does not exist or password not valid",
    "status": 401,
}
invalid_username = {
    "error": "invalid_username",
    "message": "User with provided credentials does not exist or password not valid",
    "status": 401,
}

provided_credentials_wrong = {
    "error": "provided_credentials_wrong",
    "message": "User with provided credentials does not exist",
    "status": 401,
}

username_already_taken = {
    "error": "username_already_taken",
    "message": "User with provided username already exists",
    "status": 409,
}

token_not_provided = {
    "error": "token_not_provided",
    "message": "The provided token is not linked to any User or no token provided",
    "status": 401,
}

token_not_linked = {
    "error": "token_not_linked",
    "message": "The provided token is not linked to any User or no token provided",
    "status": 401,
}

dataset_not_valid = {
    "error": "dataset_not_valid",
    "message": "Provided dataset is not valid",
    "status": 422,
}

ground_truth_not_valid = {
    "error": "ground_truth_not_valid",
    "message": "Provided ground-truth is not valid",
    "status": 422,
}

no_experiment_with_id = {
    "error": "no_experiment_with_id",
    "message": "No experiment exists with provided id",
    "status": 404,
}

no_create_experiment_data_provided = {
    "error": "no_experiment_with_id",
    "message": "No create experiment data provided - for this use key experiment",
    "status": 422,
}

create_experiment_data_not_valid = {
    "error": "create_experiment_data_not_valid",
    "message": "Data passed for create experiment is not valid",
    "status": 422,
}

error_other = {
    "error": "error_other",
    "message": "Something went wrong",
    "status": 400,
}

no_odm_with_id = {
    "error": "no_odm_with_id",
    "message": "No ODM exists with provided id",
    "status": 404,
}
